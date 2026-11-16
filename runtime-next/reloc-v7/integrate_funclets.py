r"""integrate_funclets.py: put the converted EH-funclet functions (emit2asm.py output) into the recipe as real source units and retire their contributions.
Steps (all backed up first): write fnv_decomp\src\funclets\eh_funclets_NN.cpp (grouped by compiler+flags, declaration conflicts split); append the units to units.json and
compile them into pinned-build\obj_v3 (+ compile_v3.jsonl lines); move FNV\contributions\FUN_<addr>.cpp to FNV\local\contributions-replaced\ (.asm-20261116); remove the
addresses from local-targets state.accepted and catalog.targets (the queue state). usage: python -I integrate_funclets.py e2a_all [--apply]"""
import collections
import json
import os
import re
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\pinned-build')
sys.path.insert(0, r'C:\Projects\Decompilation\FNV\scripts')
import compile_units_v3 as CU
import local_targets as LT

SRCDIR = Path(sys.argv[1]); APPLY = '--apply' in sys.argv
FN = CU.FN
rep = json.load(open(SRCDIR / 'report.json'))
ok = {a: r for a, r in rep.items() if r['status'] == 'ok'}
IDENT = re.compile(r'(\w+)\s*(?:\(|;|\[)')
groups = collections.defaultdict(list)
for a, r in sorted(ok.items()): groups[(r['compiler'], tuple(r['flags']))].append(a)
bins = []          # (compiler, flags, decls{ident: line}, [addr])
for (comp, fl), addrs in groups.items():
    cur = []
    for a in addrs:
        hdr = ok[a]['hdr']; ids = {}
        for l in hdr:
            m = IDENT.search(l)
            ids[m.group(1) if m else l] = l
        placed = False
        for b in bins:
            if b[0] == comp and b[1] == fl and len(b[3]) < 80 and all(b[2].get(i, l) == l for i, l in ids.items()):
                b[2].update(ids); b[3].append(a); placed = True; break
        if not placed: bins.append([comp, fl, dict(ids), [a]])
print('functions', len(ok), 'units', len(bins), [len(b[3]) for b in bins])
if not APPLY: sys.exit(0)

(FN / 'src' / 'funclets').mkdir(exist_ok=True)
udoc_path = FN / 'build' / 'units.json'
bak = Path(str(udoc_path) + '.bak2-20261116-wB-pre-funclets')
if not bak.exists(): shutil.copy(udoc_path, bak)
udoc = json.loads(udoc_path.read_text())
units = udoc['units']
tc = CU.find_toolchains()
logp = Path(r'C:\Projects\Decompilation\runtime-next\pinned-build\logs\compile_v3.jsonl')
logbak = Path(str(logp) + '.bak-20261116-wB')
if not logbak.exists(): shutil.copy(logp, logbak)
newlog = []
for n, (comp, fl, decls, addrs) in enumerate(bins):
    rel = 'src/funclets/eh_funclets_%02d.cpp' % n
    parts = ['// funclets/eh_funclets_%02d.cpp: %d EH unwind funclet(s) of the original (Gy sections of functions with unwinding), written as naked asm with real instructions' % (n, len(addrs)), '// and symbolic call targets; replaces the _emit contributions loc_%s..loc_%s.' % (addrs[0][2:], addrs[-1][2:]), '']
    parts += sorted(set(decls.values()))
    parts.append('')
    funcs = []
    for a in addrs:
        txt = (SRCDIR / ('%s.cpp' % a[2:])).read_text(encoding='latin1')
        i = txt.index('__declspec')
        parts.append('// @fnv %s' % a); parts.append(txt[i:].rstrip('\n')); parts.append('')
        funcs.append(dict(address=a[:2] + '%08x' % int(a, 16), symbol='?FUN_%s@@YAXXZ' % a[2:], size=ok[a]['size']))
    (FN / rel).write_bytes('\r\n'.join(parts).encode('latin1'))
    idx = len(units)
    u = dict(source=rel, compiler=comp, flags=list(fl), functions=funcs, symbols={})
    units.append(u)
    r = CU.one((idx, u, tc))
    print(rel, idx, r['status'], r['error'][:150])
    if r['status'] != 'ok': raise SystemExit('compile failed; units.json not written')
    newlog.append(json.dumps(dict(index=idx, source=rel, compiler=comp, status='ok', rc=0, error='', seconds=r['seconds'])))
udoc_path.write_text(json.dumps(udoc, indent=1).replace('\n', '\r\n') + '\r\n')
with open(logp, 'a') as f:
    for l in newlog: f.write(l + '\n')
# queue state + retire contributions
st_bak = Path(str(LT.STATE) + '.bak-20261116-wB'); cat_bak = Path(str(LT.CATALOG) + '.bak-20261116-wB')
if not st_bak.exists(): shutil.copy(LT.STATE, st_bak)
if not cat_bak.exists(): shutil.copy(LT.CATALOG, cat_bak)
state = json.loads(LT.STATE.read_text(encoding='utf-8')); cat = json.loads(LT.CATALOG.read_text(encoding='utf-8'))
dst = Path(r'C:\Projects\Decompilation\FNV\local\contributions-replaced')
n_ret = 0
for a in ok:
    state['accepted'].pop(a, None)
    for k in [k for k, t in cat['targets'].items() if t['address'] == a]: cat['targets'].pop(k)
    src = LT.CONTRIB / ('FUN_%s.cpp' % a[2:])
    if src.exists():
        shutil.move(str(src), str(dst / ('FUN_%s.cpp.emit2asm-20261116' % a[2:]))); n_ret += 1
LT.STATE.write_text(json.dumps(state, indent=1), encoding='utf-8'); LT.CATALOG.write_text(json.dumps(cat, indent=1), encoding='utf-8')
print('retired', n_ret, 'contributions; accepted now', len(state['accepted']))
json.dump(dict(ok=sorted(ok), units_added=len(bins)), open(r'C:\Projects\Decompilation\runtime-next\reloc-v7\funclets_integrated.json', 'w'))
