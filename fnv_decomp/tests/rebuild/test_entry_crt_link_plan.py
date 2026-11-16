"""Finite candidate mapping tests, with no compiler/image/library inputs."""
import copy
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import tempfile

PATH=Path(__file__).resolve().parents[2]/'tools/rebuild/entry_crt_link_plan.py'
SPEC=importlib.util.spec_from_file_location('entry_crt_link_plan',PATH)
m=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


def row(base,role,ordinal,caller='0x0086a850'):
    return dict(derived_source_symbol_base_va=base,exact_original_target_va=base,
        classification='EXPLICIT_NORMAL_CRT_CONTRACT_CANDIDATE' if role=='crt-contract' else 'UNSELECTED_EXECUTABLE_TARGET_UNCLASSIFIED',
        recipe_id='recipe',function_va=caller,source_field_offset=20,physical_section=3,physical_offset=20,
        original_field_va='0x0086a864',source_resolution_basis='OWN_RECIPE_BINDING',proof_consistency='EXACT_OWN_SOURCE_RESOLUTION',
        coff_relocation=dict(symbol_section=0,symbol_storage=2,symbol_value=0,kind=20,addend=0,symbol_index=9,symbol='actual_source_spelling'),
        ordinal=ordinal,sha256='0'*64,source='src/example.cpp',source_sha256='1'*64,object_sha256='2'*64)


def evidence():
    providers=dict(previous_six_member_evidence=[],new_indexed_member_evidence=[],field_sites=[])
    frontier=dict(boundaries=dict(generated_or_unselected_code_unknown={}))
    exports=set()
    for i,(base,role,export)in enumerate(m.CANDIDATES,1):
        r=row(base,role,i,m.LEAF if base=='0x00ecb3a8' else '0x0086a850')
        if (base,role)in (('0x00ec6bd2','code'),('0x00ec43fb','code')):
            frontier['boundaries']['generated_or_unselected_code_unknown'][base]=[r]
        else:providers['field_sites'].append(r)
        if export and export not in exports:
            providers['new_indexed_member_evidence'].append(dict(compiler_family='sp1',symbol=export,
                archive_sha256='3'*64,member_header_offset=100,member_sha256='4'*64,definition=dict(section=3,value=0)))
            exports.add(export)
    return providers,frontier


class EntryCrtLinkPlanTests(unittest.TestCase):
    def test_role_keyed_namespace_is_existing_fread_identity(self):
        self.assertEqual(m.undefined('0x00ecb3a8','code'),
            '_fnv_undefined_0c4e496a4a88850bf6d891c83171901bbbf2c62066442d845d0fb5bdd4787b0c')
        self.assertNotEqual(m.undefined('0x00ec43fb','code'),m.undefined('0x00ec43fb','crt-contract'))

    def test_same_address_other_role_remains_unresolved(self):
        p,f=evidence();result=m.mapping(p,f)
        target={r['role']:r for r in result if r['original_base']=='0x00ec43fb'}
        self.assertIsNotNone(target['crt-contract']['proposed_provider'])
        self.assertIsNone(target['code']['proposed_provider'])
        self.assertEqual(target['code']['initial_preparation_site_ordinals'],[])
        self.assertTrue(all(not r['provider_selected'] and not r['provider_alias_emitted'] for r in result))

    def test_append_main_only_and_fread_leaf_only(self):
        p,f=evidence()
        for base in ('0x00406d50','0x00ecb3a8'):
            p['field_sites'].append(row(base,'code',100+len(p['field_sites']),'0x00500000'))
        result=m.mapping(p,f)
        for r in result:
            if r['original_base']in ('0x00406d50','0x00ecb3a8'):
                self.assertEqual(r['observed_field_count'],2)
                self.assertEqual(len(r['initial_preparation_site_ordinals']),1)

    def test_zero_addend_physical_contract_guard(self):
        for key,value in [('symbol_section',1),('symbol_storage',3),('symbol_value',4),('kind',6),('addend',1)]:
            r=row('0x00ecb3a8','code',1);r['coff_relocation'][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):m.field_identity(r)

    def test_proof_consistency_guard(self):
        r=row('0x00ecb3a8','code',1);r['proof_consistency']='LITERAL_TOLERANCE'
        with self.assertRaises(ValueError):m.field_identity(r)

    def test_duplicate_export_and_field_guard(self):
        p,f=evidence();p['new_indexed_member_evidence'].append(copy.deepcopy(p['new_indexed_member_evidence'][0]))
        with self.assertRaisesRegex(ValueError,'ambiguous'):m.mapping(p,f)
        p,f=evidence();p['field_sites'].append(copy.deepcopy(p['field_sites'][0]))
        with self.assertRaisesRegex(ValueError,'duplicate'):m.mapping(p,f)

    def test_absent_export_and_target_drift_guard(self):
        p,f=evidence();p['new_indexed_member_evidence']=[]
        with self.assertRaisesRegex(ValueError,'export'):m.mapping(p,f)
        p,f=evidence();p['field_sites'][0]['exact_original_target_va']='0x00000001'
        with self.assertRaisesRegex(ValueError,'base mismatch'):m.mapping(p,f)

    def test_missing_field_scope_and_new_class_guard(self):
        p,f=evidence();p['field_sites'].pop()
        with self.assertRaisesRegex(ValueError,'scope'):m.mapping(p,f)
        p,f=evidence();p['field_sites'][0]['classification']='NEW_ROLE'
        with self.assertRaisesRegex(ValueError,'class'):m.mapping(p,f)

    def test_stale_implementation_rejected_before_any_metadata(self):
        with self.assertRaisesRegex(ValueError,'implementation'):
            m.run(SimpleNamespace(implementation_sha256='0'*64,metadata_dir='does-not-exist',out='does-not-exist'))

    def test_pin_widths(self):
        self.assertTrue(all(len(h)==64 and all(c in '0123456789abcdef' for c in h)for _,h in m.PINS.values()))

    def test_public_checkout_output_and_external_output_rejected(self):
        with tempfile.TemporaryDirectory()as temp,patch.object(m,'ROOT',Path(temp).resolve()):
            self.assertEqual(m.private_output(Path(temp)/'build/rebuild/report.json'),Path(temp).resolve()/'build/rebuild/report.json')
            for path in (Path(temp)/'docs/report.json',Path(temp)/'src/report.json',Path(temp).parent/'outside.json'):
                with self.subTest(path=path),self.assertRaisesRegex(ValueError,'ignored'):m.private_output(path)

    def component_fixture(self):
        assessments={a:{}for a in m.FILE_ROOTS}
        assessments[m.LEAF]=dict(physical_identity=dict(recipe_id='1821-ead65709d249dd91',
            object_sha256='c768b253bc216a32ff93300d2cd488a33c6c726c7aa01d9fb0e230fa7e396e4b',symbol_index=8),
            selected_native=dict(section=3),size=39,original_missing_fields=0,same_parent_piece_observations=0,
            blockers=[dict(code='SAFESEH_REQUIRES_CLOSURE')],
            obligations=[dict(canonical_name=m.undefined('0x00ecb3a8','code'))])
        fields={a:[]for a in m.FILE_ROOTS};r=row('0x00ecb3a8','code',384166,m.LEAF)
        r['coff_relocation']['symbol']='_fread';fields[m.LEAF]=[r]
        return assessments,fields

    def test_actual_leaf_contract_retains_gate_and_zero_execution(self):
        a,f=self.component_fixture();result=m.source_component(a,f)
        self.assertFalse(result['approved_object_emission'])
        self.assertFalse(result['runtime_eligible'])
        self.assertEqual(result['initial_retained_root'],m.LEAF)
        self.assertEqual(result['receiver_contract']['stream_pointer_offset'],12)

    def test_actual_leaf_new_missing_or_EH_evidence_rejected(self):
        for key,value in [('original_missing_fields',1),('same_parent_piece_observations',1),('size',40)]:
            a,f=self.component_fixture();a[m.LEAF][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):m.source_component(a,f)

    def test_actual_leaf_changed_fread_or_namespace_rejected(self):
        a,f=self.component_fixture();f[m.LEAF][0]['coff_relocation']['symbol']='_fwrite'
        with self.assertRaisesRegex(ValueError,'field'):m.source_component(a,f)
        a,f=self.component_fixture();a[m.LEAF]['obligations'][0]['canonical_name']='different'
        with self.assertRaisesRegex(ValueError,'namespace'):m.source_component(a,f)


if __name__=='__main__':unittest.main()
