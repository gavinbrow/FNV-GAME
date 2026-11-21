"""Read-only EH union from terminal NiMem cohort plus independently proven outside owners."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;F=R/'fnv_decomp';O=M/'out';P=O/'phase2-nimem-kind-cohort-run';sys.path[:0]=[str(F/'tools'),str(R/'runtime-next')]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
import paths
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();j=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 output=P/'independent-eh-outside-union-v3.json'
 if output.exists():raise FileExistsError(output)
 progress=P/'progress.json';pr=j(progress);raw=progress.read_bytes();scope=O/'phase2-nimemobject-coherent-kind-consumers.json'
 if pr['status'] not in ('complete-review-required','function-and-eh-pass-metadata-review-required') or h(scope)!=pr['scope_sha256'] or len(pr['units'])!=750:raise ValueError('scope incomplete')
 units=j(O/'phase2-eh-1047-ownership-archive/units.json')['units'];old=j(O/'phase2-flags-script-production-before/units.json')['units'];pe=Pe(paths.REF_IMAGE);names=recipe_names(units);ids=[x['unit'] for x in pr['units']]
 ss=j(scope);want={x['unit'] for x in ss['units']}
 if len(set(ids))!=750 or set(ids)!=want or h(O/'phase2-eh-1047-ownership-archive/units.json')!=pr['recipe_sha256']:raise ValueError('unit scope/recipe mismatch')
 records={tag:[] for tag in ('production','original','candidate')};comparisonhashes={}
 for row in pr['units']:
  i=row['unit'];p=P/('unit-%04d'%i)/'comparison.json'
  if h(p)!=row['comparison_sha256']:raise ValueError('changed comparison')
  x=j(p);comparisonhashes[str(i)]=h(p)
  for tag in records:
   e=x['ordinary_eh'][tag];records[tag].append({'eh_sections':e['eh_sections'],'eh_inferred':e['eh_inferred']})
 outsiders=[];proof=j(O/'phase2-bfc-eh-unit1027-contribution.json')
 for i,p,digest in [(1029,R/'runtime-next/pinned-build/obj_v3.bak-20261116/1029.obj',proof['outside_object_sha256']),(1033,R/'runtime-next/pinned-build/obj_v3.bak-20261116/1033.obj','2d37ac1db50aa3bdb5e3b3e18728fd0f85432ec6b1b75696b3afe7f4226527a5'),(1047,O/'phase2-eh-1047-ownership-archive/1047.obj','fe5d3807f93ceaa1aa59f582c7884d98adb61d48747485797403e71a35eddb8e'),(633,O/'phase2-bfc-cohort-production-archive/0633.obj','14787ddebcc8d4fc3e4520c1ea0bf548d8398a9ba712fe4ba39732bfdb5ba771'),(461,O/'phase2-native-source-positive/evidence/0461.obj','8af25f0f21ca41ce0173d068ae35a696e60c7079055994f4787485f01ac2f3fb'),(889,O/'phase2-native-source-positive/evidence/0889.obj','7d017f81a3366e4774c4f3c55f3a19a030afa0546fbad59ebb3577e15332f22d')]:
  if i in ids or h(p)!=digest or (i in (1029,1033,633) and old[i]!=units[i]):raise ValueError('outside owner provenance')
  c=Coff(str(p));rows=compare(c,pe,units[i]);sections,inferred,errors=eh_sections(c,pe,units[i],rows,names)
  if any(x['verdict']!='match' for x in rows) or any(not s[2] for s in sections) or errors:raise ValueError('outside owner strict/EH mismatch '+str(i))
  rec={'eh_sections':sections,'eh_inferred':{k:'0x%08x'%v for k,v in inferred.items()}}
  for tag in records:records[tag].append(rec)
  outsiders.append({'unit':i,'sha256':digest,'strict_functions':len(rows),'sections':len(sections),'inferred_names':len(inferred)})
 summary={};selected=[units[i] for i in ids]
 for tag,allrecords in records.items():
  tails,bad,inferred,count,conflicts=eh_tails(selected,allrecords,pe);summary[tag]={'tail_count':len(tails),'bad':bad,'inferred_tails':inferred,'inferred_name_count':count,'conflicts':conflicts}
 if progress.read_bytes()!=raw:raise ValueError('progress changed')
 result={'scope':'terminal 750 cohort EH union plus independently strict outside owners; unchanged ordinary oracle','progress_sha256':hashlib.sha256(raw).hexdigest(),'recipe_sha256':pr['recipe_sha256'],'scope_sha256':pr['scope_sha256'],'outside_owners':outsiders,'summary':summary,'comparison_sha256':comparisonhashes,'limitations':['outside objects are archived independently and are not newly compiled NiMem candidates','section relocation failures and unit strict mismatches remain separate; tail coverage is not complete EH correctness','oracle reports inferred names separately; no reference-only symbol binding introduced','other outside owners may exist','6757 recipe comes from immutable 1047 capture; active recipe is not read']}
 output.write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps({'outside':outsiders,'summary':summary}))
if __name__=='__main__':main()
