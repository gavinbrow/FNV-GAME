import sys, json
sys.dont_write_bytecode=True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
import numpy as np
sys.path.insert(0, r'C:\Projects\Decompilation\fnv_decomp\tools')
from compare import Pe
ref=Pe(r'C:\Projects\Decompilation\FNV\work\worker1\FalloutNV.runtime-text.exe')
st=Pe(r'C:\Projects\Decompilation\runtime-next\build-v4\FalloutNV_v4_strict.exe')
rva,vs,rs,raw=ref.sections[0]
R=np.frombuffer(ref.data,np.uint8)[raw:raw+rs]
rva2,vs2,rs2,raw2=st.sections[0]
S=np.frombuffer(st.data,np.uint8)[raw2:raw2+rs2]
print(rs,rs2,ref.base+rva)
diff=(S!=R)
print('S!=R',int(diff.sum()))
pad=np.isin(R,(0xcc,0x00))
print('diff nonpad',int((diff&~pad).sum()))
d=diff&~pad
idx=np.flatnonzero(d)
br=np.flatnonzero(np.diff(idx)>1)
starts=np.concatenate(([idx[0]],idx[br+1])); ends=np.concatenate((idx[br],[idx[-1]]))+1
L=ends-starts
print('runs',len(L))
import collections
for lim in (4,8,16,32,64):
    print(lim,int(L[L<=lim].sum()),int((L<=lim).sum()))
FN=r'C:\Projects\Decompilation\fnv_decomp'
units=json.load(open(FN+r'\build\units.json'))['units']
TV=ref.base+rva
cov=np.zeros(rs,np.uint8)
for u in units:
    for f in u['functions']:
        a=int(f['address'],16)-TV; cov[a:a+f['size']]=1
    for t in u.get('eh_tails',[]):
        a=int(t['address'],16)-TV; seg=cov[a:a+t['size']]; seg[seg==0]=2
ep=json.load(open('extra_pieces.json'))['pieces']
print(collections.Counter(p['kind'] for p in ep))
for p in ep:
    a=p['address']-TV; seg=cov[a:a+p['size']]; seg[seg==0]=3 if p['kind']=='eh' else 4
u0=d&(cov==0)
print('uncovered diffs',int(u0.sum()),'covered diffs (borrowed)',int((d&(cov>0)).sum()))
print('ref0x90 in u0',int((u0&(R==0x90)).sum()))
for c in (1,2,3,4): print('cov',c,'diff',int((d&(cov==c)).sum()))
# diffs in cov3 runs: lengths
m3=d&(cov==3); i3=np.flatnonzero(m3); print('cov3 diff bytes',len(i3))
# are cov3 diffs in runs >4?
if len(i3):
    b=np.flatnonzero(np.diff(i3)>1); s=np.concatenate(([i3[0]],i3[b+1])); e=np.concatenate((i3[b],[i3[-1]]))+1
    L3=e-s; print('cov3 runs',len(L3),'bytes in runs>4',int(L3[L3>4].sum()),'<=4',int(L3[L3<=4].sum()))
import gzip
B=np.zeros(rs,bool)
f=gzip.open(r'C:\Projects\Decompilation\runtime-next\build-v4\relocs_v4.tsv.gz','rt'); f.readline()
nb=0
for l in f:
    p=l.rstrip('\n').split('\t')
    if p[3]!='agree':
        a=int(p[0],16)-TV; B[a:a+4]=True; nb+=1
print('nonagree sites',nb,'B bytes',int(B.sum()))
rest=d&~B
print('rest',int(rest.sum()),'ref90',int((rest&(R==0x90)).sum()))
np.save('rest_mask.npy',rest)
rest2=diff&~B
print('rest2',int(rest2.sum()),'ref0',int((rest2&(R==0)).sum()),'ref90',int((rest2&(R==0x90)).sum()),'cov0',int((rest2&(cov==0)).sum()))
np.save('rest2_mask.npy',rest2)
