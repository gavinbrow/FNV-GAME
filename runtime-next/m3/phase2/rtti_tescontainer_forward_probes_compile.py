"""Compile two pinned TESContainer header guard-history probes in the exclusive lane."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';O=M/'out/phase2-tescontainer-forward-probes';STAGED=M/'out/phase2-tescontainer-forward-decls'
sys.path.insert(0,str(RN/'pinned-build'));import compile_units_v3 as CU
MANIFEST_SHA='21a7bf4ab1680780ca20fd17d2b0fedf0eacc9bab84a803c5c24a6eb4d7b60af'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 manifest=O/'manifest.json'
 if sha(manifest)!=MANIFEST_SHA:raise ValueError('probe manifest changed')
 m=json.loads(manifest.read_text())
 for name,d in m['inputs'].items():
  if sha(P/name)!=d:raise ValueError('input changed '+name)
 for name,d in m['probes'].items():
  if sha(O/name)!=d:raise ValueError('probe changed '+name)
 tmp=O/'compiler-tmp';result=O/'compile-result.json'
 if any(x.exists() for x in [tmp,result]+[O/(n+'.'+ext) for n in ('root_first','local_first') for ext in ('obj','log')]):raise FileExistsError('refusing overwrite')
 tc=CU.find_toolchains()['sp1']
 if not tc.get('ok'):raise ValueError('VC2008 SP1 unavailable')
 vc=Path(tc['vc']);env=CU.make_env(vc,Path(tc['sdk']) if tc['sdk']!='None' else None);tmp.mkdir();env['TMP']=env['TEMP']=str(tmp);rows=[]
 for tag in ('root_first','local_first'):
  obj=O/(tag+'.obj');log=O/(tag+'.log');dirs=([F/'src/fallout_shared'] if tag=='local_first' else [])+[STAGED,F/'include'];cmd=[str(vc/'bin/cl.exe'),'/c','/nologo','/showIncludes','/MT','/Od','/Oy-','/GS','/EHsc','/Gy']+['/I'+str(x) for x in dirs]+[str(O/(tag+'.cpp')),'/Fo'+str(obj)]
  r=subprocess.run(cmd,cwd=O,env=env,capture_output=True,text=True,errors='replace',stdin=subprocess.DEVNULL,timeout=900);log.write_text(r.stdout+'\n'+r.stderr);shown=[Path(x.strip()).resolve() for x in re.findall(r'(?im)^Note: including file:\s*(.+?)\s*$',r.stdout+'\n'+r.stderr)];base=F/('src/fallout_shared/BaseFormComponent.h' if tag=='local_first' else 'include/BaseFormComponent.h');trace=STAGED/'TESContainer.h' in shown and base.resolve() in shown
  rows.append({'tag':tag,'rc':r.returncode,'object_sha256':sha(obj) if obj.is_file() else None,'log_sha256':sha(log),'expected_guard_context_observed':trace})
  if r.returncode or not obj.is_file() or not trace:break
 result.write_text(json.dumps({'manifest_sha256':sha(manifest),'compiler_version':tc['version'],'outcomes':rows,'scope':'two standalone include-history probes; source mirrors and production proof remain required'},indent=2));print(json.dumps(rows))
 if len(rows)!=2 or any(x['rc'] or not x['object_sha256'] or not x['expected_guard_context_observed'] for x in rows):raise SystemExit(1)
if __name__=='__main__':main()
