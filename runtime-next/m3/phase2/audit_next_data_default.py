"""Verify the promoted default using actual archived artifacts and ordinary oracles."""
import copy
import hashlib
import json
import struct
from pathlib import Path
import audit_next_data_optin as opt
import run_frozen
from compare import Coff, Pe, compare
from build_and_match import recipe_names, eh_sections, eh_tails
from harness_evidence import accepted_verdict
import verify_saved_runs as checker
import paths

def main():
    a, O = opt.base, opt.O
    directory = O / 'phase2-next-data-default-verified'
    evidence = directory / 'evidence'
    freeze_dir = Path(str(directory) + '-freeze')
    run = a.load(directory / 'build-summary.json')
    verdict = a.load(directory / 'harness-verdict.json')
    data = a.load(opt.TX / 'manifest.json')
    promotion = a.load(O / 'phase2-next-data-promotion-private/manifest.final.json')
    controls = [a.load(O / ('phase2-next-data-' + n + '/build-summary.json')) for n in opt.IDS]
    baseline = a.load(O / 'batch8-baseline/build-summary.json')
    errors = checker.check(run, baseline, controls, verdict) + checker.check_cell_state(verdict)
    errors += checker.check_recorded_config(run, baseline, controls, 'selection.json', list(opt.IDS))
    errors += checker.check_selection_sha256(run, controls, data['selection_sha256'])
    errors += checker.check_library_consistency(run, controls, data['library_selection_sha256'])
    errors += checker.check_provenance(run, [('default', baseline)] + [('control', x) for x in controls])
    for label, item in [('default', run)] + [('control', x) for x in controls]:
        errors += checker.check_extended_mode(item, label) + checker.check_weak_coff(item, label, '0', None, None)
    assert not errors, errors
    assert accepted_verdict(run['harness']['rc'], verdict, run['exe']['path'], run['harness']['tag'])
    assert a.sha(Path(run['exe']['path'])) == run['exe']['sha256'] == opt.CANONICAL
    relocs = a.reloc(Path(run['exe']['path']))
    assert len(relocs) == 734884 and relocs == a.reloc(Path(baseline['exe']['path']))
    assert a.load(freeze_dir / 'command.json')['build_environment'] == {}
    freeze = a.load(freeze_dir / 'result.json')
    assert freeze['command_rc'] == 0 and freeze['input_freeze_passed']
    assert not freeze['final_digest_changes'] and not freeze['observed_metadata_changes']
    snapshot = opt.normal_snapshot(freeze_dir / 'inputs-before.json')
    root = opt.M.parent.parent
    required = {str((root / x['path']).resolve()).casefold(): x['new_sha256'] for x in data['files'] + promotion['files']}
    assert len(required) == 10 and all(snapshot[k]['sha256'] == v for k, v in required.items())
    assert (opt.M / 'phase2/cost245_records.py').resolve() in {p.resolve() for p in run_frozen.paths_to_watch(root, [])}
    old = opt.normal_snapshot(O / 'phase2-next-data-positive-v3-freeze/inputs-before.json')
    assert opt.source_hashes(snapshot) == opt.source_hashes(old)
    assert a.sha(evidence / 'units.json') == data['accepted_epoch_recipe_sha256']
    assert a.sha(evidence / 'selection.json') == data['selection_sha256']
    assert a.sha(evidence / 'library_candidates.json') == data['library_selection_sha256']
    assert a.sha(evidence / 'cost245_records.py') == data['files'][1]['new_sha256']
    for filename, digest in run['provenance']['data_v1_scratch_sha256'].items():
        assert a.sha(evidence / 'data-v1-scratch' / filename) == digest
    pe = Pe(paths.REF_IMAGE)
    entries = a.load(evidence / 'm3_manifest.json')['entries']
    pieces = a.load(evidence / 'dv1_pieces.json')['pieces']
    assert len(entries) == 8268 and run['provenance']['m3']['dropped'] == 0
    lib = [x for x in pieces if x.get('library_opt_in')]
    assert len(lib) == 405 and sum(x['size'] for x in lib) == 16730
    ranges, total, tls = [], 0, 0
    for item in entries + pieces:
        raw = bytearray.fromhex(item['ref'] if 'ref' in item else item['data'])
        assert len(raw) == item['size']
        for off, target, addend in item.get('relocs', []):
            assert 0 <= off <= len(raw) - 4
            struct.pack_into('<I', raw, off, target)
        assert raw == pe.read(item['va'], len(raw))
        ranges.append((item['va'], item['va'] + len(raw)))
        if item['section'] in ('.data', '.rdata'):
            total += len(raw)
        else:
            assert item['section'] == '.tls'
            tls += len(raw)
    ranges.sort()
    assert all(a[1] <= b[0] for a, b in zip(ranges, ranges[1:]))
    assert total == 1613010 and tls == 5
    units = a.load(evidence / 'units.json')['units']
    names = recipe_names(units)
    done, objects = [], []
    for index in (2, 998, 1111, 1112):
        spec = copy.deepcopy(units[index])
        if index == 2:
            key = '??1TESForm@@UAE@XZ'
            assert units[658]['symbols'][key] == units[973]['symbols'][key] == '0x00483630'
            spec['symbols'][key] = '0x00483630'
        path = evidence / ('%04d.obj' % index)
        coff = Coff(str(path))
        rows = compare(coff, pe, spec)
        assert all(x['verdict'] == 'match' for x in rows)
        sections, inferred, errors = eh_sections(coff, pe, spec, rows, names)
        assert not errors
        done.append({'eh_sections': sections, 'eh_inferred': {k: '0x%08x' % v for k, v in inferred.items()}})
        objects.append({'unit': index, 'object_sha256': a.sha(path), 'functions': len(rows)})
    tails, bad, inferred, _, conflicts = eh_tails([units[i] for i in (2, 998, 1111, 1112)], done, pe)
    assert len(tails) == 14 and not bad and not conflicts and sum(x['functions'] for x in objects) == 235
    report = {'status': 'PASS fresh no-overrides promoted default', 'whole_phase2_complete': False,
              'recipe_sha256': data['accepted_epoch_recipe_sha256'], 'selection_sha256': data['selection_sha256'],
              'library_sha256': data['library_selection_sha256'], 'actual_image_sha256': opt.CANONICAL,
              'actual_relocation_sha256': hashlib.sha256(relocs).hexdigest(), 'actual_objects': objects,
              'ordinary_eh_tails': len(tails), 'required_frozen_inputs': required, 'build_environment': {},
              'source_files_equal_optin': len(opt.source_hashes(snapshot)), 'automatic_cost_watch_evaluated': True,
              'coverage_bytes': total, 'tls_bytes_separate': tls, 'new_library_bytes': 10356,
              'typed_source_view_bytes_within_existing_coverage': 364,
              'independent_audits': {n: a.sha(evidence / n) for n in ('independent-artifact-audit.json', 'independent-library-replay.json', 'independent-freeze-audit.json')},
              'harness_tag': run['harness']['tag'], 'play_seconds': verdict['steps']['play_secs'],
              'cells': [verdict['steps']['extended'][k] for k in ('cell_before_save', 'cell_after_coc', 'cell_after_load')]}
    (evidence / 'root-default-review.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('status', 'coverage_bytes', 'ordinary_eh_tails', 'source_files_equal_optin')}))

if __name__ == '__main__':
    main()
