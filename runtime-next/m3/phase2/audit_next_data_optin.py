"""Replay the next-data opt-in gates without promoting the accepted defaults."""
import copy
import hashlib
import json
import struct
from pathlib import Path
import audit_native_methods_acceptance as base
from compare import Coff, Pe, compare
from build_and_match import recipe_names, eh_sections, eh_tails
from harness_evidence import accepted_verdict
import verify_saved_runs as checker
import paths

M = Path(__file__).resolve().parent.parent
O = M / 'out'
TX = O / 'phase2-next-data-transaction6757'
CANONICAL = 'c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f'
IDS = ('p2av', 'p2wp', 'p2lv')
HASHES = ('a8cc4e724cd6b9a7bfbcbae046a6ad2058383555e05d006d1788ef464a069b6b',
          'f60aab12eb29c7ad62b9097a287e61c1710fdcfb4a46aa27fc2959dee5249a60',
          'd1e930c080f460018e4fd5ded4ab7cafed35f7ac3cee79bbd6aec46c21ef9a73')

def normal_snapshot(path):
    return {str(Path(k).resolve()).casefold(): v for k, v in base.load(path).items()}

def source_hashes(snapshot):
    return {k: v['sha256'] for k, v in snapshot.items()
            if '/fnv_decomp/src/' in k.replace('\\', '/') or '/fnv_decomp/include/' in k.replace('\\', '/')}

def main():
    manifest = base.load(TX / 'manifest.json')
    baseline = base.load(O / 'batch8-baseline/build-summary.json')
    controls = [base.load(O / ('phase2-next-data-' + n + '/build-summary.json')) for n in IDS]
    required = {str((M.parent.parent / x['path']).resolve()).casefold(): x['new_sha256'] for x in manifest['files']}
    required[str((TX / 'selection.json').resolve()).casefold()] = manifest['selection_sha256']
    required[str((TX / 'library_candidates.json').resolve()).casefold()] = manifest['library_selection_sha256']
    positive_dir = O / 'phase2-next-data-positive-v3'
    sources = source_hashes(normal_snapshot(Path(str(positive_dir) + '-freeze/inputs-before.json')))
    assert sources
    evidence_ids = {}
    for n, run, expected in zip(IDS, controls, HASHES):
        directory = O / ('phase2-next-data-' + n)
        assert base.sha(Path(run['exe']['path'])) == run['exe']['sha256'] == expected
        assert checker.check_control_logs(directory / 'build-summary.json', run) == ('pointer' if n == 'p2wp' else 'value')
        evidence_ids[n] = {'summary_sha256': base.sha(directory / 'build-summary.json'),
                           'actual_image_sha256': expected,
                           'independent_proof_sha256': base.sha(directory / 'evidence' / ('independent-' + n + '-proof.json'))}
    pe = Pe(paths.REF_IMAGE)
    for name in ('positive-v3', *IDS, 'repeat'):
        directory = O / ('phase2-next-data-' + name)
        freeze_dir = Path(str(directory) + '-freeze')
        freeze = base.load(freeze_dir / 'result.json')
        snapshot = normal_snapshot(freeze_dir / 'inputs-before.json')
        assert freeze['input_freeze_passed'] and freeze['command_rc'] == 0
        assert not freeze['final_digest_changes'] and not freeze['observed_metadata_changes']
        assert all(snapshot[k]['sha256'] == v for k, v in required.items())
        assert source_hashes(snapshot) == sources
        assert base.sha(directory / 'evidence/units.json') == manifest['accepted_epoch_recipe_sha256']
        if name in IDS:
            continue
        evidence = directory / 'evidence'
        run = base.load(directory / 'build-summary.json')
        verdict = base.load(directory / 'harness-verdict.json')
        errors = checker.check(run, baseline, controls, verdict) + checker.check_cell_state(verdict)
        errors += checker.check_recorded_config(run, baseline, controls, 'selection.json', list(IDS))
        errors += checker.check_selection_sha256(run, controls, manifest['selection_sha256'])
        errors += checker.check_library_consistency(run, controls, manifest['library_selection_sha256'])
        errors += checker.check_provenance(run, [('default', baseline)] + [('control', x) for x in controls])
        for label, x in [('positive', run)] + [('control', x) for x in controls]:
            errors += checker.check_extended_mode(x, label) + checker.check_weak_coff(x, label, '0', None, None)
        assert not errors, errors
        assert accepted_verdict(run['harness']['rc'], verdict, run['exe']['path'], run['harness']['tag'])
        assert base.sha(Path(run['exe']['path'])) == run['exe']['sha256'] == CANONICAL
        relocs = base.reloc(Path(run['exe']['path']))
        assert relocs == base.reloc(Path(baseline['exe']['path'])) and len(relocs) == 734884
        assert base.sha(evidence / 'selection.json') == manifest['selection_sha256']
        assert base.sha(evidence / 'library_candidates.json') == manifest['library_selection_sha256']
        assert base.sha(evidence / 'cost245_records.py') == manifest['files'][1]['new_sha256']
        for filename, digest in run['provenance']['data_v1_scratch_sha256'].items():
            assert base.sha(evidence / 'data-v1-scratch' / filename) == digest
        entries = base.load(evidence / 'm3_manifest.json')['entries']
        pieces = base.load(evidence / 'dv1_pieces.json')['pieces']
        assert len(entries) == 8268 and run['provenance']['m3']['dropped'] == 0
        library = [x for x in pieces if x.get('library_opt_in')]
        assert len(library) == 405 and sum(x['size'] for x in library) == 16730
        ranges, raw_bytes, tls_bytes = [], 0, 0
        for row in entries + pieces:
            raw = bytes.fromhex(row['ref'] if 'ref' in row else row['data'])
            assert row['size'] == len(raw)
            linked = bytearray(raw)
            sites = set()
            # DV1 stores unrelocated COFF bytes and already resolved original
            # target values. load_dv1 passes those targets with zero addend.
            for offset, target, addend in row.get('relocs', []):
                assert 0 <= offset <= len(raw) - 4 and not sites.intersection(range(offset, offset + 4))
                sites.update(range(offset, offset + 4))
                struct.pack_into('<I', linked, offset, target)
            assert linked == pe.read(row['va'], len(raw))
            ranges.append((row['va'], row['va'] + len(raw)))
            if row['section'] in ('.data', '.rdata'):
                raw_bytes += len(raw)
            else:
                assert row['section'] == '.tls'
                tls_bytes += len(raw)
        ranges.sort()
        assert all(a[1] <= b[0] for a, b in zip(ranges, ranges[1:]))
        assert raw_bytes == 1613010 and tls_bytes == 5
        units = base.load(evidence / 'units.json')['units']
        names = recipe_names(units)
        done, facts = [], []
        for index in (2, 998, 1111, 1112):
            spec = copy.deepcopy(units[index])
            if index == 2:
                key = '??1TESForm@@UAE@XZ'
                assert units[658]['symbols'][key] == units[973]['symbols'][key] == '0x00483630'
                spec['symbols'][key] = '0x00483630'
            obj = evidence / ('%04d.obj' % index)
            coff = Coff(str(obj))
            rows = compare(coff, pe, spec)
            assert all(x['verdict'] == 'match' for x in rows)
            sections, inferred, errors = eh_sections(coff, pe, spec, rows, names)
            assert not errors
            done.append({'eh_sections': sections, 'eh_inferred': {k: '0x%08x' % v for k, v in inferred.items()}})
            facts.append({'unit': index, 'object_sha256': base.sha(obj), 'strict_functions': len(rows)})
        tails, bad, inferred, _, conflicts = eh_tails([units[i] for i in (2, 998, 1111, 1112)], done, pe)
        assert len(tails) == 14 and not bad and not conflicts and sum(x['strict_functions'] for x in facts) == 235
        audit_files = ('data-artifact-audit.json', 'data-library-replay.json') if name == 'positive-v3' else ('independent-artifact-audit.json', 'independent-library-replay.json', 'independent-freeze-audit.json')
        report = {'status': 'PASS opt-in next-data positive/three-controls/repeat; eligible for guarded promotion',
                  'default_promoted': False, 'whole_phase2_complete': False,
                  'transaction_manifest_sha256': base.sha(TX / 'manifest.json'),
                  'recipe_sha256': manifest['accepted_epoch_recipe_sha256'],
                  'selection_sha256': manifest['selection_sha256'], 'library_sha256': manifest['library_selection_sha256'],
                  'run': name, 'summary_sha256': base.sha(directory / 'build-summary.json'),
                  'actual_image_sha256': CANONICAL, 'actual_relocation_sha256': hashlib.sha256(relocs).hexdigest(),
                  'actual_objects': facts, 'ordinary_eh_tails': len(tails), 'frozen_required_inputs': required,
                  'freeze_result_sha256': base.sha(freeze_dir / 'result.json'), 'matching_source_files': len(sources),
                  'independent_audits': {n: base.sha(evidence / n) for n in audit_files}, 'controls': evidence_ids,
                  'initialized_data_bytes': raw_bytes, 'tls_bytes_separate': tls_bytes, 'new_library_bytes': 10356,
                  'typed_source_view_bytes_within_old_coverage': 364, 'play_seconds': verdict['steps']['play_secs'],
                  'cells': [verdict['steps']['extended'][k] for k in ('cell_before_save', 'cell_after_coc', 'cell_after_load')]}
        (evidence / 'root-acceptance-review.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps({'run': name, 'status': report['status'], 'raw_bytes': raw_bytes, 'source_files': len(sources)}))

if __name__ == '__main__':
    main()
