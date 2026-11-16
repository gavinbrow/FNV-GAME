import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
from test_crt_v13_four_alias_contract import V13ConsumerTests
import crt_v14_four_alias_contract as gate

class V14ConsumerTests(unittest.TestCase):
    def bundle(self,disable_cookie=False):
        payload,review,response,fields,_,_,response_sha,digest=V13ConsumerTests().bundle(disable_cookie)
        actual=copy.deepcopy(gate.v14.ACTUAL_COHORT);actual['complete_field_count']=5
        plan=json.loads(payload);plan.update(kind='V14-existing-four-CRT-diagnostic-contract',scope=gate.v14.SCOPE,
            actual_cohort=actual,own_sources=gate.v14.OWN_SOURCES,unknown_flags_preserved=True,requested_batch_assumed=False,
            extra_fields=55,new_current_CRT_uses=2,qualified_UUID_evidence={k:False for k in ('base_closure_observed','full_serialization_eligible',
            'provider_selected','runtime_eligible','ABI_verified','UUID_selected_or_loaded','fresh_sdk_identity_verified')})
        payload=json.dumps(plan).encode();psha=hashlib.sha256(payload).hexdigest()
        reviewed=json.loads(review);reviewed.update(kind='V14-existing-four-CRT-contract-artifact-review',
            status='approved-for-V14-diagnostic-successor-preparation',plan_sha256=psha)
        review=json.dumps(reviewed).encode()
        return payload,review,response,fields,psha,hashlib.sha256(review).hexdigest(),response_sha,digest,actual
    def call(self,bundle,strong=None):
        payload,review,response,fields,psha,rsha,response_sha,digest,actual=bundle
        with patch.multiple(gate,PLAN=psha,REVIEW=rsha,RESPONSE=response_sha):
            with patch.multiple(gate.v14,FULL_DIGEST=digest,COMPLETE_FIELDS=5,ALIAS_USE_COUNT=4,ACTUAL_COHORT=actual):
                return gate.validate(payload,review,response,fields,{} if strong is None else strong)
    def test_actual_source_scope_keeps_four_existing_tokens(self):
        result=self.call(self.bundle());self.assertEqual(len(result['tokens']),4)
        self.assertEqual(len(result['inherited_tokens_to_remove']),4);self.assertFalse(result['runtime_eligible'])
    def test_cookie_disable_cannot_survive_in_inherited_response(self):
        result=self.call(self.bundle(True));self.assertEqual(len(result['tokens']),2)
        self.assertEqual(len(result['inherited_tokens_to_remove']),4)
    def test_hydrated_unknown_annotation_changes_rejected(self):
        b=list(self.bundle());b[3][-1]['full_original_proof']['source_sha256']='b'*64
        with self.assertRaises(ValueError):self.call(b)
    def test_canonical_cookie_strong_definition_rejected(self):
        name=gate.v14.old.undefined('0x011c16bc','data')
        with self.assertRaises(ValueError):self.call(self.bundle(),{name:True})
    def test_artifact_unbound_consumer_rejects_before_input_decode(self):
        with patch.multiple(gate,PLAN=None,REVIEW=None,RESPONSE=None):
            with self.assertRaisesRegex(ValueError,'identities are unbound'):
                gate.validate(object(),object(),object(),object(),object())

if __name__=='__main__':unittest.main()
