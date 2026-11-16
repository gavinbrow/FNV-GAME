"""link-v2: compile every accepted contribution (queue state) like the checker does into link-v2\obj_contrib\<addr>.obj. usage: python -I compile_contribs.py [jobs]"""
import sys, os, json, subprocess, shutil, tempfile, hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.dont_write_bytecode = True
sys.path.insert(0, r'C:\Projects\Decompilation\FNV\scripts')
import local_targets as LT
HERE = Path(__file__).resolve().parent; OBJ = HERE / 'obj_contrib'; OBJ.mkdir(exist_ok=True)
state = json.loads(LT.STATE.read_text(encoding='utf-8')); acc = state['accepted']
cat = {t['address']: t for t in LT.catalog().values()}
def one(addr):
    a = acc[addr]; t = cat[addr]
    comp = a.get('compiler') or t['compiler']
    flags = list(a['flags']) if a.get('flags') else (t['flags'] if comp == t['compiler'] else LT._flags_for(comp, t))
    src = LT.CONTRIB / ('FUN_%s.cpp' % addr[2:])
    raw = src.read_bytes()
    raw = raw.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
    w = Path(tempfile.mkdtemp(prefix='lc_'))
    try:
        cl, env = LT._env_for(comp); env = dict(env); env['TMP'] = env['TEMP'] = str(w)
        sp = w / 'a.cpp'; sp.write_bytes(raw); op = OBJ / (addr[2:] + '.obj')
        r = subprocess.run([str(cl), '/c', '/nologo'] + flags + ['/I' + str(LT.FN / 'include'), str(sp), '/Fo' + str(op)], cwd=str(LT.FN), env=env, capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL, timeout=300)
        return addr, r.returncode == 0 and op.exists(), (r.stdout + r.stderr)[-200:], comp, flags
    finally: shutil.rmtree(w, ignore_errors=True)
res = {}
with ThreadPoolExecutor(int(sys.argv[1]) if len(sys.argv) > 1 else 12) as ex:
    for addr, ok, err, comp, flags in ex.map(one, sorted(acc)): res[addr] = dict(ok=ok, err=err if not ok else '', compiler=comp, flags=flags)
json.dump(res, open(HERE / 'contrib_compile.json', 'w'))
print('ok', sum(1 for r in res.values() if r['ok']), 'of', len(res))
