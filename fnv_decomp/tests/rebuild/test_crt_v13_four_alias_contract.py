import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
from test_crt_v10_four_alias_contract import V10ConsumerTests
import crt_v13_four_alias_contract as gate

class V13ConsumerTests(unittest.TestCase):
    def bundle(self,disable_cookie=False):
        payload,review,response,fields,_,_,rsha,digest=V10ConsumerTests().bundle(disable_cookie)
        plan=json.loads(payload);plan.update(kind='V13-existing-four-CRT-diagnostic-contract',scope='V12-plus-CODE56',extra_fields=290,normative_source_evidence_enriched=False)
        payload=json.dumps(plan).encode();psha=hashlib.sha256(payload).hexdigest()
        reviewed=json.loads(review);reviewed.update(kind='V13-existing-four-CRT-contract-artifact-review',
            status='approved-for-V13-diagnostic-successor-preparation',plan_sha256=psha)
        review=json.dumps(reviewed).encode()
        return payload,review,response,fields,psha,hashlib.sha256(review).hexdigest(),rsha,digest
    def call(self,bundle,strong=None):
        payload,review,response,fields,psha,rsha,response_sha,digest=bundle
        with patch.multiple(gate,PLAN=psha,REVIEW=rsha,RESPONSE=response_sha,COMPLETE_FIELDS=5,POTENTIAL_FIELDS=4):
            with patch.object(gate.v13,'FULL_DIGEST',digest):
                return gate.validate(payload,review,response,fields,{} if strong is None else strong)
    def test_v13_full_scope_retains_four_existing_tokens(self):
        result=self.call(self.bundle());self.assertEqual(len(result['tokens']),4)
        self.assertEqual(len(result['inherited_tokens_to_remove']),4)
        self.assertFalse(result['native_operation_authorized'])
    def test_disabled_cookie_pair_cannot_survive_inherited_response(self):
        result=self.call(self.bundle(True));self.assertEqual(len(result['tokens']),2)
        self.assertEqual(len(result['inherited_tokens_to_remove']),4)
    def test_all_raw_annotations_are_in_full_snapshot(self):
        b=list(self.bundle());b[3][-1]['full_original_proof']['source_sha256']='b'*64
        with self.assertRaises(ValueError):self.call(b)
    def test_strong_canonical_cookie_definition_rejected(self):
        name=gate.v13.old.undefined('0x011c16bc','data')
        with self.assertRaises(ValueError):self.call(self.bundle(),{name:True})

if __name__=='__main__':unittest.main()
