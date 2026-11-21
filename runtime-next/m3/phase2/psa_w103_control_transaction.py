"""Hash-guarded private tool transaction; apply only under explicit coordinator grant."""
import argparse,hashlib,json,os,sys,tempfile,time
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;T=M/'out/phase2-psa-w103-control-patch';sys.path.insert(0,str(H));import rtti_tesform_bindings_transaction as locks
PIN='cd1971f4edf3d6c98d0da55fc8018ce910db22cf81ecee4dd0b097c9e8a02f71';RECIPE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68';h=lambda b:hashlib.sha256(b).hexdigest()
def atomic(path,data,tempdir):
 fd,name=tempfile.mkstemp(prefix='psa-tool-',dir=tempdir);tmp=Path(name)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(tmp,path)
 except BaseException:
  if tmp.exists():tmp.unlink()
  raise
def execute(root,package,manifest,action,writer=atomic):
 if action not in ('apply','restore','recover'):raise ValueError('bad action')
 plans=[]
 for z in manifest['files']:
  path=(root/z['path']).resolve()
  if not path.is_relative_to(root.resolve()):raise ValueError('path escape')
  old=(package/'original'/z['path']).read_bytes();new=(package/'payload'/z['path']).read_bytes();cur=path.read_bytes()
  if h(old)!=z['old_sha256'] or h(new)!=z['new_sha256']:raise ValueError('payload mismatch')
  allowed=[z['old_sha256']] if action=='apply' else [z['new_sha256']] if action=='restore' else [z['old_sha256'],z['new_sha256']]
  if h(cur) not in allowed:raise ValueError('unknown preimage '+z['path'])
  plans.append((path,cur,new if action=='apply' else old))
 changed=[]
 try:
  for path,cur,wanted in plans:
   if cur!=wanted:writer(path,wanted,package);changed.append((path,cur))
  if any(path.read_bytes()!=wanted for path,_,wanted in plans):raise ValueError('postwrite mismatch')
 except BaseException:
  for path,cur in reversed(changed):atomic(path,cur,package)
  raise
 return len(plans)
def main():
 a=argparse.ArgumentParser();a.add_argument('action',choices=('apply','restore','recover'));args=a.parse_args();guards=locks.acquire_guard()
 try:
  raw=(T/'transaction-manifest.json').read_bytes()
  if h(raw)!=PIN or h((R/'fnv_decomp/build/units.json').read_bytes())!=RECIPE:raise ValueError('transaction or recipe changed')
  m=json.loads(raw)
  if h((T/'manifest.json').read_bytes())!=m['proposal_sha256']:raise ValueError('proposal changed')
  result=execute(R,T,m,args.action)
  print(json.dumps({'action':args.action,'files':result,'manifest':PIN}))
 finally:
  for p in reversed(guards):p.unlink()
if __name__=='__main__':main()
