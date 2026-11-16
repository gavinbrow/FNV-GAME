import copy
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'tools/rebuild'))
import prepared_code56_successor as m


def fixture():
    records = []
    for i in range(14478):
        identity = dict(recipe_id='authored-unit', object_sha256='a' * 64, symbol_index=i)
        records.append(dict(canonical=m.physical(identity), original_address='0x%08x' % i,
            namespace_identity=identity, origin_identity=identity.copy(),
            category='ordinary' if i < 14472 else 'application-candidate',
            identity_mode='authored-logical' if i >= 14472 else 'original-selected-physical',
            retained_unknown={'value': None, 'flag': False}))
    names, ordinary = m.census(records)
    parent = dict(schema_version=6, kind='prepared-CODE-collision-exclusions',
        ordinary_prepared_count=14472, collision_exclusion_count=14478,
        broader_application_candidate_count=6, records=records,
        exclusion_names=names, ordinary_names=ordinary, application_selected_code_count=None,
        application_selection_inferred_from_counts=False, runtime_eligible=False)
    handoff = dict(schema_version=1, kind='accepted-prepared-CODE-export-handoff',
        requires_successor_exclusion_epoch=True, new_distinct_exports=56,
        upstream_ordinary_prepared_count=14472, upstream_collision_exclusion_count=14478,
        successor_ordinary_prepared_count=14528, successor_collision_exclusion_count=14534,
        full_field_proof_rows=290, field_proofs={'sha256': 'b' * 64}, records=[])
    handoff.update({k: False for k in ('application_cohort_adopted', 'application_manifest_adopted',
        'provider_selected', 'runtime_eligible', 'ABI_verified', 'link_ready')})
    members = []
    for i in range(56):
        root = dict(recipe_id='authored-unit', object_sha256='a' * 64, symbol_index=20000+i,
                    section=8, original_address='0x%08x' % (20000+i))
        name = m.physical({k: root[k] for k in ('recipe_id','object_sha256','symbol_index')})
        count = 6 if i < 10 else 5
        row = dict(root=root, canonical=name, member='authored-%d.obj' % i,
            member_sha256='c'*64, authority={'authored': i}, certificate_sha256='d'*64,
            contract_identity_sha256='e'*64, field_proof_ordinal=i+1, fields=count,
            serialized_section=2, serialized_symbol_index=6,
            field_proof_record_sha256='f'*64, original_fields_sha256='0'*64)
        handoff['records'].append(row)
        p = dict(requested_roots=[root], exports=[name], output_sha256='c'*64,
            authority=row['authority'], certificate_sha256='d'*64, contract_identity_sha256='e'*64,
            fields=[{} for _ in range(count)], maps={'section_map': {'8': 2}, 'symbol_map': {str(20000+i): 6}})
        members.append({'name':row['member'], 'projection':p})
    return parent, handoff, members


class SuccessorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = fixture()

    def test_complete_successor_preserves_unknown_historical_modes(self):
        before = copy.deepcopy(self.data)
        out = m.build(*self.data)
        self.assertEqual(self.data, before)
        self.assertEqual(out['records'][:14478], self.data[0]['records'])
        self.assertEqual((out['ordinary_prepared_count'],out['collision_exclusion_count']), (14528,14534))
        self.assertIsNone(out['application_selected_code_count'])
        self.assertNotIn('application_manifest_adopted',out)
        self.assertFalse(out['fresh_original_stability_verified'])

    def test_address_collision_rejected(self):
        p,h,members = copy.deepcopy(self.data)
        h['records'][0]['root']['original_address'] = p['records'][0]['original_address']
        with self.assertRaises(ValueError): m.build(p,h,members)

    def test_wrong_serialized_identity_rejected(self):
        p,h,members = copy.deepcopy(self.data)
        members[0]['projection']['maps']['symbol_map']['20000'] = 7
        with self.assertRaises(ValueError): m.build(p,h,members)

    def test_bool_ordinal_rejected(self):
        p,h,members = copy.deepcopy(self.data)
        h['records'][0]['field_proof_ordinal'] = True
        with self.assertRaises(ValueError): m.build(p,h,members)

    def test_parent_adoption_or_byte_drift_rejected(self):
        p,h,members = copy.deepcopy(self.data)
        p['application_manifest_adopted'] = False
        with self.assertRaises(ValueError): m.build(p,h,members)
        with self.assertRaises(ValueError): m.from_bytes(b'{}',b'{}',b'{}')


if __name__ == '__main__': unittest.main()
