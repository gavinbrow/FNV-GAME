"""Break down borrowed relocation fields (build-v7/borrowed_v7.tsv.gz) by cause, owner unit/source, target name; resolve the original target from the reference.
usage: python -I breakdown.py  -> reloc-v7/breakdown.json (+ prints summary)"""
import sys, json, gzip, struct, collections
sys.dont_write_bytecode = True
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\pinned-build')
import assemble_v3 as A
R = r'C:\Projects\Decompilation\runtime-next'
units = json.loads((A.FN / 'build/units.json').read_text())['units']
pe = A.Pe(A.IMG)
rows = [l.rstrip('\n').split('\t') for l in gzip.open(R + r'\build-v7\borrowed_v7.tsv.gz', 'rt')][1:]
# recipe function names by address
fnat = collections.defaultdict(set)
for i, u in enumerate(units):
    for f in u['functions']:
        fnat[int(f['address'], 16)].add(f['symbol'])
out = []
for r in rows:
    va = int(r[0], 16); kind = r[1]; unit = int(r[7])
    raw, = struct.unpack('<I', pe.read(va, 4))
    if kind == '20': tgt = (va + 4 + struct.unpack('<i', pe.read(va, 4))[0]) & 0xffffffff
    else: tgt = raw
    out.append(dict(va=va, kind=kind, source=r[2], status=r[3], origin=r[4], cause=r[5], name=r[6], unit=unit,
                    src=(units[unit]['source'] if unit >= 0 else {-3: 'contrib-eh', -2: 'contrib'}.get(unit, '?')), target=tgt,
                    target_fn=sorted(fnat.get(tgt, []))[:3]))
json.dump(out, open(R + r'\reloc-v7\breakdown_fields.json', 'w'))
print(len(out), 'fields,', 4 * len(out), 'bytes')
def top(key, n=15):
    c = collections.Counter(); 
    for o in out: c[key(o)] += 1
    for k, v in c.most_common(n): print('  %6d fields %7d B  %s' % (v, 4 * v, k))
print('by cause'); top(lambda o: o['cause'], 30)
print('by origin/status'); top(lambda o: (o['origin'], o['status'], o['source']))
print('by source file (top)'); top(lambda o: o['src'], 40)
