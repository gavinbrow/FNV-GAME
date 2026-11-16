"""Independent authored DATA/cache routing tests; no original inputs."""
import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'tools/rebuild'), str(ROOT/'tests/rebuild')]
import current_code_frontier as frontier
from test_ordinary_relocation_factory import planned_map


def context():
    data, choices, units, _, _ = planned_map()
    providers = data['providers']
    roots = [frontier.root_record(a, entry, units) for a, entry in sorted(providers.items())]
    summaries = [dict(event='SINGLE_ROOT_OBSERVATION', roots=[r['original_address']],
                      closure_observed=False, graph_observation_complete=False,
                      blocker_codes={'UNSUPPORTED_SECTION_SEMANTICS': 1}) for r in roots]
    groups = []
    for root in roots:
        identity = {key: root[key] for key in ('recipe_id','object_sha256','symbol_index')}
        groups.append(dict(symbol=frontier.base.pool.canonical(identity), classification='CODE',
                           observed_roles=['code'], included_provenance_is_extraction_proof=False,
                           original_bases=[root['original_address']], original_targets=[root['original_address']]))
    report = dict(kind='actual-unresolved-LNK-target-groups', executable_execution=False,
                  runtime_eligible=False, classifications={'CODE': 2}, groups=groups)
    return report, providers, units, {'observations': summaries}, roots


def reconcile(values, exclusions=()):
    return frontier.reconcile(*values, set(exclusions), expected_code_count=2)


class IndependentDataRoutingTests(unittest.TestCase):
    def test_prepared_negative_DATA_scope_is_skipped_without_promoting_other_negative(self):
        values = context()
        prepared_name = values[0]['groups'][0]['symbol']
        result = reconcile(values, [prepared_name])
        self.assertEqual(result['counts'], {'PREPARED_SKIP': 1, 'CACHED_ORIGINAL_OMISSION_BLOCKED': 1})
        self.assertEqual(result['cached_positive_roots'], [])
        self.assertEqual(result['new_roots'], [])

    def test_extra_composed_positive_metadata_cannot_relabel_negative_bare_observation(self):
        values = context()
        values[3]['observations'][0]['composed_omission_complete'] = True
        values[3]['observations'][0]['witness_complete'] = True
        result = reconcile(values)
        self.assertEqual(result['counts'], {'CACHED_ORIGINAL_OMISSION_BLOCKED': 2})
        self.assertEqual(result['cached_positive_roots'], [])

    def test_positive_bare_cache_is_only_a_fresh_classification_candidate(self):
        values = context()
        values[3]['observations'][0].update(closure_observed=True, graph_observation_complete=True, blocker_codes={})
        result = reconcile(values)
        self.assertEqual(len(result['cached_positive_roots']), 1)
        self.assertEqual(result['records'][0]['state'], 'CACHED_BARE_POSITIVE_REQUIRES_FRESH_CLASSIFICATION')
        self.assertTrue(result['eligibility_not_inferred_from_closure'])
        for key in ('original_objects_read','original_image_read','source_bodies_read','provider_selected','runtime_eligible'):
            self.assertIs(result[key], False)

    def test_new_selected_DATA_dependency_requires_its_own_observation(self):
        values = list(context())
        values[3]['observations'].pop()
        values[4].pop()
        result = reconcile(values)
        self.assertEqual(len(result['new_roots']), 1)
        self.assertEqual(result['cached_positive_roots'], [])
        self.assertEqual(result['records'][1]['state'], 'NEW_SELECTED_ROOT_REQUIRES_OBSERVATION')

    def test_stale_cached_source_identity_cannot_borrow_observation(self):
        values = copy.deepcopy(context())
        values[4][0]['source_sha256'] = 'f'*64
        with self.assertRaises(ValueError):
            reconcile(values)


if __name__ == '__main__':
    unittest.main()
