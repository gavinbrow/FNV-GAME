r"""M3 phase 1 generator: scalar DAT_ globals as definitions in OUR source, compiled with the unit compiler (sp1, /MT /Od /Oy- /GS /EHsc /Gy).
usage: python -I gen_m3.py [--select]          (--select: (re)build pilot_selection.json from units.json + reference + current data-v3 state; otherwise it is read)
Env:   FNV_M3_NEGCTL=1  negative control: the initializer of the first entry is changed (+1) and that entry skips the self-check.
Outputs (m3\gen): m3_data.cpp, m3_data.obj, m3_manifest.json, skip_ranges.json (DV3_SKIP format), m3_gen.log.json
Batch 3 (phase 1b slice 1): FNV_M3_SEL=batch3_selection.json (gen_m3.py --select-batch3 writes it: batch2 + single-pointer globals). A pointer entry is
`void* DAT_x = (void*)&M3F_<target>;` (code target) / `&M3D_<target>` (data target), extern "C" targets named by their original address; DIR32 reloc, addend 0 (checked).
Env:   FNV_M3_NEGCTL=ptr  negative control for pointers: the first pointer entry is retargeted to another entry's target (exempt from the self-check).
Batch 4 (phase 1b slice 2): FNV_M3_SEL=batch4_selection.json (gen_m3.py --select-batch4: batch3 + arrays/strings (tc 'A'), pointer tables (tc 'T'), regular mixed tables (tc 'X')).
Env:   FNV_M3_NEGCTL=b4v (first int array: first element +1) / b4p (first pointer table: first relocated element retargeted); both exempt from the self-check.
Batch 7: FNV_M3_SEL=batch7_selection.json (b7_select.py writes it: batch4 + generic typed objects 'W' for namespaced-only globals, scalar-declared tables, undeclared tails).
Env:   FNV_M3_NEGCTL=b7v (first new object with a dword run: first dword +1) / b7p (first new object with a pointer cell: retargeted); both exempt from the self-check.
Entries beyond batch 4 are compiled into extra objects m3_data_<k>.obj (a COFF section holds at most 65535 relocations); entry['obj'] = k.
Self-check: every kept definition's bytes sliced out of the object (per symbol) == the reference bytes; section name matches the VA's section; no relocation; no dynamic initializer."""
import os, sys, re, json, struct, math, subprocess, collections, bisect
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
PROJ = os.environ.get('FNV_PROJ_ROOT') or r'C:\path\to\Decompilation'
RN = os.path.join(PROJ, 'runtime-next')
sys.path.insert(0, os.path.join(RN, 'data-v3')); sys.path.insert(0, os.path.join(RN, 'pinned-build'))
if os.environ.get('FNV_M3_DATASRC') == '1' and 'datasrc_gen' not in sys.modules and not any(a.startswith('--select') for a in sys.argv):      # batch 10: the data as source; never opens the reference
    import datasrc_build; datasrc_build.main(); raise SystemExit(0)
from common import ref, SEC, sec_of, orig_reloc_sites, TLO, THI
import splice
ORIG_SITES = sorted(orig_reloc_sites()); ORIG_SET = set(ORIG_SITES); RENDER_STAT = collections.Counter()
GEN = splice.GEN; os.makedirs(GEN, exist_ok=True)
SELF = os.path.join(HERE, os.environ.get('FNV_M3_SEL') or 'pilot_selection.json')   # FNV_M3_SEL=batch2_selection.json for batch 2 (default: the pilot)
BATCH2 = os.path.join(HERE, 'batch2_selection.json')
BATCH3 = os.path.join(HERE, 'batch3_selection.json')
BATCH4 = os.path.join(HERE, 'batch4_selection.json')
NEG = os.environ.get('FNV_M3_NEGCTL') == '1'
NEGP = os.environ.get('FNV_M3_NEGCTL') == 'ptr'
NEG4V = os.environ.get('FNV_M3_NEGCTL') == 'b4v'      # batch 4 negative controls: a value inside an array / a pointer inside a table
NEG4P = os.environ.get('FNV_M3_NEGCTL') == 'b4p'
NEG7V = os.environ.get('FNV_M3_NEGCTL') == 'b7v'      # batch 7 negative controls: a value / a pointer inside the new generic objects
NEG7P = os.environ.get('FNV_M3_NEGCTL') == 'b7p'
NEG8V = os.environ.get('FNV_M3_NEGCTL') == 'b8v'
NEG8P = os.environ.get('FNV_M3_NEGCTL') == 'b8p'
NEG9V = os.environ.get('FNV_M3_NEGCTL') == 'b9v'      # batch 9 negative controls: a value / a pointer inside the new batch 9 objects
NEG9P = os.environ.get('FNV_M3_NEGCTL') == 'b9p'
NEGP2SV = os.environ.get('FNV_M3_NEGCTL') == 'p2sv'
NEGP2AV = os.environ.get('FNV_M3_NEGCTL') == 'p2av'
NEGP2WP = os.environ.get('FNV_M3_NEGCTL') == 'p2wp'
NEGP2BW = os.environ.get('FNV_M3_NEGCTL') == 'p2bw'
NEGP2CW = os.environ.get('FNV_M3_NEGCTL') == 'p2cw'
NEGP2LV = os.environ.get('FNV_M3_NEGCTL') == 'p2lv'
NEGP2R = os.environ.get('FNV_M3_NEGCTL') in ('p2rv', 'p2rp', 'p2tv', 'p2tp', 'p2nv', 'p2np', 'p2bv', 'p2bp', 'p2cv', 'p2cp')
ANYNEG = NEG or NEGP or NEG4V or NEG4P or NEG7V or NEG7P or NEG8V or NEG8P or NEG9V or NEG9P or NEGP2SV or NEGP2AV or NEGP2WP or NEGP2BW or NEGP2CW or NEGP2LV or NEGP2R
TYPES = {'H': ('int', 4), 'I': ('unsigned', 4), 'M': ('float', 4), 'N': ('double', 8),
         'J': ('long', 4), 'K': ('unsigned long', 4), 'F': ('short', 2), 'G': ('unsigned short', 2), 'D': ('char', 1), 'E': ('unsigned char', 1), '_N': ('bool', 1), 'C': ('signed char', 1)}
PILOT_TYPES = 'HIMN'
DAT_RE = re.compile(r'\?DAT_([0-9a-f]{8})((?:@[A-Za-z0-9_]+)*)@@3(.+)$')
ADDR_RE = re.compile(r'DAT_([0-9a-f]{8})')


def sec_range(n):
    s = SEC[n]; return s['va'], s['va'] + s['raw']


def refbytes(va, sz):
    n = sec_of(va); return ref[SEC[n]['off'] + va - SEC[n]['va']:][:sz]


def select(batch2=False, batch3=False):
    units = json.load(open(os.path.join(PROJ, 'fnv_decomp', 'build', 'units.json')))['units']
    forms = collections.defaultdict(set); glob = set(); alld = set()
    for u in units:
        for k in u.get('symbols', {}):
            for m in ADDR_RE.finditer(k): alld.add(int(m.group(1), 16))
            m = DAT_RE.match(k)
            if not m: continue
            va = int(m.group(1), 16); forms[va].add(m.group(3)[:-1])      # type code without the trailing A/B (const) letter
            if not m.group(2): glob.add(va)
    inv = json.load(open(os.path.join(HERE, 'inventory', 'dat_globals.json')))['globals']
    has_def = {int(g['addr'], 16) for g in inv if g['defs']}
    sj = json.load(open(os.path.join(RN, 'data-v3', 'symbolic.json')))
    fld = sorted({SEC[r[0]]['va'] + r[1] for r in sj['fields']} | set(orig_reloc_sites()))
    labels = sorted(int(v['va']) for v in json.load(open(os.path.join(RN, 'data-v3', 'out', 'data_labels.json')))['data_labels'].values())
    prod = sorted((r['va'], r['va'] + r['size']) for r in json.load(open(os.path.join(RN, 'data-v3', 'out', 'produced_ranges.json'))) if r['tier'] != 'M')
    alls = sorted(alld)
    def hit(sl, lo, hi):
        i = bisect.bisect_left(sl, lo); return i < len(sl) and sl[i] < hi
    cand = collections.defaultdict(list); why = collections.Counter(); pcand = []; drel = set(orig_reloc_sites())
    if batch3:
        for va in sorted(glob):
            t = forms[va]; w = 'p-'
            if len(t) != 1: continue
            tc = next(iter(t))
            if not (tc[0] in 'PQ' or tc in ('H', 'I')): continue          # pointer-typed, or int/unsigned used as a pointer; others are not pointer candidates
            n = sec_of(va)
            if n not in ('.data', '.rdata'): why[w + 'section'] += 1; continue
            if va + 4 > sec_range(n)[1] or va % 4: why[w + 'bounds/align'] += 1; continue
            if va not in drel: why[w + 'no-orig-reloc-at-va'] += 1; continue
            if va in has_def: why[w + 'source-def'] += 1; continue
            if any(f != va and (va - 3 <= f < va + 4 or (f == va + 4 and (va + 4) not in alls)) for f in drel | set(fld)): why[w + 'other-field-near'] += 1; continue   # a field at +4 is fine when +4 is a separately declared DAT_ (adjacent single pointers)
            if hit(alls, va + 1, va + 4) or hit(labels, va + 1, va + 4): why[w + 'inner-name'] += 1; continue
            if any(a < va + 4 and va < b for a, b in prod): why[w + 'produced'] += 1; continue
            tv = struct.unpack('<I', refbytes(va, 4))[0]; tn = sec_of(tv)
            bss_lo = SEC['.data']['va'] + SEC['.data']['raw']
            if not (tn in ('.text', '.rdata', '.data', 'CONST', '.tls') or bss_lo <= tv < SEC['.data']['va'] + SEC['.data']['vs']): why[w + 'target-outside'] += 1; continue
            pcand.append(dict(va=va, tc='P', decl=tc, ptr=tv, tgt=('code' if tn == '.text' else 'data'), sec=n))
    for va in sorted(glob):
        t = forms[va]
        if len(t) != 1 or next(iter(t)) not in TYPES: why['type'] += 1; continue
        tc = next(iter(t)); cty, sz = TYPES[tc]; n = sec_of(va)
        if n not in ('.data', '.rdata'): why['section'] += 1; continue
        lo, hi = sec_range(n)
        if va + sz > hi or va % sz: why['bounds/align'] += 1; continue
        raw = refbytes(va, sz)
        if not any(raw): why['zero'] += 1; continue
        if va in has_def: why['source-def'] += 1; continue
        if hit(alls, va + 1, va + sz) or hit(labels, va + 1, va + sz): why['inner-name'] += 1; continue
        if hit(fld, va - 3, va + sz): why['field'] += 1; continue
        if any(a < va + sz and va < b for a, b in prod): why['produced'] += 1; continue
        if tc == '_N' and raw[0] > 1: why['bool-not-0/1'] += 1; continue
        if tc == 'M':
            v = struct.unpack('<f', raw)[0]
            if math.isnan(v) or math.isinf(v) or (v != 0 and abs(v) < 1.1754944e-38): why['float-special'] += 1; continue
        if tc == 'N':
            v = struct.unpack('<d', raw)[0]
            if math.isnan(v) or math.isinf(v) or (v != 0 and abs(v) < 2.2250738585072014e-308): why['float-special'] += 1; continue
        cand[(n, tc)].append(va)
    c = {'%s/%s' % k: len(v) for k, v in cand.items()}
    print('candidates', c, 'rejected', dict(why))
    pick = [(va, 'H') for va in cand[('.data', 'H')]] + [(va, 'I') for va in cand[('.data', 'I')]] + [(va, 'M') for va in cand[('.data', 'M')][:37]] \
        + [(va, 'M') for va in cand[('.rdata', 'M')][:12]] + [(va, 'N') for va in cand[('.rdata', 'N')][:12]]
    if batch2:       # pilot first (subset, same order), then every other candidate by (section, type, va)
        have = {va for va, tc in pick}
        rest = [(va, k[1]) for k in sorted(cand) for va in cand[k] if va not in have]
        sel = [dict(va=va, tc=tc) for va, tc in pick + rest]
        json.dump(dict(note='frozen batch2 selection (gen_m3.py --select-batch2); pilot entries first; candidates per section/type: %s' % c, entries=sel), open(BATCH2, 'w'), indent=0)
        return sel
    if batch3:       # batch2 (pilot first) + the single-pointer globals, by (section, target kind, va)
        b2 = json.load(open(BATCH2))['entries']; sel = b2 + sorted(pcand, key=lambda e: (e['sec'], e['tgt'], e['va']))
        pc = collections.Counter('%s/%s/%s' % (e['sec'], e['tgt'], e['decl']) for e in pcand)
        print('pointer candidates', len(pcand), dict(pc), 'rejected', {k: v for k, v in why.items() if k.startswith('p-')})
        json.dump(dict(note='frozen batch3 selection (gen_m3.py --select-batch3): batch2 entries first, then %d single-pointer globals (%s)' % (len(pcand), dict(pc)), entries=sel), open(BATCH3, 'w'), indent=0)
        return sel
    sel = [dict(va=va, tc=tc) for va, tc in pick]
    json.dump(dict(note='frozen pilot selection (gen_m3.py --select); candidates per section/type: %s' % c, entries=sel), open(os.path.join(HERE, 'pilot_selection.json'), 'w'), indent=0)
    return sel


SCALAR_TEXT = {'int': 'H', 'unsigned int': 'I', 'unsigned': 'I', 'float': 'M', 'double': 'N', 'char': 'D', 'unsigned char': 'E', 'short': 'F', 'unsigned short': 'G', 'long': 'J', 'unsigned long': 'K'}
INTS_TEXT = {'int', 'unsigned int', 'unsigned', 'long', 'unsigned long', 'DWORD', 'u32', 'uint', 'UINT', 'LONG', 'ULONG', 'uintptr_t', 'intptr_t', 'size_t'}
ARR_RE = re.compile(r'^(.*?)\s*\[(\d*)\]$')


def _norm(t):
    t = t.strip()
    for w in ('const ', 'volatile ', 'static '):
        while t.startswith(w): t = t[len(w):].strip()
    return t


def ptrish_text(t):
    t = _norm(t)
    return '*' in t or t in INTS_TEXT


def form_class(f):
    """mangled type (without the trailing A/B) -> ('scalar', tc) | ('arr', tc) | ('other', None)"""
    if f in TYPES: return ('scalar', f)
    if len(f) >= 3 and f[:2] in ('PA', 'QB', 'PB', 'QA') and f[2:] in TYPES and f[2:] != '_N': return ('arr', f[2:])
    return ('other', None)


def select_batch4():
    """batch 4 = batch3 + arrays of scalars / strings (tc 'A'), pointer tables (tc 'T'), regular mixed {ptr,int,..} tables (tc 'X').  -> (new entries, stats)"""
    units = json.load(open(os.path.join(PROJ, 'fnv_decomp', 'build', 'units.json')))['units']
    forms = collections.defaultdict(set); glob = set(); alld = set()
    for u in units:
        for k in u.get('symbols', {}):
            for m in ADDR_RE.finditer(k): alld.add(int(m.group(1), 16))
            m = DAT_RE.match(k)
            if not m: continue
            va = int(m.group(1), 16); forms[va].add(m.group(3)[:-1])
            if not m.group(2): glob.add(va)
    alls = sorted(alld)
    inv = {int(g['addr'], 16): g for g in json.load(open(os.path.join(HERE, 'inventory', 'dat_globals.json')))['globals']}
    sj = json.load(open(os.path.join(RN, 'data-v3', 'symbolic.json')))
    drel = set(orig_reloc_sites()); fldall = {SEC[r[0]]['va'] + r[1] for r in sj['fields']} | drel
    vr = fldall - drel                                            # value-rule fields (no .reloc entry): never inside an emitted table
    fldS = sorted(fldall)
    labels = sorted(int(v['va']) for v in json.load(open(os.path.join(RN, 'data-v3', 'out', 'data_labels.json')))['data_labels'].values())
    prod = sorted((r['va'], r['va'] + r['size']) for r in json.load(open(os.path.join(RN, 'data-v3', 'out', 'produced_ranges.json'))) if r['tier'] != 'M')
    chunks = sorted((m['va'], m['va'] + m['size']) for m in json.load(open(os.path.join(RN, 'data-v3', 'out', 'manifest.json'))) if m['section'] in ('.data', '.rdata'))
    b3 = json.load(open(BATCH3))['entries']
    prior = sorted((e['va'], e['va'] + (4 if e['tc'] == 'P' else TYPES[e['tc']][1])) for e in b3)
    cover = sorted(prod + prior); coverS = [a for a, b in cover]; hard = sorted(set(coverS))
    why = collections.Counter(); out = []; taken = []; folded = collections.Counter()
    bss_lo = SEC['.data']['va'] + SEC['.data']['raw']; bss_hi = SEC['.data']['va'] + SEC['.data']['vs']

    def covered(lo, hi):
        i = bisect.bisect_right(coverS, hi - 1) - 1
        return any(cover[j][0] < hi and lo < cover[j][1] for j in range(max(0, i - 60), i + 1))

    def nxt(sl, va):
        i = bisect.bisect_right(sl, va); return sl[i] if i < len(sl) else 1 << 40

    def fld_in(lo, hi):         # a 4-byte field overlapping [lo, hi)
        i = bisect.bisect_right(fldS, lo - 4); return i < len(fldS) and fldS[i] < hi

    def lab_in(lo, hi):         # a data-v3 label strictly inside (lo, hi)
        i = bisect.bisect_right(labels, lo); return i < len(labels) and labels[i] < hi

    def decl_ok(a, cls, etc):   # declared name `a` inside a table: an element of the same table (non-array scalar of the element kind, no source definition)
        g = inv.get(a)
        if not g or g['defs'] or not g['declared_types']: return False
        if cls == 'S': return all(SCALAR_TEXT.get(_norm(t)) == etc for t in g['declared_types'])
        return all((not ARR_RE.match(_norm(t))) and ptrish_text(t) for t in g['declared_types'])

    def bound(va, cls, esz, etc):
        n = sec_of(va); E = min(sec_range(n)[1], nxt(hard, va))
        i = bisect.bisect_right(alls, va); fo = []
        while i < len(alls) and alls[i] < E:
            a = alls[i]
            if (a - va) % esz == 0 and decl_ok(a, cls, etc): fo.append(a); i += 1; continue
            E = a; break
        return E, fo

    def validtarget(tv):
        tn = sec_of(tv)
        return tn in ('.text', '.rdata', '.data', 'CONST', '.tls') or bss_lo <= tv < bss_hi

    def floatok(raw, tc):
        if tc == 'M':
            v = struct.unpack('<f', raw)[0]; return not (math.isnan(v) or math.isinf(v) or (v != 0 and abs(v) < 1.1754944e-38))
        if tc == 'N':
            v = struct.unpack('<d', raw)[0]; return not (math.isnan(v) or math.isinf(v) or (v != 0 and abs(v) < 2.2250738585072014e-308))
        return True

    def one_chunk(lo, hi):
        i = bisect.bisect_right([a for a, b in chunks], lo) - 1
        return i >= 0 and chunks[i][0] <= lo and hi <= chunks[i][1]

    for va in sorted(glob):
        t = forms[va]
        if len(t) != 1: continue
        f = next(iter(t)); kc, ftc = form_class(f); n = sec_of(va)
        if n not in ('.data', '.rdata'): continue
        if covered(va, va + 1): why['start covered by batch2/3 or produced'] += 1; continue
        if taken and taken[-1][0] <= va < taken[-1][1]: why['declared name folded into an earlier table'] += 1; continue
        g = inv.get(va)
        if g is None or g['defs']: why['source definition'] += 1; continue
        arrdecl = any(ARR_RE.match(_norm(t_)) for t_ in g['declared_types'])
        first_reloc = va in drel
        cand = []
        # ---- arrays of scalars / strings (declared T[] with a single consistent mangled array type, no field inside)
        if kc == 'arr' and arrdecl and not first_reloc:
            cty, esz = TYPES[ftc]
            if va % esz: why['array: unaligned'] += 1; continue
            E, fo = bound(va, 'S', esz, ftc); raw = refbytes(va, E - va); ne = len(raw) // esz; i = 0
            while i < ne:
                pos = va + i * esz
                if fld_in(pos, pos + esz) or not floatok(raw[i * esz:(i + 1) * esz], ftc): break
                if esz > 1 and any(pos < l_ < pos + esz for l_ in labels[bisect.bisect_right(labels, pos):bisect.bisect_right(labels, pos + esz)]): break
                i += 1
            raw = raw[:i * esz]
            if not any(raw): why['array: all zero / no element'] += 1
            else:
                k = max(j for j, b in enumerate(raw) if b)
                keep = (k + 2 + 3) // 4 * 4 if ftc == 'D' else ((k // esz + 1) * esz + 16) // esz * esz     # string: last char + NUL, padded to 4; numeric: trailing zeros capped at 16 bytes
                keep = max(min(keep, len(raw)), esz)
                if keep // esz == 1 and ftc != 'D': why['array: single element (scalar, left)'] += 1
                else: cand.append((keep, dict(va=va, tc='A', et=ftc, size=keep), fo))
        # ---- pointer tables and regular mixed tables
        if (kc == 'other' or ftc in ('H', 'I', 'J', 'K')) and va % 4 == 0 and (kc != 'scalar' or ftc in ('H', 'I', 'J', 'K')):
            E, fo = bound(va, 'P', 4, None); m = (E - va) // 4; cls = []
            for i in range(m):
                pos = va + 4 * i; v = struct.unpack('<I', refbytes(pos, 4))[0]
                if i and lab_in(pos, pos + 4): break
                if pos in drel:
                    if not validtarget(v): break
                    cls.append('R')
                elif pos in vr: break
                elif v == 0: cls.append('Z')
                else: cls.append('I')
            nT = 0
            while nT < len(cls) and cls[nT] in 'RZ': nT += 1
            if sum(1 for c in cls[:nT] if c == 'R') >= 2:
                last = max(i for i in range(nT) if cls[i] == 'R'); keepT = min(nT, last + 1 + 4)
                cand.append((keepT * 4, dict(va=va, tc='T', size=keepT * 4), fo))
            bestX = None
            for p in (2, 3, 4):
                col = ['?'] * p; rows = 0
                for r in range(len(cls) // p):
                    nc = list(col); ok = True
                    for c, ch in enumerate(cls[r * p:(r + 1) * p]):
                        if ch == 'R':
                            if nc[c] == 'I': ok = False
                            nc[c] = 'R'
                        elif ch == 'I':
                            if nc[c] == 'R': ok = False
                            nc[c] = 'I'
                    if not ok: break
                    col = nc; rows += 1
                nzr = [r for r in range(rows) if any(c != 'Z' for c in cls[r * p:(r + 1) * p])]
                if not nzr: continue
                rows = min(rows, nzr[-1] + 2)
                pat = ''.join('P' if c == 'R' else 'I' for c in col)
                nrel = sum(1 for c in cls[:rows * p] if c == 'R'); nint = sum(1 for c in cls[:rows * p] if c == 'I')
                if rows >= 3 and nrel >= 2 and nint >= 1 and 'P' in pat and 'I' in pat and (bestX is None or rows * p > bestX[0]): bestX = (rows * p, pat)
            if bestX: cand.append((bestX[0] * 4, dict(va=va, tc='X', size=bestX[0] * 4, pat=bestX[1]), fo))
        if not cand:
            why['no array/table shape (left)'] += 1; continue
        cand.sort(key=lambda c: -c[0]); nb, e, fo = cand[0]
        if va + nb > sec_range(n)[1]: why['bounds'] += 1; continue
        if covered(va, va + nb): why['overlaps batch2/3 or produced'] += 1; continue
        if not one_chunk(va, va + nb): why['crosses a data-v3 chunk boundary'] += 1; continue
        out.append(e); taken.append((va, va + nb))
        folded[e['tc']] += sum(1 for a in fo if a < va + nb)
    why.update({'folded names (' + k + ')': v for k, v in folded.items()})
    return out, why


def fmt(tc, raw):
    if tc in 'FGDEC' or tc == '_N':
        sz = len(raw)
        if tc == '_N': return 'true' if raw[0] else 'false'
        v = int.from_bytes(raw, 'little', signed=tc in 'FDC')
        if tc == 'F': return '(short)%d' % v
        if tc == 'G': return '(unsigned short)%d' % v
        if tc == 'D': return '(char)%d' % v
        if tc == 'C': return '(signed char)%d' % v
        return '(unsigned char)%d' % v
    if tc == 'J':
        v = struct.unpack('<i', raw)[0]; return str(v) if v != -2147483648 else '(-2147483647L-1)'
    if tc == 'K': return '0x%08xul' % struct.unpack('<I', raw)[0]
    if tc == 'H':
        v = struct.unpack('<i', raw)[0]; return str(v) if v != -2147483648 else '(-2147483647-1)'
    if tc == 'I': return '0x%08xu' % struct.unpack('<I', raw)[0]
    if tc == 'M':
        v = struct.unpack('<f', raw)[0]
        if v == 0: return '-0.0f' if raw[3] & 0x80 else '0.0f'
        for p in (6, 7, 8, 9):
            s = '%.*g' % (p, v)
            if struct.pack('<f', float(s)) == raw and abs(float(s)) <= 3.4028234663852886e38: break
        else: s = '%.17g' % v
        if not any(ch in s for ch in '.e'): s += '.0'
        return s + 'f'
    v = struct.unpack('<d', raw)[0]
    if v == 0: return '-0.0' if raw[7] & 0x80 else '0.0'
    s = '%.17g' % v
    if not any(ch in s for ch in '.e'): s += '.0'
    return s


# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# Batch 7: generic typed objects 'W' (packed struct of runs). Run classes: P pointers (void*, 0 = null), U unsigned dwords, H int, I unsigned (declared head), J long, K unsigned long,
# M float, N double, S char string (NUL terminated, padded), B bytes, Z zero bytes.  A run descriptor is [cls, count] (count = elements; S/B/Z: bytes; N: doubles).
PRINT = frozenset(list(range(0x20, 0x7f)) + [9, 10, 13])
RUN_SZ = {'P': 4, 'U': 4, 'H': 4, 'I': 4, 'J': 4, 'K': 4, 'M': 4, 'N': 8, 'S': 1, 'B': 1, 'Z': 1}
RUN_CTY = {'P': 'void*', 'U': 'unsigned', 'H': 'int', 'I': 'unsigned', 'J': 'long', 'K': 'unsigned long', 'M': 'float', 'N': 'double', 'S': 'char', 'B': 'unsigned char', 'Z': 'unsigned char'}
MAXRUNS = 1500


def _plaus_f(raw):
    v = struct.unpack('<f', raw)[0]
    if v != v or v in (float('inf'), float('-inf')) or v == 0 or not (1e-6 <= abs(v) <= 1e9): return False
    return any(struct.pack('<f', float('%.*g' % (p, v))) == raw for p in range(1, 7))


def _plaus_d(raw):
    v = struct.unpack('<d', raw)[0]
    if v != v or v in (float('inf'), float('-inf')) or v == 0 or not (1e-9 <= abs(v) <= 1e12): return False
    return any(struct.pack('<d', float('%.*g' % (p, v))) == raw for p in range(1, 13))


def _floatok4(raw, tc):
    if tc == 'M':
        v = struct.unpack('<f', raw)[0]; return not (math.isnan(v) or math.isinf(v) or (v != 0 and abs(v) < 1.1754944e-38))
    v = struct.unpack('<d', raw)[0]; return not (math.isnan(v) or math.isinf(v) or (v != 0 and abs(v) < 2.2250738585072014e-308))


def _site_in(lo, hi):          # an original .reloc site in [lo, hi)
    i = bisect.bisect_left(ORIG_SITES, lo); return i < len(ORIG_SITES) and ORIG_SITES[i] < hi


def layout(va, raw, head, labels):
    """reference bytes of one piece -> run descriptors [[cls, count], ...] (exact: every byte is accounted for; pointers only at original .reloc sites; no label strictly inside a multi-byte element)"""
    n = len(raw); cells = []; p = 0; brk_next = False

    def lab_in(lo, hi):
        i = bisect.bisect_right(labels, lo); return i < len(labels) and labels[i] < hi
    if head in ('H', 'I', 'J', 'K') and n >= 4 and not _site_in(va + 1, va + 4):
        cells.append(['P' if va in ORIG_SET else head, 4, 1]); p = 4; brk_next = True
    elif head == 'M' and n >= 4 and not _site_in(va, va + 4) and not lab_in(va, va + 4) and _floatok4(raw[:4], 'M'):
        cells.append(['M', 4, 1]); p = 4; brk_next = True
    elif head == 'N' and n >= 8 and not _site_in(va, va + 8) and not lab_in(va, va + 8) and _floatok4(raw[:8], 'N'):
        cells.append(['N', 8, 1]); p = 8; brk_next = True
    while p < n:
        a = va + p; c = None
        if a in ORIG_SET and p + 4 <= n: c = ['P', 4, 0]
        elif raw[p] == 0:
            q = p
            while q < n and raw[q] == 0 and (va + q) not in ORIG_SET: q += 1
            if q - p >= 16: c = ['Z', q - p, 0]
        if c is None and raw[p] in PRINT:
            j = p
            while j < n and raw[j] in PRINT: j += 1
            if j - p >= 4 and j < n and raw[j] == 0 and not _site_in(a, va + j + 1):
                e = j + 1
                while (va + e) % 4 and e < n and raw[e] == 0 and (va + e) not in ORIG_SET: e += 1
                c = ['S', e - p, 0]
        if c is None and a % 4 == 0 and p + 4 <= n and not _site_in(a + 1, a + 4) and not lab_in(a, a + 4):
            w = raw[p:p + 4]
            if w == b'\0\0\0\0': c = ['z', 4, 0]
            elif a % 8 == 0 and p + 8 <= n and not _site_in(a + 4, a + 8) and not lab_in(a, a + 8) and _plaus_d(raw[p:p + 8]): c = ['N', 8, 0]
            elif _plaus_f(w): c = ['M', 4, 0]
            else: c = ['U', 4, 0]
        if c is None: c = ['B', 1, 0]
        if brk_next: c[2] = 1; brk_next = False
        cells.append(c); p += c[1]
    assert p == n
    for i, c in enumerate(cells):      # zero dwords join the neighbouring dword-class run
        if c[0] != 'z': continue
        pc = next((x[0] for x in reversed(cells[:i]) if x[0] != 'z'), None) if i and not c[2] else None
        nc = next((x[0] for x in cells[i + 1:] if x[0] != 'z'), None) if not (i + 1 < len(cells) and cells[i + 1][2]) else None
        c[0] = pc if pc in ('P', 'U', 'M') else (nc if nc in ('P', 'U', 'M') else 'U')
    runs = []
    for c in cells:
        if runs and not c[2] and runs[-1][0] == c[0] and c[0] != 'S': runs[-1][1] += c[1] // RUN_SZ[c[0]]
        else: runs.append([c[0], c[1] // RUN_SZ[c[0]]])
    return runs


def g_items(va, raw, runs):
    """run descriptors + reference bytes -> items per run (P: (is_site, value); other dword/float/double: raw bytes of one element; S/B/Z: the bytes)"""
    out = []; p = 0
    for cls, cnt in runs:
        sz = RUN_SZ[cls]; nb = cnt * sz; seg = raw[p:p + nb]
        if cls == 'P': it = [((va + p + 4 * k) in ORIG_SET, struct.unpack('<I', seg[4 * k:4 * k + 4])[0]) for k in range(cnt)]
        elif cls in ('S', 'B', 'Z'): it = seg
        else: it = [seg[sz * k:sz * (k + 1)] for k in range(cnt)]
        out.append(it); p += nb
    assert p == len(raw)
    return out


def g_fields(e):
    """pointer fields [offset, '', 0] and their target VAs of a G entry (from the run items)"""
    f = []; t = []; p = 0
    for (cls, cnt), it in zip(e['runs'], e['items']):
        if cls == 'P':
            for k, (site, v) in enumerate(it):
                if site: f.append([p + 4 * k, '', 0]); t.append(v)
        p += cnt * RUN_SZ[cls]
    e['fields'] = f; e['tgts'] = t


def g_render(e, ext):
    """struct definition text and initializer text of a G entry; extern "C" targets are added to ext {tv: decl}"""
    mem = []; ini = []
    for k, ((cls, cnt), it) in enumerate(zip(e['runs'], e['items'])):
        if cls == 'S':
            mem.append('char r%d[%d];' % (k, cnt)); assert it[-1] == 0; ini.append(cstr(it[:-1]))
            continue
        mem.append('%s r%d[%d];' % (RUN_CTY[cls], k, cnt))
        if cls == 'P':
            cs = []
            for site, v in it:
                if not site: cs.append('0'); continue
                code = TLO <= v < THI; ext[v] = 'extern "C" void M3F_%08x(void);' % v if code else 'extern "C" char M3D_%08x;' % v
                cs.append('(void*)&%s_%08x' % ('M3F' if code else 'M3D', v))
                RENDER_STAT['extern'] += 1
            ini.append('{%s}' % ', '.join(cs))
        elif cls == 'B': ini.append('{%s}' % ', '.join(str(b) for b in it))
        elif cls == 'Z': ini.append('{0}')
        else: ini.append('{%s}' % ', '.join(fmt({'U': 'I', 'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'M': 'M', 'N': 'N'}[cls], x) for x in it))
    return 'struct M3S_%08x { %s };' % (e['va'], ' '.join(mem)), '{%s}' % ', '.join(ini)


def mutate_bsaudio_tail(entries):
    hits = [e for e in entries if e.get('tc') == 'W' and e.get('va') == 0x011ac972]
    if len(hits) != 1: raise ValueError('BSAudio tail control requires exactly one tail')
    e = hits[0]
    if e['name'] != 'M3_011ac972' or e['size'] != 78 or e['section'] != '.data' or e['align'] != 1 or e['runs'] != [['S',2],['P',2],['S',24],['P',2],['U',9]] or e.get('fields') != [[2,'',0],[34,'',0]] or e.get('tgts') != [0x010f1ee0,0x010f1ee0]: raise ValueError('BSAudio tail control identity mismatch')
    if e['items'][1][0] != (True,0x010f1ee0): raise ValueError('BSAudio first pointer mismatch')
    e['items'][1][0] = (True,0x010f1ee4); g_fields(e); e['negctl'] = True
    print('NEGATIVE CONTROL (p2 BSAudio tail pointer): VA 011ac972 offset 2 changed from 010f1ee0 to 010f1ee4')


def mutate_bulk_tail(entries):
    hits = [e for e in entries if e.get('tc') == 'W' and e.get('va') == 0x01183f98]
    if len(hits) != 1: raise ValueError('bulk control requires one residual fragment')
    e = hits[0]
    if e['name'] != 'M3_01183f98' or e['size'] != 28 or e['section'] != '.data' or e['align'] != 1 or not e.get('file_backed') or e['runs'] != [['P',2],['S',20]] or e.get('fields') != [[0,'',0]] or e.get('tgts') != [0x010f1ee0] or e['items'][0][0] != (True,0x010f1ee0): raise ValueError('bulk residual fragment identity mismatch')
    e['items'][0][0] = (True,0x010f1ee4); g_fields(e); e['negctl'] = True
    print('NEGATIVE CONTROL (p2 bulk tail pointer): VA 01183f98 offset 0 changed from 010f1ee0 to 010f1ee4')


def check_g(e, data, rel, tab):
    """generic object: relocation offsets == original .reloc sites inside, each DIR32 with target + addend == the reference dword and addend bytes == reference minus target;
    every other byte equals the reference. -> reason or None"""
    ref_ = bytes.fromhex(e['ref']); sites = sorted(f - e['va'] for f in ORIG_SITES if e['va'] <= f < e['va'] + e['size'])
    if [r[0] for r in rel] != sites: return 'reloc sites %s != original .reloc sites %s' % ([r[0] for r in rel][:8], sites[:8])
    mask = bytearray(len(ref_))
    for off, nm, add in rel:
        refv = struct.unpack('<I', ref_[off:off + 4])[0]; tv = splice.resolve(nm, tab)
        if tv is None: return 'offset %d: unresolvable target %s' % (off, nm)
        if (tv + add) & 0xffffffff != refv: return 'offset %d: target %x + addend %d != reference value %x' % (off, tv, add, refv)
        if int.from_bytes(data[off:off + 4], 'little') != (refv - tv) & 0xffffffff: return 'offset %d: addend bytes %s' % (off, data[off:off + 4].hex())
        mask[off:off + 4] = b'\1\1\1\1'
    if len(data) != len(ref_): return 'size'
    if not any(mask) and data == ref_: return None
    for i in range(len(ref_)):
        if not mask[i] and data[i] != ref_[i]: return 'byte %d (va %08x): %02x != ref %02x' % (i, e['va'] + i, data[i], ref_[i])
    return None



def explicit_scalar_identity(r):
    """Validate an opt-in namespaced scalar identity against its exact COFF spelling."""
    if not any(k in r for k in ('scalar_namespace', 'scalar_const', 'scalar_symbol')):
        return None
    ns, const, symbol = r.get('scalar_namespace'), r.get('scalar_const'), r.get('scalar_symbol')
    if r.get('tc') not in TYPES or not isinstance(ns, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', ns):
        raise ValueError('invalid explicit scalar namespace or type')
    if type(const) is not bool or not isinstance(symbol, str) or r.get('generated_name'):
        raise ValueError('invalid explicit scalar constness or name')
    expected = '?DAT_%08x@%s@@3%s%s' % (r['va'], ns, r['tc'], 'B' if const else 'A')
    if symbol != expected or r.get('decl') != [symbol]:
        raise ValueError('explicit scalar declaration does not match symbol')
    return ns, const, symbol


def explicit_array_identity(r):
    """Validate the explicitly source-evidenced bounded array allowlist."""
    keys = ('array_namespace', 'array_const', 'array_symbol')
    if not any(k in r for k in keys): return None
    a = r.get('va'); ns = r.get('array_namespace'); const = r.get('array_const'); symbol = r.get('array_symbol')
    approved = {x: ('E', 256, 'sa238a0', 'PAEA') for x in range(0x011a7440, 0x011a7e40, 0x100)}
    approved.update({0x011aced8: ('I', 36, 'fnv_00af4550', 'PAIA'), 0x01093b6c: ('H', 16, 'fnv_009f9e50', 'PAHA')})
    if type(a) is not int or a not in approved: raise ValueError('unreviewed array address')
    et, size, expected_ns, suffix = approved[a]
    expected = '?DAT_%08x@%s@@3%s' % (a, expected_ns, suffix)
    if (r.get('tc') != 'A' or r.get('et') != et or r.get('size') != size or
        ns != expected_ns or const is not False or symbol != expected or r.get('decl') != [expected] or
        r.get('align') != 4 or a % 4 or r.get('generated_name')):
        raise ValueError('invalid reviewed array identity, type, extent or alignment')
    section = sec_of(a)
    if section not in ('.data', '.rdata'): raise ValueError('invalid array section')
    s = SEC[section]
    if not (s['va'] <= a and a + size <= s['va'] + s['raw']): raise ValueError('array outside raw section')
    with open(os.path.join(RN, 'data-v3', 'symbolic.json')) as f: sj = json.load(f)
    fields = {SEC[x[0]]['va'] + x[1] for x in sj['fields']} | ORIG_SET
    if any(a - 3 <= x < a + size for x in fields): raise ValueError('array overlaps field or relocation')
    with open(os.path.join(RN, 'data-v3', 'out', 'manifest.json')) as f: chunks = json.load(f)
    if not any(x['section'] == section and x['va'] <= a and a + size <= x['va'] + x['size'] for x in chunks):
        raise ValueError('array crosses data chunk')
    return ns, const, symbol


def build_entries(sel):
    out = []
    for r in sel:
        va, tc = r['va'], r['tc']; n = sec_of(va)
        if tc == 'Y':
            sys.path.insert(0, os.path.join(RN, 'm3', 'phase2'))
            import cost245_records
            out.append(cost245_records.build_entry(r, sys.modules[__name__])); continue
        if tc == 'V':
            approved = (0x010cb620, 0x010cb630)
            expected = '?DAT_%08x@fnv_00cd9d10@@3U__m128@1@A' % va
            if (va not in approved or r.get('size') != 16 or r.get('align') != 16 or r.get('class_namespace') != 'fnv_00cd9d10' or r.get('class_name') != '__m128' or r.get('class_symbol') != expected or r.get('decl') != [expected] or va % 16): raise ValueError('invalid source SIMD identity')
            with open(os.path.join(RN, 'data-v3', 'symbolic.json')) as f: sj = json.load(f)
            fields = {SEC[x[0]]['va']+x[1] for x in sj['fields']} | ORIG_SET
            with open(os.path.join(RN, 'data-v3', 'out', 'manifest.json')) as f: chunks = json.load(f)
            if sec_of(va) != '.rdata' or any(va-3 <= f < va+16 for f in fields) or not any(x['section']=='.rdata' and x['va']<=va and va+16<=x['va']+x['size'] for x in chunks): raise ValueError('invalid source SIMD range')
            raw = refbytes(va,16)
            if len(raw) != 16 or any(not _floatok4(raw[i:i+4], 'M') for i in range(0,16,4)): raise ValueError('unsupported source SIMD float')
            init = '{%s}' % ', '.join(fmt('M',raw[i:i+4]) for i in range(0,16,4))
            out.append(dict(sym=expected,name='DAT_%08x'%va,ns='fnv_00cd9d10',va=va,size=16,type='__m128',tc='V',section='.rdata',init=init,ref=raw.hex(),simd=True,file_backed=True,align=16)); continue
        if tc == 'Q':
            if (va != 0x011a9c30 or r.get('size') != 12 or r.get('align') != 4 or r.get('class_namespace') != 'fnv_005c25f0' or r.get('class_name') != 'NiPoint3' or r.get('class_symbol') != '?DAT_011a9c30@fnv_005c25f0@@3VNiPoint3@1@A' or r.get('decl') != [r.get('class_symbol')]): raise ValueError('invalid source-point identity')
            sj = json.load(open(os.path.join(RN, 'data-v3', 'symbolic.json')))
            fields = {SEC[x[0]]['va']+x[1] for x in sj['fields']} | ORIG_SET
            chunks = json.load(open(os.path.join(RN, 'data-v3', 'out', 'manifest.json')))
            if sec_of(va) != '.data' or any(va-3 <= f < va+12 for f in fields) or not any(x['section']=='.data' and x['va']<=va and va+12<=x['va']+x['size'] for x in chunks): raise ValueError('invalid source-point range')
            raw = refbytes(va,12)
            if len(raw) != 12 or any(not _floatok4(raw[i:i+4], 'M') for i in range(0,12,4)): raise ValueError('unsupported source-point float')
            init = '{%s}' % ', '.join(fmt('M',raw[i:i+4]) for i in range(0,12,4))
            out.append(dict(sym=r['class_symbol'],name='DAT_011a9c30',ns=r['class_namespace'],va=va,size=12,type='NiPoint3',tc='Q',section='.data',init=init,ref=raw.hex(),point3=True,align=4)); continue
        if tc == 'R':
            import b8_records
            out.append(b8_records.build_entry(r, sys.modules[__name__])); continue
        if tc == 'W':        # batch 7: generic typed object (run descriptors frozen in the selection, items re-derived from the reference bytes)
            raw = refbytes(va, r['size']); runs = [list(x) for x in r['runs']]; items = g_items(va, raw, runs); nm = ('DAT_%08x' if r.get('named') else 'M3_%08x') % va
            e = dict(sym=None, name=nm, ns=r.get('ns') or '', va=va, size=r['size'], type='M3S', tc='W', section=n, kind=r['kind'], ref=raw.hex(), align=r['align'], runs=runs, items=items, decl=r.get('decl'), head=r.get('head'))
            g_fields(e); out.append(e); continue
        if tc == 'P':        # pointer global: one DIR32 field at +0 to an extern "C" target named by its original address, addend 0
            raw = refbytes(va, 4); tv = r['ptr']; code = TLO <= tv < THI; k = 'M3F' if code else 'M3D'
            out.append(dict(sym=('?DAT_%08x@@3QAXA' if n == '.rdata' else '?DAT_%08x@@3PAXA') % va,
                            name='DAT_%08x' % va, va=va, size=4, type='void*', tc='P', section=n, init='(void*)&%s_%08x' % (k, tv), ref=raw.hex(),
                            ptr=dict(target=tv, addend=0, kind='code' if code else 'data'), fields=[[0, '_%s_%08x' % (k, tv), 0]]))
            continue
        if tc == 'A':        # array of scalars (tc 'A', element type code et); et 'D' = char array, emitted as a string initializer when exact
            et = r['et']; cty, esz = TYPES[et]; size = r['size']; raw = refbytes(va, size); assert size % esz == 0
            els = [fmt(et, raw[i:i + esz]) for i in range(0, size, esz)]
            init = None
            if et == 'D':
                k = max((j for j, b in enumerate(raw) if b), default=-1)
                if k + 2 <= size and k + 1 <= 6000: init = cstr(raw[:k + 1])
            e = dict(sym=None, name='DAT_%08x' % va, va=va, size=size, type=cty, tc='A', et=et, n=size // esz, section=n, ref=raw.hex(), kind='string' if et == 'D' else 'array', align=esz,
                     init=init or '{%s}' % ', '.join(els), els=els)
            out.append(e); continue
        if tc in ('T', 'X'):    # pointer table / regular mixed table: one descriptor per dword ('z' zero, 'p' pointer to target VA, 'i' integer)
            size = r['size']; raw = refbytes(va, size); el = []
            for i in range(size // 4):
                v = struct.unpack('<I', raw[4 * i:4 * i + 4])[0]
                el.append(('p', v) if (va + 4 * i) in ORIG_SET else (('z',) if v == 0 else ('i', v)))
            if tc == 'T': assert all(d[0] in 'zp' for d in el)
            e = dict(sym=None, name='DAT_%08x' % va, va=va, size=size, type='void*' if tc == 'T' else 'M3R_' + r['pat'], tc=tc, n=(size // 4 if tc == 'T' else size // 4 // len(r['pat'])), section=n,
                     ref=raw.hex(), kind='ptrtable' if tc == 'T' else 'mixed', align=4, elems=el)
            if tc == 'X': e['pat'] = r['pat']
            out.append(e); continue
        cty, sz = TYPES[tc]; raw = refbytes(va, sz)
        out.append(dict(sym='?DAT_%08x@@3%s%s' % (va, tc, 'B' if n == '.rdata' else 'A'), name='DAT_%08x' % va, va=va, size=sz, type=cty, tc=tc,
                        section=n, init=fmt(tc, raw), ref=raw.hex()))
    # Batch 8 uses separate generated names for declarations whose native
    # linkage or semantic aliases are unresolved.  Preserve the reviewed
    # evidence without pretending that a storage definition resolves aliases.
    for e, r in zip(out, sel):
        identity = explicit_scalar_identity(r)
        if identity:
            e['ns'], e['scalar_const'], e['sym'] = identity
            # Explicit placement permits mutable objects in .rdata and const
            # objects in .data without changing their native C++ identity.
            e['file_backed'] = True
        array_identity = explicit_array_identity(r)
        if array_identity:
            e['ns'], e['array_const'], e['sym'] = array_identity
            if e['section'] == '.rdata': e['file_backed'] = True
        if r.get('generated_name'):
            if not re.fullmatch(r'M3_[0-9a-f]{8}', r['generated_name']):
                raise ValueError('invalid generated storage name')
            if r['generated_name'] != 'M3_%08x' % e['va']:
                raise ValueError('generated storage name/address mismatch')
            e['name'] = r['generated_name']; e['sym'] = None
        for key in ('batch', 'evidence', 'file_backed', 'partial'):
            if key in r: e[key] = r[key]
        if 'align' in r: e['align'] = r['align']
    return out


def set_fields(e):
    """table entries: pointer fields [offset, '', 0] and their target VAs, derived from the element descriptors (the manifest keeps these, not the descriptors)"""
    e['fields'] = [[4 * i, '', 0] for i, d in enumerate(e['elems']) if d[0] in ('p', 'px')]
    e['tgts'] = [d[1] for d in e['elems'] if d[0] in ('p', 'px')]


def cstr(b):
    """bytes -> C string literal (adjacent pieces); octal escapes are always 3 digits, '?' is escaped (no trigraphs)"""
    parts = []; cur = ''
    for ch in b:
        c = chr(ch)
        if c in '"\\': cur += '\\' + c
        elif 0x20 <= ch < 0x7f and c != '?': cur += c
        else: cur += '\\%03o' % ch
        if len(cur) >= 80: parts.append('"%s"' % cur); cur = ''
    if cur or not parts: parts.append('"%s"' % cur)
    return ' '.join(parts)


def tyname(e):
    """(type, name with dimensions) of a definition / declaration of entry e"""
    rd = e['section'] == '.rdata'; tc = e['tc']
    if tc == 'T': return ('void* const' if rd else 'void*'), '%s[%d]' % (e['name'], e['n'])
    if tc in ('X', 'A'):
        isconst = e['array_const'] if 'array_const' in e else rd
        return (('const ' if isconst else '') + e['type']), '%s[%d]' % (e['name'], e['n'])
    if e.get('simd'): return e['type'], e['name']
    if 'scalar_const' in e:
        return (('const ' if e['scalar_const'] else '') + e['type']), e['name']
    ty = ('%s const' % e['type']) if e.get('ptr') and rd else (('const ' + e['type']) if rd else e['type'])
    return ty, e['name']


def render_tab(e, ents, starts):
    """initializer of a table entry; pointer cells whose target lies inside a present generated global become intra-object references (&DAT_x + off),
    the others (and 'px' = forced extern, negative control) extern "C" M3F_/M3D_ names.  -> (init, extern decls {tv: decl}, host entries)"""
    ext = {}; hosts = []; cells = []
    for d in e['elems']:
        if d[0] == 'z': cells.append('0')
        elif d[0] == 'i': cells.append(fmt('H', struct.pack('<I', d[1])))
        else:
            tv = d[1]; h = None
            if d[0] == 'p':
                j = bisect.bisect_right(starts, tv) - 1
                if j >= 0 and ents[j]['va'] <= tv < ents[j]['va'] + ents[j]['size']: h = ents[j]
            if h is not None:
                off = tv - h['va']; hosts.append(h); RENDER_STAT['intra'] += 1
                cells.append('(void*)&%s' % h['name'] if off == 0 else '(void*)((char*)&%s + %d)' % (h['name'], off))
            else:
                code = TLO <= tv < THI; RENDER_STAT['extern'] += 1
                ext[tv] = 'extern "C" void M3F_%08x(void);' % tv if code else 'extern "C" char M3D_%08x;' % tv
                cells.append('(void*)&%s_%08x' % ('M3F' if code else 'M3D', tv))
    if e['tc'] == 'T': return '{%s}' % ', '.join(cells), ext, hosts
    p = len(e['pat']); return '{%s}' % ', '.join('{%s}' % ', '.join(cells[r * p:(r + 1) * p]) for r in range(len(cells) // p)), ext, hosts


def cpp(entries):
    L = ['// M3 phase 1: generated DAT_ globals (gen_m3.py). Do not edit.']
    for section in sorted({e['section'] for e in entries if e.get('file_backed')}):
        if section not in ('.data', '.rdata'): raise ValueError('unsupported file-backed section')
        L.append('#pragma section("%s", read%s)' % (section, ', write' if section == '.data' else ''))
    cents = [e for e in entries if e['tc'] == 'Y']
    rents = [e for e in entries if e['tc'] == 'R']
    gents = [e for e in entries if e['tc'] == 'W']; entries = [e for e in entries if e['tc'] not in ('W', 'R', 'Y')]
    ents = sorted(entries, key=lambda x: x['va']); starts = [x['va'] for x in ents]
    ext = {}; hostdecl = {}; defs = []; RENDER_STAT.clear()
    if cents:
        sys.path.insert(0, os.path.join(RN, 'm3', 'phase2')); import cost245_records
        L += ['#include <stddef.h>', cost245_records.STRUCT]
        defs += [cost245_records.render_entry(e, ext, sys.modules[__name__]) for e in cents]
    for e in entries:
        if e.get('ptr'):
            tv = e['ptr']['target']; ext[tv] = 'extern "C" void M3F_%08x(void);' % tv if e['ptr']['kind'] == 'code' else 'extern "C" char M3D_%08x;' % tv
    if any(e.get('simd') for e in entries): L.append('namespace fnv_00cd9d10 { struct __declspec(intrin_type) __declspec(align(16)) __m128 { float x,y,z,w; }; }')
    if any(e.get('point3') for e in entries): L.append('namespace fnv_005c25f0 { class NiPoint3 { public: float x, y, z; }; }')
    for e in entries:
        ty, nm = tyname(e)
        if e['tc'] in ('T', 'X'):
            init, x, hs = render_tab(e, ents, starts); ext.update(x)
            if any('scalar_const' in h or 'array_const' in h or h.get('point3') or h.get('simd') for h in hs):
                raise ValueError('namespaced explicit object used as a table host')
            for h in hs: hostdecl[h['va']] = h
        else: init = e['init']
        allocation = '__declspec(allocate("%s")) ' % e['section'] if e.get('file_backed') else ''
        definition = '%s%s%s %s = %s;' % ('extern ' if e['section'] == '.rdata' or e.get('scalar_const') else '', allocation, ty, nm, init)
        if 'scalar_const' in e: definition = 'namespace %s { %s }' % (e['ns'], definition)
        if 'array_const' in e: definition = 'namespace %s { %s }' % (e['ns'], definition)
        if e.get('point3') or e.get('simd'): definition = 'namespace %s { %s }' % (e['ns'], definition)
        defs.append(definition)
    for pat in sorted({e['pat'] for e in entries if e['tc'] == 'X'}): L.append('struct M3R_%s { %s };' % (pat, ' '.join('%s f%d;' % ('void*' if c == 'P' else 'int', i) for i, c in enumerate(pat))))
    gdef = {}; gstruct = []
    for e in gents:
        sd, ini = g_render(e, ext); gstruct.append(sd)
        allocation = '__declspec(allocate("%s")) ' % e['section'] if e.get('file_backed') else ''
        gdef.setdefault(e['ns'], []).append('%s%sstruct M3S_%08x %s = %s;' % ('extern const ' if e['section'] == '.rdata' else '', allocation, e['va'], e['name'], ini))
    if rents:
        import b8_records
        record_structs = set()
        for e in rents:
            sd, definition = b8_records.render_entry(e, ext)
            record_structs.add(sd); defs.append(definition)
        L += sorted(record_structs)
    L += [ext[k] for k in sorted(ext)]
    for va in sorted(hostdecl):
        ty, nm = tyname(hostdecl[va]); L.append('extern %s %s;' % (ty, nm))
    if gstruct: L += ['#pragma pack(push, 1)'] + gstruct + ['#pragma pack(pop)']
    for ns in sorted(gdef):
        if ns: defs += ['namespace %s {' % ns] + gdef[ns] + ['}']
        else: defs += gdef[ns]
    return '\n'.join(L + defs) + '\n'


def obj_path(k): return splice.OBJ if k == 0 else splice.objpath(splice.OBJ, k)


def compile_obj(entries):
    """compile every object group (entry['obj']) with the unit compiler; objects in parallel. -> None (raises on failure)"""
    import glob
    for f in glob.glob(os.path.join(GEN, 'm3_data_*.obj')): os.remove(f)
    groups = collections.defaultdict(list)
    for e in entries: groups[e.get('obj', 0)].append(e)
    procs = []
    for k in sorted(groups): procs.append((k, compile_one(groups[k], k)))
    for k, p in procs:
        out, err = p.communicate()
        if p.returncode or not os.path.exists(obj_path(k)): raise SystemExit('m3 compile failed (object %d):\n' % k + out[-2000:] + err[-2000:])


def compile_one(entries, k):
    import compile_units_v3 as CU
    from pathlib import Path
    tc = CU.find_toolchains()['sp1']
    assert tc.get('ok'), tc
    vc = Path(tc['vc']); env = CU.make_env(vc, Path(tc['sdk']) if tc['sdk'] != 'None' else None)
    tmp = os.path.join(GEN, 'tmp'); os.makedirs(tmp, exist_ok=True); env['TMP'] = env['TEMP'] = tmp
    src = os.path.join(GEN, 'm3_data.cpp' if k == 0 else 'm3_data_%d.cpp' % k); open(src, 'w').write(cpp(entries))
    if os.path.exists(obj_path(k)): os.remove(obj_path(k))
    tk = os.path.join(tmp, str(k)); os.makedirs(tk, exist_ok=True); env['TMP'] = env['TEMP'] = tk
    return subprocess.Popen([str(vc / 'bin' / 'cl.exe'), '/c', '/nologo', '/MT', '/Od', '/Oy-', '/GS', '/EHsc', '/Gy', '/I' + os.path.join(PROJ, 'fnv_decomp', 'include'),
                             src, '/Fo' + obj_path(k)], cwd=GEN, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors='replace', stdin=subprocess.DEVNULL)


def check_ptr(e, data, rel):
    """pointer entry: relocation offsets == the original .reloc sites inside [va, va+size), each DIR32 with a resolvable target, addend bytes == reference minus target,
    target VA + addend == the reference value. -> reason string or None"""
    sites = sorted(f - e['va'] for f in ORIG_SITES if e['va'] <= f < e['va'] + e['size'])
    if [r[0] for r in rel] != sites: return 'reloc offsets %s != original .reloc sites %s' % ([r[0] for r in rel], sites)
    refv = struct.unpack('<I', bytes.fromhex(e['ref']))[0]
    for off, nm, add in rel:
        tv = splice.resolve(nm)
        if tv is None: return 'unresolvable target %s' % nm
        if (tv + add) & 0xffffffff != refv: return 'target %x + addend %d != reference value %x' % (tv, add, refv)
        if int.from_bytes(data[off:off + 4], 'little') != (refv - tv) & 0xffffffff: return 'addend bytes %s != reference minus target' % data[off:off + 4].hex()
        if tv != e['ptr']['target'] or add != e['ptr']['addend']: return 'target/addend differ from the manifest entry'
    return None


def check_elems(e, data, rel, tab):
    """element-wise self-check of arrays / tables against the reference. -> reason or None"""
    ref_ = bytes.fromhex(e['ref'])
    if e['tc'] == 'A':
        if rel: return 'array has relocation'
        esz = TYPES[e['et']][1]
        for i in range(0, e['size'], esz):
            if data[i:i + esz] != ref_[i:i + esz]: return 'element %d (va %08x): bytes %s != ref %s' % (i // esz, e['va'] + i, data[i:i + esz].hex(), ref_[i:i + esz].hex())
        return None
    sites = sorted(f - e['va'] for f in ORIG_SITES if e['va'] <= f < e['va'] + e['size'])
    if [r[0] for r in rel] != sites: return 'reloc sites %s != original .reloc sites %s' % ([r[0] for r in rel][:8], sites[:8])
    rm = {off: (nm, add) for off, nm, add in rel}
    for i in range(0, e['size'], 4):
        refv = struct.unpack('<I', ref_[i:i + 4])[0]
        if i in rm:
            nm, add = rm[i]; tv = splice.resolve(nm, tab)
            if tv is None: return 'element %d: unresolvable target %s' % (i // 4, nm)
            if (tv + add) & 0xffffffff != refv: return 'element %d: target %x + addend %d != reference value %x' % (i // 4, tv, add, refv)
            if int.from_bytes(data[i:i + 4], 'little') != (refv - tv) & 0xffffffff: return 'element %d: addend bytes %s' % (i // 4, data[i:i + 4].hex())
        elif data[i:i + 4] != ref_[i:i + 4]: return 'element %d (va %08x): bytes %s != ref %s' % (i // 4, e['va'] + i, data[i:i + 4].hex(), ref_[i:i + 4].hex())
    return None


def check(entries):
    from compare import Coff
    bad = {}; cs = {}; symmap = {}
    for k in sorted({e.get('obj', 0) for e in entries}):
        c = cs[k] = Coff(obj_path(k))
        if any(s['name'].startswith('.CRT$XC') for s in c.sections[1:] if s) or any(s['name'].startswith(('??__E', '$E')) for s in c.symbols.values()):
            raise SystemExit('dynamic initializer in the m3 object %d' % k)
        for sy in c.symbols.values():
            m = splice.SYM_RE.match(sy['name'])
            if m and sy['section'] > 0: symmap[int(m.group(1), 16)] = sy['name']
    for e in entries:
        if e.get('sym') is None: e['sym'] = symmap.get(e['va'])
    tab = splice.name_table([e for e in entries if e.get('sym')])
    for e in entries:
        c = cs[e.get('obj', 0)]
        if ANYNEG and e.get('negctl'): continue
        if not e.get('sym'): bad[e['name']] = 'symbol not defined in the object'; continue
        try: data, rel, sname, fl, st = splice.slice_entry(c, e)
        except Exception as ex: bad[e['name']] = 'symbol: %s' % ex; continue
        if st != 2: bad[e['name']] = 'storage %d' % st
        elif sname != e['section']: bad[e['name']] = 'section %s != %s' % (sname, e['section'])
        elif len(data) != e['size']: bad[e['name']] = 'size %d != %d' % (len(data), e['size'])
        elif e['tc'] == 'W':
            r = check_g(e, data, rel, tab)
            if r: bad[e['name']] = r
        elif e['tc'] in ('A', 'T', 'X', 'R', 'Y'):
            r = check_elems(e, data, rel, tab)
            if r: bad[e['name']] = r
        elif e.get('ptr'):
            r = check_ptr(e, data, rel)
            if r: bad[e['name']] = r
        elif rel: bad[e['name']] = 'has relocation'
        elif data.hex() != e['ref']: bad[e['name']] = 'bytes %s != ref %s' % (data.hex(), e['ref'])
    return bad


def partition(entries, max_relocs=30000, max_entries=2500):
    """batch 7: the first 1,948 (batch 4) entries stay in object 0 (compiled exactly as before); the generic objects go to objects 1..n (<= max_relocs relocations and max_entries entries each, one COFF
    section holds at most 65535 relocations)"""
    k = 1; nr = 0; ne = 0
    for e in entries:
        if e['tc'] != 'W': e['obj'] = 0; continue
        r = len(e['fields'])
        if ne and (nr + r > max_relocs or ne >= max_entries): k += 1; nr = 0; ne = 0
        e['obj'] = k; nr += r; ne += 1


def main():
    if '--select-batch2' in sys.argv: sel = select(True); print('wrote', BATCH2, len(sel)); return
    if '--select-batch4' in sys.argv:
        new, why = select_batch4(); b3 = json.load(open(BATCH3))['entries']
        kinds = collections.Counter(('string' if e['et'] == 'D' else 'array') if e['tc'] == 'A' else {'T': 'ptrtable', 'X': 'mixed'}[e['tc']] for e in new)
        nb = collections.Counter(); 
        for e in new: nb[('string' if e.get('et') == 'D' else 'array') if e['tc'] == 'A' else {'T': 'ptrtable', 'X': 'mixed'}[e['tc']]] += e['size']
        print('batch4 new entries', len(new), dict(kinds), 'bytes', dict(nb)); print('why', dict(why))
        json.dump(dict(note='frozen batch4 selection (gen_m3.py --select-batch4): batch3 entries first, then %d arrays/strings/pointer tables/mixed tables %s; bytes %s; skipped: %s' % (len(new), dict(kinds), dict(nb), dict(why)), entries=b3 + new), open(BATCH4, 'w'), indent=0)
        return
    if '--select-batch3' in sys.argv: sel = select(False, True); print('wrote', BATCH3, len(sel)); return
    frozen = bool(os.environ.get('FNV_M3_SEL')) and '--select' not in sys.argv
    if frozen and not os.path.isfile(SELF):
        raise SystemExit('configured M3 selection is missing: %s' % SELF)
    if '--select' in sys.argv or not os.path.exists(SELF): sel = select()
    else: sel = json.load(open(SELF))['entries']
    entries = build_entries(sel)
    for e in entries:
        if e['tc'] in ('T', 'X'): set_fields(e)
    partition(entries)
    if NEGP2AV:
        candidates = [x for x in entries if x['tc'] == 'A' and x.get('ns') and 'array_const' in x and x.get('sym') and x['et'] == 'E']
        if not candidates: raise ValueError('p2av requires an explicit namespaced unsigned char array')
        e = candidates[0]; raw = bytes.fromhex(e['ref']); value = (raw[0] + 1) & 255
        e['els'][0] = fmt('E', bytes([value])); e['init'] = '{%s}' % ', '.join(e['els']); e['negctl'] = True
        print('NEGATIVE CONTROL (p2 array value): VA %08x symbol %s element 0 changed from %02x to %02x' % (e['va'], e['sym'], raw[0], value))
    if NEGP2BW: mutate_bsaudio_tail(entries)
    if NEGP2CW: mutate_bulk_tail(entries)
    if NEGP2WP:
        candidates = [x for x in entries if x['tc'] == 'W' and x['va'] in (0x011a7e40, 0x011acefc) and x.get('tgts')]
        if not candidates: raise ValueError('p2wp requires a reviewed split tail with pointers')
        e = candidates[0]; old = e['tgts'][0]; code = TLO <= old < THI
        targets = [v for x in entries for v in x.get('tgts', []) if v != old and (TLO <= v < THI) == code]
        if not targets: raise ValueError('p2wp requires an alternative same-kind target')
        k = next(i for i, (c, n) in enumerate(e['runs']) if c == 'P' and any(flag for flag, v in e['items'][i]))
        j = next(i for i, (flag, v) in enumerate(e['items'][k]) if flag)
        e['items'][k][j] = (True, targets[0]); g_fields(e); e['negctl'] = True
        print('NEGATIVE CONTROL (p2 tail pointer): VA %08x symbol %s run %d cell %d now points to %08x instead of %08x' % (e['va'], e['name'], k, j, targets[0], old))
    if NEGP2SV:
        candidates = [x for x in entries if x.get('ns') and 'scalar_const' in x and x.get('sym') and x['tc'] in ('M', 'N')]
        if not candidates: raise ValueError('p2sv requires an explicit namespaced floating scalar')
        e = next((x for x in candidates if bytes.fromhex(x['ref']) != struct.pack('<f' if x['tc'] == 'M' else '<d', 1.0)), None)
        if e is None: raise ValueError('p2sv requires a scalar different from 1.0')
        e['init'] = '1.0f' if e['tc'] == 'M' else '1.0'; e['negctl'] = True
        print('NEGATIVE CONTROL (p2 scalar value): VA %08x symbol %s initializer changed to %s (reference bytes %s)' % (e['va'], e['sym'], e['init'], e['ref']))
    if NEG8V:
        e = next(x for x in entries if x.get('batch') == 8 and x['tc'] in ('H', 'I', 'J', 'K', 'F', 'G', 'D', 'E', 'C'))
        raw = bytes.fromhex(e['ref']); value = (int.from_bytes(raw, 'little') + 1) % (1 << (8 * len(raw)))
        # Keep a writable control file-backed when the deliberate +1 wraps.
        if value == 0: value = 1
        e['init'] = fmt(e['tc'], value.to_bytes(len(raw), 'little')); e['negctl'] = True
        print('NEGATIVE CONTROL (b8 value): %s initializer changed to %s (reference bytes %s)' % (e['name'], e['init'], raw.hex()))
    if NEG8P:
        candidates = [x for x in entries if x.get('ptr')]
        if not candidates: raise ValueError('b8p requires a pointer definition')
        e = next((x for x in candidates if x.get('batch') == 8), None)
        if e is None: e = candidates[0]
        old = e['ptr']['target']; code = e['ptr']['kind'] == 'code'
        targets = [x['ptr']['target'] for x in candidates] + [t for x in entries for t in x.get('tgts', [])]
        alt = next(t for t in targets if (TLO <= t < THI) == code and t != old)
        kind = 'M3F' if code else 'M3D'
        e['ptr']['target'] = alt; e['init'] = '(void*)&%s_%08x' % (kind, alt)
        e['fields'] = [[0, '_%s_%08x' % (kind, alt), 0]]; e['negctl'] = True
        print('NEGATIVE CONTROL (b8 pointer): %s now points to %08x instead of %08x' % (e['name'], alt, old))
    if NEG9V:
        e = next(x for x in sorted((y for y in entries if y['tc'] == 'W' and y.get('batch') == 9 and any(c == 'U' for c, n in y['runs'])), key=lambda y: not str(y.get('kind')).startswith('b9s2'))); k = next(i for i, (c, n) in enumerate(e['runs']) if c == 'U')
        raw = e['items'][k][0]; v = (struct.unpack('<I', raw)[0] + 1) & 0xffffffff; e['items'][k][0] = struct.pack('<I', v); e['negctl'] = True
        print('NEGATIVE CONTROL (b9 value): %s run %d element 0 is now %08x (reference bytes %s)' % (e['name'], k, v, raw.hex()))
    if NEG9P:
        gs = [x for x in entries if x['tc'] == 'W' and x['tgts']]; e = next(x for x in sorted((y for y in gs if y.get('batch') == 9), key=lambda y: not str(y.get('kind')).startswith('b9s2'))); t0 = e['tgts'][0]; code0 = TLO <= t0 < THI
        alt = next(t for x in gs for t in x['tgts'] if (TLO <= t < THI) == code0 and t != t0)
        k = next(i for i, (c, n) in enumerate(e['runs']) if c == 'P' and any(s for s, v in e['items'][i])); j = next(i for i, (s, v) in enumerate(e['items'][k]) if s)
        e['items'][k][j] = (True, alt); g_fields(e); e['negctl'] = True
        print('NEGATIVE CONTROL (b9 pointer): %s run %d cell %d now points to %08x instead of %08x' % (e['name'], k, j, alt, t0))
    if NEG7V:
        e = next(x for x in entries if x['tc'] == 'W' and x['kind'] not in ('tail-sec', 'tail-rw') and any(c == 'U' for c, n in x['runs'])); k = next(i for i, (c, n) in enumerate(e['runs']) if c == 'U')
        raw = e['items'][k][0]; v = (struct.unpack('<I', raw)[0] + 1) & 0xffffffff; e['items'][k][0] = struct.pack('<I', v); e['negctl'] = True
        print('NEGATIVE CONTROL (b7 value): %s run %d element 0 is now %08x (reference bytes %s)' % (e['name'], k, v, raw.hex()))
    if NEG7P:
        gs = [x for x in entries if x['tc'] == 'W' and x['kind'] not in ('tail-sec', 'tail-rw') and x['tgts']]; e = gs[0]; t0 = e['tgts'][0]; code0 = TLO <= t0 < THI
        alt = next(t for x in gs for t in x['tgts'] if (TLO <= t < THI) == code0 and t != t0)
        k = next(i for i, (c, n) in enumerate(e['runs']) if c == 'P' and any(s for s, v in e['items'][i])); j = next(i for i, (s, v) in enumerate(e['items'][k]) if s)
        e['items'][k][j] = (True, alt); g_fields(e); e['negctl'] = True
        print('NEGATIVE CONTROL (b7 pointer): %s run %d cell %d now points to %08x instead of %08x' % (e['name'], k, j, alt, t0))
    if NEG4V:
        e = next(x for x in entries if x['tc'] == 'A' and x['et'] in 'HIJK'); raw = bytes.fromhex(e['ref'])[:4]
        v = (struct.unpack('<I', raw)[0] + 1) & 0xffffffff; e['els'][0] = fmt(e['et'], struct.pack('<I', v)); e['init'] = '{%s}' % ', '.join(e['els']); e['negctl'] = True
        print('NEGATIVE CONTROL (array value): %s element 0 is now %s (reference bytes %s)' % (e['name'], e['els'][0], raw.hex()))
    if NEG4P:
        tg = [x for x in entries if x['tc'] == 'T' and any(d[0] == 'p' for d in x['elems'])]
        e = tg[0]; i = next(j for j, d in enumerate(e['elems']) if d[0] == 'p'); code0 = TLO <= e['elems'][i][1] < THI
        alt = next(d[1] for x in tg for d in x['elems'] if d[0] == 'p' and (TLO <= d[1] < THI) == code0 and d[1] != e['elems'][i][1])
        print('NEGATIVE CONTROL (table pointer): %s element %d now points to %08x instead of %08x' % (e['name'], i, alt, e['elems'][i][1]))
        e['elems'][i] = ('px', alt); set_fields(e); e['negctl'] = True
    if NEGP:
        pe = [e for e in entries if e.get('ptr')]; assert len(pe) > 1, 'FNV_M3_NEGCTL=ptr needs pointer entries'
        e = pe[0]; alt = next(x for x in pe[1:] if x['ptr']['kind'] == e['ptr']['kind'] and x['ptr']['target'] != e['ptr']['target'])
        tv = alt['ptr']['target']; k = 'M3F' if e['ptr']['kind'] == 'code' else 'M3D'
        e['ptr']['target'] = tv; e['init'] = '(void*)&%s_%08x' % (k, tv); e['fields'] = [[0, '_%s_%08x' % (k, tv), 0]]; e['negctl'] = True
        print('NEGATIVE CONTROL (pointer): %s now points to %08x instead of the reference value %s' % (e['name'], tv, e['ref']))
    if NEG and entries:
        e = entries[0]; assert e['tc'] in ('H', 'I')
        v = struct.unpack('<I', bytes.fromhex(e['ref']))[0]
        e['init'] = str(struct.unpack('<i', bytes.fromhex(e['ref']))[0] + 1) if e['tc'] == 'H' else '0x%08xu' % ((v + 1) & 0xffffffff)
        e['negctl'] = True
        print('NEGATIVE CONTROL: %s initializer changed to %s (reference bytes %s)' % (e['name'], e['init'], e['ref']))
    dropped = {}
    for it in range(8):
        bad = compile_obj(entries) or check(entries)
        if not bad: break
        if frozen:
            raise SystemExit('frozen M3 selection failed compiler/COFF checks; refusing to prune: %s' % bad)
        dropped.update(bad); entries = [e for e in entries if e['name'] not in bad]
    else: raise SystemExit('prune loop did not converge')
    json.dump(dict(entries=[{k: v for k, v in e.items() if k not in ('elems', 'els', 'init', 'items')} if e['tc'] in ('A', 'T', 'X', 'W', 'R', 'Y') else e for e in entries], negctl=ANYNEG, objs=sorted({e.get('obj', 0) for e in entries})), open(splice.MANIFEST, 'w'), indent=0)
    json.dump([[e['va'], e['size']] for e in entries], open(os.path.join(GEN, 'skip_ranges.json'), 'w'))
    tot = collections.Counter()
    for e in entries: tot[e['section']] += e['size']
    log = dict(selected=len(sel), kept=len(entries), dropped=dropped, bytes_by_section=dict(tot), by_type=dict(collections.Counter(e['type'] for e in entries)), by_type_section=dict(collections.Counter('%s/%s' % (e['section'], e['type']) for e in entries)), selection=os.path.basename(SELF), negctl=ANYNEG, kinds=dict(collections.Counter(e.get('kind', 'ptr' if e.get('ptr') else 'scalar') for e in entries)), kind_bytes=dict(sum((collections.Counter({e.get('kind', 'ptr' if e.get('ptr') else 'scalar'): e['size']}) for e in entries), collections.Counter())), table_pointer_fields=sum(len(e.get('fields', [])) for e in entries if e['tc'] in ('T', 'X')), g_pointer_fields=sum(len(e.get('fields', [])) for e in entries if e['tc'] == 'W'), objs=len({e.get('obj', 0) for e in entries}), kind_relocs=dict(sum((collections.Counter({e.get('kind', ''): len(e.get('fields', []))}) for e in entries if e['tc'] == 'W'), collections.Counter())), table_cells=dict(RENDER_STAT), pointers=sum(1 for e in entries if e.get('ptr')), pointer_targets=dict(collections.Counter(e['ptr']['kind'] for e in entries if e.get('ptr'))))
    json.dump(log, open(os.path.join(GEN, 'm3_gen.log.json'), 'w'), indent=1)
    print('m3 globals: selected %d kept %d dropped %d bytes %s' % (len(sel), len(entries), len(dropped), dict(tot)))
    for k, v in dropped.items(): print('  dropped', k, v)


if __name__ == '__main__': main()
