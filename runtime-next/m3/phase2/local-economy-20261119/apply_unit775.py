"""Guarded single-file pilot transaction; never runs builds. Coordinator applies only after review."""
import argparse,hashlib,json,os,pathlib,sys,tempfile,time
H=pathlib.Path(__file__).resolve().parent;M=H.parents[1];R=M.parents[1];F=R/'fnv_decomp';T=M/'out/phase2-local-economy-20261119/pilot';V=M/'out/phase2-web-e2e-validation-1';sys.path.insert(0,str(M/'phase2'));import rtti_tesform_bindings_transaction as locks
PIN='935071153b06bf7924355cf170f9cb6068d958bac51e7e8adaf049fe8e1fef3e';CLOSURE='36a3fff6e453c2694cfbadae15f9406a92ee3178f3b301e0b9eb16e48d9d026a';TARGET=F/'src/fallout_shared/inventorychanges_ctxr_variant.cpp';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,data):
 fd,n=tempfile.mkstemp(prefix='.unit775-',dir=T);tmp=pathlib.Path(n)
 try:
  with os.fdopen(fd,'wb') as q:q.write(data);q.flush();os.fsync(q.fileno())
  os.replace(tmp,p)
 finally:
  if tmp.exists():tmp.unlink()
def run(action):
 guards=locks.acquire_guard()
 try:
  if (R/'runtime-next/direct-v1/harness.lock').exists():raise ValueError('gameplay lane busy')
  if h(T/'manifest.json')!=PIN or h(V/'unit-0775/mirror-manifest.json')!=CLOSURE:raise ValueError('manifest drift')
  m=json.loads((T/'manifest.json').read_bytes());old=(T/'source.original').read_bytes();new=(T/'source.generated').read_bytes()
  if hashlib.sha256(old).hexdigest()!=m['old_sha256'] or hashlib.sha256(new).hexdigest()!=m['new_sha256'] or h(F/'build/units.json')!=m['recipe_sha256'] or h(F/'include/TESContainer.h')!=m['header_sha256'] or h(V/'result.json')!=m['review_result_sha256']:raise ValueError('payload or accepted inputs drift')
  closure=json.loads((V/'unit-0775/mirror-manifest.json').read_bytes())['original_inputs']
  for rel,digest in closure.items():
   p=(F/rel).resolve()
   if not p.is_relative_to(F.resolve()):raise ValueError('closure escapes source tree')
   if p!=TARGET.resolve() and h(p)!=digest:raise ValueError('include closure changed: '+rel)
  current=TARGET.read_bytes();allowed=[m['old_sha256']] if action=='apply' else [m['new_sha256']] if action=='restore' else [m['old_sha256'],m['new_sha256']]
  if hashlib.sha256(current).hexdigest() not in allowed:raise ValueError('unknown source state')
  if action=='restore' and not (T/'applied.json').exists():raise ValueError('not applied')
  marker=T/(('recover-%d-%d.json'%(os.getpid(),time.time_ns())) if action=='recover' else action+'-result.json')
  if marker.exists() or (action=='apply' and (T/'applied.json').exists()):raise FileExistsError('existing transaction marker')
  changed=False;created=[]
  try:
   wanted=new if action=='apply' else old
   if current!=wanted:atomic(TARGET,wanted);changed=True
   for p in ([marker,T/'applied.json'] if action=='apply' else [marker]):
    with p.open('x') as q:created.append(p);json.dump({'action':action,'manifest_sha256':PIN,'production_build_required':True},q)
  except BaseException:
   if changed:atomic(TARGET,current)
   for p in created:p.unlink(missing_ok=True)
   raise
  print(json.dumps({'action':action,'production_build_required':True}))
 finally:
  for p in reversed(guards):p.unlink()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=('apply','restore','recover'));run(p.parse_args().action)
