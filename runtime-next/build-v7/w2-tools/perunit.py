import sys,pickle,json,collections
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
import numpy as np
A=pickle.load(open(sys.argv[1]+'.pkl','rb')); B=pickle.load(open(sys.argv[2]+'.pkl','rb'))
G=pickle.load(open('../gaps/dump.pkl','rb')); TV=G['TEXT_VA']; ref=G['ref']
pad=np.isin(ref,(0xcc,0))
oa=(A['Wm']>0)&(A['B']==0)&~pad; ob=(B['Wm']>0)&(B['B']==0)&~pad
U=json.load(open('C:/Projects/Decompilation/fnv_decomp/build/units.json'))['units']
res={}
for i,u in enumerate(U):
    d=0
    for f in u['functions']:
        a=int(f['address'],16)-TV; d+=int(ob[a:a+f['size']].sum())-int(oa[a:a+f['size']].sum())
    for t in u.get('eh_tails',[]):
        a=int(t['address'],16)-TV; d+=int(ob[a:a+t['size']].sum())-int(oa[a:a+t['size']].sum())
    if d: res[i]=d
neg={k:v for k,v in res.items() if v<0}
print('units changed',len(res),'total',sum(res.values()),'neg',neg)
print('pos',sum(v for v in res.values() if v>0))
