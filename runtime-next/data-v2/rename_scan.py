import sys,pickle,os,struct,collections,re,json
sys.path.insert(0,r'C:\Projects\Decompilation\runtime-next\data-v1'); sys.argv=[sys.argv[0]]
import place as PL
st=pickle.load(open(os.environ['TEMP']+r'\dv1_placed.pkl','rb'))
M=0xffffffff
def rd(va,n=4): return PL.refread(va,n)
def cstr(va):
    b=PL.refread(va,200)
    return b.split(b'\0')[0].decode('latin1') if b else None
out=[];c=collections.Counter()
for k,(A,t) in st.placed.items():
    s=st.SEC[k]
    if s['kind']!='vtable': continue
    prim=[d for d in s['defs'] if d[0].startswith('??_7') and d[0].endswith('@@6B@') and d[2]==2]
    if not prim: c['no-primary']+=1; continue
    ours=prim[0][0][4:-5]
    off=prim[0][1]; va=A+off
    cp=rd(va-4)
    if not cp: c['nocol']+=1; continue
    col=struct.unpack('<I',cp)[0]; b=rd(col+12) 
    if not b: c['nocol2']+=1; continue
    td=struct.unpack('<I',b)[0]; nm=cstr(td+8)
    if not nm or not nm.startswith('.?A'): c['notd']+=1; continue
    orig=nm[4:-2]   # strip '.?AV' and '@@'
    same=(orig==ours)
    c['same' if same else 'differ']+=1
    out.append(dict(ours=ours,orig=orig,va=hex(va),units=s['units'][:3],tier=t))
json.dump(out,open('rename_scan.json','w'))
print(c)
import random
d=[x for x in out if x['ours']!=x['orig']]
for x in d[:25]: print(x['ours'],'->',x['orig'])
