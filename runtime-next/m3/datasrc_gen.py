r"""Batch 10 step B: one-shot generator of the data source (m3/datasrc/*.cpp + index.json).  MAY read the reference image (through gen_m3 / data-v3 common); the build
(FNV_M3_DATASRC=1) never does.  usage: FNV_M3_SEL=batch9s2_selection.json python -I datasrc_gen.py [--out datasrc]

Every selected global becomes a typed C++ definition with literal values:
  * non-W entries (scalars, arrays, tables, records) and the named (DAT_ / namespaced) W globals keep the definitions gen_m3.cpp() renders (files obj0000/obj0001);
  * every other W object is carved into MSVC RTTI objects (TypeDescriptor, CompleteObjectLocator, ClassHierarchyDescriptor, BaseClassArray, BaseClassDescriptor, named from the
    decorated class name), vtables (found through the COL pointer at vtable[-1]) with function-symbol entries, strings, wide strings, floats/doubles, pointer tables, zero blocks
    and opaque dword/byte arrays.  Everything is extern "C" with a real name; pointers to our own objects name them, pointers to code name the function.
index.json: one record per object (address, size, section, name, object file, expected relocation sites -> target VAs, hash of the non-pointer bytes); it drives placement
and the build-time self-check (no reference bytes)."""
import os, sys, re, json, struct, hashlib, bisect, collections
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ.setdefault('FNV_M3_SEL', 'batch9s2_selection.json')
OUT = os.path.join(HERE, 'datasrc')
if '--out' in sys.argv: OUT = os.path.abspath(sys.argv[sys.argv.index('--out') + 1])
import gen_m3 as G
from gen_m3 import fmt, cstr, ORIG_SET, ORIG_SITES, TLO, THI
_MV = memoryview(G.ref)
def refbytes(va, sz):      # gen_m3.refbytes copies the rest of the image per call
    n = G.sec_of(va); o = G.SEC[n]['off'] + va - G.SEC[n]['va']; return bytes(_MV[o:o + sz])
G.refbytes = refbytes
PROJ = G.PROJ

sel = json.load(open(G.SELF))['entries']
entries = G.build_entries(sel)
for e in entries:
    if e['tc'] in ('T', 'X'): G.set_fields(e)

# ---------------------------------------------------------------------------------------------------------------------------------- helpers
def u32(va): return struct.unpack('<I', refbytes(va, 4))[0]
def site(a): return a in ORIG_SET
def ident(s):
    s = re.sub(r'[^A-Za-z0-9_]', '_', s); s = re.sub(r'_+', '_', s).strip('_')
    return s or 'x'
def cls_name(td_name):
    """decorated type name '.?AVFoo@@' -> 'Foo' (nested '.?AVBar@Foo@@' -> 'Foo_Bar', templates sanitised)"""
    s = td_name.decode('latin1')
    m = re.match(r'^\.\?A(?:W4|[VUT])?', s)
    s = s[m.end():] if m else s
    s = s.rstrip('@')
    parts = [p for p in s.split('@') if p]
    return ident('_'.join(reversed(parts)))

FNAMES = {}
try:
    sys.path.insert(0, os.path.join(PROJ, 'fnv_decomp', 'tools'))
    import function_names_data as FND
    cnt = collections.Counter(n for a, n, ev in FND.N)
    for a, n, ev in FND.N:
        if cnt[n] == 1 and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', n) and not n.startswith(('FUN_', 'DAT_', 'M3')): FNAMES[int(a, 16)] = n
except Exception as ex:
    print('function names unavailable:', ex)

# readable (undecorated) source symbols of the functions: units.json symbols, then function_names_data.py where the source name is a FUN_ placeholder
READ = {}
def _undecorate(sym):
    if re.search(r'FUN_[0-9a-f]{8}', sym) or not sym.startswith('?'): return None
    m = re.match(r'^\?(\?[0-9A-Z]|)([^@?]+)@((?:[^@?]+@)*)@', sym)
    if sym.startswith('??0') or sym.startswith('??1'):
        m2 = re.match(r'^\?\?([01])([^@]+)@@', sym)
        return None if not m2 else ('%s::%s%s' % (m2.group(2), '~' if m2.group(1) == '1' else '', m2.group(2)))
    m = re.match(r'^\?([^@?]+)@([^@?]+(?:@[^@?]+)*)?@', sym)
    if not m: return None
    name = m.group(1); cls = [c for c in (m.group(2) or '').split('@') if c]
    return '::'.join(list(reversed(cls)) + [name]) if cls else name
try:
    for u in json.load(open(os.path.join(PROJ, 'fnv_decomp', 'build', 'units.json')))['units']:
        for f in u['functions']:
            r = _undecorate(f['symbol'])
            if r: READ[int(f['address'], 16)] = r
    n_units = len(READ)
    for a, n, ev in FND.N:
        READ.setdefault(int(a, 16), n)
    print('readable function names:', len(READ), '(units.json %d)' % n_units)
except Exception as ex:
    print('readable names unavailable:', ex)
def cm(tv):
    r = READ.get(tv) if TLO <= tv < THI else None
    return ' /* %s */' % r.replace('*/', '* /') if r else ''
CMT = collections.Counter()

# ---------------------------------------------------------------------------------------------------------------------------------- split the entries
nonw = [e for e in entries if e['tc'] != 'W']
named = [e for e in entries if e['tc'] == 'W' and (e.get('named') or e.get('ns') or e['section'] not in ('.rdata', '.data'))]
free = sorted((e for e in entries if e['tc'] == 'W' and e not in named), key=lambda e: e['va'])
fstarts = [e['va'] for e in free]; fends = [e['va'] + e['size'] for e in free]
def ent_of(a):
    j = bisect.bisect_right(fstarts, a) - 1
    return j if j >= 0 and a < fends[j] else None
taken = {j: bytearray(e['size']) for j, e in enumerate(free)}
items = []          # carved fixed items (va, size, kind, info)
def can(a, n):
    j = ent_of(a)
    if j is None or a + n > fends[j]: return False
    o = a - fstarts[j]; return not any(taken[j][o:o + n])
def take(a, nbytes, kind, **info):
    j = ent_of(a); o = a - fstarts[j]; taken[j][o:o + nbytes] = b'\1' * nbytes; items.append(dict(va=a, size=nbytes, kind=kind, **info))
def cstring(a, maxn=4096):
    j = ent_of(a); lim = fends[j]; out = bytearray(); p = a
    while p < lim and p - a < maxn:
        b = refbytes(p, 1)[0]
        if b == 0: return bytes(out)
        out.append(b); p += 1
    return None

# ---- RTTI recognition
tds = {}
for j, e in enumerate(free):
    raw = refbytes(e['va'], e['size']); i = raw.find(b'.?A')
    while i >= 0:
        a = e['va'] + i - 8
        if i >= 8 and site(a) and raw[i - 4:i] == b'\0\0\0\0' and a % 4 == 0:
            nm = cstring(a + 8)
            if nm is not None:
                n = len(nm) + 1; n += (-n) % 4
                if can(a, 8 + n) and all(x == 0 for x in refbytes(a + 8 + len(nm), n - len(nm))): tds[a] = (nm, 8 + n)
        i = raw.find(b'.?A', i + 1)
for a, (nm, sz) in tds.items(): take(a, sz, 'td', nm=nm)
cols = {}
for j, e in enumerate(free):
    for a in range(e['va'], e['va'] + e['size'] - 19, 4):
        if site(a + 12) and site(a + 16) and u32(a) in (0, 1) and u32(a + 12) in tds and can(a, 20):
            cols[a] = (u32(a + 4), u32(a + 8), u32(a + 12), u32(a + 16))
for a in cols:
    if can(a, 20): take(a, 20, 'col')
chds = {}
for a, (off, cd, td, ch) in cols.items():
    if ch not in chds and ent_of(ch) is not None and site(ch + 12) and u32(ch) == 0 and 0 < u32(ch + 8) <= 512 and can(ch, 16):
        chds[ch] = (u32(ch + 4), u32(ch + 8), u32(ch + 12)); take(ch, 16, 'chd')
bcas = {}
for ch, (attr, nb, bca) in chds.items():
    if bca not in bcas and ent_of(bca) is not None and all(site(bca + 4 * k) for k in range(nb)) and can(bca, 4 * nb):
        bcas[bca] = [u32(bca + 4 * k) for k in range(nb)]; take(bca, 4 * nb, 'bca')
bcds = {}
for bca, lst in bcas.items():
    for d in lst:
        if d in bcds or ent_of(d) is None: continue
        if site(d) and u32(d) in tds:
            sz = 28 if site(d + 24) else 24
            if can(d, sz): bcds[d] = sz; take(d, sz, 'bcd', size28=(sz == 28))
# ---- vtables via the COL pointer at vtable[-1]
colset = set(cols); vtabs = {}; VSTAT = collections.Counter()
for j, e in enumerate(free):
    for a in range(e['va'], e['va'] + e['size'] - 7, 4):
        if site(a) and u32(a) in colset:
            VSTAT['cell'] += 1
            if not can(a, 4): VSTAT['cant-meta'] += 1; continue
            n = 0
            while a + 8 + 4 * n <= fends[j] and site(a + 4 + 4 * n) and TLO <= u32(a + 4 + 4 * n) < THI and can(a + 4 + 4 * n, 4): n += 1
            if n == 0: VSTAT['n0'] += 1; continue
            take(a, 4, 'vmeta', col=u32(a)); take(a + 4, 4 * n, 'vtbl', col=u32(a), n=n); vtabs[a + 4] = u32(a)

print('vtable stats', dict(VSTAT), 'cols', len(cols), 'tds', len(tds))
# ---- names
used = set();
def uniq(base, va):
    nm = base
    if nm in used: nm = '%s_%08x' % (base, va)
    used.add(nm); return nm
cname_of_td = {a: cls_name(nm) for a, (nm, sz) in tds.items()}
name_of = {}
for a, (nm, sz) in sorted(tds.items()): name_of[a] = uniq('RTTI_TD_' + cname_of_td[a], a)
col_cls = {}
for a, (off, cd, td, ch) in sorted(cols.items()):
    c = cname_of_td[td]; col_cls[a] = c
    name_of[a] = uniq('RTTI_COL_' + c + ('_at_%d' % off if off else ''), a)
chd_cls = {}
for ch, (attr, nb, bca) in sorted(chds.items()):
    first = bcas.get(bca, [None])[0]
    c = cname_of_td.get(u32(first), None) if first in bcds else None
    if c is None: c = next((col_cls[a] for a, v in cols.items() if v[3] == ch), 'x%08x' % ch)
    chd_cls[ch] = c; name_of[ch] = uniq('RTTI_CHD_' + c, ch)
    if bca in bcas: name_of[bca] = uniq('RTTI_BCA_' + c, bca)
for d, sz in sorted(bcds.items()): name_of[d] = uniq('RTTI_BCD_' + cname_of_td[u32(d)], d)
for v, col in sorted(vtabs.items()):
    c = col_cls[col]; off = cols[col][0]
    name_of[v] = uniq('vtbl_' + c + ('_at_%d' % off if off else ''), v); name_of[v - 4] = name_of[v] + '_meta'; used.add(name_of[v - 4])

# ---- gap objects
segs = []        # dict(va,size,section,name,kind,align,fb,decl,init(fn texpr)->text, ptrs=[sites])
def sec_of(va): return G.sec_of(va)
def ro(sec): return sec == '.rdata'
def add_seg(va, size, kind, name, decl, init, fb=False):
    segs.append(dict(va=va, size=size, section=sec_of(va), kind=kind, name=name, decl=decl, init=init, fb=fb))
def cterm(sec): return 'const ' if ro(sec) else ''

def commas(cells, cms):
    out = []
    for i, (c, k) in enumerate(zip(cells, cms)):
        out.append(c + (',' if i + 1 < len(cells) else '') + k + (chr(10) if k else ' '))
        if k: CMT['commented'] += 1
    return ''.join(out)
RUNKIND = {'P': 'ptrtab', 'U': 'opaque', 'B': 'opaque', 'M': 'float', 'N': 'double', 'S': 'string', 'Z': 'zero'}

def gap_objects(va, raw):
    """carve one untaken span into typed objects"""
    n = len(raw); wides = []
    for m in re.finditer(rb'(?:[\x20-\x7e]\x00){4,}\x00\x00', raw):
        s0 = m.start()
        if (va + s0) % 2 == 0 and not G._site_in(va + s0, va + m.end()): wides.append((s0, m.end()))
    pos = 0
    for w0, w1 in wides + [(n, n)]:
        if w0 > pos: laid(va + pos, raw[pos:w0])
        if w1 > w0: wide_obj(va + w0, raw[w0:w1])
        pos = w1

def wide_obj(va, raw):
    sec = sec_of(va); chars = raw[:-2].decode('utf-16-le')
    name = uniq('wstr_%08x' % va, va)
    add_seg(va, len(raw), 'wstring', name, '%swchar_t %s[%d]' % (cterm(sec), name, len(raw) // 2), lambda tx, chars=chars: wide_lit(chars))

def wide_lit(chars):
    parts = []; cur = ''
    for ch in chars:
        c = ord(ch)
        if ch in '"\\': cur += '\\' + ch
        elif 0x20 <= c < 0x7f and ch != '?': cur += ch
        else: cur += '\\x%04x' % c; parts.append('L"%s"' % cur); cur = ''; continue
        if len(cur) > 70: parts.append('L"%s"' % cur); cur = ''
    if cur or not parts: parts.append('L"%s"' % cur)
    return ' '.join(parts)

def find_records(va, raw):
    """batch 11: arrays of records found by period detection over the relocation pattern of an aligned span: period p dwords (2..16), >= 3 rows, at least one pointer
    column and one non-pointer column.  Returns [(first dword, p, rows)]."""
    n = len(raw)
    if va % 4 or n % 4 or n < 24: return []
    nd = n // 4
    for k in range(nd):
        if any((va + 4 * k + d) in ORIG_SET for d in (1, 2, 3)): return []      # a site not on a dword boundary: leave the span to the run layout
    sit = [1 if (va + 4 * k) in ORIG_SET else 0 for k in range(nd)]
    if not any(sit) or all(sit): return []
    RUNL = {}
    for p in range(2, 17):
        if 3 * p > nd: break
        r = [0] * (nd + 1)
        for j in range(nd - p - 1, -1, -1): r[j] = r[j + 1] + 1 if sit[j] == sit[j + p] else 0
        RUNL[p] = r
    out = []; i = 0
    while i < nd:
        best = None
        for p, r in RUNL.items():
            if i + 3 * p > nd: continue
            rows = (r[i] + p) // p
            if rows >= 3 and 0 < sum(sit[i:i + p]) < p:
                cov = rows * p
                if best is None or cov > best[0]: best = (cov, p, rows)
        if best: out.append((i, best[1], best[2])); i += best[0]
        else: i += 1
    return out

def _fl_range(v, lo=1e-4, hi=1e6):
    f = struct.unpack('<f', struct.pack('<I', v))[0]
    return f == f and lo <= abs(f) <= hi
def _int_ok(v): return v <= 0xffff or v >= 0xffff0000 or v in (0x7fffffff, 0x80000000)
def rec_col_class(vals):
    """class of a non-pointer record column: 'I' small ints, 'F' floats, 'U' other dwords"""
    if all(_int_ok(v) for v in vals): return 'I'
    nz = [v for v in vals if v]
    if nz and all(_fl_range(v, 1e-6, 1e9) for v in nz) and sum(1 for v in nz if G._plaus_f(struct.pack('<I', v))) * 2 >= len(nz): return 'F'
    return 'U'

def rec_obj(va, raw, p, rows):
    nm = 'rec_%08x' % va; tname = nm + '_t'
    cls = []
    for c in range(p):
        vals = [struct.unpack_from('<I', raw, 4 * (r * p + c))[0] for r in range(rows)]
        cls.append('P' if (va + 4 * c) in ORIG_SET else rec_col_class(vals))
    cty = {'P': 'void*', 'I': 'int', 'F': 'float', 'U': 'unsigned'}
    pre = 'struct %s { %s };' % (tname, ' '.join('%s f%d;' % (cty[k], c) for c, k in enumerate(cls)))
    sec = sec_of(va); name = uniq(nm, va)
    def init(tx, va=va, raw=raw, p=p, rows=rows, cls=cls):
        out = []
        for r in range(rows):
            cells = []
            for c in range(p):
                o = 4 * (r * p + c); w = raw[o:o + 4]; k = cls[c]
                cells.append(tx(struct.unpack('<I', w)[0]) if k == 'P' else fmt('H', w) if k == 'I' else fmt('M', w) if k == 'F' else fmt('I', w))
            out.append('{' + ', '.join(cells) + '}')
        return '{' + chr(10) + (',' + chr(10)).join(out) + '}'
    segs.append(dict(va=va, size=len(raw), section=sec, kind='record', name=name, decl='%s%s %s[%d]' % (cterm(sec), tname, name, rows), init=init, fb=False, pre=pre))

def laid(va, raw):
    recs = find_records(va, raw)
    if recs:
        pos = 0
        for i0, p, rows in recs:
            if i0 * 4 > pos: laid_runs(va + pos, raw[pos:i0 * 4])
            rec_obj(va + 4 * i0, raw[4 * i0:4 * (i0 + p * rows)], p, rows); pos = 4 * (i0 + p * rows)
        if pos < len(raw): laid_runs(va + pos, raw[pos:])
        return
    laid_runs(va, raw)

def laid_runs(va, raw):
    runs = G.layout(va, raw, None, []); groups = []; p = 0
    for cls, cnt in runs:
        nb = cnt * G.RUN_SZ[cls]; k = {'P': 'P', 'U': 'O', 'B': 'O', 'M': 'M', 'N': 'N', 'S': 'S', 'Z': 'Z'}[cls]
        if groups and groups[-1][0] == k and k in ('O', 'P', 'M', 'N'): groups[-1][2] = p + nb
        else: groups.append([k, p, p + nb])
        p += nb
    for k, p0, p1 in groups: one_obj(k, va + p0, raw[p0:p1])

def retype(va, raw):
    """batch 11: re-type an opaque span (no guessing at meaning: only the stride/representation that reproduces the bytes) -> True when an object was added"""
    n = len(raw); sec = sec_of(va); ct = cterm(sec)
    if not any(raw): one_obj('Z', va, raw); return True
    if va % 4 == 0 and n % 4 == 0:
        vals = [struct.unpack_from('<I', raw, i)[0] for i in range(0, n, 4)]; m = len(vals)
        if all(_int_ok(v) for v in vals):
            name = uniq('int_%08x' % va, va)
            add_seg(va, n, 'int', name, '%sint %s[%d]' % (ct, name, m), lambda tx, raw=raw, m=m: '{%s}' % ', '.join(fmt('H', raw[4 * i:4 * i + 4]) for i in range(m))); return True
        nz = [v for v in vals if v]
        if all(G._plaus_f(struct.pack('<I', v)) for v in nz):
            name = uniq('flt_%08x' % va, va)
            add_seg(va, n, 'float', name, '%sfloat %s[%d]' % (ct, name, m), lambda tx, raw=raw, m=m: '{%s}' % ', '.join(fmt('M', raw[4 * i:4 * i + 4]) for i in range(m))); return True
        if va % 8 == 0 and n % 8 == 0 and n >= 16:
            ds = [struct.unpack_from('<d', raw, i)[0] for i in range(0, n, 8)]
            if all(d == 0 or (d == d and 1e-9 <= abs(d) <= 1e12) for d in ds) and sum(1 for d in ds if d) * 2 >= len(ds):
                name = uniq('dbl_%08x' % va, va); m8 = n // 8
                add_seg(va, n, 'double', name, '%sdouble %s[%d]' % (ct, name, m8), lambda tx, raw=raw, m8=m8: '{%s}' % ', '.join(fmt('N', raw[8 * i:8 * i + 8]) for i in range(m8))); return True
        if len(nz) >= 1 and all(_fl_range(v) for v in nz) and (len(nz) >= 4 or n == 4):
            name = uniq('flt_%08x' % va, va)
            add_seg(va, n, 'float', name, '%sfloat %s[%d]' % (ct, name, m), lambda tx, raw=raw, m=m: '{%s}' % ', '.join(fmt('M', raw[4 * i:4 * i + 4]) for i in range(m))); return True
    if va % 2 == 0 and n % 2 == 0 and n >= 4:
        hs = struct.unpack('<%dH' % (n // 2), raw)
        if all(h < 0x1000 for h in hs):
            name = uniq('shorts_%08x' % va, va)
            add_seg(va, n, 'short', name, '%sunsigned short %s[%d]' % (ct, name, n // 2), lambda tx, hs=hs: '{%s}' % ', '.join('%d' % h for h in hs)); return True
    return False

def one_obj(k, va, raw):
    sec = sec_of(va); n = len(raw); ct = cterm(sec); allzero = not any(raw)
    if k == 'S':
        name = uniq('str_%08x' % va, va)
        add_seg(va, n, 'string', name, '%schar %s[%d]' % (ct, name, n), lambda tx, raw=raw: cstr(raw[:-1]) if raw[-1] == 0 else None)
    elif k == 'M':
        name = uniq('flt_%08x' % va, va); m = n // 4
        add_seg(va, n, 'float', name, '%sfloat %s[%d]' % (ct, name, m), lambda tx, raw=raw, m=m: '{%s}' % ', '.join(fmt('M', raw[4 * i:4 * i + 4]) for i in range(m)))
    elif k == 'N':
        name = uniq('dbl_%08x' % va, va); m = n // 8
        add_seg(va, n, 'double', name, '%sdouble %s[%d]' % (ct, name, m), lambda tx, raw=raw, m=m: '{%s}' % ', '.join(fmt('N', raw[8 * i:8 * i + 8]) for i in range(m)))
    elif k == 'Z':
        name = uniq('zero_%08x' % va, va)
        add_seg(va, n, 'zero', name, '%sunsigned char %s[%d]' % (ct, name, n), lambda tx: '{0}', fb=not ro(sec))
    elif k == 'P':
        name = uniq('ptrs_%08x' % va, va); m = n // 4
        def init(tx, va=va, m=m):
            cells = []
            for i in range(m):
                a = va + 4 * i
                cells.append(tx(u32(a)) if site(a) else ('0' if u32(a) == 0 else '(void*)0x%08x' % u32(a)))
            return '{' + commas(cells, [cm(u32(va + 4 * i)) if site(va + 4 * i) else '' for i in range(m)]) + '}'
        add_seg(va, n, 'ptrtab', name, ('void* %s[%d]' if not ro(sec) else 'void* const %s[%d]') % (name, m), init, fb=allzero and not ro(sec))
    elif retype(va, raw): pass
    else:
        name = uniq('dat_%08x' % va, va)
        if n % 4 == 0 and va % 4 == 0:
            add_seg(va, n, 'opaque', name, '%sunsigned %s[%d]' % (ct, name, n // 4), lambda tx, raw=raw: '{%s}' % ', '.join('0x%08xu' % struct.unpack('<I', raw[i:i + 4])[0] for i in range(0, len(raw), 4)), fb=allzero and not ro(sec))
        else:
            add_seg(va, n, 'opaque', name, '%sunsigned char %s[%d]' % (ct, name, n), lambda tx, raw=raw: '{%s}' % ', '.join(str(b) for b in raw), fb=allzero and not ro(sec))

# ---- fixed items -> segments
def dw(a): return u32(a)
for it in sorted(items, key=lambda x: x['va']):
    va, sz, k = it['va'], it['size'], it['kind']; sec = sec_of(va); ct = cterm(sec)
    if k == 'td':
        nm = it['nm']; name = name_of[va]
        add_seg(va, sz, 'rtti-td', name, '%sRTTI_TypeDescriptor<%d> %s' % (ct, sz - 8, name), lambda tx, va=va, nm=nm: '{%s, 0, %s}' % (tx(u32(va)), cstr(nm)))
    elif k == 'col':
        name = name_of[va]
        add_seg(va, sz, 'rtti-col', name, '%sRTTI_CompleteObjectLocator %s' % (ct, name), lambda tx, va=va: '{%d, %d, %d, %s, %s}' % (u32(va), u32(va + 4), u32(va + 8), tx(u32(va + 12)), tx(u32(va + 16))))
    elif k == 'chd':
        name = name_of[va]
        add_seg(va, sz, 'rtti-chd', name, '%sRTTI_ClassHierarchyDescriptor %s' % (ct, name), lambda tx, va=va: '{%d, 0x%08xu, %d, %s}' % (u32(va), u32(va + 4), u32(va + 8), tx(u32(va + 12))))
    elif k == 'bca':
        name = name_of[va]; n = sz // 4
        add_seg(va, sz, 'rtti-bca', name, '%sconst void* %s[%d]' % ('const ' if False else '', name, n) if not ro(sec) else 'const void* const %s[%d]' % (name, n), lambda tx, va=va, n=n: '{%s}' % ', '.join(tx(u32(va + 4 * i)) for i in range(n)))
    elif k == 'bcd':
        name = name_of[va]
        if it['size28']:
            add_seg(va, sz, 'rtti-bcd', name, '%sRTTI_BaseClassDescriptor %s' % (ct, name), lambda tx, va=va: '{%s, %d, %d, %d, %d, 0x%08xu, %s}' % (tx(u32(va)), u32(va + 4), struct.unpack('<i', refbytes(va + 8, 4))[0], struct.unpack('<i', refbytes(va + 12, 4))[0], struct.unpack('<i', refbytes(va + 16, 4))[0], u32(va + 20), tx(u32(va + 24))))
        else:
            add_seg(va, sz, 'rtti-bcd', name, '%sRTTI_BaseClassDescriptor24 %s' % (ct, name), lambda tx, va=va: '{%s, %d, %d, %d, %d, 0x%08xu}' % (tx(u32(va)), u32(va + 4), struct.unpack('<i', refbytes(va + 8, 4))[0], struct.unpack('<i', refbytes(va + 12, 4))[0], struct.unpack('<i', refbytes(va + 16, 4))[0], u32(va + 20)))
    elif k == 'vmeta':
        name = name_of[va]
        add_seg(va, sz, 'vtable-meta', name, '%svoid* %s' % ('const ' if False else '', name) if not ro(sec) else 'void* const %s' % name, lambda tx, va=va: tx(u32(va)))
    elif k == 'vtbl':
        name = name_of[va]; n = it['n']
        add_seg(va, sz, 'vtable', name, 'vfunc_t %s[%d]' % (name, n) if not ro(sec) else 'const vfunc_t %s[%d]' % (name, n), lambda tx, va=va, n=n: '{' + commas([tx(u32(va + 4 * i), True) for i in range(n)], [cm(u32(va + 4 * i)) for i in range(n)]) + '}')
# ---- the gaps
for j, e in enumerate(free):
    t = taken[j]; i = 0; raw_all = refbytes(e['va'], e['size'])
    while i < e['size']:
        if t[i]: i += 1; continue
        k = i
        while k < e['size'] and not t[k]: k += 1
        gap_objects(e['va'] + i, raw_all[i:k]); i = k
segs.sort(key=lambda s: s['va'])
# sanity: the objects of the free W entries tile them exactly
cov = sum(s['size'] for s in segs); assert cov == sum(e['size'] for e in free), (cov, sum(e['size'] for e in free))
assert len({s['name'] for s in segs}) == len(segs)
sstarts = [s['va'] for s in segs]
for a, b in zip(segs, segs[1:]): assert a['va'] + a['size'] <= b['va']

# ---- batch 11: names from cross-references.  An object whose every .text reference (relocation sites of the build, build-v7/relocs_v7.tsv.gz) lies in ONE function is named
# after that function (the readable source name when known, else FUN_<va>); several users or none: the kind+address name stays.
XPFX = {'string': 'str', 'wstring': 'wstr', 'float': 'flt', 'double': 'dbl', 'zero': 'zero', 'ptrtab': 'ptrs', 'opaque': 'dat', 'record': 'rec', 'int': 'int', 'short': 'shorts'}
XSTAT = collections.Counter()
def rename_seg(sg, new):
    old = sg['name']; used.discard(old); sg['name'] = uniq(new, sg['va'])
    sg['decl'] = re.sub(r'(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])' % re.escape(old), sg['name'], sg['decl'], count=1)
if not os.environ.get('DS_NO_XREF'):
    import gzip
    FNS = []
    for u in json.load(open(os.path.join(PROJ, 'fnv_decomp', 'build', 'units.json')))['units']:
        for f in u['functions']: FNS.append((int(f['address'], 16), f['size']))
    FNS.sort(); fst = [a for a, z in FNS]
    xr = collections.defaultdict(set)
    with gzip.open(os.path.join(PROJ, 'runtime-next', 'build-v7', 'relocs_v7.tsv.gz'), 'rt') as fh:
        next(fh)
        for l in fh:
            q = l.rstrip(chr(10)).split(chr(9))
            if len(q) < 6 or not q[5]: continue
            t = int(q[5], 16); j = bisect.bisect_right(sstarts, t) - 1
            if j < 0 or t >= segs[j]['va'] + segs[j]['size']: continue
            fv = int(q[0], 16); k = bisect.bisect_right(fst, fv) - 1
            xr[j].add(FNS[k][0] if k >= 0 and fv < FNS[k][0] + FNS[k][1] else None)     # None: a field outside every unit function (several such users never name an object)
    bykey = collections.defaultdict(list)
    for j, sg in enumerate(segs):
        if sg['kind'] not in XPFX: continue
        u = xr.get(j)
        if not u: XSTAT['no code reference'] += 1; continue
        if len(u) != 1 or None in u: XSTAT['several users / outside functions'] += 1; continue
        f = next(iter(u)); bykey[(XPFX[sg['kind']], f)].append(j)
    for (pf, f), js in bykey.items():
        base = ident(READ.get(f) or 'FUN_%08x' % f)[:60]
        for n_, j in enumerate(sorted(js, key=lambda j: segs[j]['va'])):
            rename_seg(segs[j], '%s_%s%s' % (pf, base, '_%d' % (n_ + 1) if len(js) > 1 else '')); XSTAT['named from the single user'] += 1
    # second level: an object that no code references but exactly one other (already named) object points at takes that object's name + its kind prefix + an index
    GENERIC = re.compile(r'^(str|ptrs|dat|flt|zero|dbl|wstr|rec|int|shorts)_[0-9a-f]{8}$')
    dref = collections.defaultdict(set)
    for j, sg in enumerate(segs):
        for a in range(sg['va'], sg['va'] + sg['size'] - 3):
            if a in ORIG_SET:
                t = u32(a); k = bisect.bisect_right(sstarts, t) - 1
                if k >= 0 and k != j and t < segs[k]['va'] + segs[k]['size']: dref[k].add(j)
    changed = True; rounds = 0
    while changed:
        changed = False; rounds += 1; kids = collections.defaultdict(list)
        for k, sg in enumerate(segs):
            if sg['kind'] not in XPFX or not GENERIC.match(sg['name']) or xr.get(k): continue
            d = dref.get(k)
            if d and len(d) == 1:
                r = next(iter(d))
                if segs[r]['kind'] in ('rtti-td', 'rtti-col', 'rtti-chd', 'rtti-bca', 'rtti-bcd', 'vtable', 'vtable-meta') or not GENERIC.match(segs[r]['name']): kids[r].append(k)
        for r, ks in kids.items():
            cnt = collections.Counter()
            for k in sorted(ks, key=lambda k: segs[k]['va']):
                pf = XPFX[segs[k]['kind']]; cnt[pf] += 1
                total = sum(1 for k2 in ks if XPFX[segs[k2]['kind']] == pf)
                rename_seg(segs[k], '%s_%s%s' % (pf, segs[r]['name'], '_%d' % cnt[pf] if total > 1 else '')); XSTAT['named from the single referring object'] += 1; changed = True
    assert len({s_['name'] for s_ in segs}) == len(segs)
    print('xref naming:', dict(XSTAT), 'rounds', rounds)

# ---------------------------------------------------------------------------------------------------------------------------------- render
PRELUDE = """// Batch 10 datasrc (datasrc_gen.py): typed definitions with literal values.  Do not edit.
typedef void (*vfunc_t)(void);
template<int N> struct RTTI_TypeDescriptor { const void* pVFTable; void* spare; char name[N]; };
struct RTTI_CompleteObjectLocator { unsigned signature; unsigned offset; unsigned cdOffset; const void* pTypeDescriptor; const void* pClassDescriptor; };
struct RTTI_ClassHierarchyDescriptor { unsigned signature; unsigned attributes; unsigned numBaseClasses; const void* pBaseClassArray; };
struct RTTI_BaseClassDescriptor { const void* pTypeDescriptor; unsigned numContainedBases; int mdisp; int pdisp; int vdisp; unsigned attributes; const void* pClassDescriptor; };
struct RTTI_BaseClassDescriptor24 { const void* pTypeDescriptor; unsigned numContainedBases; int mdisp; int pdisp; int vdisp; unsigned attributes; };
#pragma section(".data", read, write)
"""
def fname(tv): return FNAMES.get(tv) or 'FUN_%08x' % tv

class TU:
    def __init__(self): self.segs = []; self.nrel = 0
def render_tu(k, tseg):
    mine = {s['name'] for s in tseg}; fns = set(); m3d = {}; foreign = {}
    def tx(tv, fnptr=False):
        if TLO <= tv < THI:
            nm = fname(tv); fns.add(nm); return nm if fnptr else '(void*)&%s' % nm
        j = bisect.bisect_right(sstarts, tv) - 1
        if j >= 0 and segs[j]['va'] <= tv < segs[j]['va'] + segs[j]['size']:
            s = segs[j]; nm = s['name']
            if nm not in mine: foreign[nm] = 1
            off = tv - s['va']
            return '(void*)&%s' % nm if off == 0 else '(void*)((char*)&%s + %d)' % (nm, off)
        m3d[tv] = 1; return '(void*)&M3D_%08x' % tv
    defs = []
    for s in tseg:
        body = s['init'](tx)
        pre = '__declspec(allocate(".data")) ' if s['fb'] else ''
        defs.append('extern %s%s = %s;' % (pre, s['decl'], body))
    L = [PRELUDE] + [s['pre'] for s in tseg if s.get('pre')] + ['extern "C" {']
    L += ['void %s(void);' % f for f in sorted(fns)]
    L += ['char M3D_%08x;' % v for v in sorted(m3d)]
    L += ['extern char %s;' % f for f in sorted(foreign)]
    L += ['extern %s;' % s['decl'] for s in tseg]
    return '\n'.join(L + defs + ['}']) + '\n'

def split_tus(sg, max_e=2500, max_r=30000):
    out = []; cur = []; nr = 0
    for s in sg:
        r = sum(1 for i in range(s['size'] // 4 + 1) if False)
        r = sum(1 for a in range(s['va'], s['va'] + s['size'] - 3) if a in ORIG_SET)
        if cur and (len(cur) >= max_e or nr + r > max_r or cur[0]['section'] != s['section']): out.append(cur); cur = []; nr = 0
        cur.append(s); nr += r
    if cur: out.append(cur)
    return out

os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith('.cpp') or f == 'index.json': os.remove(os.path.join(OUT, f))
index = []; files = []
def rec(e_va, size, section, name, tc, kind, obj, align, fb, mode):
    sites = [a - e_va for a in range(e_va, e_va + size - 3) if a in ORIG_SET]
    raw = bytearray(refbytes(e_va, size))
    for o in sites: raw[o:o + 4] = b'\0\0\0\0'
    relocs = [[o, u32(e_va + o)] for o in sites]
    d = dict(va=e_va, size=size, section=section, name=name, tc=tc, kind=kind, obj=obj, relocs=relocs, h=hashlib.sha256(bytes(raw)).hexdigest(), mode=mode)
    if align: d['align'] = align
    if fb: d['file_backed'] = True
    index.append(d)
# file 0: non-W (exactly as gen_m3 renders them); file 1: named W globals
for k, grp in ((0, nonw), (1, named)):
    if not grp: continue
    txt = G.cpp(grp); fn = 'obj%04d_%s.cpp' % (k, 'scalars' if k == 0 else 'named'); open(os.path.join(OUT, fn), 'w', newline='\n').write(txt); files.append([k, fn])
    for e in grp:
        rec(e['va'], e['size'], e['section'], e['name'], e['tc'], e.get('kind', 'ptr' if e.get('ptr') else 'scalar'), k, e.get('align'), bool(e.get('file_backed')), 'cpp')
k = 2
for tseg in split_tus(segs):
    fn = 'obj%04d_%s_%08x.cpp' % (k, tseg[0]['section'].lstrip('.'), tseg[0]['va']); open(os.path.join(OUT, fn), 'w', newline='\n').write(render_tu(k, tseg)); files.append([k, fn])
    for s in tseg: rec(s['va'], s['size'], s['section'], s['name'], 'W', s['kind'], k, 4 if s['va'] % 4 == 0 else 1, s['fb'], 'c')
    k += 1
index.sort(key=lambda d: d['va'])
# externs: function symbol -> VA
ext = {}
for tv in list({u32(a) for e in index for a in [e['va'] + r[0] for r in e['relocs']]}):
    if TLO <= tv < THI: ext[fname(tv)] = tv
json.dump(dict(version=1, selection=os.path.basename(G.SELF), files=files, objs=list(range(k)), externs=ext, entries=index), open(os.path.join(OUT, 'index.json'), 'w'), indent=0)
kb = collections.defaultdict(lambda: [0, 0])
for d in index: kb[d['kind']][0] += 1; kb[d['kind']][1] += d['size']
print('code entries with a readable name comment:', CMT['commented'])
print('objects', len(index), 'files', len(files), 'bytes', sum(d['size'] for d in index))
for kk, (c, b) in sorted(kb.items(), key=lambda x: -x[1][1]): print('  %-34s %7d %9d' % (kk, c, b))
if os.environ.get('DS_DEBUG'):
    c = 0
    for a in sorted(vtabs):
        j = ent_of(a)
        print(hex(a), 'ent', hex(fstarts[j]), fends[j] - fstarts[j], [(site(a + 4 * i), hex(u32(a + 4 * i)), taken[j][a - fstarts[j] + 4 * i]) for i in range(0, 6) if a + 4 * i < fends[j]])
        c += 1
        if c > 8: break
