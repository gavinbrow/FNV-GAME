"""Replay saved W103 ownership, actual M3 COFF bytes and positive image identity."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

if sys.flags.optimize:
    raise RuntimeError('Evidence audits require assertions enabled')
HERE = Path(__file__).resolve().parent
M3 = HERE.parent
ROOT = M3.parents[1]
sys.path[:0] = [str(M3), str(ROOT / 'fnv_decomp/tools'), str(HERE), str(ROOT / 'runtime-next')]
from compare import Pe
import splice
import audit_native_methods_acceptance as common
from harness_evidence import accepted_verdict
import w103_frozen_proof

def load(path):
    return json.loads(path.read_bytes())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('run', choices=('positive', 'repeat'))
    ap.add_argument('--suite', choices=('v3', 'v4'), default='v3')
    args = ap.parse_args()
    run = M3 / ('out/phase2-psa-w103-' + args.suite + '-' + args.run)
    evidence = run / 'evidence'
    output = evidence / 'root-native-ownership-image-proof.json'
    if output.exists():
        raise FileExistsError(output)
    package = M3 / 'out/phase2-psa-w103-optin-package'
    manifest = load(package / 'manifest.json')
    frozen = Path(str(run) + '-freeze')
    freeze = load(frozen / 'result.json')
    assert freeze['command_rc'] == 0 and freeze['input_freeze_passed']
    assert not freeze['observed_metadata_changes'] and not freeze['final_digest_changes']
    before = load(frozen / 'inputs-before.json')
    fixed_input_proof = w103_frozen_proof.check(run, before)
    required = {package / 'selection.json': manifest['selection_sha256'],
                package / 'manifest.json': sha(package / 'manifest.json'),
                ROOT / 'fnv_decomp/build/units.json': manifest['recipe_sha256'],
                M3 / 'phase2/library_candidates.json': manifest['library_selection_sha256'],
                ROOT / 'FNV/work/worker1/FalloutNV.runtime-text.exe': 'df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7'}
    patch = load(M3 / 'out/phase2-psa-w103-control-patch/manifest.json')
    required.update({ROOT / x['path']: x['new_sha256'] for x in patch['files']})
    for path, digest in required.items():
        assert before[str(path.resolve())]['sha256'] == digest
    preflight = load(Path(str(run) + '-preflight.json'))
    assert preflight['recipe_sha256'] == manifest['recipe_sha256']
    for row in preflight['required']:
        assert before[str(Path(row['path']).resolve())]['sha256'] == row['sha256']
    summary = load(run / 'build-summary.json')
    assert summary['status'] == 'ok' and all(s['rc'] == 0 for s in summary['steps'])
    assert summary['provenance']['weak_coff']['enabled'] is False
    assert sha(evidence / 'units.json') == manifest['recipe_sha256']
    assert sha(evidence / 'selection.json') == manifest['selection_sha256']
    assert sha(evidence / 'library_candidates.json') == manifest['library_selection_sha256']
    assert sha(run / 'FalloutNV_selfbuilt.exe') == summary['exe']['sha256'] == 'c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f'
    reloc = common.reloc(run / 'FalloutNV_selfbuilt.exe')
    assert len(reloc) == 734884 and hashlib.sha256(reloc).hexdigest() == '364b83a38aae50e6faf0a4f0512fdfa8b338bd1dab47b39fec0bd7b03fd26057'
    verdict = load(run / 'harness-verdict.json')
    assert accepted_verdict(summary['harness']['rc'], verdict, summary['exe']['path'], summary['harness']['tag'])
    steps = verdict['steps']
    assert steps['extended_ok'] and steps['extended']['new_save_written'] and steps['extended']['cell_changed'] and steps['extended']['cell_restored']
    assert steps['exited_cleanly'] and steps['exit_code'] == 0
    entries = load(evidence / 'm3_manifest.json')['entries']
    pieces = load(evidence / 'dv1_pieces.json')['pieces']
    prior = M3 / 'out/phase2-native-source-positive/evidence'
    old_entries = load(prior / 'm3_manifest.json')['entries']
    old_pieces = load(prior / 'dv1_pieces.json')['pieces']
    assert len(entries) == 8269 and summary['provenance']['m3']['dropped'] == 0
    key = lambda p: (p['va'], p['size'], p['unit'], p['kind'])
    expected = {(0x110fbe8,20,620,'rtti4'), (0x110fbfc,16,620,'rtti3'), (0x110fc0c,13,620,'rtti2'), (0x110fc1c,28,620,'rtti1'), (0x1196e20,26,620,'rtti0')}
    assert {key(p) for p in pieces} - {key(p) for p in old_pieces} == expected
    assert not ({key(p) for p in old_pieces} - {key(p) for p in pieces})
    native = [p for p in pieces if key(p) in expected]
    assert len(native) == 5 and all(p['nunits'] == 1 for p in native)
    original = [p for p in old_entries if p['va'] in (0x110fbe8, 0x1196e1e)]
    residual = [p for p in entries if p['va'] in (0x110fc19, 0x1196e1e, 0x1196e3a)]
    byte_union = lambda seq: {a for p in seq for a in range(p['va'], p['va'] + p['size'])}
    old_union, native_union, residual_union = map(byte_union, (original, native, residual))
    assert len(old_union) == 1602 and len(native_union) == 103 and len(residual_union) == 1499
    assert not native_union & residual_union and old_union == native_union | residual_union
    sites = lambda seq, field: {p['va'] + r[0] for p in seq for r in p.get(field, [])}
    old_sites, native_sites, residual_sites = sites(original,'fields'), sites(native,'relocs'), sites(residual,'fields')
    assert (len(old_sites), len(native_sites), len(residual_sites)) == (61, 9, 52)
    assert not native_sites & residual_sites and old_sites == native_sites | residual_sites
    old_other = {p['va']: p for p in old_entries if p not in original}
    new_other = {p['va']: p for p in entries if p not in residual}
    # Manifest object packing/symbol indices may shift; selection identities may not.
    identity = lambda p: {k: v for k, v in p.items() if k not in ('obj', 'index')}
    assert set(old_other) == set(new_other)
    assert all(identity(old_other[k]) == identity(new_other[k]) for k in old_other)
    libs = [p for p in pieces if p.get('library_opt_in')]
    assert len(libs) == 405 and sum(p['size'] for p in libs) == 16730
    reference_path = ROOT / 'FNV/work/worker1/FalloutNV.runtime-text.exe'
    assert sha(reference_path) == required[reference_path]
    reference = Pe(str(reference_path))
    actual = splice.load(str(evidence / 'm3_manifest.json'), str(evidence / 'm3_data.obj'))
    table = splice.name_table(entries)
    ranges, total, tls = [], 0, 0
    all_records = []
    for record in actual:
        data = bytearray(record['data'])
        for off, name, addend in record['relocs']:
            target = splice.resolve(name, table)
            assert target is not None
            struct.pack_into('<I', data, off, (target + addend) & 0xffffffff)
        all_records.append((record['va'], data, record['entry']['section']))
    for p in pieces:
        data = bytearray.fromhex(p['data'])
        for off, target, addend in p['relocs']:
            struct.pack_into('<I', data, off, target)
        all_records.append((p['va'], data, p['section']))
    for va, data, section in all_records:
        assert data == reference.read(va, len(data))
        ranges.append((va, va + len(data)))
        if section in ('.data', '.rdata'):
            total += len(data)
        else:
            assert section == '.tls'
            tls += len(data)
    ranges.sort()
    assert all(a[1] <= b[0] for a, b in zip(ranges, ranges[1:]))
    assert total == 1613018 and tls == 5
    proof = {'status': 'PASS saved positive ownership/image/relocations/gameplay', 'run': args.run, 'native_bytes_replacing_W': 103, 'residual_W_bytes': 1499, 'preserved_relocation_sites': 61, 'initialized_data_bytes': total, 'tls_bytes_separate': tls, 'whole_phase2_complete': False, 'summary_sha256': sha(run / 'build-summary.json'), 'fixed_input_proof': fixed_input_proof, 'limits': ['Production unit620 function/EH and native COFF symbol-target proofs require separate oracle evidence.', 'Controls and repeat are separate gates; defaults are unchanged.']}
    output.write_text(json.dumps(proof, indent=2), encoding='utf-8')
    print(json.dumps(proof))

if __name__ == '__main__':
    main()
