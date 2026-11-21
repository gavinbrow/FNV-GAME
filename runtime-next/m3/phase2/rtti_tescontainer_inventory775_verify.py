"""Compile and compare TESContainer inventory unit privately; exclusive compiler lane only."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';O=M/'out/phase2-tescontainer-inventory775'
sys.path[:0]=[str(F/'tools'),str(RN),str(RN/'pinned-build'),str(H)]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate():
 if sha(O/'overlay-closure.json')!='b0024fd340f4830483788d2850a298b0d838734eb4fcee7aab8735de3e1108de':raise ValueError('overlay closure manifest changed')
 for row in json.loads((O/'overlay-closure.json').read_text())['overlay_closure']:
  if sha(P/row['path'])!=row['sha256']:raise ValueError('overlay closure input changed '+row['path'])
 m=json.loads((O/'manifest.json').read_text());items=[(F/m['source'],m['source_sha256']),(F/'build/units.json',m['units_sha256']),(F/'include/TESContainer.h',m['canonical_header_sha256']),(O/'inventorychanges_ctxr_variant.cpp',m['overlay_sha256'])]+[(F/x['path'],x['sha256']) for x in m['original_include_closure']]
 for p,d in items:
  if sha(p)!=d:raise ValueError('digest mismatch '+str(p))
 u=json.loads((F/'build/units.json').read_text())['units'][775]
 if u['source']!=m['source'] or len(u['functions'])!=1:raise ValueError('unit mismatch')
 return m,u
def compile_():
 import compile_units_v3 as cu
 m,u=validate();tmp=O/'compiler-tmp';report=O/'compile-result.json'
 if any(p.exists() for p in [tmp,report]+[O/('0775.'+t+'.'+e) for t in ('original','overlay') for e in ('obj','log')]):raise FileExistsError('refusing overwrite')
 tc=cu.find_toolchains()['sp1']
 if not tc.get('ok'):raise ValueError('compiler unavailable')
 vc=Path(tc['vc']);env=cu.make_env(vc,Path(tc['sdk']) if tc['sdk']!='None' else None);tmp.mkdir();env['TMP']=env['TEMP']=str(tmp);rows=[]
 for tag,src in [('original',F/m['source']),('overlay',O/'inventorychanges_ctxr_variant.cpp')]:
  obj=O/('0775.'+tag+'.obj');log=O/('0775.'+tag+'.log');cmd=[str(vc/'bin/cl.exe'),'/c','/nologo']+u['flags']+(['/I'+str((F/m['source']).parent)] if tag=='overlay' else [])+['/I'+str(F/'include'),str(src),'/Fo'+str(obj)]
  r=subprocess.run(cmd,cwd=O,env=env,capture_output=True,text=True,errors='replace',stdin=subprocess.DEVNULL,timeout=900);log.write_text(r.stdout+'\n'+r.stderr);rows.append({'source':tag,'rc':r.returncode,'object_sha256':sha(obj) if obj.is_file() else None})
  if r.returncode or not obj.is_file():break
 report.write_text(json.dumps({'manifest_sha256':sha(O/'manifest.json'),'outcomes':rows},indent=2));print(json.dumps(rows))
 if len(rows)!=2 or any(x['rc'] or not x['object_sha256'] for x in rows):raise SystemExit(1)
def compare_():
 from compare import Coff,Pe,compare
 import paths,rtti_hkp_viewer_compare as helper
 m,u=validate();c=json.loads((O/'compile-result.json').read_text());out=O/'comparison.json'
 if out.exists():raise FileExistsError('refusing overwrite')
 if c['manifest_sha256']!=sha(O/'manifest.json') or len(c['outcomes'])!=2:raise ValueError('compile metadata mismatch')
 objects={}
 for x in c['outcomes']:
  p=O/('0775.'+x['source']+'.obj')
  if x['rc'] or sha(p)!=x['object_sha256']:raise ValueError('object mismatch')
  objects[x['source']]=Coff(str(p))
 f=u['functions'][0];a,ar=helper.relocated(objects['original'],f['symbol'],f['size'],{});b,br=helper.relocated(objects['overlay'],f['symbol'],f['size'],{});refs={}
 for tag,obj in objects.items():
  try:refs[tag]=[{'address':x['address'],'verdict':x['verdict'],'errors':len(x['errors']),'byte_differences':len(x['byte_differences']),'failed_relocations':sum(not y.get('match') for y in x['relocations'])} for x in compare(obj,Pe(paths.REF_IMAGE),u)]
  except Exception as e:refs[tag]={'fatal':type(e).__name__+': '+str(e)}
 r={'address':f['address'],'bytes_equal':a==b,'exact_relocations_equal':ar==br,'reference':refs,'note':'literal-label differences remain failures pending explicit byte/relocation evidence'};out.write_text(json.dumps(r,indent=2));print(json.dumps(r))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=('compile','compare'));a=p.parse_args();compile_() if a.action=='compile' else compare_()
