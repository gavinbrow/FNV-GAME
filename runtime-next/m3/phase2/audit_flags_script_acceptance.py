"""Replay actual saved files for the bounded TESForm/script source batch."""
import copy
import hashlib
import json
from pathlib import Path
import audit_native_methods_acceptance as base
from compare import Coff, Pe, compare
from build_and_match import recipe_names, eh_sections, eh_tails
from harness_evidence import accepted_verdict
import paths
import verify_saved_runs as checker
import class_metadata_compare as metadata

M = Path(__file__).resolve().parent.parent
O = M / 'out'
RECIPE = '6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
SELECTION = '2dc3eb28083648d0d701268d8aa858a4d90fddd45e6ffb2613073cbb83672045'
LIBRARY = 'da19c0a782f6ba4ac986e992daf4af7ed67c282d0b70f35e8804a22227bce645'
CANONICAL = 'c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f'

def main():
    baseline = base.load(O / 'batch8-baseline/build-summary.json')
    controls = [base.load(O / ('phase2-flags-script-' + n + '/build-summary.json')) for n in ('p2av', 'p2wp')]
    assert {checker.check_control_logs(O / ('phase2-flags-script-' + n + '/build-summary.json'), r)
            for n, r in zip(('p2av', 'p2wp'), controls)} == {'value', 'pointer'}
    control_hashes = [base.sha(Path(x['exe']['path'])) for x in controls]
    assert control_hashes == ['a8cc4e724cd6b9a7bfbcbae046a6ad2058383555e05d006d1788ef464a069b6b',
                              'f60aab12eb29c7ad62b9097a287e61c1710fdcfb4a46aa27fc2959dee5249a60']
    for n, control in zip(('p2av', 'p2wp'), controls):
        directory = O / ('phase2-flags-script-' + n)
        freeze = base.load(Path(str(directory) + '-freeze/result.json'))
        assert freeze['input_freeze_passed'] and freeze['command_rc'] == 0
        assert not freeze['final_digest_changes'] and not freeze['observed_metadata_changes']
        assert base.sha(directory / 'evidence/units.json') == RECIPE
        proof = base.load(directory / 'evidence/root-control-review.json')
        assert proof['status'].startswith('PASS') and proof['image_sha256'] == control['exe']['sha256']
    pe = Pe(paths.REF_IMAGE)
    census = base.load(O / 'phase2-class-census/census-6757.json')
    assert census['inputs']['units_sha256'] == RECIPE
    for name, suffix in (('positive', '-freeze-v2'), ('repeat', '-freeze')):
        directory = O / ('phase2-flags-script-' + name)
        evidence = directory / 'evidence'
        run = base.load(directory / 'build-summary.json')
        verdict = base.load(directory / 'harness-verdict.json')
        assert not checker.check(run, baseline, controls, verdict)
        assert not checker.check_cell_state(verdict)
        assert not checker.check_selection_sha256(run, controls, SELECTION)
        assert not checker.check_library_consistency(run, controls, LIBRARY)
        assert not checker.check_recorded_config(run, baseline, controls, 'selection.json', ['p2av', 'p2wp'])
        assert not checker.check_provenance(run, [('default', baseline)] + [('control', x) for x in controls])
        for label, x in [('positive', run)] + [('control', x) for x in controls]:
            assert not checker.check_extended_mode(x, label)
            assert not checker.check_weak_coff(x, label, '0', None, None)
        assert accepted_verdict(run['harness']['rc'], verdict, run['exe']['path'], run['harness']['tag'])
        assert base.sha(Path(run['exe']['path'])) == run['exe']['sha256'] == CANONICAL
        relocs = base.reloc(Path(run['exe']['path']))
        assert relocs == base.reloc(Path(baseline['exe']['path'])) and len(relocs) == 734884
        freeze = base.load(Path(str(directory) + suffix) / 'result.json')
        assert freeze['command_rc'] == 0 and freeze['input_freeze_passed']
        assert not freeze['final_digest_changes'] and not freeze['observed_metadata_changes']
        assert base.load(Path(str(directory) + suffix) / 'command.json')['build_environment'] in ({}, {'FNV_COFF_WEAK': '0'})
        for filename, digest in run['provenance']['data_v1_scratch_sha256'].items():
            assert base.sha(evidence / 'data-v1-scratch' / filename) == digest
        assert base.sha(evidence / 'units.json') == RECIPE
        assert base.sha(evidence / 'selection.json') == SELECTION
        assert base.sha(evidence / 'library_candidates.json') == LIBRARY
        units = base.load(evidence / 'units.json')['units']
        names = recipe_names(units)
        facts, done, folds = [], [], []
        for index in (2, 998, 1111, 1112):
            unit = units[index]
            spec = copy.deepcopy(unit)
            if index == 2:
                symbol = '??1TESForm@@UAE@XZ'
                assert units[658]['symbols'][symbol] == units[973]['symbols'][symbol] == '0x00483630'
                spec['symbols'][symbol] = '0x00483630'
            obj = evidence / ('%04d.obj' % index)
            coff = Coff(str(obj))
            rows = compare(coff, pe, spec)
            assert len(rows) == len(unit['functions']) and all(x['verdict'] == 'match' for x in rows)
            sections, inferred, errors = eh_sections(coff, pe, spec, rows, names)
            assert not errors
            done.append({'eh_sections': sections, 'eh_inferred': {k: '0x%08x' % v for k, v in inferred.items()}})
            for fn in unit['functions']:
                for alias in fn.get('fold_aliases', []):
                    alias_spec = copy.deepcopy(spec)
                    alias_spec['functions'] = [dict(fn, symbol=alias, fold_aliases=[])]
                    assert all(x['verdict'] == 'match' for x in compare(coff, pe, alias_spec))
                    folds.append({'address': fn['address'], 'alias': alias})
            facts.append({'unit': index, 'object_sha256': base.sha(obj), 'functions': len(rows), 'eh_sections': len(sections)})
        tails, bad, inferred, _, conflicts = eh_tails([units[i] for i in (2, 998, 1111, 1112)], done, pe)
        assert len(tails) == 14 and not bad and not conflicts and sum(x['functions'] for x in facts) == 235
        graph = metadata.compare_class(evidence / '0002.obj', units[2], units, census, '.?AVBGSEncounterZone@@')
        assert len(graph['tables']) == 1
        table = graph['tables'][0]
        assert table['graph_fields_equal'] and len(table['slots']) == 78
        assert sum(x['match'] for x in table['slots']) == 33
        assert all(table['slots'][i]['match'] for i in (39, 40, 41, 42, 52, 53, 54))
        report = {'status': 'PASS bounded flags/script source batch', 'whole_phase2_complete': False,
                  'recipe_sha256': RECIPE, 'actual_image_sha256': CANONICAL,
                  'relocation_bytes': len(relocs), 'relocation_sha256': hashlib.sha256(relocs).hexdigest(),
                  'actual_objects': facts, 'fold_aliases': folds, 'ordinary_eh_tails': len(tails),
                  'class_metadata': graph,
                  'harness_tag': run['harness']['tag'], 'play_seconds': verdict['steps']['play_secs'],
                  'cells': [verdict['steps']['extended'][k] for k in ('cell_before_save', 'cell_after_coc', 'cell_after_load')],
                  'recoveries': verdict.get('recoveries', []), 'frozen_files': freeze['watched_files'],
                  'controls_actual_hashes': control_hashes, 'initialized_data_bytes': 1602654, 'new_raw_coverage_bytes': 0}
        (evidence / 'root-acceptance-review.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps({'run': name, 'status': report['status'], 'functions': 235, 'eh_tails': len(tails)}))

if __name__ == '__main__':
    main()
