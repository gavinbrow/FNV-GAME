import copy
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'/'rebuild'))
import v14_saved11_handoff as h


class PartialHandoffTests(unittest.TestCase):
    def fixture(self):
        roots=[{'original_address':'0x%08x'%i,'size':i+1} for i in range(11)]
        excluded=[{'original_address':x,'size':1} for group in h.EXCLUDED.values() for x in group]
        members=[];saved=[];positive=[]
        for i,r in enumerate(roots):
            a=r['original_address'];m={'name':'CACHED-CODE-%03d-%s.obj'%(i,a[2:]),'sha256':'a'*64,'bytes':10}
            members.append({'root':r,'saved_member':m});saved.append({'address':a,**m})
        for i,r in enumerate(roots+excluded):
            positive.append({'root':r,'ordinal':i+1,'record_sha256':'b'*64,'certificate_sha256':'c'*64,'contract_identity_sha256':'d'*64})
        op={'kind':'v14-saved11-fresh-validation-proposal','new_object_emission':False,'prior_batch_replay':False,'prior_match_inferred':False,'exclusions':copy.deepcopy(h.EXCLUDED),'members':members}
        failure={'status':'failed-quarantined-no-replay','replay_authorized':False}
        counts=dict(roots=11,before_match_reports=11,after_match_reports=11,field_rows=22,unique_field_facts=22,relocation_match_observations=44,excluded_roots=4)
        main=dict(status='accepted-fresh-saved-validation-only-not-provider-or-runtime-admission',operation_sha256=h.INPUTS['operation'][1],receipt_sha256=h.INPUTS['validation_receipt'][1],complement_review_sha256=h.INPUTS['complement_review'][1],host_terminal_sha256=h.INPUTS['host_terminal'][1],counts=counts)
        peer=dict(approved=True,operation_sha256=h.INPUTS['operation'][1],receipt_sha256=h.INPUTS['validation_receipt'][1],host_terminal_sha256=h.INPUTS['host_terminal'][1],provider_selected=False,runtime_eligible=False,reports_sha256='e'*64)
        receipt=dict(kind='v14-saved11-validation-receipt',status='validated-unreviewed',operation_sha256=h.INPUTS['operation'][1],validated=11,full_field_proof_records=11,input_stability=True,validated_addresses=[r['original_address'] for r in roots],output_sha256={'reports.jsonl.gz':'e'*64,'progress.jsonl':'f'*64})
        for k in ('canonical_index_checked','function_index_present','excluded_member_payloads_accessed','new_object_emission','prior_batch_replay','prior_match_inferred','provider_selected','runtime_eligible','standalone_receipt_admission'):receipt[k]=False
        terminal=dict(status='completed-unreviewed',runner_receipt_sha256=h.INPUTS['validation_receipt'][1],provider_selected=False,runtime_eligible=False)
        return [op,{'verified_members':saved},failure,main,peer,receipt,terminal,{'positive_singletons':positive}]

    def test_exact_handoff_remains_partial_and_nonadmitting(self):
        result=h.derive(*self.fixture())
        self.assertEqual(len(result['members']),11);self.assertFalse(result['provider_selected'])
        self.assertFalse(result['canonical_index_checked']);self.assertIn('archive and independent native archive conformance',result['not_retained'])

    def test_altered_member_or_exclusion_cannot_be_handed_off(self):
        for case in ('member','exclusion','receipt'):
            values=self.fixture()
            if case=='member':values[0]['members'][0]['saved_member']['sha256']='f'*64
            if case=='exclusion':values[0]['exclusions']['inflight_unknown']=[]
            if case=='receipt':values[5]['prior_match_inferred']=True
            with self.subTest(case=case),self.assertRaises(ValueError):h.derive(*values)

if __name__=='__main__':unittest.main()
