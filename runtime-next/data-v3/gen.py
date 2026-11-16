r"""data-v3 gen.py: symbolic description of .rdata/.data/.tls/CONST (+ .data's bss tail) as MASM source plus symbolic.json.
Reference-derived inputs: (1) the reference image bytes (typed literals), (2) the original .reloc (pointer fields), (3) a value-based rule for pointer-sized fields without base reloc.
Outputs (data-v3\out): rdata.asm, data.asm, tls.asm, const.asm, symbolic.json (compact), code_symbols.json.
usage: python -I gen.py"""
import bisect
import collections
import json
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

OUT = os.environ.get('DV3_OUT') or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
os.makedirs(OUT, exist_ok=True)
units = load_units()
orel = orig_reloc_sites()
drel = {v for v in orel if sec_of(v) in DATA_SECS}
# ---------------------------------------------------------------- code symbols
fn = []                      # (start, end, name)
names = collections.defaultdict(set)
for u in units:
    for f in u['functions']:
        a = int(f['address'], 16); fn.append((a, a + f['size'], f['symbol'])); names[f['symbol']].add(a)
fn.sort(key=lambda x: (x[0], x[1]))
starts = {}
for a, e, nm in fn:
    starts.setdefault(a, nm)
fn_by_start = sorted(starts)
fn_end = {}
for a, e, nm in fn:
    fn_end[a] = max(fn_end.get(a, 0), e)
pieces = set()
for u in units:
    for t in u.get('eh_tails', []):
        pieces.add(int(t['address'], 16))
try:
    for p in json.load(open(RN + r'\build-v7\contrib_pieces.json'))['pieces']: pieces.add(p['address'])
except Exception:
    pass
SYM_OK = re.compile(r'^[A-Za-z_$@?][A-Za-z0-9_$@?]*$')
def code_symbol(va):
    """-> (symbol, addend, kind)"""
    j = bisect.bisect_right(fn_by_start, va) - 1
    if j >= 0:
        a = fn_by_start[j]
        if a <= va < fn_end[a]:
            nm = starts[a]
            if len(names[nm]) == 1 and SYM_OK.match(nm) and len(nm) < 200 and os.environ.get('DV3_CNAMES') != '1':
                return nm, va - a, 'function'
            return 'C_%08x' % a, va - a, 'function(addr-named)'
    return 'C_%08x' % va, 0, ('piece' if va in pieces else 'other-code')
# ---------------------------------------------------------------- pointer fields
K = set(starts) | pieces
data_targets = set()
for f in drel:
    v = struct.unpack('<I', read_ref(f))[0]
    if sec_of(v) in DATA_SECS or (SEC['.data']['va'] + SEC['.data']['raw'] <= v < SEC['.data']['va'] + SEC['.data']['vs']):
        data_targets.add(v)
K |= data_targets
fields = {}      # va -> (target, evidence)
for f in drel:
    fields[f] = (struct.unpack('<I', read_ref(f))[0], 'orig-reloc')
n_extra = 0; extra_lit = 0
for nm in DATA_SECS:
    s = SEC[nm]; blob = ref[s['off']:s['off'] + s['raw']]
    for o in range(0, len(blob) - 3, 4):
        va = s['va'] + o
        if any((va + d) in drel for d in (-3, -2, -1, 0, 1, 2, 3)): continue
        v = struct.unpack_from('<I', blob, o)[0]
        if IMG_LO <= v < IMG_HI:
            if v in K: fields[va] = (v, 'value-rule'); n_extra += 1
            else: extra_lit += 1
SKIP = []
DROPT = set()
if os.environ.get('DV3_DROPT'):     # link-v2: pointer fields whose target is CRT/lib code that no linked object defines are dead captured CRT tables: emitted as zero, no reloc
    DROPT = {int(x, 16) for x in json.load(open(os.environ['DV3_DROPT']))}
    for _f in list(fields):
        if fields[_f][0] in DROPT: del fields[_f]
if os.environ.get('DV3_SKIP'):      # link-v2: ranges whose bytes come from our objects (EH tables): emitted as zeros, no pointer fields, no labels
    SKIP = json.load(open(os.environ['DV3_SKIP']))
    for _f in list(fields):
        if any(_a <= _f < _a + _n for _a, _n in SKIP): del fields[_f]
print('fields', len(fields), 'orig-reloc', len(drel), 'value-rule', n_extra, 'literal look-alikes', extra_lit)
# ---------------------------------------------------------------- labels
bss_lo = SEC['.data']['va'] + SEC['.data']['raw']; bss_hi = SEC['.data']['va'] + SEC['.data']['vs']
def place_of(va):
    if bss_lo <= va < bss_hi: return 'bss'
    n = sec_of(va)
    return n if n in DATA_SECS else None
labels = collections.defaultdict(set)      # place -> set(va)
tgt_kind = {}
fdesc = {}                                 # va -> (symbol, addend, kind)
ext_targets = {}
for f, (v, ev) in sorted(fields.items()):
    if TLO <= v < THI:
        sym, add, k = code_symbol(v); fdesc[f] = (sym, add, k)
    else:
        p = place_of(v)
        if p is None:
            fdesc[f] = ('X_%08x' % v, 0, 'other-section'); ext_targets[v] = sec_of(v)
        else:
            labels[p].add(v); fdesc[f] = ('D_%08x' % v, 0, 'data')
if os.environ.get('DV3_CNAMES') == '1':     # link-v2: extra D_<va> labels for every data address the linked objects name
    for _v in json.load(open(RN + r'\link-v2\extra_labels.json')):
        _p = place_of(_v)
        if _p: labels[_p].add(_v)
if os.environ.get('DV3_NOLABEL'):      # link-v2: addresses whose symbol is supplied by the CRT/linker instead (e.g. the TLS index)
    _nl = {int(x, 16) for x in json.load(open(os.environ['DV3_NOLABEL']))}
    for p in list(labels): labels[p] -= _nl
# a label strictly inside another field's bytes -> retarget to the field start label (rare)
field_starts = sorted(fields)
def inside_field(va):
    j = bisect.bisect_right(field_starts, va) - 1
    return j >= 0 and field_starts[j] < va < field_starts[j] + 4
fix = 0
for p in list(labels):
    for v in list(labels[p]):
        if inside_field(v):
            labels[p].discard(v); fix += 1
print('labels', {k: len(v) for k, v in labels.items()}, 'dropped (inside a field)', fix)
for f in list(fdesc):
    if fdesc[f][2] == 'data':
        v = fields[f][0]
        p = place_of(v)
        if v not in labels[p]:
            j = bisect.bisect_right(field_starts, v) - 1
            fs = field_starts[j]
            labels[p].add(fs); fdesc[f] = ('D_%08x' % fs, v - fs, 'data')
# ---------------------------------------------------------------- emit
def q(b):
    return "'" + ''.join(chr(c) if c != 0x27 else "''" for c in b) + "'"
def emit_bytes(lines, blob):
    """typed literals: zero runs, ASCII strings, hex bytes"""
    i = 0; n = len(blob)
    while i < n:
        if blob[i] == 0:
            j = i
            while j < n and blob[j] == 0: j += 1
            if j - i >= 8: lines.append('db %d dup(0)' % (j - i)); i = j; continue
        j = i
        while j < n and 0x20 <= blob[j] < 0x7f: j += 1
        if j - i >= 4:
            for k in range(i, j, 100): lines.append('db ' + q(blob[k:min(j, k + 100)]))
            i = j
            continue
        lines.append('db ' + ','.join('0%02Xh' % b for b in blob[i:i + 16 if i + 16 <= n else n])); i += min(16, n - i)
used_ext = collections.defaultdict(set)
_PH = os.environ.get('DV3_PHASE') == '1'      # link-v2 only: PAGE-aligned segments with original phase (default output is the original DWORD segments)
SEGDEF = ({'.rdata': ("_RDATAP", "SEGMENT PAGE READONLY PUBLIC 'CONST'"), '.data': ('_DATAP', "SEGMENT PAGE PUBLIC 'DATA'"),
           '.tls': ('_TLS', "SEGMENT PAGE PUBLIC 'DATA'"), 'CONST': ('_CONSTPE', "SEGMENT PAGE READONLY PUBLIC 'CONST'")} if _PH else
          {'.rdata': ("CONST", "SEGMENT DWORD READONLY PUBLIC 'CONST'"), '.data': ('_DATA', "SEGMENT DWORD PUBLIC 'DATA'"),
           '.tls': ('_TLS', "SEGMENT DWORD PUBLIC 'DATA'"), 'CONST': ('_CONSTPE', "SEGMENT DWORD READONLY PUBLIC 'CONST'")})
FILES = {'.rdata': 'rdata', '.data': 'data', '.tls': 'tls', 'CONST': 'const'}
segmap = {}
manifest = []
LIM = 40000
def write_chunk(name, k, lines, exts, locl, tail, start, size):
    seg, defn = SEGDEF[name]
    asm = ['.386', '.model flat', 'option casemap:none']
    for e in sorted(exts | locl): asm.append('EXTERNDEF %s:%s' % (e, 'BYTE' if e.startswith(('D_', 'X_')) else 'NEAR'))
    for e in sorted(locl): asm.append('PUBLIC %s' % e)
    asm.append('%s %s' % (seg, defn))
    _ph = (SEC[name]['va'] + start) % 256 if os.environ.get('DV3_PHASE') == '1' else 0
    if _ph: asm.append('db %d dup(0)' % _ph)
    asm += lines; asm.append('%s ENDS' % seg)
    if tail:
        if _PH:
            asm.append("_BSSP SEGMENT PAGE PUBLIC 'BSS'")
            if bss_lo % 256: asm.append('db %d dup(?)' % (bss_lo % 256))
            asm += tail; asm.append('_BSSP ENDS')
        else: asm.append("_BSS SEGMENT DWORD PUBLIC 'BSS'"); asm += tail; asm.append('_BSS ENDS')
    asm.append('END')
    fn_ = '%s_%02d' % (FILES[name], k)
    open(os.path.join(OUT, fn_ + '.asm'), 'w').write(chr(10).join(asm) + chr(10))
    manifest.append(dict(file=fn_, section=name, va=SEC[name]['va'] + start, size=size, object_section={'.rdata': '.rdata', '.data': '.data', '.tls': '_TLS (rename to .tls)', 'CONST': '_CONSTPE (rename to CONST)'}[name]))
    return len(lines)
def emit_section(name):
    s = SEC[name]; blob = bytearray(ref[s['off']:s['off'] + s['raw']]) if SKIP else ref[s['off']:s['off'] + s['raw']]
    for _a, _n in SKIP:
        if s['va'] <= _a < s['va'] + s['raw']: blob[_a - s['va']:_a - s['va'] + _n] = bytes(min(_n, s['raw'] - (_a - s['va'])))
    evs = sorted([(f - s['va'], 'f') for f in fields if s['va'] <= f < s['va'] + s['raw']] + [(v - s['va'], 'l') for v in labels.get(name, ()) if s['va'] <= v < s['va'] + s['raw']])
    byoff = collections.defaultdict(list)
    for o, k in evs: byoff[o].append(k)
    offs = sorted(byoff)
    pos = 0; ofs_i = 0; k = 0; total = 0
    lines = []; exts = set(); locl = set(); nf = 0; cstart = 0
    def close(end):
        nonlocal lines, exts, locl, nf, cstart, k, total
        tail = []
        if name == '.data' and end >= len(blob):
            tailn = s['vs'] - s['raw']; bl = sorted(v - bss_lo for v in labels.get('bss', ())); p = 0
            for o in bl:
                if o > p: tail.append('db %d dup(?)' % (o - p)); p = o
                tail.append('D_%08x LABEL BYTE' % (bss_lo + o)); locl.add('D_%08x' % (bss_lo + o))
            if tailn > p: tail.append('db %d dup(?)' % (tailn - p))
        total += write_chunk(name, k, lines, exts, locl, tail, cstart, end - cstart)
        k += 1; lines = []; exts = set(); locl = set(); nf = 0; cstart = end
    while pos < len(blob):
        nxt = offs[ofs_i] if ofs_i < len(offs) else len(blob)
        if nf >= LIM and nxt >= pos:
            close(pos)
        if nxt > pos:
            lim_end = nxt
            emit_bytes(lines, blob[pos:lim_end]); pos = nxt
            continue
        ks = byoff[nxt]; ofs_i += 1
        if 'l' in ks:
            lines.append('D_%08x LABEL BYTE' % (s['va'] + nxt)); locl.add('D_%08x' % (s['va'] + nxt))
        if 'f' in ks:
            sym, add, kind = fdesc[s['va'] + nxt]
            exts.add(sym); nf += 1
            lines.append('dd offset %s%s' % (sym, ('%+d' % add) if add else ''))
            pos = nxt + 4
    close(len(blob))
    return total
for nm in DATA_SECS:
    print(nm, 'lines', emit_section(nm))
# ---------------------------------------------------------------- symbolic.json
strict = open(RN + r'\data-v1\FalloutNV_data_strict.exe', 'rb').read()
def ours(va):
    n = sec_of(va); s = SEC[n]; o = s['off'] + va - s['va']
    return strict[o:o + 4] == ref[o:o + 4] and ref[o:o + 4] != b'\0\0\0\0'
rows = []; cnt = collections.Counter()
for f in sorted(fields):
    v, ev = fields[f]; sym, add, kind = fdesc[f]; n = sec_of(f)
    og = 'ours' if ours(f) else 'captured'
    rows.append([n, f - SEC[n]['va'], sym, add, ev, og, kind])
    cnt[(ev, og, kind)] += 1
json.dump(dict(note='fields: [section, offset in section, target symbol, addend, evidence (orig-reloc = reference .reloc; value-rule = exact function/piece/label start, no reloc in reference), origin (ours = bytes produced by our objects in data-v1 and equal to the reference; captured = reference bytes), target kind]',
               sections={k: dict(va=v['va'], raw=v['raw'], virt=v['vs']) for k, v in SEC.items() if k in DATA_SECS},
               bss=dict(va=bss_lo, size=bss_hi - bss_lo), fields=rows), open(os.path.join(OUT, 'symbolic.json'), 'w'), separators=(',', ':'))
csyms = {}
for f, (sym, add, kind) in fdesc.items():
    if kind != 'data' and kind != 'other-section':
        v = fields[f][0]
        csyms[sym] = dict(va=v - add, kind=kind)
json.dump(csyms, open(os.path.join(OUT, 'code_symbols.json'), 'w'), indent=0)
json.dump(manifest, open(os.path.join(OUT, 'manifest.json'), 'w'), indent=0)
dl = {'D_%08x' % v: dict(va=v, section=p) for p, vs in labels.items() for v in vs}
json.dump(dict(data_labels=dl, ext_targets={'X_%08x' % k: v for k, v in ext_targets.items()}), open(os.path.join(OUT, 'data_labels.json'), 'w'))
print('fields by evidence/origin/kind:'); [print(' ', k, v) for k, v in sorted(cnt.items())]
print('code symbols', len(csyms), 'data labels', len(dl))
