"""Isolated selector replay; archived snapshot and provisional skip only."""
import os,sys,hashlib
from pathlib import Path
M=Path(__file__).resolve().parent.parent;R=M.parent;P=M/'out/phase2-psa-metadata-ownership-proposal';E=M/'out/phase2-native-source-positive/evidence';src=M/'dv1_splice.py';output=P/'compiled-selector-replay'
if output.exists() or not (P/'compiled-m3/fixture-result.json').is_file():raise ValueError('missing compiled fixture or existing output')
output.mkdir();s=src.read_text();pairs=[("GEN = os.path.join(HERE, 'gen')","GEN = "+repr(str((P/'compiled-m3').resolve()))),("os.path.join(RN, 'data-v3', 'symbolic.json')",repr(str((E/'data-v3-symbolic.json').resolve()))),("os.path.join(RN, 'data-v3', 'out', 'manifest.json')",repr(str((E/'data-v3-manifest.json').resolve())))]
for a,b in pairs:
 if s.count(a)!=1:raise ValueError('selector anchor mismatch '+a)
 s=s.replace(a,b,1)
os.environ['FNV_M3_DV1_OUT']=str(output.resolve());os.environ['FNV_M3_DV1_EXT']='1';os.environ['FNV_M3_LIB_SELECTION']=str((M/'phase2/library_candidates.json').resolve());os.environ['FNV_M3_LIB_SHA256']='74e3815454a8926ee3d8f70abf939e8d61eadd7173a7514c93e66fee92589700';sys.argv=[str(src),str((E/'data-v1-scratch/dv1_placed.pkl').resolve())];exec(compile(s,str(src),'exec'),{'__name__':'__main__','__file__':str(src.resolve())})
