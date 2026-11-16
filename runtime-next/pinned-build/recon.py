import sys, json, hashlib, struct, collections
sys.path.insert(0,r'C:\Projects\Decompilation\fnv_decomp\tools')
sys.path.insert(0,r'C:\Projects\Decompilation\fnv_decomp\tools')
from pathlib import Path
IMG=Path(r'C:\Projects\Decompilation\FNV\work\worker1\FalloutNV.runtime-text.exe')
INST=Path(r'C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\FalloutNV.exe')
for p in (IMG,INST):
    d=p.read_bytes()
    print(p,len(d),hashlib.sha256(d).hexdigest())
    pe=struct.unpack_from('<I',d,0x3c)[0]
    m,n,ts,_,_,osz,ch=struct.unpack_from('<HHIIIHH',d,pe+4)
    o=pe+24
    print(' ts',hex(ts),'chars',hex(ch),'RELOCS_STRIPPED',bool(ch&1),'base',hex(struct.unpack_from('<I',d,o+28)[0]),'entry',hex(struct.unpack_from('<I',d,o+16)[0]),'imagesize',hex(struct.unpack_from('<I',d,o+56)[0]),'hdrsize',hex(struct.unpack_from('<I',d,o+60)[0]))
    dd=o+96
    for i in range(16):
        rva,sz=struct.unpack_from('<II',d,dd+i*8)
        if rva or sz: print('  dd',i,hex(rva),hex(sz))
    for i in range(n):
        nm,vs,rva,rs,raw,_,_,_,_,fl=struct.unpack_from('<8sIIIIIIHHI',d,o+osz+i*40)
        print('  ',nm.rstrip(b'\0').decode(),hex(rva),hex(vs),hex(rs),hex(raw),hex(fl))
a=IMG.read_bytes(); b=INST.read_bytes()
diff=sum(1 for x,y in zip(a,b) if x!=y); print('img vs installed differing bytes',diff)
