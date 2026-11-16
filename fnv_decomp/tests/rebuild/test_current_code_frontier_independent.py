"""Independent authored successor lineage and namespace tests; no Game input."""
import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools/rebuild'), str(ROOT / 'tests/rebuild')]
import current_code_frontier as f
from test_prepared_code_exclusions_independent import epoch_fixture, sha


def successor_fixture():
    ordinary, application, providers, bindings = epoch_fixture()
    parent = f.old.build_manifest(ordinary, application, providers, bindings)
    parent.update(provider_map_sha256=f.typed.prior.MAP_PIN,
        provider_map_review_sha256=f.typed.prior.MAP_REVIEW[1],
        source_epoch_artifacts={k: h for k, (_, h) in f.old.INPUTS.items()},
        authority_state='requires-successful-producer-receipt-and-independent-outcome-review')
    members = []
    for index in range(12):
        address = '0x%08x' % (0x00a00000 + index * 16)
        physical = dict(recipe_id='authored-typed', object_sha256='c' * 64,
                        symbol_index=100 + index)
        name = f.base.pool.canonical(physical)
        providers[address] = dict(physical, planned_canonical_name=name)
        root = dict(physical, original_address=address)
        members.append(dict(name='authored-typed-%02d.obj' % index,
            projection=dict(requested_roots=[root], exports=[name],
                original_object_sha256=physical['object_sha256'],
                output_sha256=sha('authored-output-%d' % index),
                maps=dict(symbol_map={str(physical['symbol_index']): 0}))))
    physical = dict(recipe_id='authored-EH-File', object_sha256='d' * 64,
                    symbol_index=81)
    name = f.base.pool.canonical(physical)
    providers['0x005e0200'] = dict(physical, planned_canonical_name=name)
    maps = dict(symbol_map={'81': 0}, section_map={'7': 1}, auxiliary_map={},
                undefined_conversions={})
    metadata = dict(parent='0x005e0200', physical_exports=[name],
        source_object_sha256=physical['object_sha256'], object_sha256='e' * 64,
        physical_maps=maps, receipt_sha256=f.INPUTS['eh_receipt'][1],
        all_parent_EH_fields_preserved=True, actual_artifact_review_pending=True,
        native_COFF_conformance_collected=False, archive_emitted=False,
        app_link_retested=False, provider_selected=False, runtime_eligible=False,
        ABI_verified=False, link_ready=False, namespace_approved=False)
    receipt = dict(parent=metadata['parent'], input_stability=True,
        source_member_layout_verified=False, provider_selected=False,
        runtime_eligible=False, ABI_verified=False, link_ready=False,
        namespace_approved=False, native_execution=False,
        projection=dict(export=name, output_sha256=metadata['object_sha256'],
            input_sha256=physical['object_sha256'], maps=copy.deepcopy(maps),
            source_member_layout_verified=False))
    return parent, providers, members, metadata, receipt


class IndependentSuccessorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = successor_fixture()

    def build(self, values):
        return f.successor_epoch(*values, typed_members_sha256=sha('authored-typed-ledger'),
                                 eh_metadata_sha256=sha('authored-EH-ledger'))

    def test_successor_preserves_every_parent_record_and_unbound_logical_demand(self):
        parent = self.context[0]
        before = f.digest(parent)
        result = self.build(self.context)
        self.assertEqual(f.digest(parent), before)
        lookup = {r['canonical']: r for r in result['records']}
        self.assertTrue(all(lookup[r['canonical']] == r for r in parent['records']))
        self.assertEqual((result['ordinary_prepared_count'], result['collision_exclusion_count']),
                         (14341, 14346))
        self.assertIsNone(result['application_selected_code_count'])
        eh = next(r for r in parent['records'] if r['cohort'] == 'EH-physical-candidate')
        self.assertFalse(lookup[eh['canonical']]['logical_binding_applied'])
        self.assertNotIn(eh['prospective_logical_demand'], result['exclusion_names'])
        file_eh = next(r for r in result['records'] if r['cohort'] == 'parent-EH-File')
        self.assertFalse(file_eh['source_member_layout_verified'])
        self.assertTrue(all(result[k] is False for k in f.FALSE))

    def test_duplicate_typed_export_cannot_replace_an_existing_namespace(self):
        values = copy.deepcopy(self.context)
        values[2][1] = copy.deepcopy(values[2][0])
        with self.assertRaises(ValueError):
            self.build(values)

    def test_typed_wrong_old_identity_is_not_authorized_by_projected_hash(self):
        values = copy.deepcopy(self.context)
        values[2][0]['projection']['requested_roots'][0]['symbol_index'] += 999
        with self.assertRaises(ValueError):
            self.build(values)

    def test_EH_receipt_input_and_numeric_maps_must_bind_original_and_metadata(self):
        mutations = [
            lambda v: v[3].update(receipt_sha256='0' * 64),
            lambda v: v[4]['projection'].update(input_sha256='0' * 64),
            lambda v: v[4]['projection']['maps']['symbol_map'].update({'81': 9}),
        ]
        for mutate in mutations:
            values = copy.deepcopy(self.context)
            mutate(values)
            with self.subTest(mutation=mutations.index(mutate)):
                with self.assertRaises(ValueError):
                    self.build(values)


if __name__ == '__main__':
    unittest.main()
