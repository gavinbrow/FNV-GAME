"""Stage guarded unused TESContainer shell removal with unit-local mirror bindings."""
import copy,hashlib,json,os,sys,tempfile,time
from pathlib import Path
H=Path(__file__).resolve().parent; M=H.parent; RN=M.parent; F=RN.parent/'fnv_decomp'; O=M/'out'; T=O/'phase2-tescontainer-script-transaction-v2';sys.path.insert(0,str(H));import rtti_tesform_bindings_transaction as locks;import tescontainer_install as recipe_edit
BASE='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160'
E={'phase2-tescontainer-script-removal/manifest.json':'17ab354bbb3e33c16f18763afb30b700ba7dfe9c9934b638738f99dd55322bb2','phase2-tescontainer-script-remove-1111-mirror/comparison.json':'a4fb1b2e163fab1993b16c17a043f4629a10d8ce1187da1efa8006ff910e0d76','phase2-tescontainer-script-remove-1112-mirror/comparison.json':'b53c73917e6ff6dd1bb4feade68dd0a030b817a73b582ef92d4ab97f67806c27'}
def sha(b):return hashlib.sha256(b).hexdigest()
def evidence():
 for rel,h in E.items():
  if sha((O/rel).read_bytes())!=h:raise ValueError('evidence changed '+rel)
 return json.loads((O/next(iter(E))).read_bytes())
def prepare():
 m=evidence(); up=F/'build/units.json';old=up.read_bytes()
 if sha(old)!=BASE or m['base_units_sha256']!=BASE:raise ValueError('recipe changed')
 hdr=F/'src/fallout_shared/tesscript_decls.h';before=hdr.read_bytes();after=(O/'phase2-tescontainer-script-removal/tesscript_decls.h').read_bytes()
 if sha(before)!=m['original_header_sha256'] or sha(after)!=m['candidate_header_sha256']:raise ValueError('header changed')
 recipe=json.loads(old); candidate=copy.deepcopy(recipe);counts={}
 for i,n in ((1111,82),(1112,1)):
  proof=json.loads((O/f'phase2-tescontainer-script-remove-{i}-mirror/comparison.json').read_bytes());unit=recipe['units'][i];out=candidate['units'][i]
  if proof['production_reference_matches']!=n or proof['mirror_original_reference_matches']!=n or proof['mirror_candidate_reference_matches']!=n or proof['production_to_mirror_literals']:raise ValueError('comparison scope')
  bindings={}
  for row in proof['mirror_to_candidate_literals']:
   if unit['symbols'].get(row['before'])!=row['bound_va']:raise ValueError('source binding changed')
   if row['after'] in bindings and bindings[row['after']]!=row['bound_va']:raise ValueError('ambiguous candidate label')
   bindings[row['after']]=row['bound_va']
  out['symbols'].update(bindings);counts[str(i)]=len(bindings)
 for i,(a,b) in enumerate(zip(recipe['units'],candidate['units'])):
  if i not in (1111,1112) and a!=b:raise ValueError('out of scope unit')
 if T.exists():raise FileExistsError('preserve existing transaction')
 T.mkdir();new=recipe_edit.replace_unit(old,1111,candidate['units'][1111]);new=recipe_edit.replace_unit(new,1112,candidate['units'][1112]);assert json.loads(new)==candidate
 for k,v in [('0.original',before),('0.generated',after),('1.original',old),('1.generated',new)]:(T/k).write_bytes(v)
 manifest={'evidence':E,'base_recipe_sha256':BASE,'files':[{'path':'src/fallout_shared/tesscript_decls.h','original':'0.original','generated':'0.generated','old_sha256':sha(before),'new_sha256':sha(after)},{'path':'build/units.json','original':'1.original','generated':'1.generated','old_sha256':sha(old),'new_sha256':sha(new)}],'binding_counts':counts,'limits':['mirror labels are provisional; rederive and verify from actual production objects before full build','apply requires locked build lane and full closure preimage validation','no claim of complete class identity or ODR']}
 (T/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(counts))
def atomic(path,data):
 fd,n=tempfile.mkstemp(prefix='tes-script-',dir=T)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(n,path)
 finally:
  if os.path.exists(n):os.unlink(n)
def run(action,ack=False):
 if action=='apply' and not ack:raise ValueError('acknowledge production literal reproof before apply')
 guards=locks.acquire_guard()
 try:
  m=evidence();raw=(T/'manifest.json').read_bytes();t=json.loads(raw)
  if sha(raw)!='36d86875ca04c92df9531336ef0896804a65d74dae3f28c98a8defd9aca83a7a' or t['evidence']!=E or t['base_recipe_sha256']!=BASE:raise ValueError('manifest mismatch')
  if action=='apply':
   for unit in ('1111','1112'):
    for rel,h in m['original_closures'][unit]['original_project_files'].items():
     p=(F/rel).resolve()
     if not p.is_relative_to(F.resolve()) or sha(p.read_bytes())!=h:raise ValueError('closure changed '+rel)
  if action=='restore' and not (T/'applied.json').exists():raise ValueError('not applied')
  ops=[]
  for x in t['files']:
   p=(F/x['path']).resolve();old=(T/x['original']).read_bytes();new=(T/x['generated']).read_bytes();current=p.read_bytes()
   if not p.is_relative_to(F.resolve()) or sha(old)!=x['old_sha256'] or sha(new)!=x['new_sha256']:raise ValueError('payload changed')
   allowed=[x['old_sha256']] if action=='apply' else [x['new_sha256']] if action=='restore' else [x['old_sha256'],x['new_sha256']]
   if sha(current) not in allowed:raise ValueError('unknown file state')
   ops.append((p,current,new if action=='apply' else old))
  marker=T/(('recover-result-%d-%d.json'%(os.getpid(),time.time_ns())) if action=='recover' else action+'-result.json');changed=[];owned=[]
  try:
   for p,old,new in ops:
    if old!=new:atomic(p,new);changed.append((p,old))
   for p in ([marker,T/'applied.json'] if action=='apply' else [marker]):
    with p.open('x') as f:owned.append(p);json.dump({'action':action,'manifest_sha256':sha(raw)},f)
  except BaseException:
   for p,old in reversed(changed):atomic(p,old)
   for p in owned:p.unlink(missing_ok=True)
   raise
 finally:
  for p in reversed(guards):p.unlink()
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=('prepare','apply','restore','recover'));ap.add_argument('--ack-production-reproof',action='store_true');a=ap.parse_args();prepare() if a.action=='prepare' else run(a.action,a.ack_production_reproof)
