"""Recompute the compiler-placed ranges exactly as pinned-build/assemble.py does (read-only use of its helpers).
Writes only overlay-test/placed.json (address/size lists, no code)."""
import sys, os, json, collections
sys.dont_write_bytecode = True
PB = r'C:\Projects\Decompilation\runtime-next\pinned-build'
sys.path.insert(0, PB)
import assemble as A
from concurrent.futures import ProcessPoolExecutor

def main():
    units = json.loads((A.FN / 'build/units.json').read_text())['units']
    comp = {}
    for line in (A.HERE / 'logs' / 'compile.jsonl').read_text().splitlines():
        r = json.loads(line); comp[r['index']] = r
    pe = A.Pe(A.IMG)
    seen = collections.defaultdict(set)
    for u in units:
        for f in u['functions']:
            for n in [f['symbol']] + f.get('fold_aliases', []):
                seen[n].add(int(f['address'], 16))
    fnnames = {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}
    symnames = A.BAM.recipe_names(units)
    imports, thunks = A.parse_imports(pe)
    tasks = [(i, u) for i, u in enumerate(units) if comp[i]['status'] == 'ok']
    results = {}
    with ProcessPoolExecutor(28, initializer=A.init, initargs=(fnnames, symnames, imports, thunks)) as ex:
        for n, r in enumerate(ex.map(A.process, tasks, chunksize=8), 1):
            results[r['idx']] = r
    N = len(pe.data)
    cover = bytearray(N); written = bytearray(N)
    flist = [(int(f['address'], 16), f['size']) for u in units for f in u['functions']]
    tlist = [(int(t['address'], 16), t['size']) for u in units for t in u.get('eh_tails', [])]
    for a, s in flist:
        o = A.va2off(pe, a, s); cover[o:o + s] = b'\x01' * s
    for a, s in tlist:
        o = A.va2off(pe, a, s)
        for k in range(o, o + s):
            if cover[k] == 0: cover[k] = 2
    pf = pb = 0; ranges = []
    for i, u in enumerate(units):
        if comp[i]['status'] != 'ok' or results[i]['error']: continue
        for rec in results[i]['fn']:
            if rec['data'] is None: continue
            o = A.va2off(pe, rec['address'], rec['size'])
            if any(written[o:o + rec['size']]): continue
            written[o:o + rec['size']] = b'\x01' * rec['size']
            pf += 1; pb += rec['size']; ranges.append((rec['address'], rec['size']))
    tp = tb = 0; tranges = []
    for i, r in results.items():
        for t in r['tails']:
            if t['data'] is None: continue
            L = len(t['data']); o = A.va2off(pe, t['address'], max(1, L))
            if o is None: continue
            mask = [cover[o + k] == 2 and written[o + k] == 0 for k in range(L)]
            if not any(mask): continue
            tp += 1
            for k in range(L):
                if mask[k]: written[o + k] = 2
            k = 0
            while k < L:
                if mask[k]:
                    j = k
                    while j < L and mask[j]: j += 1
                    tranges.append((t['address'] + k, j - k)); tb += j - k; k = j
                else: k += 1
    json.dump(dict(functions_placed=pf, function_bytes=pb, tail_pieces=tp, tail_bytes=tb,
                   ranges=sorted(ranges + tranges)), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'placed.json'), 'w'))
    print('functions', pf, pb, 'tails', tp, tb)

if __name__ == '__main__':
    main()
