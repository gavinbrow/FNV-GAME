"""Locate EH pieces for ALL compiled units (not only those with recipe eh_tails). Writes logs/pieces_all_v2.json [at,size,ok,parent,unit,in_recipe_unit]"""
import sys, json, collections
sys.dont_write_bytecode = True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import diag_tails_v2 as D
from concurrent.futures import ProcessPoolExecutor
A = D.A

def work(task):
    try:
        r = D.work(task)
    except Exception as e:
        return [('ERR', task[0], str(e)[:100])]
    return [(p['at'], p['size'], p['ok'], p['parent'], p['unit'], bool(task[1].get('eh_tails'))) for p in r]

if __name__ == '__main__':
    units = json.loads((A.FN / 'build/units.json').read_text())['units']
    comp = {}
    for line in (HERE / 'logs' / 'compile.jsonl').read_text().splitlines():
        r = json.loads(line); comp[r['index']] = r
    pe = A.Pe(A.IMG)
    seen = collections.defaultdict(set)
    for u in units:
        for f in u['functions']:
            for n in [f['symbol']] + f.get('fold_aliases', []): seen[n].add(int(f['address'], 16))
    fnnames = {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}
    symnames = A.BAM.recipe_names(units)
    imports, thunks = A.parse_imports(pe)
    tasks = [(i, u) for i, u in enumerate(units) if comp[i]['status'] == 'ok']
    out = []
    with ProcessPoolExecutor(28, initializer=D.init, initargs=(fnnames, symnames, imports, thunks)) as ex:
        for r in ex.map(work, tasks, chunksize=4): out += r
    errs = [x for x in out if x[0] == 'ERR']
    out = [x for x in out if x[0] != 'ERR']
    (HERE / 'logs' / 'pieces_all_v2.json').write_text(json.dumps(out))
    print('pieces', len(out), 'errors', len(errs), errs[:3])
