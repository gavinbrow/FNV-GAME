"""Check the reviewed MCP TESContainer proposal in isolated native fixtures.

Never installs the proposal, edits the recipe, runs an image, or changes gates.
Uses the existing guarded mirror compiler and unchanged reference comparators.
"""
import argparse,hashlib,json,subprocess,sys
from collections import Counter
from pathlib import Path

H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp'
sys.path[:0]=[str(H),str(RN),str(F/'tools')]
import rtti_mirror_prepare as prep
import rtti_tesform_bindings_transaction as locks
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
from rtti_hkp_viewer_compare import relocated
import paths

BASE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68'
REF='df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7'
JOB='P2N19-000-TESContainer775'
CALLER='src/fallout_shared/inventorychanges_ctxr_variant.cpp'


def sha(data):return hashlib.sha256(data).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))


def stage(index,overrides,root,units):
    out=root/('unit-%04d'%index);out.mkdir()
    source=units[index]['source'];base=prep.walk(F,source,{});candidate=prep.walk(F,source,overrides)
    if set(overrides)-set(candidate['files']):raise ValueError('override not in candidate closure')
    for tag,graph in [('original',base),('candidate',candidate)]:
        for name,digest in graph['files'].items():
            data=overrides[name] if tag=='candidate' and name in overrides else (F/name).read_bytes()
            if sha(data)!=digest:raise ValueError('source changed while staging')
            p=out/tag/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    meta={'unit':index,'source':source,'units_sha256':BASE,'original_inputs':{
        n:sha((F/n).read_bytes()) for n in sorted(set(base['files'])|set(candidate['files']))},
        'original':base,'candidate':candidate,'proposal_job':JOB,'scope':'private source equivalence fixture; no installation'}
    (out/'mirror-manifest.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
    return out


def check(index,out,units,pe,names):
    unit=units[index];run=load(out/'compile-result.json');results={};objects={}
    for row in run['outcomes']:
        p=out/(row['tag']+'.obj')
        if row['rc'] or not row['trace_valid'] or sha(p.read_bytes())!=row['object_sha256']:
            raise ValueError('compile/trace/object check failed')
        obj=Coff(str(p));objects[row['tag']]=obj
        normal=compare(obj,pe,unit)
        sections,inferred,errors=eh_sections(obj,pe,unit,normal,names)
        tails,bad,_,_,conflicts=eh_tails([unit],[{'eh_sections':sections,
            'eh_inferred':{k:'0x%08x'%v for k,v in inferred.items()}}],pe)
        results[row['tag']]={'functions':len(normal),'matches':sum(x['verdict']=='match' for x in normal),
            'failed_functions':[{'address':x['address'],'errors':x['errors']} for x in normal if x['verdict']!='match'],
            'eh_sections':sections,'eh_errors':errors,'bad_tails':bad,'tail_conflicts':conflicts,
            'warning_codes':dict(Counter(__import__('re').findall(r'warning\s+(C\d+)', '\n'.join(row['warnings']))))}
    pairs=[]
    for f in unit['functions']:
        a,ar=relocated(objects['original'],f['symbol'],f['size'],{})
        b,br=relocated(objects['candidate'],f['symbol'],f['size'],{})
        if a!=b or ar!=br:pairs.append({'address':f['address'],'bytes_equal':a==b,
            'original_relocations':ar,'candidate_relocations':br})
    gates={'all_original_functions_match':results['original']['matches']==len(unit['functions']),
        'all_candidate_functions_match':results['candidate']['matches']==len(unit['functions']),
        'mapped_bytes_and_relocations_identical':not pairs,
        'all_original_located_EH_pass':all(x[2] for x in results['original']['eh_sections']),
        'all_candidate_located_EH_pass':all(x[2] for x in results['candidate']['eh_sections']),
        'no_EH_errors_or_bad_tails':all(not r['eh_errors'] and not r['bad_tails'] and not r['tail_conflicts'] for r in results.values()),
        'warning_codes_unchanged':results['original']['warning_codes']==results['candidate']['warning_codes']}
    report={'unit':index,'results':results,'pair_differences':pairs,'gates':gates,
        'limits':['private original/candidate source equivalence only','all global class views and generated metadata ownership remain open','no image build, gameplay, source installation or class-completion claim']}
    (out/'comparison.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return {'unit':index,'gates':gates,'functions':len(unit['functions']),
            'candidate_matches':results['candidate']['matches'],'candidate_EH_sections':len(results['candidate']['eh_sections'])}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--export',type=Path,required=True);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    export=args.export.resolve();out=args.out.resolve()
    if not export.is_relative_to((M/'out').resolve()) or not out.is_relative_to((M/'out').resolve()):raise ValueError('private output required')
    manifest=load(export/'proposal-manifest.json')
    if manifest['job']!=JOB:raise ValueError('wrong proposal')
    for name,digest in manifest['proposed_hashes'].items():
        if sha((export/name).read_bytes())!=digest:raise ValueError('proposal altered')
    proposal=load(export/'runtime-proposals'/JOB/'changes.json')
    if proposal['schema']!=1 or proposal['job_id']!=JOB or not proposal['edits']:raise ValueError('proposal schema')
    raw=(F/'build/units.json').read_bytes()
    if sha(raw)!=BASE or sha(Path(paths.REF_IMAGE).read_bytes())!=REF:raise ValueError('accepted inputs changed')
    units=json.loads(raw)['units'];original=(F/CALLER).read_bytes();text=original.decode('utf-8-sig').replace('\r\n','\n');expected=sha(text.encode())
    for edit in proposal['edits']:
        if edit['path']!=CALLER or edit['source_sha256']!=expected or not edit['old_text'] or text.count(edit['old_text'])!=1:
            raise ValueError('unreviewed scope or ambiguous source anchor')
        text=text.replace(edit['old_text'],edit['new_text'],1)
    if text==original.decode('utf-8-sig').replace('\r\n','\n'):raise ValueError('no actual source change')
    candidate=text.encode('utf-8');out.mkdir(exist_ok=False)
    (out/'candidate-source.cpp').write_bytes(candidate)
    rows=[];guard=locks.acquire_guard()
    try:
        if (RN/'direct-v1/harness.lock').exists():raise ValueError('gameplay lane busy')
        names=recipe_names(units);pe=Pe(paths.REF_IMAGE)
        for index in (775,980):
            fixture=stage(index,{CALLER:candidate} if index==775 else {},out,units)
            run=subprocess.run([sys.executable,str(H/'nimem_combined_825d_compile.py'),'--out',str(fixture),'--unit',str(index)],
                cwd=P,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=900)
            (fixture/'driver.log').write_text(run.stdout,encoding='utf-8')
            if run.returncode:
                rows.append({'unit':index,'compile_failed':True,'returncode':run.returncode});break
            row=check(index,fixture,units,pe,names);rows.append(row)
            if not all(row['gates'].values()):break
        source_unchanged=(F/CALLER).read_bytes()==original and sha((F/'build/units.json').read_bytes())==BASE
        report={'job':JOB,'export_manifest_sha256':sha((export/'proposal-manifest.json').read_bytes()),
            'changed_source_sha256':sha(candidate),'recipe_sha256':BASE,'reference_sha256':REF,'units':rows,
            'pass':len(rows)==2 and all('gates' in r and all(r['gates'].values()) for r in rows) and source_unchanged,
            'production_source_and_recipe_unchanged':source_unchanged,'production_installation':False}
        (out/'result.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
        if not report['pass']:raise SystemExit(1)
    finally:
        for path in reversed(guard):path.unlink()


if __name__=='__main__':main()
