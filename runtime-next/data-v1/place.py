"""data-v1 place.py: dedupe the data sections of our objects, split unit-level .rdata/.data sections at symbol boundaries, place every piece in the
reference .rdata/.data and resolve its relocation fields. Placement tiers (a piece takes the first that applies):
  B  bytes with relocation fields masked: exactly one aligned hit in the reference .rdata/.data/.tls/CONST (independent of every map)
  V  bytes + the relocation values OUR resolution produced: exactly one hit (placement independent of the reference's pointer values)
  H  no unique hit; the symbol maps (units.json symbols / recipe names / build-v7 code records) give an address and the masked bytes verify there
  L  link: the address is read from a pointer field (in the reference) of an already placed piece that points at this piece; masked bytes verify
Writes a scratch pickle for report.py."""
import sys, os, json, struct, collections, pickle, gzip, hashlib, re, time
sys.dont_write_bytecode = True
sys.path.append((__import__('os').environ.get('FNV_PY_SITE', __import__('os').path.expandvars(r'%APPDATA%\Python\Python312\site-packages'))))
from pathlib import Path
HERE = Path(__file__).resolve().parent
RN = HERE.parent
REF = Path((__import__('os').environ.get('FNV_REF_IMAGE', r'C:\Projects\Decompilation\FNV\work\worker1\FalloutNV.runtime-text.exe')))
M32 = 0xffffffff
t0 = time.time()
ref = REF.read_bytes()
peo = struct.unpack_from('<I', ref, 0x3c)[0]; ns = struct.unpack_from('<H', ref, peo + 6)[0]; osz = struct.unpack_from('<H', ref, peo + 20)[0]
BASE = struct.unpack_from('<I', ref, peo + 24 + 28)[0]
SECS = {}
for i in range(ns):
    o = peo + 24 + osz + 40 * i; nm = ref[o:o + 8].rstrip(b'\0').decode()
    vs, va, rs, rp = struct.unpack_from('<IIII', ref, o + 8); SECS[nm] = (BASE + va, vs, rp, rs)
REG = [(n, SECS[n][0], SECS[n][2], SECS[n][3], SECS[n][1]) for n in ('.rdata', '.data', '.tls', 'CONST')]
RB = {n: ref[ro:ro + rs] for n, va, ro, rs, vs in REG}
def refread(va, n=4):
    for nm, rva, ro, rs, vs in REG:
        if rva <= va and va + n <= rva + rs: return ref[ro + va - rva: ro + va - rva + n]
    return None
def region_of(va):
    for nm, rva, ro, rs, vs in REG:
        if rva <= va < rva + vs: return nm
# names resolved by build-v7 code records (agree only, names are cut at 80 chars in that log): extra name -> address source
v7names = collections.defaultdict(set)
for l in gzip.open(RN / 'build-v7' / 'relocs_v7.tsv.gz', 'rt'):
    f = l.rstrip('\n').split('\t')
    if f[3] == 'agree' and f[5] and f[1] == 'DIR32' and len(f[6]) < 80: v7names[f[6]].add(int(f[5], 16))
v7map = {k: next(iter(v)) for k, v in v7names.items() if len(v) == 1}
FIELD = {6: 4, 7: 4, 0x14: 4, 0x0B: 4, 0x0A: 2}

def algn(s): a = (s['flags'] >> 20) & 0xf; return 1 << (a - 1) if a else 1
def fieldvals(s, resolved):
    L = len(s['data']); pat = bytearray(s['data']); kn = bytearray(b'\1' * L)
    for r in s['relocs']:
        off, kind = r[0], r[1]; n = FIELD.get(kind, 4)
        for q in range(off, min(off + n, L)): kn[q] = 0
        v = resolved.get(off)
        if v is not None and kind == 6 and off + 4 <= L:
            pat[off:off + 4] = struct.pack('<I', v & M32); kn[off:off + 4] = b'\1\1\1\1'
        elif v is not None and kind == 7 and off + 4 <= L:
            pat[off:off + 4] = struct.pack('<I', (v - BASE) & M32); kn[off:off + 4] = b'\1\1\1\1'
    return pat, kn
def runs_of(pat, kn):
    out = []; i = 0; L = len(pat)
    while i < L:
        if kn[i]:
            j = i
            while j < L and kn[j]: j += 1
            out.append((i, bytes(pat[i:j]))); i = j
        else: i += 1
    return out
def search(s, resolved, cap=300):
    pat, kn = fieldvals(s, resolved); runs = runs_of(pat, kn); L = len(pat)
    if not runs: return None, 0
    bo, bb = max(runs, key=lambda r: (len(set(r[1])), len(r[1])))
    i0 = next((i for i, c in enumerate(bb) if c), 0); i0 = max(0, i0 - 2)
    key = bb[i0:i0 + 16]; ko = bo + i0; al = algn(s); hits = []
    for nm, rva, ro, rs, vs in REG:
        blob = RB[nm]; p = blob.find(key)
        while p >= 0:
            st = p - ko
            if st >= 0 and st + L <= len(blob) and (rva + st) % al == 0 and all(blob[st + o:st + o + len(b)] == b for o, b in runs):
                hits.append(rva + st)
                if len(hits) > cap: return hits, 1
            p = blob.find(key, p + 1)
    return hits, 0
def verify_at(s, resolved, va):
    pat, kn = fieldvals(s, resolved); L = len(pat)
    b = refread(va, L)
    if b is None: return False
    return all(b[o:o + len(x)] == x for o, x in runs_of(pat, kn))
def unmasked(s): return sum(len(b) for o, b in runs_of(*fieldvals(s, {})))

class State:
    def __init__(self): self.SEC = {}; self.KEYOF = {}; self.PIECES = {}; self.placed = {}; self.gdef = {}; self.info = {}
    def tkey(self, u, tsec, point):
        pcs = self.PIECES.get((u, tsec))
        if pcs is None:
            k = self.KEYOF.get((u, tsec)); return (k, 0) if k else (None, 0)
        for a, b, k in pcs:
            if a <= point < b: return k, a
        return (pcs[-1][2], pcs[-1][0]) if pcs and point == pcs[-1][1] else (None, 0)
    def rebuild_gdef(self):
        c = collections.defaultdict(set)
        for k, (a, t) in self.placed.items():
            s = self.SEC[k]
            for d in s['defs']:
                if d[2] == 2: c[d[0]].add(a + d[1])
        self.gdef = {n: next(iter(v)) for n, v in c.items() if len(v) == 1}
    def resolve(self, s):
        res = {}; src = {}; u = s['units'][0]
        for r in s['relocs']:
            off, kind, nm, tsec, tval, tstor, addend, rsrc, rexp = r
            if rsrc is not None: res[off] = rexp; src[off] = rsrc; continue
            if addend is None: continue
            if tsec > 0:
                k, a0 = self.tkey(u, tsec, tval + addend)
                if k in self.placed: res[off] = (self.placed[k][0] + (tval + addend) - a0) & M32; src[off] = 'placed-section'
            elif nm in self.gdef: res[off] = (self.gdef[nm] + addend) & M32; src[off] = 'placed-extern'
            elif nm in v7map: res[off] = (v7map[nm] + addend) & M32; src[off] = 'v7-record-name'
        return res, src

def kind_of(s):
    nm = s['name']; ds = [d[0] for d in s['defs']]
    if nm.startswith('.bss'): return 'bss'
    if nm.startswith('.tls'): return 'tls'
    if nm.startswith('.CRT'): return 'crt-init-array'
    if nm.startswith('.xdata'): return 'eh-tables'
    for d in ds:
        if d.startswith('??_7'): return 'vtable'
    for d in ds:
        for n in '01234':
            if d.startswith('??_R' + n): return 'rtti' + n
    for d in ds:
        if d.startswith('??_C@') or d.startswith('$SG'): return 'string'
        if d.startswith('__real@') or d.startswith('__xmm@'): return 'float-const'
    if nm.startswith('.rdata'): return 'rdata-other' + ('' if s['flags'] & 0x1000 else '-unit')
    if nm.startswith('.data'): return 'data' + ('' if s['flags'] & 0x1000 else '-unit')
    return 'other'

def build_state(p0path):
    P0 = pickle.load(open(p0path, 'rb'))['res']
    if os.environ.get('DV_LIB', '1') == '1':   # wB data-v2: CRT/STL library members' data sections as pseudo-units (id 100000+)
        sys.path.insert(0, str(RN / 'data-v2')); import libsecs; P0.update(libsecs.lib_units())
    st = State()
    def keyof(s):
        comdat = bool(s['flags'] & 0x1000)
        base = (s['name'], s['flags'] & 0xf00000f0, s['size'], s['data'], tuple((r[0], r[1], r[2], r[3] > 0) for r in s['relocs']))
        if comdat and s['defs']: return ('c', base, tuple(sorted(d[0] for d in s['defs'] if d[2] == 2)))
        return ('u', s['u'], s['k'])
    nsec = 0
    for u, r in P0.items():
        for s in r['secs']:
            nsec += 1
            if s['name'].startswith('.bss'): s['kind'] = 'bss'
            else: s['kind'] = kind_of(s)
            k = keyof(s); st.KEYOF[(u, s['k'])] = k
            e = st.SEC.get(k)
            sym_val = {d[0]: d[1] for d in s['defs']}
            if e is None:
                s['units'] = [u]; s['hint'] = collections.defaultdict(set); s['hint_sym'] = [(a, via, nm, sym_val.get(nm)) for a, via, nm in s['hints']]
                for a, via, nm in s['hints']: s['hint'][a].add(via)
                for d in s['defs']:
                    if d[0] in v7map and d[2] == 2: s['hint'][(v7map[d[0]] - d[1]) & M32].add('v7-record'); s['hint_sym'].append(((v7map[d[0]] - d[1]) & M32, 'v7-record', d[0], d[1]))
                st.SEC[k] = s
            else:
                e['units'].append(u)
                for a, via, nm in s['hints']: e['hint'][a].add(via)
    # split non-COMDAT unit sections of strings / plain data at symbol boundaries
    nsplit = 0
    for k in list(st.SEC):
        s = st.SEC[k]
        if k[0] != 'u' or s['kind'] not in ('string', 'rdata-other-unit', 'data-unit') or s['size'] == 0: continue
        cuts = sorted({0, s['size']} | {d[1] for d in s['defs'] if 0 < d[1] < s['size']})
        if len(cuts) <= 2: continue
        u = s['units'][0]; pcs = []
        del st.SEC[k]
        for a, b in zip(cuts, cuts[1:]):
            pk = ('p', u, s['k'], a)
            rel = [(r[0] - a,) + tuple(r[1:]) for r in s['relocs'] if a <= r[0] < b]
            ps = dict(u=u, k=s['k'], name=s['name'], flags=s['flags'], data=s['data'][a:b], size=b - a, relocs=rel,
                      defs=[(d[0], d[1] - a, d[2]) for d in s['defs'] if a <= d[1] < b], units=[u], start=a)
            ps['hint'] = collections.defaultdict(set)
            for ba, via, nm, v in s['hint_sym']:
                if v is not None and a <= v < b: ps['hint'][(ba + a) & M32].add(via)
            ps['hint_sym'] = []; ps['hints'] = []
            ps['kind'] = kind_of(ps) if any(d[0].startswith(('??_', '__real', '$SG')) for d in ps['defs']) else ('rdata-other-unit' if s['name'].startswith('.rdata') else 'data-unit')
            if s['kind'] == 'string' and ps['defs'] and all(d[0].startswith('$SG') for d in ps['defs']): ps['kind'] = 'string'
            st.SEC[pk] = ps; pcs.append((a, b, pk)); nsplit += 1
        st.PIECES[(u, s['k'])] = pcs
    print('sections', nsec, 'unique pieces', len(st.SEC), 'from split', nsplit, round(time.time() - t0), 's', flush=True)
    return st

def run(st):
    SEC, placed, info = st.SEC, st.placed, st.info
    todo = [k for k, s in SEC.items() if s['kind'] != 'bss' and s['size'] > 0]
    H1 = {}; RLEN = {}
    def place(k, a, t): placed[k] = (a, t)
    def round_(allow_hint, allow_link):
        newp = 0; st.rebuild_gdef()
        for k in todo:
            if k in placed: continue
            s = SEC[k]
            if k not in H1: H1[k] = search(s, {}); info[k] = dict(nB=(None if H1[k][0] is None else (-1 if H1[k][1] else len(H1[k][0]))))
            hits1, cap1 = H1[k]
            if hits1 is not None and not cap1 and len(hits1) == 1: place(k, hits1[0], 'B'); newp += 1; continue
            res, src = st.resolve(s)
            if res and len(res) > RLEN.get(k, 0):
                RLEN[k] = len(res)
                hits2, cap2 = search(s, res)
                if hits2 is not None and not cap2 and len(hits2) == 1: place(k, hits2[0], 'V'); newp += 1; continue
            if allow_hint and s['hint']:
                ok = [a for a in s['hint'] if verify_at(s, {}, a)]
                if len(ok) > 1: ok = [x for x in ok if verify_at(s, res, x)]
                if len(ok) == 1: place(k, ok[0], 'H'); newp += 1
        if allow_link:
            cand = collections.defaultdict(set)
            for k, (A, t) in list(placed.items()):
                s = SEC[k]; u = s['units'][0]; L = len(s['data'])
                for r in s['relocs']:
                    off, kind, nm, tsec, tval, tstor, addend, rsrc, rexp = r
                    if kind != 6 or tsec <= 0 or addend is None or off + 4 > L: continue
                    tk, a0 = st.tkey(u, tsec, tval + addend)
                    if tk is None or tk in placed or tk not in SEC or SEC[tk]['kind'] == 'bss': continue
                    b = refread(A + off, 4)
                    if not b: continue
                    rv, = struct.unpack('<I', b)
                    cand[tk].add((rv - (tval + addend - a0)) & M32)
            for tk, cs in cand.items():
                if len(cs) != 1: continue
                a = next(iter(cs)); ts = SEC[tk]
                if refread(a, len(ts['data'])) is None or a % algn(ts): continue
                if unmasked(ts) >= 4 and verify_at(ts, {}, a): place(tk, a, 'L'); newp += 1
        return newp
    for phase in range(8):
        for rnd in range(1, 9):
            n = round_(False, False); print('phase', phase, 'round', rnd, 'placed', n, 'total', len(placed), round(time.time() - t0), 's', flush=True)
            if n == 0: break
        n = round_(True, False); print(' hint round placed', n, 'total', len(placed), flush=True)
        n2 = round_(False, True); print(' link round placed', n2, 'total', len(placed), flush=True)
        if n == 0 and n2 == 0: break
    # ---- wB data-v2 tier O (duplicate-content ordering rule): pieces whose masked bytes are identical form a group; the reference has h aligned hits for the group.
    # The group's pieces, in owning-unit address order (link order), take the free hits in ascending address order (min(n, h) of them). Pieces of one group have identical
    # masked bytes, so which piece sits on which hit changes no produced byte except the pointer fields, which are counted only where our resolved value equals the reference.
    if os.environ.get('DV_ORDER', '1') == '1':
        import numpy as _np
        occ = {nm: _np.zeros(rs, _np.uint8) for nm, rva, ro, rs, vs in REG}
        def mark(a, L):
            for nm, rva, ro, rs, vs in REG:
                if rva <= a < rva + rs: occ[nm][a - rva:a - rva + L] = 1; return
        for k, (a, t_) in placed.items(): mark(a, len(SEC[k]['data']))
        ufirst = {}
        try:
            _un = json.loads((Path((__import__('os').environ.get('FNV_PROJ_ROOT', 'C:\\Projects\\Decompilation').replace('\\', '/') + '/fnv_decomp')) / 'build/units.json').read_text())['units']
            for i, u in enumerate(_un): ufirst[i] = min((int(f['address'], 16) for f in u['functions']), default=0)
        except Exception: pass
        groups = collections.defaultdict(list)
        for k in todo:
            if k in placed: continue
            s = SEC[k]
            pat, kn = fieldvals(s, {})
            if sum(1 for b, m in zip(pat, kn) if m and b) < 8: continue
            groups[(s['kind'], bytes(pat), bytes(kn), algn(s))].append(k)
        nO = 0; bO = 0; hitcap = int(os.environ.get('DV_ORDER_CAP', '20000'))
        for sig, ks in groups.items():
            ks.sort(key=lambda k: (ufirst.get(SEC[k]['units'][0], 10 ** 9 + SEC[k]['units'][0]), str(k)))
            hits, cap = search(SEC[ks[0]], {}, cap=hitcap)
            if not hits or cap: continue
            L = len(SEC[ks[0]]['data'])
            free = [h for h in sorted(hits) if not any(occ[nm][h - rva:h - rva + L].any() for nm, rva, ro, rs, vs in REG if rva <= h < rva + rs)]
            for k, h in zip(ks, free):
                place(k, h, 'O'); mark(h, L); nO += 1; bO += L
        print('tier O (ordering rule): pieces', nO, 'bytes', bO, 'groups', len(groups), flush=True)
    st.rebuild_gdef()
    print(collections.Counter(t for a, t in placed.values()))

if __name__ == '__main__':
    sys.path.insert(0, str(HERE))
    import place as PLM
    st = PLM.build_state(sys.argv[1])
    PLM.run(st)
    pickle.dump(st, open(sys.argv[2], 'wb'))
