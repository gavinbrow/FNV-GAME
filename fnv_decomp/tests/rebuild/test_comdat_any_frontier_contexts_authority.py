"""Original metadata-only candidate locator authority regressions."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import comdat_any_frontier_contexts as selector
from test_comdat_any_frontier_contexts import fixture,rebind


class IndependentCandidateAuthorityTests(unittest.TestCase):
    def test_locator_request_is_deferred_negative_evidence_and_never_selection2_proof(self):
        values=fixture();before=copy.deepcopy(values);result=selector.select_candidates(*values)
        self.assertEqual(len(result['audit']),467)
        self.assertEqual(result['counts']['selected'],len(result['roots']))
        self.assertFalse(result['selection2_inferred']);self.assertFalse(result['native_census_evaluated'])
        self.assertFalse(result['candidate_policy_evaluated']);self.assertTrue(result['body_read_required'])
        self.assertTrue(result['contract_identity_deferred'])
        for row in result['candidates']:
            self.assertFalse(row['summary']['closure_observed'])
            self.assertIsNone(row['authority']['contract_identity_sha256'])
            self.assertIn(selector.ROOT_BLOCKER,row['summary']['blocker_codes'])
            self.assertNotEqual(row['root']['original_address'],'0x0086beb0')
        for flag in selector.FALSE:self.assertIs(result[flag],False)
        self.assertEqual(values,before)

    def test_receipt_uses_exact_producer_crlf_ordered_document_not_record_or_lf_digest(self):
        f,r,n,h=fixture()
        for wrong in (hashlib.sha256(selector.canonical(n)).hexdigest(),
            hashlib.sha256((json.dumps(n,separators=(',',':'))+'\n').encode()).hexdigest()):
            self.assertNotEqual(wrong,h)
            with self.assertRaises(ValueError):selector.select_candidates(f,r,n,wrong)
        reordered=dict(reversed(list(n.items())))
        with self.assertRaises(ValueError):selector.select_candidates(f,r,reordered,h)

    def test_unknown_or_promoted_top_envelopes_are_refused_even_after_rebinding(self):
        for envelope,key,value in [('frontier','namespace_approved',True),('registry','typed_root_witnesses_consumed',True),
                                  ('receipt','emission_performed',True),('receipt','collector_sha256','e'*64)]:
            f,r,n,h=fixture();target={'frontier':f,'registry':r,'receipt':n}[envelope];target[key]=value
            with self.subTest(envelope=envelope,key=key),self.assertRaises(ValueError):selector.select_candidates(*rebind(f,r,n))

    def test_borrowed_cache_root_record_and_locator_cannot_change_candidate_origin(self):
        for mutation in ('authority','root','locator'):
            f,r,n,h=fixture();rows=list(r['records'].values())
            if mutation=='authority':f['records'][0]['cache_authority']=copy.deepcopy(f['records'][1]['cache_authority'])
            elif mutation=='root':f['records'][0]['root']=copy.deepcopy(f['records'][1]['root'])
            else:
                rows[1]['authority']['ordinal']=rows[0]['authority']['ordinal']
                rows[1]['summary']['lane_record_ordinal']=rows[0]['summary']['lane_record_ordinal']
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):selector.select_candidates(*rebind(f,r,n))

    def test_zero_boolean_blocker_counts_or_typed_annotation_cannot_stand_in_for_original_blocker(self):
        for mutation in ('zero','boolean','annotation','positive-with-blocker'):
            f,r,n,h=fixture();s=next(row for row in n['observations']if row['event']=='SINGLE_ROOT_OBSERVATION'and not row['closure_observed'])
            if mutation=='zero':s['blocker_codes']={selector.ROOT_BLOCKER:0}
            elif mutation=='boolean':s['blocker_codes']={selector.ROOT_BLOCKER:True}
            elif mutation=='annotation':s['composed_omission_complete']=True
            else:s['closure_observed']=True
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):selector.select_candidates(*rebind(f,r,n))

    def test_missing_union_duplicate_demand_or_reused_group_ordinal_is_not_complete_profile(self):
        for mutation in ('union','demand','group'):
            f,r,n,h=fixture()
            if mutation=='union':n['observations'].pop()
            elif mutation=='demand':f['records'][-1]=copy.deepcopy(f['records'][-2])
            else:f['records'][-1]['group_ordinal']=f['records'][-2]['group_ordinal']
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):selector.select_candidates(*rebind(f,r,n))

    def test_body_digest_cannot_be_guessed_and_new_physical_identity_cannot_alias_cached_definition(self):
        for mutation in ('contract','physical'):
            f,r,n,h=fixture()
            if mutation=='contract':next(iter(r['records'].values()))['authority']['contract_identity_sha256']='e'*64
            else:
                cached=next(iter(r['records'].values()))['root'];root=f['new_roots'][0]
                for key in ('recipe_id','object_sha256','symbol_index'):root[key]=cached[key]
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):selector.select_candidates(*rebind(f,r,n))


if __name__=='__main__':unittest.main()
