import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import crt_frontier_adoption_contract as gate

class ExpandedConsumerTests(unittest.TestCase):
    def fixture(self):
        fields=[];bindings=[]
        for i,(base,role,export,kind) in enumerate(gate.frontier.old.BINDINGS):
            name=gate.frontier.old.undefined(base,role)
            f=dict(component='fixture',member='fixture.obj',caller='caller',section=2,offset=i*4,
                canonical=name,physical_symbol_index=i,kind=kind,undefined=True,
                source_sha256='1'*64,proof=dict(original_base=base,original_target=base,role=role,
                    kind=kind,addend_bits=0,symbol_index=i))
            fields.append(f);bindings.append(dict(original_base=base,role=role,normal_export=export,
                canonical_undefined=name,enabled=True,fields=[copy.deepcopy(f)],field_count=1,
                field_census_sha256=gate.frontier.old.digest([f])))
        return fields,bindings
    def test_exact_four_role_and_source_uses(self):
        fields,bindings=self.fixture();self.assertEqual(len(gate.validate_bindings(bindings,fields,{})),4)
        fields[0]['source_sha256']='2'*64
        with self.assertRaises(ValueError):gate.validate_bindings(bindings,fields,{})
    def test_new_alias_or_role_is_rejected(self):
        fields,bindings=self.fixture();bindings[0]['normal_export']='_unreviewed'
        with self.assertRaises(ValueError):gate.validate_bindings(bindings,fields,{})
        fields,bindings=self.fixture();bindings[0]['role']='code'
        with self.assertRaises(ValueError):gate.validate_bindings(bindings,fields,{})
    def test_enabled_strong_definition_collision_blocks(self):
        fields,bindings=self.fixture()
        for row in bindings:
            with self.assertRaises(ValueError):gate.validate_bindings(bindings,fields,{row['canonical_undefined']:{}})
    def test_cookie_pair_must_be_enabled_or_disabled_together(self):
        fields,bindings=self.fixture();bindings[0]['enabled']=False
        with self.assertRaises(ValueError):gate.validate_bindings(bindings,fields,{})
        bindings[1]['enabled']=False
        rows=gate.validate_bindings(bindings,fields,{bindings[0]['canonical_undefined']:{}})
        self.assertEqual(sum(r['enabled'] for r in rows),2)
    def test_missing_and_extra_canonical_uses_block(self):
        fields,bindings=self.fixture()
        with self.assertRaises(ValueError):gate.validate_bindings(bindings,fields[:-1],{})
        extra=copy.deepcopy(fields[0]);extra['offset']=99
        with self.assertRaises(ValueError):gate.validate_bindings(bindings,fields+[extra],{})
    def test_unbound_plan_and_unreviewed_payload_block(self):
        with self.assertRaises(ValueError):gate.validate(b'{}',b'{}',b'/FORCE\r\n',[],{})
    def test_end_to_end_retains_generated_proof_flag_without_native_permission(self):
        fields,bindings=self.fixture();frontier=gate.frontier
        response=frontier.response_bytes(bindings,frontier.old.response(bindings).replace('\n','\r\n').encode())
        response_sha=hashlib.sha256(response).hexdigest();digest=frontier.old.digest(sorted(fields,key=frontier.old.canonical))
        plan=dict(kind='expanded-four-CRT-diagnostic-contract',scope='V6-plus-first3-CODE12-EHFile',
            complete_input_fields=4,selected_field_sha256=digest,alias_field_count=4,generated_EH_proof_remains_distinct=True,
            unreviewed_new_CRT_aliases=[],native_operation_authorized=False,provider_adopted=False,
            runtime_ABI_approved=False,runtime_eligible=False,bindings=bindings,response_text=response.decode(),
            response_sha256=response_sha,enabled_alias_count=4)
        payload=json.dumps(plan).encode();plan_sha=hashlib.sha256(payload).hexdigest()
        review=dict(kind='expanded-four-CRT-contract-artifact-review',status='approved-for-expanded-diagnostic-successor-preparation',
            reviewer='independent',plan_sha256=plan_sha,response_sha256=response_sha)
        review_bytes=json.dumps(review).encode();review_sha=hashlib.sha256(review_bytes).hexdigest()
        with patch.multiple(gate,PLAN=plan_sha,REVIEW=review_sha,RESPONSE=response_sha,COMPLETE_FIELDS=4,POTENTIAL_ALIAS_FIELDS=4):
            with patch.object(frontier,'FULL_DIGEST',digest):
                result=gate.validate(payload,review_bytes,response,fields,{})
        self.assertEqual(result['tokens'],response.decode().splitlines())
        self.assertTrue(result['generated_EH_proof_remains_distinct']);self.assertFalse(result['native_operation_authorized'])

if __name__=='__main__':unittest.main()
