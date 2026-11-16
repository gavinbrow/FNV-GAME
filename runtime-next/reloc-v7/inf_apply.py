r"""inf_apply.py: the 81 inferred literal-address sites -> real extern symbols. For each site (build-v7\inferred_literals_v7.json) the literal is replaced inside the owning function's source
(between its `// @fnv 0x<addr>` marker and the next marker): data address -> ((int)&DAT_<va>), code address -> ((int)FUN_<va>); the declaration (`extern char DAT_<va>;` / `void FUN_<va>();`)
is added before the function marker unless the file already declares the name. Backups: <file>.bak-20261116-wB. usage: python -I inf_apply.py [--apply]"""
import collections
import json
import re
import shutil
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\data-v3')
from common import *

APPLY = '--apply' in sys.argv
S = 'C:/Projects/Decompilation/fnv_decomp/'
inf = json.load(open(r'C:\Projects\Decompilation\runtime-next\build-v7\inferred_literals_v7.json'))
units = load_units()
import bisect
fr = sorted((int(f['address'], 16), i) for i, u in enumerate(units) for f in u['functions'])
ks = [x[0] for x in fr]
by_file = collections.defaultdict(list)
for k, v in sorted(inf.items()):
    va = int(k, 16); val = int(v, 16)
    j = bisect.bisect_right(ks, va) - 1
    fa, ui = fr[j]
    by_file[units[ui]['source']].append((fa, va, val))
tot = collections.Counter(); touched = []
for src, sites in by_file.items():
    raw = open(S + src, 'rb').read().decode('latin1'); nl = '\r\n' if '\r\n' in raw else '\n'
    L = raw.split(nl); decls = {}; ins = []     # (marker line index, decl)
    for fa, va, val in sites:
        mk = [i for i, l in enumerate(L) if l.strip() == '// @fnv 0x%08x' % fa or l.strip().startswith('// @fnv 0x%08x' % fa)]
        if not mk: tot['no-marker'] += 1; print('NO MARKER', src, hex(fa)); continue
        a = mk[0]; b = next((i for i in range(a + 1, len(L)) if L[i].startswith('// @fnv')), len(L))
        isfn = TLO <= val < THI
        name = ('SUB_%08x' if isfn else 'PTR_%08x') % val
        pats = ['0x%x' % val, '0x%08x' % val, '0x%X' % val, '0x%08X' % val]
        n = 0
        for i in range(a, b):
            if L[i].strip().startswith('//'): continue
            for p in pats:
                m = re.search(r'(?<![0-9A-Za-z_])' + re.escape(p) + r'(?![0-9A-Za-z_])', L[i])
                if m:
                    rep = '((int)%s%s)' % ('' if isfn else '&', name)
                    L[i] = L[i][:m.start()] + rep + L[i][m.end():]; n += 1; break
        if not n and any(name in L[i] for i in range(a, b)): n = 1       # already replaced by an earlier run
        if not n: tot['no-literal'] += 1; print('NO LITERAL', src, hex(fa), hex(val)); continue
        tot['sites-edited'] += 1
        decl = ('void %s();' if isfn else 'extern char %s;') % name
        if not any(l.strip() == decl for l in L[:a]):
            decls[name] = (min(a, decls[name][0]) if name in decls else a, decl)
    for name, (a, decl) in decls.items(): ins.append((a, decl))
    for a, decl in sorted(ins, reverse=True):
        j = a
        while j > 0 and L[j - 1].startswith('//'): j -= 1
        L.insert(j, decl)
    if APPLY and tot['sites-edited']:
        if not __import__('os').path.exists(S + src + '.bak-20261116-wB'): shutil.copy(S + src, S + src + '.bak-20261116-wB')
        open(S + src, 'wb').write(nl.join(L).encode('latin1')); touched.append(src)
print(dict(tot), 'files', len(by_file))
json.dump(touched, open(r'C:\Projects\Decompilation\runtime-next\reloc-v7\inf_touched.json', 'w'))
