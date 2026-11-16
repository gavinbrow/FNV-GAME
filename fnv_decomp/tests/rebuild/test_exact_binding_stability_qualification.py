"""Pure authored receipt qualification; historical paths deliberately do not exist."""
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import exact_binding_stability_qualification as subject


def row(name='authored-missing-a',inode=1):
    return dict(requested_path=name,path=name,sha256='a'*64,size=3,device=4,inode=inode)


def evaluate(raw,counts=(3,2,1)):
    return subject.evaluate(raw,expected_sha256=hashlib.sha256(raw).hexdigest(),expected_counts=counts)


class QualificationTests(unittest.TestCase):
    def test_full_ledger_preserved_and_no_historical_filesystem_calls(self):
        a=row();b=row('authored-missing-b',2)
        raw=json.dumps(dict(input_bindings=[a,b,dict(reversed(list(a.items())))],other={'proof':['unchanged']})).encode()
        with patch.object(Path,'open',side_effect=AssertionError('filesystem forbidden')),patch.object(Path,'stat',side_effect=AssertionError('filesystem forbidden')),patch.object(Path,'resolve',side_effect=AssertionError('filesystem forbidden')):
            result=evaluate(raw)
        self.assertTrue(result['complete_ledger_preserved'])
        self.assertEqual(result['selection']['first_occurrence_indices'],[0,1])
        self.assertEqual(len(result['selection_seconds']),3)
        self.assertFalse(result['actual_stability_delegate_called'])
        self.assertFalse(result['storage_io_speedup_measured'])

    def test_hash_counts_and_size_are_fail_closed(self):
        raw=json.dumps({'input_bindings':[row()]}).encode()
        with self.assertRaisesRegex(ValueError,'hash mismatch'):
            subject.evaluate(raw,expected_sha256='0'*64,expected_counts=(1,1,0))
        with self.assertRaisesRegex(ValueError,'counts mismatch'):evaluate(raw,(2,1,1))
        with self.assertRaisesRegex(ValueError,'typed exact'):evaluate(raw,(True,1,0))
        with patch.object(subject,'MAX_RAW_BYTES',2):
            with self.assertRaisesRegex(ValueError,'bounded raw'):evaluate(raw,(1,1,0))

    def test_json_and_identity_schema_drift_fail(self):
        for raw in (b'{"input_bindings":[],"input_bindings":[]}',b'{"input_bindings":[],"bad":NaN}',b'[]',b'{}',b'{"input_bindings":{}}'):
            with self.subTest(raw=raw),self.assertRaises(ValueError):evaluate(raw,(0,0,0))
        for altered in (dict(row(),extra=True),dict(row(),inode=True),dict(row(),sha256='B'*64)):
            with self.subTest(row=altered),self.assertRaises(ValueError):evaluate(json.dumps({'input_bindings':[altered]}).encode(),(1,1,0))

    def test_conflicts_not_hidden_by_independent_baseline(self):
        for changed in (dict(row(),inode=9),dict(row('alias'),path='authored-missing-a',size=9)):
            raw=json.dumps({'input_bindings':[row(),changed]}).encode()
            with self.assertRaisesRegex(ValueError,'conflicting'):evaluate(raw,(2,2,0))

    def test_corrupt_selector_is_detected(self):
        raw=json.dumps({'input_bindings':[row()]}).encode()
        with patch.object(subject.selection,'select_exact_bindings',return_value=([],{'first_occurrence_indices':[]})):
            with self.assertRaisesRegex(ValueError,'selection mismatch'):evaluate(raw,(1,1,0))


if __name__=='__main__':unittest.main()
