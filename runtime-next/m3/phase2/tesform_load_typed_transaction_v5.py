"""Guard staged typed TESForm/BGSE edits; never run a build with mirror labels."""
import argparse,hashlib,json,os,sys,tempfile,time
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';T=M/'out/phase2-tesform-load-typed-v5-transaction';sys.path.insert(0,str(H));import rtti_tesform_bindings_transaction as lock
PROOF='bd2ecfa08253d9588461be016bf55174add34f0f487c12b6eff7cedfd1fd2b38';FA='fa36603e3e9a2ea495644f383db983a9269d2e7cf558282a80746439386dbfc8';REL=['src/fallout_shared/tesform.cpp','src/fallout_shared/tesform_TESForm.h','src/bgsencounterzone.cpp','src/bgsencounterzone_decls.h','src/bgsencounterzone_TESForm.h','build/units.json']
def sha(b):return hashlib.sha256(b).hexdigest()
def manifest():
 b=(T/'manifest.json').read_bytes()
 if sha(b)!=PROOF:raise ValueError('reviewed transaction manifest changed')
 m=json.loads(b)
 if m['base_units_sha256']!=FA or [x['path'] for x in m['files']]!=REL or len(m['unit998_function_remaps'])!=11 or len(m['unit2_function_remaps'])!=9:raise ValueError('transaction scope changed')
 sys.path.insert(0,str(RN));import paths as buildpaths
 if sha(Path(buildpaths.REF_IMAGE).read_bytes())!='df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7':raise ValueError('reference image changed')
 audit=(M/'out/phase2-bgs-surrogate-ownership.json').read_bytes()
 if sha(audit)!=m['surrogate_ownership_evidence_sha256']:raise ValueError('surrogate ownership evidence changed')
 for name,d in m['evidence_sha256'].items():
  if sha((M/'out'/name).read_bytes())!=d:raise ValueError('proof changed '+name)
 return m

def atomic_write(path,data):
 fd,name=tempfile.mkstemp(prefix='typed-class-',dir=T);temp=Path(name)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(temp,path)
 except BaseException:
  if temp.exists():temp.unlink()
  raise

def validate_closures():
 audit=json.loads((M/'out/phase2-bgs-surrogate-ownership.json').read_bytes());index=hashlib.sha256();objects=sorted((RN/'pinned-build/obj_v3').glob('*.obj'))
 for p in objects:index.update(p.name.encode()+b'\0'+hashlib.sha256(p.read_bytes()).digest())
 if len(objects)!=audit['production_object_count'] or index.hexdigest()!=audit['production_object_index_sha256']:raise ValueError('production object set changed after ownership audit')
 for key,p in [('dv1',M/'gen/dv1_pieces.json'),('m3',M/'gen/m3_manifest.json'),('symbolic',RN/'data-v3/symbolic.json')]:
  if sha(p.read_bytes())!=audit['input_sha256'][key]:raise ValueError('ownership input changed '+key)
 for folder in ('phase2-tesform-load-typed-v4-mirror','phase2-bgs-load-typed-v4-mirror'):
  c=json.loads((M/'out'/folder/'mirror-manifest.json').read_text())
  for rel,d in c['original_inputs'].items():
   p=(F/rel).resolve()
   if not p.is_relative_to(F.resolve()) or sha(p.read_bytes())!=d:raise ValueError('original source closure changed '+rel)

def correction(m,require_current_objects):
 c=T/'production-correction';raw=(c/'manifest.json').read_bytes();e=json.loads(raw);old=(c/'units.original').read_bytes();new=(c/'units.generated').read_bytes();recipe=m['files'][-1]
 if e['transaction_manifest_sha256']!=PROOF or sha(old)!=recipe['new_sha256'] or e['original_sha256']!=sha(old) or e['generated_sha256']!=sha(new) or e['unit998_matches']!=128 or e['unit2_diagnostic_matches']!=24:raise ValueError('production correction evidence mismatch')
 a=json.loads(old);b=json.loads(new)
 if a.keys()!=b.keys() or any(a[k]!=b[k] for k in a if k!='units') or len(a['units'])!=len(b['units']) or [i for i,(x,y) in enumerate(zip(a['units'],b['units'])) if x!=y] not in ([],[998]):raise ValueError('correction exceeds unit998')
 u=a['units'][998];v=b['units'][998]
 if u.keys()!=v.keys() or any(u[k]!=v[k] for k in u if k!='symbols'):raise ValueError('correction changed non-symbol attributes')
 allowed={x['production_label']:x['binding'] for x in e['literal_facts']}
 changed={k for k in u['symbols'].keys()|v['symbols'].keys() if u['symbols'].get(k)!=v['symbols'].get(k)}
 if any(k not in allowed or v['symbols'].get(k)!=allowed[k] for k in changed):raise ValueError('correction contains unsupported binding')
 if require_current_objects:
  for path,key in [(RN/'pinned-build/obj_v3/0998.obj','tes_object_sha256'),(RN/'pinned-build/obj_v3/0002.obj','bgs_object_sha256')]:
   if sha(path.read_bytes())!=e[key]:raise ValueError('production object changed after correction proof')
 return raw,e,new

def run(action,ack=False):
 if action=='apply' and not ack:raise ValueError('explicit mirror-label acknowledgment required; no build until production reproof')
 if action=='correct' and not ack:raise ValueError('explicit independently reviewed production-correction acknowledgment required')
 guards=lock.acquire_guard()
 try:
  m=manifest();ops=[]
  if action=='apply':validate_closures()
  if action=='correct':
   if not (T/'applied.json').exists():raise ValueError('typed transaction was not applied')
   raw,e,new=correction(m,True);path=F/'build/units.json';previous=path.read_bytes();marker=T/'correct-result.json'
   if marker.exists():raise FileExistsError('correction already recorded')
   if sha(previous)!=m['files'][-1]['new_sha256']:raise ValueError('recipe differs from staged candidate')
   for x in m['files'][:-1]:
    if sha((F/x['path']).read_bytes())!=x['new_sha256']:raise ValueError('installed source changed '+x['path'])
   owned=False;written=False
   try:
    if previous!=new:atomic_write(path,new);written=True
    with marker.open('x',encoding='utf8') as f:
     owned=True;json.dump({'correction_manifest_sha256':sha(raw),'corrected_recipe_sha256':sha(new)},f)
   except BaseException:
    if written:atomic_write(path,previous)
    if owned and marker.exists():marker.unlink()
    raise
   print(json.dumps({'action':'correct','recipe_sha256':sha(new)}));return
  if action=='restore' and not (T/'applied.json').exists():raise ValueError('transaction not applied')
  marker=T/(('recover-%d-%d.json'%(os.getpid(),time.time_ns())) if action=='recover' else action+'-result.json')
  if marker.exists():raise FileExistsError('action already recorded')
  for x in m['files']:
   p=(F/x['path']).resolve()
   if not p.is_relative_to(F.resolve()):raise ValueError('path escapes source tree')
   old=(T/x['original']).read_bytes();new=(T/x['generated']).read_bytes();cur=p.read_bytes()
   if sha(old)!=x['old_sha256'] or sha(new)!=x['new_sha256']:raise ValueError('payload changed')
   valid=[x['old_sha256']] if action=='apply' else [x['new_sha256']] if action=='restore' else [x['old_sha256'],x['new_sha256']]
   if x['path']=='build/units.json' and action in ('restore','recover') and (T/'correct-result.json').exists():
    cr,ce,cn=correction(m,False);record=json.loads((T/'correct-result.json').read_bytes())
    if record.get('correction_manifest_sha256')!=sha(cr) or record.get('corrected_recipe_sha256')!=sha(cn):raise ValueError('correction record changed')
    valid.append(sha(cn))
   if sha(cur) not in valid:raise ValueError('unknown file state '+x['path'])
   ops.append((p,cur,new if action=='apply' else old))
  changed=[];result_owned=False;applied_owned=False
  try:
   for p,cur,new in ops:
    if cur!=new:atomic_write(p,new);changed.append((p,cur))
   with marker.open('x',encoding='utf8') as f:
    result_owned=True;json.dump({'action':action,'manifest_sha256':PROOF,'status':'production-literal-reproof-required' if action=='apply' else 'restored'},f)
   if action=='apply':
    with (T/'applied.json').open('x',encoding='utf8') as f:
     applied_owned=True;json.dump({'manifest_sha256':PROOF,'production_literal_reproof_required':True},f)
  except BaseException:
   for p,cur in reversed(changed):atomic_write(p,cur)
   if result_owned and marker.exists():marker.unlink()
   if applied_owned and (T/'applied.json').exists():(T/'applied.json').unlink()
   raise
  print(json.dumps({'action':action,'files':len(ops),'production_literal_reproof_required':action=='apply'}))
 finally:
  for p in reversed(guards):p.unlink()
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=('apply','correct','restore','recover'));p.add_argument('--ack-mirror-labels',action='store_true');p.add_argument('--ack-production-correction',action='store_true');a=p.parse_args();run(a.action,a.ack_production_correction if a.action=='correct' else a.ack_mirror_labels)
if __name__=='__main__':main()
