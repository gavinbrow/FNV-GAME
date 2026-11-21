"""Guarded private unit370 compiler lane and 178-function comparison."""
import copy,hashlib,json,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';P=M/'out/phase2-bfc-370-pointer-split';O=M/'out/phase2-bfc-370-pointer-split-mirror';sys.path[:0]=[str(H),str(RN/'pinned-build'),str(F/'tools'),str(RN)]
import rtti_mirror_prepare as prep
EXPECTED='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def transition(old,new,current):
 if hashlib.sha256(current).hexdigest()!=EXPECTED:raise ValueError('recipe changed')
 return json.loads(current)
prep.transition=transition
def freeze():
 m=json.loads((O/'mirror-manifest.json').read_text());p=json.loads((P/'manifest.json').read_text())
 if sha(F/'build/units.json')!=EXPECTED or sha(P/'manifest.json')!=m['proposal_sha256'] or sha(P/'unit-overlay.json')!=m['unit_overlay_sha256']:raise ValueError('input changed')
 archive=M/'out/phase2-bfc-cohort-production-archive/0370.obj';shutil.copyfile(archive,O/'production-baseline.obj')
 m['production_object_sha256']=sha(O/'production-baseline.obj');m['tooling_sha256']={n:sha(H/n) for n in ('bfc_370_pointer_split_lane.py','rtti_mirror_prepare.py','rtti_mirror_compile.py','rtti_hkp_viewer_compare.py')}
 (O/'mirror-manifest.json').write_text(json.dumps(m,indent=2),encoding='utf8');print(json.dumps({'manifest_sha256':sha(O/'mirror-manifest.json'),'production_object_sha256':m['production_object_sha256']}))
def validate():
 m=json.loads((O/'mirror-manifest.json').read_text())
 if sha(F/'build/units.json')!=EXPECTED or sha(P/'manifest.json')!=m['proposal_sha256'] or sha(P/'unit-overlay.json')!=m['unit_overlay_sha256'] or sha(O/'production-baseline.obj')!=m['production_object_sha256']:raise ValueError('frozen input changed')
 for n,h in m['tooling_sha256'].items():
  if sha(H/n)!=h:raise ValueError('tool changed '+n)
 return m
def compile_lane():
 validate();import rtti_mirror_compile as d
 old=d.CU.make_env
 def clean(vc,sdk):
  env=old(vc,sdk)
  for key in list(env):
   if key.upper().startswith(('FNV_','CODEX_NEGATIVE')) or key.upper() in ('CL','_CL_'):env.pop(key,None)
  return env
 d.CU.make_env=clean;sys.argv=['rtti_mirror_compile.py','--out',str(O)];d.main()
def compare_lane():
 from compare import Coff,Pe,compare
 from rtti_hkp_viewer_compare import relocated
 from build_and_match import eh_sections,recipe_names
 import paths
 m=validate();run=json.loads((O/'compile-result.json').read_text());objs={}
 for r in run['outcomes']:
  path=O/(r['tag']+'.obj')
  if r['rc'] or not r['trace_valid'] or sha(path)!=r['object_sha256']:raise ValueError('invalid object')
  objs[r['tag']]=Coff(str(path))
 if set(objs)!={'original','candidate'}:raise ValueError('missing mirrors')
 units=json.loads((F/'build/units.json').read_bytes())['units'];u=units[370];overlay=json.loads((P/'unit-overlay.json').read_text());expected=copy.deepcopy(u);expected['symbols'].update({'??0PtrA96@@QAE@H@Z':'0x00528cb0','??0PtrB96@@QAE@H@Z':'0x00528cb0'})
 if overlay!=expected or len(u['functions'])!=178:raise ValueError('unexpected overlay')
 norm={'??0PtrA96@@QAE@H@Z':'??0FUN_00528cb0@@QAE@H@Z','??0PtrB96@@QAE@H@Z':'??0FUN_00528cb0@@QAE@H@Z','?FUN_006f74f0@PtrA96@@QAEXPAX@Z':'?FUN_006f74f0@FUN_00528cb0@@QAEXH@Z','?FUN_0092c8b0@PtrB96@@QAEXPAX@Z':'?FUN_0092c8b0@FUN_00528cb0@@QAEXH@Z'}
 facts=[]
 for f in u['functions']:
  try:
   a,ar=relocated(objs['original'],f['symbol'],f['size'],{});b,br=relocated(objs['candidate'],f['symbol'],f['size'],norm);facts.append({'address':f['address'],'bytes_equal':a==b,'normalized_relocations_equal':ar==br})
  except (ValueError,KeyError,IndexError) as e:facts.append({'address':f['address'],'error':str(e)})
 pe=Pe(paths.REF_IMAGE);refs={};eh={}
 for label,c,spec in [('production',Coff(str(O/'production-baseline.obj')),u),('original',objs['original'],u),('candidate',objs['candidate'],overlay)]:
  try:
   rows=compare(c,pe,spec);refs[label]=[{'address':x['address'],'verdict':x['verdict'],'errors':x['errors']} for x in rows];sections,inf,errors=eh_sections(c,pe,spec,rows,recipe_names(units));eh[label]={'sections':len(sections),'failed':sum(not x[2] for x in sections),'errors':errors,'inferred':{k:hex(v) for k,v in inf.items()}}
  except Exception as e:refs[label]={'fatal':type(e).__name__+': '+str(e)}
 out=O/'comparison.json'
 with out.open('x',encoding='utf8') as f:json.dump({'functions':facts,'reference':refs,'eh':eh,'normalization':norm,'scope':'private comparison, inferred EH names reported separately'},f,indent=2)
 print(json.dumps({'functions':len(facts),'bytes_equal':sum(x.get('bytes_equal',False) for x in facts),'normalized_relocations_equal':sum(x.get('normalized_relocations_equal',False) for x in facts),'eh':eh}))
if __name__=='__main__':{'freeze':freeze,'compile':compile_lane,'compare':compare_lane}[sys.argv[1]]()
