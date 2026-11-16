"""Authored COMDAT ANY CODE metadata; no original inputs or object emission."""
import copy
import hashlib
from pathlib import Path
import struct
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import comdat_any_code_omission as candidate
import coff_code_archive as coff
import root_code_closure as ordinary
import runtime_code_pool as pool
from test_coff_code_archive import object_bytes,section,symbol,aux


def authored(*,fields=True,data_reference=False,directives=None):
    directives=directives or b' /DEFAULTLIB:"LIBCMT" /DEFAULTLIB:"OLDNAMES"'
    payload=struct.pack('<II',4,0xfffffffc)+bytes(8)
    relocs=[(0,5,6),(4,5,20)] if fields else []
    raw=object_bytes([section('.text',payload,0x60501020,relocs),section('.drectve',directives,0x100a00)],
        [symbol('.text',1,storage=3,auxiliary=aux(16,len(relocs),selection=2)),symbol('_authored_root',1,typ=32),
         symbol('.drectve',2,storage=3,auxiliary=aux(len(directives),selection=0)),
         symbol('_authored_target',0,typ=0 if data_reference else 32)])
    h=hashlib.sha256(raw).hexdigest();root=dict(original_address='0x00500000',recipe_id='authored',recipe_index=0,
        object_sha256=h,source_sha256='b'*64,symbol='_authored_root',symbol_index=2,section=1,value=0,size=16)
    proof=[]
    for off,si,kind in relocs:
        bits=struct.unpack_from('<I',payload,off)[0];add=bits if kind==6 or bits<0x80000000 else bits-0x100000000
        final=(0x00600000+add)&0xffffffff;fv=0x00500000+off
        proof.append(dict(recipe_id='authored',recipe_index=0,function_va='0x00500000',function_symbol='_authored_root',
            physical_section=1,physical_offset=off,source_field_offset=off,original_field_va='0x%08x'%fv,
            coff_relocation=dict(offset=off,symbol_index=5,kind=kind,width=4,symbol='_authored_target',symbol_section=0,
                symbol_value=0,symbol_type=0 if data_reference else 32,symbol_storage=2,addend=bits),
            derived_source_symbol_base_va='0x00600000',exact_original_target_va='0x%08x'%final,
            expected_original_target_va='0x%08x'%final,original_operand=(final-(fv+4 if kind==20 else 0))&0xffffffff,
            classification='ORIGINAL_IMAGE_DATA_REQUIRES_CANONICAL_OWNER' if data_reference else 'UNSELECTED_EXECUTABLE_TARGET_UNCLASSIFIED',
            source_resolution_basis='OWN_RECIPE_BINDING',proof_consistency='EXACT_OWN_SOURCE_RESOLUTION',physical_field_overlap_count=1))
    native={k:root[k]for k in candidate.NATIVE_KEYS}
    contract=dict(recipe_id='authored',roots=[native],export_policy=ordinary.EXPORT_POLICY,verified_match=True,
        fields_complete=True,missing_fields_complete=True,unit_proofs_complete=True,fields=proof,missing_fields=[],
        parent_eh=[],omission_field_proofs=[],unit_verified_functions=[dict(address=root['original_address'],symbol=root['symbol'],
        section=1,value=0,size=16,verdict='match')],iat_import_observation={},
        provenance={k:root[k]for k in ('recipe_id','recipe_index','object_sha256','source_sha256')})
    base=ordinary.assess_object(coff.parse(raw),contract)
    census=dict(schema_version=1,kind='planned-code-definition-census',complete=True,
        entries=[dict(root=copy.deepcopy(root),planned_canonical_name=pool.canonical({k:root[k]for k in ('recipe_id','object_sha256','symbol_index')}))])
    return raw,contract,base,root,census


def observe(values):return candidate.observe_comdat_any_code_policy(*values,policy_id=candidate.POLICY)


class ComdatAnyCodePolicyTests(unittest.TestCase):
    def test_nonzero_dir32_and_negative_rel32_addend_facts_are_unchanged(self):
        values=authored();before=copy.deepcopy(values);result=observe(values)
        self.assertTrue(result['witness_complete']);self.assertEqual(values,before)
        self.assertEqual([r['addend_bits']for r in result['root_relocations']],[4,0xfffffffc])
        self.assertEqual(result['root_section_auxiliary'][5],2)
        self.assertEqual(result['root_section_flags'],0x60501020)
        self.assertEqual(result['original_numeric_primary_indices'],[0,2,3,5])
        self.assertEqual(result['complete_root_field_proof_sha256'],candidate.digest(values[1]['fields']))

    def test_policy_observer_never_calls_namespace_or_serializer(self):
        with patch.object(coff,'namespace',side_effect=AssertionError('namespace forbidden')),\
             patch.object(coff,'serialize',side_effect=AssertionError('emission forbidden')):
            result=observe(authored())
        for key in candidate.FALSE:self.assertIs(result[key],False)
        self.assertFalse(result['selection_rewritten']);self.assertFalse(result['original_object_changed'])

    def test_unowned_undefined_data_reference_requires_separate_proof(self):
        result=observe(authored(data_reference=True))
        self.assertFalse(result['witness_complete']);self.assertEqual(result['discharge_blocker_ids'],[])
        self.assertIn('UNOWNED_OR_SHARED_DATA_REFERENCE',{b['code']for b in result['policy_blockers']})

    def test_independent_repeated_directive_occurrences_remain_in_original_order(self):
        values=authored(fields=False,directives=b' /DEFAULTLIB:"LIBCMT" /DEFAULTLIB:"OLDNAMES" /DEFAULTLIB:"uuid.lib" /DEFAULTLIB:"uuid.lib"')
        base=copy.deepcopy(values[2]);result=observe(values)
        self.assertFalse(result['witness_complete']);self.assertFalse(result['discharge_blocker_ids'])
        self.assertEqual(result['remaining_base_blockers'],base['blockers'])
        repeated=[b for b in base['blockers']if b['code']=='UNSUPPORTED_IMPLICIT_LINKER_DIRECTIVE']
        self.assertEqual(len(repeated),2);self.assertEqual(repeated[0]['blocker_id'],repeated[1]['blocker_id'])
        self.assertEqual(values[2],base)

    def test_boolean_native_owner_metadata_cannot_stand_in_for_section_one(self):
        values=list(authored());values[1]['unit_verified_functions'][0]['section']=True
        values[2]=ordinary.assess_object(coff.parse(values[0]),values[1]);result=observe(values)
        self.assertFalse(result['witness_complete']);self.assertFalse(result['discharge_blocker_ids'])

    def test_negative_base_replay_preserves_json_types_not_python_numeric_aliases(self):
        for key,value in [('schema_version',True),('provider_selected',0)]:
            values=list(authored());values[2][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):observe(values)


if __name__=='__main__':unittest.main()
