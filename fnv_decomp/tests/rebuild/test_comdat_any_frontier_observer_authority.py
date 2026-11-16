"""Authored observer authority tests; metadata pin patches confer no real approval."""
import copy
import gzip
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import comdat_any_frontier_observer as observer
from test_comdat_any_frontier_observer import fixture,rebind
from test_comdat_any_frontier_contexts import fixture as selector_fixture,rebind as rebind_selector


def context_fixture():
    f,r,n,_=selector_fixture();cached=list(r['records'].values())
    for index,source_index in [(0,206),(1,215)]:
        old=f['records'][index];row=cached[source_index];root=row['root']
        old.update(root=root,symbol=observer.base.pool.canonical(observer.selector.root_identity(root)),
            original_bases=[root['original_address']],original_targets=[root['original_address']],
            cached_observation=row['summary'],cache_authority=row['authority'])
    f,r,n,h=rebind_selector(f,r,n);request=observer.selector.select_candidates(f,r,n,h)
    prepared=dict(kind='prepared-CODE-collision-exclusions',application_selection_inferred_from_counts=False,
        provider_selected=False,runtime_eligible=False,application_manifest_adopted=False,exclusion_names=[])
    artifacts=dict(frontier=f,registry=r,new_receipt=n,manifest={},retained={},selection={},recipes={},
                   prepared_epoch=prepared,epoch_review={})
    refs={k:dict(path='build/rebuild/authored-observer/'+k+'.json',
                sha256=observer.selector.document_hash(value,sort_keys=k!='new_receipt'))for k,value in artifacts.items()}
    context=dict(schema_version=1,kind='finite-comdat-any-frontier-observer-context',epoch='authored-not-production',
        request_sha256=observer.selector.document_hash(request),artifacts=refs,
        acceptances={k:dict(path='build/rebuild/authored-observer/'+k+'.json',sha256=h)for k,h in observer.KNOWN_ACCEPTANCES.items()},
        sources=[],provider_selected=False,runtime_eligible=False,emission_performed=False,reference_image_read=False)
    wanted={}
    for c in request['candidates']:
        a=c['authority'];key=tuple(a[k]for k in ('kind','receipt_sha256','request_sha256'))
        wanted.setdefault(key,set()).add(a.get('lane'))
    for i,(key,lanes)in enumerate(wanted.items()):
        kind,receipt_sha,request_sha=key
        context['sources'].append(dict(kind=kind,receipt=dict(path='build/rebuild/authored-observer/receipt%d.json'%i,sha256=receipt_sha),
            request=dict(path='build/rebuild/authored-observer/request%d.json'%i,sha256=request_sha),
            details=[dict(lane=lane,path='build/rebuild/authored-observer/details%d-%s.gz'%(i,lane),sha256='d'*64)for lane in lanes]))
    metadata={k:refs[k]['sha256']for k in observer.METADATA_PINS}
    original={k:refs[k]['sha256']for k in ('manifest','retained','selection','recipes')}
    return request,context,artifacts,metadata,original


def validate_context(values):
    request,context,artifacts,metadata,original=values
    with patch.dict(observer.METADATA_PINS,metadata,clear=True),patch.dict(observer.base.inventory.EXPECTED,original):
        return observer.validate_request_context(request,context,artifacts)


class IndependentObserverAuthorityTests(unittest.TestCase):
    def test_whole_selector_context_authenticates_four_distinct_sources_without_opening_files(self):
        values=context_fixture();before=copy.deepcopy(values)
        with patch.object(observer.base,'observe',side_effect=AssertionError('pure context must not read')):
            result=validate_context(values)
        self.assertEqual(len(result),4);self.assertEqual(values,before)
        self.assertEqual(len({key[1]for key in result}),4)

    def test_partial_selector_request_cannot_be_authorized_by_rehashing_context(self):
        values=list(context_fixture());values[0]['roots'].pop();values[0]['candidates'].pop()
        values[1]['request_sha256']=observer.selector.document_hash(values[0])
        with self.assertRaises(ValueError):validate_context(values)

    def test_source_epoch_lane_and_acceptance_borrowing_are_fatal(self):
        for mutation in ('receipt','request','missing-source','extra-lane','lane-type','foreign-path','acceptance'):
            values=list(context_fixture());context=values[1];source=context['sources'][0]
            if mutation=='receipt':source['receipt']['sha256']='e'*64
            elif mutation=='request':source['request']['sha256']='e'*64
            elif mutation=='missing-source':context['sources'].pop()
            elif mutation=='extra-lane':source['details'].append(dict(source['details'][0],lane=2))
            elif mutation=='lane-type':source['details'][0]['lane']=True
            elif mutation=='foreign-path':source['details'][0]['path']='../outside.gz'
            else:context['acceptances']['selector_review']['sha256']='e'*64
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):validate_context(values)

    def test_prepared_collision_and_stale_epoch_reference_are_fatal(self):
        for mutation in ('collision','epoch','original-pin'):
            values=list(context_fixture());context,artifacts=values[1:3]
            if mutation=='collision':
                artifacts['prepared_epoch']['exclusion_names']=[values[0]['candidates'][0]['symbol']]
                h=observer.selector.document_hash(artifacts['prepared_epoch'])
                context['artifacts']['prepared_epoch']['sha256']=values[3]['prepared_epoch']=h
            elif mutation=='epoch':context['artifacts']['prepared_epoch']['sha256']='e'*64
            else:context['artifacts']['manifest']['sha256']='e'*64
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):validate_context(values)

    def test_standalone_body_refuses_borrowed_locator_and_guessed_contract_identity(self):
        for mutation in ('ordinal','ordinal-type','contract','kind','summary'):
            raw,row,candidate=fixture()
            if mutation=='ordinal':candidate['authority']['ordinal']=2
            elif mutation=='ordinal-type':candidate['authority']['ordinal']=True
            elif mutation=='contract':candidate['authority']['contract_identity_sha256']='e'*64
            elif mutation=='kind':candidate['authority']['kind']='cached-central'
            else:candidate['summary']['graph_observation_complete']=not candidate['summary']['graph_observation_complete']
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):observer.observe_member(raw,row,candidate)

    def test_raw_integrity_never_becomes_unsupported_and_valid_partial_never_emits(self):
        raw,row,candidate=fixture()
        with self.assertRaises(ValueError):observer.observe_member(raw[:-1],row,candidate)
        raw,row,candidate=fixture(partial=True)
        with patch.object(observer.base.coff,'namespace',side_effect=AssertionError('writer forbidden')),\
             patch.object(observer.base.coff,'serialize',side_effect=AssertionError('writer forbidden')):
            evidence=observer.observe_member(raw,row,candidate)
        self.assertFalse(evidence['native_preflight']['eligible']);self.assertEqual(evidence['witnesses'],[])
        self.assertIsNone(evidence['composed']);self.assertFalse(evidence['serialization_performed'])
        self.assertEqual(evidence['unsupported_summary']['discharged_occurrences'],0)

    def test_original_source_request_provenance_cannot_be_rebound_to_other_authority(self):
        raw,row,candidate=fixture();row['contract']['provenance']['request_sha256']='e'*64
        row['certificate']=observer.base.ordinary.assess_object(observer.base.coff.parse(raw),row['contract'])
        row['blockers']=row['certificate']['blockers'];rebind(row,candidate)
        with self.assertRaises(ValueError):observer.validate_selected_row(row,candidate)

    def test_selected_stream_rejects_borrowed_row_and_incomplete_extent(self):
        for mutation in ('borrowed','truncated','extra'):
            raw,row,candidate=fixture();rows=[copy.deepcopy(row)]
            if mutation=='borrowed':rows[0]['recipe_id']='borrowed'
            elif mutation=='truncated':rows=[]
            else:rows.append(copy.deepcopy(row))
            with tempfile.TemporaryDirectory()as td:
                path=Path(td)/'authored.gz'
                with gzip.open(path,'wt')as target:
                    for value in rows:target.write(json.dumps(value)+'\n')
                with self.subTest(mutation=mutation),self.assertRaises(ValueError):
                    list(observer.read_selected_rows(path,1,{1:candidate},lambda:None))


if __name__=='__main__':unittest.main()
