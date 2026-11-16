"""Compile every recipe unit into obj_v3/NNNN.obj, choosing the compiler per unit ('sp1' | 'rtm' | 'vc8').
Roots: sp1 = FNV_MSVC9_ROOT or FNV/tools/vc2008 ; rtm = FNV_MSVC9_RTM_ROOT ; vc8 = FNV_MSVC8_ROOT
(env, user env, machine env via registry, then the default Visual Studio 9.0 / 8 folders).
A root may be laid out as <root>/VC/bin + <root>/SDK or <root>/VC/PlatformSDK, or as a VS folder (<root>/VC/bin, <root>/VC/PlatformSDK).
Each compiler's cl.exe banner is checked against the expected version; a mismatch marks its units 'toolchain-wrong-version'.
Results: logs/compile_v3.jsonl, logs/compile_v3_summary.json, logs/compile_wall_v3.txt.  Usage: compile_units_v3.py [jobs]"""
import sys, os, json, subprocess, time, re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
HERE = Path(__file__).resolve().parent
FN = Path((__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\Projects\Decompilation') + r'\fnv_decomp'))
OBJ = HERE / 'obj_v3'
EXPECT = {'sp1': ('FNV_MSVC9_ROOT', '15.00.30729.01', [(__import__('os').environ.get('FNV_MSVC9_ROOT', r'C:\Projects\Decompilation\FNV\tools\vc2008'))]),
          'rtm': ('FNV_MSVC9_RTM_ROOT', '15.00.21022.08', [r'C:\Program Files (x86)\Microsoft Visual Studio 9.0']),
          'vc8': ('FNV_MSVC8_ROOT', '14.00.50727.762', [r'C:\Program Files (x86)\Microsoft Visual Studio 8'])}

def env_value(name):
    v = os.environ.get(name)
    if v: return v
    try:
        import winreg
        for hive, sub in ((winreg.HKEY_CURRENT_USER, 'Environment'),
                          (winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment')):
            try:
                with winreg.OpenKey(hive, sub) as k: return winreg.QueryValueEx(k, name)[0]
            except OSError: pass
    except ImportError: pass
    return None

def layout(root):
    root = Path(root)
    for vc in (root / 'VC', root):
        if (vc / 'bin' / 'cl.exe').exists():
            sdk = next((s for s in (root / 'SDK', vc / 'PlatformSDK', root / 'PlatformSDK') if (s / ('Include' if (s / 'Include').exists() else 'include')).exists()), None)
            return vc, sdk
    return None, None

def make_env(vc, sdk):
    def sub(p, *names):
        for n in names:
            if (p / n).exists(): return p / n
        return p / names[0]
    inc = [vc / 'include'] + ([sub(sdk, 'Include', 'include')] if sdk else [])
    lib = [vc / 'lib'] + ([sub(sdk, 'Lib', 'lib')] if sdk else [])
    e = os.environ.copy()
    e['INCLUDE'] = ';'.join(map(str, inc)); e['LIB'] = ';'.join(map(str, lib))
    e['PATH'] = str(vc / 'bin') + os.pathsep + e['PATH']
    e['TMP'] = e['TEMP'] = str(HERE / 'logs' / 'tmp')
    return e

def find_toolchains():
    out = {}
    for key, (var, want, defaults) in EXPECT.items():
        cands = ([env_value(var)] if env_value(var) else []) + defaults
        info = dict(want=want, var=var, tried=[str(c) for c in cands], root=None)
        for c in cands:
            vc, sdk = layout(c)
            if not vc: continue
            r = subprocess.run([str(vc / 'bin' / 'cl.exe')], capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL, env=make_env(vc, sdk))
            m = re.search(r'Version (\S+) for', r.stderr + r.stdout)
            info.update(root=str(c), vc=str(vc), sdk=str(sdk), version=m.group(1) if m else '?')
            info['ok'] = info['version'] == want
            if info['ok']: break
        out[key] = info
    return out

def one(arg):
    i, u, tc = arg
    obj = OBJ / f'{i:04d}.obj'
    t = time.time()
    info = tc[u['compiler']]
    base = dict(index=i, source=u['source'], compiler=u['compiler'])
    if not info.get('root'):
        return dict(base, status='toolchain-missing', error='compiler %s not found (%s)' % (u['compiler'], '; '.join(info['tried'])), seconds=0)
    if not info.get('ok'):
        return dict(base, status='toolchain-wrong-version', error='found %s, need %s' % (info.get('version'), info['want']), seconds=0)
    vc = Path(info['vc']); env = make_env(vc, Path(info['sdk']) if info['sdk'] != 'None' else None)
    try:
        r = subprocess.run([str(vc / 'bin' / 'cl.exe'), '/c', '/nologo'] + u['flags'] +
                           ['/I' + str(FN / 'include'), str(FN / u['source']), '/Fo' + str(obj)],
                           cwd=FN, env=env, capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL, timeout=900)
    except subprocess.TimeoutExpired:
        return dict(base, status='timeout', error='timeout 900s', seconds=time.time() - t)
    ok = r.returncode == 0 and obj.exists()
    return dict(base, status='ok' if ok else 'compile-failed', rc=r.returncode,
                error='' if ok else '\n'.join([l for l in (r.stdout + r.stderr).splitlines() if 'error' in l][:3] or [(r.stdout + r.stderr)[-300:]]),
                seconds=round(time.time() - t, 2))

if __name__ == '__main__':
    t0 = time.time()
    OBJ.mkdir(exist_ok=True); (HERE / 'logs' / 'tmp').mkdir(parents=True, exist_ok=True)
    tc = find_toolchains()
    units = json.loads((FN / 'build/units.json').read_text())['units']
    jobs = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    results = []
    with ThreadPoolExecutor(jobs) as pool:
        for res in pool.map(one, [(i, u, tc) for i, u in enumerate(units)]):
            results.append(res)
    with open(HERE / 'logs' / 'compile_v3.jsonl', 'w') as f:
        for r in results: f.write(json.dumps(r) + '\n')
    summ = {}
    for r in results:
        s = summ.setdefault(r['compiler'], {})
        s[r['status']] = s.get(r['status'], 0) + 1
    (HERE / 'logs' / 'compile_v3_summary.json').write_text(json.dumps(dict(toolchains=tc, by_compiler=summ), indent=1))
    (HERE / 'logs' / 'compile_wall_v3.txt').write_text(str(time.time() - t0))
    print(json.dumps(summ), round(time.time() - t0), 's')
