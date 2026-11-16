r"""data-v3 postproc.py: (1) produced_ranges.json: byte ranges of .rdata/.data/.tls that data-v1 produces from OUR objects (piece spans, with unit, kind, public symbol names),
(2) 'our_symbol' aliases for D_ labels that sit at a produced piece's public definition, (3) literal look-alikes list, (4) coverage numbers -> stats.json."""
import collections
import json
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
H = os.path.dirname(os.path.abspath(__file__))
OUT = H + r'\out'
pp = json.load(open(H + r'\produced_pieces.json'))
strict = open(RN + r'\data-v1\FalloutNV_data_strict.exe', 'rb').read()
rng = []
for p in pp:
    n = sec_of(p['va'])
    if n not in DATA_SECS or p['size'] == 0: continue
    rng.append(dict(va=p['va'], size=p['size'], section=n, kind=p['kind'], tier=p['tier'], unit=p['unit'], symbols=[(d[0], p['va'] + d[1]) for d in p['defs']]))
rng.sort(key=lambda r: r['va'])
json.dump(rng, open(OUT + r'\produced_ranges.json', 'w'), separators=(',', ':'))
dl = json.load(open(OUT + r'\data_labels.json'))
alias = {}
for r in rng:
    for nm, va in r['symbols']:
        lab = 'D_%08x' % va
        if lab in dl['data_labels'] and lab not in alias: alias[lab] = nm
for lab, nm in alias.items(): dl['data_labels'][lab]['our_symbol'] = nm
json.dump(dl, open(OUT + r'\data_labels.json', 'w'))
# literal look-alikes (aligned dwords with an image-range value, no base reloc, value-rule says constant)
sj = json.load(open(OUT + r'\symbolic.json'))
fset = {(r[0], r[1]) for r in sj['fields']}
lit = []
for nm in DATA_SECS:
    s = SEC[nm]; blob = ref[s['off']:s['off'] + s['raw']]
    for o in range(0, len(blob) - 3, 4):
        if any((nm, o + d) in fset for d in (-3, -2, -1, 0, 1, 2, 3)): continue
        v = struct.unpack_from('<I', blob, o)[0]
        if IMG_LO <= v < IMG_HI: lit.append([nm, o, v])
json.dump(lit, open(OUT + r'\literal_lookalikes.json', 'w'), separators=(',', ':'))
# coverage
cov = collections.Counter()
for nm in DATA_SECS:
    s = SEC[nm]; ours = 0
    for r in rng:
        if r['section'] == nm: ours += r['size']
    cov[nm + ' raw bytes'] = s['raw']; cov[nm + ' bytes inside placed pieces of our objects (data-v1)'] = ours
asm_bytes = collections.Counter()
for f in os.listdir(OUT):
    if not f.endswith('.asm'): continue
    for l in open(OUT + '\\' + f):
        if l.startswith("db '"): asm_bytes['string literals'] += len(l.rstrip().replace("''", "'")) - 6
        elif 'dup(0)' in l: asm_bytes['zero runs'] += int(re.search(r'db (\d+) dup', l).group(1))
        elif l.startswith('db 0'): asm_bytes['hex bytes'] += l.count(',') + 1
        elif l.startswith('dd offset'): asm_bytes['symbolic pointer fields (4 B each)'] += 4
nours = collections.Counter(r[5] for r in sj['fields']); nev = collections.Counter(r[4] for r in sj['fields']); nk = collections.Counter(r[6] for r in sj['fields'])
st = dict(coverage=dict(cov), asm_bytes=dict(asm_bytes), fields_total=len(sj['fields']), by_evidence=dict(nev), by_origin=dict(nours), by_target_kind=dict(nk),
          literal_lookalikes=len(lit), our_symbol_aliases=len(alias))
json.dump(st, open(OUT + r'\stats.json', 'w'), indent=1)
print(json.dumps(st, indent=1))
