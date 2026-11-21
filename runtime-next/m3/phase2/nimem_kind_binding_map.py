"""Combine source-backed unit-local diagnostic mappings, never install them."""
import argparse,collections,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M/'out'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--baseline',type=Path,required=True);ap.add_argument('--local',type=Path,required=True);ap.add_argument('--immediate',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();out=a.out.resolve()
 if not out.is_relative_to(R.resolve()) or out.exists():raise ValueError('fresh private path required')
 x=[json.loads(p.read_text()) for p in (a.baseline,a.local,a.immediate)];u=json.loads((R/'phase2-nimem-kind-cohort-run/units.snapshot.json').read_text())['units'];maps=collections.defaultdict(dict)
 if x[1]['snapshot_sha256']!=sha(a.baseline) or x[2]['snapshot_sha256']!=sha(a.baseline):raise ValueError('proofs refer to different baseline snapshot')
 def add(i,n,v,proof):
  p=maps[i].get(n)
  if p and p['target']!=v:raise ValueError('conflicting unit-local mapping')
  maps[i][n]={'target':v,'recipe_previous':u[i]['symbols'].get(n),'evidence':proof}
 for z in x[0]['fields']:
  if z['status']=='source-unique-reference-agree':add(z['unit'],z['symbol'],z['source_target'],'unique-strong-external-source-and-reference')
 for z in x[1]['fields']:
  if z['status']=='source-paired-reference-agree':add(z['unit'],z['current_label'],z['source_bound_va'],'same-unit-strict-archive-and-pool')
 for z in x[2]['fields']:
  if z['status']=='archived-source-immediate-agrees':add(z['unit'],z['symbol'],z['target'],'same-unit-strict-archive-immediate')
 unresolved=[z for z in x[1]['fields'] if z['status']=='unresolved']+[z for z in x[2]['fields'] if z['status']=='unresolved']+[z for z in x[0]['fields'] if z['status'] not in ('source-unique-reference-agree','source-binding-not-unique','local-label-deferred')]
 result={'scope':'per-unit source-backed diagnostic candidates, not installed','evidence_sha256':{p.name:sha(p) for p in (a.baseline,a.local,a.immediate)},'units':{str(i):v for i,v in sorted(maps.items())},'unit_count':len(maps),'binding_count':sum(len(z) for z in maps.values()),'unresolved':unresolved,'limits':['same-unit local labels only; no cross-unit binding','EH failures and inferred targets remain separate','all mappings need independent review and actual production reproof']};out.write_text(json.dumps(result,indent=2));print(json.dumps({'units':len(maps),'bindings':result['binding_count'],'unresolved':len(unresolved)}))
if __name__=='__main__':main()
