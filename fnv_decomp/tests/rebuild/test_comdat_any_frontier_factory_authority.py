"""Original saved-witness selection authority negatives; no real inputs."""
import copy
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import comdat_any_frontier_factory as factory
from test_comdat_any_frontier_factory import evidence_fixture
from test_comdat_any_frontier_observer import rebind


def restamp_witness(e):
    e['composed']['witness_sha256']=[factory.digest(w)for w in e['witnesses']]
    if len(e['witnesses'])==1:
        for entry in e['composed']['discharged_blockers']:entry['witness_sha256']=factory.digest(e['witnesses'][0])


def all_complete_fixture():
    receipt,rows,request,original=evidence_fixture();raw,row,candidate=original[1]
    size=len(factory.base.coff.parse(raw)['sections'][candidate['root']['section']]['payload'])
    candidate['root']['size']=row['contract']['roots'][0]['size']=row['contract']['unit_verified_functions'][0]['size']=size
    candidate['authority']['ordinal']=candidate['summary']['ordinal']=2
    candidate['symbol']=factory.base.pool.canonical(factory.observer.selector.root_identity(candidate['root']))
    row['certificate']=factory.base.ordinary.assess_object(factory.base.coff.parse(raw),row['contract'])
    row['blockers']=row['certificate']['blockers'];rebind(row,candidate)
    rows[1]=factory.observer.observe_member(raw,row,candidate)
    receipt.update(composed_complete=2,unsupported=0,blocked=0)
    return receipt,rows,request,original


class IndependentFactoryAuthorityTests(unittest.TestCase):
    def test_every_complete_composition_is_selected_without_count1_shortcut(self):
        receipt,rows,request,_=all_complete_fixture();before=copy.deepcopy((receipt,rows,request))
        selected,ledger=factory.select_eligible(receipt,rows,request)
        self.assertEqual(len(selected),2);self.assertEqual(len(ledger),2)
        self.assertTrue(all(r['selected']for r in ledger));self.assertEqual((receipt,rows,request),before)
        self.assertEqual([r['root']['original_address']for r in selected],sorted(r['root']['original_address']for r in rows))

    def test_borrowed_negative_certificate_or_contract_cannot_rebind_to_original_source(self):
        for mutation in ('certificate','contract','authority'):
            receipt,rows,request,_=evidence_fixture();e=rows[0]
            if mutation=='certificate':
                e['original_negative_certificate']['provider_selected']=0
                e['original_negative_certificate_sha256']=factory.digest(e['original_negative_certificate'])
            elif mutation=='contract':
                e['contract_identity_sha256']=e['native_preflight']['contract_identity_sha256']=e['composed']['contract_identity_sha256']='e'*64
            else:e['authority']=dict(e['authority'],receipt_sha256='e'*64)
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):factory.select_eligible(receipt,rows,request)

    def test_partial_promoted_wrong_kind_or_duplicate_witness_cannot_be_selected_after_rehash(self):
        for mutation in ('partial','promoted','kind','duplicate'):
            receipt,rows,request,_=evidence_fixture();e=rows[0];w=e['witnesses'][0]['observation']
            if mutation=='partial':w['witness_complete']=w['root_comdat2_policy_candidate']=False
            elif mutation=='promoted':w['namespace_approved']=True
            elif mutation=='kind':e['witnesses'][0]['kind']='typed-data-omission'
            else:e['witnesses'].append(copy.deepcopy(e['witnesses'][0]))
            restamp_witness(e)
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):factory.select_eligible(receipt,rows,request)

    def test_census_cannot_be_replaced_by_additional_declared_definitions(self):
        receipt,rows,request,_=evidence_fixture();e=rows[0];wrapper=e['witnesses'][0];census=wrapper['definition_census']
        extra=copy.deepcopy(census['entries'][0]);extra['root']['original_address']='0x04000000';census['entries'].append(extra)
        e['native_preflight']['definition_census']=census
        e['composed']['definition_census_sha256']=wrapper['observation']['definition_census_sha256']=factory.digest(census)
        restamp_witness(e)
        with self.assertRaises(ValueError):factory.select_eligible(receipt,rows,request)

    def test_discharge_occurrence_and_witness_identity_are_not_opaque_annotations(self):
        for field,value in [('base_blocker_ordinal',True),('base_blocker_ordinal',2),
                            ('witness_sha256','e'*64),('witness_policy_id','ordinary')]:
            receipt,rows,request,_=evidence_fixture();rows[0]['composed']['discharged_blockers'][0][field]=value
            with self.subTest(field=field,value=value),self.assertRaises(ValueError):factory.select_eligible(receipt,rows,request)

    def test_native_qualification_does_not_allow_promoted_or_serialized_preflight(self):
        for field in ('planned_definition_census_authenticated','serialization_performed','candidate_policy_evaluated'):
            receipt,rows,request,_=evidence_fixture();rows[0]['native_preflight'][field]=True
            with self.subTest(field=field),self.assertRaises(ValueError):factory.select_eligible(receipt,rows,request)

    def test_blocked_native_ledger_keeps_original_ordered_occurrences(self):
        receipt,rows,request,_=evidence_fixture();rows[1]['unsupported_summary']['remaining_blocker_ids'].pop()
        with self.assertRaises(ValueError):factory.select_eligible(receipt,rows,request)

    def test_partial_duplicate_or_forged_count_cannot_be_whole_observer_batch(self):
        for mutation in ('subset','duplicate','boolean-count'):
            receipt,rows,request,_=all_complete_fixture()
            if mutation=='subset':rows.pop()
            elif mutation=='duplicate':rows[1]=copy.deepcopy(rows[0])
            else:receipt['blocked']=False
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):factory.select_eligible(receipt,rows,request)


if __name__=='__main__':unittest.main()
