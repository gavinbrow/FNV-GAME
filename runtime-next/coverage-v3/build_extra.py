"""Build extra_pieces.json: (1) EH stubs/funclets from compiled obj\\ not in the recipe tail list, (2) stock CRT/STL functions
from the VC++ 2008 SP1 libcmt/libcpmt matched against uncovered .text.  Read-only on everything but coverage-v3\\.
usage: python -I build_extra.py eh|crt|all"""
import sys, os, re, json, struct, collections
sys.dont_write_bytecode = True
sys.path.append((__import__('os').environ.get('FNV_PY_SITE', __import__('os').path.expandvars(r'%APPDATA%\Python\Python312\site-packages'))))
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
PB = Path((__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\Projects\Decompilation') + r'\runtime-next\pinned-build'))
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(PB))
import assemble_v2 as A
import numpy as np
M32 = 0xffffffff

# ---------------------------------------------------------------- EH
_deltas = []
def _wrap(orig):
    def f(coff, unit, locals_, sec, lo, hi, base_va, buf, stats, pats, scope):
        before = collections.Counter(stats)
        orig(coff, unit, locals_, sec, lo, hi, base_va, buf, stats, pats, scope)
        d = collections.Counter(stats); d.subtract(before)
        _deltas.append({(k[1] + ':' + k[2]) if k[1] != 'e' else 'borrow': v for k, v in d.items() if v})
    return f
def init2(*a):
    A.init(*a)
    A.fill_relocs = _wrap(A.fill_relocs)
def proc2(task):
    _deltas.clear()
    if not task[1].get('eh_tails'):
        task[1]['eh_tails'] = [{'address': '0x0', 'size': 0, 'dummy': True}]
    out = A.process(task)
    ds = list(_deltas)
    k = 0
    for t in out['tails']:
        if t['data'] is None: continue
        t['rel'] = ds[k] if k < len(ds) else None; k += 1
    out['fn'] = []
    return out

def run_eh(units, comp, pe):
    seen = collections.defaultdict(set)
    for u in units:
        for f in u['functions']:
            for n in [f['symbol']] + f.get('fold_aliases', []): seen[n].add(int(f['address'], 16))
    fnnames = {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}
    symnames = A.BAM.recipe_names(units)
    imports, thunks = A.parse_imports(pe)
    tasks = [(i, u) for i, u in enumerate(units) if comp[i]['status'] == 'ok']
    res = {}
    with ProcessPoolExecutor(max(1, os.cpu_count() - 2), initializer=init2, initargs=(fnnames, symnames, imports, thunks)) as ex:
        for r in ex.map(proc2, tasks, chunksize=8): res[r['idx']] = r
    pieces = []
    for i, r in res.items():
        for t in r['tails']:
            if t['data'] is None: continue
            pieces.append(dict(address=t['address'], size=len(t['data']), parent=t['parent'], ok=t['ok'], unit=i, data=t['data'], rel=t.get('rel')))
    return pieces

def piece_stats(rel):
    a = d = b = 0
    for k, v in (rel or {}).items():
        if k == 'borrow': b += v
        elif k.endswith(':agree'): a += v
        elif k.endswith(':disagree'): d += v
    return a, d, b

def eh_extras(pieces, pe, cover_text, TEXT_VA, rs):
    out = []; seen_addr = set(); stat = collections.Counter()
    for p in sorted(pieces, key=lambda p: (p['address'], not p['ok'])):
        a = p['address'] - TEXT_VA; L = p['size']
        stat['located'] += 1
        if not (0 <= a and a + L <= rs): stat['outside-text'] += 1; continue
        if not p['ok']: stat['not-ok(matcher)'] += 1; continue
        if (cover_text[a:a + L] != 0).any(): stat['overlaps-recipe-coverage(already-placed-or-in-tail)'] += 1; continue
        if p['address'] in seen_addr: stat['dup-address'] += 1; continue
        ref = pe.read(p['address'], L)
        if ref != p['data']: stat['final-bytes-differ-from-ref'] += 1; continue
        seen_addr.add(p['address'])
        ag, di, bo = piece_stats(p['rel'])
        out.append(dict(kind='eh', address=p['address'], size=L, source=dict(obj='obj/%04d.obj' % p['unit'], parent=p['parent']),
                        relocs=dict(agree=ag, disagree=di, borrowed=bo), data=p['data'].hex()))
    occ = np.zeros(rs, np.uint8); keep = []
    for e in sorted(out, key=lambda e: e['address']):
        a = e['address'] - TEXT_VA
        if occ[a:a + e['size']].any(): stat['overlap-between-extras'] += 1; continue
        occ[a:a + e['size']] = 1; keep.append(e)
    stat['accepted'] = len(keep)
    return keep, stat

# ---------------------------------------------------------------- CRT
def read_ar(path):
    b = path.read_bytes(); assert b[:8] == b'!<arch>\n'
    pos = 8; raw = []; longn = b''
    while pos + 60 <= len(b):
        name = b[pos:pos + 16].decode('latin1').strip(); size = int(b[pos + 48:pos + 58])
        body = b[pos + 60:pos + 60 + size]
        if name == '//': longn = body
        raw.append((name, body)); pos += 60 + size + (size & 1)
    out = []
    for name, body in raw:
        if name.startswith('/') and name[1:].isdigit():
            o = int(name[1:]); name = longn[o:longn.index(b'\0', o)].decode('latin1')
        out.append((name.rstrip('/'), body))
    return out

def run_crt(units, pe, cover_text, TEXT_VA, rs, text, libdir, tag, extra_cover):
    sys.argv = ['x']
    import uncovered_v2 as U
    cover = cover_text.copy(); cover[extra_cover > 0] = 3
    W = 6
    t = bytes(text)
    index = collections.defaultdict(list)
    for p in np.flatnonzero(cover == 0)[:-W].tolist(): index[t[p:p + W]].append(p)
    cands = []
    for lname in ('libcmt.lib', 'libcpmt.lib'):
        for mname, blob in read_ar(libdir / lname):
            r = U.parse_obj(blob)
            if not r: continue
            secs, syms = r
            names = collections.defaultdict(list)
            for si, (nm, value, sec, ty, sc) in syms.items():
                if sec > 0 and sc == 2: names[sec - 1].append((value, nm))
            for k, s in enumerate(secs):
                if not (s['flags'] & 0x20) or len(s['data']) < 24 or s['name'].startswith('.text$x'): continue
                mask = bytearray(b'\x01' * len(s['data']))
                for ro, si, ty in s['relocs']:
                    for q in range(ro, min(ro + (2 if ty == 0x0a else 4), len(mask))): mask[q] = 0
                nm = sorted(names.get(k, []))
                cands.append(dict(lib=lname, member=mname, secidx=k, sec=s['name'], sym=nm[0][1] if nm else None, names=nm,
                                  data=bytes(s['data']), mask=bytes(mask), relocs=s['relocs'], syms=syms))
    cands.sort(key=lambda f: -len(f['data']))
    claimed = np.zeros(rs, np.uint8); matches = []
    for f in cands:
        data, mask = f['data'], f['mask']; L = len(data)
        k = next((i for i in range(L - W + 1) if all(mask[i:i + W])), None)
        if k is None: continue
        for p in index.get(data[k:k + W], []):
            st = p - k
            if st < 0 or st + L > rs or (cover[st:st + L] != 0).any() or claimed[st:st + L].any(): continue
            seg = t[st:st + L]
            if all(seg[i] == data[i] for i in range(L) if mask[i]):
                claimed[st:st + L] = 1; matches.append((st, f))
    defs = collections.defaultdict(set)
    for st, f in matches:
        for value, nm in f['names']: defs[nm].add(TEXT_VA + st + value)
    defaddr = {n: next(iter(v)) for n, v in defs.items() if len(v) == 1}
    seen = collections.defaultdict(set)
    for u in units:
        for fx in u['functions']:
            for n in [fx['symbol']] + fx.get('fold_aliases', []): seen[n].add(int(fx['address'], 16))
    fnn = {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}
    symnames = A.BAM.recipe_names(units)
    imports, thunks = A.parse_imports(pe)
    A.G['imp'], A.G['thunks'] = imports, thunks
    out = []; stat = collections.Counter(); relsrc = collections.Counter()
    for st, f in sorted(matches, key=lambda m: m[0]):
        va = TEXT_VA + st; L = len(f['data']); buf = bytearray(f['data'])
        ag = di = bo = 0; srcs = collections.Counter()
        for ro, si, ty in f['relocs']:
            nm, value, sec, sty, sc = f['syms'][si]
            if ty not in (0x06, 0x14, 0x07) or ro + 4 > L:
                n = max(0, min(4, L - ro)); buf[ro:ro + n] = pe.read(va + ro, n)
                bo += 1; srcs['borrow-kind-%x' % ty] += 1; continue
            fva = va + ro; orig = pe.read(fva, 4); o32, = struct.unpack('<I', orig)
            if ty == 0x14:
                addend, = struct.unpack_from('<i', buf, ro); observed = (fva + 4 + struct.unpack('<i', orig)[0]) & M32
            else:
                addend, = struct.unpack_from('<I', buf, ro); observed = o32
                if ty == 0x07: observed = (o32 + pe.base) & M32
            exp = None; src = None
            if sec > 0 and sc == 3 and sec - 1 == f['secidx']: exp, src = va + value + addend, 'self'
            elif sec > 0 and sc == 3: pass     # static symbol in another section of the member: unknown placement
            elif nm in defaddr: exp, src = defaddr[nm] + addend, 'lib-matched'
            elif nm in fnn: exp, src = fnn[nm] + addend, 'recipe-fn'
            elif nm in symnames: exp, src = symnames[nm] + addend, 'symbol-map'
            else:
                m = A.ADDR_RE.search(nm)
                if m and not nm.startswith(A.NOADDR_PREFIX): exp, src = int(m.group(1), 16) + addend, 'addr-in-name'
                else:
                    a_ = A.import_target(nm)
                    if a_ is not None: exp, src = a_ + addend, 'import'
            if exp is None:
                bo += 1; buf[ro:ro + 4] = orig; srcs['borrow'] += 1; continue
            exp &= M32
            fld = (exp - (fva + 4)) & M32 if ty == 0x14 else (exp if ty == 0x06 else (exp - pe.base) & M32)
            if exp == observed: buf[ro:ro + 4] = struct.pack('<I', fld); ag += 1; srcs[src + ':agree'] += 1
            else: buf[ro:ro + 4] = orig; di += 1; srcs[src + ':disagree'] += 1
        ref = pe.read(va, L)
        if bytes(buf) != ref: stat['final-bytes-differ'] += 1; continue
        for k, v in srcs.items(): relsrc[k] += v
        out.append(dict(kind='crt', address=va, size=L, source=dict(lib=f['lib'], member=f['member'], symbol=f['sym'], section=f['sec'], toolchain=tag),
                        relocs=dict(agree=ag, disagree=di, borrowed=bo), data=bytes(buf).hex()))
    stat['matched'] = len(matches); stat['accepted'] = len(out)
    return out, stat, relsrc

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    units = json.loads((A.FN / 'build/units.json').read_text())['units']
    comp = {}
    for line in (PB / 'logs' / 'compile.jsonl').read_text().splitlines():
        r = json.loads(line); comp[r['index']] = r
    pe = A.Pe(A.IMG)
    rva, vs, rs, raw = pe.sections[0]; TEXT_VA = pe.base + rva
    cover = np.zeros(rs, np.uint8)
    for u in units:
        for f in u['functions']:
            a = int(f['address'], 16) - TEXT_VA; cover[a:a + f['size']] = 1
        for tl in u.get('eh_tails', []):
            a = int(tl['address'], 16) - TEXT_VA; seg = cover[a:a + tl['size']]; seg[seg == 0] = 2
    text = np.frombuffer(pe.data, np.uint8)[raw:raw + rs]
    res = {}
    ehp = []; crt = []
    if mode in ('eh', 'all'):
        pieces = run_eh(units, comp, pe)
        ehp, st = eh_extras(pieces, pe, cover, TEXT_VA, rs)
        res['eh_stats'] = dict(st); res['eh_bytes'] = sum(e['size'] for e in ehp)
        res['eh_relocs'] = {k: sum(e['relocs'][k] for e in ehp) for k in ('agree', 'disagree', 'borrowed')}
        res['eh_objs_scanned'] = len(os.listdir(PB / 'obj'))
        res['obj_v3_present'] = (PB / 'obj_v3').exists()
        print(res, flush=True)
    ehm = np.zeros(rs, np.uint8)
    for e in ehp: a = e['address'] - TEXT_VA; ehm[a:a + e['size']] = 1
    if mode in ('crt', 'all'):
        libdir = Path((__import__('os').environ.get('FNV_MSVC9_ROOT', r'C:\Projects\Decompilation\FNV\tools\vc2008') + r'\VC\lib'))
        crt, st, rs_ = run_crt(units, pe, cover, TEXT_VA, rs, text, libdir, 'SP1', ehm)
        res['crt_stats'] = dict(st); res['crt_bytes'] = sum(e['size'] for e in crt)
        res['crt_relocs'] = {k: sum(e['relocs'][k] for e in crt) for k in ('agree', 'disagree', 'borrowed')}
        res['crt_reloc_sources'] = dict(rs_)
        res['crt_zero_disagree_funcs'] = sum(1 for e in crt if e['relocs']['disagree'] == 0)
        res['crt_by_lib'] = dict(collections.Counter(e['source']['lib'] for e in crt))
        print(res, flush=True)
    (HERE / 'extra_pieces.json').write_text(json.dumps(dict(summary=res, rtm_available=False, pieces=sorted(ehp + crt, key=lambda e: e['address']))))
    (HERE / 'build_summary.json').write_text(json.dumps(res, indent=1))

if __name__ == '__main__':
    main()
