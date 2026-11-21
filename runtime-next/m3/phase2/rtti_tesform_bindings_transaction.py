"""Prepare/apply/restore one hash-guarded TESForm recipe transaction."""
import argparse,copy,hashlib,json,os,tempfile,time,sys
from pathlib import Path
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';E=M/'out/phase2-tesform-binding-repair-v2';T=M/'out/phase2-tesform-bindings-transaction';TARGET=F/'build/units.json';LOCK=RN/'build.lock'
GLOBAL_LOCK=Path('C:/path/to/Decompilation/runtime-next/build.lock')
EXPECTED_OLD='e883ac21f25808a7ebba172006e09ae803ae640bf12d389ad2c10641ddba1576';EXPECTED_NEW='fa36603e3e9a2ea495644f383db983a9269d2e7cf558282a80746439386dbfc8';REF='df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7'
EVIDENCE_SHA='d152d45a23c5587162e2cf72b7fddf09ae8144f3ede27a53f450d853b2dafad3'
CLOSURE=M/'out/phase2-tesform-base-mirror-v2/mirror-manifest.json';CLOSURE_SHA='0419fea8ee18ca1516ccd8af8302aab39fbc8fe1bb5d68e7ef999f758c423646'
def sha(b):return hashlib.sha256(b).hexdigest()
def validate_payloads(old,new,evidence):
 if sha(old)!=EXPECTED_OLD or sha(new)!=EXPECTED_NEW:raise ValueError('recipe payload mismatch')
 a=json.loads(old);b=json.loads(new)
 if a.keys()!=b.keys() or any(a[k]!=b[k] for k in a if k!='units') or len(a['units'])!=len(b['units']) or [i for i,(x,y) in enumerate(zip(a['units'],b['units'])) if x!=y]!=[998]:raise ValueError('recipe changes beyond unit998')
 x=a['units'][998];y=b['units'][998]
 if x.keys()!=y.keys() or any(x[k]!=y[k] for k in x if k!='symbols'):raise ValueError('unit998 non-symbol change')
 edits=evidence['symbol_edits'];expected={e['symbol'] for e in edits};changed={k for k in x['symbols'].keys()|y['symbols'].keys() if x['symbols'].get(k)!=y['symbols'].get(k)}
 if len(edits)!=7 or len(expected)!=7 or changed!=expected:raise ValueError('expected seven distinct symbol changes')
 for e in edits:
  if x['symbols'].get(e['symbol'])!=e['before'] or y['symbols'].get(e['symbol'])!=e['after']:raise ValueError('symbol edit mismatch')
 if evidence['archived_reference_matches']!=128 or evidence['production_reference_matches']!=128 or evidence['function_count']!=128:raise ValueError('strict reference proof absent')
 if evidence['inputs_sha256']['units']!=EXPECTED_OLD or evidence['inputs_sha256']['reference']!=REF or evidence['generated_units_sha256']!=EXPECTED_NEW:raise ValueError('evidence identity mismatch')

def prepare():
 evraw=(E/'manifest.json').read_bytes()
 if sha(evraw)!=EVIDENCE_SHA:raise ValueError('reviewed evidence digest changed')
 ev=json.loads(evraw);old=(E/'units.original').read_bytes();new=(E/'units.generated').read_bytes();validate_payloads(old,new,ev)
 T.mkdir(exist_ok=False);(T/'units.original').write_bytes(old);(T/'units.generated').write_bytes(new)
 meta={'schema_version':1,'target':'build/units.json','old_sha256':EXPECTED_OLD,'new_sha256':EXPECTED_NEW,'evidence_sha256':sha(evraw),'pinned_inputs':ev['inputs_sha256'],'scope':'seven unit998 symbol binding changes only; apply after exclusive build lane is released','recovery':'single-file atomic replacement; recover restores old bytes from either known state'}
 (T/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'status':'prepared','target':meta['target'],'new_sha256':EXPECTED_NEW}))

def acquire_guard():
 # FNV_BUILD_LOCK can configure the actual driver lock; also protect the normal
 # machine-wide path so an override never bypasses a live default build.
 paths={LOCK.resolve(),GLOBAL_LOCK.resolve()};override=os.environ.get('FNV_BUILD_LOCK')
 if override:paths.add(Path(override).resolve())
 acquired=[]
 try:
  for p in sorted(paths,key=str):
   fd=os.open(p,os.O_CREAT|os.O_EXCL|os.O_WRONLY);acquired.append(p)
   try:os.write(fd,('%d %.6f phase2-tesform-transaction'%(os.getpid(),time.time())).encode())
   finally:os.close(fd)
 except BaseException:
  for p in reversed(acquired):p.unlink()
  raise ValueError('build lock held or unavailable; transaction refused')
 return acquired

def atomic_write(path,data):
 fd,name=tempfile.mkstemp(prefix='tesform-recipe-',dir=T);tmp=Path(name)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(tmp,path)
 except BaseException:
  if tmp.exists():tmp.unlink()
  raise

def validate_current_inputs(ev):
 closure_raw=CLOSURE.read_bytes()
 if sha(closure_raw)!=CLOSURE_SHA:raise ValueError('source closure manifest changed')
 closure=json.loads(closure_raw)
 for name,digest in closure['original']['files'].items():
  path=(F/name).resolve()
  if not path.is_relative_to(F.resolve()) or sha(path.read_bytes())!=digest:raise ValueError('source closure changed '+name)
 inputs={'old_obj':RN/'pinned-build/obj_v3.bak-20261116/0998.obj','current_obj':RN/'pinned-build/obj_v3/0998.obj','sidecar':RN/'build-v7/sg_sidecar_w2.json','source':F/'src/fallout_shared/tesform.cpp'}
 sys.path.insert(0,str(RN));import paths as buildpaths
 inputs['reference']=Path(buildpaths.REF_IMAGE)
 for k,p in inputs.items():
  if sha(p.read_bytes())!=ev['inputs_sha256'][k]:raise ValueError('evidence input changed '+k)

def run(action):
 guards=acquire_guard()
 try:
  manifest=json.loads((T/'manifest.json').read_text());evraw=(E/'manifest.json').read_bytes();ev=json.loads(evraw);old=(T/'units.original').read_bytes();new=(T/'units.generated').read_bytes();validate_payloads(old,new,ev)
  if sha(evraw)!=EVIDENCE_SHA or sha(evraw)!=manifest['evidence_sha256'] or manifest['target']!='build/units.json' or manifest['old_sha256']!=EXPECTED_OLD or manifest['new_sha256']!=EXPECTED_NEW:raise ValueError('transaction manifest changed')
  if action=='apply':
   validate_current_inputs(ev)
  if action=='restore' and not (T/'applied.json').exists():raise ValueError('transaction was not applied')
  marker=T/(('recover-result-%d-%d.json'%(os.getpid(),time.time_ns())) if action=='recover' else action+'-result.json')
  if marker.exists():raise FileExistsError('action result already exists')
  cur=TARGET.read_bytes();current=sha(cur);allowed=([EXPECTED_OLD] if action=='apply' else [EXPECTED_NEW] if action=='restore' else [EXPECTED_OLD,EXPECTED_NEW])
  if current not in allowed:raise ValueError('target is not an authorized transaction state')
  wanted=new if action=='apply' else old;previous=cur;written=False;applied_owned=False;result_owned=False
  try:
   if cur!=wanted:atomic_write(TARGET,wanted);written=True
   with marker.open('x',encoding='utf8') as f:
    result_owned=True;json.dump({'action':action,'previous_sha256':current,'final_sha256':sha(wanted),'manifest_sha256':sha((T/'manifest.json').read_bytes())},f,indent=2)
   if action=='apply':
    with (T/'applied.json').open('x',encoding='utf8') as f:
     applied_owned=True;json.dump({'manifest_sha256':sha((T/'manifest.json').read_bytes())},f)
  except BaseException:
   if written:atomic_write(TARGET,previous)
   if result_owned and marker.exists():marker.unlink()
   if applied_owned and (T/'applied.json').exists():(T/'applied.json').unlink()
   raise
  print(json.dumps({'action':action,'sha256':sha(wanted)}))
 finally:
  for p in reversed(guards):p.unlink()
def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=('prepare','apply','restore','recover'));a=p.parse_args();prepare() if a.action=='prepare' else run(a.action)
if __name__=='__main__':main()
