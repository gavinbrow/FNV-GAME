"""assemble_v7 = reloc-v5 relocation resolution (assemble_v5, default mode: FNV_V5_FIXUPS off) + verified local-target contributions
(contrib_pieces.json from verify_v7.py) + exception-handler pieces (funclets/tails) of those contributions.
Pass 1 (pool): re-run assemble_v3.process over obj_v3 for every compiled unit, logging every relocation field.
Pass 2: place recipe functions, verified contributions, recipe EH pieces, contribution EH pieces (exact-bytes acceptance, never over placed bytes), CRT pieces.
Writes under build-v7 only: strict/filled images, progress.json, gz TSVs, rebase_remaining_v7.json."""
import sys, os, json, struct, collections, time, gzip, bisect, hashlib
sys.dont_write_bytecode = True
sys.path.append((__import__('os').environ.get('FNV_PY_SITE', __import__('os').path.expandvars(r'%APPDATA%\Python\Python312\site-packages'))))
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
HERE = Path(__file__).resolve().parent
PB = Path((__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\path\to\Decompilation') + r'\runtime-next\pinned-build'))
CV = Path((__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\path\to\Decompilation') + r'\runtime-next\coverage-v3'))
sys.path.insert(0, str(PB)); sys.path.insert(0, str(CV)); sys.path.insert(0, str(HERE))
import numpy as np
import assemble_v3 as A
M32 = 0xffffffff
NEWBASE = 0x10000000

# ------------------------------------------------------------ worker
_log = []
_sa = {}
_sf = {}
SA_ON = os.environ.get('FNV_DUMP_SYMADDR') == '1'   # link-v2: per-object symbol -> resolved address
_tsec = {}
FIX = {}
EHBIND = {}
ICF = {}
SGSIDE = {}
# w2: EH-only variants. ehvariants_w2.json lists units whose unwind funclets the original has in a form our base source cannot produce together with a matching
# parent (e.g. a sized operator delete shifts a register-operand order inside the 12 KB parent). The variant source is compiled to an object; ONLY its EH pieces
# (funclets / handler stubs) are used, each accepted under the usual exact-bytes rule, and the parent function always comes from the base object.
# Variant task index = 100000 + unit. Gate: FNV_EH_VARIANTS=0 disables.
EHVAR = {}
OVL = dict(by_unit_name={}, global_name={}, by_field={})   # w-B: reloc-v7/binding_overlay.json (see reloc-v7/NOTES.md); FNV_OVERLAY=0 disables
if os.environ.get('FNV_EH_VARIANTS', '1') == '1' and (HERE / 'ehvariants_w2.json').exists():
    for _e in json.loads((HERE / 'ehvariants_w2.json').read_text()): EHVAR[100000 + _e['unit']] = _e['obj']
import re as _re
# w2: class-specific sized operator delete members (??3<Class>@@SAXPAXI@Z) that the recipe does not name: the recipe binds this decorated name for NiMemObject
# (and ~20 other classes) to 0x00aa1460, the shared pooled-free function, and every sized-delete unwind call seen in the image goes there. Applied only to
# otherwise unresolved REL32 targets; each site is still checked against the reference value (status agree/disagree), so a wrong target never counts as ours.
SIZED_DEL = os.environ.get('FNV_SIZED_DELETE_BIND', '1') == '1'
SIZED_DEL_RE = _re.compile(r'^\?\?3.+@@SAXPAXI@Z$')
_ovp = HERE.parent / 'reloc-v7' / 'binding_overlay.json'
if os.environ.get('FNV_OVERLAY', '1') == '1' and _ovp.exists():
    _o = json.loads(_ovp.read_text()); OVL['by_unit_name'].update(_o['by_unit_name']); OVL['global_name'].update(_o['global_name'])
    OVL['by_field'].update({int(k, 16): v for k, v in _o['by_field'].items()})
_icp = HERE.parent / 'reloc-v7' / 'int_constants.json'
INTCONST = set(json.loads(_icp.read_text())['values']) if _icp.exists() else set()
def ov_observed(kind, field_va, orig_raw):
    if kind == 0x14: return (field_va + 4 + struct.unpack('<i', orig_raw)[0]) & M32
    if kind == 6: return struct.unpack('<I', orig_raw)[0]
    return None
def init4(*a):
    A.init(*a)
    import sgmap_w2 as _SG
    if EHVAR:
        _Cv0 = A.Coff
        def _Cvar(path, *x, **k):
            p = Path(path)
            if p.stem.isdigit() and int(p.stem) in EHVAR: p = HERE / EHVAR[int(p.stem)]
            return _Cv0(p, *x, **k)
        A.Coff = _Cvar
    if (HERE / 'sg_sidecar_w2.json').exists(): SGSIDE.update(json.loads((HERE / 'sg_sidecar_w2.json').read_text()))
    if (HERE / 'icf_map.json').exists() and os.environ.get('FNV_ICF', '1') == '1': ICF.update(json.loads((HERE / 'icf_map.json').read_text()))
    import os as _os
    if _os.environ.get('FNV_V5_FIXUPS') == '1':
        FIX.update({int(k): v for k, v in json.loads((HERE / 'callee_fixups.json').read_text())['fixups'].items()})
    orig_rf, orig_fr = A.resolve_field, A.fill_relocs
    def rf(coff, unit, locals_, kind, tsym, addend, field_va, orig_raw):
        src, exp = orig_rf(coff, unit, locals_, kind, tsym, addend, field_va, orig_raw)
        if tsym['name'] in EHBIND: src, exp = 'eh-stub', (EHBIND[tsym['name']] + addend) & M32
        if src is None and tsym['name'] in ICF and (tsym['section'] <= 0 or tsym['type'] & 0x20): src, exp = 'icf-fold', (ICF[tsym['name']] + addend) & M32
        if src is None and SIZED_DEL and kind == 0x14 and tsym['section'] <= 0 and SIZED_DEL_RE.match(tsym['name']): src, exp = 'sized-delete-rule', (0x00aa1460 + addend) & M32
        if src is None and tsym['name'] == '___ImageBase': src, exp = 'linker-imagebase', (A.G['pe'].base + addend) & M32
        if FIX and src == 'a' and field_va in FIX: src, exp = 'a-fixup', FIX[field_va]
        if OVL['by_field'] or OVL['by_unit_name']:
            ob = ov_observed(kind, field_va, orig_raw)
            if ob is not None and (src is None or exp != ob):   # only where we would otherwise borrow or disagree
                ovx = OVL['by_field'].get(field_va)
                if ovx is not None: src, exp = 'overlay-field', ovx & M32
                else:
                    ovb = OVL['by_unit_name'].get(unit.get('source'), {}).get(tsym['name'][:80])
                    if ovb is None and tsym['section'] <= 0: ovb = OVL['global_name'].get(tsym['name'][:80])
                    if ovb is not None: src, exp = 'overlay-name', (ovb + addend) & M32
        _tsec[field_va] = tsym['section']
        _log.append([field_va, kind, src, exp, tsym['name'][:80], addend])
        if SA_ON and exp is not None: _sa.setdefault(tsym['name'], set()).add((exp - addend) & M32)
        if SA_ON and exp is not None: _sf[field_va] = (exp - addend) & M32
        return src, exp
    def fr(coff, unit, locals_, sec, lo, hi, base_va, buf, stats, pats, scope):
        n0 = len(_log)
        orig_fr(coff, unit, locals_, sec, lo, hi, base_va, buf, stats, pats, scope)
        pe = A.G['pe']; seen = set()
        for e in _log[n0:]:
            va, kind, src, exp = e[:4]; seen.add(va)
            st = 'borrow'
            try: raw = pe.read(va, 4)
            except ValueError: raw = None
            if raw is not None and exp is not None and kind == 0x0B:
                try: st = 'agree' if (pe.secrel(exp) & M32) == struct.unpack('<I', raw)[0] else 'disagree'
                except ValueError: st = 'borrow'
            elif raw is not None and exp is not None and kind in (6, 7, 0x14):
                o32, = struct.unpack('<I', raw)
                obs = (va + 4 + struct.unpack('<i', raw)[0]) & M32 if kind == 0x14 else ((o32 + pe.base) & M32 if kind == 7 else o32)
                st = 'agree' if (exp & M32) == obs else 'disagree'
            e += [st, scope]
        for off, idx, kind in sec['relocs']:
            if lo <= off < hi and base_va + off - lo not in seen:
                _log.append([base_va + off - lo, kind, 'skip', None, coff.symbols[idx]['name'][:80], 0, 'borrow', scope])
    A.resolve_field, A.fill_relocs = rf, fr

def proc4(task):
    _log.clear(); _tsec.clear(); _sa.clear(); _sf.clear()
    if str(task[0] % 100000) in SGSIDE and task[0] < 100000:   # w2: string labels of a recompiled unit are re-bound by content (see sgmap_w2.py)
        import sgmap_w2 as _SG
        task = (task[0], dict(task[1], symbols=_SG.remap(A.Coff(A.HERE / 'obj_v3' / ('%04d.obj' % task[0])), task[1].get('symbols', {}), SGSIDE[str(task[0])])))
    if not task[1].get('eh_tails'):
        task[1]['eh_tails'] = [{'address': '0x0', 'size': 0, 'dummy': True}]
    out = A.process(task)
    out['rl'] = [tuple(e) for e in _log]; out['tsec'] = dict(_tsec)
    if SA_ON: out['sa'] = {k: sorted(v) for k, v in _sa.items()}; _sa.clear(); out['sf'] = dict(_sf); _sf.clear()
    for k in ('stats', 'pats', 'borrows'): out.pop(k, None)
    return out

# ------------------------------------------------------------ CRT (copy of build_extra.run_crt with per-site logging)
def run_crt4(BE, units, pe, cover_text, TEXT_VA, rs, text, libdir, extra_cover):
    import uncovered_v2 as U
    Av2 = BE.A
    cover = cover_text.copy(); cover[extra_cover > 0] = 3
    W = 6; t = bytes(text)
    index = collections.defaultdict(list)
    for p in np.flatnonzero(cover == 0)[:-W].tolist(): index[t[p:p + W]].append(p)
    cands = []
    for lname in ('libcmt.lib', 'libcpmt.lib'):
        for mname, blob in BE.read_ar(libdir / lname):
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
    symnames = Av2.BAM.recipe_names(units)
    imports, thunks = Av2.parse_imports(pe)
    Av2.G['imp'], Av2.G['thunks'] = imports, thunks
    out = []; rejected = []
    for st, f in sorted(matches, key=lambda m: m[0]):
        va = TEXT_VA + st; L = len(f['data']); buf = bytearray(f['data']); sites = []
        for ro, si, ty in f['relocs']:
            nm, value, sec, sty, sc = f['syms'][si]
            if ty not in (0x06, 0x14, 0x07) or ro + 4 > L:
                n = max(0, min(4, L - ro)); buf[ro:ro + n] = pe.read(va + ro, n)
                sites.append((va + ro, ty, 'skip', None, nm[:80], 0, 'borrow', 'crt')); continue
            fva = va + ro; orig = pe.read(fva, 4); o32, = struct.unpack('<I', orig)
            if ty == 0x14:
                addend, = struct.unpack_from('<i', buf, ro); observed = (fva + 4 + struct.unpack('<i', orig)[0]) & M32
            else:
                addend, = struct.unpack_from('<I', buf, ro); observed = o32
                if ty == 0x07: observed = (o32 + pe.base) & M32
            exp = None; src = None
            if sec > 0 and sc == 3 and sec - 1 == f['secidx']: exp, src = va + value + addend, 'self'
            elif sec > 0 and sc == 3: pass
            elif nm in defaddr: exp, src = defaddr[nm] + addend, 'lib-matched'
            elif nm in fnn: exp, src = fnn[nm] + addend, 'recipe-fn'
            elif nm in symnames: exp, src = symnames[nm] + addend, 'symbol-map'
            else:
                m = Av2.ADDR_RE.search(nm)
                if m and not nm.startswith(Av2.NOADDR_PREFIX): exp, src = int(m.group(1), 16) + addend, 'addr-in-name'
                else:
                    a_ = Av2.import_target(nm)
                    if a_ is not None: exp, src = a_ + addend, 'import'
            if (exp is None or exp & M32 != observed) and ty in (6, 0x14):
                _ox = OVL['by_field'].get(fva)
                if _ox is not None: exp, src = _ox, 'overlay-field'
                elif nm in OVL['global_name']: exp, src = OVL['global_name'][nm] + addend, 'overlay-global'
            if exp is None:
                buf[ro:ro + 4] = orig; sites.append((fva, ty, 'unresolved', None, nm[:80], addend, 'borrow', 'crt')); continue
            exp &= M32
            fld = (exp - (fva + 4)) & M32 if ty == 0x14 else (exp if ty == 0x06 else (exp - pe.base) & M32)
            if exp == observed: buf[ro:ro + 4] = struct.pack('<I', fld); st_ = 'agree'
            else: buf[ro:ro + 4] = orig; st_ = 'disagree'
            sites.append((fva, ty, src, exp, nm[:80], addend, st_, 'crt'))
        if bytes(buf) != pe.read(va, L): rejected.append((va, L)); continue
        out.append(dict(address=va, size=L, data=bytes(buf), sites=sites, lib=f['lib'], member=f['member'], symbol=f['sym']))
    return out, rejected, len(matches)

# ------------------------------------------------------------ main
def sha(b): return hashlib.sha256(b).hexdigest()

def main():
    T0 = time.time()
    import build_extra as BE
    units = json.loads((A.FN / 'build/units.json').read_text())['units']
    comp = {}
    for line in (PB / 'logs' / 'compile_v3.jsonl').read_text().splitlines():
        r = json.loads(line); comp[r['index']] = r
    pe = A.Pe(A.IMG); orig = pe.data
    rva0, vs0, rs, raw0 = pe.sections[0]; TEXT_VA = pe.base + rva0
    assert rs == 12441088
    ref = np.frombuffer(orig, np.uint8)[raw0:raw0 + rs]
    seen = collections.defaultdict(set)
    for u in units:
        for f in u['functions']:
            for n in [f['symbol']] + f.get('fold_aliases', []): seen[n].add(int(f['address'], 16))
    fnnames = {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}
    symnames = A.BAM.recipe_names(units)
    imports, thunks = A.parse_imports(pe)
    tasks = [(i, u) for i, u in enumerate(units) if comp[i]['status'] == 'ok']
    tasks += [(k, units[k - 100000]) for k in sorted(EHVAR)]
    results = {}
    with ProcessPoolExecutor(int(os.environ.get('CONTRIB_WORKERS', '12')), initializer=init4, initargs=(fnnames, symnames, imports, thunks)) as ex:
        for r in ex.map(proc4, tasks, chunksize=8): results[r['idx']] = r
    if SA_ON:
        json.dump({str(i): r.get('sa', {}) for i, r in results.items()}, open(HERE.parent / 'link-v2' / 'symaddr.json', 'w'))
        json.dump({str(i): r.get('sf', {}) for i, r in results.items() if i < 100000}, open(HERE.parent / 'link-v2' / 'fieldaddr.json', 'w'), separators=(',', ':'))
    print('pass1 done', round(time.time() - T0), 's', flush=True)

    # recipe coverage over ALL units
    cover = np.zeros(rs, np.uint8); unc = np.zeros(rs, np.uint8)   # unc: range of uncompiled unit
    for i, u in enumerate(units):
        ok = comp[i]['status'] == 'ok'
        for f in u['functions']:
            a = int(f['address'], 16) - TEXT_VA; cover[a:a + f['size']] = 1
            if not ok: unc[a:a + f['size']] = 1
    for i, u in enumerate(units):
        ok = comp[i]['status'] == 'ok'
        for t in u.get('eh_tails', []):
            a = int(t['address'], 16) - TEXT_VA; seg = cover[a:a + t['size']]; seg[seg == 0] = 2
            if not ok: unc[a:a + t['size']] = 1
    S = np.full(rs, 0xcc, np.uint8)           # strict
    Wm = np.zeros(rs, np.uint8)               # 1 fn, 2 recipe tail, 3 eh extra, 4 crt
    B = np.zeros(rs, np.uint8)                # borrowed field bytes (set to 0xCC in strict)
    rej = np.zeros(rs, np.uint8)              # ranges of located-but-rejected pieces
    sites = []                                # (va, kind, src, exp, name, addend, status, origin, unit)
    reasons = collections.Counter()

    BSITES = []
    def place(o, data, P, ents, origin, cls, unit):
        L = len(data); arr = np.frombuffer(data, np.uint8)
        S[o:o + L][P] = arr[P]; Wm[o:o + L][P] = cls
        at = TEXT_VA + o
        for e in ents:
            rel = e[0] - at
            if rel < 0 or rel >= L or not P[rel]: continue
            full = rel + 4 <= L   # wB: was `and P[rel:rel + 4].all()`: a field whose other bytes were already placed by an earlier piece is still resolved in this piece's data
            st = e[6] if full else 'borrow'
            if st != 'agree':
                n = min(4, L - rel); m = P[rel:rel + n]
                S[o + rel:o + rel + n][m] = 0xcc; B[o + rel:o + rel + n][m] = 1
                BSITES.append((e[0], e[1], e[2], e[6], origin, unit, rel, L, int(m.sum())))
            sites.append((e[0], e[1], e[2], e[3], e[4], e[5], st, origin, unit))

    # ---- recipe functions (unit order, first placement wins as in v3)
    nfn_placed = 0; fn_ranges = []
    for i, u in enumerate(units):
        r = results.get(i)
        if r is None: continue
        rl = sorted((e for e in r['rl'] if e[7] == 'fn'), key=lambda e: e[0]); keys = [e[0] for e in rl]
        for rec in r['fn']:
            if rec['data'] is None: reasons['fn-' + (rec['reason'] or '?').split(' (')[0]] += 1; continue
            o = rec['address'] - TEXT_VA; L = rec['size']
            if Wm[o:o + L].any(): reasons['fn-duplicate-address'] += 1; continue
            if rec['data'] != bytes(ref[o:o + L]): reasons['fn-bytes-differ-from-reference'] += 1; rej[o:o + L] = 1; continue
            lo = bisect.bisect_left(keys, rec['address']); hi = bisect.bisect_left(keys, rec['address'] + L)
            place(o, rec['data'], np.ones(L, bool), rl[lo:hi], 'fn', 1, i); nfn_placed += 1; fn_ranges.append((rec['address'], L, rec['symbol']))
    fn_bytes = int((Wm == 1).sum())
    # ---- EH pieces (funclets/tails) of verified contributions: verified by the checker (handler stub + unwind funclets, .text$x): placed first, before any recipe EH piece, never overwritten
    ceh_stat = collections.Counter(); CTSEC = {}
    for t in sorted(json.loads((HERE / 'contrib_pieces.json').read_text()).get('eh', []), key=lambda t: t['address']):
        ceh_stat['located'] += 1
        o = t['address'] - TEXT_VA; data = bytes.fromhex(t['data']); L = len(data)
        if not (0 <= o and o + L <= rs): ceh_stat['outside-text'] += 1; continue
        if not t['ok']: ceh_stat['not-ok'] += 1; continue
        P = (Wm[o:o + L] == 0) & (cover[o:o + L] != 1)
        if not P.any(): ceh_stat['nothing-new'] += 1; continue
        arr = np.frombuffer(data, np.uint8)
        if not (arr[P] == ref[o:o + L][P]).all(): ceh_stat['bytes-differ-from-reference'] += 1; continue
        place(o, data, P, sorted((tuple(e) for e in t['sites']), key=lambda e: e[0]), 'contrib-eh', 6, -3)
        cover[o:o + L][P] = 2; CTSEC.update({int(k): v for k, v in t.get('tsec', {}).items()})
        ceh_stat['placed'] += 1; ceh_stat['new_bytes'] += int(P.sum())
    # ---- verified contributions (accepted local targets): placed right after recipe functions, before any unverified piece
    contrib_stat = collections.Counter()
    cp = json.loads((HERE / 'contrib_pieces.json').read_text())['pieces']
    for p in sorted(cp, key=lambda p: p['address']):
        o = p['address'] - TEXT_VA; L = p['size']; data = bytes.fromhex(p['data'])
        if not (0 <= o and o + L <= rs): contrib_stat['outside-text'] += 1; continue
        if Wm[o:o + L].any(): contrib_stat['overlaps-placed-recipe-function'] += 1; continue
        if data != bytes(ref[o:o + L]): contrib_stat['bytes-differ-from-reference'] += 1; continue
        psites = sorted((tuple(e) for e in p['sites']), key=lambda e: e[0])
        # the __ehhandler$ relocation resolves to our own placed stub only if that stub was placed above; otherwise it stays borrowed
        psites = [(e[:6] + ('borrow',) + e[7:]) if (e[2] == 'eh-stub' and e[3] is not None and not Wm[(e[3] & M32) - TEXT_VA]) else e for e in psites]
        place(o, data, np.ones(L, bool), psites, 'contrib', 5, -2)
        fn_ranges.append((p['address'], L, 'contrib')); CTSEC.update({int(k): v for k, v in p.get('tsec', {}).items()})
        cover[o:o + L] = 1; contrib_stat['placed'] += 1; contrib_stat['bytes'] += L
    # ---- EH pieces from obj_v3 scan: all ok pieces, exact-bytes acceptance
    pieces = []
    for i, r in results.items():
        for t in r['tails']:
            if t['data'] is None: continue
            pieces.append((t['address'], not t['ok'], i, t))
    # wB: among pieces for the same address prefer the one whose relocation fields all resolve (fewest borrowed/disagreeing fields), then the old order
    _rl_by_unit = {}
    def _nbad(p):
        at_, _nk, i_, t_ = p
        if i_ not in _rl_by_unit:
            ee_ = sorted((e for e in results[i_]['rl'] if e[7] in ('tail', 'tail_notok')), key=lambda e: e[0]); _rl_by_unit[i_] = (ee_, [e[0] for e in ee_])
        ee_, kk_ = _rl_by_unit[i_]
        return sum(1 for e in ee_[bisect.bisect_left(kk_, at_):bisect.bisect_left(kk_, at_ + len(t_['data']))] if e[6] != 'agree')
    pieces.sort(key=lambda p: (p[0], p[1], _nbad(p), p[2]))
    eh_stat = collections.Counter(); rlcache = {}
    for at, notok, i, t in pieces:
        eh_stat['located'] += 1
        o = at - TEXT_VA; data = t['data']; L = len(data)
        if not (0 <= o and o + L <= rs): eh_stat['outside-text'] += 1; continue
        if notok:
            eh_stat['not-ok(matcher)'] += 1
            # w2: the matcher's ok flag also fails for a piece whose parent function is unmatched or whose relocation target does not agree
            # (our callee differs from the original's, or the callee name is bound nowhere). Such a piece is still our own compiled code: accept it
            # under the same exact-bytes rule as ok pieces; every field that does not agree is borrowed from the reference (place() marks it B, so it
            # is not counted as ours and is 0xCC in the strict image). A piece with any other byte difference is rejected as before.
            if os.environ.get('FNV_EH_ACCEPT_NOTOK', '1') != '1':
                seg = rej[o:o + L]; seg[Wm[o:o + L] == 0] = 1; continue
        P = (Wm[o:o + L] == 0) & (cover[o:o + L] != 1)
        if not P.any(): eh_stat['nothing-new(already placed/inside function range)'] += 1; continue
        arr = np.frombuffer(data, np.uint8)
        if not (arr[P] == ref[o:o + L][P]).all(): eh_stat['bytes-differ-from-reference'] += 1; rej[o:o + L][Wm[o:o + L] == 0] = 1; continue
        if i not in rlcache:
            ee = sorted((e for e in results[i]['rl'] if e[7] in ('tail', 'tail_notok')), key=lambda e: e[0]); rlcache[i] = (ee, [e[0] for e in ee])
        ee, kk = rlcache[i]
        ents = ee[bisect.bisect_left(kk, at):bisect.bisect_left(kk, at + L)]
        recipe = bool((cover[o:o + L][P] == 2).any())
        place(o, data, P, ents, 'tail', 2 if recipe else 3, i)
        eh_stat['accepted-in-recipe-tail' if recipe else 'accepted-outside-recipe(new)'] += 1
        if notok: eh_stat['accepted-although-matcher-not-ok'] += 1; eh_stat['accepted-not-ok-new_bytes'] += int(P.sum())
    # ---- wB heal pass: a field left borrowed by the piece placed first (callee name unbound in that unit's object) but resolved by another unit's copy of the same piece
    healed = 0
    for at, notok, i, t in pieces:
        if t['data'] is None: continue
        if i not in rlcache:
            ee = sorted((e for e in results[i]['rl'] if e[7] in ('tail', 'tail_notok')), key=lambda e: e[0]); rlcache[i] = (ee, [e[0] for e in ee])
        ee, kk = rlcache[i]; o = at - TEXT_VA; data = t['data']; L = len(data)
        if not (0 <= o and o + L <= rs): continue
        for e in ee[bisect.bisect_left(kk, at):bisect.bisect_left(kk, at + L)]:
            rel = e[0] - at; x = o + rel
            if e[6] != 'agree' or rel < 0 or rel + 4 > L or not B[x:x + 4].any() or bytes(data[rel:rel + 4]) != bytes(ref[x:x + 4]): continue
            S[x:x + 4] = np.frombuffer(data[rel:rel + 4], np.uint8); B[x:x + 4] = 0; healed += 1
            sites.append((e[0], e[1], e[2], e[3], e[4], e[5], 'agree', 'tail', i))
    eh_stat['healed-borrowed-fields'] = healed
    # ---- old-obj EH pieces (not placed; measure only)
    ep = json.loads((CV / 'extra_pieces.json').read_text())
    old_eh = [p for p in ep['pieces'] if p['kind'] == 'eh']
    old_only = 0
    for p in old_eh:
        o = p['address'] - TEXT_VA
        old_only += int((Wm[o:o + p['size']] == 0).sum())
    ehm = np.zeros(rs, np.uint8)
    for p in old_eh: o = p['address'] - TEXT_VA; ehm[o:o + p['size']] = 1
    print('eh done', round(time.time() - T0), 's', flush=True)
    # ---- CRT
    import crt5
    crt5.OVL_ = OVL if OVL['global_name'] or OVL['by_field'] else None
    dsecs = [(pe.base + rva, bytes(orig[raw:raw + rsz])) for (rva, vs, rsz, raw) in pe.sections[1:] if rsz]
    crt, crt_rej, nmatch, crt5stat = crt5.run_crt5(BE, units, pe, cover, TEXT_VA, rs, ref, Path((__import__('os').environ.get('FNV_MSVC9_ROOT', 'C:\\path\\to\\Decompilation\\FNV\\tools\\vc2008').replace('\\', '/') + '/VC/lib')), ehm, dsecs)
    crt_stat = collections.Counter(matched=nmatch, accepted_by_rerun=len(crt), json_crt=sum(1 for p in ep['pieces'] if p['kind'] == 'crt'))
    jc = {p['address']: p['data'] for p in ep['pieces'] if p['kind'] == 'crt'}
    crt_stat['rerun_equals_json'] = sum(1 for c in crt if jc.get(c['address']) == c['data'].hex())
    for c in crt:
        o = c['address'] - TEXT_VA; L = c['size']
        P = (Wm[o:o + L] == 0) & (cover[o:o + L] != 1)
        if not P.any(): crt_stat['nothing-new'] += 1; continue
        arr = np.frombuffer(c['data'], np.uint8)
        if not (arr[P] == ref[o:o + L][P]).all(): crt_stat['bytes-differ'] += 1; continue
        place(o, c['data'], P, [s for s in c['sites']], 'crt', 4, -1); crt_stat['placed'] += 1
    print('crt done', round(time.time() - T0), 's', flush=True)

    # ---- images (in memory only; v5 writes no executables)
    strict = bytearray(orig); strict[raw0:raw0 + rs] = S.tobytes()
    M = Wm > 0
    filled = bytearray(orig)           # holes from reference; produced bytes from our image (non-borrowed)
    fa = np.frombuffer(filled, np.uint8)
    keep = M & (B == 0)
    fa[raw0:raw0 + rs][keep] = S[keep]
    filled_eq = bytes(filled) == bytes(orig)
    (HERE / 'FalloutNV_v7_strict.exe').write_bytes(bytes(strict))
    (HERE / 'FalloutNV_v7_filled.exe').write_bytes(bytes(filled))

    # ---- progress (same definitions as v4)
    padv = np.isin(ref, (0xcc, 0x00))
    ours = M & (B == 0) & ~padv
    padding = padv & (S == ref) & (B == 0)
    bor_bytes = int(B.sum())
    json.dump(BSITES, open(HERE / 'borrowed_sites_v7.json', 'w'))
    json.dump([TEXT_VA + int(x) for x in np.flatnonzero(B)], open(HERE / 'borrowed_bytes_v7.json', 'w'))   # wB: every byte counted in borrowed_relocation_field_bytes
    missing = ~ours & ~padding
    rest = missing & (B == 0)
    cA = rest & (unc == 1)
    cB = rest & ~cA & ((rej == 1) | ((cover > 0)))
    cC = rest & ~cA & ~cB & (cover == 0) & (ref != 0x90)
    total = rs
    prog = dict(
        headline_pct_text_from_our_compile_or_library=round(100 * int(ours.sum()) / total, 3),
        ours_bytes=int(ours.sum()),
        nonpadding_text_bytes=int((~padv).sum()), coverage_pct_of_nonpadding_text=round(100 * int(ours.sum()) / int((~padv).sum()), 3),
        ours_by_origin={k: int((ours & (Wm == c)).sum()) for k, c in (('recipe_functions', 1), ('recipe_eh_tails', 2), ('eh_pieces_outside_recipe', 3), ('crt_lib_functions', 4), ('verified_contributions', 5), ('contribution_eh_pieces', 6))},
        borrowed_relocation_field_bytes=bor_bytes,
        missing_excluding_borrowed_fields=int(rest.sum()), missing_b_failed_pieces=int(cB.sum()), missing_c_undecompiled=int(cC.sum()),
        pieces=dict(contributions=dict(contrib_stat), contribution_eh=dict(ceh_stat), functions_placed=nfn_placed, fn_reject_reasons=dict(reasons), eh=dict(eh_stat), crt=dict(crt_stat), crt5=crt5stat),
        filled_equals_reference=filled_eq,
        reference_sha256_expected_match=(sha(bytes(filled)) == 'df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7'),
        sha256=dict(strict=sha(bytes(strict)), filled=sha(bytes(filled)), reference=sha(orig)),
        undecompiled_bytes=int(cC.sum()),
        strict_nonCC_not_produced=int(((S != 0xcc) & ~M).sum()),
    )
    # ---- relocation statistics
    uniq = {}
    for s in sites: uniq[s[0]] = s
    TSEC = {}
    for r in results.values(): TSEC.update(r['tsec'])
    TSEC.update(CTSEC)
    def cause(s):
        nm = s[4]
        if s[1] == 0x0B: return 'tls-secrel'
        if s[7] == 'crt': return 'crt:' + (s[2] if s[2] not in ('unresolved', 'skip') else ('unresolved:' + A.category(nm)))
        if s[7] == 'tail' and s[2] == 'None': return 'tail:callee-not-in-recipe-symbol-names'
        return '%s:%s:%s' % (s[7], 'k%x' % s[1], s[2])
    bor = [s for s in uniq.values() if s[6] != 'agree']
    prog['relocation_fields'] = dict(total_in_placed_code=len(uniq), borrowed_from_reference=len(bor), resolved_agree=len(uniq) - len(bor),
        by_status=dict(collections.Counter(s[6] for s in uniq.values())), by_source=dict(collections.Counter(s[2] for s in uniq.values())),
        borrowed_by_cause=dict(collections.Counter(cause(s) for s in bor).most_common()),
        borrowed_by_origin_kind_source_status=dict(collections.Counter('%s|k%x|%s|%s' % (s[7], s[1], s[2], s[6]) for s in bor).most_common()))
    with gzip.open(HERE / 'relocs_v7.tsv.gz', 'wt') as f:
        f.write('field_va\tkind\tsource\tstatus\torigin\texpected\ttarget_name\ttarget_section\n')
        for s in sorted(uniq.values()):
            f.write('%08x\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (s[0], {6: 'DIR32', 7: 'DIR32NB', 0x14: 'REL32', 0x0B: 'SECREL'}.get(s[1], str(s[1])), s[2], s[6], s[7], '' if s[3] is None else '%08x' % s[3], s[4], TSEC.get(s[0], '')))
    with gzip.open(HERE / 'borrowed_v7.tsv.gz', 'wt') as f:
        f.write('field_va\tkind\tsource\tstatus\torigin\tcause\ttarget_name\tunit\taddend\n')
        for s in sorted(bor): f.write('%08x\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d\n' % (s[0], s[1], s[2], s[6], s[7], cause(s), s[4], s[8], s[5]))

    # ---- rebase test
    delta = NEWBASE - pe.base
    peo = struct.unpack_from('<I', orig, 0x3c)[0]
    rrva, rsz = struct.unpack_from('<II', orig, peo + 24 + 96 + 5 * 8)
    roff = A.rva2off(pe, rrva); p = roff; tbl = set()
    while p < roff + rsz:
        pg, bs = struct.unpack_from('<II', orig, p)
        if bs == 0: break
        for k in range((bs - 8) // 2):
            w, = struct.unpack_from('<H', orig, p + 8 + 2 * k)
            if w >> 12 == 3: tbl.add(pg + (w & 0xfff))
        p += bs
    def rebase_blob(b):
        b = bytearray(b)
        for r_ in tbl:
            o = A.rva2off(pe, r_)
            v, = struct.unpack_from('<I', b, o); struct.pack_into('<I', b, o, (v + delta) & M32)
        struct.pack_into('<I', b, peo + 52, NEWBASE)
        return b
    refreb = rebase_blob(orig)
    imgsz = struct.unpack_from('<I', orig, peo + 24 + 56)[0]
    imglo, imghi = pe.base, pe.base + imgsz
    # (1) our own relocation rule: a DIR32 we resolved is base-relocated iff its target is inside the image and the COFF target is not an absolute symbol
    rclass = collections.Counter(); reloc_ours = {}
    for s in uniq.values():
        if s[1] != 6 or s[6] != 'agree': continue
        ex = s[3]
        if TSEC.get(s[0]) == -1: c = 'abs-symbol(no base reloc)'
        elif not (imglo <= ex < imghi): c = 'target-outside-image(no base reloc)'
        else: c = 'address'; reloc_ours[s[0]] = s
        rclass[c] += 1
    # (2) literal inference: 32-bit imm/disp in our own code, no relocation record, value == exact address of an object our build already knows
    exps = set(int(s[3]) for s in uniq.values() if s[1] == 6 and s[6] == 'agree')
    Kset = set(exps)
    for u in units:
        for v in u.get('symbols', {}).values():
            try: Kset.add(int(v, 0) & M32)
            except (ValueError, TypeError): pass
        for fx in u['functions']: Kset.add(int(fx['address'], 16))
    chunks = [[] for _ in range(48)]
    for j, (a_, L_, _sym) in enumerate(fn_ranges): chunks[j % 48].append((a_, bytes(S[a_ - TEXT_VA:a_ - TEXT_VA + L_])))
    cands = []
    with ProcessPoolExecutor(12) as ex2:
        for part in ex2.map(scan_chunk, [(c, imglo, imghi) for c in chunks if c]): cands += part
    def rnd(v): return v & 0xffff == 0 or (v & 0xffffff) == 0xffffff or (v & 0xfff) == 0xfff
    known = set(uniq)
    inferred = {}
    for fa_, v, mn in cands:
        if any((fa_ + d) in known for d in range(-3, 4)): continue
        if mn in LIT_MN and v in Kset and not rnd(v) and v not in INTCONST: inferred[fa_] = v
    (HERE / 'inferred_literals_v7.json').write_text(json.dumps({'0x%08x' % k: '0x%08x' % v for k, v in sorted(inferred.items())}))
    prog['literal_inference'] = dict(candidates_imm_disp_in_image_without_reloc_record=len(cands), inferred_as_address=len(inferred),
        rule='mnemonic in %s, value == exact address of an object known to our build (our resolved targets, units.json symbol addresses, recipe function addresses), value not round (low 16 bits 0 / 0xffffff / 0xfff pattern)' % sorted(LIT_MN))
    # (3) rebase our image
    def build(reloc_fields, inferred_fields):
        Sr = S.copy()
        for fa_ in list(reloc_fields) + list(inferred_fields):
            o = fa_ - TEXT_VA; v, = struct.unpack('<I', S[o:o + 4].tobytes()); Sr[o:o + 4] = np.frombuffer(struct.pack('<I', (v + delta) & M32), np.uint8)
        oa = bytearray(refreb); oarr = np.frombuffer(oa, np.uint8)
        oarr[raw0:raw0 + rs][keep] = Sr[keep]
        return np.frombuffer(bytes(oa), np.uint8)[raw0:raw0 + rs]
    tr = np.frombuffer(bytes(refreb), np.uint8)[raw0:raw0 + rs]
    def run_variant(reloc_fields, inferred_fields):
        to = build(reloc_fields, inferred_fields); return np.flatnonzero(tr != to)
    tbl_text_va = set(pe.base + r_ for r_ in tbl if rva0 <= r_ < rva0 + rs)
    variants = {}
    variants['v4_rule'] = run_variant({s[0] for s in uniq.values() if s[1] == 6 and s[6] == 'agree' and imglo <= s[3] < imghi}, {})
    variants['v5_rule'] = run_variant(set(reloc_ours), inferred)
    # table-assisted check (uses the original .reloc table, so NOT independent): shows nothing else differs
    ours_fields_all = {s[0] for s in uniq.values() if s[1] == 6 and s[6] == 'agree'}
    asst = {f_ for f_ in tbl_text_va if M[f_ - TEXT_VA:f_ - TEXT_VA + 4].all() and B[f_ - TEXT_VA:f_ - TEXT_VA + 4].sum() == 0}
    variants['table_assisted'] = run_variant(asst, {})
    prog['rebase_test'] = dict(delta=hex(delta), reloc_table_highlow_sites=len(tbl), reloc_sites_in_text=len(tbl_text_va),
        our_dir32_agree_classes=dict(rclass), text_bytes_differing={k: int(len(v)) for k, v in variants.items()},
        text_bytes_differing_note='v4_rule = shift every DIR32 we resolved whose target is in the image (as v4); v5_rule = own rule + literal inference; table_assisted = original .reloc decides (not independent)')
    dd = variants['v5_rule']
    cls = collections.defaultdict(list)
    for d_ in dd.tolist():
        va = TEXT_VA + d_
        f_ = next((va - k for k in range(4) if (va - k) in tbl_text_va or (va - k) in reloc_ours or (va - k) in inferred), None)
        if f_ is None: cls['unclassified'].append((va, None)); continue
        if f_ in reloc_ours and f_ not in tbl_text_va: cls['we-shift-a-field-the-original-does-not-relocate'].append((f_, reloc_ours[f_][4]))
        elif f_ in inferred and f_ not in tbl_text_va: cls['inferred-literal-not-in-original-table'].append((f_, 'inferred'))
        elif f_ in tbl_text_va and f_ not in reloc_ours and f_ not in inferred: cls['original-relocates-a-field-we-emit-as-plain-literal'].append((f_, None))
        else: cls['other'].append((f_, None))
    fields = {k: sorted(set(v)) for k, v in cls.items()}
    prog['rebase_test']['remaining_diff_fields_by_cause'] = {k: len(v) for k, v in fields.items()}
    remain = {}
    for k, v in fields.items():
        remain[k] = [dict(field='0x%08x' % f_, value=hex(struct.unpack('<I', S[f_ - TEXT_VA:f_ - TEXT_VA + 4].tobytes())[0]), symbol=nm) for f_, nm in v]
    (HERE / 'rebase_remaining_v7.json').write_text(json.dumps(remain, indent=1))
    if (HERE / 'icf_report.json').exists(): prog['icf_fold'] = json.loads((HERE / 'icf_report.json').read_text())
    prog['seconds'] = round(time.time() - T0)
    (HERE / 'progress.json').write_text(json.dumps(prog, indent=1))
    print(json.dumps(prog, indent=1)[:9000])

LIT_MN = ('mov', 'push', 'fld', 'fstp', 'fcomp', 'lea')

def scan_chunk(arg):
    chunk, lo, hi = arg
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
    md = Cs(CS_ARCH_X86, CS_MODE_32); md.detail = True
    out = []
    for a, code in chunk:
        for ins in md.disasm(code, a):
            for off, size in ((ins.imm_offset, ins.imm_size), (ins.disp_offset, ins.disp_size)):
                if size == 4 and off:
                    fa_ = ins.address + off
                    v = struct.unpack_from('<I', code, fa_ - a)[0]
                    if lo <= v < hi: out.append((fa_, v, ins.mnemonic))
    return out

if __name__ == '__main__':
    main()
