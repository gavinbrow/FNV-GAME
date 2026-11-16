import os, collections, json, re, struct, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent; RN = HERE.parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(RN / 'pinned-build')); sys.path.insert(0, str(RN / 'data-v3'))
import coffrw, uncovered_v2 as U
from common import SEC, TLO, THI, sec_of
symaddr = json.load(open(HERE / 'symaddr.json'))
g = collections.defaultdict(set)
for idx, d in symaddr.items():
    for nm, a in d.items():
        g[nm].update(a)
_u = json.load(open(RN.parent / 'fnv_decomp' / 'build' / 'units.json')); _us = _u['units'] if isinstance(_u, dict) else _u
gu = collections.defaultdict(set)          # recipe-derived (reference-derived) name -> address
for x in _us:
    for f in x['functions']:
        for nm in [f['symbol']] + f.get('fold_aliases', []): gu[nm].add(int(f['address'], 16))
    for nm, a in x.get('symbols', {}).items():
        try: gu[nm].add(int(a, 16))
        except Exception: pass
libnames = set()
for ln in ('libcmt.lib', 'libcpmt.lib'):
    for mname, blob in U.read_ar(Path(r'C:\Projects\Decompilation\FNV\tools\vc2008\VC\lib') / ln):
        r = U.parse_obj(blob)
        if r:
            for si, (nm, value, sec, ty, sc) in r[1].items():
                if sc == 2 and sec > 0: libnames.add(nm)
ADDR = re.compile(r'(?<![0-9A-Za-z])(?:FUN|DAT|PTR|LAB|SUB|UNK|OFF|BYTE|WORD|DWORD|switchD|caseD|LOC|g)_([0-9a-f]{8})(?![0-9A-Za-z])')
bss_lo = SEC['.data']['va'] + SEC['.data']['raw']; bss_hi = SEC['.data']['va'] + SEC['.data']['vs']
def kind_of(va):
    if TLO <= va < THI: return 'C'
    if bss_lo <= va < bss_hi or sec_of(va) in ('.rdata', '.data', '.tls', 'CONST'): return 'D'
OUT = HERE / 'obj_contrib_rw'; OUT.mkdir(exist_ok=True)
stat = collections.Counter(); extra = set(); ct = set(); un = collections.Counter()
for p in sorted((HERE / 'obj_contrib').glob('*.obj')):
    addr = int(p.stem, 16); b = p.read_bytes(); ren = {}; defren = False
    for i, nm, value, sec, ty, sc, naux, o in coffrw.symbols(b):
        if sc != 2: continue
        if sec > 0:
            if nm.startswith('?FUN_%08x@' % addr) or nm == '_FUN_%08x' % addr or nm == 'FUN_%08x' % addr: ren[nm] = 'C_%08x' % addr; defren = True; stat['defined function -> C_'] += 1
        elif sec == 0 and value == 0:
            if nm.startswith('__imp_') or nm in libnames: stat['kept lib/import'] += 1; continue
            a = g.get(nm); va = None
            if a and len(a) == 1: va = next(iter(a))
            elif a: stat['ambiguous'] += 1; un[nm] += 1; continue
            else:
                m = ADDR.search(nm); a2 = gu.get(nm)
                if m: va = int(m.group(1), 16)
                elif a2 and len(a2) == 1: va = next(iter(a2)); stat['resolved from recipe symbols'] += 1
            if va is None or kind_of(va) is None: stat['no address'] += 1; un[nm] += 1; continue
            k = kind_of(va); ren[nm] = '%s_%08x' % (k, va); stat['undefined -> ' + k] += 1
            (ct if k == 'C' else extra).add(va)
    nb, n = coffrw.rewrite(b, ren)
    if not defren:
        secs_ = coffrw.sections(nb); idxn = {}
        from common import ref as _ref0
        _T0 = _ref0[SEC['.text']['off']:SEC['.text']['off'] + SEC['.text']['raw']]
        def _matches(sd):
            rp, = struct.unpack_from('<I', nb, sd['hdr'] + 20); dat = nb[rp:rp + sd['size']]
            if not dat or addr - TLO + len(dat) > len(_T0): return False
            m = bytearray(b'' * len(dat))
            for r in range(sd['nrel']):
                ro, = struct.unpack_from('<I', nb, sd['relptr'] + 10 * r); t_, = struct.unpack_from('<H', nb, sd['relptr'] + 10 * r + 8)
                for q in range(ro, min(ro + (2 if t_ == 0x0a else 4), len(dat))): m[q] = 0
            return all(_T0[addr - TLO + q] == dat[q] for q in range(len(dat)) if m[q])
        cands = [(i, nm, sec) for i, nm, value, sec, ty, sc, naux, o in coffrw.symbols(nb) if sec > 0 and sc in (2, 3) and value == 0 and (ty & 0x20) and (secs_[sec - 1]['flags'] & 0x20) and not nm.startswith('.')]
        good = [c for c in cands if _matches(secs_[c[2] - 1])]
        pick = (good or cands)[:1]
        for i, nm, sec in pick: idxn[i] = 'C_%08x' % addr
        if good: stat['other-name function chosen by byte match'] += 1
        if idxn: nb, _n = coffrw.rewrite_idx(nb, idxn); stat['defined function (other name) -> C_'] += 1
    # dynamic initializers / CRT$XC entries inside a contribution are compiler by-products: the original initializer lives in another unit, so they are not linked
    _s0 = coffrw.sections(nb); _sy = list(coffrw.symbols(nb))
    _keep = {sec for i, nm, value, sec, ty, sc, naux, o in _sy if nm == 'C_%08x' % addr and sec > 0}
    _dr = {x['index'] for x in _s0 if (x['name'] in ('.text$yc', '.text$yd') or x['name'].startswith('.CRT$XC')) and x['index'] not in _keep}
    _inf = coffrw.comdat_info(nb); _chg = True
    while _chg:
        _chg = False
        for k_, (sel_, num_, ex_) in _inf.items():
            if sel_ == 5 and num_ in _dr and k_ not in _dr and k_ not in _keep: _dr.add(k_); _chg = True
    if _dr: nb = coffrw.rebuild(nb, _dr, {}); stat['initializer sections dropped'] += len(_dr)
    # unreachable by-product COMDAT code (deleting destructors, inline helpers) that nothing in the kept contribution references is not linked
    _s1 = coffrw.sections(nb); _y1 = list(coffrw.symbols(nb)); _inf1 = coffrw.comdat_info(nb); _ss = {i: sec for i, nm, value, sec, ty, sc, naux, o in _y1}
    _cand = {k for k, (sel_, num_, ex_) in _inf1.items() if sel_ != 5 and (_s1[k - 1]['flags'] & 0x20) and not any(n_.startswith('C_') for n_, t_ in ex_)}
    if _cand:
        _roots = [x['index'] for x in _s1 if x['index'] not in _cand]; _seen = set(_roots); _st = list(_roots)
        while _st:
            k = _st.pop(); x = _s1[k - 1]
            for r in range(x['nrel']):
                t = _ss.get(struct.unpack_from('<I', nb, x['relptr'] + 10 * r + 4)[0], 0)
                if t > 0 and t not in _seen: _seen.add(t); _st.append(t)
        _un = _cand - _seen; _chg = True
        while _chg:
            _chg = False
            for k_, (sel_, num_, ex_) in _inf1.items():
                if sel_ == 5 and num_ in _un and k_ not in _un: _un.add(k_); _chg = True
        if _un: nb = coffrw.rebuild(nb, _un, {}); stat['unreachable by-product COMDATs dropped'] += len(_un)
    # per-site binding for names with no address: our compiled function is byte-identical in shape to the original at <addr>, so the original call/ptr at the same field gives the target
    from common import ref as _ref
    _T = _ref[SEC['.text']['off']:SEC['.text']['off'] + SEC['.text']['raw']]
    _secs = coffrw.sections(nb); _S = list(coffrw.symbols(nb)); _name = {i: (nm, sec, sc) for i, nm, value, sec, ty, sc, naux, o in _S}
    relnames_ = {}
    def _find(data, rl, rn=()):
        mask = bytearray(b'' * len(data))
        for o, ty in rl:
            for q in range(o, min(o + (2 if ty == 0x0a else 4), len(data))): mask[q] = 0
        best = None; i2 = 0
        while i2 < len(data):
            if mask[i2]:
                j2 = i2
                while j2 < len(data) and mask[j2]: j2 += 1
                if best is None or j2 - i2 > best[1] - best[0]: best = (i2, j2)
                i2 = j2
            else: i2 += 1
        if not best or best[1] - best[0] < 6: return None
        a, b_ = best; key = data[a:b_][:12]; hits = []; p_ = _T.find(key)
        while p_ >= 0 and len(hits) < 400:
            st = p_ - a
            if st >= 0 and st + len(data) <= len(_T) and all(_T[st + q] == data[q] for q in range(len(data)) if mask[q]): hits.append(st)
            p_ = _T.find(key, p_ + 1)
        if len(hits) > 1 and rn:
            good = []
            for st in hits:
                ok = True
                for ro, ty_, nm2 in rn:
                    m2 = re.fullmatch(r'[CD]_([0-9a-f]{8})', nm2)
                    if not m2: continue
                    t2 = int(m2.group(1), 16); raw2 = struct.unpack_from('<i', _T, st + ro)[0]
                    exp = (t2 - (TLO + st + ro + 4)) if ty_ == 0x14 else t2
                    if (raw2 & 0xffffffff) != (exp & 0xffffffff): ok = False; break
                if ok: good.append(st)
            hits = good
        return TLO + hits[0] if len(hits) == 1 else None
    for sd in _secs:
        if not (sd['flags'] & 0x20) or not sd['nrel'] or not sd['size']: continue
        rptr, = struct.unpack_from('<I', nb, sd['hdr'] + 20); data = nb[rptr:rptr + sd['size']]
        rl = []
        for r in range(sd['nrel']):
            ro, = struct.unpack_from('<I', nb, sd['relptr'] + 10 * r); ty_, = struct.unpack_from('<H', nb, sd['relptr'] + 10 * r + 8); rl.append((ro, ty_))
        if any(sec == sd['index'] and nm == 'C_%08x' % addr and value == 0 for i, nm, value, sec, ty, sc, naux, o in _S): base_va = addr
        else: base_va = _find(data, rl, [(ro_, t__, _name.get(struct.unpack_from('<I', nb, sd['relptr'] + 10 * r_ + 4)[0], ('',))[0]) for r_, (ro_, t__) in enumerate(rl)])
        if os.environ.get('PCD') == p.stem: print('PCD', sd['name'], base_va)
        if base_va is None: continue
        for r in range(sd['nrel']):
            si, ty_ = struct.unpack_from('<IH', nb, sd['relptr'] + 10 * r + 4); ro, = struct.unpack_from('<I', nb, sd['relptr'] + 10 * r)
            nm_, sec_, sc_ = _name.get(si, ('', 0, 0))
            if sec_ != 0 or sc_ != 2 or nm_.startswith(('C_', 'D_', '__imp_')) or nm_ in libnames: continue
            fva = base_va + ro
            if not (TLO <= fva < THI - 4): continue
            raw = struct.unpack_from('<i', _T, fva - TLO)[0]
            tgt = (fva + 4 + raw) & 0xffffffff if ty_ == 0x14 else (raw & 0xffffffff if ty_ == 6 else None)
            if tgt is None or kind_of(tgt) is None: continue
            k_ = kind_of(tgt); relnames_[(sd['index'], r)] = '%s_%08x' % (k_, tgt); stat['relocations bound per site (reference field)'] += 1
            (ct if k_ == 'C' else extra).add(tgt)
    if relnames_: nb = coffrw.rebuild(nb, set(), {}, relnames_)
    # defined data (vtables, statics) whose symbol has a verified original address: drop our copy and bind to the placed D_<va>
    syms_ = list(coffrw.symbols(nb)); secs_ = coffrw.sections(nb); bys = collections.defaultdict(list)
    for i, nm, value, sec, ty, sc, naux, o in syms_:
        if sec > 0: bys[sec].append((i, nm, value, sc, naux))
    drop_ = set(); nn = {}
    for k, lst in bys.items():
        sd = secs_[k - 1]
        if sd['flags'] & 0x20 or sd['flags'] & 0x02000000: continue
        ext = [(i, nm, v) for i, nm, v, sc, na in lst if sc == 2]
        sec_sym = [i for i, nm, v, sc, na in lst if sc == 3 and na and nm.startswith('.')]
        if not ext or len(lst) != len(ext) + len(sec_sym): continue
        bases = set()
        for i_, nm_, v_ in ext:
            a = g.get(nm_); a = a if a and len(a) == 1 else gu.get(nm_)
            if a and len(a) == 1: bases.add(next(iter(a)) - v_)
            elif ADDR.search(nm_) and kind_of(int(ADDR.search(nm_).group(1), 16)) == 'D': bases.add(int(ADDR.search(nm_).group(1), 16) - v_)
            elif nm_.startswith('??_7'):
                m_ = re.search(r'_([0-9a-f]{8})@@6B@$', nm_)
                if m_: bases.add(int(m_.group(1), 16) - v_)
        if len(bases) != 1: continue
        base = next(iter(bases))
        if kind_of(base) != 'D' or kind_of(base + sd['size'] - 1) != 'D': continue
        drop_.add(k)
        for i_, nm_, v_ in ext: nn[i_] = 'D_%08x' % (base + v_); extra.add(base + v_)
        for i_ in sec_sym: nn[i_] = 'D_%08x' % base
        extra.add(base)
    if drop_:
        nb = coffrw.rebuild(nb, drop_, nn); stat['defined data redirected to D_'] += len(drop_)
    (OUT / p.name).write_bytes(nb)
print(dict(stat), 'unresolved names', len(un), un.most_common(8))
old = set(json.load(open(HERE / 'extra_labels.json'))); new = extra - old
print('extra data labels needed by contributions not yet emitted', len(new))
json.dump(sorted(old | extra), open(HERE / 'extra_labels.json', 'w'))
oc = set(json.load(open(HERE / 'code_targets.json'))); json.dump(sorted(oc | ct), open(HERE / 'code_targets.json', 'w'))
