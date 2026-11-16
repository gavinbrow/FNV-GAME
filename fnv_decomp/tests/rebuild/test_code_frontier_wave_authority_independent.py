"""Authored epoch, cache and negative-evidence routing tests; no private inputs."""
import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'tools/rebuild'), str(ROOT/'tests/rebuild')]
import code_frontier_wave as wave


def authored(count=3):
    providers, units, roots, groups = {}, {}, [], []
    for i in range(count):
        address = '0x0086beb0' if i == 0 else '0x%08x' % (0x400000+i*16)
        recipe = 'authored-wave-%d' % i
        provider = dict(recipe_id=recipe, object_sha256='%064x' % (i+1),
                        source_sha256='f'*64, symbol_index=i+1, section=3,
                        value=0, size=17, symbol='_authored_wave_%d' % i)
        name = wave.base.pool.canonical({k: provider[k] for k in ('recipe_id', 'object_sha256', 'symbol_index')})
        provider['planned_canonical_name'] = name
        providers[address] = provider
        units[recipe] = dict(recipe_index=i, object_sha256=provider['object_sha256'],
                             source_sha256=provider['source_sha256'])
        root = wave.prior.planner.root_record(address, provider, units)
        roots.append(root)
        groups.append(dict(symbol=name, classification='CODE', observed_roles=['code'],
                           original_bases=[address], original_targets=[address],
                           included_provenance_is_extraction_proof=False))
    authorities = []
    for kind, indices, epoch in [('cached-central', [0, 1], 'a'),
                                  ('cached-frontier', [2], 'b')]:
        observations = []
        for ordinal, i in enumerate(indices, 1):
            summary = dict(event='SINGLE_ROOT_OBSERVATION', roots=[roots[i]['original_address']],
                           recipe_id=roots[i]['recipe_id'], closure_observed=i != 1,
                           graph_observation_complete=True,
                           blocker_codes={} if i != 1 else {'OMITTED_INITIALIZED_DATA': 1},
                           record_sha256='%064x' % (100+i), certificate_sha256='%064x' % (200+i))
            if kind == 'cached-central': summary.update(lane=1, lane_record_ordinal=ordinal)
            else: summary['ordinal'] = ordinal
            observations.append(summary)
        authorities.append(dict(kind=kind, receipt_sha256=epoch*64, request_sha256=epoch*64,
                                requests=[roots[i] for i in indices],
                                receipt=dict(status='metadata-only', input_stability=True, request_sha256=epoch*64,
                                             optional_function_index_present=False, observations=observations)))
    report = dict(kind='actual-unresolved-LNK-target-groups', groups=groups,
                  classifications={'CODE': count}, executable_execution=False, runtime_eligible=False)
    return authorities, providers, units, report


def registry(values):
    return wave.cache_registry(*values[:3], expected_total=3)


class IndependentAuthorityTests(unittest.TestCase):
    def test_distinct_epochs_may_share_local_ordinal_without_merging_authority(self):
        values = authored(); result = registry(values)
        first = result['records']['0x0086beb0']['authority']
        third = result['records']['0x00400020']['authority']
        self.assertEqual(first['ordinal'], third['ordinal'])
        self.assertNotEqual(first['receipt_sha256'], third['receipt_sha256'])
        self.assertEqual(first['kind'], 'cached-central')
        self.assertEqual(third['kind'], 'cached-frontier')
        self.assertIsNone(first['contract_identity_sha256'])
        self.assertTrue(first['contract_identity_is_bound_through_record_hash'])
        self.assertFalse(result['code_emission_performed'])

    def test_negative_summary_with_partial_typed_annotation_is_never_promoted(self):
        values = authored(); summary = values[0][0]['receipt']['observations'][1]
        summary['composition'] = dict(composition_complete=True, remaining_blockers=[])
        summary['witness'] = dict(witness_complete=False, rows=[dict(approved=False)])
        before = copy.deepcopy(values)
        result = registry(values)
        saved = result['records'][summary['roots'][0]]['summary']
        self.assertFalse(saved['closure_observed'])
        self.assertEqual(saved['blocker_codes'], {'OMITTED_INITIALIZED_DATA': 1})
        self.assertEqual(values, before)

    def test_borrowed_physical_root_or_recipe_is_refused(self):
        for mutation in ('source', 'object', 'symbol', 'recipe'):
            values = authored(); source = values[0][0]
            if mutation == 'recipe': source['receipt']['observations'][0]['recipe_id'] = 'borrowed'
            else:
                field = dict(source='source_sha256', object='object_sha256', symbol='symbol_index')[mutation]
                source['requests'][0][field] = 999 if mutation == 'symbol' else 'e'*64
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): registry(values)

    def test_duplicate_root_across_epochs_is_fatal_even_if_evidence_matches(self):
        values = authored(); source = copy.deepcopy(values[0][0])
        source.update(receipt_sha256='c'*64, request_sha256='d'*64)
        values[0].append(source)
        with self.assertRaises(ValueError): registry(values)

    def test_incomplete_negative_and_fake_positive_are_refused(self):
        for mutation in ('negative-without-blocker', 'positive-with-blocker', 'incomplete-positive', 'boolean-state'):
            values = authored(); summary = values[0][0]['receipt']['observations'][1]
            if mutation == 'negative-without-blocker': summary['blocker_codes'] = {}
            elif mutation == 'positive-with-blocker': summary['closure_observed'] = True
            elif mutation == 'incomplete-positive': summary.update(closure_observed=True, graph_observation_complete=False, blocker_codes={})
            else: summary['closure_observed'] = 1
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): registry(values)

    def test_missing_or_duplicate_requested_view_is_refused(self):
        for mutation in ('missing', 'duplicate'):
            values = authored(); source = values[0][0]
            if mutation == 'missing': source['receipt']['observations'].pop()
            else: source['receipt']['observations'].append(copy.deepcopy(source['receipt']['observations'][0]))
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): registry(values)

    def test_hashes_and_locator_types_are_strict(self):
        mutations = [('receipt_sha256', '', None), ('request_sha256', 'not-a-hash', None),
                     ('record_sha256', 'g'*64, 'summary'), ('certificate_sha256', None, 'summary'),
                     ('lane', True, 'summary'), ('lane_record_ordinal', 0, 'summary'),
                     ('lane_record_ordinal', -1, 'summary')]
        for field, value, target in mutations:
            values = authored(); source = values[0][0]
            (source['receipt']['observations'][0] if target else source)[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError): registry(values)

    def test_one_epoch_cannot_reuse_a_locator_for_distinct_roots(self):
        values = authored(); observations = values[0][0]['receipt']['observations']
        observations[1]['lane_record_ordinal'] = observations[0]['lane_record_ordinal']
        with self.assertRaises(ValueError): registry(values)

    def test_valid_but_borrowed_request_hash_cannot_relabel_a_receipt_epoch(self):
        values = authored()
        values[0][0]['request_sha256'] = 'e'*64
        with self.assertRaises(ValueError): registry(values)

    def test_reference_group_quarantine_survives_positive_cache_and_negative_stays_negative(self):
        values = authored(249); registered = registry(values)
        quarantine = [dict(root=registered['records']['0x0086beb0']['root'],
                           blockers=[dict(code='CANONICAL_REFERENCE_GROUP_REQUIRES_REVIEWED_V2')])]
        result = wave.reconcile_v7(values[3], values[1], values[2], registered, set(), quarantine)
        by_address = {row['root']['original_address']: row for row in result['records']}
        self.assertEqual(by_address['0x0086beb0']['state'], 'PRESERVED_REFERENCE_GROUP_QUARANTINE')
        self.assertEqual(by_address['0x00400010']['state'], 'CACHED_ORIGINAL_OMISSION_BLOCKED')
        self.assertEqual(by_address['0x00400020']['state'], 'CACHED_BARE_POSITIVE_REQUIRES_FRESH_CLASSIFICATION')
        self.assertNotIn(quarantine[0]['root'], result['cached_positive_roots'])
        self.assertFalse(result['code_emission_performed'])

    def test_quarantine_cannot_be_hidden_in_prepared_names_without_new_proof(self):
        values = authored(249); registered = registry(values)
        root = registered['records']['0x0086beb0']['root']
        quarantine = [dict(root=root, blockers=[dict(code='CANONICAL_REFERENCE_GROUP_REQUIRES_REVIEWED_V2')])]
        name = wave.base.pool.canonical({k: root[k] for k in ('recipe_id', 'object_sha256', 'symbol_index')})
        with self.assertRaises(ValueError):
            wave.reconcile_v7(values[3], values[1], values[2], registered, {name}, quarantine)


if __name__ == '__main__': unittest.main()
