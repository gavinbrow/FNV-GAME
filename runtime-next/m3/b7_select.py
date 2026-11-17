r"""M3 batch 7 selection: python -I b7_select.py [--kinds ns,scalar,tail-m3,tail-dv1,tail-prod,tail-sec] [--out batch7_selection.json]
Reads (frozen inputs): batch4_selection.json, inventory\b7_dv1_ranges.json (data-v1 pieces selected by batch 6), inventory\b7_produced.json (data-v1 produced ranges of the default build),
units.json (declared names), inventory\dat_globals.json (source definitions), data-v3 symbolic.json / out\manifest.json / out\data_labels.json (fields, chunks, labels), the reference image.
The uncovered initialised bytes of .data/.rdata (not in a batch 4 object, not a batch 6 data-v1 piece, not a data-v1 produced range) are cut into intervals at every declared name (DAT_/PTR_/OFF_...).
  * an interval that starts at a declared name is taken only for 'ns' (declared only inside one namespace, one consistent type) and 'scalar' (global scalar type: a table typed as a scalar);
    the object is named DAT_<va> (inside the namespace for 'ns') and its first run has the declared type when it is int/unsigned/long/float/double
  * an interval that starts after a covered range is a tail ('tail-m3' after a generated global, 'tail-dv1' after a data-v1 piece, 'tail-prod' after a data-v1 produced range): M3_<va>
Each interval is cut at data-v3 chunk boundaries, trimmed so that no data-v3 field straddles an end, and split around value-rule fields / unusable relocation windows (holes stay uncovered).
Every piece becomes one 'W' entry: [va, size, run descriptors]; pieces without non-zero bytes are dropped (a zero-only object would land in .bss)."""
import os, sys, re, json, struct, bisect, collections
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gen_m3 as G
from gen_m3 import SEC, sec_of, ORIG_SET, ORIG_SITES, TYPES, refbytes, PROJ, RN, layout

ap = sys.argv[1:]
KINDS = None; OUT = os.path.join(HERE, 'batch7_selection.json')
if '--kinds' in ap: KINDS = set(ap[ap.index('--kinds') + 1].split(','))
if '--out' in ap: OUT = os.path.join(HERE, ap[ap.index('--out') + 1])
DAT_RE = G.DAT_RE; ADDR_ANY = re.compile(r'(?:DAT|PTR|UNK|OFF|BYTE|WORD|DWORD)_([0-9a-f]{8})')
units = json.load(open(os.path.join(PROJ, 'fnv_decomp', 'build', 'units.json')))['units']
forms = collections.defaultdict(lambda: collections.defaultdict(set)); full = collections.defaultdict(set); bnd = set()
for u in units:
    for k in u.get('symbols', {}):
        for m in ADDR_ANY.finditer(k): bnd.add(int(m.group(1), 16))
        m = DAT_RE.match(k)
        if m:
            va = int(m.group(1), 16); forms[va][m.group(2)].add(m.group(3)[:-1]); full[va].add(k)
bnds = sorted(bnd)
inv = {int(g['addr'], 16): g for g in json.load(open(os.path.join(HERE, 'inventory', 'dat_globals.json')))['globals']}
sj = json.load(open(os.path.join(RN, 'data-v3', 'symbolic.json')))
drel = ORIG_SET; fldall = {SEC[r[0]]['va'] + r[1] for r in sj['fields']} | drel; vr = fldall - drel; fldS = sorted(fldall)
labels = sorted(int(v['va']) for v in json.load(open(os.path.join(RN, 'data-v3', 'out', 'data_labels.json')))['data_labels'].values())
chunks = sorted((m['va'], m['va'] + m['size']) for m in json.load(open(os.path.join(RN, 'data-v3', 'out', 'manifest.json'))) if m['section'] in ('.data', '.rdata'))
chunk_starts = [a for a, b in chunks]
b4 = json.load(open(os.path.join(HERE, 'batch4_selection.json')))['entries']
b4rng = [(e['va'], e['va'] + (4 if e['tc'] == 'P' else (TYPES[e['tc']][1] if e['tc'] in TYPES else e['size']))) for e in b4]
dv1 = [(a, a + n) for a, n in json.load(open(os.path.join(HERE, 'inventory', 'b7_dv1_ranges.json')))]
prod = [(a, a + n) for a, n in json.load(open(os.path.join(HERE, 'inventory', 'b7_produced.json')))]
bss_hi = SEC['.data']['va'] + SEC['.data']['vs']; bss_lo = SEC['.data']['va'] + SEC['.data']['raw']


def validtarget(tv):
    tn = sec_of(tv)
    return tn in ('.text', '.rdata', '.data', 'CONST', '.tls') or bss_lo <= tv < bss_hi


def fld_near(lo, hi):     # fields f with lo <= f < hi
    i = bisect.bisect_left(fldS, lo); return fldS[i:bisect.bisect_left(fldS, hi)]


def lab_in(lo, hi):
    i = bisect.bisect_right(labels, lo); return i < len(labels) and labels[i] < hi


# ranges that layout-v2\make_image.py rewrites itself after the data chunks are assembled (re-based import directory + IAT, TLS directory): bytes there never come from an m3 object
REWRITTEN = [(0xfdf000, 0xfdf000 + 1188), (0x118062c, 0x118062c + 6688), (0x110147c, 0x110147c + 0x18)]
tag = {}
for n in ('.data', '.rdata'):
    s = SEC[n]; lo = s['va']; hi = lo + s['raw']; arr = bytearray(hi - lo)
    for t, rs in ((4, REWRITTEN), (3, prod), (2, dv1), (1, b4rng)):
        for a, b in rs:
            if lo <= a < hi: arr[a - lo:min(b, hi) - lo] = bytes([t]) * (min(b, hi) - a)
    tag[n] = arr
TN = {0: 'tail-sec', 1: 'tail-m3', 2: 'tail-dv1', 3: 'tail-prod', 4: 'tail-rw'}


def decl_class(x):
    g = inv.get(x)
    if g and g['defs']: return None, 'source-def'
    if x not in forms: return None, 'declared-other-name'
    allt = set().union(*forms[x].values())
    if len(allt) != 1: return None, 'multi-type'
    tc = next(iter(allt))[:-1]
    if '' in forms[x]:
        return (('scalar', '', tc), None) if tc in TYPES else (None, 'global-non-scalar')
    nss = sorted(forms[x])
    if nss[0].count('@') != 1: return None, 'ns-depth'
    return ('ns', nss[0][1:], tc), None


def pieces(x, y):
    """[x, y) -> [(a, b)] cut at data-v3 chunk boundaries, trimmed at straddling fields, split around holes. -> (pieces, hole bytes)"""
    out = []; holes = 0
    cuts = [x] + [c for c in chunk_starts[bisect.bisect_right(chunk_starts, x):] if c < y] + [y]
    for a, b in zip(cuts, cuts[1:]):
        while True:      # a data-v3 field straddling an end: trim
            ch = False
            for f in fld_near(a - 3, a):
                if f < a < f + 4: holes += f + 4 - a; a = f + 4; ch = True
            for f in fld_near(b - 3, b):
                if f < b < f + 4: holes += b - f; b = f; ch = True
            if not ch or b <= a: break
        if b <= a: continue
        hs = []
        for f in fld_near(a, b):
            if f in vr: hs.append(f)
            elif f in drel:
                v = struct.unpack('<I', refbytes(f, 4))[0]
                if not validtarget(v) or lab_in(f, f + 4) or any(g in fldall for g in range(f + 1, f + 4)): hs.append(f)
        cur = a
        for h in sorted(hs):
            if h > cur: out.append((cur, h))
            holes += 4; cur = max(cur, h + 4)
        if cur < b: out.append((cur, b))
    return out, holes


entries = []; stat_bytes = collections.Counter(); stat_n = collections.Counter(); skipped = collections.Counter(); skipped_n = collections.Counter()
holes_total = 0; zero_only = 0; cut_runs = 0; head_typed = collections.Counter()


def emit(a, b, kind, ns, named, head, decl):
    global zero_only, cut_runs
    raw = refbytes(a, b - a)
    if not any(raw): zero_only += len(raw); return
    runs = layout(a, raw, head if named else None, labels)
    if len(runs) > G.MAXRUNS:        # too many members for one struct: cut at a run boundary and lay both halves out again
        k = 0; nb = 0
        for cls, cnt in runs[:G.MAXRUNS]: nb += cnt * G.RUN_SZ[cls]
        cut_runs += 1; emit(a, a + nb, kind, ns, named, head, decl); emit(a + nb, b, kind, ns, False, None, decl); return
    al = min(a & -a, 8 if (named and head == 'N') else 4)
    e = dict(va=a, tc='W', size=b - a, kind=kind, ns=ns, named=bool(named), head=head if named else None, runs=runs, align=al)
    if decl: e['decl'] = decl
    entries.append(e); stat_bytes[kind] += b - a; stat_n[kind] += 1
    if named and head and runs and runs[0][0] in ('H', 'I', 'J', 'K', 'M', 'N') and runs[0][1] == 1: head_typed[kind + '/' + head] += 1


for n in ('.data', '.rdata'):
    s = SEC[n]; lo = s['va']; arr = bytes(tag[n]); off = s['off']
    for m in re.finditer(b'\x00+', arr):
        ra, rb = lo + m.start(), lo + m.end(); prev = arr[m.start() - 1] if m.start() else 0
        cuts = [ra] + [v for v in bnds[bisect.bisect_right(bnds, ra):bisect.bisect_left(bnds, rb)]] + [rb]
        for k in range(len(cuts) - 1):
            x, y = cuts[k], cuts[k + 1]; named = False; head = None; ns = ''; decl = None
            if x in bnd:
                dc, why = decl_class(x)
                if dc is None:
                    nz = sum(1 for q in refbytes(x, y - x) if q); skipped['declared: ' + why] += nz; skipped_n['declared: ' + why] += 1; continue
                kind, ns, tc = dc; named = True; head = tc if tc in ('H', 'I', 'J', 'K', 'M', 'N') else None
                decl = sorted(full[x])[:3]
            else: kind = TN[prev if x == ra else 0]
            if KINDS is not None and kind not in KINDS: continue
            ps, h = pieces(x, y); holes_total += h
            for j, (a, b) in enumerate(ps):
                emit(a, b, kind, ns, named and a == x, head, decl)

entries.sort(key=lambda e: (e['va']))
tot = sum(e['size'] for e in entries)
note = 'frozen batch7 selection (b7_select.py): batch4 entries first, then %d generic objects (%d B) by kind %s; bytes %s; skipped declared intervals (non-zero bytes) %s; holes %d B; zero-only pieces dropped %d B; kinds filter %s' % (
    len(entries), tot, dict(stat_n), dict(stat_bytes), dict(skipped), holes_total, zero_only, sorted(KINDS) if KINDS else 'all')
json.dump(dict(note=note, entries=b4 + entries), open(OUT, 'w'), indent=0)
print(note); print('skipped intervals', dict(skipped_n)); print('head typed', dict(head_typed), 'run-cut pieces', cut_runs)
