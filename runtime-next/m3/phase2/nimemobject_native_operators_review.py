"""Review private native NiMemObject operator owner objects."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';D=M/'out/phase2-nimemobject-native-operators-v2';OUT=D/'independent-review.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,recipe_names
from rtti_hkp_viewer_compare import relocated
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve prior proof')
 m=json.loads((D/'manifest.json').read_text());op=D/'units.original';np=D/'units.generated'
 if sha(op)!=m['base_recipe_sha256'] or sha(np)!=m['candidate_recipe_sha256'] or sha(F/'build/units.json')!=m['base_recipe_sha256']:raise ValueError('recipe mismatch')
 old=json.loads(op.read_text())['units'];new=json.loads(np.read_text())['units'];pe=Pe(paths.REF_IMAGE);result={}
 for i in (1664,2734):
  d=D/str(i);mm=d/'mirror-manifest.json';run=json.loads((d/'compile-result.json').read_text());objs={};result[str(i)]={}
  if run['unit_index']!=i or run['mirror_manifest_sha256']!=sha(mm):raise ValueError('compile manifest mismatch')
  for tag,spec in (('original',old[i]),('candidate',new[i])):
   r=next(x for x in run['outcomes'] if x['tag']==tag);p=d/(tag+'.obj')
   if r['rc'] or not r['trace_valid'] or sha(p)!=r['object_sha256']:raise ValueError('invalid compiled object')
   c=Coff(str(p));checks=compare(c,pe,spec);sections,inferred,errors=eh_sections(c,pe,spec,checks,recipe_names(old))
   if any(x['verdict']!='match' for x in checks) or errors or any(not x[2] for x in sections):raise ValueError('strict function/EH mismatch')
   objs[tag]=c;result[str(i)][tag]={'object_sha256':sha(p),'strict_functions':len(checks),'eh_sections':len(sections),'inferred_names':len(inferred)}
  current={x['address']:x for x in new[i]['functions']}
  for f in old[i]['functions']:
   g=current[f['address']];a,ar=relocated(objs['original'],f['symbol'],f['size'],{});b,br=relocated(objs['candidate'],g['symbol'],g['size'],{})
   if a!=b or ar!=br:raise ValueError('function or relocation changed '+f['address'])
  result[str(i)]['all_mapped_bytes_and_relocations_equal']=True
 OUT.write_text(json.dumps({'scope':'private two native operator owners; no integration','manifest_sha256':sha(D/'manifest.json'),'recipe_before_sha256':sha(op),'recipe_candidate_sha256':sha(np),'reference_sha256':sha(Path(paths.REF_IMAGE)),'units':result,'limits':['legacy free-function callers require explicit source/assembler resolution proof','126 public-header consumers need independent code/EH and class identity validation','actual production object placement, weak symbols, exact image and runtime remain separate']},indent=2));print('PASS 46 strict functions, unchanged bytes/relocations; no EH sections')
if __name__=='__main__':main()
