r"""M3 batch 5: select the data-v1 placed pieces of OUR unit objects that can be spliced into the exe (opt-in FNV_M3_DV1=1, requires FNV_M3=1).
usage: python -I dv1_splice.py <dv1_placed.pkl> [--kinds string,float-const,...] [--out-tag TAG]
Reads: the data-v1 scratch pickle (place.py; pieces = bytes + relocations of our compiled unit objects, placement by tier B/V/H/L), the reference image (only to VERIFY
bytes/pointer values and to know the original .reloc sites), data-v3\symbolic.json + out\manifest.json (field set, chunk boundaries), m3\gen\skip_ranges.json (batch4 ranges).
Per piece (conservative; every drop is logged by reason):
  tier B / V / H / L only (O = duplicate-content ordering rule, ambiguous, is dropped); piece of one of our units (u < 100000; CRT/STL library members and m3 itself excluded);
  every relocation DIR32, resolved by our resolution to exactly the reference dword, sitting on an ORIGINAL .reloc site; the set of original .reloc sites inside the range == our relocation offsets
  (so the .reloc output and data-v3's ghost-field accounting are unchanged); no value-rule field (pointer without .reloc) inside; no data-v3 field straddling the range boundary;
  bytes (relocation fields replaced by the resolved value) == reference; target of every pointer inside the image (.text or a data chunk); range inside ONE data-v3 chunk;
  not all zero; no overlap with the m3 generated ranges or with another selected piece (identical/contained duplicates collapse onto the larger piece = COMDAT dedupe: one piece -> one position).
Writes (m3\gen): dv1_pieces.json, dv1_skip_ranges.json, skip_ranges_b5.json (m3 skip + dv1 skip, sorted, for DV3_SKIP), dv1_log.json."""
import os, sys, json, struct, collections, pickle, bisect, hashlib, re
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.environ.get('FNV_PROJ_ROOT') or r'C:\path\to\Decompilation'
RN = os.path.join(PROJ, 'runtime-next')
GEN = os.path.join(HERE, 'gen')
EXT = os.environ.get('FNV_M3_DV1_EXT') == '1'          # batch 6 (opt-in): placed-section resolution preference + link placement of unplaced target pieces verified with their own resolved relocations
GOUT = os.environ.get('FNV_M3_DV1_OUT') or GEN          # diagnostics: write the outputs elsewhere
os.makedirs(GOUT, exist_ok=True)
args = sys.argv[1:]
pkl = args[0]
kinds_only = None
if '--kinds' in args: kinds_only = set(args[args.index('--kinds') + 1].split(','))
sys.argv = [sys.argv[0]]
if os.environ.get('FNV_M3_DV1_REPLAY'):           # batch 10 step C: no reference image (dv1_replay.py)
    sys.path.insert(0, HERE); import dv1_replay; dv1_replay.main(pkl, os.environ['FNV_M3_DV1_REPLAY']); raise SystemExit(0)
sys.path.insert(0, os.path.join(RN, 'data-v1')); sys.path.insert(0, os.path.join(RN, 'data-v3'))
import place as PL
from common import ref, SEC, sec_of, orig_reloc_sites, read_ref, TLO, THI
M32 = 0xffffffff
st = pickle.load(open(pkl, 'rb'))
SECS, placed = st.SEC, st.placed
ORIG = sorted(orig_reloc_sites()); ORIGSET = set(ORIG)
sj = json.load(open(os.path.join(RN, 'data-v3', 'symbolic.json')))
VR = sorted(SEC[r[0]]['va'] + r[1] for r in sj['fields'] if r[4] == 'value-rule')
FLD = sorted(SEC[r[0]]['va'] + r[1] for r in sj['fields'])
chunks = [(m['va'], m['va'] + m['size'], m['section'], m['file']) for m in json.load(open(os.path.join(RN, 'data-v3', 'out', 'manifest.json')))]
bss_lo = SEC['.data']['va'] + SEC['.data']['raw']; bss_hi = SEC['.data']['va'] + SEC['.data']['vs']
m3skip = json.load(open(os.path.join(GEN, 'skip_ranges.json'))); m3rng = sorted((a, a + n) for a, n in m3skip)
RTTI_PROVEN = None
if os.environ.get('FNV_M3_RTTI_NAME_LITERAL') not in (None, '0', '1'): raise ValueError('invalid FNV_M3_RTTI_NAME_LITERAL')
if os.environ.get('FNV_M3_RTTI_NAME_LITERAL') == '1':
    sys.path.insert(0, os.path.join(HERE, 'phase2'))
    import selector_bridge as RTTI_BRIDGE
    RTTI_PROVEN, RTTI_OBJECTS = RTTI_BRIDGE.prepare_selector(st, sj, SEC, ORIGSET, read_ref, chunks, m3rng, os.path.join(RN, 'pinned-build', 'obj_v3'))
    RTTI_FIELDS = {field for _, field in RTTI_PROVEN}
    VR = [field for field in VR if field not in RTTI_FIELDS]

def any_in(sl, lo, hi):
    i = bisect.bisect_left(sl, lo); return i < len(sl) and sl[i] < hi
def hit_range(rngs, lo, hi):
    i = bisect.bisect_right(rngs, (lo, 1 << 40)) - 1
    for j in (i - 1, i, i + 1):
        if 0 <= j < len(rngs) and rngs[j][0] < hi and lo < rngs[j][1]: return True
    return False
def chunk_of(va, n):
    for lo, hi, sec, f in chunks:
        if lo <= va and va + n <= hi: return f, sec
    return None, None
def target_ok(v):
    if TLO <= v < THI: return True
    if any(lo <= v <= hi for lo, hi, sec, f in chunks): return True            # <= hi: one-past-the-end of a chunk
    return bss_lo <= v <= bss_hi

def resolve2(s):
    """data-v1 resolution (st.resolve) + [EXT] placed-section preference: a relocation whose target is a data section piece of the SAME unit that data-v1 placed
    resolves to that piece's placed address; the name-embedded address rule ('b': ADDR_RE on e.g. ??_R4FUN_00a11b80@@6B@ = the CLASS name) is not a location for a data piece."""
    res, src = st.resolve(s)
    if not EXT: return res, src
    u = s['units'][0]
    for r in s['relocs']:
        off, kind, nm, tsec, tval, tstor, addend, rsrc, rexp = r
        if rsrc == 'b' and kind == 6 and tsec > 0 and addend is not None:
            tk, a0 = st.tkey(u, tsec, tval + addend)
            if tk is not None and tk in placed:
                v = (placed[tk][0] + (tval + addend) - a0) & M32
                if res.get(off) != v: res[off] = v; src[off] = 'placed-section-pref'; ext_stats['pref_relocs'] += 1
    return res, src
ext_stats = collections.Counter(); ext_placed = collections.Counter()
if EXT:
    # link placement 'X' (fixpoint): an unplaced data piece T that a placed piece P points to (reference dword at the field => candidate address of T) is placed there when
    # (1) all of T's own relocations are resolved by our resolution and (2) T's bytes with those resolved values equal the reference at that address (needs >= 1 relocation,
    # so the check is a content check independent of the pointer that proposed the address), aligned, and not overlapping a differently-sized/placed piece.
    def pl_ranges(): return sorted((A, A + len(SECS[k]['data'])) for k, (A, t_) in placed.items() if len(SECS[k]['data']))
    for rnd in range(12):
        cand_x = collections.defaultdict(set)
        for k, (A, t_) in list(placed.items()):
            if t_ in ('O', 'M'): continue
            s = SECS[k]; u = s['units'][0]; L = len(s['data'])
            for r in s['relocs']:
                off, kind, nm, tsec, tval, tstor, addend, rsrc, rexp = r
                if kind != 6 or tsec <= 0 or addend is None or off + 4 > L: continue
                tk, a0 = st.tkey(u, tsec, tval + addend)
                if tk is None or tk in placed or tk not in SECS or SECS[tk]['kind'] == 'bss' or not SECS[tk]['data']: continue
                b = PL.refread(A + off, 4)
                if not b: continue
                rv, = struct.unpack('<I', b); cand_x[tk].add((rv - (tval + addend - a0)) & M32)
        n_new = 0; prs = pl_ranges(); prl = [x[0] for x in prs]
        for tk, cs in cand_x.items():
            if len(cs) != 1: ext_stats['x_multi_addr'] += 1; continue
            a = next(iter(cs)); ts = SECS[tk]; L = len(ts['data'])
            if PL.refread(a, L) is None or a % PL.algn(ts): ext_stats['x_unreadable_or_misaligned'] += 1; continue
            if not ts['relocs'] or any(r[1] != 6 or r[6] is None for r in ts['relocs']): ext_stats['x_not_pure_dir32'] += 1; continue
            res, src_ = resolve2(ts)
            if len(res) != len(ts['relocs']): ext_stats['x_unresolved_own_relocs'] += 1; continue
            if not PL.verify_at(ts, res, a): ext_stats['x_bytes_differ'] += 1; continue
            i = bisect.bisect_left(prl, a + L); ov = [x for x in prs[max(0, i - 3):i] if x[0] < a + L and a < x[1]]
            if any((x[0], x[1]) != (a, a + L) for x in ov): ext_stats['x_overlap'] += 1; continue
            placed[tk] = (a, 'X'); n_new += 1; ext_placed[ts['kind']] += 1; ext_placed['bytes:' + ts['kind']] += L
        print('EXT link round', rnd, 'newly placed', n_new, flush=True)
        if n_new == 0: break

rej = collections.Counter(); rejb = collections.Counter(); cand = []
rejsub = collections.Counter(); rejsubb = collections.Counter(); rejrng = collections.defaultdict(list)
TIERS = ('B', 'V', 'H', 'L', 'X') if EXT else ('B', 'V', 'H', 'L')
tierc = collections.Counter(); seen_in = collections.Counter()
for k, (A, tier) in sorted(placed.items(), key=lambda x: x[1][0]):
    s = SECS[k]; L = len(s['data']); kd = s['kind']
    if kd == 'bss' or L == 0: continue
    us = s['units']
    def drop(why):
        rej[(kd, why)] += 1; rejb[(kd, why)] += L; rejrng[why].append((A, A + L))
    if 200000 in us or tier == 'M': continue                                   # m3 generated: already overlaid by the batch 1-4 machinery
    if not any(u < 100000 for u in us): drop('library-object-not-our-unit'); continue
    if kinds_only is not None and kd not in kinds_only: drop('kind-not-in-this-stage'); continue
    if tier not in TIERS: drop('tier-%s-ambiguous-duplicate-ordering' % tier); continue
    data = bytes(s['data'])
    if not any(data) and not s['relocs']: drop('all-zero'); continue
    res, src = resolve2(s)
    rl = []; why = None; offs = set(); extf = EXT and tier == 'X'
    for r in s['relocs']:
        off, kind, nm, tsec, tval, tstor, addend, rsrc, rexp = r
        if kind != 6 or off + 4 > L: why = 'non-dir32-reloc'; break
        if any(abs(off - o2) < 4 for o2 in offs): why = 'overlapping-relocs'; break
        offs.add(off)
        e = res.get(off)
        rv, = struct.unpack('<I', read_ref(A + off, 4))
        if e is None:
            why = 'unresolved-reloc'
            if tsec > 0:
                tk, a0 = st.tkey(us[0], tsec, tval + (addend or 0))
                if tk is None: sub = 'target-is-code/eh-section-without-address'
                elif tk in placed: sub = 'target-placed-but-unresolved'
                else:
                    ts = SECS[tk]; a2 = (rv - (tval + addend - a0)) & M32 if addend is not None else None
                    sub = 'target-piece-unplaced(%s):%s' % (ts['kind'], 'reference-bytes-match(not unique/placed)' if a2 is not None and PL.refread(a2, len(ts['data'])) is not None and PL.verify_at(ts, {}, a2) else 'our-bytes-differ-from-reference')
            else: sub = 'extern-name-without-address(%s)' % kd
            rejsub[(why, sub)] += 1; rejsubb[(why, sub)] += L
            break
        if e & M32 != rv:
            why = 'reloc-resolves-differently-from-reference'
            sub = '%s|target-tsec>0:%s|ours %s|ref %s' % (src.get(off), tsec > 0, 'code' if TLO <= e & M32 < THI else 'data', 'code' if TLO <= rv < THI else 'data')
            rejsub[(why, sub)] += 1; rejsubb[(why, sub)] += L
            break
        if (A + off) not in ORIGSET: why = 'reloc-not-an-original-reloc-site'; break
        if not target_ok(rv): why = 'target-outside-image'; break
        if EXT:
            if src.get(off) == 'placed-section-pref': extf = True
            if tsec > 0 and addend is not None:
                tk_, _a0 = st.tkey(us[0], tsec, tval + addend)
                if tk_ is not None and tk_ in placed and placed[tk_][1] == 'X': extf = True       # depends on a link-placed (tier X) piece
        rl.append((off, rv, struct.unpack_from('<i', data, off)[0], src.get(off)))
    if why: drop(why); continue
    sites = {x for x in ORIG[bisect.bisect_left(ORIG, A):bisect.bisect_left(ORIG, A + L)]}
    if sites != {A + o for o in offs}: drop('original-reloc-site-without-our-reloc'); continue
    if any_in(VR, A - 3, A + L): drop('value-rule-field-inside-or-adjacent'); continue
    j = bisect.bisect_right(FLD, A) - 1
    if j >= 0 and FLD[j] < A < FLD[j] + 4: drop('field-straddles-start'); continue
    j = bisect.bisect_left(FLD, A + L) - 1
    if j >= 0 and FLD[j] < A + L < FLD[j] + 4: drop('field-straddles-end'); continue
    buf = bytearray(data)
    for off, rv, add, sr in rl: buf[off:off + 4] = struct.pack('<I', rv)
    rb = read_ref(A, L)
    if rb is None or bytes(buf) != rb: drop('bytes-differ-from-reference'); continue
    f, sec = chunk_of(A, L)
    if f is None: drop('not-inside-one-data-v3-chunk'); continue
    if hit_range(m3rng, A, A + L): drop('overlaps-m3-generated-range'); continue
    cand.append(dict(va=A, size=L, kind=kd, tier=tier, unit=min(u for u in us if u < 100000), nunits=len(us), section=sec, chunk=f,
                     names=[d[0] for d in s['defs'] if d[2] == 2][:2], ext=bool(extf), data=data, relocs=rl, sources=sorted({x[3] for x in rl}), k=k))
    tierc[tier] += 1

# ---- overlap resolution = COMDAT dedupe: larger piece first; an identical or contained duplicate collapses onto it; a partial overlap drops the later piece
cand.sort(key=lambda c: (-c['size'], c['va'], c['unit']))
acc = []; accr = []      # accepted (sorted by va for bisect)
dup = collections.Counter(); dupb = collections.Counter()
import bisect as _b
starts = []; accl = []
for c in cand:
    lo, hi = c['va'], c['va'] + c['size']
    i = _b.bisect_left(starts, lo)
    nb = [accl[j] for j in (i - 1, i, i + 1) if 0 <= j < len(accl)]
    # (accepted pieces never overlap each other, so only the immediate neighbours can overlap this one... except a long accepted piece starting far before: check i-1 only by end)
    ov = [a for a in nb if a['va'] < hi and lo < a['va'] + a['size']]
    if ov:
        o = ov[0]
        if o['va'] <= lo and hi <= o['va'] + o['size']:
            why = 'duplicate-collapsed-onto-identical-range' if (o['va'] == lo and o['size'] == c['size']) else 'contained-in-a-larger-selected-piece'
        else: why = 'partial-overlap-with-selected-piece'
        rej[(c['kind'], why)] += 1; rejb[(c['kind'], why)] += c['size']; rejrng[why].append((c['va'], c['va'] + c['size'])); continue
    k2 = _b.bisect_left(starts, lo); starts.insert(k2, lo); accl.insert(k2, c)
acc = accl
# Explicit, digest-pinned experimental library path. The default selector
# continues to exclude library units. Validate every entry before writing output.
lib_meta = None
lib_selection = os.environ.get('FNV_M3_LIB_SELECTION')
if lib_selection:
    expected = os.environ.get('FNV_M3_LIB_SHA256', '')
    if not re.fullmatch(r'[0-9a-fA-F]{64}', expected):
        raise SystemExit('FNV_M3_LIB_SHA256 must pin the library selection')
    sys.path.insert(0, os.path.join(HERE, 'phase2'))
    sys.path.insert(0, os.path.join(RN, 'data-v2'))
    import library_overlay, libsecs
    additions, lib_meta = library_overlay.select_library(lib_selection, expected, st, m3skip, acc, chunks, FLD, ORIGSET, read_ref, libsecs)
    acc = sorted(acc + additions, key=lambda c: c['va'])
elif os.environ.get('FNV_M3_LIB_SHA256'):
    raise SystemExit('FNV_M3_LIB_SHA256 requires FNV_M3_LIB_SELECTION')
# ---- outputs
dv1skip = sorted([c['va'], c['size']] for c in acc)
merged = sorted(m3skip + dv1skip)
for x, y in zip(merged, merged[1:]): assert x[0] + x[1] <= y[0], ('overlap in merged skip ranges', x, y)
pieces = [dict(va=c['va'], size=c['size'], section=c['section'], chunk=c['chunk'], kind=c['kind'], tier=c['tier'], unit=c['unit'], nunits=c['nunits'], names=c['names'], ext=c['ext'],
               data=c['data'].hex(), relocs=[[o, t, a] for o, t, a, sr in c['relocs']],
               **({'library_opt_in': True} if c.get('library_opt_in') else {})) for c in sorted(acc, key=lambda c: c['va'])]
payload = json.dumps(dict(note='M3 batch 5: data-v1 placed pieces of our unit objects (bytes as compiled, relocation fields hold the object addend); relocs = [offset, resolved target VA, object addend]', pieces=pieces), separators=(',', ':')).encode('utf8')
if RTTI_PROVEN is not None:
    if os.path.exists(os.path.join(os.environ['TEMP'], 'rtti-name-field-proof.json')): raise FileExistsError('RTTI proof already exists')
    proof = RTTI_BRIDGE.finish(RTTI_PROVEN, RTTI_OBJECTS, pieces, hashlib.sha256(payload).hexdigest(), os.path.join(PROJ, 'fnv_decomp', 'build', 'units.json'), (os.environ.get('FNV_REF_IMAGE') or os.path.join(PROJ, 'FNV', 'work', 'worker1', 'FalloutNV.runtime-text.exe')), pkl)
with open(os.path.join(GOUT, 'dv1_pieces.json'), 'wb') as f: f.write(payload)
FREEZE = os.environ.get('FNV_M3_DV1_FREEZE')
if FREEZE:          # batch 10 step C: freeze piece identities (hash of the compiled section key), VAs, tiers and target VAs of this normal run; no section bytes
    def _kh(k): return hashlib.sha256(repr(k).encode('utf8')).hexdigest()
    os.makedirs(FREEZE, exist_ok=True)
    rp = dict(note='frozen identity -> VA map of the accepted data-v1 pieces (no reference bytes); dsha = sha256 of OUR compiled bytes', payload_sha256=hashlib.sha256(payload).hexdigest(), pieces=[
        dict(kh=_kh(c['k']), va=c['va'], size=c['size'], tier=c['tier'], kind=c['kind'], unit=c['unit'], nunits=c['nunits'], section=c['section'], chunk=c['chunk'], names=c['names'], ext=c['ext'],
             dsha=hashlib.sha256(bytes(c['data'])).hexdigest(), relocs=[[o, t, a] for o, t, a, sr in c['relocs']], **({'library_opt_in': True} if c.get('library_opt_in') else {})) for c in sorted(acc, key=lambda c: c['va'])])
    if lib_meta: rp['library'] = dict(selected=lib_meta['selected'], bytes=lib_meta['bytes'], archive_sha256=lib_meta['archive_sha256'])
    if RTTI_PROVEN is not None: rp['rtti_proof_template'] = {k_: proof[k_] for k_ in ('schema', 'removed_value_fields', 'selected', 'objects_sha256')}
    json.dump(rp, open(os.path.join(FREEZE, 'dv1_replay.json'), 'w'), separators=(',', ':'))
    pmap = {_kh(k_): [a_, t_] for k_, (a_, t_) in placed.items() if t_ != 'M' and SECS[k_]['kind'] != 'bss' and len(SECS[k_]['data'])}
    json.dump(dict(image_base=PL.BASE, map=pmap), open(os.path.join(FREEZE, 'placement_map.json'), 'w'), separators=(',', ':'))
    print('FROZEN:', len(rp['pieces']), 'pieces,', len(pmap), 'placed pieces ->', FREEZE)
if RTTI_PROVEN is not None:
    with open(os.path.join(os.environ['TEMP'], 'rtti-name-field-proof.json'), 'x') as f: json.dump(proof, f, indent=2)

json.dump(dv1skip, open(os.path.join(GOUT, 'dv1_skip_ranges.json'), 'w'))
json.dump(merged, open(os.path.join(GOUT, 'skip_ranges_b5.json'), 'w'))
bykind = collections.defaultdict(lambda: [0, 0, 0]); bytier = collections.Counter()
for c in acc:
    b = bykind[c['kind']]; b[0] += 1; b[1] += c['size']; b[2] += len(c['relocs']); bytier[c['tier']] += c['size']
def merge(rs):
    out = []
    for lo, hi in sorted(rs):
        if out and lo <= out[-1][1]: out[-1][1] = max(out[-1][1], hi)
        else: out.append([lo, hi])
    return out
def uncovered(rs, cov):
    """bytes of the union of rs that lie outside the union cov (both merged lists)"""
    n = 0; starts = [x[0] for x in cov]
    for lo, hi in merge(rs):
        cur = lo
        i = max(0, bisect.bisect_right(starts, lo) - 1)
        while i < len(cov) and cov[i][0] < hi:
            if cov[i][1] > cur:
                if cov[i][0] > cur: n += cov[i][0] - cur
                cur = max(cur, cov[i][1])
            i += 1
        if cur < hi: n += hi - cur
    return n
covered = merge([(c['va'], c['va'] + c['size']) for c in acc] + [(a_, a_ + n_) for a_, n_ in m3skip])
uncov = {w: dict(piece_ranges=len(r), unique_uncovered_bytes=uncovered(r, covered)) for w, r in sorted(rejrng.items())}
log = dict(selected=len(acc), bytes=sum(c['size'] for c in acc), relocs=sum(len(c['relocs']) for c in acc), kinds_filter=sorted(kinds_only) if kinds_only else None,
           library_opt_in=lib_meta,
           by_kind={k: dict(pieces=v[0], bytes=v[1], relocs=v[2]) for k, v in sorted(bykind.items())}, bytes_by_tier=dict(bytier),
           by_section={s_: sum(c['size'] for c in acc if c['section'] == s_) for s_ in ('.data', '.rdata', 'CONST', '.tls')},
           rejected={'%s|%s' % k: dict(pieces=v, bytes=rejb[k]) for k, v in sorted(rej.items(), key=lambda kv: -rejb[kv[0]])},
           rejected_bytes_by_reason={w: sum(b for (kk, ww), b in rejb.items() if ww == w) for w in sorted({ww for kk, ww in rej})},
           rejected_sub={'%s|%s' % k: dict(pieces=v, bytes=rejsubb[k]) for k, v in sorted(rejsub.items(), key=lambda kv: -rejsubb[kv[0]])},
           rejected_unique_uncovered=uncov, ext=dict(enabled=EXT, stats=dict(ext_stats), placed_by_kind=dict(ext_placed), selected_pieces=sum(1 for c in acc if c['ext']), selected_bytes=sum(c['size'] for c in acc if c['ext']), selected_relocs=sum(len(c['relocs']) for c in acc if c['ext'])),
           pieces_sha=hashlib.sha256(open(os.path.join(GOUT, 'dv1_pieces.json'), 'rb').read()).hexdigest()[:16])
json.dump(log, open(os.path.join(GOUT, 'dv1_log.json'), 'w'), indent=1)
print(json.dumps({k: log[k] for k in ('selected', 'bytes', 'relocs', 'by_kind', 'bytes_by_tier', 'by_section', 'rejected_bytes_by_reason')}, indent=1))
