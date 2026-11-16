"""Recompile the given unit indices (or --file list.json) into pinned-build\obj_v3 (backup: obj_v3.bak-20261116). Needs FNV_MSVC9_RTM_ROOT.
usage: python -I recompile_units.py 12 34 ... | --file edited_units_consts.json"""
import sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\pinned-build')
import compile_units_v3 as CU
tc = CU.find_toolchains()
units = json.loads((CU.FN / 'build/units.json').read_text())['units']
ids = json.load(open(sys.argv[2])) if sys.argv[1] == '--file' else [int(x) for x in sys.argv[1:]]
from concurrent.futures import ThreadPoolExecutor
def go(i): return CU.one((i, units[i], tc))
with ThreadPoolExecutor(6) as ex:
    for r in ex.map(go, ids): print(r['index'], r['status'], r.get('seconds'), r['error'][:200])
