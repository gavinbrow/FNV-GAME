import json,re,os,collections,struct,sys,pickle
sys.path.insert(0,r'C:\Projects\Decompilation\runtime-next\data-v1'); sys.argv=[sys.argv[0]]
import place as PL
st=pickle.load(open(os.environ['TEMP']+r'\dv1_placed.pkl','rb'))
simple=re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
cand=[]
for k,(A,t) in st.placed.items():
    s=st.SEC[k]
    if s['kind']!='vtable': continue
    prim=[d for d in s['defs'] if d[0].startswith('??_7') and d[0].endswith('@@6B@') and d[2]==2]
    if len(prim)!=1: continue
    ours=prim[0][0][4:-5]; va=A+prim[0][1]
    cp=PL.refread(va-4); 
    if not cp: continue
    col=struct.unpack('<I',cp)[0]; b=PL.refread(col,20)
    if not b: continue
    sig,off,cd,ptd,ph=struct.unpack('<5I',b)
    if sig!=0 or off!=0: continue
    nm=PL.refread(ptd+8,200).split(b'\0')[0].decode('latin1')
    if not nm.startswith('.?AV') and not nm.startswith('.?AU'): continue
    orig=nm[4:-2]
    if simple.match(ours) and simple.match(orig) and ours!=orig: cand.append((ours,orig,va,s['units'][:4],'class' if nm.startswith('.?AV') else 'struct'))
print(len(cand))
want={c[0] for c in cand}|{c[1] for c in cand}
S='C:/Projects/Decompilation/fnv_decomp/src'
idx=collections.defaultdict(set); tok=re.compile(rb'[A-Za-z_][A-Za-z0-9_]*')
nfiles=0
for root,ds,fs in os.walk(S):
    for f in fs:
        if not f.endswith(('.cpp','.h')): continue
        p=os.path.join(root,f); nfiles+=1
        for t in set(tok.findall(open(p,'rb').read())):
            t=t.decode('latin1')
            if t in want: idx[t].add(os.path.relpath(p,S).replace(chr(92),'/'))
print('files',nfiles)
good=[]
for ours,orig,va,us,kw in cand:
    fo=idx.get(ours,set()); fn=idx.get(orig,set())
    if len(fo)==1 and next(iter(fo)) not in fn: good.append(dict(old=ours,new=orig,va=hex(va),file=next(iter(fo)),units=us,kw=kw))
print('good',len(good))
json.dump(good,open('batch_cands.json','w'),indent=0)
c=collections.Counter(g['file'] for g in good); print(len(c)); print(c.most_common(5))
for g in good[:10]: print(g)
