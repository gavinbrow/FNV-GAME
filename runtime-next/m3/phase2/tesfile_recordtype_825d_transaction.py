"""Guard reviewed TESFile global correction; no action without explicit command."""
import argparse,hashlib,json,os,sys,tempfile,time
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';D=M/'out/phase2-tesfile-recordtype-825d';P=M/'out/phase2-tesfile-recordtype-global';T=M/'out/phase2-source-integration6757-transaction-v2';sys.path.insert(0,str(H));import rtti_tesform_bindings_transaction as locks
PIN='45425a3ac83c34c3709240e07e069138e37265298570644735a790ca4688fc30';REL=['build/units.json','src/fallout_shared/tesfile.cpp']
def sha(b):return hashlib.sha256(b).hexdigest()
def atomic(path,data):
 fd,name=tempfile.mkstemp(prefix='tesfile-global-',dir=D)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(name,path)
 finally:
  if os.path.exists(name):os.unlink(name)
def run(action,ack=False):
 if action=='apply' and not ack:raise ValueError('acknowledge actual-production literal reproof')
 guards=locks.acquire_guard()
 try:
  raw=(D/'manifest.json').read_bytes()
  if sha(raw)!=PIN:raise ValueError('transaction manifest changed')
  m=json.loads(raw)
  if [x['path'] for x in m['files']]!=REL or m['recipe_units_changed']!=[995] or m['candidate_strict']!=87 or m['listed_tails_passed']!=4:raise ValueError('transaction scope differs')
  if sha((T/'manifest.json').read_bytes())!=m['transition_manifest_sha256']:raise ValueError('transition provenance differs')
  for name,digest in m['source_evidence_sha256'].items():
   if sha((P/name).read_bytes())!=digest:raise ValueError('source proof differs '+name)
  if action=='apply':
   for rel,digest in m['source_closure_sha256'].items():
    p=(F/rel).resolve()
    if not p.is_relative_to(F.resolve()) or sha(p.read_bytes())!=digest:raise ValueError('source closure changed '+rel)
   p=json.loads((P/'manifest.json').read_text());q=(F/p['source_other_unit_path']).resolve()
   if not q.is_relative_to(F.resolve()) or sha(q.read_bytes())!=p['source_other_unit_sha256']:raise ValueError('independent global source changed')
  if action=='restore' and not (D/'applied.json').exists():raise ValueError('transaction not applied')
  marker=D/(('recover-%d-%d.json'%(os.getpid(),time.time_ns())) if action=='recover' else action+'-result.json')
  if marker.exists():raise FileExistsError('action already recorded')
  operations=[]
  for x in m['files']:
   p=(F/x['path']).resolve();old=(D/x['original']).read_bytes();new=(D/x['generated']).read_bytes();cur=p.read_bytes()
   if not p.is_relative_to(F.resolve()) or sha(old)!=x['old_sha256'] or sha(new)!=x['new_sha256']:raise ValueError('payload differs')
   allowed=[x['old_sha256']] if action=='apply' else [x['new_sha256']] if action=='restore' else [x['old_sha256'],x['new_sha256']]
   if sha(cur) not in allowed:raise ValueError('unknown file state '+x['path'])
   operations.append((p,cur,new if action=='apply' else old))
  changed=[];owned=[]
  try:
   for p,old,new in operations:
    if old!=new:atomic(p,new);changed.append((p,old))
   for p in ([marker,D/'applied.json'] if action=='apply' else [marker]):
    with p.open('x') as f:owned.append(p);json.dump({'action':action,'manifest_sha256':PIN,'actual_production_literal_reproof_required':action=='apply'},f)
  except BaseException:
   for p,old in reversed(changed):atomic(p,old)
   for p in owned:p.unlink(missing_ok=True)
   raise
  print(json.dumps({'action':action,'files':len(operations),'production_reproof_required':action=='apply'}))
 finally:
  for p in reversed(guards):p.unlink()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=('apply','restore','recover'));p.add_argument('--ack-production-reproof',action='store_true');a=p.parse_args();run(a.action,a.ack_production_reproof)
