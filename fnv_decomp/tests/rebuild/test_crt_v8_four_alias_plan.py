import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import crt_v8_four_alias_plan as plan

class V8ProofTests(unittest.TestCase):
    def ordinary(self,helper):
        base,role,export,kind,index,offset,outindex=(
            ('0x00ec408c','crt-contract','@__security_check_cookie@4',20,31,119,5) if helper else
            ('0x011c16bc','data','___security_cookie',6,28,10,4))
        name=plan.old.undefined(base,role)
        norm=dict(proof_consistency='EXACT_OWN_SOURCE_RESOLUTION',source_resolution_basis='OWN_RECIPE_BINDING',
            recipe_id='0576-dd603b7071c482c6',function_va='0x0086d500',physical_section=24,source_field_offset=offset,
            coff_relocation=dict(symbol=export,symbol_index=index,kind=kind,addend=0,symbol_section=0,symbol_storage=2,symbol_value=0))
        digest=plan.factory.digest(norm)
        raw=dict(section=24,offset=offset,symbol_index=index,kind=kind,addend_bits=0,original_base=base,
            original_target=base,role=role,canonical_name=name,field_proof_sha256=digest)
        field=dict(component='CODE59',root='0x0086d500',recipe_id='0576-dd603b7071c482c6',member='frontier-044-0086d500.obj',
            member_sha256='2'*64,object_sha256='1'*64,physical_symbol_index=index,section=2,symbol_index=outindex,
            offset=offset,kind=kind,canonical=name,undefined=True,proof=dict(raw,physical_section=24,field_offset=offset))
        root=dict(original_address='0x0086d500',recipe_id=field['recipe_id'],object_sha256='1'*64)
        before=dict(offset=offset,symbol=export,match=True,observed=base)
        after=dict(offset=offset,symbol=name,match=True,observed=base)
        member=dict(name=field['member'],projection=dict(requested_roots=[root],output_sha256='2'*64,original_object_sha256='1'*64,
            fields=[raw],maps=dict(section_map={'24':2},symbol_map={str(index):outindex}),
            before_comparison=[dict(relocations=[before])],after_comparison=[dict(relocations=[after])]))
        unit=dict(compiler='sp1',flags=['/MT','/GS'],symbols={export:base})
        return field,member,{digest:norm},unit,base,digest
    def verify_ordinary(self,args):
        with patch.dict(plan.GS_PROOFS,{args[4]:args[5]}):return plan.ordinary_evidence(*args[:4])
    def model(self,helper):
        base,role,export,kind,index,section,offset,outsection,outindex=(
            ('0x00ec408c','crt-contract','@__security_check_cookie@4',20,765,421,61,4,6) if helper else
            ('0x011c16bc','data','___security_cookie',6,762,420,21,3,4))
        name=plan.old.undefined(base,role);family='PARENT_OWNED_GENERATED_EH_FIELD' if helper else 'PARENT_FINAL_BINDING'
        consistency='EXACT_GENERATED_EH_FIELD_RESOLUTION' if helper else 'EXACT_OWN_SOURCE_RESOLUTION'
        identity=dict(base=int(base,0),role=role,symbol=export,symbol_index=index,proof_consistency=consistency,
            semantic_domain='code' if helper else 'data',contract_kind='security-cookie-check' if helper else 'security-cookie')
        raw=dict(section=section,offset=offset,target_index=index,kind=kind,addend=0,original_base=int(base,0),
            original_target=int(base,0),proof_family=family,output_section=outsection,output_target_index=outindex,
            external_identity=identity,output_symbol=name,output_symbol_section=0,output_symbol_value=0,
            output_symbol_storage=2,output_symbol_type=32 if helper else 0)
        witnessed={k:v for k,v in raw.items() if k in ['section','offset','target_index','kind','addend','original_base','original_target','proof_family']}
        field=dict(component='ModelLoader-EH',root='0x00448420',recipe_id='2633-a302a748a2f3dbae',member='component.obj',
            object_sha256='1'*64,member_sha256='2'*64,physical_symbol_index=index,section=outsection,symbol_index=outindex,
            offset=offset,kind=kind,canonical=name,undefined=True,proof=dict(original_base=base,original_target=base,
                role=role,canonical_name=name,kind=kind,addend_bits=0,physical_section=section,symbol_index=index,
                field_offset=offset,proof_family=family,external_identity=copy.deepcopy(identity)))
        integration=dict(source_object_sha256='1'*64,object_sha256='2'*64,fields=[raw])
        record=dict(root=dict(original_address='0x00448420',recipe_id=field['recipe_id'],object_sha256='1'*64),source='model.cpp',
            result=dict(blockers=[],structural_projection_candidate=True,semantic=dict(object_sha256='1'*64,fields=[witnessed],
                external_obligations=[identity],comparisons=[dict(section=421,start=48,end=75,nonfield_differences=0)])),
            central_contract=dict(fields=[dict(coff_relocation=dict(symbol_index=762,symbol='___security_cookie'),
                physical_section=420,source_field_offset=21,proof_consistency='EXACT_OWN_SOURCE_RESOLUTION')]))
        unit=dict(compiler='sp1',flags=['/MT','/GS','/EHsc'],source='model.cpp',symbols={'___security_cookie':'0x011c16bc'})
        return field,integration,record,unit
    def test_ordinary_two_normative_proofs(self):
        for helper in (False,True):
            evidence=self.verify_ordinary(self.ordinary(helper))
            self.assertEqual(evidence['proof_consistency'],'EXACT_OWN_SOURCE_RESOLUTION')
            self.assertIn('not DIR32 operand width',evidence['cookie_scalar_basis'])
    def test_caller_compiler_label_does_not_choose_runtime_provider(self):
        for compiler in ('sp1','rtm','vc8'):
            args=self.ordinary(True);args[3]['compiler']=compiler
            self.assertTrue(self.verify_ordinary(args)['verified'])
    def test_ordinary_requires_normative_not_compact_only(self):
        args=self.ordinary(True);args[2][args[5]]['proof_consistency']='UNKNOWN'
        with self.assertRaises(ValueError):self.verify_ordinary(args)
    def test_model_parent_and_generated_handler_classes(self):
        for helper,consistency in ((False,'EXACT_OWN_SOURCE_RESOLUTION'),(True,'EXACT_GENERATED_EH_FIELD_RESOLUTION')):
            evidence=plan.model_evidence(*self.model(helper))
            self.assertEqual(evidence['proof_consistency'],consistency);self.assertFalse(evidence['runtime_frame_or_ABI_approved'])
    def test_model_not_ehfile_offsets_or_global_name_class_inference(self):
        args=self.model(True);args[0]['offset']=21
        with self.assertRaises(ValueError):plan.model_evidence(*args)
        args=self.model(True);args[3]['symbols']['@__security_check_cookie@4']='0x00ec408c'
        self.assertEqual(plan.model_evidence(*args)['proof_consistency'],'EXACT_GENERATED_EH_FIELD_RESOLUTION')
        args[3]['symbols']['@__security_check_cookie@4']='0x00ec408d'
        with self.assertRaises(ValueError):plan.model_evidence(*args)
    def test_model_actual_handler_coverage_and_source_identity(self):
        args=self.model(True);args[2]['result']['semantic']['comparisons'][0]['end']=35
        with self.assertRaises(ValueError):plan.model_evidence(*args)
        args=self.model(True);args[0]['member_sha256']='3'*64
        with self.assertRaises(ValueError):plan.model_evidence(*args)

if __name__=='__main__':unittest.main()
