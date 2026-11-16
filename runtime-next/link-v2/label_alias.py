"""link-v2 label_alias.py: undefined C_<va> names that point INSIDE a function/piece another linked object defines (mid-function jump targets like SUB_<va>) get an alias symbol
C_<va> at that offset in the defining object (section offset = va - owner base). usage: python -I label_alias.py (after prep3 / prep_contribs)"""
import collections, json, struct, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
import coffrw
files = sorted(p for d in ('obj_rw', 'obj_contrib_rw', 'crt_obj') for p in (HERE / d).glob('*.obj'))
_u = json.load(open(HERE.parent.parent / 'fnv_decomp' / 'build' / 'units.json'))['units']
fsize = {}
for x in _u:
    for f in x['functions']: fsize[int(f['address'], 16)] = max(fsize.get(int(f['address'], 16), 0), f['size'])
for _k, _v in json.load(open(HERE / 'eh_pieces.json')).items():
    for _sec, _pl in _v.items():
        for s0, s1, at in _pl: fsize[at] = max(fsize.get(at, 0), s1 - s0)
defined = {}; undef = set(); per = {}
for p in files:
    b = p.read_bytes(); S = list(coffrw.symbols(b)); secs = coffrw.sections(b)
    for i, nm, value, sec, ty, sc, naux, o in S:
        if not nm.startswith('C_'): continue
        if sec > 0 and sc == 2: defined[int(nm[2:], 16)] = (p, sec, value, secs[sec - 1]['size'])
        elif sec == 0: undef.add(int(nm[2:], 16))
miss = sorted(undef - set(defined))
ds = sorted(defined)
import bisect
adds = collections.defaultdict(list); n = 0; left = []
for va in miss:
    i = bisect.bisect(ds, va) - 1
    if i >= 0:
        base = ds[i]; p, sec, value, size = defined[base]
        # same section: aliases must stay within the section
        if va - base < fsize.get(base, 0) and value + (va - base) < size: adds[p].append(('C_%08x' % va, sec, value + (va - base), 0x20)); n += 1; continue
    left.append(va)
for p, a in adds.items(): p.write_bytes(coffrw.add_symbols(p.read_bytes(), a))
print('mid-function labels aliased', n, 'objects', len(adds), 'still undefined C_ targets', len(left), [hex(x) for x in left[:20]])
