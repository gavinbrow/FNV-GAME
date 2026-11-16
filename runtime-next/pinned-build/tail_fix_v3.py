"""Add `static void operator delete(void*, unsigned int);` to the classes that EH tails need it for.
usage: tail_fix_v3.py plan   -> logs/sized_plan_v3.json (unit,parent,at,size -> candidate class, definition file/line)
       tail_fix_v3.py apply [unit...] -> edits sources (idempotent: skips classes already carrying the line)"""
import sys, json, re, os
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FN = Path(r'C:\Projects\Decompilation\fnv_decomp')
U = json.load(open(FN / 'build/units.json'))['units']
LAY = json.load(open(HERE / 'logs/layouts_v3.json'))
ROWS = json.load(open(HERE / 'logs/newscan.json'))
DECL = 'static void operator delete(void*, unsigned int);'
cache = {}
def lines(p):
    if p not in cache: cache[p] = p.read_text(errors='replace').split('\n')
    return cache[p]
def find_defs(path, name):
    short = name.split('::')[-1]
    res = []
    t = lines(path)
    for i, l in enumerate(t):
        m = re.match(r'\s*(struct|class)\s+' + re.escape(short) + r'\b([^;{]*)(\{.*)?$', l)
        if m and not l.rstrip().endswith(';'):
            # needs a '{' on this or the next two lines
            j = i
            while j < len(t) and j < i + 4 and '{' not in t[j]: j += 1
            if j < len(t) and '{' in t[j]: res.append((i, j, m.group(1)))
    return res
def plan():
    out = []
    for (u, parent, at, size, sizehex, news, rels) in ROWS:
        lay = LAY[str(u)]; src = FN / U[u]['source']
        cands = []
        for ln, n in news:
            keys = [k for k in lay if k == n or k.endswith('::' + n)]
            if any(size in lay[k] for k in keys): cands.append(n)
        cands = list(dict.fromkeys(cands))
        out.append(dict(unit=u, parent=parent, at=at, size=size, cands=cands, news=[n for _, n in news]))
    json.dump(out, open(HERE / 'logs/sized_plan_v3.json', 'w'), indent=0)
    for o in out: print(o['unit'], o['parent'], hex(o['size']), o['cands'], '' if o['cands'] else 'NEWS=%s' % o['news'][:5])
def apply(only):
    plan_ = json.load(open(HERE / 'logs/sized_plan_v3.json'))
    done = set(); log = []
    for o in plan_:
        if only and o['unit'] not in only: continue
        for n in o['cands']:
            if os.environ.get('TF_ONLY') is not None and n not in os.environ['TF_ONLY'].split(','): continue
            key = (o['unit'], n, o['parent'])
            if key in done: continue
            done.add(key)
            src = FN / U[o['unit']]['source']; t = lines(src)
            fl = [l for l in t[:0]]
            # the function's line in the source
            fidx = next((i for i, l in enumerate(t) if '@fnv ' + o['parent'] in l), None)
            defs = find_defs(src, n)
            where = src
            if not defs:
                for h in (FN / 'include').rglob('*'):
                    if h.is_file() and h.suffix in ('.h', '.hpp'):
                        d2 = find_defs(h, n)
                        if d2: where, defs = h, d2; break
            if not defs: log.append((o['unit'], n, 'NO DEFINITION')); continue
            # closest definition before the function (same file) else first
            if where == src and fidx is not None:
                before = [d for d in defs if d[0] < fidx]
                d = before[-1] if before else defs[0]
            else: d = defs[0]
            tt = lines(where)
            if any(DECL in x for x in tt[d[1]:d[1] + 6]): log.append((o['unit'], n, 'already')); continue
            i, j, kind = d
            line = tt[j]; k = line.index('{')
            ins = (' ' + DECL) if kind == 'struct' else (' public: ' + DECL + ' private:')
            # keep on the same line after the brace
            tt[j] = line[:k + 1] + ins + line[k + 1:]
            log.append((o['unit'], n, str(where.relative_to(FN)), j + 1))
    for p, t in cache.items():
        p.write_text('\n'.join(t))
    for l in log: print(l)
if __name__ == '__main__':
    if sys.argv[1] == 'plan': plan()
    else: apply({int(x) for x in sys.argv[2:]})
