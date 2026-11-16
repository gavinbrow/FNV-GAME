import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import crt_frontier_adoption_plan as plan

class ExpandedPlanTests(unittest.TestCase):
    def test_preparation_receipt_and_actual_link_ancestry_are_distinct(self):
        observation=dict(baseline_V6_receipt_sha256='prepared')
        review=dict(prepared_receipt_sha256='prepared',link_receipt_sha256='actual-link')
        plan.ancestry(observation,review,'prepared','actual-link')
        with self.assertRaises(ValueError):plan.ancestry(observation,review,'actual-link','actual-link')
    def fixture(self,index):
        helper=index==509
        base,role,kind,symbol,contract,consistency,family,section,outsection,outindex,domain=(
            ('0x00ec408c','crt-contract',20,'@__security_check_cookie@4','security-cookie-check',
             'EXACT_GENERATED_EH_FIELD_RESOLUTION','PARENT_OWNED_GENERATED_EH_FIELD',242,4,6,'code') if helper else
            ('0x011c16bc','data',6,'___security_cookie','security-cookie',
             'EXACT_OWN_SOURCE_RESOLUTION','PARENT_FINAL_BINDING',241,3,4,'data'))
        identity=dict(base=int(base,0),contract_kind=contract,proof_consistency=consistency,role=role,
            semantic_domain=domain,symbol=symbol,symbol_index=index)
        raw=dict(section=section,offset=21,target_index=index,kind=kind,addend=0,original_base=int(base,0),
            original_target=int(base,0),proof_family=family,output_section=outsection,output_target_index=outindex,
            external_identity=identity)
        field=dict(component='EHFile',member='component.obj',root='0x005e0200',recipe_id='2656-e9bf85b93a320794',
            object_sha256='1'*64,member_sha256='2'*64,section=outsection,symbol_index=outindex,offset=21,
            kind=kind,canonical=plan.old.undefined(base,role),undefined=True,physical_symbol_index=index,
            proof=dict(external_identity=copy.deepcopy(identity),proof_family=family,physical_section=section,
                field_offset=21,kind=kind,addend_bits=0,symbol_index=index,role=role,original_base=base,original_target=base,
                canonical_name=plan.old.undefined(base,role)))
        witnessed={k:v for k,v in raw.items() if k not in ['output_section','output_target_index','external_identity']}
        record=dict(root=dict(object_sha256='1'*64),source='example.cpp',result=dict(blockers=[],
            structural_projection_candidate=True,semantic=dict(object_sha256='1'*64,fields=[witnessed],external_obligations=[identity],
                comparisons=[dict(nonfield_differences=0)])),central_contract=dict(fields=[dict(
                    coff_relocation=dict(symbol_index=506,symbol='___security_cookie'),
                    proof_consistency='EXACT_OWN_SOURCE_RESOLUTION',source_resolution_basis='OWN_RECIPE_BINDING')]))
        integration=dict(fields=[raw],source_object_sha256='1'*64,object_sha256='2'*64)
        unit=dict(compiler='sp1',flags=['/MT','/GS','/EHsc'],source='example.cpp',symbols={'___security_cookie':'0x011c16bc'})
        return field,integration,record,unit
    def bindings(self):
        return [dict(canonical_undefined=plan.old.undefined(b,r),normal_export=e,enabled=True,disabled_reasons=[])
                for b,r,e,k in plan.old.BINDINGS]
    def test_parent_and_generated_proofs_remain_distinct(self):
        for index,expected in [(506,'EXACT_OWN_SOURCE_RESOLUTION'),(509,'EXACT_GENERATED_EH_FIELD_RESOLUTION')]:
            evidence,reason=plan.new_field_evidence(*self.fixture(index))
            self.assertIsNone(reason);self.assertEqual(evidence['proof_consistency'],expected)
            self.assertFalse(evidence['runtime_frame_or_ABI_approved'])
    def test_generated_field_class_survives_agreeing_recipe_symbol(self):
        args=self.fixture(509);args[0]['proof']['external_identity']['proof_consistency']='EXACT_OWN_SOURCE_RESOLUTION'
        self.assertIsNotNone(plan.new_field_evidence(*args)[1])
        args=self.fixture(509);args[3]['symbols']['@__security_check_cookie@4']='0x00ec408c'
        evidence,reason=plan.new_field_evidence(*args)
        self.assertIsNone(reason);self.assertEqual(evidence['proof_consistency'],'EXACT_GENERATED_EH_FIELD_RESOLUTION')
        args[3]['symbols']['@__security_check_cookie@4']='0x00ec408d'
        self.assertIsNotNone(plan.new_field_evidence(*args)[1])
    def test_changed_physical_or_serialized_identity_blocks(self):
        for key,value in [('physical_symbol_index',508),('symbol_index',7),('member_sha256','3'*64)]:
            args=self.fixture(509);args[0][key]=value
            self.assertIsNotNone(plan.new_field_evidence(*args)[1])
    def test_nonzero_addend_wrong_recipe_and_failed_comparison_block(self):
        args=self.fixture(506);args[0]['proof']['addend_bits']=4
        self.assertIsNotNone(plan.new_field_evidence(*args)[1])
        args=self.fixture(509);args[3]['compiler']='vc8'
        self.assertIsNotNone(plan.new_field_evidence(*args)[1])
        args=self.fixture(509);args[2]['result']['semantic']['comparisons'][0]['nonfield_differences']=1
        self.assertIsNotNone(plan.new_field_evidence(*args)[1])
    def test_uncertainty_disables_both_cookie_owners_only(self):
        rows=self.bindings();rows[0]['enabled']=False;rows[0]['disabled_reasons']=['uncertain witness']
        plan.coupled_disable(rows)
        self.assertEqual([x['enabled'] for x in rows],[False,False,True,True])
    def test_response_selects_existing_tokens_and_forbids_new_alias(self):
        rows=self.bindings();previous=plan.old.response(rows).replace('\n','\r\n').encode()
        self.assertEqual(plan.response_bytes(rows,previous),previous)
        rows[0]['enabled']=False;plan.coupled_disable(rows)
        selected=plan.response_bytes(rows,previous)
        self.assertEqual(len(selected.splitlines()),2)
        rows[3]['normal_export']='_strcpy_s'
        with self.assertRaises(ValueError):plan.response_bytes(rows,previous)
    def test_half_cookie_response_rejected(self):
        rows=self.bindings();previous=plan.old.response(rows).replace('\n','\r\n').encode()
        rows[0]['enabled']=False
        with self.assertRaises(ValueError):plan.response_bytes(rows,previous)

if __name__=='__main__':unittest.main()
