"""Bounded report of mapped function pair differences, no reference-derived aliases."""
import json,hashlib,sys
from pathlib import Path
from collections import Counter
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;sys.path.insert(0,str(R/'fnv_decomp/tools'));from compare import Coff
O=M/'out';D=O/'phase2-nimem-combined-825d-run';OUT=D/'independent-mapped-pair-triage.json';IDS=(147,392,509,592,703,725);SKIP=(548,721,722,726)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 if OUT.exists():raise FileExistsError(OUT)
 progress=j(D/'progress.json');raw=(D/'progress.json').read_bytes();rows={x['unit']:x for x in progress['units']};recipe=j(O/'phase2-nimem-combined-825d/units.original')['units'];proof=O/'phase2-nimem-kind-source-bindings-final.json';evidence=j(proof)['units'];results=[]
 for i in IDS:
  d=D/('unit-%04d'%i);cp=d/'comparison.json'
  if h(cp)!=rows[i]['comparison_sha256']:raise ValueError('comparison changed')
  report=j(cp);compile=j(d/'compile-result.json');objs={}
  for z in compile['outcomes']:
   p=d/(z['tag']+'.obj')
   if z['rc'] or not z['trace_valid'] or h(p)!=z['object_sha256']:raise ValueError('object identity')
   objs[z['tag']]=Coff(str(p))
  cases=[]
  for x in report['mapped_function_pair_differences']:
   if 'error' in x:cases.append({'address':x['address'],'classification':'unresolved object comparison','error':x['error']});continue
   a={(q[0],q[1]):(q[2],q[3]) for q in x['original_relocations']};b={(q[0],q[1]):(q[2],q[3]) for q in x['candidate_relocations']};ds=[]
   for key in sorted(a.keys()|b.keys()):
    if a.get(key)==b.get(key):continue
    left,right=a.get(key),b.get(key);entry={'offset':key[0],'type':key[1],'before':left,'after':right}
    if left and right and left[0].startswith('$SG') and right[0].startswith('$SG') and left[1]==right[1] and key[1]==6:
     try:
      os=objs['original'].named(left[0]);ns=objs['candidate'].named(right[0]);ob=objs['original'].sections[os['section']]['data'];nb=objs['candidate'].sections[ns['section']]['data'];entry.update(same_offset=os['value']==ns['value'],whole_pool_equal=ob==nb,pool_sha256=hashlib.sha256(ob).hexdigest())
      direct=recipe[i]['symbols'].get(left[0]);source=evidence.get(str(i),{}).get(left[0]);entry['prior_recipe_target']=direct;entry['source_binding_evidence']=source
     except (ValueError,KeyError,IndexError) as exc:entry['proof_error']=str(exc)
    ds.append(entry)
   literal_only=bool(x['bytes_equal']) and bool(ds) and all(z.get('same_offset') and z.get('whole_pool_equal') for z in ds)
   cases.append({'address':x['address'],'classification':'same-unit literal renumbering, whole pool and offsets equal' if literal_only else 'actual code/target change or unresolved','code_bytes_equal':x['bytes_equal'],'relocation_differences':ds})
  results.append({'unit':i,'comparison_sha256':h(cp),'production_strict':report['reference']['production'],'candidate_strict':report['reference']['candidate'],'cases':cases})
 if (D/'progress.json').read_bytes()!=raw:raise ValueError('run changed')
 counts=Counter(c['classification'] for r in results for c in r['cases']);report={'scope':'six mapped-function-pair review units; 548/721/722/726 reserved for separate EH review','progress_sha256':hashlib.sha256(raw).hexdigest(),'source_binding_proof_sha256':h(proof),'reviewed_units':list(IDS),'cases_by_class':dict(counts),'units':results,'limits':['equal pool/offset alone establishes same emitted literal position, not native target identity','source binding candidates remain source-backed diagnostic evidence and require field-level review before recipe update','44 prior immediate proofs remain field-scoped, not propagated as global symbol aliases','compiler warnings and preexisting EH issues remain separate','five fresh kind-only units require their own section-pair evidence']}
 OUT.write_text(json.dumps(report,indent=2));print(json.dumps({'sha256':h(OUT),'classes':counts,'pairs':sum(len(r['cases']) for r in results)}))
if __name__=='__main__':main()
