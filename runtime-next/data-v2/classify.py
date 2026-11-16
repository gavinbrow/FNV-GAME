r"""data-v2 classify.py: structural classification of the reference .rdata/.data bytes that data-v1 does NOT produce (non-zero, outside import dir/IAT).
Read-only: reads the reference image, data-v1's strict image (produced bytes) and build-v7's relocs. Writes classify.json (+ prints tables).
Categories (first rule that claims a byte wins): rtti typedesc, rtti COL / hierarchy / base array / base class descriptors, vtable (+ plain code-pointer tables),
EH tables (FuncInfo, unwind map, try map, handler arrays, ip-to-state map), wide/ascii strings, code-referenced constants (<=8 B scalars, bigger tables), rest."""
import bisect
import collections
import gzip
import json
import re
import struct
import sys

sys.dont_write_bytecode = True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
import numpy as np

RN = r'C:\Projects\Decompilation\runtime-next'
REF = r'C:\Projects\Decompilation\FNV\work\worker1\FalloutNV.runtime-text.exe'
ref = open(REF, 'rb').read()
stb = open(RN + r'\data-v1\FalloutNV_data_strict.exe', 'rb').read()
peo = struct.unpack_from('<I', ref, 0x3c)[0]; ns = struct.unpack_from('<H', ref, peo + 6)[0]; osz = struct.unpack_from('<H', ref, peo + 20)[0]
BASE = struct.unpack_from('<I', ref, peo + 24 + 28)[0]
S = {}
for i in range(ns):
    o = peo + 24 + osz + 40 * i; nm = ref[o:o + 8].rstrip(b'\0').decode()
    vs, va, rs, rp = struct.unpack_from('<IIII', ref, o + 8); S[nm] = (BASE + va, vs, rp, rs)
TLO, TSZ = S['.text'][0], S['.text'][1]
imp_rva, imp_sz = struct.unpack_from('<II', ref, peo + 24 + 96 + 1 * 8)
iat_rva, iat_sz = struct.unpack_from('<II', ref, peo + 24 + 96 + 12 * 8)
skip = [(BASE + imp_rva, imp_sz), (BASE + iat_rva, iat_sz)]
units = json.load(open(r'C:\Projects\Decompilation\fnv_decomp\build\units.json'))['units']
fr = sorted((int(f['address'], 16), int(f['address'], 16) + f['size'], i) for i, u in enumerate(units) for f in u['functions'])
fk = [x[0] for x in fr]
def unit_of(va):
    j = bisect.bisect_right(fk, va) - 1
    return fr[j][2] if j >= 0 and fr[j][0] <= va < fr[j][1] else None
# code references into data: field target -> set of units
refs = collections.defaultdict(set)
for l in gzip.open(RN + r'\build-v7\relocs_v7.tsv.gz', 'rt'):
    f = l.split('\t')
    if f[1] != 'DIR32' or not f[5]: continue
    t = int(f[5], 16)
    if S['.rdata'][0] <= t < S['.data'][0] + S['.data'][1]:
        u = unit_of(int(f[0], 16))
        refs[t].add(u if u is not None else -1)
rk = sorted(refs)
res = {}
total = collections.Counter(); owned = collections.Counter(); ownedunits = collections.defaultdict(collections.Counter)
for rn in ('.rdata', '.data'):
    va0, vs, ro, rs = S[rn]
    R = np.frombuffer(ref, np.uint8, rs, ro); T = np.frombuffer(stb, np.uint8, rs, ro)
    U = (R != 0) & (T == 0)
    for a, n in skip:
        if va0 <= a < va0 + rs: U[a - va0:a - va0 + n] = False
    res[rn + '_unproduced_nonzero'] = int(U.sum())
    cat = np.full(rs, '', dtype=object); own = {}
    def claim(a, n, c, owner=None):
        a = max(a, 0); b = min(a + n, rs)
        for i in range(a, b):
            if cat[i] == '': cat[i] = c
        if owner is not None: own[a] = owner
    D = bytes(R); dw = lambda o: struct.unpack_from('<I', D, o)[0] if 0 <= o <= rs - 4 else None
    inrd = lambda v: v is not None and S['.rdata'][0] <= v < S['.rdata'][0] + S['.rdata'][3]
    intext = lambda v: v is not None and TLO <= v < TLO + TSZ
    off = lambda v: v - va0
    # 1. type descriptors: '.?A' names
    for m in re.finditer(rb'\.\?A[UVW][\x20-\x7e]+?\x00', D):
        s = m.start(); claim(s - 8, 8 + (m.end() - s), 'rtti: type descriptor (name keeps original class name)')
    # 2. vtables with COL
    i = 0
    vt_unit = {}
    while i + 8 <= rs:
        v = dw(i)
        if intext(v) and intext(dw(i + 4)):
            j = i
            while j + 4 <= rs and intext(dw(j)): j += 4
            colp = dw(i - 4) if i >= 4 else None
            if colp is not None and inrd(colp) and rn == '.rdata' and dw(off(colp)) == 0:
                claim(i - 4, 4, 'rtti: COL pointer (vtable[-1])')
                co = off(colp); claim(co, 20, 'rtti: complete object locator')
                hp = dw(co + 16)
                if inrd(hp):
                    ho = off(hp); claim(ho, 16, 'rtti: class hierarchy descriptor'); nb = dw(ho + 8); ba = dw(ho + 12)
                    if nb is not None and 0 < nb < 64 and inrd(ba):
                        claim(off(ba), 4 * nb, 'rtti: base class array')
                        for k in range(nb):
                            b = dw(off(ba) + 4 * k)
                            if inrd(b): claim(off(b), 28, 'rtti: base class descriptor')
                kind = 'vtable (with RTTI)'
            else: kind = 'code-pointer table (no RTTI: vtable, callback/dispatch tables)'
            claim(i, j - i, kind)
            u = unit_of(v) if kind.startswith('vtable') else None
            for k in range(i, j, 4):
                u = unit_of(dw(k))
                if u is not None: break
            vt_unit[i] = (u, j, kind)
            i = j
        else: i += 4
    # 3. EH tables
    for m in re.finditer(rb'[\x20\x21\x22]\x05\x93\x19', D):
        o = m.start()
        if o % 4: continue
        n = 36 if D[o] in (0x21, 0x22) else 28
        claim(o, n, 'EH: FuncInfo')
        ms, pu, nt, pt, ni, pip = dw(o + 4), dw(o + 8), dw(o + 12), dw(o + 16), dw(o + 20), dw(o + 24)
        if ms is not None and ms < 4096 and inrd(pu): claim(off(pu), 8 * ms, 'EH: unwind map')
        if ni is not None and ni < 4096 and inrd(pip): claim(off(pip), 8 * ni, 'EH: ip-to-state map')
        if nt is not None and nt < 256 and inrd(pt):
            claim(off(pt), 20 * nt, 'EH: try-block map')
            for k in range(nt):
                nc, ph = dw(off(pt) + 20 * k + 12), dw(off(pt) + 20 * k + 16)
                if nc is not None and nc < 64 and inrd(ph): claim(off(ph), 20 * nc, 'EH: catch handler types')
    # 4. strings
    for m in re.finditer(rb'(?:[\x20-\x7e\t\r\n]{3,})\x00', D): claim(m.start(), m.end() - m.start(), 'strings: ASCII')
    for m in re.finditer(rb'(?:[\x20-\x7e]\x00){3,}\x00\x00', D): claim(m.start(), m.end() - m.start(), 'strings: UTF-16')
    # 5. code-referenced remainder / other
    cl = [t - va0 for t in rk if va0 <= t < va0 + rs]
    for o in cl:
        if o < rs and cat[o] == '' and U[o]:
            j = o
            nxt = bisect.bisect_right(cl, o)
            lim = cl[nxt] if nxt < len(cl) else rs
            while j < lim and j < rs and cat[j] == '': j += 1
            n = j - o
            claim(o, n, 'code-referenced data <=8 B (float/double/int constants)' if n <= 8 else ('code-referenced data 9-64 B (small constant tables, float4, structs)' if n <= 64 else 'code-referenced data >64 B (lookup tables, static structs/arrays)'))
    cat[(cat == '') & U] = 'other (not code-referenced; data-referenced structs, arrays, padding patterns)'
    # tally
    for i in np.flatnonzero(U):
        c = cat[i]; total[(rn, c)] += 1
    # ownership of bytes: strings/consts via first code reference; vtables via function unit
    for t, us in refs.items():
        if va0 <= t < va0 + rs and U[t - va0]:
            c = cat[t - va0]
            n = 0; j = t - va0
            while j < rs and U[j] and cat[j] == c: j += 1
            n = j - (t - va0)
            ks = {u for u in us if u is not None and u >= 0}
            owned[(rn, c, 'owned by recipe unit' if ks else 'referenced only from code outside the recipe')] += n
    for st, (u, en, kd) in vt_unit.items():
        n = int(U[st:en].sum())
        if n: owned[(rn, kd, 'owned by recipe unit' if u is not None else 'no recipe function in slots')] += n
out = collections.defaultdict(dict)
for (rn, c), n in sorted(total.items(), key=lambda x: -x[1]): out[rn][c] = n
own = collections.defaultdict(dict)
for (rn, c, w), n in owned.items(): own[rn + '|' + c][w] = n
json.dump(dict(totals=res, by_category=out, ownership=own), open(RN + r'\data-v2\classify.json', 'w'), indent=1)
for rn in out:
    print(rn, res[rn + '_unproduced_nonzero'], sum(out[rn].values()))
    for c, n in out[rn].items(): print('  %9d  %s' % (n, c))
