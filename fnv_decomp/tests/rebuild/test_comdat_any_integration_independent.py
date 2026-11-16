"""Independent pure COMDAT-ANY integration fixtures; no original artifacts."""
from pathlib import Path
import copy
import importlib
import hashlib
import struct
import sys
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import coff_code_archive as coff
import root_code_closure as ordinary
import runtime_code_pool as pool
import comdat_any_code_omission as typed
from test_comdat2_code_policy_independent import fixture,field_fixture,census_for
from test_coff_code_archive import object_bytes,section,symbol,aux


def authored(fields=False):
    raw,k,root=fixture();k['provenance'].update(recipe_id=root['recipe_id'],recipe_index=root['recipe_index'])
    if fields:
        raw,k,root=field_fixture(raw,k,root)
        for row in k['fields']:
            row.update(recipe_index=root['recipe_index'],function_symbol=root['symbol'],
                source_resolution_basis='OWN_RECIPE_BINDING',code_ownership_ambiguous=False,
                code_owners=[dict(address=root['original_address'],offset=4)],
                expected_original_target_va=row['exact_original_target_va'],
                original_field_va='0x%08x'%(int(root['original_address'],16)+row['source_field_offset']),
                original_operand=int(row['exact_original_target_va'],16))
    base=ordinary.assess_object(coff.parse(raw),k);census=census_for(root)
    observation=typed.observe_comdat_any_code_policy(raw,k,base,root,census,policy_id=typed.POLICY)
    witness=dict(kind='typed-comdat-any-code-witness',definition_census=census,observation=observation)
    providers={root['original_address']:{x:root[x] for x in ('recipe_id','object_sha256','symbol_index')}}
    return raw,k,base,[witness],[root],providers


def shifted_authored():
    raw,k,_,_,roots,_=authored(fields=True);r=copy.deepcopy(roots[0]);obj=coff.parse(raw)
    secs=[section('.debug$S',b'authored-debug',flags=0x42100040)]+copy.deepcopy(list(obj['sections'].values()))
    for sec in secs[1:]:sec['relocs']=[(off,index+2,kind) for off,index,kind in sec['relocs']]
    syms=[symbol('.debug$S',1,storage=3,auxiliary=aux(len(secs[0]['payload']),selection=0))]
    syms.extend(symbol(s['name'],s['section']+1 if s['section']>0 else s['section'],s['value'],s['type'],s['storage'],s['aux']) for s in obj['symbols'].values())
    raw=object_bytes(secs,syms);k=copy.deepcopy(k);h=hashlib.sha256(raw).hexdigest()
    r.update(section=r['section']+1,symbol_index=r['symbol_index']+2,object_sha256=h);k['provenance']['object_sha256']=h
    k['roots'][0].update(section=r['section'],symbol_index=r['symbol_index']);k['unit_verified_functions'][0]['section']=r['section']
    for row in k['fields']:
        row['physical_section']+=1;row['coff_relocation']['symbol_index']+=2;row['coff_relocation']['symbol_section']+=1
    base=ordinary.assess_object(coff.parse(raw),k);census=census_for(r)
    w=dict(kind='typed-comdat-any-code-witness',definition_census=census,
        observation=typed.observe_comdat_any_code_policy(raw,k,base,r,census,policy_id=typed.POLICY))
    return raw,k,base,[w],[r],{r['original_address']:{key:r[key] for key in ('recipe_id','object_sha256','symbol_index')}}


def external_authored(selected=True,addend=0):
    raw,k,_,_,roots,providers=authored();r=copy.deepcopy(roots[0]);obj=coff.parse(raw);secs=copy.deepcopy(list(obj['sections'].values()))
    offsets=[(0,6,6)] if selected else [(0,6,6),(4,6,20)]
    payload=bytearray(secs[0]['payload']);struct.pack_into('<I',payload,0,addend if selected else 4)
    if not selected:struct.pack_into('<I',payload,4,0xfffffffc)
    secs[0].update(payload=bytes(payload),relocs=offsets)
    syms=[symbol(s['name'],s['section'],s['value'],s['type'],s['storage'],s['aux']) for s in obj['symbols'].values()]
    syms[0]=symbol('.text',1,storage=3,auxiliary=aux(len(payload),len(offsets),selection=2));syms.append(symbol('_external_code',0,typ=32))
    raw=object_bytes(secs,syms);h=hashlib.sha256(raw).hexdigest();r['object_sha256']=h;k=copy.deepcopy(k);k['provenance']['object_sha256']=h;k['fields']=[]
    target_base=0x01002000;root_va=int(r['original_address'],16)
    for off,index,kind in offsets:
        bits=int.from_bytes(payload[off:off+4],'little');add=bits if kind==6 or bits<0x80000000 else bits-0x100000000;final=(target_base+add)&0xffffffff
        k['fields'].append(dict(recipe_id=r['recipe_id'],recipe_index=r['recipe_index'],function_va=r['original_address'],function_symbol=r['symbol'],
            physical_section=1,physical_offset=off,source_field_offset=off,physical_field_overlap_count=1,
            coff_relocation=dict(offset=off,symbol_index=index,kind=kind,width=4,addend=bits,symbol='_external_code',symbol_section=0,symbol_value=0,symbol_type=32,symbol_storage=2),
            derived_source_symbol_base_va='0x01002000',exact_original_target_va=f'0x{final:08x}',expected_original_target_va=f'0x{final:08x}',
            original_field_va=f'0x{root_va+off:08x}',original_operand=final if kind==6 else (final-root_va-off-4)&0xffffffff,
            source_resolution_basis='OWN_RECIPE_BINDING',proof_consistency='EXACT_OWN_SOURCE_RESOLUTION',
            classification='SELECTED_CODE_ENTRY' if selected else 'UNSELECTED_EXECUTABLE_TARGET_UNCLASSIFIED',code_ownership_ambiguous=False,
            code_owners=[dict(address='0x01002000',offset=0)] if selected else []))
    providers={r['original_address']:{x:r[x] for x in ('recipe_id','object_sha256','symbol_index')}}
    if selected:providers['0x01002000']=dict(recipe_id='authored-other',object_sha256='b'*64,symbol_index=4)
    base=ordinary.assess_object(coff.parse(raw),k);census=census_for(r)
    wrapper=dict(kind='typed-comdat-any-code-witness',definition_census=census,
        observation=typed.observe_comdat_any_code_policy(raw,k,base,r,census,policy_id=typed.POLICY))
    return raw,k,base,[wrapper],[r],providers


class IntegrationBaseline(unittest.TestCase):
    def test_typed_wrapper_contains_real_negative_base_and_selection2(self):
        raw,k,base,witnesses,roots,providers=authored()
        self.assertFalse(base['closure_observed']);self.assertEqual(len(base['blockers']),1)
        self.assertTrue(witnesses[0]['observation']['witness_complete'])
        self.assertEqual(struct.unpack('<IHHIhBBH',coff.parse(raw)['symbols'][0]['aux'])[5],2)
        self.assertEqual(pool.canonical(providers[roots[0]['original_address']]),witnesses[0]['observation']['planned_canonical_name'])


class IndependentComposerTests(unittest.TestCase):
    def setUp(self):self.composer=importlib.import_module('comdat_any_root_composer')

    def compose(self,values):
        raw,k,base,witnesses,roots,providers=values
        return self.composer.compose(raw,k,base,witnesses,policy_id=self.composer.POLICY)

    def test_exact_witness_composes_without_promoting_negative_base(self):
        values=authored();before=copy.deepcopy(values);result=self.compose(values)
        self.assertEqual(result['kind'],'comdat-any-composed-root-observation')
        self.assertTrue(result['composed_omission_complete']);self.assertEqual(len(result['discharged_blockers']),1)
        self.assertEqual(result['remaining_blockers'],[]);self.assertEqual(result['remaining_blocker_occurrences'],[])
        self.assertEqual(result['base_certificate'],values[2]);self.assertFalse(result['base_certificate']['closure_observed'])
        for key in self.composer.FALSE:self.assertIs(result[key],False)
        self.assertEqual(values,before)

    def test_blocked_valid_witness_preserves_full_negative_occurrences(self):
        values=list(authored());census=copy.deepcopy(values[3][0]['definition_census']);census['entries']=[]
        values[3]=[dict(kind='typed-comdat-any-code-witness',definition_census=census,
            observation=typed.observe_comdat_any_code_policy(values[0],values[1],values[2],values[4][0],census,policy_id=typed.POLICY))]
        result=self.compose(values)
        self.assertFalse(result['composed_omission_complete']);self.assertEqual(result['discharged_blockers'],[])
        self.assertEqual(result['remaining_blockers'],values[2]['blockers'])

    def test_unknown_duplicate_or_extended_wrapper_cannot_discharge(self):
        for mode in ('unknown','duplicate','extra'):
            values=list(authored());values[3]=copy.deepcopy(values[3])
            if mode=='unknown':values[3][0]['kind']='typed-local-label-omission-witness'
            elif mode=='duplicate':values[3]*=2
            else:values[3][0]['namespace_approved']=True
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.compose(values)

    def test_typed_observation_and_base_cannot_be_coerced_by_equality(self):
        for mode in ('schema_bool','false_zero','candidate_false','base_schema_bool'):
            values=list(authored());values[3]=copy.deepcopy(values[3]);values[2]=copy.deepcopy(values[2])
            if mode=='schema_bool':values[3][0]['observation']['schema_version']=True
            elif mode=='false_zero':values[3][0]['observation']['provider_selected']=0
            elif mode=='candidate_false':values[3][0]['observation']['root_comdat2_policy_candidate']=False
            else:values[2]['schema_version']=True
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.compose(values)

    def test_original_scope_and_explicit_policy_are_mandatory(self):
        values=authored();raw,k,base,witnesses,_,_=values
        with self.assertRaises(TypeError):self.composer.compose(raw,k,base,witnesses)
        with self.assertRaises(ValueError):self.composer.compose(raw,k,base,witnesses,policy_id='unrelated')
        bad=copy.deepcopy(base);bad['closure_observed']=True
        with self.assertRaises(ValueError):self.composer.compose(raw,k,bad,witnesses,policy_id=self.composer.POLICY)

    def test_complete_declared_census_must_equal_reconstructed_original_definition(self):
        values=list(authored());census=copy.deepcopy(values[3][0]['definition_census']);other=copy.deepcopy(values[4][0])
        other.update(original_address='0x01002000',recipe_id='authored-other',recipe_index=1,object_sha256='b'*64,source_sha256='c'*64)
        census['entries']+=census_for(other)['entries']
        observation=typed.observe_comdat_any_code_policy(values[0],values[1],values[2],values[4][0],census,policy_id=typed.POLICY)
        self.assertTrue(observation['witness_complete'])
        values[3]=[dict(kind='typed-comdat-any-code-witness',definition_census=census,observation=observation)]
        with self.assertRaises(ValueError):self.compose(values)


class IndependentConsumerTests(unittest.TestCase):
    def setUp(self):
        self.composer=importlib.import_module('comdat_any_root_composer');self.consumer=importlib.import_module('comdat_any_code_projection')

    def compose(self,v):return self.composer.compose(*v[:4],policy_id=self.composer.POLICY)

    def assess(self,v,composed=None,exports=None):
        return self.consumer.assess_member(*v[:4],self.compose(v) if composed is None else composed,*v[4:],
            existing_exports=[] if exports is None else exports,policy_id=self.consumer.POLICY)

    def project(self,v,composed=None,exports=None):
        return self.consumer.project_member(*v[:4],self.compose(v) if composed is None else composed,*v[4:],
            existing_exports=[] if exports is None else exports,policy_id=self.consumer.POLICY)

    def test_zero_field_serialization_preserves_ANY_and_original_negative(self):
        v=authored();before=copy.deepcopy(v);self.assertTrue(self.assess(v)['eligible'])
        output,receipt=self.project(v);old,new=coff.parse(v[0]),coff.parse(output);maps=receipt['maps']
        self.assertEqual(coff.exports(output),receipt['exports']);self.assertEqual(len(receipt['exports']),1)
        for oldindex,newindex in maps['section_map'].items():
            self.assertEqual(old['sections'][oldindex]['payload'],new['sections'][newindex]['payload'])
            self.assertEqual(old['sections'][oldindex]['flags'],new['sections'][newindex]['flags'])
        self.assertEqual(old['symbols'][0]['aux'],new['symbols'][maps['symbol_map'][0]]['aux'])
        self.assertEqual(struct.unpack('<IHHIhBBH',new['symbols'][maps['symbol_map'][0]]['aux'])[5],2)
        self.assertFalse(v[2]['closure_observed']);self.assertEqual(v,before)
        self.assertTrue(receipt['serialization_performed']);self.assertFalse(receipt['artifact_disk_write_performed'])
        for key in self.consumer.FALSE:self.assertIs(receipt[key],False)

    def test_shifted_maps_and_self_addend_use_root_base_not_interior_provider(self):
        v=shifted_authored();self.assertTrue(self.assess(v)['eligible']);output,receipt=self.project(v);maps=receipt['maps']
        self.assertEqual(maps['section_map'],{2:1,3:2});self.assertEqual(maps['symbol_map'],{2:0,4:2,5:3,7:5})
        self.assertEqual(maps['auxiliary_map'],{3:1,6:4});self.assertEqual(maps['undefined_conversions'],[])
        old,new=coff.parse(v[0]),coff.parse(output)
        self.assertEqual(new['sections'][1]['relocs'],[(0,2,6)])
        self.assertEqual(new['sections'][1]['payload'],old['sections'][2]['payload'])
        self.assertEqual(int.from_bytes(new['sections'][1]['payload'][:4],'little'),4)
        name=receipt['exports'][0];self.assertEqual(receipt['comparison_base_view'],{name:v[4][0]['original_address']})
        self.assertEqual(receipt['undefined'],[]);self.assertTrue(receipt['fields'][0]['retained_self_reference'])

    def test_typed_composed_replay_rejects_bool_and_promoted_flags(self):
        v=authored()
        for mode in ('schema_bool','false_zero','nested_base_bool','root_bool','omission_false'):
            c=copy.deepcopy(self.compose(v))
            if mode=='schema_bool':c['schema_version']=True
            elif mode=='false_zero':c['provider_selected']=0
            elif mode=='nested_base_bool':c['base_certificate']['schema_version']=True
            elif mode=='root_bool':c['roots'][0]['section']=True
            else:c['composed_omission_complete']=False
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.project(v,composed=c)

    def test_requested_root_and_provider_typed_identity_must_match(self):
        for mode in ('root_bool','provider_float','provider_extra','provider_missing'):
            v=list(authored());v[4]=copy.deepcopy(v[4]);v[5]=copy.deepcopy(v[5]);address=v[4][0]['original_address']
            if mode=='root_bool':v[4][0]['recipe_index']=False
            elif mode=='provider_float':v[5][address]['symbol_index']=2.0
            elif mode=='provider_extra':v[5][address]['provider_selected']=True
            else:v[5]={}
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.project(v)

    def test_preexisting_export_and_duplicate_census_refuse_projection(self):
        v=authored();name=pool.canonical(v[5][v[4][0]['original_address']])
        for exports in ([name],['_other','_other']):
            with self.subTest(exports=exports),self.assertRaises(ValueError):self.project(v,exports=exports)

    def test_valid_incomplete_composition_can_be_assessed_but_not_projected(self):
        v=list(authored());census=copy.deepcopy(v[3][0]['definition_census']);census['entries']=[]
        v[3]=[dict(kind='typed-comdat-any-code-witness',definition_census=census,
            observation=typed.observe_comdat_any_code_policy(v[0],v[1],v[2],v[4][0],census,policy_id=typed.POLICY))]
        result=self.assess(v);self.assertFalse(result['eligible']);self.assertEqual(result['blockers'],v[2]['blockers'])
        with self.assertRaises(ValueError):self.project(v)

    def test_independent_original_operand_and_owner_proofs_remain_fatal(self):
        for mode in ('operand','owners','source_basis','field_bool'):
            v=list(authored(fields=True));v[1]=copy.deepcopy(v[1]);row=v[1]['fields'][0]
            if mode=='operand':row['original_operand']=0
            elif mode=='owners':row['code_owners']=[dict(address=v[4][0]['original_address'],offset=0)]
            elif mode=='source_basis':row['source_resolution_basis']='EXACT_LOCAL_FUNCTION_CONTAINMENT'
            else:row['recipe_index']=False
            v[2]=ordinary.assess_object(coff.parse(v[0]),v[1]);census=v[3][0]['definition_census']
            v[3]=[dict(kind='typed-comdat-any-code-witness',definition_census=census,
                observation=typed.observe_comdat_any_code_policy(v[0],v[1],v[2],v[4][0],census,policy_id=typed.POLICY))]
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.project(v)

    def test_selected_external_CODE_is_an_exact_undefined_canonical_entry(self):
        v=external_authored();self.assertTrue(self.assess(v)['eligible']);output,r=self.project(v);obj=coff.parse(output)
        expected=pool.canonical(v[5]['0x01002000']);self.assertEqual(len(r['undefined']),1)
        self.assertEqual(r['undefined'][0]['name'],expected);self.assertEqual(r['comparison_base_view'][expected],'0x01002000')
        symbol=obj['symbols'][r['maps']['symbol_map'][6]];self.assertEqual((symbol['name'],symbol['section'],symbol['value'],symbol['storage']),(expected,0,0,2))
        self.assertEqual(coff.exports(output),r['exports'])

    def test_external_CODE_addend_cannot_invent_selected_interior_provider(self):
        with self.assertRaises(ValueError):self.project(external_authored(addend=4))

    def test_unselected_CODE_preserves_DIR32_and_signed_REL32_addends(self):
        v=external_authored(selected=False);self.assertTrue(self.assess(v)['eligible']);output,r=self.project(v);before,after=coff.parse(v[0]),coff.parse(output)
        self.assertEqual(after['sections'][1]['payload'],before['sections'][1]['payload'])
        self.assertEqual([f['addend_bits'] for f in r['fields']],[4,0xfffffffc])
        name=pool.unresolved('0x01002000','code');self.assertEqual(r['undefined'][0]['name'],name)
        self.assertEqual(r['comparison_base_view'][name],'0x01002000');self.assertEqual(len(r['exports']),1)

    def test_unselected_CODE_cannot_hide_a_selected_provider_contradiction(self):
        v=list(external_authored(selected=False));v[5]['0x01002000']=dict(recipe_id='authored-other',object_sha256='b'*64,symbol_index=4)
        with self.assertRaises(ValueError):self.project(v)

    def test_stale_original_field_parent_is_retained_as_independent_blocker(self):
        v=list(authored(fields=True));v[1]=copy.deepcopy(v[1]);v[1]['fields'][0].update(source_field_offset=4,original_field_va='0x01001004')
        v[2]=ordinary.assess_object(coff.parse(v[0]),v[1]);census=v[3][0]['definition_census']
        v[3]=[dict(kind='typed-comdat-any-code-witness',definition_census=census,
            observation=typed.observe_comdat_any_code_policy(v[0],v[1],v[2],v[4][0],census,policy_id=typed.POLICY))]
        c=self.compose(v);self.assertFalse(c['composed_omission_complete'])
        self.assertIn('STALE_FIELD_PARENT',{b['code'] for b in c['remaining_blockers']})
        self.assertFalse(self.assess(v,c)['eligible'])
        with self.assertRaises(ValueError):self.project(v,c)


class IndependentNativePreflightTests(unittest.TestCase):
    def setUp(self):self.composer=importlib.import_module('comdat_any_root_composer')

    def assess(self,v):return self.composer.assess_native_definition(v[0],v[1],v[2],v[4][0],policy_id=self.composer.POLICY)

    def test_native_qualification_is_census_only_and_never_evaluates_candidate_policy(self):
        v=authored();before=copy.deepcopy(v)
        with patch.object(typed,'observe_comdat_any_code_policy',side_effect=AssertionError('candidate policy not allowed')):
            r=self.assess(v)
        self.assertTrue(r['eligible']);self.assertFalse(r['candidate_policy_evaluated']);self.assertFalse(r['serialization_performed'])
        self.assertEqual(r['definition_census'],v[3][0]['definition_census'])
        self.assertEqual(r['original_blocker_ids'],[b['blocker_id'] for b in v[2]['blockers']]);self.assertEqual(v,before)
        for key in self.composer.FALSE:self.assertIs(r[key],False)

    def test_valid_partial_and_alias_ownership_are_structured_unsupported(self):
        v=list(authored());v[1]=copy.deepcopy(v[1]);v[4]=copy.deepcopy(v[4])
        v[4][0]['size']-=1;v[1]['roots'][0]['size']-=1;v[1]['unit_verified_functions'][0]['size']-=1
        v[2]=ordinary.assess_object(coff.parse(v[0]),v[1])
        r=self.assess(v);self.assertFalse(r['eligible']);self.assertIsNone(r['definition_census']);self.assertTrue(r['blockers'])
        v=list(authored());obj=coff.parse(v[0]);syms=[symbol(s['name'],s['section'],s['value'],s['type'],s['storage'],s['aux']) for s in obj['symbols'].values()]
        syms.append(symbol('_other_definition',1,value=4,typ=32));v[0]=object_bytes(list(obj['sections'].values()),syms)
        h=hashlib.sha256(v[0]).hexdigest();v[1]=copy.deepcopy(v[1]);v[4]=copy.deepcopy(v[4]);v[1]['provenance']['object_sha256']=h;v[4][0]['object_sha256']=h
        v[2]=ordinary.assess_object(coff.parse(v[0]),v[1]);r=self.assess(v)
        self.assertFalse(r['eligible']);self.assertIsNone(r['definition_census'])
        self.assertEqual(r['original_blocker_ids'],[b['blocker_id'] for b in v[2]['blockers']])

    def test_selection1_with_real_independent_negative_is_not_ANY(self):
        raw,k,root=fixture(selection=1);k['provenance'].update(recipe_id=root['recipe_id'],recipe_index=root['recipe_index']);k['missing_fields']=[dict(authored_missing=True)]
        base=ordinary.assess_object(coff.parse(raw),k);self.assertFalse(base['closure_observed'])
        r=self.composer.assess_native_definition(raw,k,base,root,policy_id=self.composer.POLICY)
        self.assertFalse(r['eligible']);self.assertIsNone(r['definition_census']);self.assertFalse(r['candidate_policy_evaluated'])

    def test_corrupt_identity_hash_base_and_schema_remain_fatal(self):
        for mode in ('hash','name','base_bool','root_bool','schema'):
            v=list(authored());v[1]=copy.deepcopy(v[1]);v[4]=copy.deepcopy(v[4]);v[2]=copy.deepcopy(v[2])
            if mode=='hash':v[4][0]['object_sha256']='0'*64
            elif mode=='name':
                v[4][0]['symbol']='_invented';v[1]['roots'][0]['symbol']='_invented';v[1]['unit_verified_functions'][0]['symbol']='_invented'
                v[2]=ordinary.assess_object(coff.parse(v[0]),v[1])
            elif mode=='base_bool':v[2]['schema_version']=True
            elif mode=='root_bool':v[4][0]['section']=True
            else:v[1]['unexpected']=True
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.assess(v)


if __name__=='__main__':unittest.main()
