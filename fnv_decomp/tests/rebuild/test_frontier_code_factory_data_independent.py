"""Independent authored cache/new-source authority routing negatives."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'tools/rebuild'), str(ROOT/'tests/rebuild')]
import frontier_code_factory as factory
from test_current_code_frontier import fixture
from test_composed_relocation_projection_data_independent import authored_data


OLD_SHA = 'a'*64
NEW_SHA = 'b'*64


def authored_frontier():
    values = fixture()
    for i, summary in enumerate(values[3]['observations'], 1):
        summary.update(lane=1, lane_record_ordinal=i, certificate_sha256='c'*64,
                       recipe_id=values[1][summary['roots'][0]]['recipe_id'])
    frontier = factory.planner.reconcile(*values, expected_code_count=4)
    new_root = frontier['new_roots'][0]
    observed = dict(event='SINGLE_ROOT_OBSERVATION', roots=[new_root['original_address']],
                    recipe_id=new_root['recipe_id'],
                    closure_observed=True, graph_observation_complete=True, blocker_codes={},
                    ordinal=2, record_sha256='d'*64, certificate_sha256='e'*64)
    return frontier, dict(observations=[observed]), values[-1]


def candidates(values, old_sha=OLD_SHA, new_sha=NEW_SHA):
    frontier, observed, exclusions = values
    return factory.candidate_request(frontier, observed, old_sha, new_sha, exclusions)


class IndependentFrontierAuthorityTests(unittest.TestCase):
    def test_all_cached_and_new_positives_are_requested_without_sampling(self):
        values = authored_frontier()
        request, selected, ledger = candidates(values)
        self.assertEqual(len(request['roots']), 2)
        self.assertEqual(len(selected), 2)
        self.assertEqual(len(ledger), 4)
        self.assertEqual({s['authority']['kind'] for s in selected}, {'cached-central','new-frontier'})
        self.assertEqual({s['authority']['receipt_sha256'] for s in selected}, {OLD_SHA, NEW_SHA})

    def test_negative_cache_composition_flags_do_not_create_bare_authority(self):
        values = authored_frontier()
        negative = next(r for r in values[0]['records'] if r['state']=='CACHED_ORIGINAL_OMISSION_BLOCKED')
        negative['cached_observation'].update(composed_omission_complete=True, witness_complete=True)
        request, _, ledger = candidates(values)
        self.assertNotIn(negative['root'], request['roots'])
        self.assertTrue(any(r['status']=='CACHED_ORIGINAL_OMISSION_BLOCKED' for r in ledger))

    def test_borrowed_cached_root_or_union_observation_is_fatal(self):
        for mutation in ('root','event'):
            values = authored_frontier()
            cached = next(r for r in values[0]['records'] if r['state'].startswith('CACHED_BARE_POSITIVE'))
            if mutation == 'root': cached['cached_observation']['roots'] = [values[0]['new_roots'][0]['original_address']]
            else: cached['cached_observation']['event'] = 'RECIPE_ROOT_UNION_OBSERVATION'
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                candidates(values)

    def test_positive_flag_without_complete_graph_cannot_enter_request(self):
        for branch in ('cached','new'):
            values = authored_frontier()
            summary = values[1]['observations'][0] if branch=='new' else values[0]['records'][0]['cached_observation']
            summary['graph_observation_complete'] = False
            with self.subTest(branch=branch), self.assertRaises(ValueError):
                candidates(values)

    def test_contradictory_cached_state_cannot_silently_drop_a_positive_candidate(self):
        values = authored_frontier()
        summary = values[0]['records'][0]['cached_observation']
        summary.update(closure_observed=False, blocker_codes={'UNKNOWN_FRAME': 1})
        with self.assertRaises(ValueError):
            candidates(values)

    def test_new_root_cannot_borrow_another_source_identity(self):
        values = authored_frontier()
        fresh = next(r for r in values[0]['records'] if r['state']=='NEW_SELECTED_ROOT_REQUIRES_OBSERVATION')
        fresh['root'] = dict(fresh['root'], source_sha256='1'*64)
        with self.assertRaises(ValueError):
            candidates(values)

    def test_duplicate_new_request_or_missing_new_outcome_is_fatal(self):
        for mutation in ('duplicate','missing'):
            values = authored_frontier()
            if mutation == 'duplicate': values[0]['new_roots'].append(copy.deepcopy(values[0]['new_roots'][0]))
            else: values[1]['observations'] = []
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                candidates(values)

    def test_new_negative_is_preserved_without_composed_promotion(self):
        values = authored_frontier()
        values[1]['observations'][0].update(closure_observed=False, blocker_codes={'DATA_OMISSION_BLOCKED': 1},
                                           composed_omission_complete=True)
        request, _, ledger = candidates(values)
        self.assertEqual(len(request['roots']), 1)
        self.assertEqual(sum(r['status']=='NEW_ORIGINAL_OMISSION_BLOCKED' for r in ledger), 1)

    def test_prepared_skip_must_be_in_current_exclusions(self):
        values = authored_frontier()
        values[0]['records'][0]['state'] = 'PREPARED_SKIP'
        from collections import Counter
        values[0]['counts'] = dict(Counter(r['state'] for r in values[0]['records']))
        with self.assertRaises(ValueError):
            candidates(values)

    def test_original_negative_DATA_cannot_use_bare_verification_route(self):
        raw, contract, negative, _, composed, roots, providers = authored_data()
        row = dict(contract=contract, certificate=negative, requested_roots=roots,
                   witness_complete=True, composed_certificate=composed)
        with tempfile.TemporaryDirectory() as td:
            with patch.object(factory.fields,'verify_member') as fields_consumer, patch.object(factory.base,'project_member') as zero_consumer:
                with self.assertRaises(ValueError):
                    factory.verify_candidate(raw,row,roots[0],providers,set(),Path(td)/'original.obj',
                                             Path(td)/'stage.obj',object(),{})
                fields_consumer.assert_not_called()
                zero_consumer.assert_not_called()


if __name__ == '__main__':
    unittest.main()
