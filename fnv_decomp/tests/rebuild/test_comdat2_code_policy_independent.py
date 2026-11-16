"""Independent authored Selection-2 CODE cases; no game/native inputs."""
from pathlib import Path
import copy
import hashlib
import importlib
import struct
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/rebuild'))
import coff_code_archive as frozen_coff
import root_code_closure as frozen_root
import runtime_code_pool as pool
from test_coff_code_archive import object_bytes,section,symbol,aux


def fixture(selection=2):
    payload=b'authored-code-01!'
    directives=b' /DEFAULTLIB:"LIBCMT" /DEFAULTLIB:"OLDNAMES" '
    raw=object_bytes([section('.text',payload),section('.drectve',directives,flags=0x100a00)],
        [symbol('.text',1,storage=3,auxiliary=aux(len(payload),selection=selection)),
         symbol('_authored_any_root',1,typ=32),symbol('.drectve',2,storage=3,auxiliary=aux(len(directives),selection=0)),
         symbol('@feat.00',-1,value=1,storage=3)])
    physical=dict(original_address='0x01001000',symbol='_authored_any_root',symbol_index=2,section=1,value=0,size=len(payload))
    requested=dict(physical,recipe_id='authored-comdat-any',recipe_index=0,object_sha256=hashlib.sha256(raw).hexdigest(),source_sha256='a'*64)
    contract=dict(recipe_id='authored-comdat-any',roots=[physical],
        provenance=dict(object_sha256=hashlib.sha256(raw).hexdigest(),source_sha256='a'*64),
        export_policy=frozen_root.EXPORT_POLICY,fields_complete=True,missing_fields_complete=True,verified_match=True,
        fields=[],missing_fields=[],parent_eh=[],unit_proofs_complete=True,omission_field_proofs=[],iat_import_observation={},
        unit_verified_functions=[dict(symbol=requested['symbol'],address=requested['original_address'],section=1,value=0,size=len(payload),verdict='match')])
    return raw,contract,requested


def census_for(root):
    identity={k:root[k] for k in ('recipe_id','object_sha256','symbol_index')}
    return dict(schema_version=1,kind='planned-code-definition-census',complete=True,
                entries=[dict(root=copy.deepcopy(root),planned_canonical_name=pool.canonical(identity))])


def rewrite(raw,contract,root,change):
    obj=frozen_coff.parse(raw);secs=copy.deepcopy(list(obj['sections'].values()))
    syms=[symbol(v['name'],v['section'],v['value'],v['type'],v['storage'],v['aux']) for v in obj['symbols'].values()]
    change(secs,syms,obj)
    raw=object_bytes(secs,syms);contract=copy.deepcopy(contract);root=copy.deepcopy(root)
    root['object_sha256']=hashlib.sha256(raw).hexdigest();contract['provenance']['object_sha256']=root['object_sha256']
    return raw,contract,root


def field_fixture(raw,contract,root):
    def change(secs,syms,obj):
        payload=bytearray(secs[0]['payload']);struct.pack_into('<I',payload,0,4)
        secs[0].update(payload=bytes(payload),relocs=[(0,2,6)])
        syms[0]=symbol('.text',1,storage=3,auxiliary=aux(len(payload),1,selection=2))
    raw,k,r=rewrite(raw,contract,root,change)
    k['fields']=[dict(recipe_id=r['recipe_id'],function_va=r['original_address'],physical_section=1,physical_offset=0,source_field_offset=0,
        coff_relocation=dict(offset=0,symbol_index=2,kind=6,symbol=r['symbol'],symbol_section=1,symbol_value=0,symbol_type=32,symbol_storage=2,addend=4,width=4),
        derived_source_symbol_base_va=r['original_address'],exact_original_target_va='0x01001004',classification='SELECTED_CODE_ENTRY',
        physical_field_overlap_count=1,proof_consistency='EXACT_OWN_SOURCE_RESOLUTION')]
    return raw,k,r


class FrozenSelectionBaseline(unittest.TestCase):
    def test_actual_selection2_auxiliary_and_exact_negative_root(self):
        raw,k,r=fixture();before=bytes(raw);obj=frozen_coff.parse(raw)
        self.assertEqual(struct.unpack('<IHHIhBBH',obj['symbols'][0]['aux'])[5],2)
        negative=frozen_root.assess_object(obj,k)
        self.assertEqual([b['code'] for b in negative['blockers']],['UNSUPPORTED_OR_PARTIAL_ROOT_SECTION'])
        self.assertEqual(negative['blockers'][0]['evidence'],k['roots'][0])
        self.assertFalse(negative['closure_observed']);self.assertFalse(negative['full_serialization_eligible'])
        self.assertEqual(raw,before)

    def test_control_selection1_is_existing_policy_eligible(self):
        raw,k,_=fixture(selection=1);c=frozen_root.assess_object(frozen_coff.parse(raw),k)
        self.assertTrue(c['closure_observed']);self.assertEqual(c['blockers'],[])


class IndependentComdatAnyPolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy=importlib.import_module('comdat_any_code_omission')
        self.raw,self.contract,self.root=fixture()
        self.contract['provenance'].update(recipe_id=self.root['recipe_id'],recipe_index=self.root['recipe_index'])

    def observe(self,raw=None,contract=None,root=None,census=None):
        raw=self.raw if raw is None else raw;k=self.contract if contract is None else contract;r=self.root if root is None else root
        base=frozen_root.assess_object(frozen_coff.parse(raw),k)
        return self.policy.observe_comdat_any_code_policy(raw,k,base,r,census_for(r) if census is None else census,policy_id=self.policy.POLICY),base

    def assertUnsupported(self,raw,k,r):
        result,base=self.observe(raw,k,r)
        self.assertFalse(result['witness_complete']);self.assertFalse(result['root_comdat2_policy_candidate'])
        self.assertEqual(result['discharge_blocker_ids'],[]);self.assertEqual(result['remaining_base_blockers'],base['blockers'])

    def test_positive_is_separate_exact_one_id_witness_with_original_bytes(self):
        before=(bytes(self.raw),copy.deepcopy(self.contract),copy.deepcopy(self.root));result,base=self.observe()
        self.assertEqual(result['kind'],'typed-comdat-any-code-policy-candidate-witness')
        self.assertTrue(result['witness_complete']);self.assertTrue(result['root_comdat2_policy_candidate'])
        self.assertEqual(result['discharge_blocker_ids'],[base['blockers'][0]['blocker_id']])
        self.assertEqual(result['remaining_base_blockers'],[])
        for key in ('namespace_approved','provider_selected','runtime_eligible','full_serialization_eligible','emission_performed','serialization_approved'):
            self.assertIs(result[key],False)
        self.assertEqual((self.raw,self.contract,self.root),before)
        self.assertFalse(base['closure_observed']);self.assertEqual(struct.unpack('<IHHIhBBH',frozen_coff.parse(self.raw)['symbols'][0]['aux'])[5],2)

    def test_explicit_correct_policy_optin_required(self):
        base=frozen_root.assess_object(frozen_coff.parse(self.raw),self.contract)
        with self.assertRaises(TypeError):self.policy.observe_comdat_any_code_policy(self.raw,self.contract,base,self.root,census_for(self.root))
        for policy in ('',None,'unrelated-policy'):
            with self.subTest(policy=policy),self.assertRaises(ValueError):
                self.policy.observe_comdat_any_code_policy(self.raw,self.contract,base,self.root,census_for(self.root),policy_id=policy)

    def test_field_bearing_code_preserves_exact_addend_and_all_proof_hashes(self):
        raw,k,r=field_fixture(self.raw,self.contract,self.root);before=bytes(raw);result,base=self.observe(raw,k,r)
        self.assertTrue(result['witness_complete'])
        self.assertEqual(result['root_relocations'],[dict(offset=0,symbol_index=2,kind=6,addend_bits=4)])
        self.assertEqual(result['complete_root_field_proof_sha256'],self.policy.digest(k['fields']))
        self.assertEqual(result['original_negative_certificate_sha256'],self.policy.digest(base))
        self.assertEqual(raw,before)

    def test_native_symbol_and_owner_boolean_aliases_are_blocked(self):
        raw,k,r=field_fixture(self.raw,self.contract,self.root)
        for name,value in [('symbol_section',True),('symbol_value',False),('offset',False),('addend',True)]:
            bad=copy.deepcopy(k);bad['fields'][0]['coff_relocation'][name]=value
            with self.subTest(field=name):self.assertUnsupported(raw,bad,r)
        for name,value in [('section',True),('value',False)]:
            bad=copy.deepcopy(self.contract);bad['unit_verified_functions'][0][name]=value
            with self.subTest(owner_field=name):self.assertUnsupported(self.raw,bad,self.root)

    def test_existing_positive_and_other_COMDAT_modes_are_not_reclassified(self):
        raw,k,r=fixture(selection=1);k['provenance'].update(recipe_id=r['recipe_id'],recipe_index=r['recipe_index'])
        with self.assertRaises(ValueError):self.observe(raw,k,r)
        for selection in (0,3,4,6,7):
            raw,k,r=fixture(selection=selection);k['provenance'].update(recipe_id=r['recipe_id'],recipe_index=r['recipe_index'])
            with self.subTest(selection=selection):self.assertUnsupported(raw,k,r)

    def test_zero_multiple_or_stale_planned_definition_is_blocked(self):
        for mode in ('empty','duplicate','stale_root','same_address_other_identity'):
            c=census_for(self.root)
            if mode=='empty':c['entries']=[]
            elif mode=='duplicate':c['entries'].append(copy.deepcopy(c['entries'][0]))
            elif mode=='stale_root':c['entries'][0]['root']['source_sha256']='b'*64
            else:
                other=copy.deepcopy(self.root);other.update(recipe_id='other-authored',recipe_index=1,object_sha256='b'*64,source_sha256='c'*64)
                c['entries']+=census_for(other)['entries']
            result,base=self.observe(census=c)
            with self.subTest(mode=mode):
                self.assertFalse(result['witness_complete']);self.assertEqual(result['discharge_blocker_ids'],[])
                self.assertEqual(result['remaining_base_blockers'],base['blockers'])

    def test_unrelated_strict_census_entry_does_not_fake_duplicate_root(self):
        c=census_for(self.root);other=copy.deepcopy(self.root)
        other.update(recipe_id='other-authored',recipe_index=1,object_sha256='b'*64,source_sha256='c'*64,original_address='0x01002000')
        c['entries']+=census_for(other)['entries'];result,_=self.observe(census=c)
        self.assertTrue(result['witness_complete']);self.assertEqual(result['planned_definition_observations'],1)

    def test_census_schema_and_complete_flag_are_strict(self):
        for key,value in [('schema_version',True),('complete',False),('complete',1),('kind','arbitrary'),('extra',0)]:
            c=census_for(self.root);c[key]=value
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):self.observe(census=c)
        c=census_for(self.root);c['entries'][0]['planned_canonical_name']='_fnv_code_'+'0'*64
        with self.assertRaises(ValueError):self.observe(census=c)
        for name in ('recipe_index','symbol_index','section','value','size'):
            c=census_for(self.root);c['entries'][0]['root'][name]=False
            with self.subTest(root_field=name),self.assertRaises(ValueError):self.observe(census=c)

    def test_original_CODE_extent_cannot_wrap_32bit_address_space(self):
        k=copy.deepcopy(self.contract);r=copy.deepcopy(self.root)
        r['original_address']='0xfffffff8';k['roots'][0]['original_address']=r['original_address'];k['unit_verified_functions'][0]['address']=r['original_address']
        with self.assertRaises(ValueError):self.observe(contract=k,root=r)

    def test_stale_raw_contract_and_negative_certificate_reject(self):
        base=frozen_root.assess_object(frozen_coff.parse(self.raw),self.contract)
        bad=copy.deepcopy(base);bad['blockers']=[]
        with self.assertRaises(ValueError):self.policy.observe_comdat_any_code_policy(self.raw,self.contract,bad,self.root,census_for(self.root),policy_id=self.policy.POLICY)
        with self.assertRaises(ValueError):self.policy.observe_comdat_any_code_policy(self.raw+b'changed',self.contract,base,self.root,census_for(self.root),policy_id=self.policy.POLICY)
        k=copy.deepcopy(self.contract);k['provenance']['object_sha256']='0'*64
        with self.assertRaises(ValueError):self.observe(contract=k)

    def test_contract_root_boolean_aliases_cannot_match_typed_requested_scope(self):
        for name,value in [('section',True),('value',False)]:
            k=copy.deepcopy(self.contract);k['roots'][0][name]=value
            with self.subTest(field=name),self.assertRaises(ValueError):self.observe(contract=k)

    def test_partial_extent_cannot_use_selection_only_discharge(self):
        k=copy.deepcopy(self.contract);r=copy.deepcopy(self.root)
        r['size']-=1;k['roots'][0]['size']-=1;k['unit_verified_functions'][0]['size']-=1
        self.assertUnsupported(self.raw,k,r)

    def test_bad_flags_cannot_use_selection_only_discharge(self):
        def change(secs,syms,obj):secs[0]['flags']=0x40501020
        self.assertUnsupported(*rewrite(self.raw,self.contract,self.root,change))

    def test_alias_or_multiple_function_definition_blocks(self):
        def change(secs,syms,obj):syms.append(symbol('_alias',1,value=4,typ=32))
        self.assertUnsupported(*rewrite(self.raw,self.contract,self.root,change))

    def test_unowned_data_never_waived_by_CODE_policy(self):
        def change(secs,syms,obj):
            secs.append(section('.data',b'authored-data',flags=0xc0300040))
            syms.extend([symbol('.data',3,storage=3,auxiliary=aux(len(secs[2]['payload']),selection=0)),symbol('_unowned_data',3)])
        self.assertUnsupported(*rewrite(self.raw,self.contract,self.root,change))

    def test_association_EH_TLS_CRT_and_SafeSEH_contexts_block(self):
        for name in ('.text$x','.tls$A','.CRT$XCU','.sxdata','.associated'):
            def change(secs,syms,obj):
                payload=struct.pack('<I',2) if name=='.sxdata' else b'authored-context'
                secs.append(section(name,payload,flags=0x40401040))
                syms.append(symbol(name,3,storage=3,auxiliary=aux(len(payload),selection=5 if name=='.associated' else 0,association=1 if name=='.associated' else 0)))
            with self.subTest(name=name):self.assertUnsupported(*rewrite(self.raw,self.contract,self.root,change))

    def test_implicit_directive_and_weak_index_context_block(self):
        def directive(secs,syms,obj):
            secs[1]['payload']+=b' /INCLUDE:_authored_any_root';secs[1]['size']=len(secs[1]['payload'])
            syms[2]=symbol('.drectve',2,storage=3,auxiliary=aux(secs[1]['size'],selection=0))
        self.assertUnsupported(*rewrite(self.raw,self.contract,self.root,directive))
        def weak(secs,syms,obj):syms.append(symbol('_weak',0,typ=32,storage=105,auxiliary=struct.pack('<II10s',2,2,bytes(10))))
        self.assertUnsupported(*rewrite(self.raw,self.contract,self.root,weak))


if __name__=='__main__':unittest.main()
