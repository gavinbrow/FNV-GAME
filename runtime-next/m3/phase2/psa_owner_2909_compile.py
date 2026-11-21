"""Compile a prepared mirror using production include order, on exclusive lane only."""
import argparse,hashlib,json,os,re,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';sys.path[:0]=[str(H),str(RN),str(RN/'pinned-build')];import rtti_mirror_prepare as prep,paths
import compile_units_v3 as CU
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--unit',required=True,type=int);a=p.parse_args();out=a.out.resolve()
 try:out.relative_to((M/'out').resolve())
 except ValueError:raise ValueError('private output required')
 manifest=out/'mirror-manifest.json';m=json.loads(manifest.read_text());raw=(F/'build/units.json').read_bytes();idx=a.unit
 if hashlib.sha256(raw).hexdigest()!='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c' or idx not in (2909,2910):raise ValueError('recipe or unit mismatch')
 units=json.loads(raw)['units']
 if idx<0 or idx>=len(units):raise ValueError('unit index outside recipe')
 u=units[idx]
 if u['source']!=m['source']:raise ValueError('indexed source mismatch')
 if 'original_inputs' not in m:raise ValueError('mirror lacks production input hashes; regenerate to a new output')
 for name,digest in m['original_inputs'].items():
  if sha(F/prep.logical(name))!=digest:raise ValueError('production input changed '+name)
 for tag in ('original','candidate'):
  for name,digest in m[tag]['files'].items():
   q=out/tag/prep.logical(name)
   if not q.is_file() or sha(q)!=digest:raise ValueError('mirror changed '+name)
  for edge in m[tag]['edges']:
   if edge['resolved'] not in m[tag]['files']:raise ValueError('include outside captured graph')
 tmp=out/'compiler-tmp';result=out/'compile-result.json'
 if any(x.exists() for x in [tmp,result]+[out/(tag+'.'+ext) for tag in ('original','candidate') for ext in ('obj','log')]):raise FileExistsError('refusing overwrite')
 os.environ.update(FNV_MSVC9_ROOT=paths.MSVC9_SP1,FNV_MSVC9_RTM_ROOT=paths.MSVC9_RTM,FNV_MSVC8_ROOT=paths.MSVC8)
 tc=CU.find_toolchains()[u['compiler']]
 if not tc.get('ok'):raise ValueError('toolchain unavailable')
 vc=Path(tc['vc']);env=CU.make_env(vc,Path(tc['sdk']) if tc['sdk']!='None' else None);tmp.mkdir();env['TMP']=env['TEMP']=str(tmp);rows=[]
 for tag in ('original','candidate'):
  root=out/tag;source=root/m['source'];obj=out/(tag+'.obj');log=out/(tag+'.log');cmd=[str(vc/'bin/cl.exe'),'/c','/nologo','/showIncludes']+u['flags']+['/I'+str(root/'include'),str(source),'/Fo'+str(obj)]
  r=subprocess.run(cmd,cwd=root,env=env,stdin=subprocess.DEVNULL,capture_output=True,text=True,errors='replace',timeout=900);log.write_text(r.stdout+'\n'+r.stderr)
  shown=re.findall(r'(?im)^Note: including file:\s*(.+?)\s*$',r.stdout+'\n'+r.stderr);project=[];system=[];unrecognized=[]
  sdk=Path(tc['sdk']).resolve() if tc['sdk']!='None' else None
  for raw in shown:
   path=Path(raw.strip()).resolve()
   try:
    logical=path.relative_to(root.resolve()).as_posix();project.append(logical)
    if logical not in m[tag]['files']:unrecognized.append(raw)
    continue
   except ValueError:pass
   if path.is_relative_to(vc.resolve()) or (sdk is not None and path.is_relative_to(sdk)):system.append(raw)
   else:unrecognized.append(raw)
  rows.append({'tag':tag,'rc':r.returncode,'object_sha256':sha(obj) if obj.is_file() else None,'show_includes_log_sha256':sha(log),'observed_project_includes':project,'system_include_count':len(system),'unrecognized_includes':unrecognized,'trace_valid':bool(shown) and not unrecognized})
  if r.returncode or not obj.is_file():break
 result.write_text(json.dumps({'unit_index':idx,'flags':u['flags'],'compiler_version':tc['version'],'mirror_manifest_sha256':sha(manifest),'outcomes':rows,'note':'review actual /showIncludes against logical include graph; compare final production object before literal bindings'},indent=2));print(json.dumps(rows))
 if len(rows)!=2 or any(x['rc'] or not x['object_sha256'] or not x['trace_valid'] for x in rows):raise SystemExit(1)
if __name__=='__main__':main()
