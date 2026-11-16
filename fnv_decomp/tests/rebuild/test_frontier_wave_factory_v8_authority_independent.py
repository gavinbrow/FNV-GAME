"""Original V8 dynamic finite scope and new-epoch frame tests."""
import copy
import gzip
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import frontier_wave_factory_v8 as factory
from test_code_frontier_wave_v8_authority_independent import fixture as registry_fixture,reconcile,registry
from test_frontier_code_factory_spool_independent import context


def fixture():
    values=registry_fixture();registered=registry(values)
    positive_names={g['symbol']for g in values[3]['groups']if any(g['original_bases']==s['roots']
        for src in values[0][1:]for s in src['receipt']['observations']if s['closure_observed'])}
    frontier=reconcile(values,registered,positive_names)
    positive,_=context();root=positive['requested_roots'][0];old=frontier['new_roots'][0]
    for row in frontier['records']:
        if row.get('root')==old:
            row.update(root=root,symbol=factory.base.pool.canonical({k:root[k]for k in ('recipe_id','object_sha256','symbol_index')}))
    frontier['new_roots'][0]=root
    rows=[];summaries=[]
    for ordinal,r in enumerate(frontier['new_roots'],1):
        row=copy.deepcopy(positive)if ordinal==1 else dict(event='SINGLE_ROOT_OBSERVATION',recipe_id=r['recipe_id'],
            requested_roots=[r],closure_observed=False,graph_observation_complete=True)
        rows.append(row);summaries.append(dict(event=row['event'],ordinal=ordinal,recipe_id=r['recipe_id'],roots=[r['original_address']],
            closure_observed=row['closure_observed'],graph_observation_complete=True,record_sha256=factory.digest(row),
            certificate_sha256=row.get('certificate_sha256'),blocker_codes={}if ordinal==1 else{'ROOT_CONJUNCT':1}))
    receipt=dict(policy_id='new-frontier-ordinary-root-observation-v3',status='metadata-only',input_stability=True,
        optional_function_index_present=False,summary=dict(roots=len(rows)),observations=summaries)
    return frontier,registered,receipt,rows


def select(v):return factory.select_new_contexts(*v[:3],'d'*64)
def spool(v,selected,folder):
    details=folder/'new.jsonl.gz'
    with gzip.open(details,'wt')as target:
        for row in v[3]:target.write(json.dumps(row)+'\n')
    out=folder/'out';out.mkdir()
    with patch.object(factory.base,'budget',return_value={}):
        return factory.spool_new_contexts(out,v[2],details,selected,{},time.monotonic(),expected_receipt_sha256='d'*64)


class IndependentV8FrameAuthorityTests(unittest.TestCase):
    def test_scope_derives_all198_authored_missing_roots_not_old54_cap(self):
        v=fixture();before=copy.deepcopy(v);request,selected,ledger=select(v)
        self.assertEqual(len(v[0]['new_roots']),198);self.assertEqual(len(ledger),467)
        self.assertEqual(len(selected),1);self.assertEqual(request['roots'],[v[3][0]['requested_roots'][0]])
        self.assertEqual(selected[0]['authority']['kind'],'new-frontier-v3')
        self.assertEqual(sum(r['production_status']=='NEW_ORIGINAL_OMISSION_BLOCKED'for r in ledger),197)
        self.assertEqual(v,before)

    def test_old_epoch_partial_receipt_duplicate_demand_and_cached_root_are_refused(self):
        for mutation in ('old-policy','partial','summary54','duplicate','cached'):
            v=fixture()
            if mutation=='old-policy':v[2]['policy_id']='new-frontier-ordinary-root-observation-v2'
            elif mutation=='partial':v[2]['input_stability']=False
            elif mutation=='summary54':v[2]['summary']['roots']=54
            elif mutation=='duplicate':v[0]['records'][-1]=copy.deepcopy(v[0]['records'][-2])
            else:
                root=v[0]['new_roots'][0];v[1]['records'].pop(next(iter(v[1]['records'])))
                v[1]['records'][root['original_address']]=dict(root=root)
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):select(v)

    def test_COMDAT_annotation_cannot_promote_negative_or_route_existing_quarantine(self):
        v=fixture();v[2]['observations'][1].update(witness_complete=True,composed_omission_complete=True)
        request,selected,ledger=select(v)
        self.assertEqual(len(selected),1);self.assertNotIn(v[0]['new_roots'][1],request['roots'])
        q=next(r for r in ledger if r['state']=='PRESERVED_REFERENCE_GROUP_QUARANTINE')
        self.assertEqual(q['root']['original_address'],'0x0086beb0');self.assertNotIn(q['root'],request['roots'])

    def test_new_only_frame_roundtrip_keeps_v3_authority(self):
        v=fixture();_,selected,_=select(v)
        with tempfile.TemporaryDirectory()as td:
            path,index=spool(v,selected,Path(td));entry=next(iter(index.values()))
            with path.open('rb')as stream:
                self.assertEqual(factory.frozen.read_context(stream,entry,selected[0]),v[3][0])
                other=copy.deepcopy(selected[0]);other['authority']['kind']='new-frontier-v2'
                with self.assertRaises(ValueError):factory.frozen.read_context(stream,entry,other)

    def test_borrowed_v2_epoch_or_missing_positive_fails_before_spool_file(self):
        for mutation in ('kind','receipt','missing-positive','duplicate-selected'):
            v=fixture();_,selected,_=select(v)
            if mutation=='kind':selected[0]['authority']['kind']='new-frontier-v2'
            elif mutation=='receipt':selected[0]['authority']['receipt_sha256']='e'*64
            elif mutation=='missing-positive':selected=[]
            else:selected.append(copy.deepcopy(selected[0]))
            with tempfile.TemporaryDirectory()as td:
                folder=Path(td)
                with self.subTest(mutation=mutation),self.assertRaises(ValueError):spool(v,selected,folder)
                self.assertFalse((folder/'out/contexts.bin').exists())

    def test_truncated_or_borrowed_detail_source_never_publishes_complete_index(self):
        for mutation in ('missing','borrowed-row','borrowed-hash'):
            v=fixture();_,selected,_=select(v)
            if mutation=='missing':v[3].pop()
            elif mutation=='borrowed-row':v[3][0]['recipe_id']='borrowed'
            else:selected[0]['authority']['record_sha256']='e'*64
            with tempfile.TemporaryDirectory()as td:
                folder=Path(td)
                with self.subTest(mutation=mutation),self.assertRaises(ValueError):spool(v,selected,folder)
                self.assertFalse((folder/'out/contexts-index.json').exists())


if __name__=='__main__':unittest.main()
