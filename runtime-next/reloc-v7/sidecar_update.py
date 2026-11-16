"""For edited units whose $SG label list changed (name or content): rebuild the unit's sidecar entry in build-v7/sg_sidecar_w2.json so the labels of the recompiled
object keep the addresses of the same strings. Labels are paired old->new by C-string content (up to the first NUL) and order; the entry is keyed by the NEW object's
label contents (which include alignment padding that depends on the neighbouring label), so build-v7/sgmap_w2.remap works unchanged.
usage: python -I sidecar_update.py idx... | --file list.json"""
import sys, json, collections
sys.dont_write_bytecode = True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
from pathlib import Path
PB = Path(r'C:\Projects\Decompilation\runtime-next\pinned-build'); BV = Path(r'C:\Projects\Decompilation\runtime-next\build-v7')
sys.path.insert(0, str(PB)); sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\coverage-v3'); sys.path.insert(0, str(BV))
import assemble_v3 as A, sgmap_w2 as SG
units = json.loads((A.FN / 'build/units.json').read_text())['units']
pe = A.Pe(A.IMG)
seen = collections.defaultdict(set)
for u in units:
    for f in u['functions']:
        for n in [f['symbol']] + f.get('fold_aliases', []): seen[n].add(int(f['address'], 16))
fnn = {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}
sym = A.BAM.recipe_names(units); imp, th = A.parse_imports(pe); A.init(fnn, sym, imp, th)
SIDEF = BV / 'sg_sidecar_w2.json'
side = json.loads(SIDEF.read_text()); changed = 0
bak = BV / 'sg_sidecar_w2.json.bak-20261116-wB'
if not bak.exists(): bak.write_text(SIDEF.read_text())
orig_side = json.loads(bak.read_text())          # sidecar as it was before my edits (describes obj_v3.bak-20261116)
ids = json.load(open(sys.argv[2])) if sys.argv[1] == '--file' else [int(x) for x in sys.argv[1:]]
def key(c): return c.split(b'\0', 1)[0]
for i in ids:
    old = A.Coff(PB / 'obj_v3.bak-20261116' / ('%04d.obj' % i)); new = A.Coff(PB / 'obj_v3' / ('%04d.obj' % i))
    lo = SG.sg_labels(old); ln = SG.sg_labels(new)
    if [(n, c) for _, n, c in lo] == [(n, c) for _, n, c in ln] and str(i) not in side: continue
    symbols = units[i].get('symbols', {})
    so = orig_side.get(str(i))
    if so: oldmap = SG.remap(old, symbols, so)
    else: oldmap = {k: v for k, v in symbols.items()}
    def addr(name):
        v = oldmap.get(name)
        if v is None: v = A.G['sym'].get(name)
        return None if v is None else (int(v, 0) if isinstance(v, str) else int(v))
    og = collections.defaultdict(list); ng = collections.defaultdict(list)
    for _, n, c in lo: og[key(c)].append(n)
    for _, n, c in ln: ng[key(c)].append((n, c))
    ns = {}; bad = 0
    for k, items in ng.items():
        olds = og.get(k, [])
        if len(olds) < len(items): bad += len(items); continue
        for (n, c), on in zip(items, olds):
            a = addr(on)
            if a is None: bad += 1; continue
            ns.setdefault(c.hex(), []).append(a)
    side[str(i)] = ns; changed += 1
    print('unit', i, 'old labels', len(lo), 'new', len(ln), 'entries', sum(map(len, ns.values())), 'unpaired', bad)
SIDEF.write_text(json.dumps(side))
print('changed', changed)
