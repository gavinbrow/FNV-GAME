import sys,pickle,os,json
sys.path.insert(0,r'C:\Projects\Decompilation\runtime-next\data-v1'); sys.argv=[sys.argv[0]]
import place as PL
st=pickle.load(open(os.environ['TEMP']+r'\dv1_placed.pkl','rb'))
out={}
for (u,k),key in st.KEYOF.items():
    if u>=100000: continue
    pcs=st.PIECES.get((u,k))
    ent=[]
    if pcs:
        for a,b,pk in pcs:
            if pk in st.placed: ent.append((a,b,st.placed[pk][0]))
    else:
        if key in st.placed:
            s=st.SEC[key]; ent.append((0,s['size'],st.placed[key][0]))
    if ent: out['%d:%d'%(u,k)]=ent
json.dump(out,open(r'C:\Projects\Decompilation\runtime-next\link-v2\secmap.json','w'),separators=(',',':'))
print(len(out),len(st.KEYOF))
