"""Private production-layout mirror preparation, compilation, and comparison."""
import copy,hashlib,json,os,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;ROOT=RN.parent;F=ROOT/'fnv_decomp';PROPOSAL=M/'out/phase2-forenderedmenu-node-view';OUT=M/'out/phase2-forenderedmenu-node-view-mirror'
sys.path[:0]=[str(H),str(RN/'pinned-build'),str(F/'tools'),str(RN)]
import rtti_mirror_prepare as prep
EXPECTED='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def transition(old,new,current):
 if hashlib.sha256(current).hexdigest()!=EXPECTED:raise ValueError('units hash changed')
 return json.loads(current)
prep.transition=transition
def prepare():
 proposal=json.loads((PROPOSAL/'manifest.json').read_text());candidate=PROPOSAL/'forenderedmenu.cpp'
 if proposal['units_sha256']!=EXPECTED or sha(candidate)!=proposal['candidate_source_sha256'] or sha(PROPOSAL/'unit-overlay.json')!=proposal['unit_overlay_sha256']:raise ValueError('proposal changed')
 meta=prep.prepare(proposal['source'],{proposal['source']:candidate.read_bytes()},OUT)
 meta['units_sha256']=EXPECTED;meta['reviewed_units_sha256']=EXPECTED
 production=RN/'pinned-build/obj_v3/0425.obj';shutil.copyfile(production,OUT/'production-baseline.obj')
 meta['production_object_sha256']=sha(OUT/'production-baseline.obj')
 meta['proposal_sha256']=sha(PROPOSAL/'manifest.json');meta['unit_overlay_sha256']=sha(PROPOSAL/'unit-overlay.json')
 meta['tooling_sha256']={n:sha(H/n) for n in ('forenderedmenu_node_view_lane.py','rtti_mirror_prepare.py','rtti_mirror_compile.py','rtti_hkp_viewer_compare.py')}
 (OUT/'mirror-manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
 print(json.dumps({'manifest_sha256':sha(OUT/'mirror-manifest.json'),'production_object_sha256':meta['production_object_sha256'],'original_files':len(meta['original']['files']),'candidate_files':len(meta['candidate']['files'])}))
def validate():
 m=json.loads((OUT/'mirror-manifest.json').read_text())
 if sha(F/'build/units.json')!=EXPECTED or sha(PROPOSAL/'manifest.json')!=m['proposal_sha256'] or sha(PROPOSAL/'unit-overlay.json')!=m['unit_overlay_sha256']:raise ValueError('recipe/proposal changed')
 if sha(OUT/'production-baseline.obj')!=m['production_object_sha256']:raise ValueError('archived production object changed')
 for name,digest in m['tooling_sha256'].items():
  if sha(H/name)!=digest:raise ValueError('tooling changed '+name)
 return m
def compile_lane():
 validate();import rtti_mirror_compile as driver
 original=driver.CU.make_env
 def clean(vc,sdk):
  env=original(vc,sdk)
  for key in list(env):
   if key.upper().startswith(('FNV_','CODEX_NEGATIVE')) or key.upper() in ('CL','_CL_'):env.pop(key,None)
  return env
 driver.CU.make_env=clean
 sys.argv=['rtti_mirror_compile.py','--out',str(OUT)];driver.main()
def compare_lane():
 from compare import Coff,Pe,compare
 from rtti_hkp_viewer_compare import relocated
 import paths
 m=validate();run=json.loads((OUT/'compile-result.json').read_text());objects={}
 for row in run['outcomes']:
  p=OUT/(row['tag']+'.obj')
  if row['rc'] or not row['trace_valid'] or sha(p)!=row['object_sha256']:raise ValueError('invalid compiler result')
  objects[row['tag']]=Coff(str(p))
 if set(objects)!={'original','candidate'}:raise ValueError('missing mirror')
 u=json.loads((F/'build/units.json').read_bytes())['units'][425];overlay=json.loads((PROPOSAL/'unit-overlay.json').read_text());old='?GetPartName@BGSBodyPart@@QAEPAUNiAVObjectS@@XZ';new='?GetMenuNode@FORenderedMenuNodeView@@QAEPAUNiAVObjectS@@XZ'
 base=copy.deepcopy(u);base['symbols'].pop(old);base['symbols'][new]='0x006838b0'
 if base!=overlay or len(u['functions'])!=44:raise ValueError('overlay exceeds one symbol change')
 facts=[]
 for f in u['functions']:
  try:
   a,ar=relocated(objects['original'],f['symbol'],f['size'],{});b,br=relocated(objects['candidate'],f['symbol'],f['size'],{new:old})
   facts.append({'address':f['address'],'bytes_equal':a==b,'normalized_relocations_equal':ar==br})
  except (ValueError,KeyError,IndexError) as e:facts.append({'address':f['address'],'error':str(e)})
 pe=Pe(paths.REF_IMAGE);refs={}
 for name,coff,spec in [('production',Coff(str(OUT/'production-baseline.obj')),u),('original',objects['original'],u),('candidate',objects['candidate'],overlay)]:
  try:
   r=compare(coff,pe,spec);refs[name]=[{'address':x['address'],'verdict':x['verdict'],'errors':x['errors']} for x in r]
  except Exception as e:refs[name]={'fatal':type(e).__name__+': '+str(e)}
 report={'scope':'private function and reference comparison; EH/section review separate','functions':facts,'reference':refs,'symbol_before':old,'symbol_after':new,'target':'0x006838b0','manifest_sha256':sha(OUT/'mirror-manifest.json')}
 out=OUT/'comparison.json'
 with out.open('x',encoding='utf8') as q:json.dump(report,q,indent=2)
 print(json.dumps({'functions':len(facts),'bytes_equal':sum(x.get('bytes_equal',False) for x in facts),'normalized_relocations_equal':sum(x.get('normalized_relocations_equal',False) for x in facts),'report':str(out)}))
if __name__=='__main__':{'prepare':prepare,'compile':compile_lane,'compare':compare_lane}[sys.argv[1]]()
