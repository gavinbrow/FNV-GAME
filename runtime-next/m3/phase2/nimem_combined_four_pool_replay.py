"""Replay four strict same-unit source-pool binding diagnostics; do not install."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;sys.path[:0]=[str(R/'fnv_decomp/tools'),str(R/'runtime-next')];from compare import Coff,Pe,compare;from build_and_match import eh_sections,recipe_names;import paths
O=M/'out';D=O/'phase2-nimem-combined-825d-run';OUT=D/'independent-four-pool-binding-replay.json';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError(OUT)
 triage=D/'independent-mapped-pair-triage.json';q=json.loads(triage.read_text());recipe=O/'phase2-nimem-combined-825d/units.generated';doc=json.loads(recipe.read_text());pe=Pe(paths.REF_IMAGE);out=[]
 for row in q['units']:
  i=row['unit']
  if i not in (147,392,703,725):continue
  unit=copy.deepcopy(doc['units'][i]);changes={}
  for case in row['cases']:
   if case['classification']!='same-unit literal renumbering, whole pool and offsets equal':raise ValueError('pool proof missing')
   for x in case['relocation_differences']:
    target=x['prior_recipe_target'];name=x['after'][0]
    if not target or (name in changes and changes[name]!=target):raise ValueError('unbound or conflicting source target')
    changes[name]=target
  unit['symbols'].update(changes);obj=D/('unit-%04d'%i)/'candidate.obj';c=Coff(str(obj));rows=compare(c,pe,unit);sections,inferred,errors=eh_sections(c,pe,unit,rows,recipe_names(doc['units']))
  if any(x['verdict']!='match' for x in rows) or any(not x[2] for x in sections) or errors:raise ValueError('strict replay failed '+str(i))
  out.append({'unit':i,'object_sha256':h(obj),'bindings':changes,'strict_functions':len(rows),'eh_sections':len(sections),'eh_failures':0,'eh_errors':0,'inferred_names':{k:hex(v) for k,v in inferred.items()}})
 if len(out)!=4:raise ValueError('scope missing')
 OUT.write_text(json.dumps({'scope':'private same-unit pool diagnostic, no recipe edits','triage_sha256':h(triage),'candidate_recipe_sha256':h(recipe),'units':out,'limitations':['bindings reflect these fixture objects; actual production reproof required','unit725 candidate key replaces stale colliding old name only in private diagnostic','field-scoped prior immediate proofs are not generalized','no final linker, metadata or runtime acceptance']},indent=2));print(h(OUT))
if __name__=='__main__':main()
