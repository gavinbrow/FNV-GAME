import sys, struct, gzip, json
sys.dont_write_bytecode = True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
import numpy as np
REF = r'C:\Projects\Decompilation\FNV\work\worker1\FalloutNV.runtime-text.exe'
RN = r'C:\Projects\Decompilation\runtime-next'
class PE:
    def __init__(s, path=REF):
        d = s.d = open(path, 'rb').read()
        pe = struct.unpack_from('<I', d, 0x3c)[0]
        ns = struct.unpack_from('<H', d, pe + 6)[0]; osz = struct.unpack_from('<H', d, pe + 20)[0]
        o = pe + 24
        s.base = struct.unpack_from('<I', d, o + 28)[0]; s.entry = struct.unpack_from('<I', d, o + 16)[0]
        s.dd = [struct.unpack_from('<II', d, o + 96 + 8 * i) for i in range(16)]
        s.secs = []
        so = o + osz
        for i in range(ns):
            nm = d[so:so + 8].rstrip(b'\0').decode(); vs, va, rs, rp = struct.unpack_from('<IIII', d, so + 8)
            s.secs.append((nm, va, vs, rp, rs)); so += 40
    def sec_of(s, va):
        r = va - s.base
        for nm, v, vs, rp, rs in s.secs:
            if v <= r < v + max(vs, rs): return nm
        return None
    def off(s, va):
        r = va - s.base
        for nm, v, vs, rp, rs in s.secs:
            if v <= r < v + rs: return rp + r - v
        return None
    def relocs(s):
        va, sz = s.dd[5]; out = []
        if not va: return out
        off = s.off(s.base + va); end = off + sz
        while off < end:
            pg, bs = struct.unpack_from('<II', s.d, off)
            if bs == 0: break
            for i in range((bs - 8) // 2):
                e = struct.unpack_from('<H', s.d, off + 8 + 2 * i)[0]
                if e >> 12 == 3: out.append(s.base + pg + (e & 0xfff))
            off += bs
        return out
