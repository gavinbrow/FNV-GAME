"""Static import closure of the build entry scripts + hard-coded path literals. Read-only."""
import ast, os, re, sys, json, collections
P = r'C:\Projects\Decompilation'
J = os.path.join
roots = [J(P, 'runtime-next', d) for d in ('pinned-build','build-v7','reloc-v7','reloc-v5','coverage-v3','data-v1','data-v2','data-v3','direct-v1','layout-v2','contrib-v5','build-v6','build-v4')]
roots += [P + r'\FNV\scripts', P + r'\fnv_decomp\tools', P + r'\runtime-next']
byname = collections.defaultdict(list)
for r in roots:
    if not os.path.isdir(r): continue
    for f in os.listdir(r):
        if f.endswith('.py'): byname[f[:-3]].append(os.path.join(r, f))
entries = [P+r'\runtime-next\pinned-build\compile_units_v3.py', P+r'\runtime-next\build-v7\verify_v7.py', P+r'\runtime-next\build-v7\assemble_v7.py', P+r'\runtime-next\build-v7\icf_v7.py',
           P+r'\runtime-next\reloc-v7\ownreloc.py', P+r'\runtime-next\data-v3\gen.py', P+r'\runtime-next\data-v3\verify.py', P+r'\runtime-next\data-v3\postproc.py',
           P+r'\runtime-next\layout-v2\snapshot.py', P+r'\runtime-next\layout-v2\make_image.py', P+r'\runtime-next\direct-v1\harness.py', P+r'\runtime-next\direct-v1\make_direct.py', P+r'\runtime-next\data-v1\phase0.py', P+r'\runtime-next\data-v1\place.py', P+r'\runtime-next\data-v1\report.py', P+r'\runtime-next\data-v3\dump_pieces.py', P+r'\runtime-next\data-v3\gen.py']
seen = {}; q = list(entries)
while q:
    f = q.pop()
    if f in seen or not os.path.isfile(f): continue
    src = open(f, encoding='utf-8', errors='replace').read(); seen[f] = src
    try: t = ast.parse(src)
    except SyntaxError: continue
    names = set()
    for n in ast.walk(t):
        if isinstance(n, ast.Import): names |= {a.name.split('.')[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module: names.add(n.module.split('.')[0])
    for nm in names:
        for c in byname.get(nm, []): q.append(c)
    # also dynamic loads of sibling py files by name
    for m in re.finditer(r"['\"]([A-Za-z0-9_\-]+\.py)['\"]", src):
        for c in byname.get(m.group(1)[:-3], []): q.append(c)
BS = chr(92)
pat = re.compile('(?:[A-Za-z]:[' + BS + BS + '/]+|/c/)(?:Projects|Users|Program|Windows)[^' + chr(39) + chr(34) + BS + 'n]*')
out = {}
for f, src in sorted(seen.items()):
    hits = sorted(set(m.group(0)[:110] for m in pat.finditer(src)))
    out[f] = hits
json.dump(out, open('scan_deps.json', 'w'), indent=1)
print(len(seen), 'files in closure;', sum(1 for v in out.values() if v), 'with hard-coded paths')
for f, h in out.items():
    if h: print(os.path.relpath(f, P), len(h), h[:3])
