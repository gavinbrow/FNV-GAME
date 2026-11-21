"""Read-only full selector replay against actual compiled private skip."""
import argparse,hashlib,json,os,sys,time
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M/'out/phase2-psa-metadata-ownership-proposal';E=M/'out/phase2-native-source-positive/evidence';DEST=P/'compiled-selector-replay-v3';SRC=M/'dv1_splice.py';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def validate():
 if any(k.upper() in ('CL','_CL_') or k.upper().startswith(('FNV_','DV_','CODEX_NEGATIVE')) for k in os.environ):raise ValueError('inherited build environment forbidden')
 pins=json.loads((P/'compiled-fixture-v3-pins.json').read_bytes())
 for n,d in pins['files'].items():
  if h(Path(n))!=d:raise ValueError('input changed '+n)
 if h(Path(pins['reference_path']))!=pins['reference_expected']:raise ValueError('reference changed')
 result=json.loads((P/'compiled-m3-v3/fixture-result.json').read_bytes())
 if result['pins_sha256']!=h(P/'compiled-fixture-v3-pins.json'):raise ValueError('fixture pin mismatch')
 for n,d in result['files'].items():
  if h(P/'compiled-m3-v3'/n)!=d:raise ValueError('fixture output changed '+n)
 if DEST.exists():raise FileExistsError(DEST)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--validate-only',action='store_true');a=ap.parse_args();validate()
 if a.validate_only:print('PASS selector preflight');return
 sys.path.insert(0,str(M.parent));import buildlock
 fd=os.open(buildlock.LOCK,os.O_CREAT|os.O_EXCL|os.O_WRONLY);owned=False
 try:
  owned=True;os.write(fd,('%d %f psa-selector-fixture'%(os.getpid(),time.time())).encode());os.close(fd);fd=None;validate()
  s=SRC.read_text();pairs=[("GEN = os.path.join(HERE, 'gen')","GEN = "+repr(str((P/'compiled-m3-v3').resolve()))),("os.path.join(RN, 'data-v3', 'symbolic.json')",repr(str((E/'data-v3-symbolic.json').resolve()))),("os.path.join(RN, 'data-v3', 'out', 'manifest.json')",repr(str((E/'data-v3-manifest.json').resolve())))]
  for old,new in pairs:
   if s.count(old)!=1:raise ValueError('selector source changed')
   s=s.replace(old,new,1)
  DEST.mkdir();os.environ['FNV_M3_DV1_OUT']=str(DEST.resolve());os.environ['FNV_M3_DV1_EXT']='1';os.environ['FNV_M3_LIB_SELECTION']=str((M/'phase2/library_candidates.json').resolve());os.environ['FNV_M3_LIB_SHA256']='74e3815454a8926ee3d8f70abf939e8d61eadd7173a7514c93e66fee92589700';sys.argv=[str(SRC),str((E/'data-v1-scratch/dv1_placed.pkl').resolve())];exec(compile(s,str(SRC),'exec'),{'__name__':'__main__','__file__':str(SRC.resolve())})
 finally:
  if fd is not None:os.close(fd)
  if owned:
   try:os.unlink(buildlock.LOCK)
   except FileNotFoundError:pass
if __name__=='__main__':main()
