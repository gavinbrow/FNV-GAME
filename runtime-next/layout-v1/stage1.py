# builds blocks (atoms + blobs tiling .text), loads records; saves pickle in scratchpad
import sys; sys.path.insert(0,'.')
from common import *
import pickle, bisect, collections, json, gzip
SCR = r'C:\Users\cjhub\AppData\Local\Temp\claude\d3df7c44bb2dc2c7\04ce5394-2d00-49a0-970d-e3a38a4b457e\scratchpad'
pe = PE(); TV = 0x401000; TS = 12441088
ref = np.frombuffer(pe.d, np.uint8)[1024:1024+TS]
strict = np.frombuffer(open(RN+r'\build-v6\FalloutNV_v6_strict.exe','rb').read(), np.uint8)[1024:1024+TS]
units = json.load(open(r'C:\Projects\Decompilation\fnv_decomp\build\units.json'))['units']
iv = []   # (start,end,kind,unit)
for i,u in enumerate(units):
    for f in u['functions']: a=int(f['address'],16)-TV; iv.append((a,a+f['size'],'fn',i))
    for t in u.get('eh_tails',[]): a=int(t['address'],16)-TV; iv.append((a,a+t['size'],'eh',i))
cp = json.load(open(RN+r'\build-v6\contrib_pieces.json'))
for p in cp['pieces']: a=int(p['address'])-TV; iv.append((a,a+int(p['size']),'contrib',-2))
iv = [x for x in iv if 0<=x[0]<x[1]<=TS]
iv.sort()
# merge overlaps; first listed owner (functions before tails) keeps unit
merged=[]
for s,e,k,u in iv:
    if merged and s < merged[-1][1]:
        m=merged[-1]; merged[-1]=(m[0],max(m[1],e),m[2],m[3])
    else: merged.append((s,e,k,u))
print('known atoms', len(merged))
# records
import csv
rows = []
with gzip.open(RN+r'\build-v6\relocs_v6.tsv.gz','rt') as f:
    r = csv.reader(f, delimiter='\t'); next(r)
    for x in r: rows.append(x)
F = np.array([int(x[0],16) for x in rows],np.int64)
KIND = np.array([x[1] for x in rows]); SRC=np.array([x[2] for x in rows]); ST=np.array([x[3] for x in rows]); ORG=np.array([x[4] for x in rows])
EXP = np.array([int(x[5],16) if x[5] else -1 for x in rows],np.int64)
print('records',len(F))
# leftover atoms: sites outside known atoms
starts = np.array([m[0] for m in merged]); ends=np.array([m[1] for m in merged])
off = F - TV
idx = np.searchsorted(starts, off, 'right')-1
inside = (idx>=0) & (off < ends[np.maximum(idx,0)])
left = np.where(~inside)[0]
print('sites outside known atoms', len(left), collections.Counter(ORG[left]))
# build leftover runs
bad = strict==0xcc
extra=[]
lo_sorted = sorted(set(int(o) for o in off[left]))
cur=None
def run_around(o):
    s=o
    # extend left while non-CC (bridge CC runs <=4 within 4 bytes of field)
    def okb(p): return not bad[p]
    a=o
    while a>0 and not (merged and False):
        if not bad[a-1]: a-=1
        else:
            # bridge short CC run if followed by non-CC
            k=1
            while a-1-k>=0 and bad[a-1-k] and k<5: k+=1
            if k<=4 and a-1-k>=0 and not bad[a-1-k]: a-=k
            else: break
    b=o+1
    while b<TS:
        if not bad[b]: b+=1
        else:
            k=0
            while b+k<TS and bad[b+k] and k<5: k+=1
            if k<=4 and b+k<TS and not bad[b+k]: b+=k
            else: break
    return a,b
done=set()
for o in lo_sorted:
    if any(a<=o<b for a,b in extra[-1:]): continue
    a,b=run_around(o)
    # clip to gaps between known atoms
    j=bisect.bisect_right(starts.tolist(), o)-1
    gs = ends[j] if j>=0 else 0
    k=j+1; ge = starts[k] if k<len(starts) else TS
    a=max(a,gs); b=min(b,ge)
    extra.append((a,b))
extra=sorted(set(extra))
ex=[list(x) for x in extra]
exs=[x[0] for x in ex]
for o in lo_sorted:
    j=bisect.bisect_right(exs,o)-1
    if j>=0 and ex[j][0]<=o<ex[j][1] and ex[j][1]<o+4:
        ex[j][1]=o+4
extra=[tuple(x) for x in ex]
mergedx=[]
for a,b in extra:
    if mergedx and a<mergedx[-1][1]: mergedx[-1]=(mergedx[-1][0],max(b,mergedx[-1][1]))
    else: mergedx.append((a,b))
print('leftover atoms',len(mergedx), sum(b-a for a,b in mergedx))
atoms = sorted(merged+[(a,b,'other',-1) for a,b in mergedx])
# tile: blocks = atoms w/ trailing pad; blobs between
PADV = (0xcc,0x00,0x90)
blocks=[] # (start,end,type,unit)
pos=0
def padrun(a,b):
    # return end of leading-pad within [a,b)
    p=a
    while p<b and ref[p] in PADV: p+=1
    return p
for i,(s,e,k,u) in enumerate(atoms):
    if s>pos:
        # gap pos..s : leading pad goes to previous block, rest is blob
        p=padrun(pos,s)
        if blocks and p>pos: bs,be,bt,bu=blocks[-1]; blocks[-1]=(bs,p,bt,bu); pos=p
        if s>pos: blocks.append((pos,s,'blob',-1))
    nxt = atoms[i+1][0] if i+1<len(atoms) else TS
    blocks.append((s,e,'atom_'+k,u)); pos=e
    p=padrun(pos,nxt); 
    bs,be,bt,bu=blocks[-1]; blocks[-1]=(bs,p,bt,bu); pos=p
if pos<TS: blocks.append((pos,TS,'blob',-1))
assert blocks[0][0]==0 and all(blocks[i][1]==blocks[i+1][0] for i in range(len(blocks)-1)) and blocks[-1][1]==TS
print('blocks',len(blocks),collections.Counter(b[2] for b in blocks))
for t in set(b[2] for b in blocks): print(t, sum(b[1]-b[0] for b in blocks if b[2]==t))
pickle.dump(dict(blocks=blocks,F=F,KIND=KIND,SRC=SRC,ST=ST,ORG=ORG,EXP=EXP), open(SCR+r'\s1.pkl','wb'))
