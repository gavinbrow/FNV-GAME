import sys,pickle,os,struct,collections
sys.path.insert(0,r'C:\Projects\Decompilation\runtime-next\data-v1'); sys.argv=[sys.argv[0]]
import place as PL
st=pickle.load(open(os.environ['TEMP']+r'\dv1_placed.pkl','rb'))
vals=collections.Counter()
for k,s in st.SEC.items():
    if s['kind']=='crt-init-array' and s['name']=='.CRT$XCU' and k not in st.placed:
        res,src=st.resolve(s)
        for v in res.values(): vals[v]+=1
print(len(vals),sum(vals.values()),'dups',sum(1 for v in vals.values() if v>1))
blob=PL.RB['.rdata'];va0=PL.SECS['.rdata'][0]
tl,th=PL.SECS['.text'][0],PL.SECS['.text'][0]+PL.SECS['.text'][1]
runs=[];i=0;n=len(blob)//4
d=struct.unpack('<%dI'%n,blob[:n*4])
inr=[tl<=x<th for x in d]
i=0
while i<n:
    if inr[i]:
        j=i
        while j<n and inr[j]: j+=1
        runs.append((j-i,i,j));i=j
    else: i+=1
runs.sort(reverse=True)
for ln,a,b in runs[:6]:
    arr=d[a:b]
    print(hex(va0+4*a),ln,'ours',sum(1 for x in arr if x in vals),'sorted',sum(1 for p,q in zip(arr,arr[1:]) if q>=p))
