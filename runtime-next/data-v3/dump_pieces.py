import sys,pickle,os,json
sys.path.insert(0,(__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\path\to\Decompilation') + r'\runtime-next\data-v1')); sys.argv=[sys.argv[0]]
import place as PL
st=pickle.load(open(os.environ['TEMP']+r'\dv1_placed.pkl','rb'))
out=[]
for k,(A,t) in st.placed.items():
    s=st.SEC[k]
    out.append(dict(va=A,size=len(s['data']),kind=s['kind'],tier=t,unit=s['units'][0],sec=s['name'],defs=[(d[0],d[1]) for d in s['defs'] if d[2]==2][:6]))
json.dump(out,open((__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\path\to\Decompilation') + r'\runtime-next\data-v3\produced_pieces.json'),'w'))
print(len(out),sum(1 for o in out if o['defs']))
