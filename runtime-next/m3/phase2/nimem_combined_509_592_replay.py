"""Replay source-backed 509/592 diagnostics from archived same-unit pools."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;sys.path[:0]=[str(R/'fnv_decomp/tools'),str(R/'runtime-next')];from compare import Coff,Pe,compare;from build_and_match import eh_sections,recipe_names;import paths
O=M/'out';D=O/'phase2-nimem-combined-825d-run';OUT=D/'independent-509-592-binding-replay.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();j=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 if OUT.exists():raise FileExistsError(OUT)
 tri=D/'independent-mapped-pair-triage.json';q=j(tri);proof=O/'phase2-nimem-kind-source-bindings-final.json';p=j(proof)
 if sha(proof)!='1b08d57f69d9fb473ed511de4b9dfc172072f3836244cdce596774cf413200de':raise ValueError('source binding proof changed')
 for rel,digest in p['evidence_sha256'].items():
  if sha(O/rel)!=digest:raise ValueError('underlying evidence changed')
 base=j(O/'phase2-nimem-combined-825d/units.original')['units'];candidate=j(O/'phase2-nimem-combined-825d/units.generated')['units'];pe=Pe(paths.REF_IMAGE);result=[]
 for i in (509,592):
  item=next(x for x in q['units'] if x['unit']==i);b=p['units'][str(i)];existing=copy.deepcopy(base[i]);out=copy.deepcopy(candidate[i]);updates={};source={}
  for name,record in b.items():
   if record['evidence'] not in ('same-unit-strict-archive-and-pool','unique-strong-external-source-and-reference'):raise ValueError('unsupported/field-only proof')
   if existing['symbols'].get(name)!=record['recipe_previous']:raise ValueError('baseline target preimage mismatch')
   source[name]=record['target']
  existing['symbols'].update(source);out['symbols'].update(source)
  for case in item['cases']:
   if case['classification']!='same-unit literal renumbering, whole pool and offsets equal':raise ValueError('pair not proven')
   for x in case['relocation_differences']:
    old=x['before'][0];new=x['after'][0];target=source.get(old,x['prior_recipe_target'])
    if not target or (new in updates and updates[new]!=target):raise ValueError('missing/conflicting source target')
    updates[new]=target
  out['symbols'].update(updates);checks={}
  for tag,spec in [('original',existing),('candidate',out)]:
   obj=D/('unit-%04d'%i)/(tag+'.obj');c=Coff(str(obj));rows=compare(c,pe,spec);sec,inf,err=eh_sections(c,pe,spec,rows,recipe_names(candidate));checks[tag]={'object_sha256':sha(obj),'functions':len(rows),'matches':sum(r['verdict']=='match' for r in rows),'failures':[{'address':r['address'],'errors':r['errors']} for r in rows if r['verdict']!='match'],'eh_sections':len(sec),'eh_failed':sum(not x[2] for x in sec),'eh_errors':err,'inferred_names':{k:hex(v) for k,v in inf.items()}}
  result.append({'unit':i,'source_bound_baseline':source,'candidate_pool_bindings':updates,'checks':checks})
 OUT.write_text(json.dumps({'scope':'source-backed diagnostic only; no recipe edit or field-only alias promotion','triage_sha256':sha(tri),'source_binding_proof_sha256':sha(proof),'units':result,'limitations':['candidate labels require fresh production reproof after any source installation','44 field-scoped immediates are not used as global aliases','EH failures, inferred names and final image ownership remain separate']},indent=2));print(json.dumps({'sha256':sha(OUT),'results':[{k:v for k,v in r.items() if k in ('unit','checks')} for r in result]}))
if __name__=='__main__':main()
