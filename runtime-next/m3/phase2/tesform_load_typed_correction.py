"""Apply/rollback an independently reviewed production literal correction only."""
import argparse,copy,hashlib,json,os,sys,tempfile,time
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';T=M/'out/phase2-tesform-load-typed-v4-transaction';C=T/'production-correction';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
import paths,tesform_load_typed_transaction_v4 as tx

def sha(b):return hashlib.sha256(b).hexdigest()
def delta(old,new,e):
 a=json.loads(old);b=json.loads(new)
 if a.keys()!=b.keys() or any(a[k]!=b[k] for k in a if k!='units') or len(a['units'])!=len(b['units']) or [i for i,(x,y) in enumerate(zip(a['units'],b['units'])) if x!=y] not in ([],[998]):raise ValueError('correction exceeds unit998')
 u=a['units'][998];v=b['units'][998]
 if u.keys()!=v.keys() or any(u[k]!=v[k] for k in u if k!='symbols'):raise ValueError('correction changed non-symbol data')
 expected={}
 for f in e['literal_facts']:
  k=f['production_label'];value=f['binding']
  if k in expected and expected[k]!=value:raise ValueError('ambiguous binding')
  expected[k]=value
 changed={k for k in u['symbols'].keys()|v['symbols'].keys() if u['symbols'].get(k)!=v['symbols'].get(k)}
 if any(k not in expected or v['symbols'].get(k)!=expected[k] for k in changed):raise ValueError('unsupported symbol edit')
 return b

def proof(reviewed,verify_objects):
 raw=(C/'manifest.json').read_bytes()
 if sha(raw)!=reviewed:raise ValueError('correction manifest does not match reviewed digest')
 e=json.loads(raw);m=tx.manifest();old=(C/'units.original').read_bytes();new=(C/'units.generated').read_bytes()
 if e['transaction_manifest_sha256']!=tx.PROOF or sha(old)!=m['files'][-1]['new_sha256'] or e['original_sha256']!=sha(old) or e['generated_sha256']!=sha(new) or e['unit998_matches']!=128 or e['unit2_diagnostic_matches']!=24:raise ValueError('correction proof mismatch')
 doc=delta(old,new,e)
 if verify_objects:
  for x in m['files'][:-1]:
   if sha((F/x['path']).read_bytes())!=x['new_sha256']:raise ValueError('installed candidate source changed')
  tp=RN/'pinned-build/obj_v3/0998.obj';bp=RN/'pinned-build/obj_v3/0002.obj'
  if sha(tp.read_bytes())!=e['tes_object_sha256'] or sha(bp.read_bytes())!=e['bgs_object_sha256']:raise ValueError('production objects changed')
  pe=Pe(paths.REF_IMAGE);tes=compare(Coff(str(tp)),pe,doc['units'][998]);diag=copy.deepcopy(doc['units'][2]);diag['symbols']['??1TESForm@@UAE@XZ']='0x00483630'
  for x in m['unit998_function_remaps']:diag['symbols'][x['after']]=x['address']
  for n in m['noop_fold']['new_symbols']:diag['symbols'][n]=m['noop_fold']['source_address']
  bgs=compare(Coff(str(bp)),pe,diag)
  if len(tes)!=128 or len(bgs)!=24 or any(x['verdict']!='match' for x in tes+bgs):raise ValueError('production strict reference checks failed')
 return old,new

def atomic(data):
 fd,name=tempfile.mkstemp(prefix='typed-correction-',dir=C);p=Path(name)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(p,F/'build/units.json')
 except BaseException:
  if p.exists():p.unlink()
  raise

def run(action,reviewed):
 if len(reviewed)!=64 or any(c not in '0123456789abcdef' for c in reviewed):raise ValueError('explicit reviewed SHA-256 required')
 guards=tx.lock.acquire_guard()
 try:
  if not (T/'applied.json').exists():raise ValueError('source transaction was not applied')
  old,new=proof(reviewed,action=='apply');target=F/'build/units.json';cur=target.read_bytes();allowed=([sha(old)] if action=='apply' else [sha(new)] if action=='restore' else [sha(old),sha(new)])
  if sha(cur) not in allowed:raise ValueError('unknown correction state')
  if action=='restore' and not (C/'applied.json').exists():raise ValueError('correction was not applied')
  marker=C/(('recover-%d-%d.json'%(os.getpid(),time.time_ns())) if action=='recover' else action+'-result.json')
  if marker.exists():raise FileExistsError('action already recorded')
  wanted=new if action=='apply' else old;changed=False;owned=False;applied_owned=False
  try:
   if cur!=wanted:atomic(wanted);changed=True
   with marker.open('x',encoding='utf8') as f:
    owned=True;json.dump({'action':action,'reviewed_manifest_sha256':reviewed,'recipe_sha256':sha(wanted)},f)
   if action=='apply':
    with (C/'applied.json').open('x',encoding='utf8') as f:
     applied_owned=True;json.dump({'reviewed_manifest_sha256':reviewed},f)
  except BaseException:
   if changed:atomic(cur)
   if owned and marker.exists():marker.unlink()
   if applied_owned and (C/'applied.json').exists():(C/'applied.json').unlink()
   raise
  print(json.dumps({'action':action,'recipe_sha256':sha(wanted)}))
 finally:
  for p in reversed(guards):p.unlink()
def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=('apply','restore','recover'));p.add_argument('--reviewed-manifest-sha256',required=True);a=p.parse_args();run(a.action,a.reviewed_manifest_sha256.lower())
if __name__=='__main__':main()
