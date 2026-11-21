"""Guard private four-file flag-pair transaction; production reproof mandatory."""
import argparse,hashlib,json,os,sys,tempfile,time
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';T=M/'out/phase2-flagpairs-transaction';sys.path.insert(0,str(H));import rtti_tesform_bindings_transaction as locks
PIN='58540236d8d682fbd2838599e6ee9d071156b903e3cb48931ae363cbe24a0fe9';REL=['src/fallout_shared/tesform.cpp','src/fallout_shared/tesform_TESForm.h','src/bgsencounterzone_TESForm.h','build/units.json']
def sha(b):return hashlib.sha256(b).hexdigest()
def atomic(path,data):
 fd,name=tempfile.mkstemp(prefix='flag-pairs-',dir=T);p=Path(name)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(p,path)
 except BaseException:
  if p.exists():p.unlink()
  raise
def run(action,ack=False):
 if action=='apply' and not ack:raise ValueError('acknowledge production literal reproof before apply')
 guards=locks.acquire_guard()
 try:
  raw=(T/'manifest.json').read_bytes()
  if sha(raw)!=PIN:raise ValueError('manifest changed')
  m=json.loads(raw)
  if [x['path'] for x in m['files']]!=REL or len(m['getter_folds'])!=2 or len(m['setter_alignments'])!=3:raise ValueError('scope changed')
  for rel,d in m['evidence_sha256'].items():
   if sha((M/'out'/rel).read_bytes())!=d:raise ValueError('evidence changed '+rel)
  if action=='apply':
   for folder in ('phase2-tesform-two-flagpairs-mirror','phase2-bgs-two-flagpairs-mirror'):
    cm=json.loads((M/'out'/folder/'mirror-manifest.json').read_bytes())
    for rel,d in cm['original_inputs'].items():
     p=(F/rel).resolve()
     if not p.is_relative_to(F.resolve()) or sha(p.read_bytes())!=d:raise ValueError('closure changed '+rel)
  if action=='restore' and not (T/'applied.json').exists():raise ValueError('not applied')
  marker=T/(('recover-%d-%d.json'%(os.getpid(),time.time_ns())) if action=='recover' else action+'-result.json')
  if marker.exists():raise FileExistsError('action already recorded')
  ops=[]
  for x in m['files']:
   p=(F/x['path']).resolve()
   if not p.is_relative_to(F.resolve()):raise ValueError('path escapes source')
   old=(T/x['original']).read_bytes();new=(T/x['generated']).read_bytes();cur=p.read_bytes()
   if sha(old)!=x['old_sha256'] or sha(new)!=x['new_sha256']:raise ValueError('payload changed')
   allowed=[x['old_sha256']] if action=='apply' else [x['new_sha256']] if action=='restore' else [x['old_sha256'],x['new_sha256']]
   if sha(cur) not in allowed:raise ValueError('unknown target state '+x['path'])
   ops.append((p,cur,new if action=='apply' else old))
  changed=[];owned_result=False;owned_applied=False
  try:
   for p,old,new in ops:
    if old!=new:atomic(p,new);changed.append((p,old))
   with marker.open('x',encoding='utf8') as f:owned_result=True;json.dump({'action':action,'manifest_sha256':PIN,'production_literal_reproof_required':action=='apply'},f)
   if action=='apply':
    with (T/'applied.json').open('x',encoding='utf8') as f:owned_applied=True;json.dump({'manifest_sha256':PIN},f)
  except BaseException:
   for p,old in reversed(changed):atomic(p,old)
   if owned_result and marker.exists():marker.unlink()
   if owned_applied and (T/'applied.json').exists():(T/'applied.json').unlink()
   raise
  print(json.dumps({'action':action,'files':len(ops),'production_literal_reproof_required':action=='apply'}))
 finally:
  for p in reversed(guards):p.unlink()
def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=('apply','restore','recover'));p.add_argument('--ack-production-reproof',action='store_true');a=p.parse_args();run(a.action,a.ack_production_reproof)
if __name__=='__main__':main()
