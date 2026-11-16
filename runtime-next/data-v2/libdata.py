r"""data-v2 libdata.py: CRT/STL library members' data sections (libcmt.lib, libcpmt.lib) as placement candidates, tier B only (bytes with relocation fields masked,
exactly one aligned hit in the reference .rdata/.data, at least MINB unmasked non-zero bytes). Writes libdata.json (placed pieces: member, section, va, size, kind) and prints a summary.
Read-only on the reference."""
import collections
import json
import struct
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\data-v1')
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\pinned-build')
sys.argv = [sys.argv[0]]
import place as PL
import uncovered_v2 as U
from pathlib import Path

LIB = Path(r'C:\Projects\Decompilation\FNV\tools\vc2008\VC\lib')
MINB = 12
cands = {}
for ln in ('libcmt.lib', 'libcpmt.lib'):
    for mname, blob in U.read_ar(LIB / ln):
        r = U.parse_obj(blob)
        if not r: continue
        secs, syms = r
        defs = collections.defaultdict(list)
        for si, (nm, value, sec, ty, sc) in syms.items():
            if sec > 0 and not nm.startswith('.'): defs[sec - 1].append((nm, value, sc))
        for k, s in enumerate(secs):
            fl = s['flags']
            if fl & 0x20 or fl & 0x80 or not s['data']: continue
            if not s['name'].startswith(('.rdata', '.data', '.xdata', '.CRT', 'CONST')): continue
            rl = []
            for ro, si, ty in s['relocs']:
                nm, value, sec, sty, sc = syms[si]
                add = struct.unpack_from('<I', s['data'], ro)[0] if ro + 4 <= len(s['data']) else 0
                rl.append((ro, ty, nm, sec, value, sc, add, None, None))
            sd = dict(name=s['name'], flags=fl, data=bytes(s['data']), size=len(s['data']), relocs=rl, defs=defs.get(k, []))
            key = (s['name'], fl & 0xf00000f0, bytes(s['data']), tuple((r[0], r[1], r[2]) for r in rl))
            cands.setdefault(key, []).append((ln, mname, k, sd))
placed = []; byk = collections.Counter(); tot = 0
for key, lst in cands.items():
    sd = lst[0][3]
    if PL.unmasked(sd) < MINB: continue
    pat, kn = PL.fieldvals(sd, {})
    if not any(b for b, m in zip(pat, kn) if m): continue
    hits, cap = PL.search(sd, {})
    if cap or hits is None or len(hits) != 1: continue
    va = hits[0]
    kind = sd['name'].split('$')[0]
    placed.append(dict(lib=lst[0][0], member=lst[0][1], sec=sd['name'], va=va, size=sd['size'], nmem=len(lst)))
    byk[kind] += sd['size']; tot += sd['size']
json.dump(placed, open(r'C:\Projects\Decompilation\runtime-next\data-v2\libdata.json', 'w'))
print('candidate unique sections', len(cands), 'placed', len(placed), 'bytes', tot, dict(byk))
