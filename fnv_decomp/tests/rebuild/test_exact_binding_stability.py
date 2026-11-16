"""Authored identity ledgers and temporary text files; no Game/archive inputs."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/rebuild'))
import exact_binding_stability as subject
import application_link_diagnostic as diagnostic


def binding(request='C:/authored/a.txt',path=None,sha='a'*64,size=12,device=9,inode=13):
    return dict(requested_path=request,path=path or request,sha256=sha,size=size,device=device,inode=inode)


class ExactBindingStabilityTests(unittest.TestCase):
    def test_complete_row_equality_ignores_only_dictionary_insertion_order(self):
        a=binding();b=binding('C:/authored/b.txt',inode=14)
        ledger=[a,dict(reversed(list(a.items()))),b,dict(a),dict(b)]
        before=json.dumps(ledger);ids=[id(r) for r in ledger]
        unique,facts=subject.select_exact_bindings(ledger)
        self.assertEqual(unique,[a,b]);self.assertEqual(facts['first_occurrence_indices'],[0,2])
        self.assertEqual((facts['input_rows'],facts['unique_rows'],facts['exact_duplicate_rows']),(5,2,3))
        self.assertEqual(json.dumps(ledger),before);self.assertEqual([id(r) for r in ledger],ids)
        self.assertIsNot(unique[0],a)

    def test_distinct_requested_aliases_of_same_resolved_file_remain_checks(self):
        a=binding('C:/authored/request-a.txt','C:/authored/resolved.txt')
        b=binding('C:/authored/request-b.txt','C:/authored/resolved.txt')
        unique,facts=subject.select_exact_bindings([a,b,a,b])
        self.assertEqual(unique,[a,b]);self.assertEqual(facts['unique_rows'],2)

    def test_case_and_byteidentical_physical_copies_are_not_normalized(self):
        a=binding('C:/Authored/A.txt');case=binding('c:/authored/a.txt')
        copied=binding('C:/authored/copy.txt',inode=99)
        hardlink=binding('C:/authored/hardlink.txt')
        unique,_=subject.select_exact_bindings([a,case,copied,hardlink])
        self.assertEqual(len(unique),4)

    def test_requested_path_conflicts_refuse_before_delegate(self):
        for field,value in [('path','C:/authored/other.txt'),('sha256','b'*64),('size',13),('device',10),('inode',14)]:
            ledger=[binding(),dict(binding(),**{field:value})];calls=[]
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'requested-path'):
                subject.stable_phase(ledger,phase='pre',stable_fn=lambda rows:calls.append(rows))
            self.assertEqual(calls,[])

    def test_resolved_path_conflicts_refuse_even_for_distinct_requested_aliases(self):
        a=binding('C:/authored/alias1','C:/authored/resolved')
        for field,value in [('sha256','b'*64),('size',13),('device',10),('inode',14)]:
            b=dict(binding('C:/authored/alias2','C:/authored/resolved'),**{field:value})
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'resolved-path'):
                subject.select_exact_bindings([a,b])

    def test_complete_typed_schema_does_not_project_away_extra_fields(self):
        cases=[dict(binding(),extra=True),{k:v for k,v in binding().items() if k!='inode'},
               dict(binding(),size=True),dict(binding(),inode=1.0),dict(binding(),device=-1),
               dict(binding(),path=''),dict(binding(),sha256='A'*64),dict(binding(),sha256='not-a-hash')]
        class ForeignDict(dict):pass
        cases.append(ForeignDict(binding()))
        for row in cases:
            with self.subTest(row=row),self.assertRaises(ValueError):subject.select_exact_bindings([row])
        for ledger in ((binding(),),iter([binding()]),None):
            with self.assertRaises(ValueError):subject.select_exact_bindings(ledger)

    def test_small_patched_bound_refuses_without_checking_any_files(self):
        with patch.object(subject,'MAX_ROWS',1),self.assertRaises(ValueError):subject.select_exact_bindings([binding(),binding()])

    def test_each_phase_rebuilds_and_rechecks_all_unique_rows(self):
        a=binding();b=binding('C:/authored/b.txt',inode=14);ledger=[a,a,b,b]
        actual={a['requested_path']:a,b['requested_path']:b};checked=[]
        def stable(rows):
            for row in rows:
                checked.append(row['requested_path'])
                if actual[row['requested_path']]!=row:raise ValueError('authored drift')
        pre=subject.stable_phase(ledger,phase='pre',stable_fn=stable)
        post=subject.stable_phase(ledger,phase='post',stable_fn=stable)
        self.assertEqual(checked,[a['requested_path'],b['requested_path']]*2)
        self.assertEqual(pre['ledger_identity_sequence_sha256'],post['ledger_identity_sequence_sha256'])
        actual[a['requested_path']]=dict(a,sha256='f'*64)
        with self.assertRaises(ValueError):subject.stable_phase(ledger,phase='post',stable_fn=stable)
        self.assertEqual(checked[-1],a['requested_path'])

    def test_actual_frozen_delegate_detects_authored_file_drift_between_phases(self):
        with tempfile.TemporaryDirectory() as td:
            first=Path(td)/'first.txt';second=Path(td)/'second.txt'
            first.write_text('authored one');second.write_text('authored two')
            a=diagnostic.identity(first);b=diagnostic.identity(second);ledger=[a,b,a,b,a,b]
            real=diagnostic.identity;calls=[]
            def counted(path):calls.append(str(path));return real(path)
            with patch.object(diagnostic,'identity',side_effect=counted):
                subject.stable_phase(ledger,phase='pre',stable_fn=diagnostic.stable)
                self.assertEqual(len(calls),2)
                first.write_text('authored changed')
                with self.assertRaisesRegex(ValueError,'identity drift'):
                    subject.stable_phase(ledger,phase='post',stable_fn=diagnostic.stable)
            self.assertEqual(len(ledger),6)

    def test_delegate_exception_propagates_once_without_retry(self):
        failure=ValueError('authored delegate failure');calls=[]
        def stable(rows):calls.append(rows);raise failure
        with self.assertRaises(ValueError) as caught:subject.stable_phase([binding(),binding()],phase='pre',stable_fn=stable)
        self.assertIs(caught.exception,failure);self.assertEqual(len(calls),1)

    def test_selected_snapshot_cannot_mutate_original_ledger_or_pass_silently(self):
        ledger=[binding(),binding()];before=copy.deepcopy(ledger)
        def mutate(rows):rows[0]['size']+=1
        with self.assertRaisesRegex(ValueError,'selected snapshot'):
            subject.stable_phase(ledger,phase='pre',stable_fn=mutate)
        self.assertEqual(ledger,before)

    def test_concurrent_original_ledger_change_refuses_completed_metadata(self):
        ledger=[binding(),binding()]
        def mutate(_):ledger[1]['inode']+=1
        with self.assertRaisesRegex(ValueError,'caller ledger changed'):
            subject.stable_phase(ledger,phase='post',stable_fn=mutate)

    def test_explicit_phase_and_delegate_are_required_and_empty_ledger_is_preserved(self):
        for phase in ('other',None,True):
            with self.assertRaises(ValueError):subject.stable_phase([binding()],phase=phase,stable_fn=lambda rows:None)
        with self.assertRaises(ValueError):subject.stable_phase([],phase='pre',stable_fn=None)
        calls=[];result=subject.stable_phase([],phase='pre',stable_fn=lambda rows:calls.append(rows))
        self.assertEqual(calls,[[]]);self.assertEqual(result['unique_rows'],0)
        self.assertFalse(result['cross_phase_cache_used']);self.assertFalse(result['original_ledger_rewritten'])


if __name__=='__main__':unittest.main()
