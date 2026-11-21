"""Prepare (do not apply) library-option/provenance driver + checker patch."""
from pathlib import Path
import difflib
R=Path(__file__).resolve().parents[2]
def inject(s,anchor,added,before=False):
 if s.count(anchor)!=1:raise ValueError('unexpected anchor: '+anchor[:90])
 return s.replace(anchor,added+anchor if before else anchor+added,1)
def config(s):
 s=inject(s,'    weak = env.get(\'FNV_COFF_WEAK\', \'0\')\n', '''    raw = env if raw_environment is None else raw_environment
    selection, digest = raw.get('FNV_M3_LIB_SELECTION'), raw.get('FNV_M3_LIB_SHA256')
    if selection is not None or digest is not None:
        import re
        if not selection or not digest or re.fullmatch(r'[0-9a-fA-F]{64}', digest) is None:
            raise ValueError('library overlay requires selection and a SHA-256 digest')
        if env.get('FNV_M3') != '1' or env.get('FNV_M3_DV1') != '1' or skip_data_v1:
            raise ValueError('library overlay requires active M3/DV1 and fresh data-v1')
''',True)
 return s.replace('def validate_driver_options(env, skip_data_v1=False):','def validate_driver_options(env, skip_data_v1=False, raw_environment=None):')
def driver(s):
 s=s.replace('import os, sys, json, time, subprocess, argparse, hashlib, shutil, ntpath','import os, sys, json, time, subprocess, argparse, hashlib, shutil, ntpath, re',1)
 s=inject(s,"env = configure(os.environ, promoted=True)\n", "if env.get('FNV_M3_LIB_SELECTION'): env['FNV_M3_LIB_SELECTION'] = os.path.abspath(env['FNV_M3_LIB_SELECTION'])\n")
 s=s.replace('validate_driver_options(env, skip_data_v1=a.skip_data_v1)','validate_driver_options(env, skip_data_v1=a.skip_data_v1, raw_environment=os.environ)')
 anchor="summary.setdefault('provenance', {})['weak_coff'] = dict(enabled=env.get('FNV_COFF_WEAK', '0') == '1', helper_sha256=None, resolver_sha256=None)\n"
 s=inject(s,anchor,"summary['provenance']['library_overlay'] = dict(enabled=bool(env.get('FNV_M3_LIB_SELECTION')), selection=ntpath.basename(env.get('FNV_M3_LIB_SELECTION') or '') or None, selection_sha256=None, archive_sha256=None, selected=None, bytes=None)\n")
 anchor="if not buildlock.acquire('build-all', a.lock_wait): finish('failed', 'could not get build.lock')\n"
 s=inject(s,anchor,'''if env.get('FNV_M3_LIB_SELECTION'):
    try:
        with open(env['FNV_M3_LIB_SELECTION'], 'rb') as f: library_digest = hashlib.sha256(f.read()).hexdigest()
        if library_digest != env['FNV_M3_LIB_SHA256'].lower():
            finish('failed', 'library selection SHA-256 does not match requested digest')
        summary['provenance']['library_overlay']['selection_sha256'] = library_digest
    except OSError as exc:
        finish('failed', 'cannot hash library selection: ' + str(exc))
''')
 anchor="    if M3_DV1: step(4, 'm3-dv1', [PY, '-I', J(RN, 'm3', 'dv1_splice.py'), J(env.get('TEMP') or os.environ.get('TEMP'), 'dv1_placed.pkl')] + (['--kinds', env['FNV_M3_DV1_KINDS']] if env.get('FNV_M3_DV1_KINDS') else []))\n"
 s=inject(s,anchor,'''    if env.get('FNV_M3_LIB_SELECTION'):
        try:
            with open(J(RN, 'm3', 'gen', 'dv1_log.json')) as f: library_result = json.load(f)['library_opt_in']
            if library_result['selection_sha256'] != library_digest or set(library_result['archive_sha256']) != {'libcmt.lib', 'libcpmt.lib'}:
                raise ValueError('missing or mismatched library overlay provenance')
            if any(not isinstance(v, str) or re.fullmatch(r'[0-9a-f]{64}', v) is None for v in library_result['archive_sha256'].values()):
                raise ValueError('invalid archive hashes')
            if type(library_result['selected']) is not int or library_result['selected'] <= 0 or type(library_result['bytes']) is not int or library_result['bytes'] <= 0:
                raise ValueError('invalid library selected/byte counts')
            summary['provenance']['library_overlay'].update(archive_sha256=library_result['archive_sha256'], selected=library_result['selected'], bytes=library_result['bytes'])
        except (OSError, KeyError, ValueError, TypeError) as exc:
            finish('failed', 'cannot validate library overlay provenance: ' + str(exc))
''')
 return s
def checker(s):
 anchor='def check_weak_consistency(positive, controls):\n'
 s=inject(s,anchor,'''def check_library_consistency(positive, controls, expected_sha256=None):
    runs = [('positive', positive)] + [('control %d' % (i + 1), c) for i, c in enumerate(controls)]
    configs = [(label, run.get('provenance', {}).get('library_overlay')) for label, run in runs]
    active = [c for _, c in configs if isinstance(c, dict) and c.get('enabled') is True]
    if not active and expected_sha256 is None:
        return []
    if not active:
        return ['library overlay expected but not recorded']
    first = active[0]; errors = []
    if expected_sha256 is not None and (re.fullmatch(r'[0-9a-fA-F]{64}', expected_sha256) is None or first.get('selection_sha256') != expected_sha256.lower()):
        errors.append('library selection digest mismatch')
    for label, c in configs:
        if not isinstance(c, dict) or c.get('enabled') is not True:
            errors.append(label + ': library overlay mode missing or disabled'); continue
        if not isinstance(c.get('selection_sha256'), str) or re.fullmatch(r'[0-9a-f]{64}', c['selection_sha256']) is None:
            errors.append(label + ': invalid library selection digest')
        if c.get('selection_sha256') != first.get('selection_sha256') or c.get('archive_sha256') != first.get('archive_sha256') or c.get('selected') != first.get('selected') or c.get('bytes') != first.get('bytes'):
            errors.append(label + ': library provenance mismatch')
        archives=c.get('archive_sha256')
        if not isinstance(archives,dict) or set(archives) != {'libcmt.lib','libcpmt.lib'} or any(not isinstance(v,str) or re.fullmatch(r'[0-9a-f]{64}',v) is None for v in archives.values()):
            errors.append(label + ': invalid library archive hashes')
        if type(c.get('selected')) is not int or c['selected'] <= 0 or type(c.get('bytes')) is not int or c['bytes'] <= 0:
            errors.append(label + ': invalid library coverage counts')
    return errors


''',True)
 anchor="    args = parser.parse_args()\n";s=inject(s,anchor,"    parser.add_argument('--expected-library-sha256')\n",True)
 anchor="        errors.extend(check_weak_consistency(positive, controls))\n";s=inject(s,anchor,"        errors.extend(check_library_consistency(positive, controls, args.expected_library_sha256))\n")
 return s
out=[]
for rel,func in [(Path('m3/config.py'),config),(Path('build_all.py'),driver),(Path('m3/tools/verify_saved_runs.py'),checker)]:
 old=(R/rel).read_text();new=func(old)
 out.extend(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='a/runtime-next/'+rel.as_posix(),tofile='b/runtime-next/'+rel.as_posix()))
path=R/'m3/phase2/library_driver_provenance.patch';path.write_text(''.join(out));print(path)
