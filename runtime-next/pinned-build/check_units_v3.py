"""Compile selected units (to a temp dir) with the per-unit compiler and report matched functions / ok EH tail pieces.
usage: check_units_v3.py <out.json> idx [idx...]      (or: check_units_v3.py --diff base.json new.json)"""
import sys, os, json, subprocess, tempfile, shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.dont_write_bytecode = True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import compile_units_v3 as C
FN = C.FN
sys.path.insert(0, str(FN / 'tools'))
from compare import Coff, Pe, compare
import build_and_match as BAM
IMG = Path(r'C:\Projects\Decompilation\FNV\work\worker1\FalloutNV.runtime-text.exe')

def check(idx, units, pe, names, tc, scratch):
    u = units[idx]; info = tc[u['compiler']]
    vc = Path(info['vc']); env = C.make_env(vc, Path(info['sdk']))
    obj = Path(scratch) / ('%04d.obj' % idx)
    r = subprocess.run([str(vc / 'bin/cl.exe'), '/c', '/nologo'] + u['flags'] + ['/I' + str(FN / 'include'), str(FN / u['source']), '/Fo' + str(obj)],
                       cwd=FN, env=env, capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL)
    if r.returncode or not obj.exists():
        return idx, dict(status='compile-failed', error='\n'.join(l for l in (r.stdout + r.stderr).splitlines() if 'error' in l)[:600])
    coff = Coff(obj)
    rows = compare(coff, pe, dict(symbols=u.get('symbols', {}), functions=u['functions'], literal_symbols=u.get('literal_symbols', [])), None)
    res = dict(status='ok', matched=sorted(x['address'] for x in rows if x['verdict'] == 'match'),
               total=len(rows), tails_ok=[], tails_bad=[])
    if u.get('eh_tails'):
        try:
            secs, inferred, errs = BAM.eh_sections(coff, pe, u, rows, names)
            for s in secs: (res['tails_ok'] if s[2] else res['tails_bad']).append(s[0])
            res['errors'] = errs[:3]
        except Exception as e:
            res['errors'] = [str(e)[:200]]
    return idx, res

if __name__ == '__main__':
    if sys.argv[1] == '--diff':
        a, b = json.load(open(sys.argv[2])), json.load(open(sys.argv[3]))
        for k in b:
            if a.get(k, {}).get('status') != 'ok' and b[k]['status'] != 'ok':
                print(k, 'FAILED', b[k].get('error')); continue
            if b[k]['status'] != 'ok': print(k, 'COMPILE FAIL', b[k]['error']); continue
            lost = set(a[k]['matched']) - set(b[k]['matched']); gain = set(b[k]['matched']) - set(a[k]['matched'])
            tl = set(a[k]['tails_ok']) - set(b[k]['tails_ok']); tg = set(b[k]['tails_ok']) - set(a[k]['tails_ok'])
            print(k, 'fn match %d->%d tails_ok %d->%d' % (len(a[k]['matched']), len(b[k]['matched']), len(a[k]['tails_ok']), len(b[k]['tails_ok'])),
                  'LOST fn %s' % sorted(lost) if lost else '', 'LOST tails %s' % [hex(x) for x in sorted(tl)] if tl else '', 'gained tails %d' % len(tg))
        sys.exit()
    units = json.loads((FN / 'build/units.json').read_text())['units']
    tc = C.find_toolchains(); names = BAM.recipe_names(units); pe = Pe(IMG)
    scratch = tempfile.mkdtemp(prefix='chk_', dir=str(HERE / 'logs' / 'tmp'))
    try:
        with ThreadPoolExecutor(12) as p:
            out = dict(p.map(lambda i: check(i, units, pe, names, tc, scratch), [int(x) for x in sys.argv[2:]]))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    json.dump({str(k): v for k, v in out.items()}, open(sys.argv[1], 'w'))
    for k, v in out.items():
        print(k, v['status'], len(v.get('matched', [])), '/', v.get('total'), 'tails ok', len(v.get('tails_ok', [])), 'bad', len(v.get('tails_bad', [])), v.get('error', ''))
