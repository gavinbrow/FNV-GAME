"""Accept only the complete saved native-source positive/control/repeat suite."""
import hashlib
import json
from pathlib import Path
import sys

H = Path(__file__).resolve().parent
M = H.parent
R = M.parent.parent
sys.path[:0] = [str(H), str(M / 'tools'), str(R / 'runtime-next')]
import verify_saved_runs as checker
import audit_native_source_artifacts as artifact

O = M / 'out'
IDS = ('p2av', 'p2wp')
CONTROL_HASHES = ('a8cc4e724cd6b9a7bfbcbae046a6ad2058383555e05d006d1788ef464a069b6b',
                  'f60aab12eb29c7ad62b9097a287e61c1710fdcfb4a46aa27fc2959dee5249a60')


def load(p):
    return json.loads(p.read_bytes())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def source_snapshot(path):
    return {str(Path(k).resolve()).casefold(): v['sha256'] for k, v in load(path).items()
            if '/fnv_decomp/src/' in k.lower().replace('\\', '/')
            or '/fnv_decomp/include/' in k.lower().replace('\\', '/')}


def main():
    output = O / 'phase2-native-source-acceptance.json'
    if output.exists():
        raise FileExistsError(output)
    baseline = load(O / 'batch8-baseline/build-summary.json')
    controls = [load(O / ('phase2-native-source-' + n) / 'build-summary.json') for n in IDS]
    positive = O / 'phase2-native-source-positive'
    sources = source_snapshot(Path(str(positive) + '-freeze/inputs-before.json'))
    assert len(sources) == 5497
    control_proofs = []
    for n, expected, control in zip(IDS, CONTROL_HASHES, controls):
        d = O / ('phase2-native-source-' + n)
        freeze_dir = Path(str(d) + '-freeze')
        freeze = load(freeze_dir / 'result.json')
        assert freeze['command_rc'] == 0 and freeze['input_freeze_passed']
        assert not freeze['final_digest_changes'] and not freeze['observed_metadata_changes']
        assert source_snapshot(freeze_dir / 'inputs-before.json') == sources
        assert load(freeze_dir / 'command.json')['build_environment'] == {'FNV_COFF_WEAK': '0', 'FNV_M3_NEGCTL': n}
        assert sha(d / 'FalloutNV_selfbuilt.exe') == control['exe']['sha256'] == expected
        assert sha(d / 'evidence/units.json') == artifact.RECIPE
        proof_path = d / 'evidence' / ('independent-' + n + '-proof.json')
        proof = load(proof_path)
        assert proof['control'] == n and proof['roundtrip_failure_observed'] and proof['source_files_equal'] == 5497
        assert checker.check_control_logs(d / 'build-summary.json', control) == ('pointer' if n == 'p2wp' else 'value')
        control_proofs.append({'id': n, 'summary_sha256': sha(d / 'build-summary.json'),
                               'mutation_proof_sha256': sha(proof_path), 'image_sha256': expected})
    accepted = []
    for tag in ('positive', 'repeat'):
        d = O / ('phase2-native-source-' + tag)
        summary = load(d / 'build-summary.json')
        verdict = load(d / 'harness-verdict.json')
        errors = checker.check(summary, baseline, controls, verdict) + checker.check_cell_state(verdict)
        errors += checker.check_recorded_config(summary, baseline, controls, 'selection.json', list(IDS))
        errors += checker.check_selection_sha256(summary, controls, artifact.SEL)
        errors += checker.check_library_consistency(summary, controls, artifact.LIB)
        errors += checker.check_provenance(summary, [('default', baseline)] + [('control', x) for x in controls])
        for label, x in [(tag, summary)] + [('control', x) for x in controls]:
            errors += checker.check_extended_mode(x, label) + checker.check_weak_coff(x, label, '0', None, None)
        assert not errors, errors
        assert source_snapshot(Path(str(d) + '-freeze/inputs-before.json')) == sources
        data = load(d / 'evidence/root-data-image-freeze-review.json')
        assert data['summary_sha256'] == sha(d / 'build-summary.json') and data['recipe_sha256'] == artifact.RECIPE
        assert data['initialized_data_bytes'] == 1613018 and data['tls_bytes_separate'] == 5
        audit_path = O / ('phase2-native-source-' + tag + '-audit.json')
        audit = load(audit_path)
        assert audit['summary_sha256'] == sha(d / 'build-summary.json')
        assert set(audit['objects']) == {'253', '370', '425', '620', '621', '2909', '2910'}
        assert sum(x['functions'] for x in audit['objects'].values()) == 1100
        assert sum(x['matches'] for x in audit['objects'].values()) == 1100
        assert sum(len(x['eh_sections']) for x in audit['objects'].values()) == 389
        assert all(not x['failures'] and not x['eh_errors'] and all(y[2] for y in x['eh_sections']) for x in audit['objects'].values())
        assert audit['recipe_eh_tail_count'] == 8 and not audit['bad_tails'] and not audit['tail_conflicts']
        assert not audit['recipe_primary_bindings'] and audit['archived_icf_primary'] is None
        pins = O / ('phase2-native-source-' + tag + '-pins.json')
        assert audit['archive_pins_sha256'] == sha(pins)
        for rel, digest in load(pins).items():
            assert sha(d / rel) == digest
        assert all(x['sha256'] == sha(d / 'evidence' / ('%04d.obj' % int(i))) for i, x in audit['objects'].items())
        accepted.append({'run': tag, 'summary_sha256': sha(d / 'build-summary.json'),
                         'artifact_review_sha256': sha(d / 'evidence/root-data-image-freeze-review.json'),
                         'oracle_audit_sha256': sha(audit_path), 'archive_pins_sha256': sha(pins),
                         'image_sha256': artifact.CANONICAL, 'functions': 1100, 'ordinary_eh_sections': 389,
                         'ordinary_eh_tails': 8, 'play_seconds': verdict['steps']['play_secs']})
    assert sha(R / 'fnv_decomp/build/units.json') == artifact.RECIPE
    result = {'status': 'PASS complete native-source positive/two-controls/repeat suite',
              'whole_phase2_complete': False, 'recipe_sha256': artifact.RECIPE,
              'transaction_manifest_sha256': sha(O / 'phase2-source-integration6757-transaction-v2/manifest.json'),
              'runs': accepted, 'controls': control_proofs, 'source_inputs_unchanged_between_runs': len(sources),
              'initialized_data_bytes': 1613018, 'tls_bytes_separate': 5,
              'limitations': ['PSA weak E remains excluded; no generic weak resolver is enabled.',
                             'Whole-class registry, global ODR/source consolidation and remaining Phase 2 types are open.']}
    output.write_text(json.dumps(result, indent=2), encoding='utf8')
    print(json.dumps({k: result[k] for k in ('status', 'initialized_data_bytes', 'whole_phase2_complete')}))


if __name__ == '__main__':
    main()
