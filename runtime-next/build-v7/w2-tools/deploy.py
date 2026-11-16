import os,shutil,glob
PB='C:/Projects/Decompilation/runtime-next/pinned-build/'
bak=PB+'obj_v3.bak-20261115/'; ed=set(open('edited_units.txt').read().split())
n=0
for f in glob.glob('obj_v3/*.obj'):
    nm=os.path.basename(f); dst=PB+'obj_v3/'+nm
    if os.path.exists(dst) and open(dst,'rb').read()==open(f,'rb').read(): ed.add(str(int(nm[:4]))); continue
    if not os.path.exists(bak+nm): shutil.copy(dst,bak+nm)
    shutil.copy(f,dst); ed.add(str(int(nm[:4]))); n+=1
open('edited_units.txt','w').write(' '.join(sorted(ed,key=int)))
print('deployed',n,'total edited',len(ed))
