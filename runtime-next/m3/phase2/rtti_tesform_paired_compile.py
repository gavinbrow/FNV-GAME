"""Compile pinned TESForm/BGSE original and paired private objects; serialized lane only."""
import hashlib,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';O=M/'out/phase2-tesform-paired-closure';T=M/'out/phase2-tesform-base-slots';B=M/'out/phase2-bgsencounterzone-six-override'
sys.path.insert(0,str(RN/'pinned-build'));import compile_units_v3 as CU
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if sha(O/'closure-manifest.json')!='55e56bc5b2ee85b07fffcaa5322b4dc135ad526fce5f78598421f1be1b1f5e0a':raise ValueError('closure manifest changed')
 m=json.loads((O/'closure-manifest.json').read_text());tm=json.loads((T/'manifest.json').read_text());bm=json.loads((B/'manifest.json').read_text())
 for p,d in [(F/'build/units.json',m['units_sha256']),(T/'manifest.json',m['tes_manifest_sha256']),(B/'manifest.json',m['bgs_manifest_sha256']),(M/'out/phase2-class-census/census-current.json',m['census_sha256'])]:
  if sha(p)!=d:raise ValueError('pinned input changed '+p.name)
 for row in m['closures'].values():
  for x in row['files']:
   if sha(P/x['path'])!=x['sha256']:raise ValueError('closure input changed '+x['path'])
 paths={'tes_original':F/'src/fallout_shared/tesform.cpp','tes_overlay':O/'tes/tesform.cpp','bgs_original':F/'src/bgsencounterzone.cpp','bgs_overlay':O/'bgs/bgsencounterzone.cpp'}
 tmp=O/'compiler-tmp';result=O/'compile-result.json'
 if any(p.exists() for p in [tmp,result]+[O/(x+'.obj') for x in paths]+[O/(x+'.log') for x in paths]):raise FileExistsError('refusing overwrite')
 tc=CU.find_toolchains()['sp1']
 if not tc.get('ok'):raise ValueError('VC2008 SP1 unavailable')
 vc=Path(tc['vc']);env=CU.make_env(vc,Path(tc['sdk']) if tc['sdk']!='None' else None);tmp.mkdir();env['TMP']=env['TEMP']=str(tmp);rows=[]
 for tag,src in paths.items():
  obj=O/(tag+'.obj');log=O/(tag+'.log');flags=tm['flags'] if tag.startswith('tes') else bm['flags'];inc=P/m['closures'][tag]['source_dir']
  cmd=[str(vc/'bin/cl.exe'),'/c','/nologo']+flags+['/I'+str(inc),'/I'+str(F/'include'),str(src),'/Fo'+str(obj)]
  proc=subprocess.run(cmd,cwd=O,env=env,capture_output=True,text=True,errors='replace',stdin=subprocess.DEVNULL,timeout=900);log.write_text(proc.stdout+'\n'+proc.stderr)
  row={'source':tag,'rc':proc.returncode,'object_present':obj.is_file()}
  if obj.is_file():row['object_sha256']=sha(obj)
  rows.append(row)
  if proc.returncode or not obj.is_file():break
 result.write_text(json.dumps({'compiler_version':tc['version'],'outcomes':rows},indent=2));print(json.dumps(rows))
 if len(rows)!=4 or any(x['rc'] or not x['object_present'] for x in rows):raise SystemExit(1)
if __name__=='__main__':main()
