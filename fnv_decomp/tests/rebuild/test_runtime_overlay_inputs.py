"""Synthetic alternate-lane contracts; no private objects, image or native tools."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
sys.path.insert(0,str(Path(__file__).resolve().parent))
import runtime_overlay_inputs as registry
import entry_relocation_batch as batch
from coff_inventory import Coff
from test_entry_relocation_batch import fixture,recipe


def request(owner):
    return dict(address=owner['function_va'],selection=owner['original_selected_owner'],
        fields=[dict(offset=f['function_offset'],target=f['target_va'],symbol=f['proposed_target_symbol']) for f in owner['fields']])


class RegistryTests(unittest.TestCase):
    def test_fixed_explicit_policy_is_nine_units_thirteen_owners_twenty_two_fields(self):
        p=registry.policy()
        self.assertEqual(len(p['units']),9)
        self.assertEqual(sum(len(u['requested_owners']) for u in p['units']),13)
        self.assertEqual(sum(len(o['fields']) for u in p['units'] for o in u['requested_owners']),22)
        self.assertEqual(p['expected_function_rows'],931)
        self.assertFalse(p['adopted_for_link'])

    def test_complete_scope_keeps_unaffected_defined_code_owners_original(self):
        owner=batch.policy()['units'][0]['owners'][0]
        with tempfile.TemporaryDirectory() as td:
            before,after=Path(td)/'old.obj',Path(td)/'new.obj';before.write_bytes(fixture(owner));after.write_bytes(fixture(owner,True))
            scope=registry.function_scope(Coff(before),Coff(after),recipe(owner),[request(owner)],dict(witnesses=[]))
        self.assertGreater(len(scope),1)
        self.assertEqual(sum(r['requested_alternate'] for r in scope),1)
        selected={r['address']:dict(recipe_id=owner['original_selected_owner']['recipe_id'],symbol=r['symbol'],size=r['size'],section=r['original_native']['section'],value=r['original_native']['value']) for r in scope}
        mapping=registry.replacement_map(owner['original_selected_owner']['recipe_id'],'oldhash','newhash','new-unit',scope,[request(owner)],selected)
        original=[r for r in mapping if not r['alternate_requested_by_fixed_policy']]
        self.assertTrue(all(r['effective_provider_lane']=='original-selection-unchanged' and not r['alternate_same_TU_definition_exported'] for r in original))

    def test_unapproved_extra_reference_or_nonfield_body_change_rejected(self):
        owner=batch.policy()['units'][0]['owners'][0]
        with tempfile.TemporaryDirectory() as td:
            old,new=Path(td)/'old.obj',Path(td)/'new.obj';old.write_bytes(fixture(owner))
            for kwargs in [dict(extra_relocation=True),dict(changed_byte=True),dict(wrong_target=True),dict(code_undefined=True)]:
                new.write_bytes(fixture(owner,True,**kwargs))
                with self.assertRaises(ValueError):registry.function_scope(Coff(old),Coff(new),recipe(owner),[request(owner)],dict(witnesses=[]))

    def test_literal_namespace_changes_require_exact_witness_name_pair(self):
        def ref(name):return dict(semantic=dict(offset=4,kind=6,addend=0,target=dict(name=name,section=3,value=0,type=0,storage=3,aux_count=0)))
        old,new=[ref('$SG100')],[ref('$SG900')]
        registry.normalize_fields(old,new,[],{'$SG900':'$SG100'})
        with self.assertRaises(ValueError):registry.normalize_fields(old,new,[],{})
        bad=copy.deepcopy(new);bad[0]['semantic']['target']['storage']=2
        with self.assertRaises(ValueError):registry.normalize_fields(old,bad,[],{'$SG900':'$SG100'})

    def test_replacement_conflicts_wrong_original_provider_or_coalesced_symbols_reject(self):
        scope=[dict(address='0x00401000',symbol='_f',size=8,original_native=dict(symbol_index=3,section=1,value=0),overlay_native=dict(symbol_index=7,section=2,value=0))]
        request0=dict(address='0x00401000',fields=[])
        selected={'0x00401000':dict(recipe_id='recipe',symbol='_f',size=8,section=1,value=0)}
        registry.replacement_map('recipe','old','new','unit',scope,[request0],selected)
        wrong=copy.deepcopy(selected);wrong['0x00401000']['recipe_id']='other'
        with self.assertRaises(ValueError):registry.replacement_map('recipe','old','new','unit',scope,[request0],wrong)
        scope2=scope+[dict(scope[0],address='0x00402000',symbol='_g')]
        selected['0x00402000']=dict(selected['0x00401000'],symbol='_g')
        with self.assertRaises(ValueError):registry.replacement_map('recipe','old','new','unit',scope2,[request0,dict(address='0x00402000')],selected)

    def test_migration_hashes_actual_fresh_lane_rows_and_retains_remaining_missing(self):
        old=[dict(event='MISSING_ORIGINAL_HIGHLOW_SOURCE_MIGRATION_BLOCKER',function_va='0x00401000',source_field_offset=4)]
        row=dict(event='SELECTED_FUNCTION_COFF_RELOCATION',function_va='0x00401000',source_field_offset=4,
            coff_relocation=dict(kind=6,addend=0,symbol='_data'),exact_original_target_va='0x00600000',proof_consistency='EXACT_OWN_SOURCE_RESOLUTION',
            overlay_unit_id='fresh-unit',actual_object_sha256='fresh-object')
        requests=[dict(address='0x00401000',fields=[dict(offset=4,target='0x00600000',symbol='_data')])]
        proof=registry.migration(old,[row],requests)
        self.assertEqual(proof['repairs'][0]['binding_sha256'],registry.identity(row))
        for bad in ([dict(row,exact_original_target_va='0x00600004')],[],[row,row]):
            with self.assertRaises(ValueError):registry.migration(old,bad,requests)
        unresolved=dict(event='MISSING_ORIGINAL_HIGHLOW_SOURCE_MIGRATION_BLOCKER',function_va='0x00401000',source_field_offset=12)
        proof=registry.migration(old+[unresolved],[row,unresolved],requests)
        self.assertEqual(proof['alternate_missing_count'],1)
        with self.assertRaises(ValueError):registry.migration(old+[unresolved],[row],requests)

    def test_whole_root_contract_has_new_physical_indices_and_blocks_old_v3_relabel(self):
        functions=[dict(address='0x00401000',symbol='_f',size=8,overlay_native=dict(symbol_index=17,section=9,value=0))]
        requests=[dict(address='0x00401000')];replacements=[dict(address='0x00401000',alternate_definition_id='alternate-id')]
        rows=[dict(function_va='0x00401000',function_symbol='_f',overlay_unit_id='unit',actual_object_sha256='fresh-object')]
        contract=registry.root_contract('unit',{'recipe_id':'old'},dict(generated_source_sha256='generated'),'private.obj','fresh-object',functions,requests,replacements,rows,{'original_only':True})
        self.assertEqual(contract['roots'][0]['symbol_index'],17)
        self.assertEqual(contract['roots'][0]['binding_refs'][0]['sha256'],registry.identity(rows[0]))
        self.assertFalse(contract['ordinary_v3_input_compatible'])
        self.assertFalse(contract['provider_adopted'])
        with self.assertRaises(ValueError):registry.root_contract('unit',{}, {},'x','hash',[],requests,replacements,rows,{})

    def test_compile_lineage_requires_exact_accepted_object_source_and_profile(self):
        spec=dict(group='first-two',recipe_id='recipe',object='overlay.obj',generated_source='source.cpp',artifacts={'overlay.obj':'object','source.cpp':'generated'})
        key='build/rebuild/entry-relocation-repair-native-v1/result.json'
        records={key:dict(units=[dict(recipe_id='recipe',object_sha256='object',generated_source_sha256='generated',original_recipe_flags=['/Od'])])}
        registry.compile_lineage(spec,records,{'flags':['/Od']})
        for prop,value in [('object_sha256','old-object'),('generated_source_sha256','original-source'),('original_recipe_flags',['/O2'])]:
            broken=copy.deepcopy(records);broken[key]['units'][0][prop]=value
            with self.assertRaises(ValueError):registry.compile_lineage(spec,broken,{'flags':['/Od']})


if __name__=='__main__':unittest.main()
