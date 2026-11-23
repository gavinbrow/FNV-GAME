r"""M3 batch 9 (stage 1) selection + inventory.
  python -I b9_select.py --inventory      writes inventory\remaining_20261122.json (what the CURRENT default build still takes from the dump, with b7-rule reasons)
  python -I b9_select.py [--holes k1,k2] [--out batch9_selection.json]
                                           writes the selection = phase2\selection.json (default, untouched) + new 'W' entries for the bytes batch 7 skipped.
Coverage of the default build is frozen in inventory\b9_default_cov.json (taken once from gen\m3_manifest.json + gen\dv1_pieces.json of a default build; --freeze-cov redoes it).
Uncovered = initialised .data/.rdata raw bytes in no M3 object, no data-v1 piece, no builder-rewritten range (import dir + IAT, TLS dir), and not in a frozen data-v1 produced range
('prod-unplaced', stage 2). The uncovered bytes are cut like b7_select.py (at every declared name), then:
  b7 rules   : declared messy names skipped, holes, all-zero pieces dropped
  b9 rules   : declared messy intervals are emitted as unnamed M3_<va> objects (source-def owners are still left alone); holes whose field is an original .reloc site are emitted as pointer cells
               to M3F_/M3D_<target> (any target address resolves through the name); all-zero pieces are emitted file-backed (__declspec(allocate)) so they are not compiled into .bss.
Value-rule fields (data-v3 fields without a .reloc entry) stay holes: the round trip counts every data-v3 field as a relocation the overlay must provide and checks that each one is an original .reloc site."""
import os, sys, re, json, struct, bisect, collections
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gen_m3 as G
from gen_m3 import SEC, sec_of, ORIG_SET, TYPES, refbytes, PROJ, RN, layout

ap = sys.argv[1:]
OUT = os.path.join(HERE, 'batch9_selection.json'); INV = os.path.join(HERE, 'inventory', 'remaining_20261122.json'); COV = os.path.join(HERE, 'inventory', 'b9_default_cov.json')
if '--out' in ap: OUT = os.path.join(HERE, ap[ap.index('--out') + 1])
STAGE2 = '--stage2' in ap
OK_HOLES = {'invalid-target', 'label-inside', 'null-target'}
if STAGE2:
    OUT = os.path.join(HERE, 'batch9s2_selection.json'); OK_HOLES = OK_HOLES | {'value-rule'}
    if '--out' in ap: OUT = os.path.join(HERE, ap[ap.index('--out') + 1])
if '--holes' in ap: OK_HOLES = set(x for x in ap[ap.index('--holes') + 1].split(',') if x)
DAT_RE = G.DAT_RE; ADDR_ANY = re.compile(r'(?:DAT|PTR|UNK|OFF|BYTE|WORD|DWORD)_([0-9a-f]{8})')
J = os.path.join
DEFAULT_SEL = J(HERE, 'phase2', 'selection.json')


def merged(rs):
    out = []
    for a, b in sorted(rs):
        if out and a <= out[-1][1]: out[-1][1] = max(out[-1][1], b)
        else: out.append([a, b])
    return out


if '--freeze-cov' in ap or not os.path.exists(COV):
    man = json.load(open(J(HERE, 'gen', 'm3_manifest.json')))['entries']; pcs = json.load(open(J(HERE, 'gen', 'dv1_pieces.json')))['pieces']
    json.dump(dict(note='ranges of the default build (gen\\m3_manifest.json entries, gen\\dv1_pieces.json pieces, all sections), merged',
                   m3=merged([(e['va'], e['va'] + e['size']) for e in man]), dv1=merged([(e['va'], e['va'] + e['size']) for e in pcs])), open(COV, 'w'))
cov = json.load(open(COV)); m3rng = [tuple(x) for x in cov['m3']]; dv1rng = [tuple(x) for x in cov['dv1']]
prodrng = [(a, a + n) for a, n in json.load(open(J(HERE, 'inventory', 'b7_produced.json')))]
BASE_SEL = J(HERE, 'batch9_selection.json')
if STAGE2:      # stage 2: the stage 1 objects count as covered, prod-unplaced ranges are now selectable
    s1 = [e for e in json.load(open(BASE_SEL))['entries'] if e.get('batch') == 9]
    m3rng = m3rng + [(e['va'], e['va'] + e['size']) for e in s1]
    prodrng_all = prodrng; prodrng = []
REWRITTEN = [(0xfdf000, 0xfdf000 + 1188), (0x118062c, 0x118062c + 6688), (0x110147c, 0x110147c + 0x18)]
# ---- declared names, data-v3 fields, labels, chunks (as b7_select.py)
units = json.load(open(J(PROJ, 'fnv_decomp', 'build', 'units.json')))['units']
forms = collections.defaultdict(lambda: collections.defaultdict(set)); full = collections.defaultdict(set); bnd = set()
for u in units:
    for k in u.get('symbols', {}):
        for m in ADDR_ANY.finditer(k): bnd.add(int(m.group(1), 16))
        m = DAT_RE.match(k)
        if m:
            va = int(m.group(1), 16); forms[va][m.group(2)].add(m.group(3)[:-1]); full[va].add(k)
bnds = sorted(bnd)
inv = {int(g['addr'], 16): g for g in json.load(open(J(HERE, 'inventory', 'dat_globals.json')))['globals']}
sj = json.load(open(J(RN, 'data-v3', 'symbolic.json')))
drel = ORIG_SET; fldall = {SEC[r[0]]['va'] + r[1] for r in sj['fields']} | drel; vr = fldall - drel; fldS = sorted(fldall)
labels = sorted(int(v['va']) for v in json.load(open(J(RN, 'data-v3', 'out', 'data_labels.json')))['data_labels'].values())
chunks = sorted((m['va'], m['va'] + m['size']) for m in json.load(open(J(RN, 'data-v3', 'out', 'manifest.json'))) if m['section'] in ('.data', '.rdata'))
chunk_starts = [a for a, b in chunks]
bss_hi = SEC['.data']['va'] + SEC['.data']['vs']; bss_lo = SEC['.data']['va'] + SEC['.data']['raw']
TAGN = {0: 'uncovered', 1: 'm3', 2: 'dv1', 3: 'prod', 4: 'rewritten'}
tag = {}
for n in ('.data', '.rdata'):
    s = SEC[n]; lo = s['va']; hi = lo + s['raw']; arr = bytearray(hi - lo)
    for t, rs in ((3, prodrng), (4, REWRITTEN), (2, dv1rng), (1, m3rng)):      # later paints win: m3 > dv1 > rewritten > prod
        for a, b in rs:
            a2, b2 = max(a, lo), min(b, hi)
            if a2 < b2: arr[a2 - lo:b2 - lo] = bytes([t]) * (b2 - a2)
    tag[n] = arr


def u32(va): return struct.unpack('<I', refbytes(va, 4))[0]


def validtarget(tv):
    tn = sec_of(tv)
    return tn in ('.text', '.rdata', '.data', 'CONST', '.tls') or bss_lo <= tv < bss_hi


def fld_near(lo, hi):
    i = bisect.bisect_left(fldS, lo); return fldS[i:bisect.bisect_left(fldS, hi)]


def lab_in(lo, hi):
    i = bisect.bisect_right(labels, lo); return i < len(labels) and labels[i] < hi


def decl_class(x):
    g = inv.get(x)
    if g and g['defs']: return None, 'source-def'
    if x not in forms: return None, 'declared-other-name'
    allt = set().union(*forms[x].values())
    if len(allt) != 1: return None, 'multi-type'
    tc = next(iter(allt))[:-1]
    if '' in forms[x]: return (('scalar', '', tc), None) if tc in TYPES else (None, 'global-non-scalar')
    nss = sorted(forms[x])
    if nss[0].count('@') != 1: return None, 'ns-depth'
    return ('ns', nss[0][1:], tc), None


def field_hole(f):
    """None when the data-v3 field at f is a plain original relocation cell; else the hole kind"""
    if f in vr: return 'value-rule'
    v = u32(f)
    if v == 0: return 'null-target'
    if not validtarget(v): return 'invalid-target'
    if any(g in fldall for g in range(f + 1, f + 4)): return 'overlapping-field'
    if lab_in(f, f + 4): return 'label-inside'
    return None


def pieces(x, y, ok):
    """[x, y) -> ([(a, b)], [(a, b, kind)]): cut at data-v3 chunk boundaries, trimmed where a data-v3 field straddles an end, split around holes (kinds in `ok` are not holes)"""
    out = []; holes = []
    cuts = [x] + [c for c in chunk_starts[bisect.bisect_right(chunk_starts, x):] if c < y] + [y]
    for a, b in zip(cuts, cuts[1:]):
        while True:
            ch = False
            for f in fld_near(a - 3, a):
                if f < a < f + 4: holes.append((a, f + 4, 'straddle')); a = f + 4; ch = True
            for f in fld_near(b - 3, b):
                if f < b < f + 4: holes.append((f, b, 'straddle')); b = f; ch = True
            if not ch or b <= a: break
        if b <= a: continue
        hs = []
        for f in fld_near(a, b):
            k = field_hole(f)
            if k and k not in ok: hs.append((f, k))
        cur = a
        for h, k in sorted(hs):
            if h > cur: out.append((cur, h))
            holes.append((h, h + 4, k)); cur = max(cur, h + 4)
        if cur < b: out.append((cur, b))
    return out, holes


def process(messy_ok, ok_holes, zero_ok, allow_sd=False):
    """-> [(a, b, disposition, reason, section)] partition of every uncovered byte; disposition 'emit' (piece to turn into a W entry) or 'skip'"""
    res = []
    for n in ('.data', '.rdata'):
        s = SEC[n]; lo = s['va']; arr = bytes(tag[n])
        for m in re.finditer(b'\x00+', arr):
            ra, rb = lo + m.start(), lo + m.end(); prev = arr[m.start() - 1] if m.start() else 0
            cuts = [ra] + [v for v in bnds[bisect.bisect_right(bnds, ra):bisect.bisect_left(bnds, rb)]] + [rb]
            for k in range(len(cuts) - 1):
                x, y = cuts[k], cuts[k + 1]; why = None; tk = {0: 'tail-sec', 1: 'tail-m3', 2: 'tail-dv1', 3: 'tail-prod', 4: 'tail-rw'}[prev if x == ra else 0]
                if x in bnd:
                    dc, why = decl_class(x)
                    if dc is None and ((why == 'source-def' and not allow_sd) or not messy_ok): res.append((x, y, 'skip', 'declared: ' + why, n)); continue
                ps, hs = pieces(x, y, ok_holes)
                for a, b, kind in hs: res.append((a, b, 'skip', 'hole: ' + kind, n))
                for a, b in ps:
                    if not any(refbytes(a, b - a)):
                        if zero_ok: res.append((a, b, 'emit', 'zero-only' if not why else 'zero-only/declared-' + why, n))
                        else: res.append((a, b, 'skip', 'zero-only', n))
                    else: res.append((a, b, 'emit', 'declared-' + why if why else tk + ' (b7-emittable, absent from default)', n))
    res.sort()
    return res


def emit_entries(parts):
    entries = []; stat = collections.Counter(); stat_n = collections.Counter(); cut = [0]

    def emit(a, b, kind, zero):
        raw = refbytes(a, b - a)
        runs = layout(a, raw, None, labels)
        if len(runs) > G.MAXRUNS:
            nb = sum(cnt * G.RUN_SZ[cls] for cls, cnt in runs[:G.MAXRUNS]); cut[0] += 1
            emit(a, a + nb, kind, zero and not any(raw[:nb])); emit(a + nb, b, kind, zero and not any(raw[nb:])); return
        e = dict(va=a, tc='W', size=b - a, kind=kind, ns='', named=False, head=None, runs=runs, align=min(a & -a, 4), batch=9)
        if STAGE2: e['stage'] = 2
        if not any(raw): e['file_backed'] = True        # an all-zero object would be compiled into .bss: allocate it in the file-resident section
        entries.append(e); stat[kind] += b - a; stat_n[kind] += 1
    for a, b, disp, reason, n in parts:
        if disp != 'emit': continue
        kind = ('b9s2-' if STAGE2 else 'b9-') + reason.split('/')[0].split(' ')[0]
        emit(a, b, kind, not any(refbytes(a, b - a)))
    entries.sort(key=lambda e: e['va'])
    return entries, stat, stat_n, cut[0]


def run_ranges(parts, key):
    """merge adjacent parts with the same key -> [(a, b, key, section)]"""
    out = []
    for a, b, disp, reason, n in parts:
        k = key(disp, reason)
        if out and out[-1][1] == a and out[-1][2] == k and out[-1][3] == n: out[-1][1] = b
        else: out.append([a, b, k, n])
    return out


def inventory():
    parts = process(messy_ok=False, ok_holes=set(), zero_ok=False)       # batch 7 rules
    rng = []
    for a, b, k, n in run_ranges(parts, lambda d, r: r):
        raw = refbytes(a, b - a); nz = sum(1 for q in raw if q)
        rng.append(dict(va=a, size=b - a, section=n, bucket='uncovered-nonzero' if nz else 'uncovered-zero', nonzero=nz, zero=b - a - nz, reason=k))
    # prod-unplaced: split by the current produced_ranges.json kind (own rtti / own vtable / own other / library), as phase2\account_ranges.py
    meta = json.load(open(J(RN, 'data-v3', 'out', 'produced_ranges.json')))
    for n in ('.data', '.rdata'):
        s = SEC[n]; lo = s['va']; hi = lo + s['raw']; kinds = bytearray(hi - lo)
        for e in meta:
            if e['tier'] == 'M': continue
            kd = e['kind']; bit = 8 if e['unit'] >= 100000 else 1 if kd.startswith('rtti') else 2 if kd == 'vtable' else 4
            a, b = max(lo, e['va']), min(hi, e['va'] + e['size'])
            for i in range(a - lo, b - lo): kinds[i] |= bit
        names = {1: 'rtti', 2: 'vtable', 4: 'other', 8: 'library'}
        t = tag[n]; i = 0
        while i < len(t):
            if t[i] not in (3, 4): i += 1; continue
            j = i; tg = t[i]; kk = kinds[i] if tg == 3 else 0
            while j < len(t) and t[j] == tg and (tg == 4 or kinds[j] == kk): j += 1
            raw = refbytes(lo + i, j - i); nz = sum(1 for q in raw if q)
            if tg == 3:
                nm = '+'.join(v for k_, v in names.items() if kk & k_) or 'unmatched-in-current-produced-metadata'
                rng.append(dict(va=lo + i, size=j - i, section=n, bucket='prod-unplaced', nonzero=nz, zero=j - i - nz, reason=nm))
            else:
                rng.append(dict(va=lo + i, size=j - i, section=n, bucket='rewritten', nonzero=nz, zero=j - i - nz, reason='import dir/IAT/TLS dir rebuilt by make_image.py'))
            i = j
    tot = collections.Counter(); byreason = collections.Counter()
    for r in rng:
        tot[(r['bucket'], 'nonzero')] += r['nonzero']; tot[(r['bucket'], 'zero')] += r['zero']; byreason[(r['bucket'], r['reason'])] += r['size']
    cb = sum(1 for n in ('.data', '.rdata') for t in tag[n] if t in (1, 2))
    summary = dict(covered_initialised_bytes=cb, raw_initialised_bytes=sum(SEC[n]['raw'] for n in ('.data', '.rdata')),
                   bytes={'%s/%s' % k: v for k, v in sorted(tot.items())}, bucket_bytes={b: sum(v for (bk, z), v in tot.items() if bk == b) for b in sorted({k[0] for k in tot})},
                   reason_bytes={'%s | %s' % k: v for k, v in sorted(byreason.items(), key=lambda kv: -kv[1])})
    json.dump(dict(note='remaining initialised .data/.rdata ranges of the current default build (frozen coverage inventory\\b9_default_cov.json); uncovered reasons = batch 7 rules (b9_select.py --inventory)',
                   summary=summary, ranges=rng), open(INV, 'w'), indent=0)
    print(json.dumps(summary, indent=1))


if '--inventory' in ap:
    inventory(); sys.exit(0)
parts = process(messy_ok=True, ok_holes=OK_HOLES, zero_ok=True, allow_sd=STAGE2)
new, stat, stat_n, cutn = emit_entries(parts)
base = json.load(open(BASE_SEL if STAGE2 else DEFAULT_SEL))
resid = collections.Counter()
for a, b, disp, reason, n in parts:
    if disp == 'skip':
        raw = refbytes(a, b - a); resid[reason + (' nonzero' if any(raw) else ' zero')] += b - a
tot = sum(e['size'] for e in new)
note = ('batch9 stage-%d selection (b9_select.py): base selection (%d entries) + %d new W objects (%d B, %d file-backed zero objects) by kind %s; bytes %s; '
        'holes emitted as pointer cells %s; residual uncovered %s; run-cut pieces %d' % (2 if STAGE2 else 1, len(base['entries']), len(new), tot, sum(1 for e in new if e.get('file_backed')), dict(stat_n), dict(stat), sorted(OK_HOLES), dict(resid), cutn))
json.dump(dict(note=note, base_sha256=base.get('base_sha256'), entries=base['entries'] + new), open(OUT, 'w'), indent=0)
print(note)
