"""Authored metadata and response tests; no SDK or game reads."""
import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import application_uuid2768 as m

class ResponseGuardTests(unittest.TestCase):
    def setUp(self):
        self.identity=copy.deepcopy(m.EXPECTED_SDK);self.path=self.identity['path']
        self.q=dict(kind='qualified-uuid2768-consumer-evidence-v1',policy_id=m.POLICY,
                    dependency_identity=copy.deepcopy(self.identity),future_uuid_response_token=self.path)
    def test_exact_single_path_and_physical_identity(self):
        r=m.guard_response(['/nologo',self.path,'kernel32.lib'],self.identity,self.q)
        self.assertEqual(r['status'],'response-obligation-consistent');self.assertFalse(r['fresh_sdk_identity_verified'])
        self.assertFalse(r['library_selected']);self.assertFalse(r['library_loaded'])
    def test_missing_duplicate_unqualified_and_alternate_requests_fail(self):
        for tokens in ([],[self.path,self.path],['uuid.lib'],[self.path,'uuid'],[self.path,'/DEFAULTLIB:uuid.lib'],
                       [self.path,'/DEFAULTLIB:"UUID"'],[self.path,r'C:\\other\\uuid.lib'],[self.path,'--lib=uuid.lib,foo']):
            with self.subTest(tokens=tokens),self.assertRaises(ValueError):m.guard_response(tokens,self.identity,self.q)
    def test_forged_identity_same_hash_different_origin_and_types_fail(self):
        for k,value in [('path',r'C:\\other\\uuid.lib'),('sha256','0'*64),('device',True),('inode',0),('size',1)]:
            other=copy.deepcopy(self.identity);other[k]=value
            with self.subTest(key=k),self.assertRaises(ValueError):m.guard_response([self.path],other,self.q)
        q=copy.deepcopy(self.q);q['dependency_identity']['path']=r'C:\\other\\uuid.lib';q['future_uuid_response_token']=q['dependency_identity']['path']
        with self.assertRaises(ValueError):m.guard_response([q['future_uuid_response_token']],q['dependency_identity'],q)
    def test_malformed_tokens_and_extra_identity_keys_fail(self):
        for tokens in ('not-a-list',[self.path,2],[self.path,'']):
            with self.assertRaises(ValueError):m.guard_response(tokens,self.identity,self.q)
        with self.assertRaises(ValueError):m.guard_response([self.path],dict(self.identity,extra=True),self.q)

class SavedComparisonTests(unittest.TestCase):
    def setUp(self):
        self.fields=[dict(offset=i*4,kind=20,original_target='0x00123456') for i in range(9)]
        self.row=dict(address=m.ROOT,symbol='authored',size=58,compiled_extent=58,verdict='match',errors=[],
          relocations=[dict(offset=f['offset'],kind=f['kind'],expected=f['original_target'],observed=f['original_target'],match=True) for f in self.fields])
    def test_full_saved_proofs_and_field_join(self):m._comparison([self.row],'authored',self.fields)
    def test_bad_match_span_relocation_and_targets_fail(self):
        for change in ('span','verdict','match','target','extra'):
            r=copy.deepcopy(self.row)
            if change=='span':r['compiled_extent']=57
            elif change=='verdict':r['verdict']='mismatch'
            elif change=='match':r['relocations'][0]['match']=False
            elif change=='target':r['relocations'][0]['expected']='0x00000000'
            else:r['relocations'].append(copy.deepcopy(r['relocations'][0]))
            with self.subTest(change=change),self.assertRaises(ValueError):m._comparison([r],'authored',self.fields)
    def test_fixed_scope_authentication_rejects_synthetic_bytes(self):
        with self.assertRaises(ValueError):m.consume({k:b'{}' for k in m.PINS})
        with self.assertRaises(ValueError):m.consume({})

if __name__=='__main__':unittest.main()
