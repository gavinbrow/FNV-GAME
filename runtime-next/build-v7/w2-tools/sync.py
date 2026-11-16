import sys,glob,json,shutil,os
sys.path.insert(0,'.')
import w2lib as L
L.setup()
side={}
for f in sorted(glob.glob('auto/*.json')):
    i=int(os.path.basename(f)[:4])
    if not os.path.exists('auto/%04d.obj'%i): continue
    srcrel=L.U[i]['source']; src='C:/Projects/Decompilation/fnv_decomp/'+srcrel
    if os.path.exists('auto/%04d.cpp'%i) and open(src,'rb').read()!=open('auto/%04d.cpp'%i,'rb').read():
        if not os.path.exists(src+'.bak-20261115-w2'): shutil.copy(src,src+'.bak-20261115-w2')
        shutil.copy('auto/%04d.cpp'%i,src)
        if srcrel not in open('changed_files.txt').read(): open('changed_files.txt','a').write(srcrel+' (unit %d, backup .bak-20261115-w2)\n'%i)
    side[str(i)]=L.SG.make_sidecar(L._Coff((L.BAK/('%04d.obj'%i) if (L.BAK/('%04d.obj'%i)).exists() else L.PB/'obj_v3'/('%04d.obj'%i))),L.U[i].get('symbols',{}), L.A.G['sym'])
    shutil.copy('auto/%04d.obj'%i,'obj_v3/%04d.obj'%i)
json.dump(side,open('sg_sidecar_w2.json','w'))
shutil.copy('sg_sidecar_w2.json','C:/Projects/Decompilation/runtime-next/build-v7/sg_sidecar_w2.json')
print(len(side))
