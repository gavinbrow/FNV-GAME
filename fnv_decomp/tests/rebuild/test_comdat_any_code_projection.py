"""Producer-backed authored COMDAT composer/consumer tests; no game inputs."""
import copy
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild'),str(ROOT/'tools')]
import comdat_any_root_composer as composer
import comdat_any_code_projection as projection
import comdat_any_code_omission as witness
import coff_code_archive as coff
import root_code_closure as ordinary
import runtime_code_pool as pool
import bulk_code_pool as bulk
import compare as oracle
from test_comdat_any_code_omission import authored


def context(*,fields=True,directives=None):
    raw,contract,_,root,_=authored(fields=fields,directives=directives)
    for row in contract['fields']:
        row.update(code_ownership_ambiguous=False,code_owners=[])
    base=ordinary.assess_object(coff.parse(raw),contract)
    census=composer.reconstruct_definition_census(raw,contract,root)
    observation=witness.observe_comdat_any_code_policy(raw,contract,base,root,census,policy_id=witness.POLICY)
    wrappers=[dict(kind=composer.WITNESS_KIND,definition_census=census,observation=observation)]
    composed=composer.compose(raw,contract,base,wrappers,policy_id=composer.POLICY)
    providers={root['original_address']:{k:root[k]for k in ('recipe_id','object_sha256','symbol_index')}}
    return [raw,contract,base,wrappers,composed,[root],providers]


def project(values,**kwargs):
    return projection.project_member(*values,existing_exports=kwargs.pop('existing_exports',()),
        policy_id=kwargs.pop('policy_id',projection.POLICY),**kwargs)


class ComdatAnyIntegrationTests(unittest.TestCase):
    def test_original_negative_and_selection2_survive_code_field_projection(self):
        values=context();before=copy.deepcopy(values);output,receipt=project(values)
        self.assertEqual(values,before);self.assertFalse(values[2]['closure_observed'])
        self.assertTrue(receipt['selection2_auxiliary_preserved']);self.assertFalse(receipt['selection_rewritten'])
        self.assertEqual([e['addend_bits']for e in receipt['fields']],[4,0xfffffffc])
        self.assertEqual(coff.exports(output),receipt['exports'])
        self.assertEqual(receipt['undefined'][0]['name'],pool.unresolved('0x00600000','code'))
        old,new=coff.parse(values[0]),coff.parse(output)
        self.assertEqual(old['sections'][1]['payload'],new['sections'][receipt['maps']['section_map'][1]]['payload'])
        for symbol in new['symbols'].values():
            if symbol['name']=='.text':self.assertEqual(struct.unpack('<IHHIhBBH',symbol['aux'])[5],2)

    def test_zero_field_any_root_and_independent_reader(self):
        output,receipt=project(context(fields=False))
        self.assertFalse(receipt['fields']);self.assertFalse(receipt['undefined'])
        with tempfile.TemporaryDirectory(prefix='authored-comdat-any-')as td:
            p=Path(td)/'authored.obj';p.write_bytes(output);bulk.strict_reparse(p,output)

    def test_unchanged_comparator_before_and_after_matches_authored_dir32_rel32(self):
        values=context();output,receipt=project(values);root=values[5][0]
        image=bytearray(coff.parse(values[0])['sections'][1]['payload'])
        for row in values[1]['fields']:struct.pack_into('<I',image,row['source_field_offset'],row['original_operand'])
        class AuthoredImage:
            def read(self,address,size):
                start=address-int(root['original_address'],16)
                if start<0 or start+size>len(image):raise ValueError('authored image span')
                return bytes(image[start:start+size])
        with tempfile.TemporaryDirectory(prefix='authored-comdat-oracle-')as td:
            before=Path(td)/'before.obj';after=Path(td)/'after.obj';before.write_bytes(values[0]);after.write_bytes(output)
            for path,symbol,mapping in [(before,root['symbol'],{'_authored_target':'0x00600000'}),
                (after,receipt['exports'][0],receipt['comparison_base_view'])]:
                rows=oracle.compare(oracle.Coff(path),AuthoredImage(),dict(functions=[dict(address=root['original_address'],
                    symbol=symbol,size=root['size'])],symbols=mapping))
                self.assertEqual(rows[0]['verdict'],'match');self.assertTrue(all(r['match']for r in rows[0]['relocations']))

    def test_no_cached_assessment_or_composed_type_coercion_authority(self):
        values=context();assessed=projection.assess_member(*values,existing_exports=(),policy_id=projection.POLICY)
        self.assertTrue(assessed['eligible'])
        with self.assertRaises(TypeError):project(values,assessment=assessed)
        for key,value in [('schema_version',True),('provider_selected',0)]:
            changed=copy.deepcopy(values);changed[4][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):project(changed)

    def test_wrapper_cannot_borrow_declared_global_census(self):
        values=context();census=copy.deepcopy(values[3][0]['definition_census']);census['entries'].append(copy.deepcopy(census['entries'][0]))
        observation=witness.observe_comdat_any_code_policy(values[0],values[1],values[2],values[5][0],census,policy_id=witness.POLICY)
        wrappers=[dict(kind=composer.WITNESS_KIND,definition_census=census,observation=observation)]
        result=composer.compose(values[0],values[1],values[2],wrappers,policy_id=composer.POLICY)
        self.assertFalse(result['composed_omission_complete']);self.assertEqual(result['remaining_blockers'],values[2]['blockers'])

    def test_structured_unsupported_summary_preserves_repeated_original_ids(self):
        values=context(fields=False,directives=b' /DEFAULTLIB:"LIBCMT" /DEFAULTLIB:"OLDNAMES" /DEFAULTLIB:"uuid.lib" /DEFAULTLIB:"uuid.lib"')
        summary=composer.summarize_unsupported(*values[:5],policy_id=composer.POLICY)
        self.assertTrue(summary['selection2_observed']);self.assertFalse(summary['root_conjunct_discharge_proved'])
        self.assertEqual(summary['original_blocker_ids'],[b['blocker_id']for b in values[2]['blockers']])
        self.assertEqual(summary['remaining_blocker_ids'],summary['original_blocker_ids'])
        self.assertFalse(summary['discharged_blocker_ids'])
        assessed=projection.assess_member(*values,existing_exports=(),policy_id=projection.POLICY)
        self.assertFalse(assessed['eligible']);self.assertEqual(assessed['unsupported_summary'],summary)
        with patch.object(coff,'serialize',side_effect=AssertionError('blocked serialization forbidden')):
            with self.assertRaises(ValueError):project(values)

    def test_native_census_preflight_distinguishes_partial_form_from_corruption(self):
        values=context(fields=False);root=copy.deepcopy(values[5][0]);contract=copy.deepcopy(values[1])
        result=composer.assess_native_definition(values[0],contract,values[2],root,policy_id=composer.POLICY)
        self.assertTrue(result['eligible']);self.assertFalse(result['candidate_policy_evaluated'])
        self.assertEqual(result['definition_census'],values[3][0]['definition_census'])
        root['size']=8;contract['roots'][0]['size']=8;contract['unit_verified_functions'][0]['size']=8
        base=ordinary.assess_object(coff.parse(values[0]),contract)
        result=composer.assess_native_definition(values[0],contract,base,root,policy_id=composer.POLICY)
        self.assertFalse(result['eligible']);self.assertIsNone(result['definition_census'])
        self.assertIn('ROOT_NOT_EXACT_WHOLE_NATIVE_SECTION',{b['code']for b in result['blockers']})
        with self.assertRaises(ValueError):
            composer.assess_native_definition(values[0]+b'changed',contract,base,root,policy_id=composer.POLICY)


if __name__=='__main__':unittest.main()
