r"""link-v2 prep3.py: unit objects -> link objects.
 1. recipe functions -> C_<va>;  2. unplaced code COMDATs (and their EH children) removed;
 3. data sections that data-v1 placed (secmap.json) are removed and every reference to them is redirected to the appended undefined symbol D_<va> (symbol-level: named symbols at their
    placed address, section symbols only for single-piece sections); a data section is only removed when every reference to it could be redirected;
 4. remaining undefined externals with a verified address (symaddr.json) -> C_/D_<va>.
Writes obj_rw\<idx>.obj (overwrites), extra_labels.json, code_targets.json, prep3_report.json. usage: python -I prep3.py"""
import os
import collections
import json
import re
import struct
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RN = HERE.parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(RN / 'pinned-build')); sys.path.insert(0, str(RN / 'data-v3'))
import coffrw
import uncovered_v2 as U
from common import SEC, TLO, THI, sec_of, read_ref

units = json.loads(open(r'C:\Projects\Decompilation\fnv_decomp\build\units.json').read())['units']
symaddr = json.load(open(HERE / 'symaddr.json'))
secmap = json.load(open(HERE / 'secmap.json'))
ehp = json.load(open(HERE / 'eh_pieces.json'))
fieldaddr = json.load(open(HERE / 'fieldaddr.json'))
choice = {}
for _u in sorted(ehp, key=int):
    for _k, _l in ehp[_u].items():
        for _s0, _s1, _at in _l: choice.setdefault(_at, (int(_u), int(_k)))      # one defining (unit, section) per EH piece address: the lowest unit index, then section
json.dump({hex(a): list(u) for a, u in choice.items()}, open(HERE / 'eh_choice.json', 'w'))
libnames = set()
for ln in ('libcmt.lib', 'libcpmt.lib'):
    for mname, blob in U.read_ar(Path(r'C:\Projects\Decompilation\FNV\tools\vc2008\VC\lib') / ln):
        r = U.parse_obj(blob)
        if r:
            for si, (nm, value, sec, ty, sc) in r[1].items():
                if sc == 2 and sec > 0: libnames.add(nm)
bss_lo = SEC['.data']['va'] + SEC['.data']['raw']; bss_hi = SEC['.data']['va'] + SEC['.data']['vs']


def kind_of(va):
    if TLO <= va < THI: return 'C'
    if bss_lo <= va < bss_hi or sec_of(va) in ('.rdata', '.data', '.tls', 'CONST'): return 'D'


owner = {}
for _i, _u in enumerate(units):
    for _f in _u['functions']: owner.setdefault(int(_f['address'], 16), _i)      # build rule: the first unit (in unit order) that lists the address places it
DATA_NAMES = ('.rdata', '.data', '.bss', '.CRT', '.tls', 'CONST', '.xdata')
OUT = HERE / 'obj_rw'; OUT.mkdir(exist_ok=True)
stat = collections.Counter(); extra = set(); ctargets = set(); unresolved = collections.Counter(); multi = collections.Counter()


def reloc_syms(b, secs, drop):
    out = collections.defaultdict(int)
    for s in secs:
        if s['index'] in drop or not s['nrel']: continue
        for r in range(s['nrel']):
            out[struct.unpack_from('<I', b, s['relptr'] + 10 * r + 4)[0]] += 1
    return out


_TT = ref[SEC['.text']['off']:SEC['.text']['off'] + SEC['.text']['raw']]
REV = set(json.load(open(HERE / 'revive_names.json'))) if (HERE / 'revive_names.json').exists() else set()
for p in sorted((RN / 'pinned-build' / 'obj_v3').glob('*.obj'), key=lambda x: int(x.stem)):
    idx = int(p.stem); b = p.read_bytes(); u = units[idx] if idx < len(units) else None
    ren = {}
    if u:
        byname = collections.defaultdict(set)
        for f in u['functions']:
            for nm in [f['symbol']] + f.get('fold_aliases', []): byname[nm].add(int(f['address'], 16))
        for nm, a in byname.items():
            if len(a) == 1 and owner.get(next(iter(a))) == idx: ren[nm] = 'C_%08x' % next(iter(a))
            elif len(a) == 1: stat['recipe function owned by another unit (not defined here)'] += 1
            else: stat['function name with several addresses in one unit'] += 1
    b1, n1 = coffrw.rewrite(b, ren)
    pcs = ehp.get(str(idx), {})
    if pcs:
        idxn = {}
        for i, nm, value, sec, ty, sc, naux, o in coffrw.symbols(b1):
            if sec > 0 and sc in (2, 3) and not nm.startswith(('C_', '.')) and str(sec) in pcs:
                for s0, s1, at in pcs[str(sec)]:
                    if value == s0 and kind_of(at) == 'C' and choice.get(at) == (idx, sec) and at not in owner: idxn[i] = 'C_%08x' % at; break
        if idxn: b1, nn = coffrw.rewrite_idx(b1, idxn); stat['EH piece symbols -> C_<va>'] += nn
    b1, nsp = coffrw.split_packs(b1); stat['funclet packs split'] += nsp
    secs = coffrw.sections(b1); info = coffrw.comdat_info(b1)
    revive = set(); _it = 0
    while True:
        _it += 1
        # --- code removal set
        rem = set()
        for k, (sel, num, ex) in info.items():
            s = secs[k - 1]
            if (s['flags'] & 0x20) and sel != 5 and not any(n.startswith('C_') for n, ty in ex): rem.add(k)
        ch = True
        while ch:
            ch = False
            for k, (sel, num, ex) in info.items():
                if sel == 5 and num in rem and k not in rem: rem.add(k); ch = True
        rem |= {s['index'] for s in secs if s['name'] == '.sxdata'}
        if REV:
            for _i, _nm, _v, _sec, _ty, _sc, _na, _o in coffrw.symbols(b1):
                if _sec in rem and _sc == 2 and _nm in REV: revive.add(_sec)
        if revive:
            _cl = set(revive); _ch = True
            while _ch:
                _ch = False
                for k, (sel, num, ex) in info.items():
                    if sel == 5 and num in _cl and k not in _cl: _cl.add(k); _ch = True
            rem -= _cl
        stat['code COMDATs removed (unplaced)'] += len(rem) - sum(1 for s in secs if s['name'] == '.sxdata')
        # --- data sections: placed ones are redirected to D_<va>, defined data symbols with a verified address likewise; unreachable COMDAT data is dropped
        sa = symaddr.get(str(idx), {})
        syms = list(coffrw.symbols(b1)); symsec = {i: sec for i, nm, value, sec, ty, sc, naux, o in syms}
        _sn = {i: nm for i, nm, value, sec, ty, sc, naux, o in syms}
        def symname_nm(i): return _sn.get(i, '')
        isdata = lambda s: not (s['flags'] & 0x20) and not (s['flags'] & 0x02000000) and s['name'].startswith(DATA_NAMES)
        placed = {}
        for s in secs:
            if s['index'] in rem or not isdata(s): continue
            ent = secmap.get('%d:%d' % (idx, s['index']))
            if ent and sum(b_ - a_ for a_, b_, v in ent) >= s['size']: placed[s['index']] = ent
        newnames = {}
        for i, nm, value, sec, ty, sc, naux, o in syms:
            if sec <= 0 or sec in rem: continue
            if sec in placed:
                ent = placed[sec]; va = None
                if sc == 3 and naux >= 1 and value == 0 and nm.startswith('.'):
                    if len(ent) == 1: va = ent[0][2]
                else:
                    for a_, b_, v in ent:
                        if a_ <= value < b_: va = v + value - a_; break
                if va is not None: newnames[i] = 'D_%08x' % va; extra.add(va)
            elif isdata(secs[sec - 1]) and sc in (2, 3) and not (sc == 3 and naux >= 1 and nm.startswith('.')):
                a = sa.get(nm)
                if a and len(a) == 1 and kind_of(a[0]) == 'D' and value == 0:
                    newnames[i] = 'D_%08x' % a[0]; extra.add(a[0]); stat['defined data symbol redirected by verified address'] += 1
        # EH stubs: the original handler stub (known address of `__ehhandler$...`) loads the original FuncInfo; redirect our stub's FuncInfo reference to that D_<va>
        relnames0 = {}
        secsym = collections.defaultdict(list)
        for i, nm, value, sec, ty, sc, naux, o in syms:
            if sec > 0: secsym[sec].append((nm, value))
        for s_ in secs:
            if s_['index'] in rem or not s_['nrel'] or not s_['name'].startswith('.text$x'): continue
            hn = [nm for nm, v in secsym.get(s_['index'], []) if nm.startswith('__ehhandler$')]
            if not hn: continue
            a = sa.get(hn[0])
            if not a or len(a) != 1: continue
            code = read_ref(a[0], 48)
            m_ = re.search(bytes([0xb8]) + b'(....)' + bytes([0xe9]), code, re.S) if code else None
            if not m_: continue
            fi = struct.unpack('<I', m_.group(1))[0]
            if kind_of(fi) != 'D': continue
            for r in range(s_['nrel']):
                si, = struct.unpack_from('<I', b1, s_['relptr'] + 10 * r + 4)
                if symname_nm(si).startswith('__ehfuncinfo$'): relnames0[(s_['index'], r)] = 'D_%08x' % fi; extra.add(fi); stat['EH stub FuncInfo redirected to the original table'] += 1
        comdat = {k for k in info}
        roots = [s['index'] for s in secs if s['index'] not in rem and (((s['flags'] & 0x20) and not (s['name'].startswith('.text$x') and not any(n.startswith('C_') for n, ty in info.get(s['index'], [0, 0, []])[2]))) or (not isdata(s) and not (s['flags'] & 0x02000000) and not s['name'].startswith('.text$x')) or False)]
        seen = set(roots); stack = list(roots); par = {}
        while stack:
            k = stack.pop(); s = secs[k - 1]
            for r in range(s['nrel']):
                if (k, r) in relnames0: continue
                si = struct.unpack_from('<I', b1, s['relptr'] + 10 * r + 4)[0]
                if si in newnames: continue
                t = symsec.get(si, 0)
                if t > 0 and t not in rem and t not in seen: seen.add(t); stack.append(t); par[t] = (k, si)
        if os.environ.get('PK_DBG') == str(idx):
            for t in sorted(seen):
                if secs[t-1]['name'].startswith('.text$x') and t not in roots:
                    ch = [t]
                    while ch[-1] in par: ch.append(par[ch[-1]][0])
                    print('DBG', [(c, secs[c-1]['name'], [n for n, v in secsym.get(c, [])][:2]) for c in ch][:5]); break
        dropdata = {s['index'] for s in secs if (isdata(s) or s['name'].startswith('.text$x')) and s['index'] not in rem and s['index'] not in seen}
        stat['data sections dropped (placed/redirected or unreachable)'] += len(dropdata)
        drop = set(rem) | dropdata
        names2 = {i: n for i, n in newnames.items() if symsec.get(i) in dropdata}
        # per-site binding: relocations to undefined names that have several (or no) verified addresses get the address of THEIR field
        relnames = dict(relnames0); fa = fieldaddr.get(str(idx), {}); pcs2 = ehp.get(str(idx), {})
        symname = {i: (nm, sec, sc) for i, nm, value, sec, ty, sc, naux, o in syms}
        secbase = {}
        for i, nm, value, sec, ty, sc, naux, o in syms:
            if sec > 0 and sc == 2 and nm.startswith('C_') and value == 0 and sec not in secbase: secbase[sec] = int(nm[2:], 16)
        cpos = collections.defaultdict(list)
        for i, nm, value, sec, ty, sc, naux, o in syms:
            if sec > 0 and sc == 2 and nm.startswith('C_'): cpos[sec].append((value, int(nm[2:], 16)))
        for _k in cpos: cpos[_k].sort()
        for s in secs:
            if s['index'] in drop or not s['nrel'] or not (s['flags'] & 0x20): continue
            for r in range(s['nrel']):
                si, = struct.unpack_from('<I', b1, s['relptr'] + 10 * r + 4); ro, = struct.unpack_from('<I', b1, s['relptr'] + 10 * r)
                nm, sec_, sc_ = symname.get(si, ('', 0, 0))
                if os.environ.get('PK_DBG2') == str(idx) and 'PointerArrayBase' in nm: print('DBG1', s['index'], s['name'], nm, sec_, sc_, s['index'] in drop)
                if sc_ != 2 or nm.startswith(('C_', 'D_', '__imp_')) or nm in libnames: continue
                if sec_ != 0 and sec_ not in rem: continue
                a = sa.get(nm)
                if a and len(a) == 1: continue
                fva = None
                if s['index'] in secbase and not cpos.get(s['index']): fva = secbase[s['index']] + ro
                elif cpos.get(s['index']) and any(v_ <= ro for v_, a_ in cpos[s['index']]):
                    _l = [(v_, a_) for v_, a_ in cpos[s['index']] if v_ <= ro]
                    if ro - _l[-1][0] < 8192: fva = _l[-1][1] + ro - _l[-1][0]
                elif str(s['index']) in pcs2:
                    for s0, s1, at in pcs2[str(s['index'])]:
                        if s0 <= ro < s1: fva = at + ro - s0; break
                base = fa.get(str(fva)) if fva is not None else None
                if base is None and fva is not None and s['index'] in secbase_or_pieces(s['index']) and TLO <= fva < THI - 4:
                    _ty, = struct.unpack_from('<H', b1, s['relptr'] + 10 * r + 8); _raw, = struct.unpack_from('<i', read_ref_raw(fva, 4), 0) if False else (struct.unpack_from('<i', _TT, fva - TLO)[0],)
                    base = ((fva + 4 + _raw) & 0xffffffff) if _ty == 0x14 else ((_raw & 0xffffffff) if _ty == 6 else None)
                    if base is not None and kind_of(base) is not None: stat['relocations bound per site (reference field decode)'] += 1
                    else: base = None
                if os.environ.get('PK_DBG2') == str(idx) and 'PointerArrayBase' in nm: print('DBG2', s['index'], s['name'], nm, fva, base, s['index'] in secbase, s['index'] in pcs2)
                if base is None: continue
                k = kind_of(base)
                if k is None: continue
                relnames[(s['index'], r)] = '%s_%08x' % (k, base); stat['relocations bound per site'] += 1
                (ctargets if k == 'C' else extra).add(base)
        b2 = coffrw.rebuild(b1, drop, names2, relnames)
        # revival: kept code that still references a removed (unplaced) code COMDAT without any address gets that COMDAT (real compiled code) linked in
        newrev = set()
        for s_ in secs:
            if s_['index'] in drop or not s_['nrel'] or not (s_['flags'] & 0x20): continue
            for r_ in range(s_['nrel']):
                if (s_['index'], r_) in relnames: continue
                si_, = struct.unpack_from('<I', b1, s_['relptr'] + 10 * r_ + 4)
                nm_, sec2, sc2 = symname.get(si_, ('', 0, 0))
                if sec2 > 0 and sec2 in rem and sc2 == 2 and not nm_.startswith(('C_', 'D_')):
                    a_ = sa.get(nm_)
                    if not (a_ and len(a_) == 1): newrev.add(sec2)
        newrev -= revive
        if not newrev or _it >= 8: break
        revive |= newrev
    # --- remaining undefined names -> addresses
    ren2 = {}
    for i, nm, value, sec, ty, sc, naux, o in coffrw.symbols(b2):
        if sc != 2 or sec != 0 or value != 0 or nm in ren2 or nm.startswith(('C_', 'D_')): continue
        if nm.startswith('__imp_') or nm in libnames: stat['kept (lib/import)'] += 1; continue
        a = sa.get(nm)
        if not a: stat['undefined, no address'] += 1; unresolved[nm] += 1; continue
        if len(a) > 1: stat['undefined, several addresses (per-site binding)'] += 1; multi[nm] += 1; continue
        va = a[0]; k = kind_of(va)
        if k is None: stat['undefined, address outside text/data'] += 1; unresolved[nm] += 1; continue
        ren2[nm] = '%s_%08x' % (k, va); stat['undefined -> ' + k] += 1
        (ctargets if k == 'C' else extra).add(va)
    nb, n2 = coffrw.rewrite(b2, ren2)
    (OUT / p.name).write_bytes(nb); stat['objects'] += 1
json.dump(sorted(extra), open(HERE / 'extra_labels.json', 'w')); json.dump(sorted(ctargets), open(HERE / 'code_targets.json', 'w'))
json.dump(dict(stat=dict(stat), unresolved_top=unresolved.most_common(300)), open(HERE / 'prep3_report.json', 'w'), indent=0)
print(dict(stat)); print('data labels', len(extra), 'code targets', len(ctargets))
