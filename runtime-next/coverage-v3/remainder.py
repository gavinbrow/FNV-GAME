import sys, json; sys.dont_write_bytecode=True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
import numpy as np, re
from pathlib import Path
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\pinned-build'); sys.argv=['x']
import uncovered_v2 as U
H=Path(__file__).resolve().parent
cov=U.cover.copy()
for p in json.loads((H/'extra_pieces.json').read_text())['pieces']:
    a=p['address']-U.TEXT_VA; cov[a:a+p['size']]=4
rem=(cov==0)&U.nontriv
idx=np.flatnonzero(rem)
runs=[]; s=p=idx[0]
for i in idx[1:]:
    if i-p>64: runs.append((s,p+1)); s=i
    p=i
runs.append((s,p+1))
runs=sorted(runs,key=lambda r:-int(rem[r[0]:r[1]].sum()))
print('remaining nt',int(rem.sum()),'runs(gap>64)',len(runs))
t=bytes(U.text)
for s,e in runs[:12]:
    va=U.TEXT_VA+s; b=t[s:e]
    print('0x%08x'%va,'len',e-s,'nt',int(rem[s:e].sum()),'prologues',len(re.findall(rb'\x55\x8b\xec|\x8b\xff\x55\x8b\xec|\x83\xec|\x56\x57',b)),'rets',b.count(b'\xc3')+b.count(b'\xc2'),'calls',b.count(b'\xe8'),'first16',b[:16].hex(), 'names',U.names_in(s,e)[:3])

