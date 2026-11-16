"""Independent authored actual-DATA-envelope joins; no saved private inputs."""
import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'tools/rebuild'), str(ROOT/'tests/rebuild')]
from test_composed_relocation_projection_data_independent import authored_data
import composed_relocation_factory as factory


def authored_envelope(two_sections=False):
    raw, contract, negative, witnesses, composed, roots, providers = authored_data(two_sections=two_sections)
    witness = witnesses[0]
    original_record = dict(event='SINGLE_ROOT_OBSERVATION', recipe_id=roots[0]['recipe_id'],
                           requested_roots=roots, contract=contract, certificate=negative)
    record_sha = factory.digest(original_record)
    row = dict(lane=5, ordinal=2, event=original_record['event'], recipe_id=original_record['recipe_id'],
               requested_roots=roots, central_record_sha256=record_sha,
               contract_identity_sha256=factory.digest(contract),
               original_certificate_sha256=factory.digest(negative), witness=witness,
               witness_sha256=factory.digest(witness), composition=composed,
               composition_sha256=factory.digest(composed))
    receipt = dict(status='observed-typed-witnesses-only', inputs_stable=True,
                   original_certificates_unchanged=True, composer_used=True,
                   central_receipt_sha256=factory.core.composer.CENTRAL_PIN,
                   views=1, objects=1, passed_views=1, discharged_blockers=len(witness['discharge_blocker_ids']))
    receipt.update({key: False for key in ('provider_selected','runtime_eligible','emission_performed',
        'compiler_performed','executable_link_performed','game_execution_performed',
        'native_operations_performed','original_data_ownership_proved','ABI_verified')})
    summary = dict(lane=5, lane_record_ordinal=2, event=row['event'], recipe_id=row['recipe_id'],
                   record_sha256=record_sha, roots=[roots[0]['original_address']],
                   certificate_sha256=factory.digest(negative), closure_observed=False,
                   graph_observation_complete=negative['graph_observation_complete'])
    return receipt, [row], dict(observations=[summary]), {roots[0]['original_address']: roots[0]}


def relink_and_hash(row):
    """Keep attacker-controlled local digests consistent; authority stays fixed."""
    row['witness_sha256'] = factory.digest(row['witness'])
    for observation in row['composition']['witness_observations']:
        observation['witness_sha256'] = row['witness_sha256']
    for discharge in row['composition']['discharged_blockers']:
        discharge['witness_sha256'] = row['witness_sha256']
    row['composition_sha256'] = factory.digest(row['composition'])


class IndependentDataEnvelopeTests(unittest.TestCase):
    def test_exact_authored_saved_envelope_joins_original_scope(self):
        args = authored_envelope()
        result = factory.join_data_rows(*args)
        self.assertEqual(set(result), {'0x00500000'})
        self.assertEqual(result['0x00500000']['requested_root'], args[3]['0x00500000'])

    def test_borrowed_locator_root_or_original_certificate_is_fatal(self):
        for mutation in ('locator', 'root', 'base_hash', 'contract_hash'):
            args = copy.deepcopy(authored_envelope())
            row = args[1][0]
            if mutation == 'locator': row['ordinal'] = 3
            elif mutation == 'root': row['requested_roots'][0]['symbol_index'] = 77
            elif mutation == 'base_hash': row['original_certificate_sha256'] = 'f'*64
            else: row['contract_identity_sha256'] = 'f'*64
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                factory.join_data_rows(*args)

    def test_rehashed_borrowed_witness_source_or_object_cannot_override_root(self):
        for field in ('source_sha256', 'object_sha256', 'recipe_id'):
            args = authored_envelope()
            row = args[1][0]
            row['witness'][field] = 'f'*64 if field != 'recipe_id' else 'borrowed-recipe'
            relink_and_hash(row)
            with self.subTest(field=field), self.assertRaises(ValueError):
                factory.join_data_rows(*args)

    def test_witness_observation_hash_is_linked_to_actual_saved_witness(self):
        args = authored_envelope()
        row = args[1][0]
        row['composition']['witness_observations'][0]['witness_sha256'] = 'f'*64
        row['composition_sha256'] = factory.digest(row['composition'])
        with self.assertRaises(ValueError):
            factory.join_data_rows(*args)

    def test_selected_root_has_no_remaining_occurrence_and_exact_discharge_partition(self):
        args = authored_envelope()
        row = args[1][0]
        original = row['composition']['base_certificate']
        row['composition']['discharged_blockers'] = []
        row['composition']['remaining_blocker_occurrences'] = [
            dict(base_blocker_ordinal=1, blocker=copy.deepcopy(original['blockers'][0]))]
        row['composition_sha256'] = factory.digest(row['composition'])
        with self.assertRaises(ValueError):
            factory.join_data_rows(*args)

    def test_duplicate_discharged_occurrence_cannot_replace_another_original(self):
        args = authored_envelope(two_sections=True)
        row = args[1][0]
        self.assertEqual(len(row['composition']['discharged_blockers']), 2)
        row['composition']['discharged_blockers'][1] = copy.deepcopy(row['composition']['discharged_blockers'][0])
        row['composition_sha256'] = factory.digest(row['composition'])
        with self.assertRaises(ValueError):
            factory.join_data_rows(*args)

    def test_partial_row_aborted_unstable_or_promoted_envelope_is_not_authority(self):
        for mutation in ('row', 'aborted', 'unstable', 'witness_promoted', 'receipt_ABI'):
            args = authored_envelope()
            row = args[1][0]
            if mutation == 'row':
                row['witness']['rows'][0]['approved'] = False
                relink_and_hash(row)
            elif mutation == 'aborted': args[0]['status'] = 'aborted-no-retry'
            elif mutation == 'unstable': args[0]['inputs_stable'] = False
            elif mutation == 'receipt_ABI': args[0]['ABI_verified'] = True
            else:
                row['witness']['provider_selected'] = True
                relink_and_hash(row)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                factory.join_data_rows(*args)

    def test_unknown_saved_DATA_row_field_is_not_silently_discarded(self):
        args = authored_envelope()
        args[1][0]['unreviewed_override'] = True
        with self.assertRaises(ValueError):
            factory.join_data_rows(*args)

    def test_duplicate_saved_locator_does_not_fill_a_missing_view(self):
        args = authored_envelope()
        args[1].append(copy.deepcopy(args[1][0]))
        args[0].update(views=2, passed_views=2, discharged_blockers=2)
        with self.assertRaises(ValueError):
            factory.join_data_rows(*args)


if __name__ == '__main__':
    unittest.main()
