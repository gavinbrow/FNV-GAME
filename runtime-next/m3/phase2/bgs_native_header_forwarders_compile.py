"""Compile private BGS header placement variants, serialized verifier lane only."""
import argparse,hashlib,json,os,re,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';D=M/'out/phase2-bgs-native-header-forwarders-v2';P=M/'out/phase2-bgsbodypart-native-destructor-rebase6757';sys.path[:0]=[str(RN),str(RN/'pinned-build')];import paths,compile_units_v3 as CU
BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--unit',type=int,required=True,choices=(620,621));a=ap.parse_args();idx=a.unit;mf=D/'manifest.json';m=json.loads(mf.read_text());fp=P/'manifest.json';f=json.loads(fp.read_text());u=json.loads((F/'build/units.json').read_text())['units'][idx]
 if sha(F/'build/units.json')!=BASE or m['base_recipe_sha256']!=BASE or sha(fp)!=m['tested_fixture_manifest_sha256'] or f['semantic_rebase']['new_units_sha256']!=BASE:raise ValueError('recipe or fixture changed')
 row=next(x for x in m['units'] if x['unit']==idx)
 if row['source']!=u['source'] or row['flags']!=u['flags'] or row['compiler']!=u['compiler']:raise ValueError('unit identity differs')
 freeze=json.loads((P/'lane-freeze.json').read_text())
 for closure in freeze['include_closure'].values():
  for item in closure['quoted']:
   p=F/item['path']
   if sha(p)!=item['sha256']:raise ValueError('source closure changed '+item['path'])
 for tag in ('prior','forwarded'):
  for rel,digest in row[tag]['files'].items():
   path=D/str(idx)/tag/rel
   if not path.exists() or sha(path)!=digest:raise ValueError('mirror changed '+rel)
   overlay=D/'payload'/tag/rel
   if overlay.exists():
    if sha(overlay)!=digest:raise ValueError('payload differs '+rel)
   elif sha(F/rel)!=digest:raise ValueError('source input differs '+rel)
 out=D/str(idx);result=out/'compile-result.json';tmp=out/'compiler-tmp'
 if result.exists() or tmp.exists() or any((out/(x+'.'+ext)).exists() for x in ('prior','forwarded') for ext in ('obj','log')):raise FileExistsError('preserve existing results')
 os.environ.update(FNV_MSVC9_ROOT=paths.MSVC9_SP1,FNV_MSVC9_RTM_ROOT=paths.MSVC9_RTM,FNV_MSVC8_ROOT=paths.MSVC8);tc=CU.find_toolchains()[u['compiler']]
 if not tc.get('ok'):raise ValueError('toolchain unavailable')
 vc=Path(tc['vc']);sdk=Path(tc['sdk']) if tc['sdk']!='None' else None;env=CU.make_env(vc,sdk);tmp.mkdir();env['TMP']=env['TEMP']=str(tmp);rows=[]
 for tag in ('prior','forwarded'):
  root=out/tag;obj=out/(tag+'.obj');log=out/(tag+'.log');cmd=[str(vc/'bin/cl.exe'),'/c','/nologo','/showIncludes']+u['flags']+['/I'+str(root/'include'),str(root/u['source']),'/Fo'+str(obj)];r=subprocess.run(cmd,cwd=root,env=env,stdin=subprocess.DEVNULL,capture_output=True,text=True,errors='replace',timeout=900);log.write_text(r.stdout+'\n'+r.stderr);shown=re.findall(r'(?im)^Note: including file:\s*(.+?)\s*$',r.stdout+'\n'+r.stderr);project=[];bad=[]
  for raw in shown:
   p=Path(raw.strip()).resolve()
   try:
    rel=p.relative_to(root.resolve()).as_posix();project.append(rel)
    if rel not in row[tag]['files']:bad.append(raw)
   except ValueError:
    if not p.is_relative_to(vc.resolve()) and not (sdk and p.is_relative_to(sdk.resolve())):bad.append(raw)
  rows.append({'tag':tag,'rc':r.returncode,'object_sha256':sha(obj) if obj.exists() else None,'include_log_sha256':sha(log),'observed_project_includes':project,'unexpected_includes':bad,'trace_valid':bool(shown) and not bad})
  if r.returncode or not obj.exists():break
 result.write_text(json.dumps({'unit_index':idx,'recipe_sha256':BASE,'manifest_sha256':sha(mf),'toolchain':tc['version'],'outcomes':rows},indent=2));print(json.dumps(rows))
 if len(rows)!=2 or any(x['rc'] or not x['trace_valid'] for x in rows):raise SystemExit(1)
if __name__=='__main__':main()
