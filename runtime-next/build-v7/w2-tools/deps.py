import sys,glob,json,os
sys.path.insert(0,'.')
import w2lib as L, autohdr as H
L.setup()
hdrs=set()
for f in glob.glob('auto/*.hdr.json'): hdrs.add(json.load(open(f))['header'])
dep=set()
for h in hdrs: dep |= set(H.dependents(h))
print(len(hdrs),'headers',len(dep),'dependent units')
n=0
for d in sorted(dep):
    if os.path.exists('auto/%04d.json'%d) and os.path.exists('auto/%04d.obj'%d):
        # unit already edited: recompile its current source (includes header edits) and re-verify
        pass
    op=L.W2/'auto'/('%04d.obj'%d)
    ok,_=L.compile_src(d,L.U[d]['source'],L.W2/'auto'/('d%04d.obj'%d))
    if not ok: print(d,'COMPILE FAIL'); continue
    a=L.evalunit(d); b=L.evalunit(d,L.W2/'auto'/('d%04d.obj'%d)); rg=L.regress(a,b)
    if rg: print(d,'REGRESS',len(rg)); continue
    import shutil; shutil.copy('auto/d%04d.obj'%d,op); n+=1
    if not os.path.exists('auto/%04d.json'%d): json.dump(dict(unit=d,source=L.U[d]['source'],gain=L.score(b)-L.score(a),log=['header dependent']),open('auto/%04d.json'%d,'w'))
print('ok',n)
