"""link-v2 relcheck.py: layout-aware base-reloc check. Original reloc sites (reference exe .reloc) are mapped to their new VA through the C_/D_ labels of linked.map (nearest label
below + offset), original pointer values to their new target the same way; then compare against our exe: (a) is the new site in our .reloc, (b) does our file hold the mapped value.
Also lists our relocs that have no original counterpart. usage: python -I relcheck.py [exe]"""
import bisect, collections, json, re, struct, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE.parent / 'data-v3'))
from common import REF
exe = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / 'FalloutNV_linked.exe'
def load(p):
    d = Path(p).read_bytes(); pe = struct.unpack_from('<I', d, 0x3c)[0]; n = struct.unpack_from('<H', d, pe + 6)[0]; so = pe + 24 + struct.unpack_from('<H', d, pe + 20)[0]
    secs = [struct.unpack_from('<8sIIII', d, so + 40 * i) for i in range(n)]; rr, rs = struct.unpack_from('<II', d, pe + 24 + 96 + 40); base, = struct.unpack_from('<I', d, pe + 52)
    return d, secs, rr, rs, base
def relocs(d, secs, rr, rs):
    off = lambda rva: next(ro + rva - va for _, vs, va, rsz, ro in secs if va <= rva < va + max(vs, rsz))
    p = off(rr); out = set(); e = p + rs
    while p < e:
        pg, bs = struct.unpack_from('<II', d, p)
        if bs == 0: break
        for k in range((bs - 8) // 2):
            w, = struct.unpack_from('<H', d, p + 8 + 2 * k)
            if w >> 12 == 3: out.add(pg + (w & 0xfff))
        p += bs
    return out
od, osec, orr, ors, obase = load(REF); nd, nsec, nrr, nrs, nbase = load(exe)
orel = {x + obase for x in relocs(od, osec, orr, ors)}; nrel = {x + nbase for x in relocs(nd, nsec, nrr, nrs)}
def rdv(d, secs, base, va, n=4):
    rva = va - base
    for _, vs, sva, rsz, ro in secs:
        if sva <= rva < sva + rsz: return d[ro + rva - sva: ro + rva - sva + n]
    return None
lab = []
for l in open(HERE / 'linked.map', errors='replace'):
    m = re.match(r'\s*[0-9a-f]{4}:[0-9a-f]{8}\s+([CD])_([0-9a-f]{8})\s+([0-9a-f]{8})\s', l)
    if m: lab.append((int(m.group(2), 16), int(m.group(3), 16), m.group(1)))
lab.sort(); keys = [x[0] for x in lab]
# data section VA ranges in the ORIGINAL (to pick D vs C labels)
def kind(va):
    rva = va - obase
    for n, vs, sva, rsz, ro in osec:
        if sva <= rva < sva + max(vs, rsz): return 'C' if n.rstrip(b'\0') == b'.text' else 'D'
    return None
labC = [x for x in lab if x[2] == 'C']; labD = [x for x in lab if x[2] == 'D']
kC = [x[0] for x in labC]; kD = [x[0] for x in labD]
def newva(va, exact=False):
    k = kind(va)
    if k is None: return None
    L, K = (labC, kC) if k == 'C' else (labD, kD)
    i = bisect.bisect_right(K, va) - 1
    if i < 0: return None
    if exact and L[i][0] != va: return None
    if va - L[i][0] > 0x10000: return None
    return L[i][1] + (va - L[i][0])
stat = collections.Counter(); bad = []
mapped_new = set()
for s in sorted(orel):
    if s + 4 > 0xffffffff: continue
    ns = newva(s)
    if ns is None: stat['site unmapped'] += 1; continue
    ov = rdv(od, osec, obase, s)
    if ov is None: continue
    v, = struct.unpack('<I', ov); nt = newva(v)
    mapped_new.add(ns)
    if ns not in nrel:
        nv0 = rdv(nd, nsec, nbase, ns); nvv0, = struct.unpack('<I', nv0) if nv0 else (None,)
        tag = 'stale literal (file holds original value)' if nvv0 == v else ('file holds mapped value, no reloc' if nvv0 == nt else 'other')
        stat['norel: ' + tag] += 1; bad.append(('norel', s, ns, v, nt, nvv0)); continue
    nv = rdv(nd, nsec, nbase, ns)
    if nv is None: stat['our site not in file'] += 1; continue
    nvv, = struct.unpack('<I', nv)
    if nt is None: stat['target unmapped'] += 1; continue
    if nvv == nt: stat['ok'] += 1
    else: stat['value differs'] += 1; bad.append(('val', s, ns, v, nt, nvv))
stat['our relocs without original counterpart'] = len(nrel - mapped_new)
print(dict(stat)); print('orig relocs', len(orel), 'our relocs', len(nrel))
json.dump(bad[:60000], open(HERE / 'relcheck_bad.json', 'w'))
for b in bad[:12]: print([hex(x) if isinstance(x, int) else x for x in b])
