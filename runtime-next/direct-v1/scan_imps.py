import struct,glob,sys,json
def imps(path):
    d=open(path,'rb').read()
    if struct.unpack_from('<H',d,0)[0]!=0x14c: return set()
    ptr,n=struct.unpack_from('<II',d,8); st=ptr+18*n
    out=set(); i=0
    while i<n:
        o=ptr+18*i; nm=d[o:o+8]
        if nm[:4]==b'\0\0\0\0': name=d[st+struct.unpack('<I',nm[4:])[0]:].split(b'\0')[0]
        else: name=nm.rstrip(b'\0')
        sec,=struct.unpack_from('<h',d,o+12); sc,na=d[o+16],d[o+17]
        if name.startswith(b'__imp_') and sec==0 and sc==2: out.add(name.decode())
        i+=1+na
    return out
if __name__=='__main__':
    allp=set()
    for dirn in sys.argv[1:]:
        for f in glob.glob(dirn+'/*.obj'): allp|=imps(f)
    print(len(allp)); json.dump(sorted(allp),open('objs_imps.json','w'))
