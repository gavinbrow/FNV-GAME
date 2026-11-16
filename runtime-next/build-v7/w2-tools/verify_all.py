import sys,glob,os,json
sys.path.insert(0,'.')
import w2lib as L
L.setup()
units=sorted(int(os.path.basename(f)[:4]) for f in glob.glob('auto/*.json'))
res={}
for i in units:
    src=L.U[i]['source']
    objp=L.W2/'auto'/('v%04d.obj'%i)
    ok,out=L.compile_src(i,src,objp)
    if not ok: print(i,'COMPILE FAIL'); continue
    a=L.evalunit(i); b=L.evalunit(i,objp)
    rg=L.regress(a,b); res[i]=(L.score(b)-L.score(a),len(rg))
    print(i,src,'gain',res[i][0],'regress',{hex(k):v for k,v in list(rg.items())[:3]})
json.dump(res,open('verify_all.json','w'))
print('total gain',sum(v[0] for v in res.values()),'regressed units',[i for i,v in res.items() if v[1]])
