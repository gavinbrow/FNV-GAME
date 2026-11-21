"""Guarded six-file opt-in data tooling transaction; no default selection switch."""
import argparse,hashlib,json,os,sys,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;ROOT=RN.parent;T=M/'out/phase2-next-data-transaction6757';sys.path.insert(0,str(H));import rtti_tesform_bindings_transaction as locks
PIN='03b8b754d0583454c46d0488e5ea182acc01dd5b99f9b55e374a3eced8307e22';EVIDENCE='e43c2c9e7276755fe64c547acac872c3559c25136286170444a5921b682364fe';CONFIG='b3407808a88a951b916d6c243d0b327e82ef77eda0f79b458eff6dda72febc90'
REL=['runtime-next/m3/gen_m3.py','runtime-next/m3/phase2/cost245_records.py','runtime-next/m3/splice.py','runtime-next/m3/m3secs.py','runtime-next/layout-v2/make_image.py','runtime-next/m3/phase2/library_overlay.py']
FIXTURES={'point3':'runtime-next/m3/out/phase2-point3/isolated-fixture/result.json','simd':'runtime-next/m3/out/phase2-align16/isolated-fixture/result.json','cost':'runtime-next/m3/out/phase2-cost245-proposal/isolated-fixture/result.json'}
def sha(data):return hashlib.sha256(data).hexdigest()
def atomic(path,data):
 fd,name=tempfile.mkstemp(prefix='.next-data-',dir=path.parent);tmp=Path(name)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(tmp,path)
 finally:
  if tmp.exists():tmp.unlink()
def read_manifest():
 raw=(T/'manifest.json').read_bytes()
 if sha(raw)!=PIN:raise ValueError('transaction manifest changed')
 m=json.loads(raw)
 if [x['path'] for x in m['files']]!=REL or len(m['files'])!=6:raise ValueError('transaction path scope changed')
 for i,x in enumerate(m['files']):
  if x['original']!=str(i)+'.original' or x['generated']!=str(i)+'.generated':raise ValueError('payload names changed')
  for kind in ('original','generated'):
   if sha((T/x[kind]).read_bytes())!=x['old_sha256' if kind=='original' else 'new_sha256']:raise ValueError('payload changed')
 if sha((T/'selection.json').read_bytes())!=m['selection_sha256'] or sha((T/'library_candidates.json').read_bytes())!=m['library_selection_sha256']:raise ValueError('private selection changed')
 return m
def validate_inputs(m):
 expected={'fnv_decomp/build/units.json':m['accepted_epoch_recipe_sha256'],
  'runtime-next/m3/phase2/selection.json':m['accepted_selection_sha256'],
  'runtime-next/m3/phase2/library_candidates.json':m['accepted_library_sha256'],
  'runtime-next/m3/config.py':CONFIG}
 for n,h in expected.items():
  if sha((ROOT/n).read_bytes())!=h:raise ValueError('accepted preimage changed: '+n)
 e=ROOT/'runtime-next/m3/phase2/next_batch_manifest.json';raw=e.read_bytes()
 if sha(raw)!=EVIDENCE:raise ValueError('source evidence manifest changed')
 evidence=json.loads(raw)
 for x in evidence['source_evidence']:
  if sha((ROOT/x['path']).read_bytes())!=x['sha256']:raise ValueError('source evidence changed: '+x['path'])
 for n,path in FIXTURES.items():
  if sha((ROOT/path).read_bytes())!=m['fixture_sha256'][n]:raise ValueError('fixture evidence changed: '+n)
def run(action):
 guards=locks.acquire_guard()
 try:
  m=read_manifest()
  if action=='apply':validate_inputs(m)
  marker=T/(action+'-result.json')
  if marker.exists():raise FileExistsError('action already recorded')
  if action=='apply' and (T/'applied.json').exists():raise FileExistsError('already applied')
  if action=='restore' and not (T/'applied.json').exists():raise ValueError('no applied marker')
  ops=[]
  for x in m['files']:
   p=(ROOT/x['path']).resolve()
   if not p.is_relative_to(ROOT.resolve()):raise ValueError('target escapes workspace')
   old=(T/x['original']).read_bytes();new=(T/x['generated']).read_bytes();cur=p.read_bytes();h=sha(cur)
   allowed=[x['old_sha256']] if action=='apply' else [x['new_sha256']] if action=='restore' else [x['old_sha256'],x['new_sha256']]
   if h not in allowed:raise ValueError('unknown target state: '+x['path'])
   ops.append((p,cur,new if action=='apply' else old))
  changed=[];created=[]
  try:
   for path,previous,wanted in ops:
    if previous!=wanted:atomic(path,wanted);changed.append((path,previous))
   for path in ([marker,T/'applied.json'] if action=='apply' else [marker]):
    with path.open('x',encoding='utf8') as f:
     created.append(path);json.dump({'action':action,'manifest_sha256':PIN,'private_selections_only':True},f)
  except BaseException:
   failures=[]
   for path,previous in reversed(changed):
    try:atomic(path,previous)
    except BaseException as exc:failures.append(str(path)+': '+str(exc))
   for path in created:path.unlink(missing_ok=True)
   if failures:raise RuntimeError('rollback incomplete; use recover: '+', '.join(failures))
   raise
  print(json.dumps({'action':action,'files':len(ops),'manifest_sha256':PIN,'defaults_unchanged':True}))
 finally:
  for p in reversed(guards):p.unlink()
def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=('apply','restore','recover'));a=p.parse_args();run(a.action)
if __name__=='__main__':main()
