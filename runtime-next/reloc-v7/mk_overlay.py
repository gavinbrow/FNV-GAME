"""Build reloc-v7/binding_overlay.json from build-v7/borrowed_v7.tsv.gz (+ reference target values).
The overlay is symbol binding data, applied by assemble_v7 (FNV_OVERLAY=1, default): it plays the role of the original link's decisions
(which of several identical/ICF-folded copies a name resolves to; addresses of CRT globals) that our objects cannot know.
 by_unit_name: {unit source file: {mangled name: address}}   (REL32 / DIR32 target = address + addend)
 global_name : {name: address}                                (CRT globals / functions, consistent across all sites)
 by_field    : {field va: absolute target address}            (the rest)
The 48 wrong-callee sites (origin fn, source a) are NOT in the overlay: those are source bugs to be fixed in the source (see NOTES).
usage: python -I mk_overlay.py [--include-fn-a]"""
import sys, json, gzip, struct, collections
sys.dont_write_bytecode = True
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\pinned-build')
import assemble_v3 as A
R = r'C:\Projects\Decompilation\runtime-next'
units = json.loads((A.FN / 'build/units.json').read_text())['units']
pe = A.Pe(A.IMG)
rows = [l.rstrip('\n').split('\t') for l in gzip.open(R + r'\reloc-v7\borrowed_base.tsv.gz', 'rt')][1:]
fnat = set()
for u in units:
    for f in u['functions']: fnat.add(int(f['address'], 16))
INC = '--include-fn-a' in sys.argv
recs = []; excl = []
for r in rows:
    va = int(r[0], 16); kind = int(r[1]); origin = r[4]; src = r[2]; unit = int(r[7]); add = int(r[8])
    if origin == 'fn' and src == 'a' and not INC: excl.append(va); continue
    raw, = struct.unpack('<I', pe.read(va, 4))
    T = (va + 4 + struct.unpack('<i', pe.read(va, 4))[0]) & 0xffffffff if kind == 0x14 else raw
    recs.append(dict(va=va, kind=kind, origin=origin, name=r[6], unit=unit, add=add, T=T))
by_unit = collections.defaultdict(lambda: collections.defaultdict(set)); glob = collections.defaultdict(set)
for x in recs:
    base = (x['T'] - x['add']) & 0xffffffff
    if x['origin'] == 'crt': glob[x['name']].add(base)
    elif x['origin'] in ('tail', 'fn') and x['kind'] == 0x14 and x['unit'] >= 0:
        by_unit[units[x['unit'] % 100000]['source']][x['name']].add(base)
    # contrib / contrib-eh: per field
ov = dict(by_unit_name={}, global_name={}, by_field={})
bad = collections.Counter()
for x in recs:
    base = (x['T'] - x['add']) & 0xffffffff
    if x['origin'] == 'crt':
        if len(glob[x['name']]) == 1 and not x['name'].startswith('??_C@'): ov['global_name'][x['name']] = base; continue
    elif x['origin'] in ('tail', 'fn') and x['kind'] == 0x14 and x['unit'] >= 0:
        s = units[x['unit'] % 100000]['source']
        if len(by_unit[s][x['name']]) == 1: ov['by_unit_name'].setdefault(s, {})[x['name']] = base; continue
    ov['by_field']['%08x' % x['va']] = x['T']
    bad[(x['origin'], 'field-fallback')] += 1
print('records', len(recs), 'excluded fn-a', len(excl))
print('by_unit_name names', sum(len(v) for v in ov['by_unit_name'].values()), 'units', len(ov['by_unit_name']), '| global names', len(ov['global_name']), '| by_field', len(ov['by_field']), dict(bad))
json.dump(ov, open(R + r'\reloc-v7\binding_overlay.json', 'w'), indent=0, sort_keys=True)
