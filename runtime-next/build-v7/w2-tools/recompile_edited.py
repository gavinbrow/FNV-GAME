"""Recompile the units edited by worker 2 into pinned-build\obj_v3 (what assemble_v7 reads). Run with FNV_MSVC9_RTM_ROOT set, before rebuild.cmd's assemble steps
(rebuild.cmd itself does not compile). usage: python -I recompile_edited.py"""
import sys, json
from pathlib import Path
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\pinned-build')
import compile_units_v3 as CU
tc = CU.find_toolchains()
units = json.loads((CU.FN / 'build/units.json').read_text())['units']
ids = [int(x) for x in (Path(__file__).parent / 'edited_units.txt').read_text().split()]
for i in ids:
    r = CU.one((i, units[i], tc)); print(i, r['status'], r['error'][:100])

# EH-only variant objects (build-v7\ehvariants_w2.json): compile each variant source with its unit's flags into build-v7\ehvar\<unit>.obj
import subprocess
for e in json.loads(Path(r'C:\Projects\Decompilationuntime-nextuild-v7\ehvariants_w2.json').read_text()):
    u = dict(units[e['unit']], source=e['source']); old = CU.OBJ; CU.OBJ = Path(r'C:\Projects\Decompilationuntime-nextuild-v7\ehvar')
    (CU.OBJ).mkdir(exist_ok=True); r = CU.one((e['unit'], u, tc)); CU.OBJ = old
    print('variant', e['unit'], r['status']); 
