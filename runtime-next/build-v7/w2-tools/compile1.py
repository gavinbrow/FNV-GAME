"""w2: compile single units into w2/obj_v3 (NOT the shared pinned-build/obj_v3). usage: compile1.py idx..."""
import sys, json
sys.dont_write_bytecode = True
from pathlib import Path
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\pinned-build')
import compile_units_v3 as CU
CU.OBJ = Path(__file__).resolve().parent / 'obj_v3'
tc = CU.find_toolchains()
units = json.loads((CU.FN / 'build/units.json').read_text())['units']
SRC = {}
def go(i):
    u = dict(units[i])
    if i in SRC: u['source'] = SRC[i]
    r = CU.one((i, u, tc)); return r
if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    ids = []
    for x in sys.argv[1:]:
        if ':' in x: a, b = x.split(':', 1); SRC[int(a)] = b; ids.append(int(a))
        else: ids.append(int(x))
    with ThreadPoolExecutor(6) as ex:
        for r in ex.map(go, ids): print(r['index'], r['status'], r['seconds'], r['error'][:300])
