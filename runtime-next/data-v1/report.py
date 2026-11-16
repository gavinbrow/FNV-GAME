"""data-v1 report.py: from the placements (place.py) resolve every data relocation field with our resolution, compare with the reference,
write FalloutNV_data_strict.exe (build-v7 strict .text + produced .rdata/.data pieces, rest of .rdata/.data = 0x00) and the filled variant, progress.json."""
import sys, struct, collections, pickle, json, hashlib, gzip, re, time
sys.dont_write_bytecode = True
sys.path.append((__import__('os').environ.get('FNV_PY_SITE', __import__('os').path.expandvars(r'%APPDATA%\Python\Python312\site-packages'))))
import numpy as np
sys.argv = [sys.argv[0]] + sys.argv[1:]
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import place as PL
from place import ref, REG, SECS, BASE, M32, refread, region_of, v7map
HERE = PL.HERE; RN = PL.RN
V7S = RN / 'build-v7' / 'FalloutNV_v7_strict.exe'
REFSHA = 'df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7'
TEXT_LO = SECS['.text'][0]; TEXT_HI = TEXT_LO + SECS['.text'][1]
def sha(b): return hashlib.sha256(b).hexdigest()
ST = pickle.load(open(sys.argv[1], 'rb'))
SEC, placed, info = ST.SEC, ST.placed, ST.info
# ---- original .reloc data->code fields
peo = PL.peo
rrva, rsz = struct.unpack_from('<II', ref, peo + 24 + 96 + 5 * 8)
rs0 = SECS['.reloc']; p = rs0[2] + (rrva - (rs0[0] - BASE)); end = p + rsz; orel = set()
while p < end:
    pg, bs = struct.unpack_from('<II', ref, p)
    if bs == 0: break
    for k in range((bs - 8) // 2):
        w, = struct.unpack_from('<H', ref, p + 8 + 2 * k)
        if w >> 12 == 3: orel.add(BASE + pg + (w & 0xfff))
    p += bs
d2c = {}
for f in orel:
    if region_of(f) in ('.rdata', '.data'):
        b = refread(f)
        if b:
            v, = struct.unpack('<I', b)
            if TEXT_LO <= v < TEXT_HI: d2c[f] = v
orel_data = {f for f in orel if region_of(f) in ('.rdata', '.data')}
print('data->code in orig .reloc', len(d2c), collections.Counter(region_of(f) for f in d2c))
resolve = ST.resolve
def category(nm):
    for pre, c in (('__ehhandler$', 'ehhandler'), ('__ehfuncinfo$', 'ehfuncinfo'), ('__unwindtable$', 'unwindtable'), ('__unwindfunclet$', 'unwindfunclet'),
                   ('__catch$', 'catch'), ('??_7', 'vtable'), ('??_R0', 'rtti0'), ('??_R1', 'rtti1'), ('??_R2', 'rtti2'), ('??_R3', 'rtti3'), ('??_R4', 'rtti4'),
                   ('??_C', 'string'), ('$SG', 'string'), ('__real@', 'float'), ('__imp_', 'import'), ('__purecall', 'purecall'), ('__tryblocktable', 'tryblock'), ('__catchsym', 'catchsym')):
        if nm.startswith(pre): return c
    if re.search(r'\?(Unk|vfn)_\d+@', nm): return 'unnamed-virtual-slot(Unk_/vfn_)'
    if nm.startswith('?') or nm.startswith('_'): return 'other-named'
    return 'other'
RD = {n: (va, ro, rs, vs) for n, va, ro, rs, vs in REG}
def idx(va):
    for n, (rva, ro, rs, vs) in RD.items():
        if rva <= va < rva + rs: return n, va - rva
    return None, None
# produced image buffers (file bytes), per region
buf = {n: bytearray(RD[n][2]) for n in RD}
prod = {n: np.zeros(RD[n][2], np.uint8) for n in RD}          # 1 = produced
kindarr = {n: np.zeros(RD[n][2], np.uint8) for n in RD}
KINDS = sorted({s['kind'] for s in SEC.values()}); KID = {k: i + 1 for i, k in enumerate(KINDS)}
fieldstat = {}      # field va -> (status, src, cause, tier, kind)
cnt = collections.Counter(); cause = collections.Counter()
tier_n = collections.Counter(); tier_b = collections.Counter(); kind_tier_b = collections.Counter(); kind_n = collections.Counter()
fields_by = collections.Counter()
dis_ex = {}
def first32(a):
    b = refread(a, 32)
    return b
for k, (A, tier) in sorted(placed.items(), key=lambda x: x[1][0]):
    s = SEC[k]; L = len(s['data']); res, src = resolve(s)
    n, o = idx(A)
    if n is None or o + L > RD[n][2]: cnt['placed-outside-file-bytes'] += 1; continue
    tier_n[tier] += 1; tier_b[tier] += L; kind_n[s['kind']] += 1; kind_tier_b[(s['kind'], tier)] += L
    b = bytearray(s['data']); pm = bytearray(b'\1' * L)
    for r in s['relocs']:
        off, kind, nm, tsec, tval, tstor, addend, rsrc, rexp = r; w = 2 if kind == 0x0A else 4
        for q in range(off, min(off + w, L)): pm[q] = 0; b[q] = 0
    for r in s['relocs']:
        off, kind, nm, tsec, tval, tstor, addend, rsrc, rexp = r
        fva = A + off
        if kind not in (6, 7) or off + 4 > L:
            fieldstat[fva] = ('borrow', None, 'kind-%x' % kind, tier, s['kind']); cnt['field-other-kind'] += 1; continue
        rv, = struct.unpack('<I', refread(fva, 4)); exp = res.get(off); sr = src.get(off)
        if exp is None:
            c = ('unplaced-local-section:' + category(nm)) if tsec > 0 else ('extern-unmapped:' + category(nm))
            fieldstat[fva] = ('borrow', None, c, tier, s['kind']); cause[c] += 1; continue
        want = exp if kind == 6 else (exp - BASE) & M32
        if want == rv:
            b[off:off + 4] = struct.pack('<I', want); pm[off:off + 4] = b'\1\1\1\1'
            fieldstat[fva] = ('agree', sr, '', tier, s['kind'])
        else:
            if TEXT_LO <= exp < TEXT_HI and TEXT_LO <= rv < TEXT_HI:
                x, y = refread(exp, 32), refread(rv, 32)
                if x == y and x is not None: c = 'identical-code-other-copy(ICF-like)'
                elif abs(exp - rv) <= 16: c = 'near-delta'
                else: c = 'different-function'
            elif TEXT_LO <= rv < TEXT_HI: c = 'ours-not-code(ref-code)'
            elif TEXT_LO <= exp < TEXT_HI: c = 'ours-code(ref-not-code)'
            else: c = 'data-target-different'
            c = '%s|%s' % (sr, c); dis_ex.setdefault(c, (nm[:60], hex(exp), hex(rv)))
            fieldstat[fva] = ('disagree', sr, c, tier, s['kind']); cause[c] += 1
    for q in range(L):
        if pm[q]: buf[n][o + q] = b[q]
    a = np.frombuffer(bytes(pm), np.uint8).astype(bool)
    seg = prod[n][o:o + L]; kseg = kindarr[n][o:o + L]
    new = a & (seg == 0); kseg[new] = KID[s['kind']]; seg[a] = 1
# ---- wB data-v2: CRT$XCU init array. The linker concatenates the .CRT$XCU contributions into ascending (link-order) runs of code pointers; our compiled units' initializer
# addresses (resolved by name, 6,266 distinct) are located as members of the long ascending runs of the reference; a dword is produced when its value is one of ours.
if os.environ.get('DV_XCU', '1') == '1':
    xv = collections.Counter()
    for k, s_ in SEC.items():
        if s_['kind'] == 'crt-init-array' and s_['name'] == '.CRT$XCU' and k not in placed and s_['units'][0] < 100000:
            r_, _src = resolve(s_)
            for v_ in r_.values(): xv[v_ & M32] += 1
    n_, (rva_, ro_, rs_, vs_) = '.rdata', RD['.rdata']
    dws = struct.unpack('<%dI' % (rs_ // 4), ref[ro_:ro_ + (rs_ // 4) * 4]); i_ = 0; nx = 0
    while i_ < len(dws):
        if TEXT_LO <= dws[i_] < TEXT_HI:
            j_ = i_
            while j_ < len(dws) and TEXT_LO <= dws[j_] < TEXT_HI: j_ += 1
            run = dws[i_:j_]; mine = sum(1 for x in run if x in xv)
            if len(run) >= 100 and mine >= 0.8 * len(run) and sum(1 for p_, q_ in zip(run, run[1:]) if q_ >= p_) >= 0.95 * (len(run) - 1):
                for t_, x in enumerate(run):
                    if x in xv:
                        o4 = 4 * (i_ + t_)
                        if not prod[n_][o4:o4 + 4].any():
                            buf[n_][o4:o4 + 4] = struct.pack('<I', x); prod[n_][o4:o4 + 4] = 1; kindarr[n_][o4:o4 + 4] = KID['crt-init-array']; nx += 4
            i_ = j_
        else: i_ += 1
    print('crt init array bytes produced', nx)
# ---- images
v7 = bytearray(V7S.read_bytes()); v7sha = sha(bytes(v7))
strict = bytearray(v7)
for n, (rva, ro, rs, vs) in RD.items():
    if n in ('.rdata', '.data'): strict[ro:ro + rs] = bytes(rs)
    for i in np.flatnonzero(prod[n]).tolist() if False else []: pass
for n, (rva, ro, rs, vs) in RD.items():
    m = prod[n].astype(bool); arr = np.frombuffer(bytes(buf[n]), np.uint8)
    seg = np.frombuffer(strict, np.uint8)[ro:ro + rs]   # read-only view of bytearray is writable
    sv = np.frombuffer(strict, dtype=np.uint8)
    sv[ro:ro + rs][m] = arr[m]
filled = bytearray(strict)
for n, (rva, ro, rs, vs) in RD.items():
    m = ~prod[n].astype(bool)
    fv = np.frombuffer(filled, dtype=np.uint8); rv_ = np.frombuffer(ref, dtype=np.uint8)
    fv[ro:ro + rs][m] = rv_[ro:ro + rs][m]
# the text of the strict build is untouched; the filled variant must equal the reference only if the strict .text holes are also filled from the reference
tro, trs = SECS['.text'][2], SECS['.text'][3]
fv = np.frombuffer(filled, dtype=np.uint8); fv[tro:tro + trs][np.frombuffer(v7, np.uint8)[tro:tro + trs] == 0xcc] = np.frombuffer(ref, np.uint8)[tro:tro + trs][np.frombuffer(v7, np.uint8)[tro:tro + trs] == 0xcc]
# (build-v7's own filled image does the same job exactly: use it for .text so the SHA means the same thing)
v7f = (RN / 'build-v7' / 'FalloutNV_v7_filled.exe').read_bytes()
filled[tro:tro + trs] = v7f[tro:tro + trs]
(HERE / 'FalloutNV_data_strict.exe').write_bytes(bytes(strict))
(HERE / 'FalloutNV_data_filled.exe').write_bytes(bytes(filled))
filled_ok = sha(bytes(filled)) == REFSHA
print('filled sha ok', filled_ok, sha(bytes(filled)))
# ---- stats
reg_tot = {n: RD[n][2] for n in RD}
prod_by_kind = {}
for n in RD:
    for kname, kid in KID.items():
        c = int((kindarr[n] == kid).sum())
        if c: prod_by_kind.setdefault(kname, {})[n] = c
prodsum = {n: int(prod[n].sum()) for n in RD}
fs = collections.Counter(v[0] for v in fieldstat.values())
dres = collections.Counter(); dtier = collections.Counter(); dsrc = collections.Counter(); dcause = collections.Counter(); dkind = collections.Counter()
for f, tv in d2c.items():
    st = fieldstat.get(f)
    if st is None:
        n, o = idx(f)
        dres['produced-bytes-but-no-reloc-record' if (n and prod[n][o]) else 'no-placed-piece'] += 1; continue
    status, sr, c, tier, kd = st
    dres[status] += 1; dkind[(kd, status)] += 1
    if status == 'agree': dtier[tier] += 1; dsrc[sr] += 1
    elif status == 'disagree': dcause[c] += 1
    else: dcause['unresolved:' + c] += 1
# fields ours: text-range value in our data fields not in orig .reloc
extra_text = sum(1 for f, st in fieldstat.items() if st[0] == 'agree' and f not in orel_data and False)
# hint cross-check
hx = collections.Counter()
for k, (A, tier) in placed.items():
    s = SEC[k]
    if not s['hint']: hx['%s:no-hint' % tier] += 1; continue
    hx['%s:hint-equal' % tier if A in s['hint'] else '%s:hint-differs' % tier] += 1

# ---- extra diagnostics
ceil = collections.Counter()
for k, s in SEC.items():
    pl = 'placed' if k in placed else 'unplaced'
    for rr in s['relocs']:
        if rr[1] != 6: continue
        code = (rr[7] in ('a', 'eh-piece', 'icf-fold')) or (rr[7] is None and rr[3] <= 0 and not rr[2].startswith(('??_', '__real', '$SG', '__imp')))
        if code: ceil['%s|%s' % (s['kind'], pl)] += 1
# unresolved extern names in placed pieces: would the reference's own values for them be consistent? (circular, NOT counted as produced)
infer = collections.defaultdict(set); infer_n = collections.Counter()
for k, (A, tier) in placed.items():
    s = SEC[k]; res, src = resolve(s)
    for rr in s['relocs']:
        if rr[1] != 6 or rr[0] in res or rr[6] is None or rr[3] > 0: continue
        b = refread(A + rr[0], 4)
        if b: infer[rr[2]].add(struct.unpack('<I', b)[0] - rr[6]); infer_n[rr[2]] += 1
cons = [n for n, v in infer.items() if len(v) == 1]
inf = dict(unresolved_extern_names=len(infer), names_with_one_reference_value=len(cons), fields_of_those=sum(infer_n[n] for n in cons), all_fields=sum(infer_n.values()))
b8 = collections.Counter(); b_diff = 0
for k, (A, tier) in placed.items():
    s = SEC[k]
    if tier == 'B':
        b8['B>=8 unmasked bytes' if PL.unmasked(s) >= 8 else 'B<8 unmasked bytes'] += 1
        if s['hint'] and A not in s['hint']: b_diff += 1
unpl = collections.Counter(); unpl_b = collections.Counter(); nB = collections.Counter(); unpl_hint = collections.Counter()
for k, s in SEC.items():
    if k in placed or s['kind'] == 'bss' or s['size'] == 0: continue
    nbk = info.get(k, {}).get('nB')
    why = 'no-unmasked-bytes' if nbk is None else ('bytes-match-nowhere' if nbk == 0 else ('bytes-ambiguous(%s)' % ('many' if nbk == -1 or nbk > 50 else ('2-50' if nbk > 1 else '?'))))
    unpl[(s['kind'], why)] += 1; unpl_b[(s['kind'], why)] += s['size']
    if s['hint']: unpl_hint[s['kind']] += 1
bss = [s for s in SEC.values() if s['kind'] == 'bss']
datavs = SECS['.data']; bss_lo = datavs[0] + datavs[3]
bss_hint = sum(1 for s in bss if any(a >= bss_lo for a in s['hint']))
# leftover classification in .rdata/.data
left = collections.Counter()
imp_ranges = []
for di in (1, 12):
    va, sz = struct.unpack_from('<II', ref, peo + 24 + 96 + 8 * di)
    if va: imp_ranges.append((BASE + va, BASE + va + sz))
for n in ('.rdata', '.data'):
    rva, ro, rs, vs = RD[n]
    m = prod[n] == 0; refb = np.frombuffer(ref, np.uint8)[ro:ro + rs]
    ir = np.zeros(rs, bool)
    for lo, hi in imp_ranges:
        a, b_ = max(lo - rva, 0), min(hi - rva, rs)
        if a < b_: ir[a:b_] = True
    zero = m & (refb == 0) & ~ir
    left[(n, 'import-dir/IAT')] += int((m & ir).sum()); left[(n, 'zero-bytes(padding/zero-init)')] += int(zero.sum())
    left[(n, 'nonzero-other')] += int((m & ~ir & ~zero).sum())
pd = dict(
    ref_sizes={n: dict(raw=RD[n][2], virt=RD[n][3]) for n in RD},
    produced_bytes_by_region=prodsum,
    produced_pct_of_rdata_data_raw=round(100 * (prodsum['.rdata'] + prodsum['.data']) / (RD['.rdata'][2] + RD['.data'][2]), 3),
    produced_bytes_by_kind=prod_by_kind,
    placed_pieces_by_tier=dict(tier_n), placed_bytes_by_tier=dict(tier_b), placed_pieces_by_kind=dict(kind_n),
    tier_legend=dict(B='bytes with reloc fields masked: exactly one aligned hit in the reference', V='bytes + our own resolved reloc values: exactly one hit',
                     H='no unique hit; placed at the symbol-map hint address after bytes verified there'),
    unique_sections=len(SEC), placed_sections=len(placed),
    hint_crosscheck=dict(hx), B_tier_strength=dict(b8), B_tier_hint_differs=b_diff,
    ceiling_code_pointing_relocs_in_our_data=dict(ceil), ceiling_total=sum(ceil.values()), inferable_from_reference_circular=inf,
    placed_bytes_by_kind_tier={'%s|%s' % k: v for k, v in sorted(kind_tier_b.items())},
    unplaced_sections={'%s|%s' % k: dict(n=v, bytes=unpl_b[k]) for k, v in sorted(unpl.items(), key=lambda kv: -unpl_b[kv[0]])},
    unplaced_with_hint_by_kind=dict(unpl_hint),
    bss=dict(sections=len(bss), bytes=sum(s['size'] for s in bss), with_hint_in_data_virtual_tail=bss_hint, note='no file bytes; only the layout is known'),
    fields_in_placed_pieces=dict(fs),
    fields_unresolved_or_disagree_causes=dict(cause.most_common()),
    data_to_code=dict(total_orig_reloc=len(d2c), by_region=dict(collections.Counter(region_of(f) for f in d2c)),
                      our_agree=dres['agree'], our_disagree=dres['disagree'], borrowed_unresolved=dres['borrow'],
                      produced_bytes_but_no_reloc_record=dres['produced-bytes-but-no-reloc-record'], no_placed_piece=dres['no-placed-piece'],
                      agree_by_tier=dict(dtier), agree_by_source=dict(dsrc), disagree_causes=dict(dcause.most_common()),
                      agree_by_kind={'%s|%s' % k: v for k, v in dkind.items()}),
    disagree_examples={c: v for c, v in dis_ex.items()},
    leftover_unproduced={'%s|%s' % k: v for k, v in left.items()},
    sha256=dict(v7_strict_used=v7sha, data_strict=sha(bytes(strict)), data_filled=sha(bytes(filled)), reference=sha(ref)),
    filled_equals_reference=filled_ok,
)
(HERE / 'progress.json').write_text(json.dumps(pd, indent=1))
# compact piece table (address, size, tier, kind id), no names
with gzip.open(HERE / 'pieces.tsv.gz', 'wt') as f:
    f.write('va\tsize\ttier\tkind\n')
    for k, (A, t) in sorted(placed.items(), key=lambda x: x[1][0]): f.write('%08x\t%d\t%s\t%s\n' % (A, len(SEC[k]['data']), t, SEC[k]['kind']))
print(json.dumps({k: pd[k] for k in ('produced_bytes_by_region', 'produced_pct_of_rdata_data_raw', 'placed_pieces_by_tier', 'data_to_code', 'filled_equals_reference')}, indent=1))
