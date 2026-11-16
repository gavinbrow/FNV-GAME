import copy
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'/'rebuild'))
import v14_saved11_validation_runner as subject


class ReviewTests(unittest.TestCase):
    def fixture(self):
        source={p:'a'*64 for p in subject.SOURCE_ROLES}
        primary=dict(schema_version=1,kind='v14-saved11-source-input-review-v1',reviewer='reviewer',approved=True,
            root_authorized=True,source_review_pass=True,input_review_pass=True,resource_lease_required=True,
            operation_sha256=subject.OP_SHA,source_sha256=source,peer_review_path='build/rebuild/peer.json',
            peer_review_sha256='b'*64,reference_path='reference',allow_reference_and_original_reads=True,
            allow_saved_object_reads=True,allow_native_tools=False,allow_object_emission=False,allow_game_execution=False)
        peer=dict(schema_version=1,kind='v14-saved11-complement-review-v1',reviewer='peer',approved=True,
            operation_sha256=subject.OP_SHA,source_sha256=copy.deepcopy(source),provider_selected=False,runtime_eligible=False)
        return primary,peer

    def test_independent_review_binding(self):
        primary,peer=self.fixture();self.assertTrue(subject.validate_review(primary,peer,subject.OP_SHA,'reference'))
        for field,value in [('reviewer','reviewer'),('provider_selected',True),('operation_sha256','c'*64)]:
            bad=copy.deepcopy(peer);bad[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):subject.validate_review(primary,bad,subject.OP_SHA,'reference')

    def test_reject_claimed_emission_and_false_lease_policy(self):
        primary,peer=self.fixture()
        for key,value in [('allow_object_emission',True),('resource_lease_required',False),('root_authorized',False)]:
            bad=copy.deepcopy(primary);bad[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):subject.validate_review(bad,peer,subject.OP_SHA,'reference')


class PublicationTests(unittest.TestCase):
    def fixture(self,out):
        for name in ('progress.jsonl','reports.jsonl.gz'):(out/name).write_bytes(name.encode())
        pins={name:hashlib.sha256((out/name).read_bytes()).hexdigest() for name in ('progress.jsonl','reports.jsonl.gz')}
        return dict(output_sha256=pins,validated=11,new_object_emission=False)

    def test_late_stability_failure_retracts_canonical_receipt(self):
        import os
        import cached_frontier_code_factory_v13 as v13
        if os.name!='nt':self.skipTest('reviewed Windows hardlink semantics required')
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory);receipt=self.fixture(out)
            with patch.object(v13.base,'stable',side_effect=[None,None,ValueError('drift')]),patch.object(v13.base,'budget'):
                with self.assertRaisesRegex(ValueError,'drift'):subject.publish_receipt(out,receipt,{},0,small_metadata=())
            self.assertFalse((out/'receipt.json').exists());self.assertTrue((out/'receipt.pending.json').exists())

    def test_unexpected_output_prevents_publication(self):
        import cached_frontier_code_factory_v13 as v13
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory);receipt=self.fixture(out);(out/'unexpected.obj').write_bytes(b'fake')
            with patch.object(v13.base,'stable'),patch.object(v13.base,'budget'):
                with self.assertRaises(ValueError):subject.publish_receipt(out,receipt,{},0,small_metadata=())
            self.assertFalse((out/'receipt.json').exists())


class InputAndIndexGuardTests(unittest.TestCase):
    def test_private_metadata_reparse_rejected_before_resolution(self):
        import stat
        from types import SimpleNamespace
        with patch.object(Path,'lstat',return_value=SimpleNamespace(st_mode=stat.S_IFREG,st_size=20,st_file_attributes=0x400)), \
             patch.object(Path,'resolve',side_effect=AssertionError('unexpected resolution')):
            with self.assertRaises(ValueError):subject._private_path('build/rebuild/peer.json')

    def test_output_lstat_rejects_any_lexical_entry_before_resolution(self):
        from types import SimpleNamespace
        with patch.object(Path,'lstat',return_value=SimpleNamespace(st_file_attributes=0x400)), \
             patch.object(Path,'resolve',side_effect=AssertionError('unexpected resolution')):
            with self.assertRaises(FileExistsError):subject._require_absent('dangling-output')
        with patch.object(Path,'lstat',side_effect=FileNotFoundError):
            subject._require_absent('missing-output')

    def test_reparse_input_and_oversize_rejected_before_resolve(self):
        import stat
        from types import SimpleNamespace
        with patch.object(Path,'lstat',return_value=SimpleNamespace(st_mode=stat.S_IFREG,st_size=5,st_file_attributes=0x400)), \
             patch.object(Path,'resolve',side_effect=AssertionError('unexpected resolution')):
            with self.assertRaises(ValueError):subject._regular_no_reparse('candidate',1024)
        with patch.object(Path,'lstat',return_value=SimpleNamespace(st_mode=stat.S_IFREG,st_size=1025,st_file_attributes=0)), \
             patch.object(Path,'resolve',side_effect=AssertionError('unexpected resolution')):
            with self.assertRaises(ValueError):subject._regular_no_reparse('candidate',1024)

    def test_index_appearing_after_publication_retracts_receipt(self):
        import os
        import cached_frontier_code_factory_v13 as v13
        import cached_frontier_code_factory_v14_driver as driver
        if os.name!='nt':self.skipTest('reviewed Windows hardlink semantics required')
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory)
            for name in ('progress.jsonl','reports.jsonl.gz'):(out/name).write_bytes(name.encode())
            pins={name:hashlib.sha256((out/name).read_bytes()).hexdigest() for name in ('progress.jsonl','reports.jsonl.gz')}
            receipt=dict(output_sha256=pins,validated=11,new_object_emission=False)
            with patch.object(v13.base,'stable'),patch.object(v13.base,'budget'), \
                 patch.object(driver,'_require_absent_index',side_effect=[None,None,None,None,None,ValueError('index appeared')]):
                with self.assertRaisesRegex(ValueError,'index appeared'):
                    subject.publish_receipt(out,receipt,{},0,small_metadata=())
            self.assertFalse((out/'receipt.json').exists());self.assertTrue((out/'receipt.pending.json').exists())


class FieldFactTests(unittest.TestCase):
    def test_cross_root_conflict_rejected(self):
        facts={1:(6,7,8)}
        subject.merge_field_facts(facts,{1:(6,7,8),2:(20,9,10)})
        self.assertEqual(len(facts),2)
        with self.assertRaises(ValueError):subject.merge_field_facts(facts,{1:(6,99,8)})


class RetractionFailureTests(PublicationTests):
    def test_unlink_failure_is_explicit_and_receipt_never_self_admits(self):
        import os
        import cached_frontier_code_factory_v13 as v13
        if os.name!='nt':self.skipTest('reviewed Windows hardlink semantics required')
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory);receipt=self.fixture(out)
            with patch.object(v13.base,'stable',side_effect=[None,None,ValueError('drift')]), \
                 patch.object(v13.base,'budget'),patch.object(Path,'unlink',side_effect=PermissionError('denied')):
                with self.assertRaises(subject.ReceiptRetractionFailed):
                    subject.publish_receipt(out,receipt,{},0,small_metadata=())
            self.assertTrue((out/'receipt.json').exists())

if __name__=='__main__':unittest.main()
