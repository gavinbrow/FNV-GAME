"""Validate tools/function_names_data.py against build/units.json and the source tree, then write
docs/function-names.json and docs/function-names.md.  Read-only on src/ and build/.

Usage: python tools/gen_function_names.py [--check]
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from function_names_data import N

units = json.load(open(os.path.join(ROOT, 'build', 'units.json')))
by_addr = {}
for u in units['units']:
    for f in u['functions']:
        by_addr[f['address'][2:].lower().zfill(8)] = (f, u['source'])

cache = {}
def text(src):
    if src not in cache:
        cache[src] = open(os.path.join(ROOT, src), encoding='latin1').read()
    return cache[src]

_idx = None
_tok = re.compile(r'[0-9A-Za-z_]+')
def _build():
    global _idx
    _idx = {}   # FUN_ identifier -> list of file paths ; plus per-file token sets
    toks = {}
    for d, _, fs in os.walk(os.path.join(ROOT, 'src')):
        for fn in fs:
            if fn.endswith(('.cpp', '.h', '.inl')):
                p = os.path.join(d, fn)
                try:
                    t = open(p, encoding='latin1').read()
                except OSError:
                    continue
                s = set(_tok.findall(t))
                toks[p] = s
                for w in s:
                    if w.startswith('FUN_'):
                        _idx.setdefault(w, []).append(p)
    _idx['__toks'] = toks

def src_files_with(old):
    if _idx is None:
        _build()
    return [(p, _idx['__toks'][p]) for p in _idx.get(old, [])]

rows, errs, seen = [], [], set()
for addr, new, ev in N:
    old = 'FUN_' + addr
    if addr in seen:
        errs.append('duplicate address ' + addr); continue
    seen.add(addr)
    if addr not in by_addr:
        errs.append('not in units.json: ' + addr); continue
    f, src = by_addr[addr]
    m = re.match(r'\?FUN_%s@(.*)' % addr, f['symbol'])
    scope = ''
    if m:
        scope = m.group(1).split('@@')[0].split('@')
        scope = '::'.join(reversed([s for s in scope if s]))
    files = src_files_with(old)
    newpat = re.compile(r'(?<![0-9A-Za-z_])' + re.escape(new) + r'(?![0-9A-Za-z_])')
    clash = [os.path.relpath(p, ROOT).replace('\\', '/') for p, t in files if new in t]
    rows.append(dict(address='0x' + addr, old=old, new=new, scope=scope, size=f['size'], unit=src,
                     evidence=ev, files=len(files), clash=clash))
    if clash:
        errs.append('name clash %s -> %s in %s' % (old, new, clash[:2]))

for e in errs:
    print('WARN', e)
print(len(rows), 'rows,', len(errs), 'warnings')
if '--check' in sys.argv:
    sys.exit(1 if errs else 0)

rows.sort(key=lambda r: -r['size'])
json.dump(rows, open(os.path.join(ROOT, 'docs', 'function-names.json'), 'w'), indent=1)
with open(os.path.join(ROOT, 'docs', 'function-names.md'), 'w') as o:
    o.write('# Function names for the largest address-named functions\n\n')
    o.write('The build recipe (`build/units.json`), the link maps and the assembler key on the `FUN_<addr>` identifiers, '
            'so the live tree keeps them. This table is the rename map. `tools/apply_function_names.py <src-copy-dir>` '
            'rewrites a copy of `src/` (for the public export) with the new names; it never touches the build tree.\n\n')
    o.write('Sizes are bytes of the original function. Names come from referenced strings, named callees, enclosing class and file; '
            'functions with thin evidence were left alone.\n\n')
    o.write('| Address | Size | Old name | New name | Scope | Evidence |\n|---|---|---|---|---|---|\n')
    for r in rows:
        o.write('| %s | %d | `%s` | `%s` | %s | %s |\n' % (r['address'], r['size'], r['old'], r['new'],
                ('`%s`' % r['scope']) if r['scope'] else 'free function', r['evidence'].replace('|', '/')))
print('wrote docs/function-names.json and .md')
