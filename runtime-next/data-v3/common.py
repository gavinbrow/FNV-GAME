"""data-v3 common: reference image, sections, original .reloc fields in data sections, recipe function map."""
import bisect
import collections
import json
import re
import struct
import sys

sys.dont_write_bytecode = True
sys.path.append((__import__('os').environ.get('FNV_PY_SITE', r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')))
RN = (__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\Projects\Decompilation') + r'\runtime-next')
REF = (__import__('os').environ.get('FNV_REF_IMAGE', r'C:\Projects\Decompilation\FNV\work\worker1\FalloutNV.runtime-text.exe'))
ref = open(REF, 'rb').read()
peo = struct.unpack_from('<I', ref, 0x3c)[0]
nsec = struct.unpack_from('<H', ref, peo + 6)[0]
osz = struct.unpack_from('<H', ref, peo + 20)[0]
BASE = struct.unpack_from('<I', ref, peo + 24 + 28)[0]
IMGSZ = struct.unpack_from('<I', ref, peo + 24 + 56)[0]
SEC = {}
for _i in range(nsec):
    _o = peo + 24 + osz + 40 * _i
    _n = ref[_o:_o + 8].rstrip(b'\0').decode()
    _vs, _va, _rs, _rp = struct.unpack_from('<IIII', ref, _o + 8)
    SEC[_n] = dict(va=BASE + _va, vs=_vs, raw=_rs, off=_rp)
DATA_SECS = ['.rdata', '.data', '.tls', 'CONST']
TEXT = SEC['.text']
TLO, THI = TEXT['va'], TEXT['va'] + TEXT['vs']
IMG_LO, IMG_HI = BASE, BASE + IMGSZ


def sec_of(va):
    for n in ('.text', '.rdata', '.data', '.tls', 'CONST', '.rsrc', '.reloc', '.bind'):
        s = SEC.get(n)
        if s and s['va'] <= va < s['va'] + max(s['vs'], s['raw']):
            return n
    return None


def read_ref(va, n=4):
    for nm in DATA_SECS + ['.text']:
        s = SEC[nm]
        if s['va'] <= va and va + n <= s['va'] + s['raw']:
            o = s['off'] + va - s['va']
            return ref[o:o + n]
    return None


def orig_reloc_sites():
    rrva, rsz = struct.unpack_from('<II', ref, peo + 24 + 96 + 5 * 8)
    r = SEC['.reloc']
    p = r['off'] + (rrva - (r['va'] - BASE)); end = p + rsz; out = set()
    while p < end:
        pg, bs = struct.unpack_from('<II', ref, p)
        if bs == 0: break
        for k in range((bs - 8) // 2):
            w, = struct.unpack_from('<H', ref, p + 8 + 2 * k)
            if w >> 12 == 3: out.add(BASE + pg + (w & 0xfff))
        p += bs
    return out


def load_units():
    return json.loads(open((__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\Projects\Decompilation') + r'\fnv_decomp\build\units.json')).read())['units']
