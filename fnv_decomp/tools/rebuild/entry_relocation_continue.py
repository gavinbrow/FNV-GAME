"""Reuse four terminal proofs; compile only the two remaining fixed overlay TUs."""
import argparse
import json
import os
from pathlib import Path
import re
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
import entry_relocation_batch as batch
import literal_symbol_migration as literal
from coff_inventory import Coff, peak_memory_bytes
from data_plan import Pe, file_hash
from import_plan import ImagePe, image_ok, require
from compare import Coff as CompareCoff, compare as plain_compare
import toolchain

ROOT=batch.ROOT
POLICY=ROOT/'runtime/source-overlays/entry-nineteen-continuation.json'
POLICY_SHA='76ce3b2b8bfe92ea5ca138006adf8a08e7c55a110211b44648d9923d9a0a38e4'
HELPER_SHA='65ea3e7e97ecbbab5768e8e40eecc235f1415ac5ce4a2d956597a1f7b3206b11'
PREVIOUS=ROOT/'build/rebuild/entry-relocation-batch-native-v1'
PREVIEW=ROOT/'build/rebuild/entry-relocation-literal-preview-v1.json'


def policy():return batch.frozen.read_bound(POLICY,POLICY_SHA)


def cached_units(previous, p):
    require(previous['status'] == 'error' and [u['recipe_index'] for u in previous['units']] == p['reused_recipe_indices'], 'previous terminal unit set differs')
    require(sum(u['plain_comparison_rows'] for u in previous['units']) == p['reused_original_rows'], 'cached row census differs')
    require(sum(u['migration']['repaired_count'] for u in previous['units']) == 11, 'cached repair census differs')
    return previous['units']


def final_census(units):
    require([u['recipe_index'] for u in units] == [213,214,272,870,2709,2757], 'continuation unit coverage differs')
    require(sum(u['plain_comparison_rows'] for u in units) == 619 and
            sum(u['migration']['repaired_count'] for u in units) == 19, 'combined row/repair census differs')
    require([u['recipe_index'] for u in units if u['operation'] == 'compiled_v2'] == [2709,2757], 'compiled continuation scope differs')


def stability(observations):
    return all(file_hash(path) == pin for path,pin in observations.items())


def run(args):
    require(os.name == 'nt' and args.compile_only is True,'explicit Windows compile-only operation required')
    started=time.monotonic();p=policy();specs=batch.policy()['units']
    require(file_hash(__file__) == args.implementation_sha256,'reviewed continuation implementation differs')
    observations={Path(__file__).resolve():args.implementation_sha256,POLICY:POLICY_SHA,
        ROOT/'tools/rebuild/literal_symbol_migration.py':HELPER_SHA,
        ROOT/'tools/rebuild/entry_relocation_batch.py':p['batch_tool_sha256'],
        batch.POLICY:p['batch_policy_sha256'],PREVIEW:p['literal_preview_sha256'],
        PREVIOUS/'result.json':p['first_result_sha256'],PREVIOUS/'failure-reconciliation.json':p['failure_reconciliation_sha256']}
    previous=batch.frozen.read_bound(PREVIOUS/'result.json',p['first_result_sha256'])
    reconciliation=batch.frozen.read_bound(PREVIOUS/'failure-reconciliation.json',p['failure_reconciliation_sha256'])
    require(reconciliation['all_protected_inputs_unchanged'] and reconciliation['all_completed_unit_artifacts_unchanged'] and
            len(reconciliation['protected_inputs']) == 64 and len(reconciliation['completed_unit_artifacts']) == 28,'saved failure reconciliation incomplete')
    ancestry_path=PREVIOUS/'original-ancestry.json';observations[ancestry_path]=reconciliation['original_ancestry_sha256']
    ancestry=batch.frozen.read_bound(ancestry_path,observations[ancestry_path])
    observations.update({Path(path):pin for path,pin in ancestry['inputs'].items()})
    cached=cached_units(previous,p)
    progress=[json.loads(line) for line in (PREVIOUS/'progress.jsonl').read_text().splitlines()]
    require([r['recipe_id'] for r in progress if r['state'] == 'compile_started'] == [s['recipe_id'] for s in specs[:5]],'previous attempt scope differs')
    observations[PREVIOUS/'progress.jsonl']=file_hash(PREVIOUS/'progress.jsonl')
    recipes=batch.frozen.read_bound(batch.frozen.DEFAULTS['recipes'],batch.frozen.PINS['recipes'])
    manifest=batch.frozen.read_bound(batch.frozen.DEFAULTS['manifest'],batch.frozen.PINS['manifest'])
    selection=batch.frozen.read_bound(batch.frozen.DEFAULTS['selection'],batch.frozen.PINS['selection'])
    for old in cached:
        spec=next(s for s in specs if s['recipe_index'] == old['recipe_index']);folder=PREVIOUS/old['recipe_id']
        for name,pin in old['artifacts'].items():observations[folder/name]=pin
        comparison=json.loads((folder/'comparison.json').read_text())['rows']
        batch.complete_matches(comparison,recipes['units'][old['recipe_index']],spec['owners'])
        require(batch.sha(batch.transform((ROOT/spec['source']).read_bytes(),spec)) == old['lane']['generated_source_sha256'], 'cached generated source/context differs')
    for row in reconciliation['protected_inputs']+reconciliation['completed_unit_artifacts']:
        require(row['equal'] and row['expected'] == row['actual'],'reconciliation contains failed observation')
    reference=Path(args.reference).resolve();require(file_hash(reference) == batch.frozen.PINS['reference'],'owned reference differs')
    doctor=Path(args.doctor).resolve();tc=json.loads(doctor.read_text())['toolchains']['sp1'];compiler_root,_=toolchain.layout(tc['root']);cl=compiler_root/'VC/bin/cl.exe'
    require(doctor in observations and observations[doctor] == file_hash(doctor) and tc['ready'] and tc['version'] == '15.00.30729.01' and
            tc['cl_sha256'] == file_hash(cl) == manifest['toolchains']['sp1']['cl_sha256'],'compiler/doctor context differs')
    require(stability(observations),'protected/cached inputs changed')
    out=batch.frozen.new_output(args.out,observations);out.mkdir(parents=True)
    def note(state,**fields):
        with (out/'progress.jsonl').open('a',encoding='utf-8') as stream:
            stream.write(json.dumps(dict(state=state,**fields))+'\n');stream.flush();os.fsync(stream.fileno())
    note('started',reused_recipes=p['reused_recipe_indices'],compile_recipes=p['compiled_recipe_indices'])
    report=dict(kind='fnv-entry-nineteen-continuation-result',status='error',inputs={str(k):v for k,v in observations.items()},
        original_result_sha256=p['first_result_sha256'],units=[dict(u,operation='reused_v1_verified_terminal',artifact_root=str(PREVIOUS/u['recipe_id'])) for u in cached],
        new_compile_count=0,game_execution=False,link_performed=False,provider_selected=False,runtime_eligible=False,runtime_closure_verified=False)
    batch.frozen.save(out/'original-ancestry.json',dict(original_ancestry_path=str(ancestry_path),original_ancestry_sha256=observations[ancestry_path],
        original_failed_attempt_sha256=p['first_result_sha256'],original_protected_inputs=ancestry['inputs'],reused_terminal_recipes=p['reused_recipe_indices']))
    try:
        image=ImagePe(reference);ok,hits,probes=image_ok(image);require(ok,'original image probes failed');pe=Pe(reference)
        try:
            highlows=sorted(pe.base+r for r in pe.relocations())
            for idx in p['compiled_recipe_indices']:
                require(time.monotonic()-started < 600,'continuation wall limit exceeded')
                spec=next(s for s in specs if s['recipe_index'] == idx);unit=manifest['units'][idx];recipe=unit['recipe']
                original=(batch.frozen.DEFAULTS['manifest'].parent/manifest.get('object_root_relative','.')/unit['object']).resolve()
                generated=batch.transform((ROOT/spec['source']).read_bytes(),spec)
                folder=out/spec['recipe_id'];folder.mkdir();source=folder/Path(spec['source']).name;obj=folder/'overlay.obj'
                with source.open('xb') as stream:stream.write(generated)
                require(stability(observations) and file_hash(source) == batch.sha(generated),'inputs changed before compile')
                command=[cl,'/c','/nologo']+recipe['flags']+['/I'+str((ROOT/spec['source']).parent),'/I'+str(ROOT/'include'),'/showIncludes',source,'/Fo'+str(obj)]
                note('compile_started',recipe_id=spec['recipe_id']);report['new_compile_count']+=1
                code,text=toolchain.run(command,compiler_root,ROOT,timeout=min(120,max(1,int(600-(time.monotonic()-started)))))
                with (folder/'compile.log').open('x',encoding='utf-8') as stream:stream.write(text)
                require(code == 0 and obj.is_file(),'continuation compile failed')
                obj_hash=file_hash(obj);batch.frozen.generated_stability(source,obj,batch.sha(generated),obj_hash)
                includes=[Path(x.strip()).resolve() for x in re.findall(r'(?im)^Note: including file:\s*(.+)$',text)]
                allowed={((ROOT if h['kind'] == 'source' else compiler_root)/h['path']).resolve() for h in spec['headers']}
                require(set(includes) <= allowed and bool(includes),'include origin outside fixed closure')
                before,after=Coff(original),Coff(obj);require(batch.sha(after.data) == obj_hash,'generated object drift')
                geometry=[batch.verify_owner(before,after,o,recipe) for o in spec['owners']]
                adapted,supplement=literal.supplement(before,after,recipe,pe,highlows)
                supplement.update(original_object_sha256=unit['object_sha256'],overlay_object_sha256=obj_hash,
                    original_recipe_sha256=batch.sha(json.dumps(recipe,sort_keys=True,separators=(',',':')).encode()),
                    alternate_resolver_recipe_sha256=batch.sha(json.dumps(adapted,sort_keys=True,separators=(',',':')).encode()),helper_sha256=HELPER_SHA)
                batch.frozen.save(folder/'literal-supplement.json',supplement)
                batch.frozen.save(folder/'alternate-resolver-recipe.json',adapted)
                comparable=CompareCoff(obj);require(batch.sha(comparable.data) == obj_hash,'object drift before comparison')
                rows=plain_compare(comparable,image,adapted)
                sanitized=[{k:v for k,v in r.items() if k != 'byte_differences'} | dict(byte_difference_offsets=[d['offset'] for d in r['byte_differences']]) for r in rows]
                batch.frozen.save(folder/'comparison.json',dict(rows=sanitized,original_recipe_rows_unchanged=True,literal_supplement_sha256=file_hash(folder/'literal-supplement.json')))
                batch.complete_matches(rows,recipe,spec['owners'])
                oldrows,oldcounts,_=batch.source_bound_rows(before,unit,pe,highlows,selection)
                newrows,newcounts,functions=batch.source_bound_rows(after,dict(unit,recipe=adapted),pe,highlows,selection)
                migration=batch.migrations_match(oldrows,newrows,spec)
                lane=dict(original_object_sha256=unit['object_sha256'],overlay_object_sha256=obj_hash,original_source_sha256=spec['source_sha256'],generated_source_sha256=batch.sha(generated),literal_supplement_sha256=file_hash(folder/'literal-supplement.json'))
                for row in newrows:row.update(overlay_lane=lane,producer_sha256=args.implementation_sha256)
                batch.save_gzip(folder/'source-bindings.jsonl.gz',newrows)
                batch.frozen.save(folder/'native-inventory.json',dict(object_sha256=obj_hash,**batch.inventory(after),all_physical_fields=[dict(section=s['index'],**batch.relocation_record(after,s,r)) for s in after.sections.values() for r in s['relocs']]))
                batch.frozen.save(folder/'migration.json',dict(lane=lane,geometry=geometry,census=migration,original_highlow_partition=oldcounts,overlay_highlow_partition=newcounts,original_global_missing_census_unchanged=88,original_entry_missing_census_unchanged=47))
                batch.frozen.generated_stability(source,obj,batch.sha(generated),obj_hash)
                names=[source.name,'overlay.obj','comparison.json','literal-supplement.json','alternate-resolver-recipe.json','source-bindings.jsonl.gz','native-inventory.json','migration.json','compile.log']
                artifacts={name:file_hash(folder/name) for name in names}
                report['units'].append(dict(recipe_id=spec['recipe_id'],recipe_index=idx,operation='compiled_v2',artifact_root=str(folder),lane=lane,actual_includes=[str(q) for q in includes],flags=recipe['flags'],plain_comparison_rows=len(rows),fresh_verified_functions=functions,migration=migration,artifacts=artifacts))
                note('unit_verified',recipe_id=spec['recipe_id'],object_sha256=obj_hash)
                require((peak_memory_bytes() or 0) <= 1024**3,'observer memory limit exceeded')
                require(sum(f.stat().st_size for f in out.rglob('*') if f.is_file()) <= 100*1024**2,'private output limit exceeded')
        finally:pe.close()
        del image;final_census(report['units']);require(report['new_compile_count'] == 2,'continuation compile count differs')
        require(stability(observations),'protected/cached input drift at completion')
        for unit in report['units']:
            require(all(file_hash(Path(unit['artifact_root'])/name) == pin for name,pin in unit['artifacts'].items()),'generated/reused artifact drift')
        manifest_out=dict(schema_version=2,kind='fnv-runtime-source-overlay-manifest',policy_sha256=POLICY_SHA,producer_sha256=args.implementation_sha256,
            original_ancestry_sha256=file_hash(out/'original-ancestry.json'),units=report['units'],new_compile_count=2,reused_terminal_unit_count=4,
            combined_original_function_rows=619,original_global_missing_census_unchanged=88,original_entry_missing_census_unchanged=47,
            alternate_owner_selection_performed=False,provider_selected=False,runtime_eligible=False,link_ready=False,runtime_closure_verified=False)
        batch.frozen.save(out/'runtime-overlays.json',manifest_out)
        report.update(status='pass_pending_independent_review',runtime_overlays_sha256=file_hash(out/'runtime-overlays.json'),generated_artifacts_stability_verified=True,image_gate=dict(hits=hits,probes=probes))
        note('verified_pending_review')
    except Exception as error:
        report['error']=str(error);note('failed',error_type=type(error).__name__)
    # A failed operation still gets an explicit terminal protected-input recheck.
    try:report['input_stability_verified']=stability(observations)
    except OSError:report['input_stability_verified']=False
    if not report['input_stability_verified']:report.update(status='error',error='protected input drift at terminal recheck')
    report.update(elapsed_seconds=time.monotonic()-started,observer_peak_memory_bytes=peak_memory_bytes(),compiler_child_peak_memory_measured=False)
    batch.frozen.save(out/'result.json',report)
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--compile-only',action='store_true',required=True)
    parser.add_argument('--implementation-sha256',required=True)
    for name in ('reference','doctor','out'):parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args()
    try:result=run(args)
    except (ValueError,OSError,KeyError,TypeError) as error:parser.exit(2,'continuation rejected: '+str(error)+'\n')
    print(result['status']);return 0 if result['status'] == 'pass_pending_independent_review' else 1


if __name__=='__main__':raise SystemExit(main())
