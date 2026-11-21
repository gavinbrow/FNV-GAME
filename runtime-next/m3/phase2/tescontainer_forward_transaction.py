"""Stage and guard a two-file TESContainer header/651 source transaction."""
import argparse,hashlib,json,os,sys,tempfile,time
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';E=M/'out/phase2-next-source-proposals-v4';T=M/'out/phase2-tescontainer-forward-transaction';sys.path.insert(0,str(H));import rtti_tesform_bindings_transaction as locks
PROOF='15f007f7ace5368ac6a53bb670271e058796dda2278ce558c635d3c181080855';FA='fa36603e3e9a2ea495644f383db983a9269d2e7cf558282a80746439386dbfc8';RELS=['include/TESContainer.h','src/fallout_shared/bgsloadedreferencecollection.cpp']
def sha(b):return hashlib.sha256(b).hexdigest()
def evidence():
 raw=(E/'manifest.json').read_bytes()
 if sha(raw)!=PROOF:raise ValueError('reviewed proposal manifest changed')
 m=json.loads(raw)
 if m['base_units_sha256']!=FA or m['forward']['recipe_change'] or [x['path'] for x in m['forward']['files']]!=RELS:raise ValueError('unexpected transaction scope')
 if m['forward']['gates']!={'unit651':4,'unit980':31,'guard_probes':2}:raise ValueError('reviewed checks missing')
 for rel,digest in m['evidence_sha256'].items():
  if sha((M/rel).read_bytes())!=digest:raise ValueError('review evidence changed '+rel)
 return m

def prepare():
 m=evidence();items=[]
 if sha((F/'build/units.json').read_bytes())!=FA:raise ValueError('live recipe changed')
 if T.exists():raise FileExistsError('refusing overwrite')
 for x in m['forward']['files']:
  old=(E/'forward'/x['original']).read_bytes();new=(E/'forward'/x['generated']).read_bytes();actual=(F/x['path']).read_bytes()
  if sha(old)!=x['old_sha256'] or sha(new)!=x['new_sha256'] or old!=actual:raise ValueError('file payload differs '+x['path'])
  items.append((x,old,new))
 T.mkdir()
 for x,old,new in items:(T/x['original']).write_bytes(old);(T/x['generated']).write_bytes(new)
 (T/'manifest.json').write_text(json.dumps({'proposal_sha256':PROOF,'recipe_sha256':FA,'files':m['forward']['files'],'scope':'two-file TESContainer source/header experiment; no recipe edit or native class-completeness claim','recovery':'restore both originals from either known old/new state'},indent=2));print(json.dumps({'status':'prepared','files':len(items)}))

def atomic_write(path,data):
 fd,name=tempfile.mkstemp(prefix='tes-forward-',dir=T);temp=Path(name)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(temp,path)
 except BaseException:
  if temp.exists():temp.unlink()
  raise

def run(action):
 guards=locks.acquire_guard()
 try:
  m=evidence();raw=(T/'manifest.json').read_bytes();t=json.loads(raw)
  if t['proposal_sha256']!=PROOF or t['recipe_sha256']!=FA or t['files']!=m['forward']['files']:raise ValueError('transaction manifest changed')
  if sha((F/'build/units.json').read_bytes())!=FA:raise ValueError('recipe no longer matches reviewed base')
  if action=='apply':
   for unit in ('unit651','unit980'):
    for rel,digest in m['include_closures'][unit]['original_files'].items():
     p=(F/rel).resolve()
     if not p.is_relative_to(F.resolve()) or sha(p.read_bytes())!=digest:raise ValueError('source closure changed '+rel)
  if action=='restore' and not (T/'applied.json').exists():raise ValueError('transaction was not applied')
  marker=T/(('recover-result-%d-%d.json'%(os.getpid(),time.time_ns())) if action=='recover' else action+'-result.json')
  if marker.exists():raise FileExistsError('transaction action already recorded')
  operations=[]
  for x in t['files']:
   path=(F/x['path']).resolve()
   if not path.is_relative_to(F.resolve()):raise ValueError('path escapes project')
   old=(T/x['original']).read_bytes();new=(T/x['generated']).read_bytes();current=path.read_bytes()
   if sha(old)!=x['old_sha256'] or sha(new)!=x['new_sha256']:raise ValueError('payload changed')
   allowed=[x['old_sha256']] if action=='apply' else [x['new_sha256']] if action=='restore' else [x['old_sha256'],x['new_sha256']]
   if sha(current) not in allowed:raise ValueError('unknown file state '+x['path'])
   operations.append((path,current,new if action=='apply' else old))
  changed=[];result_owned=False;applied_owned=False
  try:
   for path,old,new in operations:
    if old!=new:atomic_write(path,new);changed.append((path,old))
   with marker.open('x',encoding='utf8') as f:
    result_owned=True;json.dump({'action':action,'manifest_sha256':sha(raw)},f)
   if action=='apply':
    with (T/'applied.json').open('x',encoding='utf8') as f:
     applied_owned=True;json.dump({'manifest_sha256':sha(raw)},f)
  except BaseException:
   for path,old in reversed(changed):atomic_write(path,old)
   if result_owned and marker.exists():marker.unlink()
   if applied_owned and (T/'applied.json').exists():(T/'applied.json').unlink()
   raise
  print(json.dumps({'action':action,'files':len(operations)}))
 finally:
  for p in reversed(guards):p.unlink()

def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=('prepare','apply','restore','recover'));a=p.parse_args();prepare() if a.action=='prepare' else run(a.action)
if __name__=='__main__':main()
