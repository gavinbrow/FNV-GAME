"""Compile private scratch common-source fixture on the exclusive lane only."""
import hashlib,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';O=M/'out/phase2-scratch258-common-fixture-v2';sys.path.insert(0,str(RN/'pinned-build'));import compile_units_v3 as CU
PIN='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 meta=json.loads((O/'manifest.json').read_bytes());units=F/'build/units.json'
 if sha(units)!=PIN or meta['recipe_sha256']!=PIN:raise ValueError('recipe changed')
 for n,d in meta['outputs'].items():
  if sha(O/n)!=d:raise ValueError('fixture changed '+n)
 for k,path in [('unit258',F/'src/fallout/ai/actor_o2_nood_variant.cpp'),('unit2662',F/'src/staging/blk_00620000_od.cpp')]:
  if sha(path)!=meta['source_inputs'][k]:raise ValueError('source owner changed')
 out=O/'compile-result.json';tmp=O/'tmp'
 if out.exists() or tmp.exists() or any((O/(n+'.obj')).exists() for n in ('od','o2')):raise FileExistsError('no overwrite')
 tc=CU.find_toolchains()['sp1']
 if not tc.get('ok'):raise ValueError('toolchain unavailable')
 vc=Path(tc['vc']);env=CU.make_env(vc,Path(tc['sdk']) if tc['sdk']!='None' else None);tmp.mkdir();env['TEMP']=env['TMP']=str(tmp);rows=[]
 for tag,src in [('od','owner_od.cpp'),('o2','scratch_o2.cpp')]:
  obj=O/(tag+'.obj');flags=meta['compile_variants'][tag]['flags'];p=subprocess.run([str(vc/'bin/cl.exe'),'/c','/nologo','/showIncludes']+flags+['/I'+str(O),str(O/src),'/Fo'+str(obj)],cwd=O,env=env,capture_output=True,text=True,errors='replace',stdin=subprocess.DEVNULL,timeout=300);(O/(tag+'.log')).write_text(p.stdout+'\n'+p.stderr)
  row={'tag':tag,'rc':p.returncode,'object_present':obj.exists(),'object_sha256':sha(obj) if obj.exists() else None,'log_sha256':sha(O/(tag+'.log'))};rows.append(row)
  if p.returncode or not obj.exists():break
 out.write_text(json.dumps({'manifest_sha256':sha(O/'manifest.json'),'compiler_version':tc['version'],'outcomes':rows},indent=2));print(json.dumps(rows))
 if len(rows)!=2 or any(r['rc'] or not r['object_present'] for r in rows):raise SystemExit(1)
if __name__=='__main__':main()
