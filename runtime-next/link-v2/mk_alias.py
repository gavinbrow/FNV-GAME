"""link-v2 mk_alias.py: /ALTERNATENAME lines binding C_<va> names to libcmt/libcpmt symbols (and unit-defined C_ names are already real definitions).
A lib symbol name that the build resolved (symaddr.json) to address <va> gives C_<va> = that symbol. Only C_ names that the last link left unresolved are written."""
import json, collections, sys
from pathlib import Path
sys.dont_write_bytecode = True
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'pinned-build'))
import uncovered_v2 as U
libnames = set()
for ln in ('libcmt.lib', 'libcpmt.lib'):
    for mname, blob in U.read_ar(Path(r'C:\Projects\Decompilation\FNV\tools\vc2008\VC\lib') / ln):
        r = U.parse_obj(blob)
        if r:
            for si, (nm, value, sec, ty, sc) in r[1].items():
                if sc == 2 and sec > 0: libnames.add(nm)
sa = json.load(open(H / 'symaddr.json')); byva = collections.defaultdict(set)
for idx, d in sa.items():
    for nm, a in d.items():
        if nm in libnames and len(a) == 1: byva[a[0]].add(nm)
for nm, a in json.load(open(H / 'crt_defaddr.json')).items():
    if nm in libnames: byva[a].add(nm)
un = [n for n in json.load(open(H / 'link_errors.json'))['unresolved'] if n.startswith('C_')]
lines = []; amb = 0; miss = 0
for n in un:
    va = int(n[2:], 16); c = byva.get(va)
    if c and len(c) == 1: lines.append('/ALTERNATENAME:%s=%s' % (n, next(iter(c))))
    elif c: amb += 1
    else: miss += 1
open(H / 'opts_extra.txt', 'w').write('\n'.join(lines) + '\n')
print('C_ unresolved', len(un), 'aliased to lib symbols', len(lines), 'ambiguous', amb, 'no lib name', miss)
