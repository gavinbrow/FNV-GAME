import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
from test_crt_v8_four_alias_contract import V8ConsumerTests
import crt_v9_four_alias_contract as gate

class V9ConsumerTests(unittest.TestCase):
    def bundle(self,disable_cookie=False):
        payload,review,response,fields,_,_,rsha,digest=V8ConsumerTests().bundle(disable_cookie)
        plan=json.loads(payload);plan.update(kind='V9-existing-four-CRT-diagnostic-contract',scope='V8-plus-three-CODE',
            extra_fields=3,new_fields_use_existing_CRT_aliases=False,new_current_CRT_uses=0,
            inherited_binding_evidence_scope='V7-plus-CODE59-ModelLoader')
        payload=json.dumps(plan).encode();psha=hashlib.sha256(payload).hexdigest()
        reviewed=json.loads(review);reviewed.update(kind='V9-existing-four-CRT-contract-artifact-review',
            status='approved-for-V9-diagnostic-successor-preparation',plan_sha256=psha)
        review=json.dumps(reviewed).encode()
        return payload,review,response,fields,psha,hashlib.sha256(review).hexdigest(),rsha,digest
    def call(self,bundle,strong=None):
        payload,review,response,fields,psha,rsha,response_sha,digest=bundle
        with patch.multiple(gate,PLAN=psha,REVIEW=rsha,RESPONSE=response_sha,COMPLETE_FIELDS=5,POTENTIAL_FIELDS=4):
            with patch.object(gate.v9,'FULL_DIGEST',digest):
                return gate.validate(payload,review,response,fields,{} if strong is None else strong)
    def test_new_scope_returns_only_four_existing_tokens(self):
        result=self.call(self.bundle());self.assertEqual(len(result['tokens']),4)
        self.assertEqual(len(result['inherited_tokens_to_remove']),4)
        self.assertFalse(result['runtime_eligible'])
    def test_cookie_disable_removes_all_inherited_tokens(self):
        result=self.call(self.bundle(True));self.assertEqual(len(result['tokens']),2)
        self.assertEqual(len(result['inherited_tokens_to_remove']),4)
    def test_full_hydrated_snapshot_remains_exact(self):
        b=list(self.bundle());b[3][-1]['full_original_proof']['source_sha256']='b'*64
        with self.assertRaises(ValueError):self.call(b)
    def test_strong_canonical_collision_fails(self):
        name=gate.v9.old.undefined('0x011c16bc','data')
        with self.assertRaises(ValueError):self.call(self.bundle(),{name:True})

if __name__=='__main__':unittest.main()
