"""Block model of .text for the free-layout tool (self-contained; inputs read-only)."""
import sys, struct, gzip, json, bisect, collections
sys.dont_write_bytecode = True
import numpy as np
RN = (__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\Projects\Decompilation') + r'\runtime-next')
import os
SNAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'snapshot')   # frozen inputs (snapshot.py)
B7 = SNAP
UNITS = os.path.join(SNAP, 'units.json')
TV = 0x401000          # .text VA
TS = 0xbdd600          # .text raw size (includes trailing pad)

def load_atoms():
    iv = []
    for i, u in enumerate(json.load(open(UNITS))['units']):
        for f in u['functions']:
            a = int(f['address'], 16) - TV; iv.append((a, a + f['size'], 'fn', i))
        for t in u.get('eh_tails', []):
            a = int(t['address'], 16) - TV; iv.append((a, a + t['size'], 'eh', i))
    cp = json.load(open(B7 + r'\contrib_pieces.json'))
    for p in cp['pieces']:
        a = p['address'] - TV; iv.append((a, a + p['size'], 'contrib', -2))
    for p in cp.get('eh', []):
        if isinstance(p, dict) and 'address' in p:
            a = int(p['address']) - TV; iv.append((a, a + int(p['size']), 'contrib', -2))
    iv = [x for x in iv if 0 <= x[0] < x[1] <= TS]; iv.sort()
    merged = []
    for s, e, k, u in iv:
        if merged and s < merged[-1][1]:
            m = merged[-1]; merged[-1] = (m[0], max(m[1], e), m[2], m[3])
        else: merged.append((s, e, k, u))
    return merged

def load_records():
    rows = []
    for l in gzip.open(B7 + r'\relocs_v7.tsv.gz', 'rt'):
        f = l.rstrip('\n').split('\t')
        if f[0] == 'field_va': continue
        rows.append((int(f[0], 16) - TV, f[1], f[3], f[4], int(f[5], 16) if f[5] else -1, f[7]))
    return rows
if __name__ == '__main__':
    at = load_atoms(); print('atoms', len(at), collections.Counter(a[2] for a in at), sum(e - s for s, e, k, u in at))
    d = open(RN + r'\direct-v1\FalloutNV_direct.exe', 'rb').read()
    text = np.frombuffer(d, np.uint8)[0x400:0x400 + TS]
    PAD = (0xcc, 0x00, 0x90)
    gaps = []; pos = 0
    for s, e, k, u in at + [(TS, TS, 'end', -1)]:
        if s > pos:
            p = pos
            while p < s and text[p] in PAD: p += 1
            if p < s: gaps.append((p, s))
        pos = max(pos, e)
    print('gaps (non-pad)', len(gaps), sum(b - a for a, b in gaps)); gs = sorted(gaps, key=lambda g: g[0] - g[1])[:8]; print([(hex(a + TV), b - a) for a, b in gs])
    rec = load_records(); print('records', len(rec))
    starts = [a[0] for a in at]
    out = 0; ob = collections.Counter()
    for r in rec:
        j = bisect.bisect_right(starts, r[0]) - 1
        if not (j >= 0 and r[0] < at[j][1]): out += 1; ob[r[3]] += 1
    print('records outside atoms', out, ob)
