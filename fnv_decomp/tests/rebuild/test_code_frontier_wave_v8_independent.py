"""Independent full-count authored V8 successor lineage; no original bodies."""
import copy
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import code_frontier_wave_v8 as f
from test_code_frontier_wave_independent import wave_fixture
from test_prepared_code_exclusions_independent import sha


def v8_fixture():
    old=wave_fixture();parent=f.old.extend_epoch(*old);providers=old[1];units=old[2];members=[]
    for index in range(3):
        address='0x%08x'%(0x00c00000+16*index);recipe='authored-V8-%d'%index
        entry=dict(recipe_id=recipe,object_sha256=sha(recipe),source_sha256=sha('source-'+recipe),
            symbol_index=3000+index,symbol='_authored_V8_%d'%index,section=9,value=0,size=20+index)
        entry['planned_canonical_name']=f.base.pool.canonical({k:entry[k] for k in ('recipe_id','object_sha256','symbol_index')})
        providers[address]=entry;units[recipe]=dict(recipe_index=3000+index,object_sha256=entry['object_sha256'],source_sha256=entry['source_sha256'])
        root=f.prior.planner.root_record(address,entry,units)
        members.append(dict(name='authored-V8-%d.obj'%index,projection=dict(requested_roots=[root],
            exports=[entry['planned_canonical_name']],original_object_sha256=entry['object_sha256'],
            output_sha256=sha('projected-'+recipe),maps=dict(symbol_map={str(entry['symbol_index']):2}))))
    return parent,providers,units,members


class IndependentV8EpochTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.values=v8_fixture()

    def test_exact_full_parent_preservation_and_new_three_records(self):
        before=f.digest(self.values[0]);result=f.extend_epoch(*self.values)
        self.assertEqual(f.digest(self.values[0]),before)
        records={r['canonical']:r for r in result['records']}
        self.assertEqual((len(records),len(result['ordinary_names'])),(14409,14403))
        self.assertTrue(all(records[r['canonical']]==r for r in self.values[0]['records']))
        self.assertEqual(result['broader_application_candidate_count'],6)
        self.assertIsNone(result['application_selected_code_count'])
        self.assertTrue(all(result[k] is False for k in f.FALSE))
        for ordinal,member in enumerate(self.values[3],1):
            p=member['projection'];r=records[p['exports'][0]]
            self.assertEqual(r['source_record_sha256'],f.digest(member))
            self.assertEqual(r['source_record_ordinal'],ordinal)
            self.assertEqual(r['source_ledger_sha256'],f.INPUTS['members3'][1])
            self.assertEqual(r['serialized_symbol_index'],2)

    def test_duplicate_or_missing_new_member_cannot_close_successor(self):
        values=copy.deepcopy(self.values);values[3][1]=copy.deepcopy(values[3][0])
        with self.assertRaises(ValueError):f.extend_epoch(*values)
        values=copy.deepcopy(self.values);values[3].pop()
        with self.assertRaises(ValueError):f.extend_epoch(*values)

    def test_stale_original_identity_or_namespace_cannot_borrow_projected_hash(self):
        changes=[lambda v:v[3][0]['projection']['requested_roots'][0].update(symbol_index=42),
            lambda v:v[3][0]['projection'].update(original_object_sha256='0'*64),
            lambda v:v[3][0]['projection'].update(exports=['_authored_wrong_namespace']),
            lambda v:v[1][v[3][0]['projection']['requested_roots'][0]['original_address']].update(source_sha256='0'*64)]
        for index,change in enumerate(changes):
            values=copy.deepcopy(self.values);change(values)
            with self.subTest(index=index),self.assertRaises(ValueError):f.extend_epoch(*values)

    def test_broader_ModelLoader_and_physical_IOTask_remain_separate_from_ordinary(self):
        result=f.extend_epoch(*self.values)
        ml=next(r for r in result['records'] if r['cohort']=='ModelLoader-EH')
        self.assertFalse(ml['source_member_layout_verified']);self.assertFalse(ml['historical_native_flag'])
        self.assertNotIn(ml['canonical'],result['ordinary_names'])
        eh=next(r for r in result['records'] if r['cohort']=='EH-physical-candidate')
        self.assertFalse(eh['logical_binding_applied'])
        self.assertNotIn(eh['prospective_logical_demand'],result['exclusion_names'])
        self.assertFalse(result['application_manifest_adopted'])


if __name__=='__main__':unittest.main()
