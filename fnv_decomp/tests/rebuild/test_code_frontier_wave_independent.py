"""Independent full-count V7 epoch and ModelLoader metadata lineage fixtures."""
import copy
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import code_frontier_wave as f
from test_current_code_frontier_independent import successor_fixture
from test_prepared_code_exclusions_independent import sha


def wave_fixture():
    values=successor_fixture()
    parent=f.prior.planner.successor_epoch(*values,typed_members_sha256=sha('authored-typed-ledger'),
        eh_metadata_sha256=sha('authored-EH-ledger'))
    providers=values[1];units={};members=[]
    def root(address,index,recipe):
        entry=dict(recipe_id=recipe,object_sha256=sha(recipe),symbol_index=index,
            source_sha256=sha('source-'+recipe),symbol='_authored_%d'%index,section=7,value=0,size=21)
        entry['planned_canonical_name']=f.base.pool.canonical({k:entry[k] for k in ('recipe_id','object_sha256','symbol_index')})
        providers[address]=entry;units[recipe]=dict(recipe_index=index,object_sha256=entry['object_sha256'],source_sha256=entry['source_sha256'])
        return f.prior.planner.root_record(address,entry,units)
    for index in range(59):
        r=root('0x%08x'%(0x00b00000+16*index),1000+index,'authored-wave-%d'%index)
        members.append(dict(name='authored-wave-%02d.obj'%index,projection=dict(requested_roots=[r],
            exports=[providers[r['original_address']]['planned_canonical_name']],original_object_sha256=r['object_sha256'],
            output_sha256=sha('projected-wave-%d'%index),maps=dict(symbol_map={str(r['symbol_index']):2}))))
    r=root('0x00448420',2000,'authored-ModelLoader');name=providers[r['original_address']]['planned_canonical_name']
    maps=dict(symbol_map={'2000':2},section_map={'7':1},auxiliary_map={},undefined_conversions=[])
    ml=dict(original_root=r,parent=r['original_address'],physical_exports=[name],source_object_sha256=r['object_sha256'],
        object_sha256=sha('authored-ModelLoader-projected'),receipt_sha256=f.INPUTS['ML_receipt'][1],physical_maps=maps,
        all_parent_EH_fields_preserved=True,no_symbol_coalescing=True,native_COFF_conformance_collected=False,
        observation_sha256=sha('authored-observation'),input_request_sha256=sha('authored-request'),
        provider_selected=False,runtime_eligible=False,ABI_verified=False,link_ready=False,namespace_approved=False)
    receipt=dict(parent=r['original_address'],input_stability=True,source_member_layout_verified=False,
        observation_sha256=ml['observation_sha256'],input_request_sha256=ml['input_request_sha256'],
        provider_selected=False,runtime_eligible=False,ABI_verified=False,link_ready=False,namespace_approved=False,
        projection=dict(input_sha256=r['object_sha256'],output_sha256=ml['object_sha256'],export=name,maps=copy.deepcopy(maps)))
    return parent,providers,units,members,ml,receipt


class IndependentWaveEpochTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.values=wave_fixture()

    def test_complete_successor_keeps_parent_and_explicit_broader_limitations(self):
        before=f.digest(self.values[0]);result=f.extend_epoch(*self.values)
        self.assertEqual(f.digest(self.values[0]),before)
        records={r['canonical']:r for r in result['records']}
        self.assertTrue(all(records[r['canonical']]==r for r in self.values[0]['records']))
        self.assertEqual((len(records),len(result['ordinary_names'])),(14406,14400))
        self.assertEqual(result['broader_application_candidate_count'],6)
        self.assertIsNone(result['application_selected_code_count'])
        ml=next(r for r in result['records'] if r['cohort']=='ModelLoader-EH')
        self.assertEqual(ml['category'],'application-candidate')
        self.assertNotIn(ml['canonical'],result['ordinary_names'])
        self.assertFalse(ml['source_member_layout_verified'])
        self.assertFalse(ml['historical_native_flag'])
        self.assertEqual(ml['subsequent_native_review_sha256'],f.INPUTS['ML_native_review'][1])
        old=next(r for r in result['records'] if r['cohort']=='EH-physical-candidate')
        self.assertFalse(old['logical_binding_applied'])
        self.assertNotIn(old['prospective_logical_demand'],result['exclusion_names'])
        self.assertTrue(all(result[k] is False for k in f.FALSE))

    def test_duplicate_or_stale_ordinary_physical_namespace_rejected(self):
        for mutation in (lambda v:v[3].__setitem__(1,copy.deepcopy(v[3][0])),
                         lambda v:v[3][0]['projection']['requested_roots'][0].update(symbol_index=99)):
            values=copy.deepcopy(self.values);mutation(values)
            with self.assertRaises(ValueError):f.extend_epoch(*values)

    def test_ModelLoader_source_output_export_and_numeric_maps_cannot_be_borrowed(self):
        changes=[lambda v:v[4].update(source_object_sha256='0'*64),
            lambda v:v[5]['projection'].update(input_sha256='0'*64),
            lambda v:v[5]['projection'].update(output_sha256='0'*64),
            lambda v:v[5]['projection'].update(export='_authored_wrong_namespace'),
            lambda v:v[5]['projection']['maps']['symbol_map'].update({'2000':9}),
            lambda v:v[4].update(no_symbol_coalescing=False)]
        for index,change in enumerate(changes):
            values=copy.deepcopy(self.values);change(values)
            with self.subTest(index=index),self.assertRaises(ValueError):f.extend_epoch(*values)

    def test_ModelLoader_actual_layout_and_stability_limits_are_preserved(self):
        changes=[lambda v:v[5].update(input_stability=False),
            lambda v:v[5].update(source_member_layout_verified=True),
            lambda v:v[5].update(observation_sha256='0'*64),
            lambda v:v[5].update(input_request_sha256='0'*64)]
        for index,change in enumerate(changes):
            values=copy.deepcopy(self.values);change(values)
            with self.subTest(index=index),self.assertRaises(ValueError):f.extend_epoch(*values)


if __name__=='__main__':unittest.main()
