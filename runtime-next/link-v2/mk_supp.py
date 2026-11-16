"""link-v2 mk_supp.py: compile supp\supp.cpp (real forwarders) and assemble supp\supp_data.asm; names with an embedded address become C_/D_<va>. -> supp_obj\*.obj (linked by mk_rsp)
usage: python -I mk_supp.py"""
import os, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
import coffrw
VC = 'C:/Projects/Decompilation/FNV/tools/vc2008/VC'; out = HERE / 'supp_obj'; out.mkdir(exist_ok=True)
env = dict(os.environ); env['PATH'] = VC + '/bin;' + 'C:/Projects/Decompilation/FNV/tools/vc2008/Common7/IDE;' + env['PATH']; env['INCLUDE'] = VC + '/include'; env['LIB'] = VC + '/lib'
r = subprocess.run([VC + '/bin/cl.exe', '/c', '/nologo', '/MT', '/O2', '/GS-', '/Fo' + str(out / 'supp_raw.obj'), str(HERE / 'supp' / 'supp.cpp')], env=env, capture_output=True, text=True); print(r.stdout[-300:], r.stderr[-300:])
b = (out / 'supp_raw.obj').read_bytes(); ren = {}
import re
for i, nm, v, sec, ty, sc, na, o in coffrw.symbols(b):
    m = re.search(r'FUN_([0-9a-f]{8})', nm)
    if sec == 0 and m: ren[nm] = 'C_' + m.group(1)
nb, n = coffrw.rewrite(b, ren); (out / 'supp.obj').write_bytes(nb); (out / 'supp_raw.obj').unlink()
r = subprocess.run([VC + '/bin/ml.exe', '/c', '/coff', '/nologo', '/Cp', '/Fo' + str(out / 'supp_data.obj'), str(HERE / 'supp' / 'supp_data.asm')], env=env, capture_output=True, text=True); print(r.stdout[-300:], r.stderr[-200:])
import json
names = [nm for f in ('supp.obj', 'supp_data.obj') for i, nm, v, sec, ty, sc, na, o in coffrw.symbols((out / f).read_bytes()) if sc == 2 and (sec > 0 or sec == -1)]
json.dump(names, open(HERE / 'supp_names.json', 'w')); print(len(names), 'supplement symbols')
