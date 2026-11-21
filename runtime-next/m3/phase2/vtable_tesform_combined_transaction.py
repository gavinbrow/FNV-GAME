"""Guard the reviewed disjoint TESForm/Script source batch; no build."""
import argparse,hashlib,json,os,sys,tempfile,time
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';O=M/'out';T=O/'phase2-combined-source-transaction';sys.path.insert(0,str(H));import rtti_tesform_bindings_transaction as locks
PIN='b0d4204b54df8d37fc96e15bd5ef174a10ef0d7c5b022e81d1b076a6f4808130';BASE='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160';REL=['src/fallout_shared/tesform.cpp','src/fallout_shared/tesform_TESForm.h','src/bgsencounterzone_TESForm.h','src/fallout_shared/tesscript_decls.h','build/units.json']
def sha(b):return hashlib.sha256(b).hexdigest()
def atomic(path,data):
 fd,name=tempfile.mkstemp(prefix='combined-source-',dir=T);p=Path(name)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(p,path)
 finally:
  if p.exists():p.unlink()
def run(action,ack=False):
 if action=='apply' and not ack:raise ValueError('acknowledge production literal reproof before apply')
 guards=locks.acquire_guard()
 try:
  raw=(T/'manifest.json').read_bytes()
  if sha(raw)!=PIN:raise ValueError('combined manifest changed')
  m=json.loads(raw)
  if m['base_recipe_sha256']!=BASE or [x['path'] for x in m['files']]!=REL or m['parent_recipe_units']!=[998,1111,1112]:raise ValueError('scope changed')
  a=O/'phase2-flagpairs-transaction/manifest.json';b=O/'phase2-tescontainer-script-transaction-v2/manifest.json'
  if sha(a.read_bytes())!=m['parent_manifests']['flagpairs'] or sha(b.read_bytes())!=m['parent_manifests']['script']:raise ValueError('parent manifest changed')
  flag=json.loads(a.read_bytes());script=json.loads(b.read_bytes())
  for rel,d in {**flag['evidence_sha256'],**script['evidence']}.items():
   if sha((O/rel).read_bytes())!=d:raise ValueError('evidence changed '+rel)
  if action=='apply':
   closure={}
   for name in ('phase2-tesform-two-flagpairs-mirror','phase2-bgs-two-flagpairs-mirror'):
    x=json.loads((O/name/'mirror-manifest.json').read_bytes())
    for rel,d in x['original_inputs'].items():
     if rel in closure and closure[rel]!=d:raise ValueError('closure hash conflict')
     closure[rel]=d
   x=json.loads((O/'phase2-tescontainer-script-removal/manifest.json').read_bytes())
   for unit in ('1111','1112'):
    for rel,d in x['original_closures'][unit]['original_project_files'].items():
     if rel in closure and closure[rel]!=d:raise ValueError('closure hash conflict')
     closure[rel]=d
   for rel,d in closure.items():
    p=(F/rel).resolve()
    if not p.is_relative_to(F.resolve()) or sha(p.read_bytes())!=d:raise ValueError('source closure changed '+rel)
  if action=='restore' and not (T/'applied.json').exists():raise ValueError('not applied')
  marker=T/(('recover-%d-%d.json'%(os.getpid(),time.time_ns())) if action=='recover' else action+'-result.json')
  if marker.exists():raise FileExistsError('action already recorded')
  ops=[]
  for x in m['files']:
   p=(F/x['path']).resolve();old=(T/x['original']).read_bytes();new=(T/x['generated']).read_bytes();cur=p.read_bytes()
   if not p.is_relative_to(F.resolve()) or sha(old)!=x['old_sha256'] or sha(new)!=x['new_sha256']:raise ValueError('payload changed')
   allowed=[x['old_sha256']] if action=='apply' else [x['new_sha256']] if action=='restore' else [x['old_sha256'],x['new_sha256']]
   if sha(cur) not in allowed:raise ValueError('unknown target state '+x['path'])
   ops.append((p,cur,new if action=='apply' else old))
  changed=[];owned=[]
  try:
   for p,old,new in ops:
    if old!=new:atomic(p,new);changed.append((p,old))
   for p in ([marker,T/'applied.json'] if action=='apply' else [marker]):
    with p.open('x',encoding='utf8') as f:owned.append(p);json.dump({'action':action,'manifest_sha256':PIN,'production_literal_reproof_required':action=='apply'},f)
  except BaseException:
   for p,old in reversed(changed):atomic(p,old)
   for p in owned:p.unlink(missing_ok=True)
   raise
  print(json.dumps({'action':action,'files':len(ops),'production_literal_reproof_required':action=='apply'}))
 finally:
  for p in reversed(guards):p.unlink()
def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=('apply','restore','recover'));p.add_argument('--ack-production-reproof',action='store_true');a=p.parse_args();run(a.action,a.ack_production_reproof)
if __name__=='__main__':main()
