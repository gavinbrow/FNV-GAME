import sys,pickle,os,struct,collections
sys.path.insert(0,r'C:\Projects\Decompilation\runtime-next\data-v1'); sys.argv=[sys.argv[0]]
import place as PL
st=pickle.load(open(os.environ['TEMP']+r'\dv1_placed.pkl','rb'))
for k,s in st.SEC.items():
    if s['kind']!='crt-init-array': continue
    res,src=st.resolve(s)
    nrel=sum(1 for r in s['relocs'] if r[1]==6)
    hits,cap=PL.search(s,res) if res else (None,0)
    print(s['units'][:3],s['name'],s['size'],'relocs',nrel,'resolved',len(res),collections.Counter(src.values()),'hits',None if hits is None else len(hits),cap)
print('----')
import struct
for k,s in st.SEC.items():
    if s['kind']=='crt-init-array' and s['size'] in (13460,752,284,5232):
        res,src=st.resolve(s); vals=[res[o] for o in sorted(res)]
        blob=PL.RB['.rdata']; va0=PL.SECS['.rdata'][0]
        pos=blob.find(struct.pack('<I',vals[0]))
        # all occurrences
        occ=[];p=blob.find(struct.pack('<I',vals[0]))
        while p>=0: occ.append(p);p=blob.find(struct.pack('<I',vals[0]),p+1)
        print(s['size'],len(vals),[hex(va0+o) for o in occ[:5]],'first vals',[hex(v) for v in vals[:4]])
        for o in occ[:2]:
            ref4=[struct.unpack_from('<I',blob,o+4*i)[0] for i in range(6)]
            print('   ref seq',[hex(x) for x in ref4],'ours',[hex(x) for x in vals[:6]])
        break
