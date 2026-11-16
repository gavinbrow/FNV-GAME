import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import crt_v8_four_alias_contract as gate

class V8ConsumerTests(unittest.TestCase):
    def bundle(self,disable_cookie=False,own_sources=None):
        old=gate.v8.old;fields=[];bindings=[]
        for i,(base,role,export,kind) in enumerate(old.BINDINGS):
            name=old.undefined(base,role)
            field=dict(component='fixture',member='fixture.obj',caller='caller',section=2,offset=i*4,
                canonical=name,physical_symbol_index=i,kind=kind,undefined=True,
                proof=dict(original_base=base,original_target=base,role=role,kind=kind,addend_bits=0,symbol_index=i))
            fields.append(field);bindings.append(dict(original_base=base,role=role,normal_export=export,
                canonical_undefined=name,enabled=not(disable_cookie and i<2),fields=[copy.deepcopy(field)],
                field_count=1,field_census_sha256=old.digest([field])))
        # Hydrated annotations are part of the complete snapshot even when the
        # associated field is outside all four CRT aliases.
        fields.append(dict(canonical='_unrelated_iat',full_original_proof=dict(source_sha256='a'*64)))
        digest=old.digest(sorted(fields,key=old.canonical))
        previous=old.response(bindings).replace('\n','\r\n').encode()
        response=gate.v8.prior.response_bytes(bindings,previous);rsha=hashlib.sha256(response).hexdigest()
        plan=dict(kind='V8-existing-four-CRT-diagnostic-contract',scope='V7-plus-CODE59-ModelLoader',
            complete_input_fields=5,selected_field_sha256=digest,alias_field_count=4,
            own_sources=gate.v8.OWN_SOURCES if own_sources is None else own_sources,
            old_raw_source_records_preserved=True,old_annotation_delta=[],generated_and_ordinary_proofs_remain_distinct=True,
            unreviewed_new_CRT_aliases=[],native_operation_authorized=False,provider_adopted=False,
            runtime_ABI_approved=False,runtime_eligible=False,bindings=bindings,response_text=response.decode(),response_sha256=rsha,
            enabled_alias_count=sum(b['enabled'] for b in bindings),enabled_alias_field_count=sum(b['enabled'] for b in bindings))
        payload=json.dumps(plan).encode();psha=hashlib.sha256(payload).hexdigest()
        review=dict(kind='V8-existing-four-CRT-contract-artifact-review',status='approved-for-V8-diagnostic-successor-preparation',
            reviewer='independent',plan_sha256=psha,response_sha256=rsha)
        reviewed=json.dumps(review).encode();review_sha=hashlib.sha256(reviewed).hexdigest()
        return payload,reviewed,response,fields,psha,review_sha,rsha,digest
    def call(self,bundle,strong=None):
        payload,review,response,fields,psha,review_sha,rsha,digest=bundle
        with patch.multiple(gate,PLAN=psha,REVIEW=review_sha,RESPONSE=rsha,COMPLETE_FIELDS=5,POTENTIAL_FIELDS=4):
            with patch.object(gate.v8,'FULL_DIGEST',digest):
                return gate.validate(payload,review,response,fields,{} if strong is None else strong)
    def test_both_source_ledgers_and_existing_four_tokens(self):
        result=self.call(self.bundle());self.assertEqual(len(result['tokens']),4)
        self.assertEqual(len(result['inherited_tokens_to_remove']),4)
        self.assertFalse(result['native_operation_authorized']);self.assertFalse(result['runtime_ABI_approved'])
    def test_single_legacy_source_is_not_both_own_sources(self):
        sources=dict(list(gate.v8.OWN_SOURCES.items())[:1])
        with self.assertRaises(ValueError):self.call(self.bundle(own_sources=sources))
    def test_hydrated_unrelated_annotation_cannot_be_dropped(self):
        bundle=list(self.bundle());bundle[3][-1]['full_original_proof']['source_sha256']='b'*64
        with self.assertRaises(ValueError):self.call(bundle)
    def test_coupled_disable_requires_removing_all_inherited_tokens(self):
        result=self.call(self.bundle(disable_cookie=True))
        self.assertEqual(len(result['tokens']),2);self.assertEqual(len(result['inherited_tokens_to_remove']),4)
        self.assertEqual(result['enabled_alias_field_count'],2)
    def test_strong_canonical_definition_cannot_supersede_enabled_alias(self):
        name=gate.v8.old.undefined('0x011c16bc','data')
        with self.assertRaises(ValueError):self.call(self.bundle(),{name:{}})
    def test_old_or_arbitrary_payload_is_not_new_scope(self):
        with self.assertRaises(ValueError):gate.validate(b'{}',b'{}',b'/FORCE\r\n',[],{})

if __name__=='__main__':unittest.main()
