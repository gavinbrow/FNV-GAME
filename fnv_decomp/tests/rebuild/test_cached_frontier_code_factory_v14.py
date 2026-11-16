"""Synthetic V14 candidate-selection tests; no original inputs or production runs."""
import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools/rebuild'), str(ROOT / 'tests/rebuild')]
import cached_frontier_code_factory_v14 as factory
import test_cached_frontier_code_factory_v13 as fixtures


def fixture(**kwargs):
    with patch.object(fixtures, 'factory', factory):
        args = fixtures.fixture(**kwargs)
    args[0]['historical_registry_roots_reobserved'] = args[0].pop('historical_roots_reobserved')
    args[0].update(graph_observation_scope='physical primary symbols, section metadata, ordinary edges and SafeSEH including omitted relocations',
        graph_observation_excludes=['whole EH closure', 'HIGHLOW closure', 'raw-byte proof'],
        additional_source_and_object_stability_rehash_reads=True)
    epoch = args[4]
    epoch.pop('application_manifest_adopted')
    epoch.update(schema_version=9, policy_id='prepared-cached-V13-successor-v1',
                 application_selected_code_count=None, historical_records_preserved=True)
    for key in ('ABI_verified', 'admission_decision_created', 'certificate_created', 'closure_inferred',
                'code_emission_performed', 'emission_performed', 'full_serialization_eligible', 'link_ready',
                'materialization_approved', 'namespace_approved'):
        epoch[key] = False
    return args


def select(args):
    return factory.select_candidates(*args, expected_census=(2, 1, 3),
        expected_current_codes=2, expected_prepared=(0, 0), receipt_sha256='d'*64)


class V14SelectionTests(unittest.TestCase):
    def test_positive_singletons_only_preserve_inputs(self):
        args = fixture()
        before = copy.deepcopy(args)
        request, selected, ledger = select(args)
        self.assertEqual(args, before)
        self.assertEqual(len(request['roots']), 2)
        self.assertEqual(len(selected), 2)
        self.assertEqual(ledger[-1]['state'], 'RECIPE_UNION_EVIDENCE_ONLY')

    def test_negative_is_preserved(self):
        args = fixture(field=False, safeseh=True)
        request, _, ledger = select(args)
        self.assertEqual(len(request['roots']), 1)
        self.assertEqual(ledger[1]['state'], 'ORIGINAL_NEGATIVE_PRESERVED')

    def test_wrong_policy_rejected_even_if_receipt_resealed(self):
        args = fixture()
        args[1][0]['qualified_metadata_identity']['policy_id'] = 'old-policy'
        with patch.object(fixtures, 'factory', factory):
            fixtures.reseal(args[0], args[1])
        with self.assertRaises(ValueError):
            select(args)

    def test_omitted_observation_cannot_be_admitted(self):
        args = fixture()
        args[1].pop()
        with self.assertRaises(ValueError):
            select(args)

    def test_mutated_contract_cannot_be_resealed_as_observation(self):
        args = fixture()
        args[1][0]['contract']['export_policy'] = 'forged'
        with patch.object(fixtures, 'factory', factory):
            fixtures.reseal(args[0], args[1])
        with self.assertRaises(ValueError):
            select(args)

    def test_changed_certificate_cannot_validate_as_selected(self):
        args = fixture()
        _, selected, _ = select(args)
        record = copy.deepcopy(args[1][0])
        record['certificate']['blockers'] = ['invented']
        with self.assertRaises(ValueError):
            factory.validate_selected(record, selected[0])

    def test_operation_rejects_before_access(self):
        with self.assertRaisesRegex(ValueError, 'authority.*pending'):
            factory.validate_operation({'artifacts': {'source': '/must-not-open'}})

    def test_incomplete_tail_never_calls_callback(self):
        args = fixture()
        args[1].pop()
        calls = []
        with self.assertRaises(ValueError):
            factory.select_candidates(*args, expected_census=(2, 1, 3),
                expected_current_codes=2, expected_prepared=(0, 0), receipt_sha256='d'*64,
                on_selected=lambda *x: calls.append(x))
        self.assertEqual(calls, [])

    def test_callback_cannot_mutate_input_or_returned_selection(self):
        args = fixture()
        before = copy.deepcopy(args)
        def mutate(record, selection):
            record['requested_roots'][0]['symbol'] = 'changed'
            selection['root']['symbol'] = 'changed'
            selection['authority']['kind'] = 'changed'
        request, selected, _ = factory.select_candidates(*args, expected_census=(2, 1, 3),
            expected_current_codes=2, expected_prepared=(0, 0), receipt_sha256='d'*64,
            on_selected=mutate)
        self.assertEqual(args, before)
        self.assertNotEqual(request['roots'][0]['symbol'], 'changed')
        self.assertNotEqual(selected[0]['authority']['kind'], 'changed')

    def test_bool_counts_rejected(self):
        args = fixture()
        for census, current, prepared in [((True, 1, 3), 2, (0, 0)),
                ((2, 1, 3), True, (0, 0)), ((2, 1, 3), 2, (False, False))]:
            with self.subTest(census=census, current=current, prepared=prepared):
                with self.assertRaises(ValueError):
                    factory.select_candidates(*args, expected_census=census,
                        expected_current_codes=current, expected_prepared=prepared, receipt_sha256='d'*64)

    def test_string_base_list_and_invalid_root_rejected(self):
        args = fixture()
        args[3]['groups'][0]['original_bases'] = args[3]['groups'][0]['original_bases'][0]
        with self.assertRaises(ValueError):
            select(args)

    def test_schema_nine_prepared_epoch_remains_nonadmitting(self):
        args = fixture()
        epoch = args[4]
        self.assertEqual(len(select(args)[0]['roots']), 2)
        epoch['link_ready'] = True
        with self.assertRaises(ValueError):
            select(args)
        epoch['link_ready'] = False
        epoch['schema_version'] = 8
        with self.assertRaises(ValueError):
            select(args)
        epoch['application_manifest_adopted'] = False
        with self.assertRaises(ValueError):
            select(args)

    def test_receipt_scope_and_schema_are_not_promotion_claims(self):
        for key, value in [('schema_version', 99), ('graph_observation_excludes', []),
                           ('graph_observation_scope', 'complete'),
                           ('additional_source_and_object_stability_rehash_reads', False)]:
            args = fixture()
            args[0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                select(args)
        args = fixture()
        args[2]['roots'][0]['section'] = 0
        with self.assertRaises(ValueError):
            select(args)


if __name__ == '__main__':
    unittest.main()
