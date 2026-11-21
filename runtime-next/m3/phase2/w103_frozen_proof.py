"""Fixed accepted input identities for independent saved W103 artifact audits."""
import hashlib
import json
from pathlib import Path
import sys

if sys.flags.optimize:
    raise RuntimeError('Evidence audits require assertions enabled')
M3 = Path(__file__).resolve().parent.parent
ROOT = M3.parents[1]
PACKAGE = M3 / 'out/phase2-psa-w103-optin-package'
PACKAGE_SHA = '65b12a3744550167f48c4af749fbe92a13624c265dadf7d0c408741d54207374'
PATCH_SHA = 'e1151c84a099a09b2acc021f93fd8d458bcb77baef66d412f5840b1885b3e107'
BASELINE_SHA = '48ef88bb8a247d5d09cd633964052c2ce2dd79cc98c6bc787e66d673cb008c96'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path):
    return json.loads(path.read_bytes())

def sources(snapshot):
    return {str(Path(k).resolve()).casefold(): v['sha256'] for k, v in snapshot.items()
            if '/fnv_decomp/src/' in k.lower().replace('\\', '/')
            or '/fnv_decomp/include/' in k.lower().replace('\\', '/')}

def check(run, snapshot):
    baseline = M3 / 'out/phase2-native-source-positive-freeze/inputs-before.json'
    patch_file = M3 / 'out/phase2-psa-w103-control-patch/manifest.json'
    assert sha(baseline) == BASELINE_SHA
    assert sha(patch_file) == PATCH_SHA
    assert sha(PACKAGE / 'manifest.json') == PACKAGE_SHA
    assert len(sources(snapshot)) == 5497 and sources(snapshot) == sources(load(baseline))
    manifest = load(PACKAGE / 'manifest.json')
    command = load(Path(str(run) + '-freeze') / 'command.json')
    environment = command['build_environment']
    assert environment.get('FNV_M3_LIB') == '1', 'explicit custom selection requires library enable flag'
    assert environment.get('FNV_COFF_WEAK') == '0'
    assert Path(environment['FNV_M3_SEL']).resolve() == (PACKAGE / 'selection.json').resolve()
    if environment.get('FNV_M3_LIB_SELECTION'):
        assert Path(environment['FNV_M3_LIB_SELECTION']).resolve() == (M3 / 'phase2/library_candidates.json').resolve()
    mode = run.name.rsplit('-', 1)[-1]
    assert environment.get('FNV_M3_NEGCTL') == (mode if mode in ('p2rv', 'p2rp') else None)
    expected = {str((ROOT / row['path']).resolve()): row['new_sha256'] for row in load(patch_file)['files']}
    expected.update({
        str((PACKAGE / 'selection.json').resolve()): manifest['selection_sha256'],
        str((M3 / 'phase2/library_candidates.json').resolve()): manifest['library_selection_sha256'],
        str((M3 / 'phase2/cost245_records.py').resolve()): '42770efbf44d39d9bcded7ab3e93f8d038d80a26bc7120d43c7fa197685cb64a',
        str((M3 / 'phase2/library_overlay.py').resolve()): 'dbdc7d9440ed99f4f64716fc77445df0f7cff21a5472925e875526b1cc9be1f7',
        str((ROOT / 'runtime-next/direct-v1/harness.py').resolve()): 'b6881aa7494d6e9a5b10d52fecf2ece943b697cc2df025c0f7ada66507a38f45',
    })
    assert len(expected) == 10
    preflight_path = Path(str(run) + '-preflight.json')
    preflight = load(preflight_path)
    assert preflight['recipe_sha256'] == manifest['recipe_sha256'] and preflight['watched_source_count'] == 5497
    rows = preflight['required']
    recorded = {str(Path(row['path']).resolve()): row['sha256'] for row in rows}
    assert len(rows) == 10 and recorded == expected, 'ten exact distinct preflight pins required'
    for name, digest in expected.items():
        assert snapshot[name]['sha256'] == digest
    assert snapshot[str((PACKAGE / 'manifest.json').resolve())]['sha256'] == PACKAGE_SHA
    return {'preflight_sha256': sha(preflight_path), 'accepted_source_snapshot_sha256': BASELINE_SHA,
            'package_manifest_sha256': PACKAGE_SHA, 'control_patch_manifest_sha256': PATCH_SHA,
            'required_production_inputs': 10, 'accepted_source_inputs': 5497}
