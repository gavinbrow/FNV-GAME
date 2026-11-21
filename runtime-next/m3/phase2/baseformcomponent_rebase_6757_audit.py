"""Read-only BFC d569-to-6757 semantic/source transition audit."""
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;F=M.parent.parent/'fnv_decomp';O=M/'out';S=O/'phase2-baseformcomponent-core';T=O/'phase2-combined-source-transaction';R=O/'phase2-bfc-core-rebase-6757.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if R.exists():raise FileExistsError('preserve transition evidence')
 old=T/'4.original';new=T/'4.generated';live=F/'build/units.json';m=json.loads((T/'manifest.json').read_text());co=json.loads((S/'manifest.json').read_text());a=json.loads(old.read_text());b=json.loads(new.read_text())
 if sha(old)!='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160' or sha(new)!='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c' or sha(live)!=sha(new):raise ValueError('recipe preimage/postimage differs')
 if {k:v for k,v in a.items() if k!='units'}!={k:v for k,v in b.items() if k!='units'} or len(a['units'])!=len(b['units']) or [i for i,(x,y) in enumerate(zip(a['units'],b['units'])) if x!=y]!=[998,1111,1112]:raise ValueError('recipe transition differs')
 changed={x['path']:x for x in m['files'] if x['path']!='build/units.json'}
 for rel,x in changed.items():
  if sha(F/rel)!=x['new_sha256'] or sha(T/x['original'])!=x['old_sha256'] or sha(T/x['generated'])!=x['new_sha256']:raise ValueError('source transaction differs '+rel)
 affected=[];checked={}
 for unit in co['units']:
  hits=[]
  for rel,digest in unit['original']['files'].items():
   if rel in changed:
    if digest!=changed[rel]['old_sha256']:raise ValueError('closure old digest differs '+rel)
    hits.append(rel)
   else:
    got=checked.setdefault(rel,sha(F/rel))
    if got!=digest:raise ValueError('unreviewed closure change '+rel)
  if hits:affected.append({'unit':unit['unit'],'functions':len(unit['functions']),'recipe_eh_tails':len(unit['eh_tails']),'changed_inputs':sorted(hits)})
 if [x['unit'] for x in affected]!=[2,1111,1112]:raise ValueError('unexpected affected cohort')
 R.write_text(json.dumps({'old_recipe_sha256':sha(old),'new_recipe_sha256':sha(new),'transaction_manifest_sha256':sha(T/'manifest.json'),'old_cohort_manifest_sha256':sha(S/'manifest.json'),'checked_unchanged_project_closure_paths':len(checked),'affected':affected,'status':'semantic recipe transition and lexical project closure preimages verified; no mirrors regenerated','limits':['compiler/preprocessor contexts and actual objects require fresh proof','ordinary recipe EH tails and generated data/ownership are unverified']},indent=2));print('verified',len(checked),'unchanged closure paths; affected',[x['unit'] for x in affected])
if __name__=='__main__':main()
