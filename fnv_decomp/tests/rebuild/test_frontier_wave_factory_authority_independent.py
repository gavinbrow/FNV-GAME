"""Original finite54/cache215 authority regressions; no original inputs."""
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
import frontier_wave_factory as factory
from test_code_frontier_wave_authority_independent import authored
from test_frontier_code_factory_spool_independent import context


def fixture():
    values=authored(269)
    all_roots={a:factory.wave.prior.planner.root_record(a,p,values[2]) for a,p in values[1].items()}
    roots=list(all_roots.values())
    registry=dict(roots=215,records={r['original_address']:dict(root=r) for r in roots[:215]})
    positive,_=context();new=[positive['requested_roots'][0]]+roots[216:269]
    assert len(new)==54 and not(set(r['original_address'] for r in new)&set(registry['records']))
    records=[]
    for r in roots[1:129]:records.append(dict(symbol=r['symbol'],root=r,state='CACHED_ORIGINAL_OMISSION_BLOCKED'))
    for i in range(60):records.append(dict(symbol='prepared%d'%i,state='PREPARED_SKIP'))
    records.append(dict(symbol=roots[0]['symbol'],root=roots[0],state='PRESERVED_REFERENCE_GROUP_QUARANTINE'))
    for i in range(6):records.append(dict(symbol='unknown%d'%i,state='UNSELECTED_OR_NAMESPACE_UNPROVED'))
    for r in new:records.append(dict(symbol=factory.base.pool.canonical({k:r[k] for k in ('recipe_id','object_sha256','symbol_index')}),root=r,state='NEW_SELECTED_ROOT_REQUIRES_OBSERVATION'))
    frontier=dict(frontier='accepted-V7',code_demands=249,records=records,new_roots=new,cached_positive_roots=[],
        counts=dict(CACHED_ORIGINAL_OMISSION_BLOCKED=128,PREPARED_SKIP=60,PRESERVED_REFERENCE_GROUP_QUARANTINE=1,
                    UNSELECTED_OR_NAMESPACE_UNPROVED=6,NEW_SELECTED_ROOT_REQUIRES_OBSERVATION=54))
    rows=[];summaries=[]
    for i,root in enumerate(new,1):
        row=copy.deepcopy(positive) if i==1 else dict(event='SINGLE_ROOT_OBSERVATION',recipe_id=root['recipe_id'],
            requested_roots=[root],closure_observed=False,graph_observation_complete=True)
        rows.append(row)
        summaries.append(dict(event=row['event'],ordinal=i,recipe_id=root['recipe_id'],roots=[root['original_address']],
            closure_observed=row['closure_observed'],graph_observation_complete=True,record_sha256=factory.digest(row),
            certificate_sha256=row.get('certificate_sha256'),blocker_codes={} if i==1 else {'OMITTED_INITIALIZED_DATA':1}))
    receipt=dict(policy_id='new-frontier-ordinary-root-observation-v2',status='metadata-only',input_stability=True,optional_function_index_present=False,
                 request_sha256='c'*64,summary=dict(roots=54),observations=summaries)
    return frontier,registry,receipt,rows


def select(values):return factory.select_new_contexts(*values[:3],'d'*64)


class IndependentNewAuthorityTests(unittest.TestCase):
    def test_exact_positive_subset_and_negative_partition_keep_new_receipt_authority(self):
        values=fixture();before=copy.deepcopy(values);request,selected,ledger=select(values)
        self.assertEqual(len(ledger),249);self.assertEqual(len(selected),1)
        self.assertEqual(request['roots'],[values[0]['new_roots'][0]])
        self.assertEqual(selected[0]['authority']['kind'],'new-frontier-v2')
        self.assertEqual(selected[0]['authority']['receipt_sha256'],'d'*64)
        self.assertEqual(sum(r['production_status']=='NEW_ORIGINAL_OMISSION_BLOCKED' for r in ledger),53)
        self.assertEqual(values,before)

    def test_duplicate_frontier_demand_cannot_drop_one_requested_root(self):
        values=fixture();values[0]['records'][-1]=copy.deepcopy(values[0]['records'][-2])
        with self.assertRaises(ValueError):select(values)

    def test_negative_typed_annotations_cannot_promote_original_negative(self):
        values=fixture();summary=values[2]['observations'][1]
        summary.update(composition=dict(composition_complete=True),witness=dict(witness_complete=False))
        request,selected,ledger=select(values)
        self.assertEqual(len(selected),1)
        row=next(r for r in ledger if r.get('root')==values[0]['new_roots'][1])
        self.assertEqual(row['production_status'],'NEW_ORIGINAL_OMISSION_BLOCKED')
        self.assertNotIn(row['root'],request['roots'])

    def test_cached_root_or_partial_receipt_cannot_enter_new_only_scope(self):
        for mutation in ('cached-root','incomplete','aborted','optional-index','missing-summary'):
            values=fixture()
            if mutation=='cached-root':
                root=values[0]['new_roots'][0];values[1]['records'].pop(next(iter(values[1]['records'])))
                values[1]['records'][root['original_address']]=dict(root=root)
            elif mutation=='incomplete':values[2]['input_stability']=False
            elif mutation=='aborted':values[2]['status']='aborted'
            elif mutation=='optional-index':values[2]['optional_function_index_present']=True
            else:values[2]['observations'].pop()
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):select(values)

    def test_borrowed_recipe_duplicate_locator_or_incomplete_positive_is_refused(self):
        for mutation in ('recipe','locator','positive','graph','recordhash'):
            values=fixture();row=values[2]['observations'][0]
            if mutation=='recipe':row['recipe_id']='borrowed'
            elif mutation=='locator':values[2]['observations'][1]['ordinal']=row['ordinal']
            elif mutation=='positive':row['blocker_codes']={'UNPROVED':1}
            elif mutation=='graph':row['graph_observation_complete']=False
            else:row['record_sha256']='g'*64
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):select(values)

    def test_quarantine_remains_outside_selected_and_unknown_cached_positive_is_fatal(self):
        values=fixture();request,_,ledger=select(values)
        quarantine=next(r for r in ledger if r['state']=='PRESERVED_REFERENCE_GROUP_QUARANTINE')
        self.assertEqual(quarantine['root']['original_address'],'0x0086beb0')
        self.assertNotIn(quarantine['root'],request['roots'])
        values[0]['records'][0]['state']='CACHED_BARE_POSITIVE_REQUIRES_FRESH_CLASSIFICATION'
        values[0]['counts']['CACHED_ORIGINAL_OMISSION_BLOCKED']-=1
        values[0]['counts']['CACHED_BARE_POSITIVE_REQUIRES_FRESH_CLASSIFICATION']=1
        with self.assertRaises(ValueError):select(values)

    def spool(self,values,selected,folder):
        details=folder/'details.jsonl.gz'
        with gzip.open(details,'wt') as stream:
            for row in values[3]:stream.write(json.dumps(row)+'\n')
        out=folder/'out';out.mkdir()
        with patch.object(factory.base,'budget',return_value={}):
            return factory.spool_new_contexts(out,values[2],details,selected,{},time.monotonic(),expected_receipt_sha256='d'*64)

    def test_new_only_spool_preserves_full_frame_authority(self):
        values=fixture();_,selected,_=select(values)
        with tempfile.TemporaryDirectory() as td:
            path,indices=self.spool(values,selected,Path(td))
            self.assertEqual(len(indices),1)
            with path.open('rb') as stream:
                self.assertEqual(factory.frozen.read_context(stream,next(iter(indices.values())),selected[0]),values[3][0])
                borrowed=copy.deepcopy(selected[0]);borrowed['authority']['receipt_sha256']='e'*64
                with self.assertRaises(ValueError):factory.frozen.read_context(stream,next(iter(indices.values())),borrowed)

    def test_borrowed_row_or_locator_and_missing_complete_source_cannot_publish_index(self):
        for mutation in ('row','locator','missing','duplicate-selected'):
            values=fixture();_,selected,_=select(values)
            if mutation=='row':values[3][0]['recipe_id']='borrowed'
            elif mutation=='locator':selected[0]['authority']['ordinal']=2
            elif mutation=='missing':values[3].pop()
            else:selected.append(copy.deepcopy(selected[0]))
            with tempfile.TemporaryDirectory() as td:
                folder=Path(td)
                with self.subTest(mutation=mutation),self.assertRaises(ValueError):self.spool(values,selected,folder)
                self.assertFalse((folder/'out/contexts-index.json').exists())

    def test_borrowed_epoch_or_kind_is_refused_before_creating_context_file(self):
        for mutation in ('epoch','kind','record','certificate'):
            values=fixture();_,selected,_=select(values)
            field=dict(epoch='receipt_sha256',kind='kind',record='record_sha256',certificate='certificate_sha256')[mutation]
            selected[0]['authority'][field]='cached-central' if mutation=='kind' else 'e'*64
            with tempfile.TemporaryDirectory() as td:
                folder=Path(td)
                with self.subTest(mutation=mutation),self.assertRaises(ValueError):self.spool(values,selected,folder)
                self.assertFalse((folder/'out/contexts.bin').exists())

    def test_spool_cannot_silently_omit_a_positive_selected_context(self):
        values=fixture()
        with tempfile.TemporaryDirectory() as td:
            folder=Path(td)
            with self.assertRaises(ValueError):self.spool(values,[],folder)
            self.assertFalse((folder/'out/contexts.bin').exists())


if __name__=='__main__':unittest.main()
