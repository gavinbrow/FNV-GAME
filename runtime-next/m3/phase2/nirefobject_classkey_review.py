"""Strict two-unit NiMemObject key experiment review; no placement claim."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';D=M/'out/phase2-nirefobject-classkey-fixture';OUT=D/'independent-review.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,recipe_names
from rtti_hkp_viewer_compare import relocated
from class_metadata_compare import ObjectRecords
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve evidence')
 m=json.loads((D/'manifest.json').read_text());recipe=F/'build/units.json'
 if sha(recipe)!=m['recipe_sha256']:raise ValueError('recipe changed')
 units=json.loads(recipe.read_text())['units'];pe=Pe(paths.REF_IMAGE);res={};allobjs={}
 for i in (1484,1503):
  d=D/str(i);mm=d/'mirror-manifest.json';r=json.loads((d/'compile-result.json').read_text());
  if r['unit_index']!=i or r['mirror_manifest_sha256']!=sha(mm):raise ValueError('compile manifest differs')
  objs={};res[str(i)]={}
  for tag in ('original','candidate'):
   row=next(x for x in r['outcomes'] if x['tag']==tag);f=d/(tag+'.obj')
   if row['rc'] or not row['trace_valid'] or sha(f)!=row['object_sha256']:raise ValueError('invalid compile')
   obj=Coff(str(f));checks=compare(obj,pe,units[i]);sections,inferred,errors=eh_sections(obj,pe,units[i],checks,recipe_names(units))
   if any(x['verdict']!='match' for x in checks) or errors or any(not x[2] for x in sections):raise ValueError('strict function or EH mismatch')
   objs[tag]=obj;res[str(i)][tag]={'object_sha256':sha(f),'functions':len(checks),'eh_sections':len(sections),'inferred_names':len(inferred),'observed_project_includes':row['observed_project_includes']}
  for f in units[i]['functions']:
   a,ar=relocated(objs['original'],f['symbol'],f['size'],{});b,br=relocated(objs['candidate'],f['symbol'],f['size'],{})
   if a!=b or ar!=br:raise ValueError('code relocation difference '+f['address'])
  allobjs[i]=objs
 old=ObjectRecords(allobjs[1503]['original']).tables('.?AVNiRefObject@@');new=ObjectRecords(allobjs[1503]['candidate']).tables('.?AVNiRefObject@@')
 if len(old)!=1 or len(new)!=1:raise ValueError('table missing')
 og=old[0]['locator']['graph'];ng=new[0]['locator']['graph'];bases=ng['bases']
 if [x['type_name'] for x in og['bases']]!=['.?AVNiRefObject@@','.?AVNiMemObject@@'] or [x['type_name'] for x in bases]!=['.?AVNiRefObject@@','.?AUNiMemObject@@'] or [x['pmd'] for x in bases]!=[[0,-1,0],[4,-1,0]] or len(new[0]['slots'])!=2:raise ValueError('metadata hypothesis differs')
 OUT.write_text(json.dumps({'scope':'private class-key candidate; original and candidate mapped functions and emitted graph','manifest_sha256':sha(D/'manifest.json'),'recipe_sha256':sha(recipe),'results':res,'original_graph':og,'candidate_graph':ng,'candidate_slots':[x['symbol']['name'] for x in new[0]['slots']],'limits':['slot 0 weak deleting wrapper remains unresolved and original 46-byte owner differs from emitted 42-byte fallback','shared layout_support.h and all prior declarations require full affected-consumer scope','ABI/ODR, generated sections, production placement and final image remain separate']},indent=2));print('PASS 13 functions unchanged; candidate RTTI base struct and PMD match; slot 0 remains unresolved')
if __name__=='__main__':main()
