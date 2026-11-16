"""Run /d1reportAllClassLayout for given units; write logs/layouts_v3.json {unit: {classname: [sizes]}}"""
import sys, json, re, subprocess, tempfile, shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
import compile_units_v3 as C
units = json.loads((C.FN / 'build/units.json').read_text())['units']; tc = C.find_toolchains()
tmp = Path(tempfile.mkdtemp(dir=str(HERE / 'logs' / 'tmp')))
def run(i):
    u = units[i]; vc = Path(tc[u['compiler']]['vc']); env = C.make_env(vc, Path(tc[u['compiler']]['sdk']))
    r = subprocess.run([str(vc / 'bin/cl.exe'), '/c', '/nologo', '/d1reportAllClassLayout'] + u['flags'] + ['/I' + str(C.FN / 'include'), str(C.FN / u['source']), '/Fo' + str(tmp / ('%d.obj' % i))],
                       cwd=C.FN, env=env, capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL)
    out = {}
    for m in re.finditer(r'^(?:class|struct|union)\s+(\S+)\s+size\((\d+)\)', r.stdout, re.M):
        out.setdefault(m.group(1), []).append(int(m.group(2)))
    return i, out
try:
    with ThreadPoolExecutor(8) as p: res = dict(p.map(run, [int(x) for x in sys.argv[1:]]))
finally: shutil.rmtree(tmp, ignore_errors=True)
json.dump(res, open(HERE / 'logs' / 'layouts_v3.json', 'w'))
print({k: len(v) for k, v in res.items()})
