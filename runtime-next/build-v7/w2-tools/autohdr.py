"""w2: sized-delete fix for classes defined in a header (not in the unit's .cpp). Sequential only (edits the header in place, reverts unless accepted).
Dependents of the header (every unit whose include closure contains it) are compiled and must not lose any good bytes.
usage: autohdr.py unit_idx..."""
import sys, re, json, os, shutil
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
import w2lib as L, autosized as AS
from pathlib import Path
FN = L.FN
INC = re.compile(r'^\s*#\s*include\s+"([^"]+)"', re.M)
_cache = {}
def includes(path):
    path = Path(path)
    if path in _cache: return _cache[path]
    out = []
    try: t = path.read_text(errors='replace')
    except OSError: _cache[path] = out; return out
    for m in INC.finditer(t):
        for base in (path.parent, FN / 'include'):
            q = (base / m.group(1)).resolve()
            if q.exists(): out.append(q); break
    _cache[path] = out; return out
def closure(path, depth=6, seen=None):
    seen = set() if seen is None else seen
    for q in includes(path):
        if q not in seen:
            seen.add(q)
            if depth: closure(q, depth - 1, seen)
    return seen
DEP = None
def dependents(hdr):
    global DEP
    if DEP is None:
        DEP = {}
        for i, u in enumerate(L.U):
            for q in closure(FN / u['source']): DEP.setdefault(q, []).append(i)
    return DEP.get(Path(hdr).resolve(), [])
def run(idx):
    u = L.U[idx]; srcp = FN / u['source']
    ev0 = L.evalunit(idx)
    text, nl = AS.read(srcp); lines = text.split(nl)
    bad = [(a, v) for a, v in ev0.items() if v[0] == 'tail' and v[2] < v[1]]
    byp = {}
    for a, v in bad:
        ref = L.PE.read(a, v[1]); sz = AS.needed_size(ref)
        if sz is None or not AS.FUNCLET.match(ref): continue
        byp.setdefault(int(v[4], 16) if isinstance(v[4], str) else v[4], set()).add(sz)
    lay = AS.layout_sizes(idx, u['source']); done = []
    hdrs = sorted(closure(srcp))
    for parent in sorted(byp):
        fb = AS.func_block(lines, parent)
        if not fb: continue
        news = []
        for l in lines[fb[0]:fb[1]]:
            for m in re.finditer(r'\bnew\s+(?:\([^)]*\)\s*)?([A-Za-z_]\w*(?:::\w+)*)', l): news.append(m.group(1).split('::')[-1])
        for n in dict.fromkeys(news):
            szs = lay.get(n)
            if szs and not (szs & byp[parent]): continue
            if AS.class_def(lines, n, len(lines) - 1) is not None: continue
            for h in hdrs:
                ht, hnl = AS.read(h); hl = ht.split(hnl)
                cd = AS.class_def(hl, n, len(hl) - 1)
                if cd is None: continue
                win = ' '.join(AS.class_window(hl, cd))
                if AS.DECL in win: break
                bak = Path(str(h) + '.bak-20261115-w2')
                if not bak.exists(): shutil.copy(h, bak)
                trial = hl[:]
                k1 = next((k for k in range(cd, cd + len(AS.class_window(trial, cd))) if re.search(r'operator\s+delete\s*\(\s*void\s*\*\s*\w*\s*\)', trial[k])), None)
                if k1 is not None:
                    trial[k1] = re.sub(r'(operator\s+delete\s*\(\s*void\s*\*\s*(\w*))\s*\)', lambda m: m.group(1) + ', unsigned int' + (' ' + m.group(2) + '_sz' if m.group(2) else '') + ')', trial[k1], count=1)
                else: AS.insert_decl(trial, cd)
                orig = h.read_bytes()
                h.write_bytes(hnl.join(trial).encode('latin1'))
                try:
                    objp = AS.AUTO / ('%04d.try.obj' % idx)
                    ok, out = L.compile_src(idx, u['source'], objp)
                    res = None
                    if ok:
                        ev = L.evalunit(idx, objp); rg = L.regress(ev0, ev); gain = L.score(ev) - L.score(ev0)
                        if not rg and gain > 0:
                            # dependents
                            bad_dep = []
                            for d in dependents(h):
                                if d == idx: continue
                                b = L.evalunit(d); op = AS.AUTO / ('dep%04d.obj' % d)
                                okd, _ = L.compile_src(d, L.U[d]['source'], op)
                                if not okd: bad_dep.append((d, 'compile')); continue
                                e2 = L.evalunit(d, op)
                                if L.regress(b, e2): bad_dep.append((d, 'regress'))
                            res = (gain, bad_dep)
                finally:
                    keep = res is not None and not res[1]
                    if not keep: h.write_bytes(orig)
                print(idx, n, h.name, 'gain', res, 'KEEP' if keep else 'revert', flush=True)
                if keep:
                    shutil.copy(objp, AS.AUTO / ('%04d.obj' % idx)); ev0 = L.evalunit(idx, objp)
                    json.dump(dict(unit=idx, header=str(h), gain=res[0]), open(AS.AUTO / ('%04d.hdr.json' % idx), 'w'))
                    open(L.W2 / 'changed_files.txt', 'a').write(str(h) + ' (header, backup .bak-20261115-w2; unit %d)\n' % idx)
                break
if __name__ == '__main__':
    L.setup()
    for a in sys.argv[1:]: run(int(a))
