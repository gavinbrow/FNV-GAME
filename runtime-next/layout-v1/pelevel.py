import sys; sys.path.insert(0,'.')
from common import *
import json, collections
pe=PE(); D=pe.d; TV=0x401000; TE=TV+12441088
o=pe.off(pe.base+0xd0147c)
tls=struct.unpack_from('<6I',D,o); print('TLS dir',[hex(x) for x in tls])
cb=tls[3]; cbs=[]
oo=pe.off(cb)
while oo is not None:
    v=struct.unpack_from('<I',D,oo)[0]
    if v==0: break
    cbs.append(v); oo+=4
print('callbacks',[hex(x) for x in cbs], 'sec',pe.sec_of(cb))
print('entry',hex(pe.base+pe.entry),pe.sec_of(pe.base+pe.entry))
# bind section dwords into text
for nm,va,vs,rp,rs in pe.secs:
    if nm=='.bind':
        a=np.frombuffer(D,np.uint32,count=rs//4,offset=rp).astype(np.int64)
        m=(a>=TV)&(a<TE); print('.bind dwords in text range',int(m.sum()))
        rel=set(pe.relocs()); print('.bind relocs',sum(1 for x in rel if pe.sec_of(x)=='.bind'))
# debug dir
o=pe.off(pe.base+0xc11410); dbg=struct.unpack_from('<IIHHIIII',D,o); print('debug',dbg)
# any reloc entry in .rsrc/.tls/CONST/.reloc?
print(collections.Counter(pe.sec_of(x) for x in pe.relocs()))
# TLS template / IAT: does IAT/import thunk call sites exist - count text refs to IAT (data) irrelevant
# exports none: dd[0]
print('exports',pe.dd[0],'load cfg',pe.dd[10],'exception',pe.dd[3],'delay',pe.dd[13])
