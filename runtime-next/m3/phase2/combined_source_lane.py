"""Exclusive-lane combined mirrors; strict functions/EH and metadata, no production writes."""
import hashlib,json,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;F=R/'fnv_decomp';L=M/'out/phase2-source-integration6757-lane';S=M/'out/phase2-source-integration6757';sys.path[:0]=[str(H),str(R/'runtime-next'),str(F/'tools')]
import rtti_mirror_prepare as prep
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
IDS=(253,370,425,620,621,2909,2910);MAN='81547b70a3471f423953800494083534349dab885afba119b525b6e522b37a41';BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';CAND='e71caa504effee614c560412dea1ecf8dc40f1317663e4799663cafc54b6c2ec'
def validate():
 if sha(S/'manifest.json')!=MAN or sha(F/'build/units.json')!=BASE or sha(S/'units.generated')!=CAND:raise ValueError('recipe or proposal changed')
 if sha(L/'tool-freeze.json')!='6672a1e7ce5baaeacb21bd8b7888854106a146850fa904977066a6a0615552a0':raise ValueError('tool freeze changed')
 freeze=json.loads((L/'tool-freeze.json').read_text())
 for name,digest in freeze['files'].items():
  if sha(R/name)!=digest:raise ValueError('tool or census changed: '+name)
 if sha(L/'capture.json')!=freeze['capture_sha256']:raise ValueError('capture manifest changed')
 cap=json.loads((L/'capture.json').read_text());records={x['unit']:x for x in cap['captured']}
 if set(records)!=set(IDS):raise ValueError('capture missing units')
 for i in IDS:
  d=L/str(i);r=records[i]
  if sha(d/'mirror-manifest.json')!=r['manifest_sha256'] or sha(d/'production-baseline.obj')!=r['production_object_sha256']:raise ValueError('capture changed')
 return json.loads((F/'build/units.json').read_text())['units'],json.loads((S/'units.generated').read_text())['units']
def compile_all():
 validate();import rtti_mirror_compile as c
 def transition(old,new,current):
  if hashlib.sha256(current).hexdigest()!=BASE:raise ValueError('live recipe changed')
  return json.loads(current)
 prep.transition=transition;old=c.CU.make_env
 def clean(vc,sdk):
  e=old(vc,sdk)
  for k in list(e):
   if k.upper().startswith(('FNV_','CODEX_NEGATIVE')) or k.upper() in ('CL','_CL_'):e.pop(k,None)
  return e
 c.CU.make_env=clean
 for i in IDS:
  sys.argv=['rtti_mirror_compile.py','--out',str(L/str(i))];c.main()
def compare_all():
 before,after=validate();from compare import Coff,Pe,compare
 from build_and_match import eh_sections,recipe_names
 import paths,class_metadata_compare as cm
 pe=Pe(paths.REF_IMAGE);results={}
 for i in IDS:
  d=L/str(i);run=json.loads((d/'compile-result.json').read_text());out={}
  if len(run['outcomes'])!=2 or any(x['rc'] or not x['trace_valid'] or sha(d/(x['tag']+'.obj'))!=x['object_sha256'] for x in run['outcomes']):raise ValueError('compiler/trace/object mismatch '+str(i))
  for tag,unit,namespace in (('production',before[i],before),('original',before[i],before),('candidate',after[i],after)):
   c=Coff(str(d/('production-baseline.obj' if tag=='production' else tag+'.obj')))
   try:
    rows=compare(c,pe,unit);sections,inferred,errors=eh_sections(c,pe,unit,rows,recipe_names(namespace))
    out[tag]={'object_sha256':sha(d/('production-baseline.obj' if tag=='production' else tag+'.obj')),'functions':len(rows),'matches':sum(x['verdict']=='match' for x in rows),'function_failures':[{'address':x['address'],'verdict':x['verdict'],'errors':x['errors']} for x in rows if x['verdict']!='match'],'eh_sections':len(sections),'eh_failed':[x for x in sections if not x[2]],'eh_errors':errors,'eh_inferred':{k:hex(v) for k,v in inferred.items()}}
   except Exception as e:out[tag]={'error':type(e).__name__+': '+str(e)}
  results[str(i)]=out
 census_path=M/'out/phase2-class-census/census-6757.json';census=json.loads(census_path.read_text())
 if census['inputs']['units_sha256']!=BASE:raise ValueError('metadata census stale')
 graphs={}
 for name in ('.?AVBGSBodyPart@@','.?AVTESModelPSA@@'):
  try:graphs[name]=cm.compare_class(L/'620/candidate.obj',after[620],after,census,name)
  except Exception as e:graphs[name]={'error':type(e).__name__+': '+str(e)}
 # Finite weak auxiliary and native body checks; final linked ownership remains separate.
 from rtti_hkp_viewer_compare import relocated
 c=Coff(str(L/'620/candidate.obj'));oc=Coff(str(L/'2909/production-baseline.obj'))
 primary='??_ETESModelPSA@@UAEPAXI@Z';fallback='??_GTESModelPSA@@UAEPAXI@Z';dtor='??1TESModelPSA@@UAE@XZ';weak=[(i,x) for i,x in c.symbols.items() if x['name']==primary and x['storage']==105]
 weakproof={'status':'failed'}
 try:
  if len(weak)!=1:raise ValueError('weak primary ambiguous')
  idx,kind=struct.unpack_from('<II',c.data,struct.unpack_from('<I',c.data,8)[0]+18*(weak[0][0]+1))
  defs=[x for x in c.by_name.get(fallback,[]) if x['section']>0 and x['storage']==2]
  if kind!=2 or c.symbols[idx]['name']!=fallback or len(defs)!=1:raise ValueError('weak fallback/definition mismatch')
  a,ar=relocated(c,fallback,44,{dtor:'??1BGSTextureModel@@UAE@XZ'});b,br=relocated(c,'?FUN_005e3c30@BGSTextureModel@@QAEPAXI@Z',44,{})
  if a!=b or ar!=br:raise ValueError('wrapper body differs')
  a,ar=relocated(c,dtor,19,{'??1TESModel@@UAE@XZ':'??1TESModel@@QAE@XZ'});b,br=relocated(oc,'?FUN_0051b950@FUN_0051b950_shell@@QAEXXZ',19,{})
  if a!=b or ar!=br:raise ValueError('implicit destructor differs')
  weakproof={'status':'finite COFF checks passed','primary':primary,'fallback':fallback,'aux_characteristics':kind,'fallback_defined_count':len(defs),'wrapper_44_equal':True,'implicit_destructor_19_equal':True,'final_link_ownership':'not verified'}
 except Exception as e:weakproof={'status':'failed','error':type(e).__name__+': '+str(e)}
 out={'scope':'strict mapped functions, ordinary EH and metadata; weak/COMDAT final ownership requires independent review','proposal_sha256':MAN,'units':results,'metadata':graphs,'weak_comdat':weakproof,'full_gate':'NOT VERIFIED'}
 p=L/'combined-comparison.json'
 if p.exists():raise FileExistsError(p)
 p.write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps({'results':{k:{t:(v.get('matches'),v.get('functions')) for t,v in x.items()} for k,x in results.items()},'output':str(p)}))
if __name__=='__main__':{'compile':compile_all,'compare':compare_all}[sys.argv[1]]()
