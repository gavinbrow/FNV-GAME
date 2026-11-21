"""Guard staged typed TESForm/BGSE edits; never run a build with mirror labels."""
import argparse,hashlib,json,os,sys,tempfile,time
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';T=M/'out/phase2-tesform-typed-transaction';sys.path.insert(0,str(H));import rtti_tesform_bindings_transaction as lock
PROOF='20cbe796e1b67856f568f8dadfe925dfac6d021054a5dd219389e7fdada32f89';FA='fa36603e3e9a2ea495644f383db983a9269d2e7cf558282a80746439386dbfc8';REL=['src/fallout_shared/tesform.cpp','src/fallout_shared/tesform_TESForm.h','src/bgsencounterzone.cpp','src/bgsencounterzone_decls.h','src/bgsencounterzone_TESForm.h','build/units.json']
def sha(b):return hashlib.sha256(b).hexdigest()
def manifest():
 b=(T/'manifest.json').read_bytes()
 if sha(b)!=PROOF:raise ValueError('reviewed transaction manifest changed')
 m=json.loads(b)
 if m['base_units_sha256']!=FA or [x['path'] for x in m['files']]!=REL or len(m['unit998_function_remaps'])!=10 or len(m['unit2_function_remaps'])!=9:raise ValueError('transaction scope changed')
 sys.path.insert(0,str(RN));import paths as buildpaths
 if sha(Path(buildpaths.REF_IMAGE).read_bytes())!='df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7':raise ValueError('reference image changed')
 for name,d in m['evidence_sha256'].items():
  if sha((M/'out'/name).read_bytes())!=d:raise ValueError('proof changed '+name)
 return m

def atomic_write(path,data):
 fd,name=tempfile.mkstemp(prefix='typed-class-',dir=T);temp=Path(name)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(temp,path)
 except BaseException:
  if temp.exists():temp.unlink()
  raise

def validate_closures():
 for folder in ('phase2-tesform-typed-mirror','phase2-bgs-typed-mirror'):
  c=json.loads((M/'out'/folder/'mirror-manifest.json').read_text())
  for rel,d in c['original_inputs'].items():
   p=(F/rel).resolve()
   if not p.is_relative_to(F.resolve()) or sha(p.read_bytes())!=d:raise ValueError('original source closure changed '+rel)

def run(action,ack=False):
 if action=='apply' and not ack:raise ValueError('explicit mirror-label acknowledgment required; no build until production reproof')
 guards=lock.acquire_guard()
 try:
  m=manifest();ops=[]
  if action=='apply':validate_closures()
  if action=='restore' and not (T/'applied.json').exists():raise ValueError('transaction not applied')
  marker=T/(('recover-%d-%d.json'%(os.getpid(),time.time_ns())) if action=='recover' else action+'-result.json')
  if marker.exists():raise FileExistsError('action already recorded')
  for x in m['files']:
   p=(F/x['path']).resolve()
   if not p.is_relative_to(F.resolve()):raise ValueError('path escapes source tree')
   old=(T/x['original']).read_bytes();new=(T/x['generated']).read_bytes();cur=p.read_bytes()
   if sha(old)!=x['old_sha256'] or sha(new)!=x['new_sha256']:raise ValueError('payload changed')
   valid=[x['old_sha256']] if action=='apply' else [x['new_sha256']] if action=='restore' else [x['old_sha256'],x['new_sha256']]
   if sha(cur) not in valid:raise ValueError('unknown file state '+x['path'])
   ops.append((p,cur,new if action=='apply' else old))
  changed=[];result_owned=False;applied_owned=False
  try:
   for p,cur,new in ops:
    if cur!=new:atomic_write(p,new);changed.append((p,cur))
   with marker.open('x',encoding='utf8') as f:
    result_owned=True;json.dump({'action':action,'manifest_sha256':PROOF,'status':'production-literal-reproof-required' if action=='apply' else 'restored'},f)
   if action=='apply':
    with (T/'applied.json').open('x',encoding='utf8') as f:
     applied_owned=True;json.dump({'manifest_sha256':PROOF,'production_literal_reproof_required':True},f)
  except BaseException:
   for p,cur in reversed(changed):atomic_write(p,cur)
   if result_owned and marker.exists():marker.unlink()
   if applied_owned and (T/'applied.json').exists():(T/'applied.json').unlink()
   raise
  print(json.dumps({'action':action,'files':len(ops),'production_literal_reproof_required':action=='apply'}))
 finally:
  for p in reversed(guards):p.unlink()
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=('apply','restore','recover'));p.add_argument('--ack-mirror-labels',action='store_true');a=p.parse_args();run(a.action,a.ack_mirror_labels)
if __name__=='__main__':main()
