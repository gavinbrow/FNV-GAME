"""phase0: per-unit worker. For every data-like COMDAT/section of each compiled unit: address hints (from the build's symbol maps)
and every relocation resolved with the same resolver as build-v7 (assemble_v3.resolve_field + ICF map). Writes scratch pickle."""
import sys, os, json, struct, collections, pickle, re
sys.dont_write_bytecode = True
sys.path.append((__import__('os').environ.get('FNV_PY_SITE', r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')))
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
RN = Path((__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\Projects\Decompilation') + r'\runtime-next'))
PB = RN / 'pinned-build'; CV = RN / 'coverage-v3'; V7 = RN / 'build-v7'
sys.path.insert(0, str(PB)); sys.path.insert(0, str(CV))
import assemble_v3 as A
from compare import Coff, compare
M32 = 0xffffffff
ICF = {}
def init(fnnames, symnames, imports, thunks):
    A.init(fnnames, symnames, imports, thunks)
    ICF.update(json.loads((V7 / 'icf_map.json').read_text()))
def isdata(s):
    n = s['name']
    return not (s['flags'] & 0x20) and n.startswith(('.rdata', '.data', '.xdata', '.CRT', '.tls', '.bss', 'CONST'))
def work(task):
    idx, unit = task
    pe = A.G['pe']; out = dict(idx=idx, secs=[], err=None)
    try: coff = Coff(PB / 'obj_v3' / ('%04d.obj' % idx))
    except Exception as e: out['err'] = 'coff:' + str(e)[:100]; return out
    unit['_fnmap'] = {}; locals_ = []
    for f in unit['functions']:
        a = int(f['address'], 16)
        for nm in [f['symbol']] + f.get('fold_aliases', []):
            unit['_fnmap'][nm] = a
            try: s = coff.named(nm); locals_.append((s['section'], s['value'], a, f['size']))
            except ValueError: pass
    # EH pieces (funclets) and xdata anchors, as build-v7 pass 1 does
    pieces = []; dbases = {}
    try:
        rows = compare(coff, pe, dict(symbols=unit.get('symbols', {}), functions=unit['functions'], literal_symbols=unit.get('literal_symbols', [])), None)
        pcs, inferred, errors, dbases, anchors = A.G['eh'](coff, pe, unit, rows, A.G['sym'])
        pieces = [p for p in pcs if len(p) >= 8]
    except Exception as e:
        out['eh_err'] = str(e)[:100]
    psec = collections.defaultdict(list)
    for p in pieces: psec[p[6]].append((p[7], p[7] + len(p[5]), p[0], p[2]))   # (s0, s1, at, ok)
    defs = collections.defaultdict(list)
    for si, s in coff.symbols.items():
        if s['section'] > 0: defs[s['section']].append(s)
    symu = unit.get('symbols', {})
    for k, s in enumerate(coff.sections):
        if not s or not isdata(s): continue
        isbss = bool(s['flags'] & 0x80)
        hints = []
        for d in defs.get(k, []):
            nm = d['name']
            if nm.startswith('.') : continue
            a = None; via = None
            if nm in symu: a = int(symu[nm], 0); via = 'unit-map'
            elif nm in A.G['sym']: a = A.G['sym'][nm]; via = 'global-map'
            elif not nm.startswith(A.NOADDR_PREFIX) and not nm.startswith(('??', '$', '__')):
                m = A.ADDR_RE.search(nm)
                if m and 0x400000 <= int(m.group(1), 16) < 0x1500000 and not re.search(r'\$\d?\?$', nm[:m.start()]): a = int(m.group(1), 16); via = 'name-embedded'
            if a is not None: hints.append(((a - d['value']) & M32, via, nm))
        if k in dbases: hints.append((dbases[k], 'eh-anchor', ''))
        rl = []
        if not isbss:
            for off, ri, kind in s['relocs']:
                t = coff.symbols[ri]; rec = [off, kind, t['name'], t['section'], t['value'], t['storage'], None, None, None]
                if kind in (6, 7, 0x0B) and off + 4 <= len(s['data']):
                    addend, = struct.unpack_from('<I', s['data'], off); rec[6] = addend
                    # funclet / EH tail pieces (text$x sections of this object)
                    src = exp = None
                    if t['section'] > 0 and coff.sections[t['section']]['name'].startswith('.text$x'):
                        pt = t['value'] + addend
                        for s0, s1, at, ok in psec.get(t['section'], ()):
                            if s0 <= pt < s1: src, exp = 'eh-piece', (at + pt - s0) & M32; break
                    if src is None:
                        try: src, exp = A.resolve_field(coff, unit, locals_, kind, t, addend, 0, b'\0\0\0\0')
                        except Exception: src, exp = None, None
                    if src is None and t['name'] in ICF and (t['section'] <= 0 or t['type'] & 0x20): src, exp = 'icf-fold', (ICF[t['name']] + addend) & M32
                    if src is None and t['name'] == '___ImageBase': src, exp = 'linker-imagebase', (pe.base + addend) & M32
                    rec[7], rec[8] = src, exp
                rl.append(tuple(rec))
        defl = [(d['name'], d['value'], d['storage']) for d in defs.get(k, []) if not d['name'].startswith('.')]
        out['secs'].append(dict(u=idx, k=k, name=s['name'], flags=s['flags'], data=(b'' if isbss else s['data']), size=len(s['data']), relocs=rl, defs=defl, hints=hints))
    return out
def main():
    import build_and_match as BAM
    units = json.loads((A.FN / 'build/units.json').read_text())['units']
    comp = {}
    for line in (PB / 'logs' / 'compile_v3.jsonl').read_text().splitlines():
        r = json.loads(line); comp[r['index']] = r
    pe = A.Pe(A.IMG)
    seen = collections.defaultdict(set)
    for u in units:
        for f in u['functions']:
            for n in [f['symbol']] + f.get('fold_aliases', []): seen[n].add(int(f['address'], 16))
    fnnames = {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}
    symnames = BAM.recipe_names(units)
    imports, thunks = A.parse_imports(pe)
    tasks = [(i, u) for i, u in enumerate(units) if comp[i]['status'] == 'ok']
    res = {}
    with ProcessPoolExecutor(8, initializer=init, initargs=(fnnames, symnames, imports, thunks)) as ex:
        for r in ex.map(work, tasks, chunksize=8): res[r['idx']] = r
    notok = [i for i in range(len(units)) if comp[i]['status'] != 'ok']
    pickle.dump(dict(res=res, notok=notok), open(sys.argv[1], 'wb'))
    print('units', len(res), 'notok', len(notok), 'secs', sum(len(r['secs']) for r in res.values()))
if __name__ == '__main__': main()
