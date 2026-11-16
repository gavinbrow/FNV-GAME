import sys, json, re, struct, collections; sys.dont_write_bytecode=True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
import numpy as np
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\pinned-build'); sys.argv=['x']
import uncovered_v2 as U
pe=U.pe; t=bytes(U.text)
def cstr(va):
    try: b=pe.read(va,48)
    except Exception: return None
    s=b.split(b'\0')[0]
    return s.decode('latin1') if len(s)>=4 and all(32<=c<127 for c in s) else None
# symbol map name lookup for call targets
def name_at(a): return sorted(U.symaddr.get(a,[]))[:1]
for va,L in [(0xf79710,28715),(0xfda000,11238),(0xefd5a0,3982),(0xfdcc30,4388),(0xf4fa60,2929),(0xee6e60,4988),(0x9fea2a,2314),(0xfb8060,1662),(0xfbce30,1937),(0xfddef0,1792)]:
    s=va-U.TEXT_VA; b=t[s:s+L]
    strs=[]; tg=collections.Counter()
    for m in re.finditer(rb'\x68(....)',b,re.S):
        v=struct.unpack('<I',m.group(1))[0]
        if 0x1000000<=v<0x1200000 or 0x10f0000<=v: 
            x=cstr(v)
            if x: strs.append(x)
    for m in re.finditer(rb'\xe8(....)',b,re.S):
        r=struct.unpack('<i',m.group(1))[0]; tg[va+m.start()+5+r]+=1
    tops=[('0x%x'%a,n,name_at(a)) for a,n in tg.most_common(4)]
    # absolute SEH handler pushes: 6a ff 68 imm
    seh=[hex(struct.unpack('<I',b[m.end():m.end()+4])[0]) for m in re.finditer(rb'\x6a\xff\x68',b)][:3]
    print(hex(va),L,'strs',strs[:5],'topcalls',tops,'seh',seh)
# zlib
for key in (b'invalid block type',b'incorrect header check',b'1.2.1',b'inflate 1.'):
    i=pe.data.find(key); print(key,i)
