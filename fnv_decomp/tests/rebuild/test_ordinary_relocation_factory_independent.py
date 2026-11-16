"""Independent synthetic factory boundaries; no game bytes or native tools."""
import copy
import hashlib
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools/rebuild'), str(ROOT / 'tests/rebuild')]
import ordinary_relocation_factory as factory
import ordinary_relocation_projection as core
import coff_code_archive as coff
from test_ordinary_relocation_projection_independent import authored
from test_scalableordinary_root_collect import fixture as context_fixture


def export_ledgers():
    """Full-sized invented names, independent of every production namespace."""
    names = ['_fnv_code_' + hashlib.sha256(('authored-export-%d' % n).encode()).hexdigest()
             for n in range(14326)]
    def distribute(values, count):
        return [dict(exports=values[n::count]) for n in range(count)]
    first = [dict(projection=dict(exports=[name])) for name in names[14318:]]
    return (distribute(names[:12946], 1019), distribute(names[12946:14318], 185), first), set(names)


def provider_context():
    raw, unit, proof, roots, selections, providers, _ = context_fixture()
    expanded = {}
    for root in roots:
        identity = {k: root[k] for k in ('recipe_id', 'object_sha256', 'symbol_index')}
        expanded[root['original_address']] = dict(identity, **{k: root[k] for k in
            ('source_sha256', 'section', 'value', 'size', 'symbol')},
            planned_canonical_name=factory.base.pool.canonical(identity))
    events = {'AUTHORED_OWNER_EVENT': 2}
    data = dict(schema_version=1, policy_id='selected-physical-provider-map-v1', kind='typed-provider-map',
        providers=expanded, census=dict(events=events, sequence_sha256=factory.OWNER_SEQUENCE,
                                        selected_owners=len(selections)),
        provider_identity_is_planned_namespace=True, materialized_exports=0,
        inputs=copy.deepcopy(factory.MAP_INPUTS), producer_sha256=factory.MAP_PRODUCER,
        input_stability=True, optional_function_index_present=False,
        **{key: False for key in factory.MAP_FALSE})
    return data, selections, {unit['recipe_id']: unit}, {proof['recipe_id']: proof}, dict(summary=dict(events=events))


def coverage_triplet(status='HISTORICAL_BLOCKED', prepared=None, ordinal=3):
    root = authored()[3][0]
    original = dict(original_address=root['original_address'], status=status,
                    physical_identity={k: root[k] for k in ('recipe_id', 'object_sha256', 'symbol_index')},
                    selected_native={k: root[k] for k in factory.base.NATIVE_KEYS},
                    retained_original_evidence={'authored': True})
    old_to_union = {'EMITTED': 'UPSTREAM_EMITTED_UNCHANGED', 'BLOCKED_UNION': 'STILL_UNION_BLOCKED',
                    'HISTORICAL_BLOCKED': 'UPSTREAM_HISTORICAL_BLOCKED'}
    union = dict(original_address=root['original_address'], physical_identity=copy.deepcopy(original['physical_identity']),
                 original_status=status, original_coverage_row=dict(ordinal=ordinal, sha256=factory.digest(original)),
                 status='NEW_UNION_V3_PROJECTED' if prepared == 'union' else old_to_union[status])
    first = dict(copy.deepcopy(original), baseline_status_preserved=True,
                 ordinary_projection_status='EMITTED_ORDINARY_NO_RELOCATION' if prepared == 'first8' else 'NOT_REQUESTED')
    return original, union, first, ordinal


class IndependentFactoryTests(unittest.TestCase):
    def test_full_export_census_three_disjoint_generations(self):
        ledgers, expected = export_ledgers()
        result = factory.combine_exports(*ledgers)
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 14326)

    def test_export_census_rejects_missing_duplicate_foreign_and_wrong_shape(self):
        for change in ('missing-row', 'missing-export', 'cross-generation-duplicate', 'foreign-name'):
            ledgers, _ = export_ledgers()
            if change == 'missing-row': ledgers[0].pop()
            elif change == 'missing-export': ledgers[1][0]['exports'].pop()
            elif change == 'cross-generation-duplicate':
                ledgers[2][0]['projection']['exports'][0] = ledgers[0][0]['exports'][0]
            else: ledgers[2][0]['projection']['exports'][0] = '_unreviewed_foreign_provider'
            with self.subTest(change=change), self.assertRaises(ValueError):
                factory.combine_exports(*ledgers)

    def test_project_stage_is_exclusive_and_preserves_old_target_addend(self):
        values = authored(classes=('ORIGINAL_IMAGE_DATA_REQUIRES_CANONICAL_OWNER',), kinds=(6,), addends=(4,))
        with tempfile.TemporaryDirectory() as td:
            stage = Path(td) / 'authored.stage.obj'
            output, receipt = factory.project_and_verify(*values, set(), stage)
            self.assertEqual(stage.read_bytes(), output)
            obj = coff.parse(output)
            text = next(s for s in obj['sections'].values() if s['name'] == '.text')
            self.assertEqual(text['payload'], coff.parse(values[0])['sections'][1]['payload'])
            self.assertEqual(len(text['relocs']), 1)
            self.assertFalse(receipt['runtime_eligible'])
            recovered = coff.read_archive(coff.archive([('authored.obj', output)]))
            self.assertEqual(recovered['members'], [('authored.obj', output)])
            recovered_path = Path(td) / 'recovered-authored.obj'
            recovered_path.write_bytes(recovered['members'][0][1])
            factory.base.bulk.strict_reparse(recovered_path, output)
            self.assertEqual(coff.parse(recovered_path.read_bytes())['sections'], obj['sections'])
            with self.assertRaises(FileExistsError):
                factory.project_and_verify(*values, set(), stage)
            self.assertEqual(stage.read_bytes(), output)

    def test_corrupt_proof_or_serialization_is_not_a_normal_quarantine(self):
        values = list(authored())
        values[1]['fields'][0]['original_operand'] = 123
        with tempfile.TemporaryDirectory() as td:
            stage = Path(td) / 'never-published.obj'
            with self.assertRaises(ValueError): factory.project_and_verify(*values, set(), stage)
            self.assertFalse(stage.exists())

    def test_fresh_projection_is_not_replaced_by_a_cached_assessment(self):
        values = authored()
        with tempfile.TemporaryDirectory() as td:
            stage = Path(td) / 'never-published.obj'
            with patch.object(core, 'project_member', side_effect=ValueError('fresh replay refused')):
                with self.assertRaisesRegex(ValueError, 'fresh replay refused'):
                    factory.project_and_verify(*values, set(), stage)
            self.assertFalse(stage.exists())

    def test_independent_stage_parse_failure_propagates_without_receipt(self):
        values = authored()
        with tempfile.TemporaryDirectory() as td:
            stage = Path(td) / 'rejected-stage.obj'
            with patch.object(factory.base.bulk, 'strict_reparse', side_effect=ValueError('independent reader refused')):
                with self.assertRaisesRegex(ValueError, 'independent reader refused'):
                    factory.project_and_verify(*values, set(), stage)
            self.assertTrue(stage.exists())  # Retained failed-stage evidence, never a success receipt.
            self.assertFalse((Path(td) / 'receipt.json').exists())

    def test_comparison_gates_surround_fresh_projection_and_independent_parse(self):
        values = authored()
        events = []
        real_project = core.project_member
        real_parse = factory.base.bulk.strict_reparse
        with tempfile.TemporaryDirectory() as td:
            original, stage = Path(td) / 'original.obj', Path(td) / 'stage.obj'
            original.write_bytes(values[0])
            def compare(path, pe, contracts, recipe, plan=None):
                events.append('after' if plan else 'before')
                self.assertEqual(path, stage if plan else original)
                self.assertEqual(contracts[0]['selected']['symbol_index'], 2)
                if plan:
                    self.assertTrue(stage.exists())
                    self.assertTrue(plan['bindings'])
                    self.assertTrue(plan['comparison_base_view'])
                else: self.assertFalse(stage.exists())
                return [dict(authored_comparison='after' if plan else 'before')]
            def project(*args, **kwargs):
                events.append('fresh-core')
                return real_project(*args, **kwargs)
            def independent(*args, **kwargs):
                events.append('independent-reader')
                return real_parse(*args, **kwargs)
            with patch.object(factory.base.bulk, 'compare_functions', side_effect=compare), \
                 patch.object(core, 'project_member', side_effect=project), \
                 patch.object(factory.base.bulk, 'strict_reparse', side_effect=independent):
                output, receipt = factory.verify_member(*values, set(), original, stage, object(), {})
            self.assertEqual(events, ['before', 'fresh-core', 'independent-reader', 'after'])
            self.assertEqual(stage.read_bytes(), output)
            self.assertEqual(receipt['before_comparison'], [dict(authored_comparison='before')])
            self.assertEqual(receipt['after_comparison'], [dict(authored_comparison='after')])

    def test_before_or_after_comparison_failure_cannot_return_success(self):
        values = authored()
        for fail_at in (1, 2):
            with self.subTest(fail_at=fail_at), tempfile.TemporaryDirectory() as td:
                original, stage = Path(td) / 'original.obj', Path(td) / 'stage.obj'
                original.write_bytes(values[0]); calls = []
                def compare(*args, **kwargs):
                    calls.append(1)
                    if len(calls) == fail_at: raise ValueError('unchanged comparator rejected')
                    return [dict(authored_comparison='match')]
                with patch.object(factory.base.bulk, 'compare_functions', side_effect=compare):
                    with self.assertRaisesRegex(ValueError, 'unchanged comparator rejected'):
                        factory.verify_member(*values, set(), original, stage, object(), {})
                self.assertEqual(stage.exists(), fail_at == 2)
                self.assertEqual(len(calls), fail_at)
                self.assertFalse((Path(td) / 'receipt.json').exists())

    def test_factory_terminal_publication_failure_rolls_back_only_its_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            directory = Path(td)
            preserved = directory / 'unrelated-evidence'
            preserved.write_text('keep')
            checks = []
            def stable(_):
                checks.append(1)
                if len(checks) == 3: raise ValueError('post-publication integrity drift')
            with (directory / 'progress.jsonl').open('w') as journal, \
                 patch.object(factory.base, 'stable', side_effect=stable), \
                 patch.object(factory.base, 'budget', return_value={}):
                with self.assertRaisesRegex(ValueError, 'post-publication integrity drift'):
                    factory.base.finalize_success(directory, dict(emitted=1, blocked=0), {},
                                                  time.monotonic(), journal, lambda *a, **k: None)
                self.assertTrue(journal.closed)
            self.assertFalse((directory / 'receipt.json').exists())
            self.assertTrue((directory / 'receipt.pending.json').exists())
            self.assertEqual(preserved.read_text(), 'keep')

    def test_complete_planned_provider_context_joins_all_selected_native_proofs(self):
        context = provider_context()
        result = factory.validate_provider_map(*context)
        self.assertEqual(set(result), set(context[1]))
        self.assertEqual(len(result), 2)
        self.assertTrue(all(set(identity) == {'recipe_id', 'object_sha256', 'symbol_index'}
                            for identity in result.values()))

    def test_missing_provider_and_promoted_or_stale_map_are_fatal(self):
        for change in ('missing', 'extra-address', 'producer', 'inputs', 'sequence', 'promoted',
                       'materialized', 'optional-index', 'planned-name', 'source', 'bool-index', 'native-section'):
            context = copy.deepcopy(provider_context())
            data = context[0]
            first = next(iter(data['providers']))
            entry = data['providers'][first]
            if change == 'missing': data['providers'].pop(first)
            elif change == 'extra-address': data['providers']['0x00ffffff'] = copy.deepcopy(entry)
            elif change == 'producer': data['producer_sha256'] = 'f' * 64
            elif change == 'inputs': data['inputs']['owners'] = 'f' * 64
            elif change == 'sequence': data['census']['sequence_sha256'] = 'f' * 64
            elif change == 'promoted': data['provider_selected'] = True
            elif change == 'materialized': data['materialized_exports'] = 1
            elif change == 'optional-index': data['optional_function_index_present'] = True
            elif change == 'planned-name': entry['planned_canonical_name'] = '_fnv_code_' + 'f' * 64
            elif change == 'source': entry['source_sha256'] = 'f' * 64
            elif change == 'bool-index': entry['symbol_index'] = True
            else: entry['section'] += 1
            with self.subTest(change=change), self.assertRaises(ValueError):
                factory.validate_provider_map(*context)

    def test_provider_context_requires_native_match_and_current_source(self):
        for key, value in (('verdict', 'mismatch'), ('source_sha256_current', 'f' * 64)):
            context = copy.deepcopy(provider_context())
            proof = next(iter(context[3].values()))
            if key == 'verdict': proof['verified_functions'][0][key] = value
            else: proof[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError): factory.validate_provider_map(*context)

    def test_coverage_states_preserve_three_disjoint_generations(self):
        for status, prepared, expected in (
            ('EMITTED', None, 'BASELINE_PREPARED'), ('BLOCKED_UNION', 'union', 'UNION_V3_PREPARED'),
            ('HISTORICAL_BLOCKED', 'first8', 'FIRST8_PREPARED'), ('HISTORICAL_BLOCKED', None, 'UNPREPARED')):
            with self.subTest(status=status, prepared=prepared):
                self.assertEqual(factory.check_coverage_triplet(*coverage_triplet(status, prepared)), expected)

    def test_coverage_stale_geometry_row_digest_and_leaf_mutation_are_fatal(self):
        for change in ('address', 'physical', 'ordinal', 'digest', 'leaf-copy', 'unknown-state',
                       'union-replace-baseline', 'first8-replace-union'):
            status = 'EMITTED' if change == 'union-replace-baseline' else 'BLOCKED_UNION' if change == 'first8-replace-union' else 'HISTORICAL_BLOCKED'
            values = list(coverage_triplet(status))
            if change == 'address': values[1]['original_address'] = '0x00ffffff'
            elif change == 'physical': values[1]['physical_identity']['symbol_index'] += 1
            elif change == 'ordinal': values[1]['original_coverage_row']['ordinal'] += 1
            elif change == 'digest': values[1]['original_coverage_row']['sha256'] = 'f' * 64
            elif change == 'leaf-copy': values[2]['retained_original_evidence']['authored'] = False
            elif change == 'unknown-state': values[1]['status'] = 'UNKNOWN_OWNER'
            elif change == 'union-replace-baseline': values[1]['status'] = 'NEW_UNION_V3_PROJECTED'
            else: values[2]['ordinary_projection_status'] = 'EMITTED_ORDINARY_NO_RELOCATION'
            with self.subTest(change=change), self.assertRaises(ValueError):
                factory.check_coverage_triplet(*values)


if __name__ == '__main__':
    unittest.main()
