"""Authored-only finite observer records and temporary gzip fixtures."""
import copy
import gzip
import json
from argparse import Namespace
from pathlib import Path
import sys
import tempfile
import subprocess
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import comdat_any_frontier_observer as observer
from test_comdat2_code_policy_independent import fixture as native_fixture


def fixture(*,partial=False):
    raw,contract,root=native_fixture()
    if partial:
        root['size']-=1;contract['roots'][0]['size']-=1;contract['unit_verified_functions'][0]['size']-=1
    p=contract['provenance'];p.update(recipe_id=root['recipe_id'],recipe_index=root['recipe_index'],
        scope_mode='singleton',request_sha256='b'*64,recipe_unit_sha256='c'*64,dependency_tools_sha256={})
    cert=observer.base.ordinary.assess_object(observer.base.coff.parse(raw),contract)
    row=dict(schema_version=1,policy_id='central-ordinary-root-views-v1',event='SINGLE_ROOT_OBSERVATION',
        recipe_id=root['recipe_id'],requested_roots=[root],provenance=p,contract=contract,
        contract_identity_sha256=observer.digest(contract),certificate_sha256=observer.digest(cert),certificate=cert,
        closure_observed=cert['closure_observed'],graph_observation_complete=cert['graph_observation_complete'],
        root_closure_candidate=cert['root_closure_candidate'],blockers=cert['blockers'],unit_EH_evidence={},**observer.base.collector.FALSE)
    s=dict(ordinal=1,event=row['event'],recipe_id=root['recipe_id'],roots=[root['original_address']],
        record_sha256=observer.digest(row),certificate_sha256=row['certificate_sha256'],
        closure_observed=False,graph_observation_complete=cert['graph_observation_complete'],
        blocker_codes=dict(observer.Counter(b['code'] for b in cert['blockers'])))
    auth=dict(kind='new-frontier-v3',receipt_sha256='d'*64,request_sha256='b'*64,details_sha256='e'*64,
        ordinal=1,record_sha256=s['record_sha256'],certificate_sha256=s['certificate_sha256'],
        contract_identity_sha256=None,contract_identity_is_bound_through_record_hash=True)
    candidate=dict(root=root,authority=auth,summary=s,source_state='NEW_SELECTED_ROOT_REQUIRES_OBSERVATION',
        symbol=observer.base.pool.canonical(observer.selector.root_identity(root)),group_ordinal=1,group_sha256='f'*64)
    return raw,row,candidate


def rebind(row,candidate):
    row['contract_identity_sha256']=observer.digest(row['contract'])
    row['certificate_sha256']=observer.digest(row['certificate'])
    candidate['authority']['record_sha256']=candidate['summary']['record_sha256']=observer.digest(row)
    candidate['authority']['certificate_sha256']=candidate['summary']['certificate_sha256']=row['certificate_sha256']


class ObserverTests(unittest.TestCase):
    def test_real_cli_initialization_and_review_refusal_before_other_inputs(self):
        result=subprocess.run([sys.executable,str(ROOT/'tools/rebuild/comdat_any_frontier_observer.py'),'--help'],
            text=True,capture_output=True,timeout=30)
        self.assertEqual(result.returncode,0,result.stderr);self.assertIn('--context-sha256',result.stdout)
        with tempfile.TemporaryDirectory(dir=ROOT/'build/rebuild',prefix='authored-comdat-observer-') as directory:
            review=Path(directory)/'review.json';review.write_text('{}',encoding='utf-8')
            args=Namespace(review=review,review_sha256=observer.base.file_hash(review),
                request_sha256='1'*64,context_sha256='2'*64)
            with self.assertRaises(ValueError):observer.review_gate(args,{})

    def test_fresh_negative_native_witness_preserves_base_and_never_emits(self):
        raw,row,candidate=fixture();before=copy.deepcopy((row,candidate));e=observer.observe_member(raw,row,candidate)
        self.assertEqual((row,candidate),before);self.assertTrue(e['native_preflight']['eligible'])
        self.assertTrue(e['composed']['composed_omission_complete'])
        self.assertFalse(e['original_negative_certificate']['closure_observed'])
        self.assertEqual(len(e['unsupported_summary']['discharged_blocker_ids']),1)
        self.assertFalse(e['serialization_performed'])
        for key in observer.FALSE:self.assertIs(e[key],False)

    def test_valid_partial_native_form_is_explicit_no_policy(self):
        raw,row,candidate=fixture(partial=True);e=observer.observe_member(raw,row,candidate)
        self.assertFalse(e['native_preflight']['eligible']);self.assertEqual(e['witnesses'],[])
        self.assertIsNone(e['composed']);self.assertEqual(e['unsupported_summary']['discharged_occurrences'],0)
        self.assertEqual(e['unsupported_summary']['original_blocker_ids'],e['unsupported_summary']['remaining_blocker_ids'])

    def test_summary_body_boolean_join_is_exact(self):
        for key in ('closure_observed','graph_observation_complete'):
            raw,row,candidate=fixture();candidate['summary'][key]=not candidate['summary'][key]
            with self.subTest(key=key),self.assertRaises(ValueError):observer.validate_selected_row(row,candidate)

    def test_fresh_raw_and_original_provenance_contradictions_are_fatal(self):
        raw,row,candidate=fixture()
        with self.assertRaises(ValueError):observer.observe_member(raw+b'changed',row,candidate)
        raw,row,candidate=fixture();row['contract']['provenance']['scope_mode']='recipe-union';rebind(row,candidate)
        with self.assertRaises(ValueError):observer.observe_member(raw,row,candidate)

    def test_selected_reader_parses_only_selected_lines_and_requires_complete_extent(self):
        raw,row,candidate=fixture()
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'authored.jsonl.gz'
            with gzip.open(path,'wb') as stream:
                stream.write(observer.selector.canonical(row)+b'\n');stream.write(b'not-json-unselected\n')
            result=list(observer.read_selected_rows(path,2,{1:candidate},lambda:None))
            self.assertEqual(result,[(candidate,row)])
            with self.assertRaises(ValueError):list(observer.read_selected_rows(path,3,{1:candidate},lambda:None))

    def test_source_receipt_request_and_exact_summary_bindings(self):
        raw,row,candidate=fixture();auth=candidate['authority']
        source=dict(kind=auth['kind'],receipt=dict(path='build/rebuild/authored/receipt.json',sha256=auth['receipt_sha256']),
            request=dict(path='build/rebuild/authored/request.json',sha256=auth['request_sha256']),
            details=[dict(lane=None,path='build/rebuild/authored/details.jsonl.gz',sha256=auth['details_sha256'])])
        receipt=dict(policy_id='new-frontier-ordinary-root-observation-v3',status='metadata-only',input_stability=True,
            optional_function_index_present=False,request_sha256=auth['request_sha256'],observations=[candidate['summary']],
            details_sha256=auth['details_sha256'],**observer.base.collector.FALSE)
        requests=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=[candidate['root']])
        result=observer.validate_source(source,receipt,requests,[candidate]);self.assertEqual(result[0][1],1)
        broken=copy.deepcopy(source);broken['request']['sha256']='9'*64
        with self.assertRaises(ValueError):observer.validate_source(broken,receipt,requests,[candidate])


if __name__=='__main__':unittest.main()
