"""Synthetic response tokens and metadata only; no SDK or actual V13 reads."""
import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import application_combined_response as m
import application_uuid2768 as uuid

class CombinedResponseTests(unittest.TestCase):
    def setUp(self):
        self.old=r'C:\cohort\old';self.new=r'C:\cohort\new'
        self.iat=[f'/ALTERNATENAME:iat{i}=target{i}' for i in range(34)]
        self.crt=[f'/ALTERNATENAME:crt{i}=crt_target{i}' for i in range(4)]
        self.tokens=['/NOLOGO',r'/OUT:C:\cohort\old\diagnostic.exe',r'/MAP:C:\cohort\old\diagnostic.map',r'C:\base\baseline.lib']+self.iat+self.crt
        self.raw=m.diagnostic.response_text(self.tokens).encode()
        self.identity=copy.deepcopy(uuid.EXPECTED_SDK)
        self.qualified=dict(kind='qualified-uuid2768-consumer-evidence-v1',policy_id=uuid.POLICY,
             future_uuid_response_token=self.identity['path'],dependency_identity=copy.deepcopy(self.identity))
        self.kw=dict(old_out=self.old,new_out=self.new,batch_archive=r'C:\cohort\batch.lib',uuid_archive=r'C:\cohort\uuid2768.lib',
             prior_iat=self.iat,prior_crt=self.crt,current_iat=self.iat[:2],current_crt=self.crt[:1],
             fresh_uuid_identity=self.identity,qualified_uuid=self.qualified)
    def test_complete_transform_and_exact_subset(self):
        before=copy.deepcopy((self.raw,self.kw));r=m._transform(self.raw,**self.kw)
        self.assertEqual(before,(self.raw,self.kw));t=r['tokens']
        self.assertEqual(m._parse(r['response_bytes']),t);self.assertEqual(t.count(self.identity['path']),1)
        self.assertEqual([x for x in t if x.startswith('/ALTERNATENAME:')],self.iat[:2]+self.crt[:1])
        self.assertIn(self.kw['batch_archive'],t);self.assertIn(self.kw['uuid_archive'],t)
        self.assertFalse(r['library_loaded']);self.assertFalse(r['link_performed']);self.assertTrue(r['caller_nonempty_accepted_batch_required'])
    def test_public_rejects_authored_baseline(self):
        with self.assertRaises(ValueError):m.transform(self.raw,**self.kw)
    def test_reject_unexpected_or_duplicate_baseline_tokens(self):
        for lines in (self.tokens+[self.tokens[0]],self.tokens+[self.iat[0].lower()],self.tokens+['/ALTERNATENAME:bad=target'],
                      self.tokens[:-1],self.tokens+[self.kw['batch_archive']],self.tokens+[r'/OUT:C:\else\diagnostic.exe']):
            with self.subTest(last=lines[-1]),self.assertRaises(ValueError):m._transform(m.diagnostic.response_text(lines).encode(),**self.kw)
    def test_reject_unknown_duplicate_cross_family_alias_and_noncanonical_paths(self):
        for patch in (dict(current_iat=['/ALTERNATENAME:evil=target']),dict(current_iat=self.iat[:1]*2),
                      dict(current_crt=self.iat[:1]),dict(batch_archive=self.kw['uuid_archive']),
                      dict(batch_archive=r'C:\cohort\..\bad.lib'),dict(old_out=r'\cohort\old')):
            kw=dict(self.kw,**patch)
            with self.subTest(patch=patch),self.assertRaises(ValueError):m._transform(self.raw,**kw)
    def test_reject_control_characters_and_alternate_data_stream_paths(self):
        for bad in (r'C:\cohort\batch.lib:stream', 'C:\\cohort\\bad\x00.lib',
                    'C:\\cohort\\bad\t.lib', r'C:\cohort\bad?.lib'):
            with self.subTest(path=bad),self.assertRaises(ValueError):
                m._transform(self.raw,**dict(self.kw,batch_archive=bad))

    def test_reject_alternate_uuid_and_identity_drift(self):
        for extra in ('uuid.lib','/DEFAULTLIB:uuid',r'C:\other\Uuid.Lib'):
            with self.subTest(extra=extra),self.assertRaises(ValueError):m._transform(m.diagnostic.response_text(self.tokens+[extra]).encode(),**self.kw)
        for key,value in (('path',r'C:\different\uuid.lib'),('inode',0),('device',True),('size',1),('sha256','0'*64)):
            wrong=dict(self.identity,**{key:value})
            with self.subTest(key=key),self.assertRaises(ValueError):m._transform(self.raw,**dict(self.kw,fresh_uuid_identity=wrong))
    def test_standalone_uuid_directory_is_rejected_by_frozen_guard(self):
        with self.assertRaises(ValueError):
            m._transform(self.raw,**dict(self.kw,new_out=r'C:\cohort\uuid\next'))
        result=m._transform(self.raw,**dict(self.kw,new_out=r'C:\cohort\v14-combined'))
        self.assertTrue(result['response_bytes'])

    def test_bad_baseline_framing_and_forbidden_policy(self):
        for raw in (b'bad\n',b'"bad"\n\n',self.raw+b'"/FORCE"\n',self.raw+b'"/WHOLEARCHIVE:x"\n'):
            with self.assertRaises(ValueError):m._transform(raw,**self.kw)
    def test_allows_empty_reviewed_alias_subsets_but_not_claim_batch_nonempty(self):
        r=m._transform(self.raw,**dict(self.kw,current_iat=[],current_crt=[]))
        self.assertFalse([x for x in r['tokens'] if x.startswith('/ALTERNATENAME:')])
        self.assertTrue(r['caller_nonempty_accepted_batch_required'])

if __name__=='__main__':unittest.main()
