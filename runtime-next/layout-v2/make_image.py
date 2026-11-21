r"""layout-v2 / M4b + M4c: self-assembled image with moved code AND moved data.
No reference exe file is the starting point. PE headers are written here, in our own layout:
  .data(+bss) .rdata(chunks reversed) CONST .tls .text .rsrc .reloc   starting at RVA 0x1082000 (the original image range 0x401000-0x1481000 is left UNMAPPED,
  so any stale absolute address faults).
Sources:
  code      build-v7 FalloutNV_v7_strict.exe .text (our placed pieces + gap blocks) + the bytes only the filled image has (borrowed fields/failed pieces, count logged)
  fields    build-v7 relocs_v7.tsv.gz (+ inferred_literals_v7.json) for .text (OWN); block boundaries units.json + contrib_pieces.json
  data      data-v3\out\*.obj raw bytes; every pointer field = obj relocation (symbol + addend) resolved to the NEW address of the symbol
  imports   direct-v1\build_imports.py spec re-based to the new IAT/import-directory addresses
  .rsrc     direct-v1\build_rsrc.py at the new RVA (binary inputs from the installed exe at build time)
  .reloc    generated here (code sites + data pointer sites)
usage: python make_image.py --layout G|U|R|REV|Z [--seed N] [--out F] [--keep-data-order]"""
import sys, os, struct, json, collections, argparse, time, pickle, bisect
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
RN = (__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\path\to\Decompilation') + r'\runtime-next')
sys.path.insert(0, RN + r'\direct-v1'); sys.path.insert(0, (__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\path\to\Decompilation') + r'\fnv_decomp\tools'))
import model
from model import TV, TS, B7
import build_imports, build_rsrc
from compare import Coff
import pefile

ap = argparse.ArgumentParser()
ap.add_argument('--layout', default='REV'); ap.add_argument('--seed', type=int, default=1)
ap.add_argument('--out', default=None); ap.add_argument('--keep-data-order', action='store_true')
ap.add_argument('--text-first', action='store_true', help='put .text first (default: data sections first)')
ap.add_argument('--no-chain', action='store_true')
ap.add_argument('--vr', choices=['skip', 'remap'], default='skip', help='297 value-rule pointer fields (no reference reloc; may be accidental ints): skip = keep original value')
a = ap.parse_args()
out = a.out or os.path.join(HERE, 'FalloutNV_image_%s.exe' % a.layout)
t0 = time.time()
def log(*x): print('[%5.1fs]' % (time.time() - t0), *x, flush=True)
BASE = 0x400000
SECT_ALIGN, FILE_ALIGN = 0x1000, 0x200
START_RVA = int(os.environ.get("START_RVA", "0x1000"), 0)
def up(x, al): return (x + al - 1) // al * al

# ------------------------------------------------------------------ code source: strict + borrowed bytes
def sec_text(path):
    return np.fromfile(path, np.uint8)
strict = sec_text(os.path.join(B7, 'strict_text.bin')); filled = sec_text(os.path.join(B7, 'filled_text.bin'))
diff = np.where(strict != filled)[0]
text = strict.copy(); text[diff] = filled[diff]
REF_CODE_BYTES = int(len(diff))
log('code: strict .text + %d bytes from the filled image (borrowed fields / failed pieces)' % REF_CODE_BYTES)

# ------------------------------------------------------------------ blocks (same model as make_layout.py)
atoms = model.load_atoms(); PAD = (0xcc, 0x00, 0x90)
def padrun(p, lim):
    while p < lim and text[p] in PAD: p += 1
    return p
blocks = []; pos = 0
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
log('blocks', nb, collections.Counter(btype))

# ------------------------------------------------------------------ fields in .text
recs = model.load_records(); inferred = json.load(open(B7 + r'\inferred_literals_v7.json'))
IMGLO, IMGHI = BASE, BASE + 0x1081000
rel_f = []; dir_f = []
for off, kind, status, origin, exp, tsec in recs:
    if kind == 'REL32': rel_f.append(off)
    elif kind == 'DIR32' and status in ('agree', 'disagree') and exp >= 0 and tsec != '-1' and IMGLO <= exp < IMGHI: dir_f.append(off)
for k in inferred:
    o = int(k, 16) - TV
    if 0 <= o < TS: dir_f.append(o)
rel_f = np.array(sorted(set(rel_f)), np.int64); dir_f = np.array(sorted(set(dir_f)), np.int64)
import hashlib, capstone
sig = hashlib.sha1(bs.tobytes() + be.tobytes() + text.tobytes()).hexdigest()[:12]
sweep_file = os.path.join(HERE, 'build', 'sweep_%s.pkl' % sig)
if os.path.exists(sweep_file): sweep = pickle.load(open(sweep_file, 'rb'))
else:
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32); md.skipdata = True
    TERM = ('ret', 'retn', 'jmp', 'int3', 'ud2', 'hlt', 'iretd', 'retf'); fall = []; rel8x = []; rel32x = []; tb = bytes(text); recset = set(rel_f.tolist())
    for bi in range(nb):
        s_, e_ = int(bs[bi]), int(be[bi]); last = None; has_pad = tb[e_ - 1] in PAD if e_ > s_ else True
        for addr, size, mn, ops in md.disasm_lite(tb[s_:e_], s_):
            last = mn
            if size == 2 and (mn[0] == 'j' or mn.startswith('loop')):
                t = addr + 2 + struct.unpack_from('<b', tb, addr + 1)[0]
                if not (s_ <= t < e_): rel8x.append((bi, addr, t))
            elif (size == 5 and tb[addr] in (0xe8, 0xe9)) or (size == 6 and tb[addr] == 0x0f and 0x80 <= tb[addr + 1] <= 0x8f):
                fo = addr + (1 if size == 5 else 2); t = fo + 4 + struct.unpack_from('<i', tb, fo)[0]
                if 0 <= t < TS and not (s_ <= t < e_) and fo not in recset: rel32x.append((bi, fo, t))
        if last and last not in TERM and not has_pad: fall.append(bi)
    sweep = dict(fall=fall, rel8x=rel8x, rel32x=rel32x); pickle.dump(sweep, open(sweep_file, 'wb'))
    log('sweep computed for the current block set:', len(fall), 'fall-through,', len(rel8x), 'rel8 crossing,', len(rel32x), 'rel32 not in records')
extra_rel = sorted(set(f for bi, f, t in sweep['rel32x'] if btype[bi] == 'gap'))
rel_all = np.array(sorted(set(rel_f.tolist()) | set(extra_rel)), np.int64)
chain = np.zeros(nb, bool)
if not a.no_chain:
    for bi in sweep['fall']:
        if bi + 1 < nb: chain[bi] = True
    for bi, addr, t in sweep['rel8x']:
        tbk = int(np.searchsorted(bs, t, 'right') - 1); lo, hi = min(bi, tbk), max(bi, tbk)
        if hi - lo <= 8: chain[lo:hi] = True
log('fields: REL32', len(rel_all), '(+%d DIS in gaps)' % len(extra_rel), 'DIR32', len(dir_f), 'chained', int(chain.sum()))
def rd32(arr, offs):
    o = np.asarray(offs, np.int64)
    return (arr[o].astype(np.int64) | (arr[o + 1].astype(np.int64) << 8) | (arr[o + 2].astype(np.int64) << 16) | (arr[o + 3].astype(np.int64) << 24))
def s32(v): return np.where(v >= 2 ** 31, v - 2 ** 32, v)

# ------------------------------------------------------------------ code layout
sb = []; i = 0
while i < nb:
    j = i
    while j < nb - 1 and chain[j]: j += 1
    sb.append(list(range(i, j + 1))); i = j + 1
def order_of(layout):
    if layout == 'G': return list(range(len(sb)))
    if layout == 'REV': return list(range(len(sb) - 1, -1, -1))
    if layout == 'Z': return list(np.random.default_rng(a.seed).permutation(len(sb)))
    grp = collections.OrderedDict()
    for k, s_ in enumerate(sb):
        u = int(bunit[s_[0]]); grp.setdefault(('u', u) if u >= 0 else ('s', k), []).append(k)
    seq = []
    for ks in grp.values(): seq += (ks[::-1] if layout == 'R' else ks)
    return seq
seq = order_of(a.layout)
NS = np.zeros(nb, np.int64); pos = 0
for k in seq:
    pos += (int(bs[sb[k][0]]) - pos) % 16
    for bi in sb[k]: NS[bi] = pos; pos += int(be[bi] - bs[bi])
text_total = pos

# ------------------------------------------------------------------ data from data-v3 objects
D3 = os.path.join(B7, 'data-v3', 'out')
sj = json.load(open(os.path.join(B7, 'data-v3', 'symbolic.json'))); csym = json.load(open(os.path.join(D3, 'code_symbols.json')))
manifest = json.load(open(os.path.join(D3, 'manifest.json')))
OBJSEC = {'.rdata': '.rdata', '.data': '.data', '.tls': '_TLS', 'CONST': '_CONSTPE'}
bss = sj['bss']; secinfo = sj['sections']
chunks = {}       # file -> dict(sec, va, size, data(bytearray), relocs[(off,symname,add)])
alladdr = {}
for m in manifest:
    c = Coff(os.path.join(D3, m['file'] + '.obj')); ch = None
    for i_, s in enumerate(c.sections):
        if not s: continue
        if s['name'] == OBJSEC[m['section']]:
            ch = dict(sec=m['section'], va=m['va'], size=m['size'], data=bytearray(s['data']), relocs=[], idx=i_)
            assert len(ch['data']) == m['size'], (m['file'], len(ch['data']), m['size'])
        elif s['name'] == '.bss': bsec = (i_, s)
    for si, sy in c.symbols.items():
        if sy['storage'] == 2 and sy['section'] > 0:
            if sy['section'] == ch['idx']: alladdr[sy['name']] = m['va'] + sy['value']
            elif m['file'] == 'data_00' and c.sections[sy['section']]['name'] == '.bss': alladdr[sy['name']] = bss['va'] + sy['value']
    for off, ri, kind in c.sections[ch['idx']]['relocs']:
        assert kind == 6
        add, = struct.unpack_from('<i', ch['data'], off)
        ch['relocs'].append((off, c.symbols[ri]['name'], add))
    chunks[m['file']] = ch
log('data objects:', {k: (v['size'], len(v['relocs'])) for k, v in chunks.items()}, 'relocations', sum(len(v['relocs']) for v in chunks.values()))
# ---- M3 phase 1 (opt-in FNV_M3=1): the bytes of the generated global definitions come from OUR compiled object (m3_data.obj), overlaid at their original offsets.
# data-v3 emitted these ranges as zeros (DV3_SKIP), so a non-zero byte here can only come from the compiled definitions.
M3_STAT = None
M3_ALIGNED16 = []
if os.environ.get('FNV_M3') == '1':
    sys.path.insert(0, RN + r'\m3'); import splice
    M3_STAT = collections.Counter(); M3_CLAIMS = splice.RangeClaims()
    for r_ in splice.load(os.path.join(B7, 'm3', 'm3_manifest.json'), os.path.join(B7, 'm3', 'm3_data.obj')):
        if r_['entry'].get('align') == 16: M3_ALIGNED16.append((r_['va'], r_['entry']['sym']))
        n_ = len(r_['data']); va_ = r_['va']; sec_ = r_['entry']['section']
        ch_ = [c_ for c_ in chunks.values() if c_['sec'] == sec_ and c_['va'] <= va_ and va_ + n_ <= c_['va'] + c_['size']]
        assert len(ch_) == 1, hex(va_)
        ch_ = ch_[0]; o_ = va_ - ch_['va']
        M3_CLAIMS.add(va_, n_)
        assert not any(ch_['data'][o_:o_ + n_]), 'range not zeroed by DV3_SKIP: %x' % va_
        # phase 1b: pointer fields. The captured relocations inside the overlaid range are dropped (DV3_SKIP already removed them from the data-v3 object, so normally 0)
        # and ours are added, symbols mapped to their original VA through alladdr; the common rewrite loop below then emits Lone(target)+addend and the .reloc site.
        nd_ = len(ch_['relocs']); ch_['relocs'] = [x_ for x_ in ch_['relocs'] if not (o_ <= x_[0] < o_ + n_)]; M3_STAT['captured_relocs_dropped'] += nd_ - len(ch_['relocs'])
        for (ro_, rnm_, radd_), rva_ in zip(r_['relocs'], r_['reloc_va']):
            assert alladdr.get(rnm_, rva_) == rva_, (rnm_, hex(rva_))
            alladdr[rnm_] = rva_; ch_['relocs'].append((o_ + ro_, rnm_, radd_)); M3_STAT['relocs_added'] += 1
            M3_STAT['relocs_to_code' if TV <= rva_ < TV + TS else 'relocs_to_data'] += 1
        ch_['data'][o_:o_ + n_] = r_['data']
        M3_STAT['globals'] += 1; M3_STAT['bytes_overlaid'] += n_; M3_STAT['nonzero_bytes_overlaid'] += sum(1 for b_ in r_['data'] if b_); M3_STAT['bytes_' + sec_] += n_
    log('M3 overlay: bytes taken from our compiled m3_data.obj:', dict(M3_STAT), 'data relocations now', sum(len(v['relocs']) for v in chunks.values()))
# ---- M3 batch 5 (opt-in FNV_M3_DV1=1, requires FNV_M3=1): pieces of OUR unit objects placed by data-v1 (strings, constants, vtables, RTTI, EH tables, ...) overlaid the same way.
# Pointer fields are DIR32 relocations of the compiled objects, re-linked to the VA our resolution produced (synthetic symbol 'M5T_<va>', addend 0).
DV1_STAT = None
if os.environ.get('FNV_M3_DV1') == '1':
    assert M3_STAT is not None, 'FNV_M3_DV1=1 requires FNV_M3=1'
    DV1_STAT = collections.Counter(); DV1_KIND = collections.defaultdict(collections.Counter)
    _bysec = collections.defaultdict(list)
    for c_ in chunks.values(): _bysec[c_['sec']].append(c_)
    for r_ in splice.load_dv1(os.path.join(B7, 'm3', 'dv1_pieces.json')):
        n_ = len(r_['data']); va_ = r_['va']; sec_ = r_['entry']['section']
        ch_ = [c_ for c_ in _bysec[sec_] if c_['va'] <= va_ and va_ + n_ <= c_['va'] + c_['size']]
        assert len(ch_) == 1, hex(va_)
        ch_ = ch_[0]; o_ = va_ - ch_['va']
        M3_CLAIMS.add(va_, n_)
        assert not any(ch_['data'][o_:o_ + n_]), 'range not zeroed by DV3_SKIP: %x' % va_
        nd_ = len(ch_['relocs']); ch_['relocs'] = [x_ for x_ in ch_['relocs'] if not (o_ <= x_[0] < o_ + n_)]; DV1_STAT['captured_relocs_dropped'] += nd_ - len(ch_['relocs'])
        kd_ = r_['entry']['kind']
        for (ro_, rnm_, radd_), rva_ in zip(r_['relocs'], r_['reloc_va']):
            assert alladdr.get(rnm_, rva_) == rva_, (rnm_, hex(rva_))
            alladdr[rnm_] = rva_; ch_['relocs'].append((o_ + ro_, rnm_, radd_)); DV1_STAT['relocs_added'] += 1; DV1_KIND[kd_]['relocs'] += 1
            DV1_STAT['relocs_to_code' if TV <= rva_ < TV + TS else 'relocs_to_data'] += 1
        ch_['data'][o_:o_ + n_] = r_['data']
        DV1_STAT['pieces'] += 1; DV1_STAT['bytes_overlaid'] += n_; DV1_STAT['bytes_' + sec_] += n_; DV1_KIND[kd_]['pieces'] += 1; DV1_KIND[kd_]['bytes'] += n_
    DV1_STAT = dict(DV1_STAT, by_kind={k_: dict(v_) for k_, v_ in sorted(DV1_KIND.items())})
    log('M3 batch 5 overlay: bytes taken from our compiled unit objects (data-v1 pieces):', DV1_STAT, 'data relocations now', sum(len(v['relocs']) for v in chunks.values()))
# ---- new section placement
sec_order = ['.rdata', '.data', 'CONST', '.tls', '.text', '.rsrc', '.reloc'] if not a.text_first else ['.text', '.rdata', '.data', 'CONST', '.tls', '.rsrc', '.reloc']
sec_order = ['.data', '.rdata', 'CONST', '.tls', '.text', '.rsrc', '.reloc'] if not a.text_first else sec_order
rdata_files = ['rdata_00', 'rdata_01', 'rdata_02', 'rdata_03']
rdata_seq = rdata_files if a.keep_data_order else rdata_files[::-1]
# per-section sizes: chunk placement keeps va mod 16
newchunk = {}   # file -> new va
sec_size = {}   # virtual size
def place(sec):
    pos = 0
    if sec == '.rdata':
        for f in rdata_seq:
            ch = chunks[f]; pos += (ch['va'] - pos) % 16; newchunk[f] = ('off', pos); pos += ch['size']
    elif sec == '.data':
        ch = chunks['data_00']; newchunk['data_00'] = ('off', 0); pos = ch['size'] + bss['size']   # bss tail rigid after data
    elif sec == 'CONST': newchunk['const_00'] = ('off', 0); pos = chunks['const_00']['size']
    elif sec == '.tls': newchunk['tls_00'] = ('off', 0); pos = chunks['tls_00']['size']
    return pos
virt = {s: place(s) for s in ('.rdata', '.data', 'CONST', '.tls')}
# raw sizes
raw = {'.rdata': up(virt['.rdata'], FILE_ALIGN), '.data': up(chunks['data_00']['size'], FILE_ALIGN), 'CONST': FILE_ALIGN, '.tls': up(chunks['tls_00']['size'], FILE_ALIGN)}
virt['.text'] = text_total; raw['.text'] = up(text_total, FILE_ALIGN)
# .rsrc size from the builder (RVA independent size)
rsrc_probe = build_rsrc.build(0x1000); virt['.rsrc'] = len(rsrc_probe); raw['.rsrc'] = up(len(rsrc_probe), FILE_ALIGN)
# .reloc size unknown yet: reserve generously (old table 735 KB)
RELOC_RESERVE = up(900000, FILE_ALIGN); virt['.reloc'] = RELOC_RESERVE; raw['.reloc'] = RELOC_RESERVE
rva = {}; cur = START_RVA
for s in sec_order:
    rva[s] = cur; cur = up(cur + max(virt[s], 1), SECT_ALIGN)
if os.environ.get('DATA_ORIG') or os.environ.get('KEEP_SECS'):   # bisect aid: listed data sections stay at their ORIGINAL RVAs (identity map), text at 0x1000 (G layout fits), the others after the original image
    keep = (os.environ.get('KEEP_SECS') or '.rdata,.data,.tls,CONST').split(',')
    ORIG = {'.rdata': 0xbdf000, '.data': 0xd83000, '.tls': 0xe72000, 'CONST': 0xe73000}
    assert text_total <= 0xbde000
    rva = {'.text': 0x1000}; cur = 0x1009000
    for k_ in ('.rdata', '.data', '.tls', 'CONST'):
        if k_ in keep: rva[k_] = ORIG[k_]
        else: rva[k_] = cur; cur = up(cur + virt[k_], 0x1000)
    rva['.rsrc'] = cur; cur = up(cur + virt['.rsrc'], 0x1000); rva['.reloc'] = cur; cur = up(cur + virt['.reloc'], 0x1000)
    sec_order = sorted(rva, key=lambda k_: rva[k_])
HOLE = min(rva.values()) > 0x1000
if HOLE:
    sec_order = ['.hole'] + sec_order; rva['.hole'] = 0x1000; virt['.hole'] = min(v for k_, v in rva.items() if k_ != '.hole') - 0x1000; raw['.hole'] = 0
    CH_HOLE = 0x00000080     # uninitialised data, no R/W/X: PAGE_NOACCESS, the old image range faults
SIZE_OF_IMAGE = cur
log('sections', {s: (hex(rva[s]), hex(virt[s])) for s in sec_order})
# ---- maps old VA -> new VA
rng = []   # (orig_lo, orig_hi, new_lo)
for f, ch in chunks.items():
    nv = BASE + rva[ch['sec']] + newchunk[f][1]
    hi = ch['va'] + ch['size'] + (bss['size'] if f == 'data_00' else 0)
    rng.append((ch['va'], hi, nv))
rng.sort(); r_lo = np.array([r[0] for r in rng], np.int64); r_hi = np.array([r[1] for r in rng], np.int64); r_nw = np.array([r[2] for r in rng], np.int64)
NBVA = BASE + rva['.text']
def L_off(o):
    o = np.asarray(o, np.int64); b = np.searchsorted(bs, o, 'right') - 1; return NS[b] + (o - bs[b])
def Lall(v):
    v = np.asarray(v, np.int64); r = v.copy()
    m = (v >= TV) & (v < TV + TS); r[m] = NBVA + L_off(v[m] - TV)
    k = np.searchsorted(r_lo, v, 'right') - 1; kk = np.maximum(k, 0)
    md = (k >= 0) & (v < r_hi[kk]) & ~m
    r[md] = r_nw[kk[md]] + (v[md] - r_lo[kk[md]])
    # one-past-the-end pointers of a section's last chunk
    return r
# one-past-end special cases
END_EXTRA = {}
for f, ch in chunks.items():
    hi = ch['va'] + ch['size'] + (bss['size'] if f == 'data_00' else 0)
    END_EXTRA[hi] = f
def Lone(v):
    r = int(Lall(np.array([v]))[0])
    if r == v and v in END_EXTRA: r = int(Lall(np.array([v - 1]))[0]) + 1     # one-past-the-end of a section's last chunk
    return r
for aligned_va, aligned_sym in M3_ALIGNED16:
    if Lone(aligned_va) % 16: raise ValueError('translated M3 destination lacks 16-byte alignment: %s' % aligned_sym)
# ------------------------------------------------------------------ rewrite code
new = bytearray(b'\xcc' * text_total); tb = bytes(text)
for bi in range(nb): new[NS[bi]:NS[bi] + be[bi] - bs[bi]] = tb[bs[bi]:be[bi]]
fo_new = L_off(rel_all); v = s32(rd32(text, rel_all)); T = TV + rel_all + 4 + v
Tn = Lall(T); newv = (Tn - (NBVA + fo_new + 4)) & 0xffffffff
for fo, nv in zip(fo_new.tolist(), newv.tolist()): struct.pack_into('<I', new, fo, nv)
rel_to_data = int(((T < TV) | (T >= TV + TS)).sum())
dfo_new = L_off(dir_f); dv = rd32(text, dir_f); dn = Lall(dv)
unmapped = [(int(x)) for x in dv[(dn == dv) & (dv >= 0x1000000)] if int(x) not in END_EXTRA]
# one-past-end values
for idx, x in enumerate(dv.tolist()):
    if x in END_EXTRA and dn[idx] == x: dn[idx] = Lone(x - 1) + 1
for fo, nv in zip(dfo_new.tolist(), dn.tolist()): struct.pack_into('<I', new, fo, nv)
chg = int((dn != dv).sum())
log('REL32 rewritten', len(rel_all), '(non-.text targets %d); DIR32 rewritten %d, changed %d, unchanged-but-large-value %d' % (rel_to_data, len(dir_f), chg, len(unmapped)))
code_sites = (rva['.text'] + dfo_new).tolist()
# ------------------------------------------------------------------ rewrite data
data_sites = []; stat = collections.Counter(); bad = []
VR = {(f_[0], f_[1]) for f_ in sj['fields'] if f_[4] == 'value-rule'}
for f, ch in chunks.items():
    base_va = ch['va']; nchunk_va = BASE + rva[ch['sec']] + newchunk[f][1]
    for off, nm, add in ch['relocs']:
        va = alladdr[nm] if nm in alladdr else csym[nm]['va']
        if a.vr == 'skip' and (ch['sec'], ch['va'] - secinfo[ch['sec']]['va'] + off) in VR:
            struct.pack_into('<I', ch['data'], off, (va + add) & 0xffffffff); stat['value-rule-kept-literal'] += 1; continue
        nv = Lone(va) + add
        # sanity: symbol+addend must map consistently (same block/chunk)
        t = va + add
        if Lone(t) != nv and not (t in END_EXTRA):
            bad.append((f, off, nm, add)); stat['inconsistent'] += 1
        struct.pack_into('<I', ch['data'], off, nv & 0xffffffff)
        data_sites.append(nchunk_va + off - BASE); stat['code' if TV <= va < TV + TS else 'data'] += 1
log('data pointer fields rewritten (from obj relocations):', dict(stat), 'inconsistent symbol+addend:', len(bad), bad[:5])
# ---- imports re-based
spec = json.load(open(build_imports.SPEC))
old_dir_va = BASE + spec['import_dir_rva']
new_dir_rva = Lone(old_dir_va) - BASE
for d_ in spec['dlls']:
    d_['iat'] = Lone(BASE + d_['iat']) - BASE
iat_new = {Lone(BASE + x['iat']) - BASE for x in []}
spec['import_dir_rva'] = new_dir_rva
r = build_imports.build(spec)
def put_data(va_old, nbytes_data, new_rva):   # write bytes at an RVA that lies in a data chunk
    for f, ch in chunks.items():
        nv = BASE + rva[ch['sec']] + newchunk[f][1]
        if nv <= BASE + new_rva < nv + ch['size']:
            o = BASE + new_rva - nv; assert o + len(nbytes_data) <= ch['size']; ch['data'][o:o + len(nbytes_data)] = nbytes_data; return f
    raise ValueError('rva not in a data chunk')
f1 = put_data(None, r['region'], r['region_rva']); f2 = put_data(None, r['iat'], r['iat_rva'])
IAT_RVA, IAT_SIZE = r['iat_rva'], len(r['iat'])
log('imports re-based: dir rva', hex(r['region_rva']), 'IAT rva', hex(IAT_RVA), 'in', f1, f2)
# ---- TLS directory (original VA 0x112147c = RVA 0xd0147c + base) : position moves with its chunk
tls_va_old = BASE + 0xd0147c; tls_rva_new = Lone(tls_va_old) - BASE
# ------------------------------------------------------------------ rsrc, reloc
rsrc = build_rsrc.build(rva['.rsrc'])
sites = sorted(set(code_sites + data_sites)); blk = bytearray(); i = 0
while i < len(sites):
    pg = sites[i] & ~0xfff; ent = []
    while i < len(sites) and (sites[i] & ~0xfff) == pg: ent.append(0x3000 | (sites[i] & 0xfff)); i += 1
    if len(ent) & 1: ent.append(0)
    blk += struct.pack('<II', pg, 8 + 2 * len(ent)) + b''.join(struct.pack('<H', x) for x in ent)
assert len(blk) <= RELOC_RESERVE
virt['.reloc'] = len(blk); raw['.reloc'] = up(len(blk), FILE_ALIGN)
log('.reloc:', len(sites), 'sites', len(blk), 'bytes')
# recompute section layout (reloc size shrank): rva of .reloc unchanged (last)
SIZE_OF_IMAGE = up(max(rva[s_] + virt[s_] for s_ in sec_order), SECT_ALIGN)
# ------------------------------------------------------------------ section contents
content = {}
for s in sec_order:
    if s == '.hole': content[s] = b''
    elif s == '.text': content[s] = bytes(new)
    elif s == '.rsrc': content[s] = rsrc
    elif s == '.reloc': content[s] = bytes(blk)
    elif s == '.rdata':
        buf = bytearray(virt['.rdata'])
        for f in rdata_seq: buf[newchunk[f][1]:newchunk[f][1] + chunks[f]['size']] = chunks[f]['data']
        content[s] = bytes(buf)
    elif s == '.data': content[s] = bytes(chunks['data_00']['data'])
    elif s == 'CONST': content[s] = bytes(chunks['const_00']['data'])
    elif s == '.tls': content[s] = bytes(chunks['tls_00']['data'])
CH = {'.hole': int(os.environ.get('HOLE_CH','0x80'),0), '.text': 0x60000020, '.rdata': 0x40000040, '.data': 0xC0000040, 'CONST': 0xC0000040, '.tls': 0xC0000040, '.rsrc': 0x40000040, '.reloc': 0x42000040}
# ------------------------------------------------------------------ headers (written here)
HDR = 0x400
img = bytearray(HDR)
img[0:64] = b'MZ' + bytes(58) + struct.pack('<I', 0x80)
struct.pack_into('<HHHHHHHHHHHHH', img, 2, 0x90, 3, 0, 4, 0, 0xffff, 0, 0xb8, 0, 0, 0, 0x40, 0)   # classic DOS header values
img[0x40:0x80] = bytes(0x40)
pe_off = 0x80
img[pe_off:pe_off + 4] = b'PE\0\0'
ns = len(sec_order)
struct.pack_into('<HHIIIHH', img, pe_off + 4, 0x14c, ns, 0x4E0D50ED, 0, 0, 224, 0x102)
o = pe_off + 24
size_code = raw['.text']; size_init = sum(raw[s] for s in sec_order if s != '.text'); size_uninit = bss['size']
struct.pack_into('<HBBIIIIII', img, o, 0x10b, 9, 0, size_code, size_init, size_uninit, Lone(0xecc4db) - BASE, rva['.text'], rva['.data'])
struct.pack_into('<IIIHHHHHHIIIIHHIIIIII', img, o + 28, BASE, SECT_ALIGN, FILE_ALIGN, 5, 0, 0, 0, 5, 0, 0, SIZE_OF_IMAGE, HDR, 0, 2, 0x8000, 0x100000, 0x1000, 0x100000, 0x1000, 0, 16)
dd = o + 96
def setdd(i, r_, s_): struct.pack_into('<II', img, dd + 8 * i, r_, s_)
setdd(1, r['region_rva'], r['dir_size']); setdd(2, rva['.rsrc'], len(rsrc)); setdd(5, rva['.reloc'], len(blk))
setdd(9, tls_rva_new, 0x18); setdd(12, IAT_RVA, IAT_SIZE)
so = o + 224; fpos = HDR
rawptr = {}
for k, s in enumerate(sec_order):
    rawptr[s] = fpos
    struct.pack_into('<8sIIIIIIHHI', img, so + 40 * k, s.encode(), virt[s], rva[s], raw[s], fpos if raw[s] else 0, 0, 0, 0, 0, CH[s]); fpos += raw[s]
for s in sec_order:
    c = content[s]; img += bytes(rawptr[s] - len(img)); img += c + bytes(raw[s] - len(c))
struct.pack_into('<I', img, o + 64, 0)
struct.pack_into('<I', img, o + 64, pefile.PE(data=bytes(img)).generate_checksum())
open(out, 'wb').write(img)
log('wrote', out, len(img))
json.dump(dict(layout=a.layout, out=out, sections={s: dict(rva=rva[s], virt=virt[s], raw=raw[s]) for s in sec_order}, reference_code_bytes=REF_CODE_BYTES,
               data_fields=dict(stat), **({'m3_overlay': dict(M3_STAT)} if M3_STAT else {}), **({'dv1_overlay': DV1_STAT} if DV1_STAT else {}), rel32=len(rel_all), dir32=len(dir_f), entry=Lone(0xecc4db)),
          open(os.path.join(HERE, 'build', 'image_%s.json' % a.layout), 'w'), indent=1)
np.savez(os.path.join(HERE, 'build', 'map_%s.npz' % a.layout), bs=bs, be=be, NS=NS, nbva=np.array([NBVA]))
