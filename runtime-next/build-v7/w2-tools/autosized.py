"""w2: fix sized/unsized operator delete of classes `new`ed by a parent whose EH funclets differ.
W2MODE=sized (default): add `static void operator delete(void*, unsigned int);` to the class whose sizeof equals the size the original pushes.
W2MODE=rev: add `static void operator delete(void*);` to classes that carry the sized one but whose original funclet is 1-argument.
Greedy per parent function; an edit is kept only if no function/EH piece of the unit loses good bytes (vs the original object) and the score rises.
usage: autosized.py unit_idx...   results in w2/auto/<idx>.cpp, <idx>.obj, <idx>.json"""
import sys, re, json, os, shutil
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
import w2lib as L
from pathlib import Path
MODE = os.environ.get('W2MODE', 'sized')
SIZED = 'static void operator delete(void*, unsigned int);'
DECL = SIZED if MODE == 'sized' else 'static void operator delete(void*);'
AUTO = L.W2 / 'auto'; AUTO.mkdir(exist_ok=True)
FUNCLET = re.compile(rb'(?:\x6a.|\x68....)\x8b(?:[\x45\x4d\x55\x5d].|[\x85\x8d\x95\x9d]....)\x50\xe8', re.S)
ONEARG = re.compile(rb'\x8b(?:[\x45\x4d\x55\x5d].|[\x85\x8d\x95\x9d]....)\x50\xe8', re.S)
def read(p):
    b = Path(p).read_bytes().decode('latin1'); nl = '\r\n' if '\r\n' in b else '\n'
    return b, nl
def needed_size(refbytes):
    m = re.match(rb'\x6a(.)', refbytes, re.S)
    if m: return m.group(1)[0]
    m = re.match(rb'\x68(....)', refbytes, re.S)
    if m: return int.from_bytes(m.group(1), 'little')
    return None
def layout_sizes(idx, src_rel):
    ok, out = L.compile_src(idx, src_rel, AUTO / ('lay%d.obj' % idx), ['/d1reportAllClassLayout'])
    sz = {}
    for m in re.finditer(r'^(?:class|struct)\s+([\w:<>,\* ]+?)\tsize\((\d+)\)', out, re.M):
        sz.setdefault(m.group(1).split('::')[-1], set()).add(int(m.group(2)))
    return sz
def func_block(lines, addr):
    pat = re.compile(r'@fnv\s+0x0*%x\b' % addr, re.I)
    i = next((k for k, l in enumerate(lines) if pat.search(l)), None)
    if i is None: return None
    j = i + 1
    while j < len(lines) and not re.search(r'//\s*@fnv\s', lines[j]): j += 1
    return i, j
def class_def(lines, name, before):
    pat = re.compile(r'^\s*(struct|class)\s+' + re.escape(name) + r'\b[^;{]*\{')
    pat2 = re.compile(r'^\s*(struct|class)\s+' + re.escape(name) + r'\b[^;{]*$')
    c = []
    for k, l in enumerate(lines[:before + 1]):
        if pat.match(l) and not l.rstrip().endswith(';'): c.append(k)
        elif pat2.match(l) and k + 1 < len(lines) and lines[k + 1].strip().startswith('{'): c.append(k + 1)
    return c[-1] if c else None
def class_window(lines, cd, n=3000):
    """lines of the class body by brace matching, starting at the line holding the opening brace"""
    out = []; depth = 0; started = False
    for k in range(cd, min(len(lines), cd + n)):
        l = re.sub(r'//.*$', '', lines[k]); out.append(lines[k])
        for ch in l:
            if ch == '{': depth += 1; started = True
            elif ch == '}': depth -= 1
        if started and depth <= 0: break
    return out
def insert_decl(trial, cd):
    first = trial[cd] if re.match(r'\s*(struct|class)', trial[cd]) else trial[cd - 1]
    kind = re.match(r'\s*(struct|class)', first).group(1)
    if kind == 'struct': trial.insert(cd + 1, '    ' + DECL)
    else:
        k = cd + 1
        while k < len(trial) and not trial[k].strip(): k += 1
        if trial[k].strip().startswith('public:'): trial.insert(k + 1, '    ' + DECL)
        else: trial.insert(cd + 1, '    public: ' + DECL + ' private:')
def run(idx):
    u = L.U[idx]; src_rel = u['source']; srcp = L.FN / src_rel
    ev0 = L.evalunit(idx)
    if ev0 is None: print(idx, 'baseline eval failed'); return
    text, nl = read(srcp); lines = text.split(nl)
    bad = [(a, v) for a, v in ev0.items() if v[0] == 'tail' and v[2] < v[1]]
    byp = {}
    for a, v in bad:
        try: ref = L.PE.read(a, v[1])
        except ValueError: continue
        if MODE == 'sized':
            sz = needed_size(ref)
            if sz is None or not FUNCLET.match(ref): continue
        else:
            if not ONEARG.match(ref): continue
            sz = 0
        byp.setdefault(int(v[4], 16) if isinstance(v[4], str) else v[4], set()).add(sz)
    if not byp: print(idx, src_rel, 'no candidate bad pieces (%s)' % MODE); return
    lay = layout_sizes(idx, src_rel) if MODE == 'sized' else {}
    prev_obj = AUTO / ('%04d.obj' % idx)
    cur = (L.evalunit(idx, prev_obj) if prev_obj.exists() else None) or ev0
    ev_start = cur; edited = set(); log = []
    curlines = lines[:]
    for parent in sorted(byp):
        fb = func_block(curlines, parent)
        if not fb: log.append((hex(parent), 'no source block')); continue
        i, j = fb
        news = []
        for l in curlines[i:j]:
            for m in re.finditer(r'\bnew\s+(?:\([^)]*\)\s*)?([A-Za-z_]\w*(?:::\w+)*)', l): news.append(m.group(1).split('::')[-1])
        cands = []
        for n in dict.fromkeys(news):
            if n in edited: continue
            if MODE == 'sized':
                szs = lay.get(n)
                if szs and not (szs & byp[parent]): continue
            cd = class_def(curlines, n, i)
            if cd is None: continue
            win = ' '.join(class_window(curlines, cd))
            if DECL in win:
                if MODE == 'sized' and re.search(r'operator\s+delete\s*\(\s*void\s*\*\s*\w*\s*\)\s*;', win): cands.append((n, cd, 'dedupe'))
                continue
            cands.append((n, cd, 'add'))
        if not cands:
            det = [(n, sorted(lay.get(n, [])), class_def(curlines, n, i) is not None, n in edited) for n in dict.fromkeys(news)][:5]
            log.append((hex(parent), 'no candidate class', sorted(byp[parent]), det)); continue
        trial = curlines[:]
        for n, cd, how in sorted(cands, key=lambda t: -t[1]):
            if how == 'dedupe':
                # sized delete present AND a bodiless 1-argument declaration: drop the 1-argument one (the compiler picks it over the sized one)
                for k in range(cd, cd + len(class_window(trial, cd, 3000))):
                    if re.match(r'\s*(?:public:\s*)?static\s+void\s+(?:__cdecl\s+)?operator\s+delete\s*\(\s*void\s*\*\s*\w*\s*\)\s*;\s*$', trial[k]): trial[k] = ''; break
                continue
            if MODE == 'sized':
                # a class that already declares the 1-argument delete (no body): replace it by the sized one
                k1 = next((k for k in range(cd, min(len(trial), cd + len(class_window(trial, cd, 3000)))) if re.search(r'operator\s+delete\s*\(\s*void\s*\*\s*\w*\s*\)', trial[k])), None)
                if k1 is not None:
                    trial[k1] = re.sub(r'(operator\s+delete\s*\(\s*void\s*\*\s*(\w*))\s*\)', lambda m: m.group(1) + ', unsigned int' + (' ' + m.group(2) + '_sz' if m.group(2) else '') + ')', trial[k1], count=1)
                    cname = n
                    for k2 in range(len(trial)):   # out-of-class definition of the same member
                        if k2 != k1 and re.search(r'\b' + re.escape(cname) + r'::operator\s+delete\s*\(\s*void\s*\*\s*\w*\s*\)', trial[k2]):
                            trial[k2] = re.sub(r'(operator\s+delete\s*\(\s*void\s*\*\s*(\w*))\s*\)', lambda m: m.group(1) + ', unsigned int' + (' ' + m.group(2) + '_sz' if m.group(2) else '') + ')', trial[k2], count=1)
                    continue
            insert_decl(trial, cd)
        tmp = srcp.parent / ('w2tmp_%d.cpp' % idx)
        tmp.write_bytes(nl.join(trial).encode('latin1'))
        objp = AUTO / ('%04d.try.obj' % idx)
        try: ok, out = L.compile_src(idx, tmp.relative_to(L.FN).as_posix(), objp)
        finally: tmp.unlink()
        if not ok: log.append((hex(parent), 'compile failed', out[-200:])); continue
        ev = L.evalunit(idx, objp)
        if ev is None: log.append((hex(parent), 'eval failed')); continue
        rg = L.regress(cur, ev)
        gain = L.score(ev) - L.score(cur)
        if rg or gain <= 0:
            log.append((hex(parent), 'rejected', 'gain', gain, 'regress', {hex(k): v for k, v in list(rg.items())[:3]}, [c[0] for c in cands])); continue
        curlines = trial; cur = ev; edited |= {c[0] for c in cands}; shutil.copy(objp, AUTO / ('%04d.obj' % idx))
        log.append((hex(parent), 'accepted', 'gain', gain, [c[0] for c in cands]))
    total = L.score(cur) - L.score(ev_start)
    print(idx, src_rel, 'gain', total, 'accepted', sum(1 for l in log if l[1] == 'accepted'), 'of', len(byp))
    for l in log: print('   ', l)
    if total > 0:
        (AUTO / ('%04d.cpp' % idx)).write_bytes(nl.join(curlines).encode('latin1'))
        json.dump(dict(unit=idx, source=src_rel, gain=total, log=[list(map(str, l)) for l in log]), open(AUTO / ('%04d.json' % idx), 'w'))
if __name__ == '__main__':
    L.setup()
    for a in [x for x in sys.argv[1:] if not x.startswith('--')]: run(int(a))
