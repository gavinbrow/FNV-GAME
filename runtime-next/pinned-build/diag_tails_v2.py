"""Diagnostics for EH tail pieces: mismatching pieces and operator-delete oddities.  Read-only; prints/writes logs/diag_tails_v2.json"""
import sys, os, json, struct, inspect, collections
sys.dont_write_bytecode = True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import assemble_v2 as A
from concurrent.futures import ProcessPoolExecutor
BAM, Coff, Pe, compare = A.BAM, A.Coff, A.Pe, A.compare
G = {}

def init(fnnames, symnames, imports, thunks):
    A.init(fnnames, symnames, imports, thunks)
    src = inspect.getsource(BAM.eh_sections)
    old = 'out.append([at, at + s1 - s0, ok, parent, sorted(guessed)])'
    new = 'out.append([at, at + s1 - s0, ok, parent, sorted(guessed), bytes(data[s0:s1]), index, s0, (s0 in where), base, sorted(mask), len(pieces), sorted(where.items())[:0]])'
    src = src.replace(old, new)
    ns = dict(BAM.__dict__); exec(src, ns); G['eh'] = ns['eh_sections']

def work(task):
    idx, unit = task
    pe = A.G['pe']
    res = []
    coff = Coff(HERE / 'obj' / ('%04d.obj' % idx))
    rows = compare(coff, pe, dict(symbols=unit.get('symbols', {}), functions=unit['functions'],
                                  literal_symbols=unit.get('literal_symbols', [])), None)
    pieces, inferred, errors = G['eh'](coff, pe, unit, rows, A.G['sym'])
    for p in pieces:
        if len(p) < 8: continue
        at, end, ok, parent, guessed, pdata, index, s0, fromwhere, base, mask, npieces, _ = p
        try: orig = pe.read(at, len(pdata))
        except ValueError: orig = None
        diffs = [] if orig is None else [i for i in range(len(pdata)) if i not in set(mask) and pdata[i] != orig[i]]
        rel_info = []
        sec = coff.sections[index]
        for off, ti, kind in sec['relocs']:
            if not s0 <= off < s0 + len(pdata): continue
            t = coff.symbols[ti]
            r = off - s0
            if orig is None: continue
            if kind == 0x14:
                obs = (at + r + 4 + struct.unpack_from('<i', orig, r)[0]) & 0xffffffff
            else:
                obs = struct.unpack_from('<I', orig, r)[0]
            rel_info.append((r, kind, t['name'][:60], obs, orig[max(0, r - 1):r + 5].hex()))
        res.append(dict(unit=idx, at=at, size=len(pdata), ok=ok, parent=parent, sec=index, s0=s0, fromwhere=fromwhere,
                        base=base, npieces=npieces, diffs=diffs, orig=None if orig is None else orig.hex(),
                        mine=pdata.hex(), mask=mask, rels=rel_info if (not ok or diffs or any('??3' in x[2] for x in rel_info)) else None))
    return res

if __name__ == '__main__':
    units = json.loads((A.FN / 'build/units.json').read_text())['units']
    comp = {}
    for line in (HERE / 'logs' / 'compile.jsonl').read_text().splitlines():
        r = json.loads(line); comp[r['index']] = r
    pe = Pe(A.IMG)
    seen = collections.defaultdict(set)
    for u in units:
        for f in u['functions']:
            for n in [f['symbol']] + f.get('fold_aliases', []): seen[n].add(int(f['address'], 16))
    fnnames = {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}
    symnames = BAM.recipe_names(units)
    imports, thunks = A.parse_imports(pe)
    tasks = [(i, u) for i, u in enumerate(units) if comp[i]['status'] == 'ok' and u.get('eh_tails')]
    allp = []
    with ProcessPoolExecutor(28, initializer=init, initargs=(fnnames, symnames, imports, thunks)) as ex:
        for r in ex.map(work, tasks, chunksize=4): allp += r
    (HERE / 'logs' / 'diag_tails_v2.json').write_text(json.dumps(allp))
    print('units', len(tasks), 'pieces', len(allp), 'not ok', sum(1 for p in allp if not p['ok']),
          'with diffs', sum(1 for p in allp if p['diffs']), 'fromwhere', sum(p['fromwhere'] for p in allp))
