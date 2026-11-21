"""Guarded default promotion: private draft; configure PIN only after acceptance review."""
import argparse,hashlib,json,os,sys,tempfile,time
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;ROOT=M.parent.parent;T=M/'out/phase2-next-data-promotion-private'
sys.path.insert(0,str(H));import rtti_tesform_bindings_transaction as locks
PIN='5f7e5a32f2db5505723306f0dab97988a560cac99cebb6a58261d0fc6f79aa77'
REL=['runtime-next/m3/phase2/selection.json','runtime-next/m3/phase2/library_candidates.json','runtime-next/m3/config.py','runtime-next/m3/phase2/run_frozen.py']
def sha(b):return hashlib.sha256(b).hexdigest()
def atomic(path,data):
 fd,name=tempfile.mkstemp(prefix='.next-promotion-',dir=path.parent);tmp=Path(name)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(tmp,path)
 finally:
  if tmp.exists():tmp.unlink()
def read_manifest():
 raw=(T/'manifest.final.json').read_bytes()
 if sha(raw)!=PIN:raise ValueError('promotion manifest not pinned or changed')
 m=json.loads(raw)
 if [x['path'] for x in m['files']]!=REL or len(m['files'])!=4:raise ValueError('target scope changed')
 for i,x in enumerate(m['files']):
  if x['original']!=str(i)+'.original' or x['candidate']!=str(i)+'.candidate':raise ValueError('payload path mismatch')
  for kind,key in [('original','old_sha256'),('candidate','new_sha256')]:
   if sha((T/x[kind]).read_bytes())!=x[key]:raise ValueError('payload mismatch')
 return m
def validate_inputs(m):
 for name,digest in m['required_inputs'].items():
  p=(ROOT/name).resolve()
  if not p.is_relative_to(ROOT.resolve()) or sha(p.read_bytes())!=digest:raise ValueError('required evidence or input changed: '+name)
 # The frozen source snapshot is pinned as evidence above; check each source now.
 snap=json.loads((ROOT/m['source_snapshot']).read_text(encoding='utf-8-sig'))
 for name,record in snap.items():
  low=name.lower()
  if '\\fnv_decomp\\src\\' in low or '\\fnv_decomp\\include\\' in low:
   p=Path(name).resolve()
   if not p.is_relative_to((ROOT/'fnv_decomp').resolve()) or sha(p.read_bytes())!=record['sha256']:raise ValueError('source snapshot changed: '+name)
def run(action):
 guards=locks.acquire_guard()
 try:
  m=read_manifest()
  if action=='apply':validate_inputs(m)
  marker=T/(('recover-result-%d-%d.json'%(os.getpid(),time.time_ns())) if action=='recover' else action+'-result.json')
  if marker.exists():raise FileExistsError('action already recorded')
  if action=='apply' and (T/'applied.json').exists():raise FileExistsError('already applied')
  if action=='restore' and not (T/'applied.json').exists():raise ValueError('not applied')
  ops=[]
  for x in m['files']:
   p=(ROOT/x['path']).resolve()
   if not p.is_relative_to(ROOT.resolve()):raise ValueError('target escapes workspace')
   old=(T/x['original']).read_bytes();new=(T/x['candidate']).read_bytes();cur=p.read_bytes();h=sha(cur)
   allowed=[x['old_sha256']] if action=='apply' else [x['new_sha256']] if action=='restore' else [x['old_sha256'],x['new_sha256']]
   if h not in allowed:raise ValueError('unknown target state: '+x['path'])
   ops.append((p,cur,new if action=='apply' else old))
  changed=[];created=[]
  try:
   for path,previous,wanted in ops:
    if previous!=wanted:atomic(path,wanted);changed.append((path,previous))
   for path in ([marker,T/'applied.json'] if action=='apply' else [marker]):
    with path.open('x',encoding='utf8') as f:
     created.append(path);json.dump({'action':action,'manifest_sha256':PIN,'fresh_no_override_default_gate_required':True},f)
  except BaseException:
   failures=[]
   for path,previous in reversed(changed):
    try:atomic(path,previous)
    except BaseException as exc:failures.append(str(path)+': '+str(exc))
   for path in created:path.unlink(missing_ok=True)
   if failures:raise RuntimeError('rollback incomplete; use recover: '+', '.join(failures))
   raise
  print(json.dumps({'action':action,'files':len(ops),'manifest_sha256':PIN,'fresh_default_gate_required':True}))
 finally:
  for p in reversed(guards):p.unlink()
def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=('apply','restore','recover'));run(p.parse_args().action)
if __name__=='__main__':main()
