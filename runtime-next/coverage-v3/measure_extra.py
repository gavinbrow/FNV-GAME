"""Shows what the extra pieces add: blank every recipe-uncovered .text byte (0xCC) in strict v2, then apply the pieces."""
import sys, json, subprocess; sys.dont_write_bytecode=True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
import numpy as np
from pathlib import Path
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\pinned-build'); sys.argv=['x']
import uncovered_v2 as U
H=Path(__file__).resolve().parent
R=np.fromfile(U.IMG,np.uint8); S=np.fromfile(r'C:\Projects\Decompilation\runtime-next\pinned-build\FalloutNV_pinned_strict_v2.exe',np.uint8)
raw=U.TEXT_RAW; rs=U.TEXT_N
B=S.copy(); seg=B[raw:raw+rs]; seg[U.cover==0]=0xcc
B.tofile(H/'strict_v2_uncovered_blanked.exe')
subprocess.check_call([sys.executable,'-I',str(H/'apply_extra.py'),str(H/'strict_v2_uncovered_blanked.exe'),str(H/'strict_v2_uncovered_blanked_plus_extra.exe')])
P=np.fromfile(H/'strict_v2_uncovered_blanked_plus_extra.exe',np.uint8)
unc=np.zeros(len(R),bool); unc[raw:raw+rs]=(U.cover==0)
for n,a in (('strict_v2',S),('uncovered blanked',B),('blanked + extra',P)):
    d=a!=R; print(n,'total diff',int(d.sum()),'in uncovered',int((d&unc).sum()),'non-trivial ref bytes in uncovered diff',int((d&unc&~np.isin(R,(0xcc,0x90,0))).sum()))
J=json.loads((H/'extra_pieces.json').read_text())['pieces']
# bytes of pieces that are relocation fields borrowed from the reference
print('pieces',len(J),'bytes',sum(p['size'] for p in J))
