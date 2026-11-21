"""Compile every recipe unit fresh into obj/NNNN.obj (NNNN = unit index in units.json). Results in logs/compile.jsonl"""
import sys, os, json, subprocess, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
HERE = Path(__file__).resolve().parent
FN = Path(r'C:\path\to\Decompilation\fnv_decomp')
VC = Path(r'C:\path\to\Decompilation\FNV\tools\vc2008\VC')   # only toolchain present: VC2008 SP1 15.00.30729.01
ENV = os.environ.copy()
ENV['INCLUDE'] = f'{VC}\include;{VC}\PlatformSDK\include'
ENV['LIB'] = f'{VC}\lib;{VC}\PlatformSDK\lib'
ENV['PATH'] = str(VC / 'bin') + os.pathsep + ENV['PATH']
ENV['TMP'] = ENV['TEMP'] = str(HERE / 'logs' / 'tmp')
(HERE / 'logs' / 'tmp').mkdir(parents=True, exist_ok=True)

def one(arg):
    i, u = arg
    obj = HERE / 'obj' / f'{i:04d}.obj'
    t = time.time()
    if u['compiler'] != 'sp1':
        return dict(index=i, source=u['source'], compiler=u['compiler'], status='toolchain-missing',
                    error='compiler %s not installed (only sp1 15.00.30729.01 found)' % u['compiler'], seconds=0)
    try:
        r = subprocess.run([str(VC / 'bin' / 'cl.exe'), '/c', '/nologo'] + u['flags'] +
                           ['/I' + str(FN / 'include'), str(FN / u['source']), '/Fo' + str(obj)],
                           cwd=FN, env=ENV, capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL, timeout=900)
    except subprocess.TimeoutExpired:
        return dict(index=i, source=u['source'], compiler=u['compiler'], status='timeout', error='timeout 900s', seconds=time.time()-t)
    ok = r.returncode == 0 and obj.exists()
    return dict(index=i, source=u['source'], compiler=u['compiler'], status='ok' if ok else 'compile-failed',
                rc=r.returncode, error='' if ok else (r.stdout + r.stderr)[-600:], seconds=round(time.time() - t, 2))

if __name__ == '__main__':
    t0 = time.time()
    units = json.loads((FN / 'build/units.json').read_text())['units']
    jobs = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    out = open(HERE / 'logs' / 'compile.jsonl', 'w')
    n = 0
    with ThreadPoolExecutor(jobs) as pool:
        for res in pool.map(one, list(enumerate(units))):
            out.write(json.dumps(res) + '\n'); n += 1
            if n % 200 == 0:
                out.flush(); print(n, 'of', len(units), round(time.time() - t0), 's', flush=True)
    out.close()
    (HERE / 'logs' / 'compile_wall.txt').write_text(str(time.time() - t0))
    print('done', time.time() - t0)
