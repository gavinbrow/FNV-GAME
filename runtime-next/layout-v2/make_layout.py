r"""layout-v2 / M4a: first runnable free-layout build.
Takes direct-v1\FalloutNV_direct.exe, moves every .text block into a NEW section (.ntext) in a different order, rewrites every code
reference and regenerates .reloc, entry point and data->code pointers. The old .text range is filled with 0xCC (so any missed reference faults).

  python make_layout.py --layout G|U|R|REV|Z [--seed N] [--out FILE] [--sweep]

Sources of every rewritten field (labelled in NOTES.md):
  OWN     .text REL32/DIR32 positions+kinds: build-v7 relocs_v7.tsv.gz (+inferred_literals_v7.json for DIR32 sites), same rule as reloc-v7\ownreloc.py
  OWN     block boundaries: units.json functions / eh_tails + build-v7 contrib_pieces.json; everything else (CRT, EH pieces outside units) = rigid gap blocks
  DIS     fields found only by capstone sweep inside gap blocks (rel32 leaving the block, not in records)   [--sweep]
  BORROW  data->code pointers in .rdata/.data: positions from the reference .reloc table (values rewritten with our block map)
Nothing outside runtime-next\layout-v2 and direct-v1 is written."""
import sys, os, struct, gzip, json, bisect, collections, argparse, time, pickle
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model
from model import TV, TS, B7, RN

ap = argparse.ArgumentParser()
ap.add_argument('--layout', default='G'); ap.add_argument('--seed', type=int, default=1)
ap.add_argument('--src', default=RN + r'\direct-v1\FalloutNV_direct.exe')
ap.add_argument('--out', default=None); ap.add_argument('--sweep', action='store_true')
ap.add_argument('--no-chain', action='store_true')
ap.add_argument('--remap-unreloc', action='store_true', help='experiment: also remap data dwords equal to a block start but absent from .reloc')
a = ap.parse_args()
out = a.out or os.path.join(HERE, 'FalloutNV_layout_%s.exe' % a.layout)
t0 = time.time()
def log(*x): print('[%5.1fs]' % (time.time() - t0), *x, flush=True)

# ------------------------------------------------------------------ image
d = bytearray(open(a.src, 'rb').read())
e_lf = struct.unpack_from('<I', d, 0x3c)[0]; fh = e_lf + 4; opt = fh + 20
nsec = struct.unpack_from('<H', d, fh + 2)[0]; so = opt + struct.unpack_from('<H', d, fh + 16)[0]
base = struct.unpack_from('<I', d, opt + 28)[0]; assert base == 0x400000
secs = []
for i in range(nsec):
    n, vs, va, rs, rp = struct.unpack_from('<8sIIII', d, so + 40 * i); secs.append((n.rstrip(b'\0').decode(), va, vs, rp, rs))
S = {n: (va, vs, rp, rs) for n, va, vs, rp, rs in secs}
assert S['.text'][0] == TV - base and S['.text'][3] == TS
def foff(va):
    r = va - base
    for n, v, vs, rp, rs in secs:
        if v <= r < v + rs: return rp + r - v
    raise ValueError(hex(va))
sizeofimage = struct.unpack_from('<I', d, opt + 56)[0]
text = np.frombuffer(bytes(d[0x400:0x400 + TS]), np.uint8)
assert S['.text'][2] == 0x400
log('image', hex(sizeofimage), 'sections', [s[0] for s in secs])

# ------------------------------------------------------------------ blocks
atoms = model.load_atoms()
PAD = (0xcc, 0x00, 0x90)
def padrun(p, lim):
    while p < lim and text[p] in PAD: p += 1
    return p
blocks = []   # [start, end, type, unit]
pos = 0
for i, (s, e, k, u) in enumerate(atoms):
    if s > pos:
        p = padrun(pos, s)
        if blocks and p > pos: blocks[-1][1] = p; pos = p
        if s > pos: blocks.append([pos, s, 'gap', -1]); pos = s
    nxt = atoms[i + 1][0] if i + 1 < len(atoms) else TS
    blocks.append([s, e, k, u]); pos = e
    p = padrun(pos, nxt); blocks[-1][1] = p; pos = p
if pos < TS: blocks.append([pos, TS, 'gap', -1])
assert blocks[0][0] == 0 and all(blocks[i][1] == blocks[i + 1][0] for i in range(len(blocks) - 1)) and blocks[-1][1] == TS
nb = len(blocks)
bs = np.array([b[0] for b in blocks], np.int64); be = np.array([b[1] for b in blocks], np.int64)
btype = [b[2] for b in blocks]; bunit = np.array([b[3] for b in blocks])
log('blocks', nb, collections.Counter(btype), 'gap bytes', int(sum(b[1] - b[0] for b in blocks if b[2] == 'gap')))

# ------------------------------------------------------------------ fields
recs = model.load_records()
inferred = json.load(open(B7 + r'\inferred_literals_v7.json'))
IMGLO, IMGHI = base, base + 0x1081000     # original image range (incl. wrapper) used by the ownreloc rule
rel_f = []; dir_f = []; nrec = collections.Counter()
for off, kind, status, origin, exp, tsec in recs:
    if kind == 'REL32': rel_f.append(off)
    elif kind == 'DIR32':
        if status in ('agree', 'disagree') and exp >= 0 and tsec != '-1' and IMGLO <= exp < IMGHI: dir_f.append(off)
    else: nrec[kind] += 1
for k in inferred:
    o = int(k, 16) - TV
    if 0 <= o < TS: dir_f.append(o)
rel_f = np.array(sorted(set(rel_f)), np.int64); dir_f = np.array(sorted(set(dir_f)), np.int64)
log('fields: REL32', len(rel_f), 'DIR32(abs, own rule)', len(dir_f), 'ignored kinds', dict(nrec))
# cross-check with the reference .reloc for .text (should be identical)
def read_orig_relocs():
    rv, rsz = struct.unpack_from('<II', d, opt + 96 + 5 * 8); p = foff(base + rv); end = p + rsz; out = []
    while p < end:
        pg, bsz = struct.unpack_from('<II', d, p)
        if bsz == 0: break
        for i in range((bsz - 8) // 2):
            w = struct.unpack_from('<H', d, p + 8 + 2 * i)[0]
            if w >> 12 == 3: out.append(pg + (w & 0xfff))
        p += bsz
    return out
orig = read_orig_relocs()
otext = sorted(r for r in orig if TV - base <= r < TV - base + TS); odata = [r for r in orig if not (TV - base <= r < TV - base + TS)]
log('orig .reloc sites', len(orig), 'text', len(otext), 'identical to own set:', set(r - (TV - base) for r in otext) == set(dir_f.tolist()))

# ------------------------------------------------------------------ chains (fall-through / rel8 across blocks)
def rd32(arr, offs):
    o = np.asarray(offs, np.int64)
    return (arr[o].astype(np.int64) | (arr[o + 1].astype(np.int64) << 8) | (arr[o + 2].astype(np.int64) << 16) | (arr[o + 3].astype(np.int64) << 24))
def s32(v): return np.where(v >= 2 ** 31, v - 2 ** 32, v)
chain = np.zeros(nb, bool)     # chain[i]: block i must stay directly before block i+1
sweep_file = os.path.join(HERE, 'build', 'sweep.pkl'); os.makedirs(os.path.dirname(sweep_file), exist_ok=True)
sweep = None
if os.path.exists(sweep_file): sweep = pickle.load(open(sweep_file, 'rb'))
if a.sweep or sweep is None:
    import capstone
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32); md.skipdata = True
    TERM = ('ret', 'retn', 'jmp', 'int3', 'ud2', 'hlt', 'iretd', 'retf')
    fall = []; rel8x = []; rel32x = []
    tb = bytes(text)
    recset = set(rel_f.tolist())
    for bi in range(nb):
        s, e = int(bs[bi]), int(be[bi]); last = None; has_pad = tb[e - 1] in PAD if e > s else True
        for addr, size, mn, ops in md.disasm_lite(tb[s:e], s):
            last = (mn, addr, size)
            if size == 2 and (mn[0] == 'j' or mn.startswith('loop')):
                t = addr + 2 + struct.unpack_from('<b', tb, addr + 1)[0]
                if not (s <= t < e): rel8x.append((bi, addr, t))
            elif (size == 5 and tb[addr] in (0xe8, 0xe9)) or (size == 6 and tb[addr] == 0x0f and 0x80 <= tb[addr + 1] <= 0x8f):
                fo = addr + (1 if size == 5 else 2)
                t = fo + 4 + struct.unpack_from('<i', tb, fo)[0] + 0   # target offset (text-relative) if in text
                if 0 <= t < TS and not (s <= t < e) and fo not in recset: rel32x.append((bi, fo, t))
        if last and last[0] not in TERM and not has_pad: fall.append(bi)
    sweep = dict(fall=fall, rel8x=rel8x, rel32x=rel32x); pickle.dump(sweep, open(sweep_file, 'wb'))
    log('sweep done: fallthrough', len(fall), 'rel8 crossing', len(rel8x), 'rel32 leaving block not in records', len(rel32x))
if not a.no_chain:
    for bi in sweep['fall']:
        if bi + 1 < nb: chain[bi] = True
    bidx = lambda o: int(np.searchsorted(bs, o, 'right') - 1)
    for bi, addr, t in sweep['rel8x']:
        tbk = bidx(t); lo, hi = min(bi, tbk), max(bi, tbk)
        if hi - lo <= 8:
            for k in range(lo, hi): chain[k] = True
log('chained boundaries', int(chain.sum()), '; rel32 fields found only by sweep (extra DIS fields):', len(sweep['rel32x']))
# extra rel32 fields: only trust sweep finds inside gap blocks (blobs), where records may be absent
extra_rel = sorted(set(f for bi, f, t in sweep['rel32x'] if btype[bi] == 'gap'))
log('extra DIS rel32 fields used (gap blocks only):', len(extra_rel), 'ignored (in atoms):', len(sweep['rel32x']) - len(extra_rel))
rel_all = np.array(sorted(set(rel_f.tolist()) | set(extra_rel)), np.int64)

# ------------------------------------------------------------------ layout
sb = []     # super-blocks: lists of consecutive original block indices
i = 0
while i < nb:
    j = i
    while j < nb - 1 and chain[j]: j += 1
    sb.append(list(range(i, j + 1))); i = j + 1
def order_of(layout):
    if layout == 'G': return list(range(len(sb)))
    if layout == 'REV': return list(range(len(sb) - 1, -1, -1))
    if layout == 'Z': return list(np.random.default_rng(a.seed).permutation(len(sb)))
    if layout in ('U', 'R'):
        grp = collections.OrderedDict()
        for k, s_ in enumerate(sb):
            u = int(bunit[s_[0]]); key = ('u', u) if u >= 0 else ('s', k)
            grp.setdefault(key, []).append(k)
        seq = []
        for key, ks in grp.items(): seq += (ks[::-1] if layout == 'R' else ks)
        return seq
    raise SystemExit('unknown layout')
seq = order_of(a.layout)
NS = np.zeros(nb, np.int64); pos = 0
for k in seq:
    first = sb[k][0]; orig_start = int(bs[first])
    pos += (orig_start - pos) % 16          # keep address mod 16
    for bi in sb[k]:
        NS[bi] = pos; pos += int(be[bi] - bs[bi])
total = pos
NBRVA = (sizeofimage + 0xfff) & ~0xfff           # new section RVA (after everything incl. .reloc)
NBVA = base + NBRVA
log('layout', a.layout, 'new text size', hex(total), 'at', hex(NBVA), 'order changed for', sum(1 for i_, k in enumerate(seq) if i_ != k), 'of', len(sb), 'super-blocks')
def L_off(o):        # text offset -> new text offset
    o = np.asarray(o, np.int64); b = np.searchsorted(bs, o, 'right') - 1
    return NS[b] + (o - bs[b])
def L_va(v):         # VA -> new VA (VAs inside .text only)
    v = np.asarray(v, np.int64); m = (v >= TV) & (v < TV + TS); r = v.copy(); r[m] = NBVA + L_off(v[m] - TV); return r

# ------------------------------------------------------------------ build new text
new = bytearray(b'\xcc' * total)
tbb = bytes(text)
for bi in range(nb): new[NS[bi]:NS[bi] + be[bi] - bs[bi]] = tbb[bs[bi]:be[bi]]
nt = np.frombuffer(bytes(new), np.uint8).copy()
nsites = []
# REL32
fo_new = L_off(rel_all)
v = s32(rd32(text, rel_all)); T = TV + rel_all + 4 + v
Tn = L_va(T); newv = (Tn - (NBVA + fo_new + 4)) & 0xffffffff
for fo, nv in zip(fo_new.tolist(), newv.tolist()): struct.pack_into('<I', new, fo, nv)
log('REL32 rewritten', len(rel_all), '; targets inside .text', int(((T >= TV) & (T < TV + TS)).sum()))
# DIR32 (absolute addresses)
fo_new = L_off(dir_f); v = rd32(text, dir_f); vin = (v >= TV) & (v < TV + TS); vn = np.where(vin, L_va(v), v)
for fo, nv in zip(fo_new.tolist(), vn.tolist()): struct.pack_into('<I', new, fo, nv)
log('DIR32 rewritten', len(dir_f), '; pointing into .text', int(vin.sum()), '; outside (unchanged)', int((~vin).sum()))
new_text_sites = sorted((NBRVA + fo_new).tolist())

# ------------------------------------------------------------------ data -> code (BORROWED site list)
nd = 0
dfo = np.array([foff(base + r) for r in odata], np.int64)
dv = np.frombuffer(bytes(d), np.uint8)
dvals = rd32(dv, dfo); dm = (dvals >= TV) & (dvals < TV + TS)
dnew = L_va(dvals[dm])
for fo_, nv_ in zip(dfo[dm].tolist(), dnew.tolist()): struct.pack_into('<I', d, fo_, nv_)
nd = int(dm.sum())
log('data->code pointers rewritten (positions from reference .reloc, BORROWED):', nd)
# candidates not in .reloc (report)
odset = set(odata)
cand = 0; cand_bs = 0; candl = []
bsva = set((TV + bs).tolist())
for n_, va_, vs_, rp_, rs_ in secs:
    if n_ in ('.rdata', '.data'):
        arr = np.frombuffer(bytes(d[rp_:rp_ + (rs_ & ~3)]), '<u4')
        m = np.where((arr >= TV) & (arr < TV + TS))[0]
        for k in m.tolist():
            if (va_ + 4 * k) not in odset:
                cand += 1
                if int(arr[k]) in bsva: cand_bs += 1; candl.append((va_ + 4 * k + base, int(arr[k])))
log('data dwords with .text-range value but NOT in .reloc:', cand, '(equal to a block start:', cand_bs, ')')
if a.remap_unreloc:
    for va, v in candl: struct.pack_into('<I', d, foff(va), int(L_va(np.array([v]))[0]))

# ------------------------------------------------------------------ entry point, section, reloc
entry_va = base + struct.unpack_from('<I', d, opt + 16)[0]
struct.pack_into('<I', d, opt + 16, int(L_va(np.array([entry_va]))[0]) - base)
d[0x400:0x400 + TS] = b'\xcc' * TS                       # old .text: any stale reference faults
raw_new = (total + 0x1ff) & ~0x1ff
rawp = (len(d) + 0x1ff) & ~0x1ff; d += bytes(rawp - len(d))
d += bytes(new) + bytes(raw_new - total)
# section header #8
sh = so + 40 * nsec
d[sh:sh + 40] = struct.pack('<8sIIIIIIHHI', b'.ntext', total, NBRVA, raw_new, rawp, 0, 0, 0, 0, 0x60000020)
struct.pack_into('<H', d, fh + 2, nsec + 1)
struct.pack_into('<I', d, opt + 56, NBRVA + ((total + 0xfff) & ~0xfff))
struct.pack_into('<I', d, opt + 4, struct.unpack_from('<I', d, opt + 4)[0] + raw_new)   # SizeOfCode
# .reloc: data sites (reference positions) + new text sites
sites = sorted(odata + new_text_sites); blk = bytearray(); i = 0
while i < len(sites):
    pg = sites[i] & ~0xfff; ent = []
    while i < len(sites) and (sites[i] & ~0xfff) == pg: ent.append(0x3000 | (sites[i] & 0xfff)); i += 1
    if len(ent) & 1: ent.append(0)
    blk += struct.pack('<II', pg, 8 + 2 * len(ent)) + b''.join(struct.pack('<H', x) for x in ent)
rrva, rsz = struct.unpack_from('<II', d, opt + 96 + 5 * 8)
_, rvs, rrp, rrs = S['.reloc']
assert len(blk) <= rrs, ('reloc table too large', len(blk), rrs)
d[rrp:rrp + rrs] = bytes(blk) + bytes(rrs - len(blk))
struct.pack_into('<II', d, opt + 96 + 5 * 8, rrva, len(blk))
log('.reloc rewritten:', len(sites), 'sites,', len(blk), 'bytes (was', rsz, ')')
# checksum
import pefile
struct.pack_into('<I', d, opt + 64, 0); struct.pack_into('<I', d, opt + 64, pefile.PE(data=bytes(d)).generate_checksum())
open(out, 'wb').write(d)
json.dump(dict(layout=a.layout, out=out, blocks=nb, superblocks=len(sb), total=total, new_base_va=NBVA, entry_new=int(L_va(np.array([entry_va]))[0]),
               rel32=len(rel_all), dir32=len(dir_f), data_to_code=nd, extra_dis_rel32=len(extra_rel), chained=int(chain.sum()),
               unreloc_candidates=cand, unreloc_block_start=cand_bs),
          open(os.path.join(HERE, 'build', 'last_%s.json' % a.layout), 'w'), indent=1)
log('wrote', out, len(d))
