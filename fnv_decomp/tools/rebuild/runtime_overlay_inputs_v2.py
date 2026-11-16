"""Overlay registry v2 with one positively proved local-label bookkeeping change."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
import entry_relocation_batch as batch
import entry_relocation_repair as first
import literal_symbol_migration as literal
import local_label_symbol_migration as local_labels
from coff_inventory import Coff
from data_plan import Pe, file_hash
from import_plan import ImagePe, image_ok, require
from compare import Coff as CompareCoff, compare as plain_compare

ROOT=batch.ROOT
POLICY=ROOT/'runtime/source-overlays/accepted-runtime-owner-selection.json'
POLICY_SHA='e879edf4f4ec4f8a2882972273c5858616cd6507d57e20a635dcd9cdd43aa72e'
LABEL_POLICY=ROOT/'runtime/source-overlays/runtime-overlay-local-label-v2.json'
LABEL_POLICY_SHA='fff7fb02caf4376530e09987d98667e977e08a9994734bd48b64a9078a0f3ac1'
LABEL_HELPER_SHA='953596af238d98ced52f6f92f83bc739054bd8105a6bcf50a8e32aa62da59b64'
INPUT_PINS={
 'build/rebuild/absolute-triage-evidence-v1.json':'4e06af226997152e1a7097e93f3b96d92804b229f97139dd21c89e249c6f5a28',
 'build/rebuild/entry-dependencies-next-projects-v1.json':'eca726d106f800b023c831280c7f2ce7eb3d448a00a570f827dcd264d7dfc803'}


def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def identity(value):return hashlib.sha256(canonical(value)).hexdigest()
def policy():return batch.frozen.read_bound(POLICY,POLICY_SHA)


def normalize_fields(oldrefs,newrefs,fields,aliases):
    old=[r['semantic'] for r in oldrefs];new=[]
    wanted={f['offset']:f for f in fields}
    seen=set()
    for ref in newrefs:
        semantic=json.loads(json.dumps(ref['semantic']));off=semantic['offset']
        if off in wanted:
            f=wanted[off]
            require(off not in seen and semantic['kind'] == 6 and semantic['addend'] == 0 and
                    semantic['target']['name'] == f['symbol'],'approved repair field differs')
            seen.add(off);continue
        semantic['target']['name']=aliases.get(semantic['target']['name'],semantic['target']['name'])
        new.append(semantic)
    require(seen == set(wanted),'approved repair field absent')
    # Actual section identities remain in the native ledger; names, values,
    # kinds/addends/type/linkage must agree and all fresh targets are PE-joined.
    strip=lambda refs:[dict(r,target={k:v for k,v in r['target'].items() if k != 'section'}) for r in refs]
    require(strip(old) == strip(new),'unaffected physical reference/namespace changed')


def function_scope(before,after,recipe,requests,supplement):
    by_address={o['address']:o for o in requests}
    require(len(by_address) == len(requests),'duplicate requested owner')
    aliases={w['new_name']:w['old_name'] for w in supplement['witnesses']}
    rows=[]
    for f in recipe['functions']:
        old,oldrefs,oldnative=batch.snapshot(before,f['symbol'],f['size'])
        new,newrefs,newnative=batch.snapshot(after,f['symbol'],f['size'])
        request=by_address.get(f['address']);fields=request['fields'] if request else []
        if request:require(request['selection']['symbol'] == f['symbol'] and request['selection']['size'] == f['size'],'requested recipe owner differs')
        mask={i for field in fields for i in range(field['offset'],field['offset']+4)}
        require(len(old) == len(new) == f['size'] and all(a == b for i,(a,b) in enumerate(zip(old,new)) if i not in mask),'unaffected function bytes changed')
        for field in fields:
            require(int.from_bytes(old[field['offset']:field['offset']+4],'little') == int(field['target'],16),'original repair operand differs')
            require(not any(r['semantic']['offset'] < field['offset']+4 and r['semantic']['offset']+4 > field['offset'] for r in oldrefs),'original field not missing')
            refs=[r['semantic'] for r in newrefs if r['semantic']['offset'] == field['offset']]
            require(len(refs) == 1,'new repair physical field ambiguous')
            target=refs[0]['target'];require(target['storage'] == 2 and target['aux_count'] == 0,'new repair target linkage differs')
            code=[f for f in recipe['functions'] if f['symbol'] == field['symbol']]
            if code:
                require(len(code) == 1 and code[0]['address'] == field['target'] and target['section'] > 0 and target['type'] == 32,'repair code identity differs')
            else:
                require(recipe['symbols'].get(field['symbol']) == field['target'] and target['section'] == target['value'] == target['type'] == 0,'repair undefined carrier differs')
        normalize_fields(oldrefs,newrefs,fields,aliases)
        rows.append(dict(address=f['address'],symbol=f['symbol'],size=f['size'],original_native=oldnative,
            overlay_native=newnative,requested_alternate=bool(request),source_body_non_field_bytes_equal=True,
            reference_names_preserved_except_proven_literal_labels=True))
    require(set(by_address) <= {r['address'] for r in rows},'requested owner missing from complete unit')
    return rows


def missing_key(row):return row['function_va'],row['source_field_offset']


def migration(oldrows,newrows,requests):
    event='MISSING_ORIGINAL_HIGHLOW_SOURCE_MIGRATION_BLOCKER'
    oldlist=[missing_key(r) for r in oldrows if r['event'] == event]
    newlist=[missing_key(r) for r in newrows if r['event'] == event]
    require(len(oldlist) == len(set(oldlist)) and len(newlist) == len(set(newlist)),'duplicate missing identity')
    old,new=set(oldlist),set(newlist)
    wanted={(o['address'],f['offset']) for o in requests for f in o['fields']}
    require(wanted <= old and new == old-wanted,'complete original/alternate missing migration differs')
    proofs=[]
    for owner in requests:
        for field in owner['fields']:
            hits=[r for r in newrows if missing_key(r) == (owner['address'],field['offset']) and r['event'] != event]
            require(len(hits) == 1,'fresh repaired binding ambiguous/missing')
            row=hits[0]
            require(row['coff_relocation']['kind'] == 6 and row['coff_relocation']['addend'] == 0 and
                    row['coff_relocation']['symbol'] == field['symbol'] and row['exact_original_target_va'] == field['target'] and
                    row['proof_consistency'] == 'EXACT_OWN_SOURCE_RESOLUTION','fresh repaired source target differs')
            proofs.append(dict(address=owner['address'],offset=field['offset'],target=field['target'],
                               symbol=field['symbol'],binding_sha256=identity(row)))
    return dict(original_missing_count=len(old),alternate_missing_count=len(new),repaired_count=len(wanted),
        remaining_missing=[dict(address=a,offset=b) for a,b in sorted(new)],repairs=proofs)


def replacement_map(recipe_id,original_object,overlay_object,unit_id,scope,requests,selections):
    requested={r['address'] for r in requests}; result=[];oldindices=set();newindices=set()
    for row in scope:
        address=row['address'];selected=selections.get(address)
        require(selected is not None,'function lacks original global selected owner')
        if address in requested:
            require(selected['recipe_id'] == recipe_id and selected['symbol'] == row['symbol'] and
                    selected['section'] == row['original_native']['section'] and selected['value'] == row['original_native']['value'] and
                    selected['size'] == row['size'],'replacement conflicts with original selected owner')
            oi=row['original_native']['symbol_index'];ni=row['overlay_native']['symbol_index']
            require(oi not in oldindices and ni not in newindices,'physical replacement coalesces distinct owners')
            oldindices.add(oi);newindices.add(ni)
            result.append(dict(address=address,original_selected_owner=selected,original_primary_index=oi,alternate_primary_index=ni,
                original_definition_id=identity(['original',recipe_id,original_object,oi]),
                alternate_definition_id=identity(['alternate-v1',unit_id,overlay_object,ni]),
                alternate_requested_by_fixed_policy=True,adopted_for_link=False,runtime_eligible=False))
        else:
            result.append(dict(address=address,original_selected_owner=selected,original_candidate_primary_index=row['original_native']['symbol_index'],
                alternate_primary_index=row['overlay_native']['symbol_index'],alternate_requested_by_fixed_policy=False,
                effective_provider_lane='original-selection-unchanged',alternate_same_TU_definition_exported=False,
                source_body_and_namespace_preserved=True,adopted_for_link=False,runtime_eligible=False))
    return result


def root_contract(unit_id,original,source_proof,object_path,object_hash,functions,requests,replacements,bindings,original_eh):
    requested={o['address'] for o in requests};by_address={r['address']:r for r in replacements}
    roots=[]
    for f in functions:
        if f['address'] not in requested:continue
        refs=[dict(ordinal=i+1,sha256=identity(r)) for i,r in enumerate(bindings) if r['function_va'] == f['address'] and r['function_symbol'] == f['symbol']]
        require(refs or not any(r['function_va'] == f['address'] for r in bindings),'root binding symbol mismatch')
        roots.append(dict(original_address=f['address'],symbol=f['symbol'],symbol_index=f['overlay_native']['symbol_index'],
            section=f['overlay_native']['section'],value=f['overlay_native']['value'],size=f['size'],
            definition_id=by_address[f['address']]['alternate_definition_id'],binding_refs=refs))
    require({r['original_address'] for r in roots} == requested,'whole requested root set incomplete')
    roots.sort(key=lambda r:r['original_address'])
    return dict(schema_version=1,kind='fnv-alternate-runtime-root-observer-input',overlay_unit_id=unit_id,
        requested_root_set_sha256=identity(roots),roots=roots,original_ancestry=original,actual_source_proof=source_proof,
        actual_object=dict(path=str(object_path),sha256=object_hash),
        original_eh_proof_lineage=original_eh,fresh_EH_revalidation=False,
        ordinary_v3_input_compatible=False,requires_overlay_aware_observer=True,
        source_initializers_adopted=False,other_same_TU_definitions_adopted=False,
        canonical_namespace_resolved=False,closure_verified=False,provider_adopted=False,runtime_eligible=False)


def compile_lineage(spec,receipts,recipe):
    obj=spec['artifacts'][spec['object']];source=spec['artifacts'][spec['generated_source']]
    if spec['group'] == 'first-two':
        key='build/rebuild/entry-relocation-repair-native-v1/result.json'
        records=[r for r in receipts[key]['units'] if r['recipe_id'] == spec['recipe_id']]
        require(len(records) == 1,'first-pair compile record absent/ambiguous');record=records[0]
        require(record['object_sha256'] == obj and record['generated_source_sha256'] == source and record['original_recipe_flags'] == recipe['flags'],'first-pair compile artifacts/profile differ')
        operation='first-pair-one-TU-compile'
    elif spec['group'] == 'nineteen-batch':
        key='build/rebuild/entry-relocation-batch-v2/runtime-overlays.json'
        records=[r for r in receipts[key]['units'] if r['recipe_id'] == spec['recipe_id']]
        require(len(records) == 1,'batch compile record absent/ambiguous');record=records[0]
        require(record['lane']['overlay_object_sha256'] == obj and record['lane']['generated_source_sha256'] == source and
                record['artifacts'] == spec['artifacts'] and record['flags'] == recipe['flags'],'batch compile artifacts/profile differ')
        operation=record['operation']
    else:
        require(spec['group'] == 'pilot','unknown accepted source lane')
        key='build/rebuild/source-overlay-niaccumulator-v2/result.json';record=receipts[key]
        require(record['overlay_object_sha256'] == obj and record['generated_source_sha256'] == source and
                record['original_recipe_flags'] == recipe['flags'] and record['generated_inputs_stability_verified'] is True,'pilot compile lineage differs')
        operation='pilot-v2-compile'
    return dict(receipt=key,accepted_compile_operation=operation,object_sha256=obj,generated_source_sha256=source,
                original_recipe_flags=recipe['flags'],registry_operation_is_metadata_only=True)


def run(args):
    started=time.monotonic();p=policy();this=Path(__file__).resolve()
    require(file_hash(this) == args.implementation_sha256,'reviewed registry implementation differs')
    label_policy=batch.frozen.read_bound(LABEL_POLICY,LABEL_POLICY_SHA)
    failed=ROOT/'build/rebuild/runtime-overlay-inputs-native-v1/registry.json'
    prior=batch.frozen.read_bound(failed,label_policy['original_failed_registry_sha256'])
    require(prior['status'] == 'error' and prior['terminal_protected_input_stability_verified'] is True,'registry v1 failure lineage differs')
    original_registry=ROOT/'tools/rebuild/runtime_overlay_inputs.py'
    require(file_hash(original_registry) == label_policy['original_registry_implementation_sha256'],'frozen v1 registry source changed')
    observations={this:args.implementation_sha256,POLICY:POLICY_SHA,LABEL_POLICY:LABEL_POLICY_SHA,
        ROOT/'tools/rebuild/local_label_symbol_migration.py':LABEL_HELPER_SHA,failed:label_policy['original_failed_registry_sha256'],
        original_registry:label_policy['original_registry_implementation_sha256']};receipts={}
    for rel,pin in p['receipt_pins'].items():
        path=ROOT/rel;receipts[rel]=batch.frozen.read_bound(path,pin);observations[path]=pin
    for key in ('build/rebuild/entry-relocation-repair-native-v1/result.json','build/rebuild/entry-relocation-batch-v2/result.json','build/rebuild/source-overlay-niaccumulator-v2/result.json'):
        r=receipts[key]
        require(r['status'] == 'pass_pending_independent_review' and r['input_stability_verified'] is True and
                r['provider_selected'] is False and r['runtime_eligible'] is False and r['game_execution'] is False and r['link_performed'] is False,'accepted receipt state differs')
        observations.update({Path(path):pin for path,pin in r['inputs'].items()})
    data={}
    for name,path in batch.frozen.DEFAULTS.items():
        data[name]=batch.frozen.read_bound(path,batch.frozen.PINS[name]);observations[path]=batch.frozen.PINS[name]
    for rel,pin in INPUT_PINS.items():data[Path(rel).stem]=batch.frozen.read_bound(ROOT/rel,pin);observations[ROOT/rel]=pin
    reference=Path(args.reference).resolve();observations[reference]=batch.frozen.PINS['reference']
    for name in batch.TOOLS+['tools/rebuild/literal_symbol_migration.py','tools/rebuild/runtime_overlay_inputs_v2.py']:
        observations.setdefault(ROOT/name,file_hash(ROOT/name))
    index=ROOT/'build/function_index.json';require(not index.exists() and data['retained']['inputs']['function_index_present'] is False,'optional index changed')
    for spec in p['units']:
        root=ROOT/spec['artifact_root']
        for name,pin in spec['artifacts'].items():observations[root/name]=pin
    require(all(file_hash(path) == pin for path,pin in observations.items()),'stale protected input')
    out=batch.frozen.new_output(args.out,observations);out.mkdir(parents=True)
    def note(state,**fields):
        with (out/'progress.jsonl').open('a',encoding='utf-8') as stream:
            stream.write(json.dumps(dict(state=state,**fields))+'\n');stream.flush();os.fsync(stream.fileno())
    note('started',policy_sha256=POLICY_SHA)
    report=dict(schema_version=1,kind='fnv-runtime-overlay-input-registry',registry_observation_version=2,status='error',units=[],
        inputs={str(k):v for k,v in observations.items()},input_stability_verified=False,compile_performed=False,
        game_execution=False,link_performed=False,provider_adopted=False,runtime_eligible=False,original_selection_unchanged=True)
    try:
        image=ImagePe(reference);ok,hits,probes=image_ok(image);require(ok,'reference probes failed');pe=Pe(reference)
        try:
            highlows=sorted(pe.base+r for r in pe.relocations());contracts=[];all_requested=set()
            for spec in p['units']:
                idx=spec['recipe_index'];unit=data['manifest']['units'][idx];recipe=data['recipes']['units'][idx];proof=data['retained']['units'][idx]
                require(unit['recipe_id'] == spec['recipe_id'] and unit['recipe'] == recipe and proof['object_sha256'] == unit['object_sha256'],'original recipe/object lineage differs')
                require(proof['recipe_id'] == unit['recipe_id'] and proof['source_sha256_recorded'] ==
                        proof['source_sha256_current'] == unit['source_sha256'],'original source proof lineage differs')
                compile_record=compile_lineage(spec,receipts,recipe)
                require(batch.first.row_identities(proof['verified_functions']) == batch.first.row_identities(recipe['functions']) and
                        all(r['verdict'] == 'match' for r in proof['verified_functions']),'original full unit proof differs')
                original_source=ROOT/recipe['source'];require(file_hash(original_source) == unit['source_sha256'],'original source differs')
                folder=ROOT/spec['artifact_root'];generated=folder/spec['generated_source'];object_path=folder/spec['object']
                if spec['group'] == 'first-two':
                    t=next(t for t in first.policy()['targets'] if t['recipe_id'] == spec['recipe_id']);expected=first.transform(original_source.read_bytes(),t)
                elif spec['group'] == 'pilot':
                    expected,_=batch.frozen.apply_overlay(original_source.read_bytes(),batch.frozen.EXPECTED)
                else:
                    s=next(s for s in batch.policy()['units'] if s['recipe_id'] == spec['recipe_id']);expected=batch.transform(original_source.read_bytes(),s)
                require(generated.read_bytes() == expected,'accepted generated source/context differs')
                original_object=(batch.frozen.DEFAULTS['manifest'].parent/data['manifest'].get('object_root_relative','.')/unit['object']).resolve()
                before,after=Coff(original_object),Coff(object_path);object_hash=spec['artifacts'][spec['object']]
                require(batch.sha(before.data) == unit['object_sha256'] and batch.sha(after.data) == object_hash,'physical object hash differs')
                adapted,supplement=literal.supplement(before,after,recipe,pe,highlows)
                if 'literal-supplement.json' in spec['artifacts']:
                    saved=json.loads((folder/'literal-supplement.json').read_text());require(saved['witnesses'] == supplement['witnesses'],'literal witness differs')
                    require(json.loads((folder/'alternate-resolver-recipe.json').read_text()) == adapted,'alternate resolver differs')
                else:require(not supplement['witnesses'],'unexpected unapproved literal namespace change')
                saved_rows=json.loads((folder/'comparison.json').read_text())['rows']
                owners=[dict(function_va=o['address'],original_selected_owner=o['selection']) for o in spec['requested_owners']]
                batch.complete_matches(saved_rows,recipe,owners)
                comparable=CompareCoff(object_path);require(batch.sha(comparable.data) == object_hash,'object drift before fresh comparison')
                rows=plain_compare(comparable,image,adapted);batch.complete_matches(rows,recipe,owners)
                local=local_labels.prove(before,after,recipe,original_source.read_bytes(),expected,pe,highlows,
                    label_policy['allowed'] if idx == label_policy['unit_recipe_index'] else [])
                namespace=dict(witnesses=supplement['witnesses']+local['witnesses'])
                scope=function_scope(before,after,recipe,spec['requested_owners'],namespace)
                for row in scope:
                    row.pop('reference_names_preserved_except_proven_literal_labels')
                    row['reference_names_preserved_except_proven_compiler_bookkeeping']=True
                old_placements={(r['address'],r['symbol'],r['size']):(r['section'],r['value']) for r in proof['verified_functions']}
                require(all(old_placements[(r['address'],r['symbol'],r['size'])] ==
                        (r['original_native']['section'],r['original_native']['value']) for r in scope),'original physical placements differ from v3 proof')
                oldrows,oldcounts,_=batch.source_bound_rows(before,unit,pe,highlows,data['selection'])
                newrows,newcounts,_=batch.source_bound_rows(after,dict(unit,recipe=adapted),pe,highlows,data['selection'])
                uid='overlay-v1-'+identity([unit['recipe_id'],object_hash,batch.sha(expected),identity(adapted)])
                for row in newrows:row.update(overlay_unit_id=uid,actual_object_sha256=object_hash,actual_generated_source_sha256=batch.sha(expected),original_recipe_id=unit['recipe_id'])
                moved=migration(oldrows,newrows,spec['requested_owners'])
                replacements=replacement_map(unit['recipe_id'],unit['object_sha256'],object_hash,uid,scope,spec['requested_owners'],data['selection']['selections'])
                for request in spec['requested_owners']:
                    require(request['selection'] == data['selection']['selections'][request['address']],'explicit alternate selection ancestry differs')
                    require(request['address'] not in all_requested,'alternate owners conflict across recipes')
                    all_requested.add(request['address'])
                    for field in request['fields']:
                        triage=[r for r in data['absolute-triage-evidence-v1']['rows'] if (r['recipe_id'],r['function_va'],r['function_offset'],r['target_va']) == (unit['recipe_id'],request['address'],field['offset'],field['target'])]
                        require(len(triage) == 1,'original missing-field triage lineage absent')
                original=dict(recipe_id=unit['recipe_id'],recipe_index=idx,recipe=recipe,original_source=str(original_source),source_sha256=unit['source_sha256'],object=str(original_object),object_sha256=unit['object_sha256'],retained_proof_sha256=batch.frozen.PINS['retained'],selection_sha256=batch.frozen.PINS['selection'])
                source_proof=dict(lane='accepted-runtime-source-overlay-v1',generated_source=str(generated),generated_source_sha256=batch.sha(expected),
                    original_source_sha256=unit['source_sha256'],receipt_pins=p['receipt_pins'],complete_original_function_rows=len(rows),all_rows_fresh_plain_match=True,
                    literal_supplement=supplement,local_label_bookkeeping=local,registry_producer_sha256=args.implementation_sha256,accepted_compile_lineage=compile_record,source_compiler_context='hash-bound accepted compile receipt; no new compilation')
                contract=root_contract(uid,original,source_proof,object_path,object_hash,scope,spec['requested_owners'],replacements,newrows,
                    dict(original_object_sha256=unit['object_sha256'],original_retained_unit=proof,not_a_fresh_overlay_EH_proof=True))
                private=out/unit['recipe_id'];private.mkdir()
                batch.save_gzip(private/'bindings.jsonl.gz',newrows)
                batch.frozen.save(private/'native-inventory.json',dict(object_sha256=object_hash,**batch.inventory(after),all_physical_fields=[dict(section=s['index'],**batch.relocation_record(after,s,r)) for s in after.sections.values() for r in s['relocs']]))
                sanitized=[{k:v for k,v in r.items() if k != 'byte_differences'} | dict(byte_difference_offsets=[d['offset'] for d in r['byte_differences']]) for r in rows]
                batch.frozen.save(private/'comparison.json',dict(rows=sanitized));batch.frozen.save(private/'source-and-replacements.json',dict(function_scope=scope,replacements=replacements,migration=moved,original_ancestry=original,actual_source_proof=source_proof))
                contract.update(binding_details_sha256=file_hash(private/'bindings.jsonl.gz'),native_inventory_sha256=file_hash(private/'native-inventory.json'),fresh_comparison_sha256=file_hash(private/'comparison.json'),complete_binding_rows=len(newrows),remaining_missing=moved['remaining_missing'])
                contract['registry_observation_version']=2
                contract['local_label_policy_sha256']=LABEL_POLICY_SHA
                contracts.append(contract)
                report['units'].append(dict(overlay_unit_id=uid,recipe_id=unit['recipe_id'],recipe_index=idx,original_ancestry=original,actual_source_proof=source_proof,
                    actual_object=dict(path=str(object_path),sha256=object_hash),requested_alternate_owners=[r for r in replacements if r['alternate_requested_by_fixed_policy']],
                    unaffected_owner_count=len(scope)-len(spec['requested_owners']),migration=moved,original_highlow_partition=oldcounts,alternate_highlow_partition=newcounts,
                    contract_sha256=identity(contract),artifacts={f.name:file_hash(f) for f in (private/'bindings.jsonl.gz',private/'native-inventory.json',private/'comparison.json',private/'source-and-replacements.json')}))
                note('unit_observed',recipe_id=unit['recipe_id'],overlay_unit_id=uid)
        finally:pe.close()
        del image
        require(len(report['units']) == 9 and len(all_requested) == 13 and sum(u['actual_source_proof']['complete_original_function_rows'] for u in report['units']) == 931 and sum(u['migration']['repaired_count'] for u in report['units']) == 22,'registry census differs')
        batch.save_gzip(out/'root-observer-inputs.jsonl.gz',contracts)
        require(not index.exists() and all(file_hash(path) == pin for path,pin in observations.items()),'protected input drift')
        for unit in report['units']:
            require(all(file_hash(out/unit['recipe_id']/name) == pin for name,pin in unit['artifacts'].items()),'registry artifact drift')
        report.update(status='pass_pending_independent_review',input_stability_verified=True,root_observer_inputs_sha256=file_hash(out/'root-observer-inputs.jsonl.gz'),
            original_entry_missing_census_unchanged=47,original_global_missing_census_unchanged=88,whole_original_selection_unchanged=True,local_label_policy_sha256=LABEL_POLICY_SHA,image_gate=dict(hits=hits,probes=probes),
            original_missing_in_observed_units=sum(u['migration']['original_missing_count'] for u in report['units']),alternate_missing_in_observed_units=sum(u['migration']['alternate_missing_count'] for u in report['units']))
        note('verified_pending_review')
    except Exception as error:
        report['error']=str(error);note('failed',error_type=type(error).__name__)
    try:report['terminal_protected_input_stability_verified']=all(file_hash(path) == pin for path,pin in observations.items())
    except OSError:report['terminal_protected_input_stability_verified']=False
    if not report['terminal_protected_input_stability_verified']:report.update(status='error',error='protected input drift at terminal recheck')
    report['elapsed_seconds']=time.monotonic()-started;batch.frozen.save(out/'registry.json',report);return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('reference','out'):parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--implementation-sha256',required=True);args=parser.parse_args()
    try:result=run(args)
    except (ValueError,OSError,KeyError,TypeError) as error:parser.exit(2,'overlay registry rejected: '+str(error)+'\n')
    print(result['status']);return 0 if result['status'] == 'pass_pending_independent_review' else 1


if __name__=='__main__':raise SystemExit(main())
