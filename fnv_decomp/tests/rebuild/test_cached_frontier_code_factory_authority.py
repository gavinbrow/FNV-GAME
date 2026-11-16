"""Original authored observations; authority literals are not actual receipts."""
import copy
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_frontier_code_factory as factory
from test_cached_root_observe import fixture as observation_fixture
from test_cached_frontier_code_factory import fixture as owner_fixture,select as owner_select


def fixture(*,safeseh=False,one=False):
    values=list(observation_fixture(field=False,safeseh=safeseh))
    if one:
        values[3]=values[3][:1];single=values[4][0];union=copy.deepcopy(single);union['event']='RECIPE_UNION_METADATA_CONTRACT';values[4]=[single,union]
    values[5].update(operation_sha256='c'*64,collector_sha256=factory.PINS['tools/rebuild/cached_root_observe.py'],
        saved_authorities=dict(qualified_request='a'*64),optional_function_index_present=False,qualified_contract_provenance_restamped=False)
    records=list(factory.native.observe_recipe_contracts(*values))
    for i,row in enumerate(records,1):row['qualified_record_ordinal']=i
    receipt=dict(policy_id=factory.native.POLICY,status='metadata-only',input_stability=True,optional_function_index_present=False,
        qualified_contracts_preserved=True,historical_roots_reobserved=0,original_binding_stream_traversals=0,owner_stream_traversals=0,cache_frame_reads=0,
        native_object_observation_reads=1,native_object_parse_attempts=1,inputs=dict(qualified_request=dict(sha256='a'*64)),
        operation_sha256='c'*64,source_sha256=factory.PINS['tools/rebuild/cached_root_observe.py'],**factory.native.FALSE)
    receipt['observations']=[factory.native.summary_row(row,i) for i,row in enumerate(records,1)]
    receipt['summary']=dict(roots=len(values[3]),recipes=1,records=len(records),
        singleton_closure=sum(r['closure_observed'] for r in records if r['event']=='SINGLE_ROOT_OBSERVATION'),
        singleton_blocked=sum(not r['closure_observed'] for r in records if r['event']=='SINGLE_ROOT_OBSERVATION'),
        union_closure=sum(r['closure_observed'] for r in records if r['event']=='RECIPE_ROOT_UNION_OBSERVATION'),
        union_blocked=sum(not r['closure_observed'] for r in records if r['event']=='RECIPE_ROOT_UNION_OBSERVATION'))
    request=dict(kind='fnv-finite-ordinary-root-request',schema_version=1,roots=values[3])
    groups=[]
    for root in values[3]:
        name=factory.base.pool.canonical({k:root[k] for k in ('recipe_id','object_sha256','symbol_index')})
        groups.append(dict(symbol=name,classification='CODE',observed_roles=['code'],included_provenance_is_extraction_proof=False,original_bases=[root['original_address']]))
    current=dict(kind='actual-unresolved-LNK-target-groups',executable_execution=False,runtime_eligible=False,classifications=dict(CODE=len(groups)),groups=groups)
    epoch=dict(kind='prepared-CODE-collision-exclusions',ordinary_prepared_count=0,collision_exclusion_count=0,exclusion_names=[],
        application_selection_inferred_from_counts=False,provider_selected=False,runtime_eligible=False,application_manifest_adopted=False)
    return [receipt,records,request,current,epoch]


def select(values):
    return factory.select_candidates(*values,expected_census=(len(values[2]['roots']),1,len(values[1])),expected_current_codes=len(values[2]['roots']),expected_prepared=(0,0))


def reseal(values,index):
    row=values[1][index]
    if 'certificate' in row:row['certificate_sha256']=factory.digest(row['certificate'])
    values[0]['observations'][index]=factory.native.summary_row(row,index+1)


class IndependentCachedFactoryAuthorityTests(unittest.TestCase):
    def test_every_positive_singleton_selected_but_union_stays_evidence(self):
        values=fixture();before=copy.deepcopy(values);request,selected,ledger=select(values)
        self.assertEqual(values,before);self.assertEqual(len(selected),2);self.assertEqual(request['roots'],values[2]['roots'])
        self.assertEqual([r['state'] for r in ledger],['ALL_POSITIVE_SINGLETON_REQUESTED']*2+['RECIPE_UNION_EVIDENCE_ONLY'])

    def test_singleton_sized_positive_union_is_never_selected_as_second_export(self):
        request,selected,ledger=select(fixture(one=True))
        self.assertEqual(len(request['roots']),1);self.assertEqual(len(selected),1);self.assertEqual(len(ledger),2)

    def test_real_negative_and_union_blockers_are_preserved_without_typed_promotion(self):
        values=fixture(safeseh=True);request,selected,ledger=select(values)
        self.assertEqual(len(selected),1);self.assertEqual([r['state'] for r in ledger],['ALL_POSITIVE_SINGLETON_REQUESTED','ORIGINAL_NEGATIVE_PRESERVED','RECIPE_UNION_EVIDENCE_ONLY'])
        self.assertIn('LIVE_SAFESEH_HANDLER_REQUIRES_ADAPTER',ledger[1]['blocker_codes'])
        row=values[1][1];row['certificate']['policy_id']='typed-composed-root-policy';reseal(values,1)
        with self.assertRaises(ValueError):select(values)

    def test_record_cannot_borrow_source_receipt_operation_or_qualified_authority(self):
        for mode in ('source','operation','receipt-ref','qualified-row'):
            values=fixture();row=values[1][0]
            if mode=='source':row['observation_provenance']['collector_sha256']='e'*64
            elif mode=='operation':row['observation_provenance']['operation_sha256']='e'*64
            elif mode=='receipt-ref':row['observation_provenance']['saved_authorities']['qualified_request']='e'*64
            else:row['qualified_metadata_row_sha256']='e'*64
            reseal(values,0)
            with self.subTest(mode=mode),self.assertRaises(ValueError):select(values)

    def test_rehashed_certificate_provenance_cannot_be_borrowed(self):
        values=fixture();values[1][0]['certificate']['provenance']=dict(values[1][0]['certificate']['provenance'],source_sha256='e'*64);reseal(values,0)
        with self.assertRaises(ValueError):select(values)

    def test_missing_duplicate_and_promoted_negative_records_rejected(self):
        values=fixture(safeseh=True);row=values[1][1];row['closure_observed']=True;reseal(values,1)
        with self.assertRaises(ValueError):select(values)
        for mode in ('missing','duplicate'):
            values=fixture()
            if mode=='missing':values[1].pop()
            else:values[1][1]=copy.deepcopy(values[1][0]);reseal(values,1)
            with self.subTest(mode=mode),self.assertRaises(ValueError):select(values)

    def test_current_namespace_duplicate_and_prepared_or_quarantined_positive_refused(self):
        values=fixture();values[3]['groups'].append(copy.deepcopy(values[3]['groups'][0]))
        with self.assertRaises(ValueError):select(values)
        values=fixture();name=values[3]['groups'][0]['symbol'];values[4].update(collision_exclusion_count=1,exclusion_names=[name])
        with self.assertRaises(ValueError):factory.select_candidates(*values,expected_census=(2,1,3),expected_current_codes=2,expected_prepared=(0,1))
        values=fixture()
        with patch.object(factory,'QUARANTINES',{values[2]['roots'][0]['original_address']}):
            with self.assertRaises(ValueError):select(values)

    def test_borrowed_selected_native_ordinal_is_rejected_before_any_context_write(self):
        values=owner_fixture();_,selected,_=owner_select(values);selection=copy.deepcopy(selected[0])
        selection['authority']['ordinal']=2
        stream=io.BytesIO()
        with self.assertRaises(ValueError):factory.write_context(stream,values['records'][0],selection)
        self.assertEqual(stream.getvalue(),b'')

    def test_selected_row_and_contract_authority_cannot_be_borrowed_before_context_write(self):
        for key in ('record_sha256','certificate_sha256','contract_identity_sha256','qualified_metadata_row_sha256'):
            values=owner_fixture();_,selected,_=owner_select(values);selection=copy.deepcopy(selected[0]);selection['authority'][key]='f'*64
            stream=io.BytesIO()
            with self.subTest(key=key),self.assertRaises(ValueError):factory.write_context(stream,values['records'][0],selection)
            self.assertEqual(stream.getvalue(),b'')

    def test_exact_independent_review_cannot_self_approve_or_expand_execution_permission(self):
        for mode in ('owner','game','native-tools','no-emission','operation','producers'):
            review=dict(schema_version=1,kind='cached-frontier-CODE-factory-review-v1',reviewer='/root/independent-authored',approved=True,
                root_authorized=True,independent_source_schema_review_pass=True,artifact_input_review_pass=True,operation_sha256='b'*64,
                source_sha256={k:'a'*64 for k in factory.OWNED},producer_sha256=copy.deepcopy(factory.PINS),allow_original_objects_read=True,
                allow_source_hashing=True,allow_reference_image_read=True,allow_code_emission=True,allow_native_tools=False,allow_executable_link=False,allow_game_execution=False)
            if mode=='owner':review['reviewer']='/root/code_lane_02'
            elif mode=='game':review['allow_game_execution']=True
            elif mode=='native-tools':review['allow_native_tools']=True
            elif mode=='no-emission':review['allow_code_emission']=False
            elif mode=='operation':review['operation_sha256']='c'*64
            else:review['producer_sha256']['tools/rebuild/cached_root_observe.py']='f'*64
            args=SimpleNamespace(review='build/rebuild/authored-review.json',review_sha256='a'*64,operation_sha256='b'*64)
            with self.subTest(mode=mode),patch.object(factory,'load_ref',return_value=review),patch.object(factory.base,'observe') as reader:
                with self.assertRaises(ValueError):factory.review_gate(args,{})
                reader.assert_not_called()

    def test_known_inventory_epoch_missing_application_flag_is_preserved_without_fabrication(self):
        values=fixture();epoch=values[4];epoch.pop('application_manifest_adopted')
        epoch.update(schema_version=6,policy_id=factory.metadata.POLICY,application_selected_code_count=None,**factory.metadata.FALSE)
        before=copy.deepcopy(epoch);request,selected,_=select(values)
        self.assertEqual(len(selected),2);self.assertEqual(epoch,before)
        self.assertNotIn('application_manifest_adopted',epoch)
        epoch['application_manifest_adopted']=True
        with self.assertRaises(ValueError):select(values)


if __name__=='__main__':unittest.main()
