"""link-v2 eh_pieces.py: per unit, the located EH pieces (funclets/handlers in .text$x sections): section index -> [(start offset, end offset, original address)], as data-v1's phase0 computes them."""
import sys, os, json, collections
sys.dont_write_bytecode = True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\data-v1')
import phase0 as P
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
A = P.A; Coff = P.Coff; compare = P.compare; PB = P.PB
def work(task):
    idx, unit = task; pe = A.G['pe']
    try: coff = Coff(PB / 'obj_v3' / ('%04d.obj' % idx))
    except Exception: return idx, {}
    unit['_fnmap'] = {}
    for f in unit['functions']:
        for nm in [f['symbol']] + f.get('fold_aliases', []): unit['_fnmap'][nm] = int(f['address'], 16)
    try:
        rows = compare(coff, pe, dict(symbols=unit.get('symbols', {}), functions=unit['functions'], literal_symbols=unit.get('literal_symbols', [])), None)
        pcs, inferred, errors, dbases, anchors = A.G['eh'](coff, pe, unit, rows, A.G['sym'])
    except Exception: return idx, {}
    out = collections.defaultdict(list)
    for p in pcs:
        if len(p) >= 8: out[p[6]].append((p[7], p[7] + len(p[5]), p[0]))
    return idx, dict(out)
def main():
    import build_and_match as BAM
    units = json.loads((A.FN / 'build/units.json').read_text())['units']
    pe = A.Pe(A.IMG); seen = collections.defaultdict(set)
    for u in units:
        for f in u['functions']:
            for n in [f['symbol']] + f.get('fold_aliases', []): seen[n].add(int(f['address'], 16))
    fnnames = {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}
    imports, thunks = A.parse_imports(pe)
    tasks = [(i, u) for i, u in enumerate(units) if i < 2988]
    res = {}
    with ProcessPoolExecutor(8, initializer=P.init, initargs=(fnnames, BAM.recipe_names(units), imports, thunks)) as ex:
        for i, d in ex.map(work, tasks, chunksize=8): res[str(i)] = {str(k): v for k, v in d.items()}
    json.dump(res, open(Path(__file__).resolve().parent / 'eh_pieces.json', 'w'), separators=(',', ':'))
    print('units with pieces', sum(1 for v in res.values() if v), 'pieces', sum(len(x) for v in res.values() for x in v.values()))
if __name__ == '__main__': main()
