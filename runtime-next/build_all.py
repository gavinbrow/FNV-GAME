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
import os, sys, json, time, subprocess, argparse, hashlib, shutil, ntpath, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import paths, buildlock
from m3.config import configure, validate_driver_options, validate_library_result, DEFAULT_SELECTION, DEFAULT_SELECTION_SHA256, DEFAULT_LIBRARY_SELECTION, DEFAULT_LIBRARY_SHA256
from harness_evidence import accepted_verdict
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
def rtti_options(environment, skip):
    mode = environment.get('FNV_M3_RTTI_NAME_LITERAL')
    if mode not in (None, '0', '1'): raise ValueError('FNV_M3_RTTI_NAME_LITERAL must be 0 or 1')
    enabled = mode == '1'
    if enabled and (environment.get('FNV_M3') != '1' or environment.get('FNV_M3_DV1') != '1' or skip):
        raise ValueError('RTTI literal mode requires active M3/DV1 and fresh data-v1')
    return enabled

def rtti_archive_names(existing, enabled, success):
    names = [n for n in ('dv1_phase0.pkl', 'dv1_placed.pkl') if n in existing]
    if enabled and 'rtti-name-field-proof.json' in existing: names.append('rtti-name-field-proof.json')
    if enabled and success and 'rtti-name-field-proof.json' not in names: raise OSError('successful RTTI build lacks current proof')
    return names

def rtti_check_proof(proof, placement_hash, recipe_hash, code_hashes):
    if proof.get('schema') != 1 or proof.get('placement_sha256') != placement_hash or proof.get('recipe_sha256') != recipe_hash:
        raise OSError('RTTI proof does not bind current placement and recipe')
    if any(proof.get(k) != v for k,v in code_hashes.items()): raise OSError('RTTI proof code hashes differ')
    fields = proof.get('removed_value_fields')
    if fields != [0x01185d6c, 0x0118676c, 0x0119dc78]: raise OSError('RTTI proof fields differ')

env = configure(os.environ, promoted=True)
if env.get('FNV_M3_LIB_SELECTION'): env['FNV_M3_LIB_SELECTION'] = os.path.abspath(env['FNV_M3_LIB_SELECTION'])
try:
    validate_driver_options(env, skip_data_v1=a.skip_data_v1, raw_environment=os.environ)
    RTTI_MODE = rtti_options(env, a.skip_data_v1)
except ValueError as exc:
    ap.error(str(exc))
env.update(FNV_PROJ_ROOT=paths.PROJ, FNV_GAME_DIR=paths.GAME_DIR, FNV_MSVC9_RTM_ROOT=paths.MSVC9_RTM, FNV_MSVC9_ROOT=paths.MSVC9_SP1, FNV_MSVC8_ROOT=paths.MSVC8, FNV_REF_IMAGE=paths.REF_IMAGE)
env.setdefault('PYTHONDONTWRITEBYTECODE', '1')
if os.path.isdir(paths.PY_SITE): env['PYTHONPATH'] = paths.PY_SITE + os.pathsep + env.get('PYTHONPATH', '')   # numpy/capstone/pefile for the steps that do not run with -I
TMP_ROOT = os.path.realpath(J(paths.PROJ, '.build-tmp'))
TMPD = None
LOCK_HELD = False
summary = dict(started=time.strftime('%Y-%m-%d %H:%M:%S'), proj_root=paths.PROJ, steps=[], status='running')
M3 = env.get('FNV_M3') == '1'
M3_DV1 = M3 and env.get('FNV_M3_DV1') == '1'
NOREF = env.get('FNV_M3_NOREF') == '1'      # batch 9 stage 3 (opt-in): the data stages never open the reference image; they read the frozen inputs in m3rozen\ (see m39_freeze.py)
if os.environ.get('FNV_M3_NOREF') not in (None, '', '0', '1'): ap.error('FNV_M3_NOREF must be 0 or 1')
if NOREF and not (M3_DV1 and not a.skip_data_v1): ap.error('FNV_M3_NOREF requires active M3/DV1 and fresh data-v1')
NOREF2 = env.get('FNV_M3_NOREF2') == '1'     # batch 10 step C (opt-in): the data path reads no reference bytes (datasrc + frozen placement/replay maps + zero-filled data-v3 base)
if os.environ.get('FNV_M3_NOREF2') not in (None, '', '0', '1'): ap.error('FNV_M3_NOREF2 must be 0 or 1')
if NOREF2 and (NOREF or env.get('FNV_M3_DATASRC') != '1' or not (M3_DV1 and not a.skip_data_v1)): ap.error('FNV_M3_NOREF2 requires M3/DV1, FNV_M3_DATASRC=1, fresh data-v1 and not FNV_M3_NOREF')
CODE_NOREF = NOREF2 or os.environ.get('FNV_CODE_NOREF') == '1'     # batch 12 (opt-in): the code stage (build-v7) runs without the reference image, from the frozen layout m3\\frozen\\code_*.json; implied by FNV_M3_NOREF2=1
if os.environ.get('FNV_CODE_NOREF') not in (None, '', '0', '1'): ap.error('FNV_CODE_NOREF must be 0 or 1')
if os.environ.get('FNV_CODE_FREEZE') not in (None, '', '0'): ap.error('FNV_CODE_FREEZE writes the frozen layout; it belongs to a separate verified run of build-v7\\rebuild.cmd, not to build-all')
if CODE_NOREF and NOREF: ap.error('FNV_CODE_NOREF / FNV_M3_NOREF2 cannot be combined with FNV_M3_NOREF (batch 9 stage 3 reuses the code outputs of an earlier build)')
if CODE_NOREF: env['FNV_CODE_NOREF'] = '1'
else: env.pop('FNV_CODE_NOREF', None)
CODE_FZ = os.environ.get('FNV_CODE_FROZEN_DIR') or J(RN, 'm3', 'frozen')     # control runs point this at an edited copy (needs pe_meta.json too)
CODE_FROZEN = ('code_eh.json', 'code_crt.json', 'code_contrib.json', 'code_overlay.json', 'code_meta.json', 'code_icf_map.json')
CODE_OUTPUTS = ('icf_map.json', 'FalloutNV_v7_strict.exe', 'FalloutNV_v7_filled.exe', 'relocs_v7.tsv.gz', 'contrib_pieces.json', 'inferred_literals_v7.json', 'progress.json')
if os.environ.get('FNV_M3_NEGCTL') in ('p2nv', 'p2np') and not RTTI_MODE:
    ap.error('native literal controls require RTTI literal mode')
if os.environ.get('FNV_M3_NEGCTL') in ('p2rv', 'p2rp', 'p2tv', 'p2tp', 'p2nv', 'p2np', 'p2bv', 'p2bp', 'p2bw', 'p2cv', 'p2cp', 'p2cw') and (not M3_DV1 or a.skip_data_v1):
    ap.error('native RTTI controls require active M3/DV1 and fresh data-v1')
if M3:
    neg = env.get('FNV_M3_NEGCTL') or None
    controls = ('1', 'ptr', 'b4v', 'b4p', 'b5v', 'b5p', 'b6v', 'b6p', 'b7v', 'b7p', 'b8v', 'b8p', 'b9v', 'b9p', 'dsv', 'dsp', 'p2sv', 'p2av', 'p2wp', 'p2lv', 'p2rv', 'p2rp', 'p2tv', 'p2tp', 'p2nv', 'p2np', 'p2bv', 'p2bp', 'p2bw', 'p2cv', 'p2cp', 'p2cw')
    summary['provenance'] = {'m3_config': dict(
        selection=ntpath.basename(env.get('FNV_M3_SEL') or 'pilot_selection.json'),
        dv1=M3_DV1, dv1_ext=M3_DV1 and env.get('FNV_M3_DV1_EXT') == '1',
        dv1_kinds=env.get('FNV_M3_DV1_KINDS') or None,
        negative_control=neg if neg in controls or neg is None else 'unknown', selection_sha256=None)}
summary.setdefault('provenance', {})['weak_coff'] = dict(enabled=env.get('FNV_COFF_WEAK', '0') == '1', helper_sha256=None, resolver_sha256=None)
summary['provenance']['library_overlay'] = dict(enabled=bool(env.get('FNV_M3_LIB_SELECTION')), selection=ntpath.basename(env.get('FNV_M3_LIB_SELECTION') or '') or None, selection_sha256=None, archive_sha256=None, selected=None, bytes=None, section_index_base=1 if env.get('FNV_DV1_LIB_COFF_INDEX_V2') == '1' else 0, reader_sha256=None)
RTTI_CODE = {}
if RTTI_MODE:
    for _key, _name in (('bridge_sha256','selector_bridge.py'),('validator_sha256','validate_type_name_literal.py'),('allowlist_sha256','rtti-descriptor-allowlist.json'),('generation_sha256','generation_bridge.py')):
        with open(J(RN, 'm3', 'phase2', _name), 'rb') as _f: RTTI_CODE[_key] = hashlib.sha256(_f.read()).hexdigest()
summary['provenance']['rtti_name_literal'] = dict(enabled=RTTI_MODE, code_sha256=RTTI_CODE, proof_sha256=None)
T0 = time.time()

def finish(status, msg=''):
    summary['status'] = status; summary['message'] = msg; summary['seconds'] = round(time.time() - T0)
    try:
        archive_ok = True
        if TMPD is not None:
            try:
                evidence = J(OUT, 'evidence', 'data-v1-scratch')
                existing = [name for name in ('dv1_phase0.pkl', 'dv1_placed.pkl', 'rtti-name-field-proof.json') if os.path.isfile(J(TMPD, name))]
                files = rtti_archive_names(existing, RTTI_MODE, status in ('ok', 'ok-harness-skipped', 'ok-harness-failed'))
                if status in ('ok', 'ok-harness-skipped', 'ok-harness-failed') and not a.skip_data_v1 and 'dv1_placed.pkl' not in files:
                    raise OSError('successful data-v1 build lacks placement evidence')
                if files:
                    os.makedirs(evidence, exist_ok=True)
                    artifacts = {}
                    for name in files:
                        target = J(evidence, name)
                        if os.path.exists(target): raise FileExistsError('scratch evidence already exists: ' + target)
                        shutil.copy2(J(TMPD, name), target)
                        with open(target, 'rb') as f: artifacts[name] = hashlib.sha256(f.read()).hexdigest()
                    summary.setdefault('provenance', {})['data_v1_scratch_sha256'] = artifacts
                    if RTTI_MODE and 'rtti-name-field-proof.json' in artifacts:
                        with open(J(evidence, 'rtti-name-field-proof.json'), 'r') as f: _proof = json.load(f)
                        with open(J(paths.PROJ, 'fnv_decomp', 'build', 'units.json'), 'rb') as f: _recipe_hash = hashlib.sha256(f.read()).hexdigest()
                        rtti_check_proof(_proof, artifacts.get('dv1_placed.pkl'), _recipe_hash, {k:v for k,v in RTTI_CODE.items() if k != 'generation_sha256'})
                        summary['provenance']['rtti_name_literal']['proof_sha256'] = artifacts['rtti-name-field-proof.json']
            except (OSError, ValueError, KeyError, TypeError) as exc:
                archive_ok = False
                status = summary['status'] = 'failed'
                msg = summary['message'] = 'cannot archive data-v1 scratch; preserved at %s: %s' % (TMPD, exc)
            if archive_ok:
                try:
                    if os.path.commonpath((TMP_ROOT, os.path.realpath(TMPD))) != TMP_ROOT or os.path.realpath(TMPD) == TMP_ROOT:
                        raise OSError('scratch path escapes private root')
                    shutil.rmtree(TMPD)
                except OSError as exc:
                    status = summary['status'] = 'failed'
                    msg = summary['message'] = 'cannot remove private scratch at %s: %s' % (TMPD, exc)
        with open(J(OUT, 'build-summary.json'), 'w') as f: json.dump(summary, f, indent=1)
    finally:
        if LOCK_HELD and not a.keep_lock: buildlock.release('build-all')
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
if NOREF:      # the reference image is not an input: frozen data inputs and the code artifacts of an earlier full build are
    need = [x for x in need if not x[0].startswith('reference image')] + [('frozen ' + f, J(RN, 'm3', 'frozen', f)) for f in ('ref_headers.bin', 'ref_data.bin.z', 'ref_reloc.bin.z', 'ref_meta.json')] +            [('build-v7 ' + f, J(RN, 'build-v7', f)) for f in ('FalloutNV_v7_strict.exe', 'FalloutNV_v7_filled.exe', 'icf_map.json', 'relocs_v7.tsv.gz', 'contrib_pieces.json', 'inferred_literals_v7.json', 'progress.json')]
if NOREF2:     # the reference image is not an input: data from the frozen placement/replay maps + datasrc, code from the frozen code layout (code_*.json); build-v7 is RERUN
    need = [x for x in need if not x[0].startswith('reference image')] + [('frozen ' + f, J(RN, 'm3', 'frozen', f)) for f in ('placement_map.json', 'dv1_replay.json', 'dv3_meta.json', 'pe_meta.json')] + \
           [('datasrc index', J(RN, 'm3', 'datasrc', 'index.json'))]
if CODE_NOREF:
    need += [('frozen ' + f, J(CODE_FZ, f)) for f in CODE_FROZEN] + [('frozen pe_meta.json', J(CODE_FZ, 'pe_meta.json'))]
missing = [n + ': ' + p for n, p in need if not os.path.exists(p)]
summary['inputs'] = {n: p for n, p in need}
if missing: finish('failed', 'missing inputs: ' + '; '.join(missing))
if not buildlock.acquire('build-all', a.lock_wait): finish('failed', 'could not get build.lock')
LOCK_HELD = True
try:
    project_root = os.path.realpath(paths.PROJ)
    if os.path.commonpath((project_root, TMP_ROOT)) != project_root or TMP_ROOT == project_root:
        raise OSError('build scratch root is outside project')
    os.makedirs(TMP_ROOT, exist_ok=True)
    TMPD = tempfile.mkdtemp(prefix='build-', dir=TMP_ROOT)
    env['TEMP'] = env['TMP'] = TMPD
except OSError as exc:
    finish('failed', 'cannot create private build scratch: ' + str(exc))
if env.get('FNV_M3_LIB_SELECTION'):
    try:
        with open(env['FNV_M3_LIB_SELECTION'], 'rb') as f: library_digest = hashlib.sha256(f.read()).hexdigest()
        if os.path.normcase(os.path.abspath(env['FNV_M3_LIB_SELECTION'])) == os.path.normcase(os.path.abspath(J(RN, 'm3', DEFAULT_LIBRARY_SELECTION))) and library_digest != DEFAULT_LIBRARY_SHA256:
            finish('failed', 'default library selection SHA-256 does not match pinned digest')
        if library_digest != env['FNV_M3_LIB_SHA256'].lower():
            finish('failed', 'library selection SHA-256 does not match requested digest')
        summary['provenance']['library_overlay']['selection_sha256'] = library_digest
    except OSError as exc:
        finish('failed', 'cannot hash library selection: ' + str(exc))
try:
    with open(J(RN, 'data-v2', 'libsecs.py'), 'rb') as f:
        summary['provenance']['library_overlay']['reader_sha256'] = hashlib.sha256(f.read()).hexdigest()
except OSError as exc:
    finish('failed', 'cannot hash library section reader: ' + str(exc))
if env.get('FNV_COFF_WEAK', '0') == '1':
    try:
        for key, name in (('helper_sha256', 'coff_weak.py'), ('resolver_sha256', 'assemble_v3.py')):
            with open(J(RN, 'pinned-build', name), 'rb') as f:
                summary['provenance']['weak_coff'][key] = hashlib.sha256(f.read()).hexdigest()
    except OSError as exc:
        finish('failed', 'cannot hash weak COFF inputs: ' + str(exc))
# Validate the selected input before compiling or mutating build outputs.
if M3:
    try:
        selection = J(RN, 'm3', env.get('FNV_M3_SEL') or 'pilot_selection.json')
        with open(selection, 'rb') as f: digest = hashlib.sha256(f.read()).hexdigest()
        summary['provenance']['m3_config']['selection_sha256'] = digest
        if os.path.normcase(os.path.abspath(selection)) == os.path.normcase(os.path.abspath(J(RN, 'm3', DEFAULT_SELECTION))) and digest != DEFAULT_SELECTION_SHA256:
            finish('failed', 'default M3 selection SHA-256 does not match pinned digest')
    except (OSError, ValueError) as exc:
        finish('failed', 'cannot read M3 selection for SHA-256: ' + str(exc))
# ---- 1..4 compile and rebuild
if NOREF:
    # stand-in image for the data stages: frozen headers/data/.reloc + the strict .text of our own earlier build; FNV_REF_IMAGE (whatever it points to) is replaced for every child process
    SYNTH = J(RN, 'm3', 'gen', 'ref-synth.exe'); os.makedirs(J(RN, 'm3', 'gen'), exist_ok=True)
    step(0, 'noref-synth', [PY, '-I', J(RN, 'm3', 'b9_freeze.py'), '--synth', SYNTH])
    env['FNV_REF_IMAGE'] = SYNTH
    summary['provenance']['noref'] = dict(enabled=True, stand_in_image=SYNTH, stand_in_sha256=hashlib.sha256(open(SYNTH, 'rb').read()).hexdigest(),
        frozen_sha256={f: hashlib.sha256(open(J(RN, 'm3', 'frozen', f), 'rb').read()).hexdigest() for f in ('ref_headers.bin', 'ref_data.bin.z', 'ref_reloc.bin.z', 'ref_meta.json')},
        build_v7_artifacts_sha256={f: hashlib.sha256(open(J(RN, 'build-v7', f), 'rb').read()).hexdigest() for f in ('FalloutNV_v7_strict.exe', 'FalloutNV_v7_filled.exe', 'icf_map.json', 'relocs_v7.tsv.gz', 'contrib_pieces.json', 'inferred_literals_v7.json', 'progress.json')},
        note='build-v7 (code placement, verifies compiled code against the reference) is NOT rerun: its outputs from the previous full build are reused')
if NOREF2:
    FZ = J(RN, 'm3', 'frozen')
    env.update(FNV_DV1_PLACEMENT_MAP=J(FZ, 'placement_map.json'), FNV_M3_DV1_REPLAY=J(FZ, 'dv1_replay.json'))
    summary['provenance']['noref2'] = dict(enabled=True, FNV_REF_IMAGE=env.get('FNV_REF_IMAGE'), reference_image_exists=os.path.exists(env.get('FNV_REF_IMAGE') or ''),
        frozen_sha256={f: hashlib.sha256(open(J(FZ, f), 'rb').read()).hexdigest() for f in ('placement_map.json', 'dv1_replay.json', 'dv3_meta.json', 'pe_meta.json') + CODE_FROZEN},
        datasrc_index_sha256=hashlib.sha256(open(J(RN, 'm3', 'datasrc', 'index.json'), 'rb').read()).hexdigest(),
        unused_frozen_files=['m3/frozen/ref_data.bin.z', 'm3/frozen/ref_reloc.bin.z', 'm3/frozen/ref_headers.bin'],
        note='data path reads no reference bytes; the code stage (build-v7) is RERUN with FNV_CODE_NOREF=1 from the frozen code layout (see provenance.code_noref)')
step(1, 'compile-units', [PY, '-I', J(RN, 'pinned-build', 'compile_units_v3.py'), '30'])
if M3:
    step(1, 'm3-gen', [PY, '-I', J(RN, 'm3', 'gen_m3.py')])
    env.update(FNV_M3='1', DV_M3='1', DV3_SKIP=J(RN, 'm3', 'gen', 'skip_ranges.json'))
if M3_DV1: env.update(FNV_M3_DV1='1', DV3_SKIP=J(RN, 'm3', 'gen', 'skip_ranges_b5.json'))
if not NOREF:
    if CODE_NOREF:      # the code stage must be rerun, not reused: delete every output the later stages read, then check they are written anew
        _gone = []
        for f in CODE_OUTPUTS:
            fp = J(RN, 'build-v7', f)
            if os.path.exists(fp): os.remove(fp); _gone.append(f)
        _t_code = time.time()
    step(2, 'build-v7', ['cmd', '/c', J(RN, 'build-v7', 'rebuild.cmd')])
    if CODE_NOREF:
        _new = {}
        for f in CODE_OUTPUTS:
            fp = J(RN, 'build-v7', f)
            if not os.path.exists(fp) or os.path.getmtime(fp) < _t_code - 1: finish('failed', 'code stage did not rewrite build-v7\\' + f)
            _new[f] = hashlib.sha256(open(fp, 'rb').read()).hexdigest()
        with open(J(RN, 'build-v7', 'progress.json')) as _f: _pg = json.load(_f)
        if not _pg.get('code_noref'): finish('failed', 'build-v7 progress.json does not record a no-reference code stage')
        summary['provenance']['code_noref'] = dict(enabled=True, deleted_before_run=_gone, rewritten_sha256=_new, progress_text_sha256=_pg.get('text_sha256'), text_equals_frozen_hash=_pg.get('text_equals_frozen_hash'),
            coverage_pct_of_nonpadding_text=_pg.get('coverage_pct_of_nonpadding_text'), borrowed_relocation_field_bytes=_pg.get('borrowed_relocation_field_bytes'),
            frozen_sha256={f: hashlib.sha256(open(J(CODE_FZ, f), 'rb').read()).hexdigest() for f in CODE_FROZEN}, frozen_dir=CODE_FZ,
            note='build-v7 outputs deleted before the step and rewritten by it (mtime checked); no reference image is opened by the code stage')
if not a.skip_data_v1:
    if NOREF or NOREF2:       # rebuild.cmd without report.py (a reporting-only pass over the whole reference)
        if NOREF2:      # phase0 compares our compiled units with the code image: a stand-in (headers from json, OUR strict .text, imports from iat_spec.json, everything else zero)
            SI = J(RN, 'm3', 'gen', 'standin.exe'); step(3, 'noref2-standin', [PY, '-I', J(RN, 'm3', 'b10_standin.py'), SI])
            REF_SAVED = env.get('FNV_REF_IMAGE'); env['FNV_REF_IMAGE'] = SI
        step(3, 'data-v1-phase0', [PY, '-I', J(RN, 'data-v1', 'phase0.py'), J(env['TEMP'], 'dv1_phase0.pkl')])
        if NOREF2: env['FNV_REF_IMAGE'] = REF_SAVED
        step(3, 'data-v1-place', [PY, '-I', J(RN, 'data-v1', 'place.py'), J(env['TEMP'], 'dv1_phase0.pkl'), J(env['TEMP'], 'dv1_placed.pkl')])
    else: step(3, 'data-v1', ['cmd', '/c', J(RN, 'data-v1', 'rebuild.cmd')])
    step(4, 'dump-pieces', [PY, '-I', J(RN, 'data-v3', 'dump_pieces.py')])
    if M3_DV1: step(4, 'm3-dv1', [PY, '-I', J(RN, 'm3', 'dv1_splice.py'), J(env.get('TEMP') or os.environ.get('TEMP'), 'dv1_placed.pkl')] + (['--kinds', env['FNV_M3_DV1_KINDS']] if env.get('FNV_M3_DV1_KINDS') else []))
    if env.get('FNV_M3_LIB_SELECTION'):
        try:
            with open(J(RN, 'm3', 'gen', 'dv1_log.json')) as f: library_result = json.load(f)['library_opt_in']
            summary['provenance']['library_overlay'].update(validate_library_result(library_result, library_digest))
        except (OSError, KeyError, ValueError, TypeError) as exc:
            finish('failed', 'cannot validate library overlay provenance: ' + str(exc))
if NOREF2:
    step(5, 'data-v3-zero-base', [PY, '-I', J(RN, 'data-v3', 'gen_zero.py')])
    step(5, 'data-v3-asm', ['cmd', '/c', J(RN, 'data-v3', 'asm.cmd')])
    # symbolic.json of the zero base stays in data-v3\out (snapshot.py takes it from there in this mode); data-v3\symbolic.json (normal builds) is not overwritten
else: step(5, 'data-v3', ['cmd', '/c', J(RN, 'data-v3', 'rebuild.cmd')])
# ---- 5..6 image
step(6, 'snapshot', [PY, J(RN, 'layout-v2', 'snapshot.py')])
exe = J(OUT, 'FalloutNV_selfbuilt.exe')
step(7, 'make-image', [PY, J(RN, 'layout-v2', 'make_image.py'), '--layout', a.layout, '--out', exe])
if not os.path.exists(exe): finish('failed', 'image missing')
summary['exe'] = dict(path=exe, bytes=os.path.getsize(exe), sha256=hashlib.sha256(open(exe, 'rb').read()).hexdigest())
# ---- provenance
prov = summary.get('provenance', {})
try:
    p = json.load(open(J(RN, 'build-v7', 'progress.json')))
    prov['code_coverage_pct_of_nonpadding_text'] = p.get('coverage_pct_of_nonpadding_text'); prov['borrowed_relocation_field_bytes'] = p.get('borrowed_relocation_field_bytes')
    prov['undecompiled_bytes'] = p.get('undecompiled_bytes'); prov['filled_equals_reference'] = p.get('filled_equals_reference')
except Exception as e: prov['progress_error'] = str(e)
try:
    im = json.load(open(J(RN, 'layout-v2', 'build', 'image_%s.json' % a.layout)))
    prov['code_bytes_taken_from_filled_image'] = im.get('reference_code_bytes'); prov['data_pointer_fields'] = im.get('data_fields'); prov['rel32_fields'] = im.get('rel32'); prov['dir32_fields'] = im.get('dir32')
except Exception as e: prov['image_json_error'] = str(e)
if M3:
    try:
        lg = json.load(open(J(RN, 'm3', 'gen', 'm3_gen.log.json'))); prov['m3'] = dict(globals=lg['kept'], dropped=len(lg['dropped']), bytes=lg['bytes_by_section'], negctl=lg['negctl'])
        if M3_DV1: dl = json.load(open(J(RN, 'm3', 'gen', 'dv1_log.json'))); prov['m3_dv1'] = dict(pieces=dl['selected'], bytes=dl['bytes'], relocs=dl['relocs'], by_kind=dl['by_kind'], rejected_bytes_by_reason=dl['rejected_bytes_by_reason'], ext=dl.get('ext'), rejected_unique_uncovered=dl.get('rejected_unique_uncovered'))
    except Exception as e: prov['m3_error'] = str(e)
summary['provenance'] = prov
# ---- harness (needs an interactive desktop)
# Do not let a reused output directory retain a verdict from an earlier run.
try:
    os.remove(J(OUT, 'harness-verdict.json'))
except FileNotFoundError:
    pass
except OSError as exc:
    finish('failed', 'cannot clear previous harness verdict: ' + str(exc))
hv = None
if a.no_harness: summary['harness'] = 'skipped (--no-harness)'
else:
    harness_tag = 'build-all-%d-%d' % (os.getpid(), time.time_ns())
    verdict_path = J(RN, 'direct-v1', 'harness-out', harness_tag, 'verdict.json')
    rc = step(8, 'harness', [PY, J(RN, 'direct-v1', 'harness.py'), exe, '--extended', '--play', str(a.play), '--tag', harness_tag], fatal=False)
    try:
        with open(verdict_path) as f: hv = json.load(f)
    except (OSError, ValueError): hv = None
    passed = rc == 0 and accepted_verdict(rc, hv, exe, harness_tag) is True
    verdict = hv if isinstance(hv, dict) else {}
    summary['harness'] = dict(rc=rc, tag=harness_tag, verdict_path=verdict_path, pass_=passed, steps=verdict.get('steps'),
                              error=verdict.get('error') or (None if passed else 'unsuccessful or invalid harness verdict'))
    if passed:
        try: shutil.copy2(verdict_path, J(OUT, 'harness-verdict.json'))
        except OSError: pass
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
