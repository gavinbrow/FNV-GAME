import json,bisect,re,sys
sys.path.insert(0,r'C:\Projects\Decompilation\runtime-next\data-v3')
from common import *
inf=json.load(open(r'C:\Projects\Decompilation\runtime-next\build-v7\inferred_literals_v7.json'))
units=load_units()
fr=sorted((int(f['address'],16),int(f['address'],16)+f['size'],i,f['symbol']) for i,u in enumerate(units) for f in u['functions'])
ks=[x[0] for x in fr]
S='C:/Projects/Decompilation/fnv_decomp/'
rows=[]
for k,v in sorted(inf.items()):
    va=int(k,16);val=int(v,16);j=bisect.bisect_right(ks,va)-1;a,e,ui,sym=fr[j]
    src=units[ui]['source']
    t=open(S+src,encoding='latin1').read()
    pats=['0x%x'%val,'0x%08x'%val,'0x%X'%val,str(val)]
    hits=[(i+1,l.strip()[:110]) for i,l in enumerate(t.split('\n')) if any(re.search(r'(?<![0-9a-fA-Fx])'+re.escape(p)+r'(?![0-9a-fA-F])',l) for p in pats)]
    rows.append((k,v,sym[:50],src.split('/')[-1],hits[:3]))
json.dump(rows,open('inf_list.json','w'))
print(len(rows))
for r in rows[:100]: print(r[0],r[1],r[2],r[3],r[4][:2])
