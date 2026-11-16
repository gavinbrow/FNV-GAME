"""Compare two strict images (0xCC = not ours): bytes that were ours in A and are not in B (lost) / gained. usage: cmp_strict.py A.exe B.exe"""
import sys
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
import numpy as np, json
a=np.fromfile(sys.argv[1],np.uint8); b=np.fromfile(sys.argv[2],np.uint8)
n=min(len(a),len(b)); a=a[:n]; b=b[:n]
lost=np.flatnonzero((a!=0xcc)&(b==0xcc)); gained=np.flatnonzero((a==0xcc)&(b!=0xcc))
print('lost',len(lost),'gained',len(gained),'changed-nonCC',int(((a!=0xcc)&(b!=0xcc)&(a!=b)).sum()))
if len(lost):
    # cluster by 16
    import collections
    c=collections.Counter(int(x)//4096 for x in lost); print('lost pages',c.most_common(8)); print([hex(int(x)) for x in lost[:20]])
