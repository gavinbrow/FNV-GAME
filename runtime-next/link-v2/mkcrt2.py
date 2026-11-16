"""link-v2 mkcrt2.py: libcmt/libcpmt code sections crt5 did not place are matched by content (relocation-masked) against the reference .text; where a match covers a
C_<va> name the link still reports unresolved, the member is linked as an object with that alias (identical code copies at several addresses all get an alias).
Reads link1.log (unresolved C_ names), writes crt_obj x*.obj. usage: python -I mkcrt2.py"""
import collections, json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / 'pinned-build'))
sys.path.insert(0, str(HERE.parent / 'coverage-v3')); sys.path.insert(0, str(HERE.parent / 'data-v3'))
import coffrw, uncovered_v2 as U
import build_extra as BE
from common import SEC, TLO, ref
T = ref[SEC['.text']['off']:SEC['.text']['off'] + SEC['.text']['raw']]
LIB = Path('C:/Projects/Decompilation/FNV/tools/vc2008/VC/lib')
need = set(int(m, 16) for m in re.findall(r'unresolved external symbol C_([0-9a-f]{8})', (HERE / 'link1.log').read_text(errors='replace')))
have = set()
for p in (HERE / 'crt_obj').glob('*.obj'):
    for i, nm, value, sec, ty, sc, naux, o in coffrw.symbols(p.read_bytes()):
        if sec > 0 and sc == 2 and nm.startswith('C_'): have.add(int(nm[2:], 16))
need -= have
for p in out.glob('x*.obj') if (out := HERE / 'crt_obj') else []: p.unlink()
def hits_of(data, relocs):
    mask = bytearray(b'\1' * len(data))
    for o, si, ty in relocs:
        for q in range(o, min(o + (2 if ty == 0x0a else 4), len(data))): mask[q] = 0
    runs = []; i = 0
    while i < len(data):
        if mask[i]:
            j = i
            while j < len(data) and mask[j]: j += 1
            runs.append((i, j)); i = j
        else: i += 1
    if not runs: return []
    a, b = max(runs, key=lambda r: r[1] - r[0])
    if b - a < 6: return []
    key = data[a:b][:12]; hits = []; p = T.find(key)
    while p >= 0 and len(hits) < 8:
        st = p - a
        if st >= 0 and st + len(data) <= len(T) and all(T[st + i] == data[i] for i in range(len(data)) if mask[i]): hits.append(TLO + st)
        p = T.find(key, p + 1)
    return hits
out = HERE / 'crt_obj'; stat = collections.Counter(); n = 0; got = set()
for ln in ('libcmt.lib', 'libcpmt.lib'):
    for mname, blob in BE.read_ar(LIB / ln):
        if blob[:2] != bytes([0x4c, 1]): continue
        parsed = U.parse_obj(blob)
        if not parsed: continue
        S = coffrw.sections(blob); syms = list(coffrw.symbols(blob)); adds = []; seen = set()
        for k, sd in enumerate(parsed[0]):
            if not (sd['flags'] & 0x20) or not sd['data'] or len(sd['data']) < 6: continue
            hs = hits_of(sd['data'], sd['relocs'])
            if not hs: continue
            offs = {0} | {value for i, nm, value, sec, ty, sc, naux, o in syms if sec == k + 1 and sc in (2, 3) and not nm.startswith('.')}
            for h in hs:
                for off in sorted(offs):
                    if h + off in need and h + off not in got:
                        nm_ = 'C_%08x' % (h + off); got.add(h + off); adds.append((nm_, k + 1, off, 0x20))
        if adds:
            base = Path(mname.replace(chr(92), '/')).name[:40]
            ex = [p for p in out.glob('*_' + base + '.obj') if not p.name.startswith('x')]
            if ex: ex[0].write_bytes(coffrw.add_symbols(ex[0].read_bytes(), adds)); stat['aliases added to placed member'] += len(adds)
            else: n += 1; (out / ('x%03d_%s.obj' % (n, base))).write_bytes(coffrw.add_symbols(blob, adds)); stat['new members'] += 1; stat['aliases'] += len(adds)
print(dict(stat), 'needed', len(need), 'still missing', sorted(hex(a) for a in need - got)[:20])
