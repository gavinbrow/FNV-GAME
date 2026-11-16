r"""One-command build of the self-compiled FalloutNV exe (driver for build-all.cmd).

  python build_all.py --out DIR [--layout G] [--no-harness] [--require-harness] [--skip-data-v1] [--keep-lock]

Steps (each logged to <out>\logs\NN-name.log, stop at the first failure):
  0 preflight   inputs present (game dir read-only, reference image read-only, toolchains) + build.lock
  1 compile     pinned-build\compile_units_v3.py   (all recipe units -> pinned-build\obj_v3; ~30 s)
  2 build-v7    build-v7\rebuild.cmd               (assemble, ICF, own .reloc; ~3-5 min)
  3 data-v1     data-v1\rebuild.cmd + data-v3\dump_pieces.py   (place our data pieces; 10-20 min)
  4 data-v3     data-v3\rebuild.cmd                (symbolic data objects, round trip proof)
  5 snapshot    layout-v2\snapshot.py              (freeze the inputs of the image maker)
  6 image       layout-v2\make_image.py --layout G (self-assembled exe)  -> <out>\FalloutNV_selfbuilt.exe
  7 harness     direct-v1\harness.py --extended    (launch, load a save, play, cell change, quicksave/load, exit)  [non-fatal unless --require-harness]
Writes <out>\build-summary.json and <out>\build-summary.txt (release notes). Never writes inside the game folder; the reference image is read only.
Environment (defaults = today's local paths): FNV_PROJ_ROOT FNV_GAME_DIR FNV_MSVC9_RTM_ROOT FNV_MSVC9_ROOT FNV_REF_IMAGE FNV_PY_SITE."""
import os, sys, json, time, subprocess, argparse, hashlib, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import paths, buildlock
J = os.path.join
ap = argparse.ArgumentParser()
ap.add_argument('--out', required=True); ap.add_argument('--layout', default='G')
ap.add_argument('--no-harness', action='store_true'); ap.add_argument('--require-harness', action='store_true')
ap.add_argument('--skip-data-v1', action='store_true'); ap.add_argument('--play', type=int, default=60)
ap.add_argument('--keep-lock', action='store_true'); ap.add_argument('--lock-wait', type=int, default=7200)
a = ap.parse_args()
OUT = os.path.abspath(a.out); LOGS = J(OUT, 'logs'); os.makedirs(LOGS, exist_ok=True)
RN = paths.RN
PY = sys.executable
env = dict(os.environ)
env.update(FNV_PROJ_ROOT=paths.PROJ, FNV_GAME_DIR=paths.GAME_DIR, FNV_MSVC9_RTM_ROOT=paths.MSVC9_RTM, FNV_MSVC9_ROOT=paths.MSVC9_SP1, FNV_MSVC8_ROOT=paths.MSVC8, FNV_REF_IMAGE=paths.REF_IMAGE)
env.setdefault('PYTHONDONTWRITEBYTECODE', '1')
if os.path.isdir(paths.PY_SITE): env['PYTHONPATH'] = paths.PY_SITE + os.pathsep + env.get('PYTHONPATH', '')   # numpy/capstone/pefile for the steps that do not run with -I
TMPD = J(paths.PROJ, '.build-tmp'); os.makedirs(TMPD, exist_ok=True)   # outside the output folder: it is zipped for the release; env['TEMP'] = env['TMP'] = TMPD   # scratch pickles (data-v1) stay inside this build
summary = dict(started=time.strftime('%Y-%m-%d %H:%M:%S'), proj_root=paths.PROJ, steps=[], status='running')
T0 = time.time()

def finish(status, msg=''):
    summary['status'] = status; summary['message'] = msg; summary['seconds'] = round(time.time() - T0)
    json.dump(summary, open(J(OUT, 'build-summary.json'), 'w'), indent=1)
    shutil.rmtree(TMPD, ignore_errors=True)
    if not a.keep_lock: buildlock.release('build-all')
    print('BUILD', status, msg, flush=True); sys.exit(0 if status in ('ok', 'ok-harness-skipped', 'ok-harness-failed') else 1)

def step(n, name, cmd, cwd=RN, fatal=True, shell=False):
    t = time.time(); log = J(LOGS, '%02d-%s.log' % (n, name)); print('[step %d] %s' % (n, name), flush=True)
    with open(log, 'wb') as f:
        r = subprocess.run(cmd, cwd=cwd, env=env, stdout=f, stderr=subprocess.STDOUT, shell=shell, stdin=subprocess.DEVNULL)
    row = dict(step=n, name=name, rc=r.returncode, seconds=round(time.time() - t, 1), log=os.path.relpath(log, OUT)); summary['steps'].append(row)
    print('   rc=%d %.0fs' % (r.returncode, row['seconds']), flush=True)
    if r.returncode and fatal: finish('failed', 'step %d %s failed (rc=%d), see %s' % (n, name, r.returncode, row['log']))
    return r.returncode

# ---- 0 preflight
need = [('game exe (read only)', J(paths.GAME_DIR, 'FalloutNV.exe')), ('reference image (read only)', paths.REF_IMAGE), ('SP1 cl.exe', J(paths.MSVC9_SP1, 'VC', 'bin', 'cl.exe')),
        ('RTM cl.exe', J(paths.MSVC9_RTM, 'VC', 'bin', 'cl.exe')), ('units.json', J(paths.FN, 'build', 'units.json'))]
missing = [n + ': ' + p for n, p in need if not os.path.exists(p)]
summary['inputs'] = {n: p for n, p in need}
if missing: finish('failed', 'missing inputs: ' + '; '.join(missing))
if not buildlock.acquire('build-all', a.lock_wait): finish('failed', 'could not get build.lock')
# ---- 1..4 compile and rebuild
step(1, 'compile-units', [PY, '-I', J(RN, 'pinned-build', 'compile_units_v3.py'), '30'])
step(2, 'build-v7', ['cmd', '/c', J(RN, 'build-v7', 'rebuild.cmd')])
if not a.skip_data_v1:
    step(3, 'data-v1', ['cmd', '/c', J(RN, 'data-v1', 'rebuild.cmd')])
    step(4, 'dump-pieces', [PY, '-I', J(RN, 'data-v3', 'dump_pieces.py')])
step(5, 'data-v3', ['cmd', '/c', J(RN, 'data-v3', 'rebuild.cmd')])
# ---- 5..6 image
step(6, 'snapshot', [PY, J(RN, 'layout-v2', 'snapshot.py')])
exe = J(OUT, 'FalloutNV_selfbuilt.exe')
step(7, 'make-image', [PY, J(RN, 'layout-v2', 'make_image.py'), '--layout', a.layout, '--out', exe])
if not os.path.exists(exe): finish('failed', 'image missing')
summary['exe'] = dict(path=exe, bytes=os.path.getsize(exe), sha256=hashlib.sha256(open(exe, 'rb').read()).hexdigest())
# ---- provenance
prov = {}
try:
    p = json.load(open(J(RN, 'build-v7', 'progress.json')))
    prov['code_coverage_pct_of_nonpadding_text'] = p.get('coverage_pct_of_nonpadding_text'); prov['borrowed_relocation_field_bytes'] = p.get('borrowed_relocation_field_bytes')
    prov['undecompiled_bytes'] = p.get('undecompiled_bytes'); prov['filled_equals_reference'] = p.get('filled_equals_reference')
except Exception as e: prov['progress_error'] = str(e)
try:
    im = json.load(open(J(RN, 'layout-v2', 'build', 'image_%s.json' % a.layout)))
    prov['code_bytes_taken_from_filled_image'] = im.get('reference_code_bytes'); prov['data_pointer_fields'] = im.get('data_fields'); prov['rel32_fields'] = im.get('rel32'); prov['dir32_fields'] = im.get('dir32')
except Exception as e: prov['image_json_error'] = str(e)
summary['provenance'] = prov
# ---- harness (needs an interactive desktop)
hv = None
if a.no_harness: summary['harness'] = 'skipped (--no-harness)'
else:
    rc = step(8, 'harness', [PY, J(RN, 'direct-v1', 'harness.py'), exe, '--extended', '--play', str(a.play), '--tag', 'build-all'], fatal=False)
    try: hv = json.load(open(J(RN, 'direct-v1', 'harness-out', 'build-all', 'verdict.json')))
    except Exception: hv = None
    summary['harness'] = dict(rc=rc, pass_=bool(hv and hv.get('pass_')), steps=(hv or {}).get('steps'), error=(hv or {}).get('error'))
    if hv:
        try: shutil.copy2(J(RN, 'direct-v1', 'harness-out', 'build-all', 'verdict.json'), J(OUT, 'harness-verdict.json'))
        except Exception: pass
# ---- notes
L = ['Self-compiled FalloutNV build (code and data laid out by our own tools).', '',
     'exe: FalloutNV_selfbuilt.exe  sha256 %s' % summary['exe']['sha256'][:16], 'source commit/workspace: %s' % paths.PROJ, '',
     'code coverage from our source: %s%% of non-padding .text; borrowed field bytes %s; undecompiled bytes %s' % (prov.get('code_coverage_pct_of_nonpadding_text'), prov.get('borrowed_relocation_field_bytes'), prov.get('undecompiled_bytes')),
     'code bytes still taken from the reference image: %s' % prov.get('code_bytes_taken_from_filled_image'),
     'data: pointer fields %s' % prov.get('data_pointer_fields'),
     'harness: %s' % ('skipped' if a.no_harness else ('PASS' if summary['harness'].get('pass_') else 'FAIL/not run')),
     'build time: %d s' % (time.time() - T0), '',
     'Needs the owner\'s installed game (resources/data literals, read only) and the decrypted reference image (read only); neither is part of this archive.']
open(J(OUT, 'build-summary.txt'), 'w').write('\n'.join(L) + '\n')
if a.no_harness: finish('ok-harness-skipped')
if not summary['harness'].get('pass_'):
    finish('failed' if a.require_harness else 'ok-harness-failed', 'harness did not pass')
finish('ok')
