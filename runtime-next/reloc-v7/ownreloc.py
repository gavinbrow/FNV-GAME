r"""Own base-relocation table for .text, from what build-v7 places (relocs_v7.tsv.gz + inferred_literals_v7.json), compared with the original .reloc.
Writes build-v7\FalloutNV_v7_filled_ownreloc.exe (= the filled exe with .reloc rebuilt: .text sites from our build, every other site from the reference table; the default
filled exe is not touched), reloc-v7\ownreloc_report.json, and merges a 'own_reloc' section into build-v7\progress.json.
usage: python -I ownreloc.py"""
import collections
import gzip
import json
import struct
import sys

sys.dont_write_bytecode = True
B = (__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\Projects\Decompilation') + r'\runtime-next\build-v7')
R = (__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\Projects\Decompilation') + r'\runtime-next\reloc-v7')
d = bytearray(open(B + r'\FalloutNV_v7_filled.exe', 'rb').read())
peo = struct.unpack_from('<I', d, 0x3c)[0]
nsec = struct.unpack_from('<H', d, peo + 6)[0]
so = peo + 24 + struct.unpack_from('<H', d, peo + 20)[0]
secs = {}
for i in range(nsec):
    n, vs, va, rs, ro = struct.unpack_from('<8sIIII', d, so + 40 * i)
    secs[n.rstrip(b'\0').decode()] = (vs, va, rs, ro, so + 40 * i)
base = struct.unpack_from('<I', d, peo + 52)[0]
imgsz = struct.unpack_from('<I', d, peo + 24 + 56)[0]
tvs, tva, trs, tro, _ = secs['.text']
rrva, rsz = struct.unpack_from('<II', d, peo + 24 + 96 + 5 * 8)
rvs, rva_, rrs, rro, rhdr = secs['.reloc']
assert rrva == rva_
# original table
orig = {}; types = collections.Counter(); p = rro
while p < rro + rsz:
    pg, bs = struct.unpack_from('<II', d, p)
    if bs == 0: break
    for k in range((bs - 8) // 2):
        w, = struct.unpack_from('<H', d, p + 8 + 2 * k); types[w >> 12] += 1
        if w >> 12 == 3: orig[pg + (w & 0xfff)] = 1
    p += bs
in_text = lambda r: tva <= r < tva + tvs
orig_text = {r for r in orig if in_text(r)}
# ours
imglo, imghi = base, base + imgsz
ours = {}; why = collections.Counter()
for l in gzip.open(B + r'\relocs_v7.tsv.gz', 'rt'):
    f = l.rstrip('\n').split('\t')
    if f[0] == 'field_va' or f[1] != 'DIR32' or f[3] not in ('agree', 'disagree') or not f[5]: continue
    va = int(f[0], 16); ex = int(f[5], 16)
    if f[3] == 'disagree': why['(included) DIR32 whose target we resolve to a different copy: still a base-relocated field'] += 1
    if f[7] == '-1': why['abs symbol (e.g. fs:[__tls_array] = 0x2c): no base reloc'] += 1; continue
    if not (imglo <= ex < imghi): why['target outside image: no base reloc'] += 1; continue
    if in_text(va - base): ours[va - base] = 'object' if f[4] != 'crt' else 'crt'
inf = json.load(open(B + r'\inferred_literals_v7.json'))
n_inf = 0
for k in inf:
    r = int(k, 16) - base
    if r not in ours and in_text(r): ours[r] = 'inferred-literal'; n_inf += 1
only_ours = sorted(set(ours) - orig_text); only_orig = sorted(orig_text - set(ours))
by_origin = collections.Counter(ours.values())
rep = dict(original_text_sites=len(orig_text), original_total_sites=len(orig), original_types=dict(types), our_text_sites=len(ours), our_by_origin=dict(by_origin),
           ours_not_in_original=len(only_ours), original_not_in_ours=len(only_orig), skipped_by_rule=dict(why))
rep['ours_not_in_original_list'] = ['0x%08x' % (base + r) for r in only_ours[:100]]
rep['original_not_in_ours_list'] = ['0x%08x' % (base + r) for r in only_orig[:100]]
# new table
sites = sorted([r for r in orig if not in_text(r)] + list(ours))
blocks = bytearray(); i = 0
while i < len(sites):
    pg = sites[i] & ~0xfff; ent = []
    while i < len(sites) and (sites[i] & ~0xfff) == pg:
        ent.append(0x3000 | (sites[i] & 0xfff)); i += 1
    if len(ent) & 1: ent.append(0)
    blocks += struct.pack('<II', pg, 8 + 2 * len(ent)) + b''.join(struct.pack('<H', e) for e in ent)
rep['own_table_bytes'] = len(blocks); rep['original_table_bytes'] = rsz; rep['own_sites_total'] = len(sites)
if len(blocks) > rrs:
    rep['error'] = 'table does not fit the section'
else:
    d[rro:rro + rrs] = bytes(blocks) + bytes(rrs - len(blocks))
    struct.pack_into('<I', d, peo + 24 + 96 + 5 * 8 + 4, len(blocks))
    open(B + r'\FalloutNV_v7_filled_ownreloc.exe', 'wb').write(bytes(d))
    # round trip
    chk = set(); p = rro
    while p < rro + len(blocks):
        pg, bs = struct.unpack_from('<II', d, p)
        for k in range((bs - 8) // 2):
            w, = struct.unpack_from('<H', d, p + 8 + 2 * k)
            if w >> 12 == 3: chk.add(pg + (w & 0xfff))
        p += bs
    rep['roundtrip_ok'] = chk == set(sites)
json.dump(rep, open(R + r'\ownreloc_report.json', 'w'), indent=1)
pj = json.load(open(B + r'\progress.json')); pj['own_reloc'] = {k: v for k, v in rep.items() if not k.endswith('_list')}
open(B + r'\progress.json', 'w').write(json.dumps(pj, indent=1))
print(json.dumps({k: v for k, v in rep.items() if not k.endswith('_list')}, indent=1)); print(rep['ours_not_in_original_list'][:10], rep['original_not_in_ours_list'][:10])
