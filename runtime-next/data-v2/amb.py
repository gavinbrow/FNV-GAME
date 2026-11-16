import sys,pickle,collections,os
sys.path.insert(0,r'C:\Projects\Decompilation\runtime-next\data-v1')
sys.argv=[sys.argv[0]]
import place as PL
T=os.environ['TEMP']
st=pickle.load(open(T+r'\dv1_placed.pkl','rb'))
SEC,placed,info=st.SEC,st.placed,st.info
groups=collections.defaultdict(list)
for k,s in SEC.items():
    if k in placed or s['kind']=='bss' or s['size']==0: continue
    nb=info.get(k,{}).get('nB')
    pat,kn=PL.fieldvals(s,{})
    sig=(s['kind'],bytes(pat),bytes(kn),s['flags']&0xf00000)
    groups[sig].append((k,nb))
tab=collections.Counter(); 
for sig,v in groups.items():
    kind=sig[0]; n=len(v); hits=v[0][1]
    tag='n==hits' if hits==n else ('n<hits' if hits is not None and hits>n else ('n>hits' if hits is not None and hits>=0 else 'hits='+str(hits)))
    tab[(kind,tag)]+=sum(len(sig[1]) for _ in v)
for k,v in sorted(tab.items(),key=lambda x:-x[1])[:30]: print(k,v)
