"""New-policy authored authority cases; no actual V13 qualification is consumed."""
import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_root_observe_v13 as subject
from test_scalableordinary_root_collect import fixture as raw_fixture
from test_cached_root_observe_v13_operational_independent import whole_authored_fixture,qualified_fixture_bytes
from test_cached_root_observe_v13 import epoch_fixture as owner_epoch_fixture


def fixture(*,safeseh=False):
    raw,unit,proof,roots,_,_,buckets=raw_fixture(safeseh=safeseh)
    provenance=dict(object_sha256=unit['object_sha256'],source_sha256=unit['source_sha256'],request_sha256='a'*64,
        collector_policy_id=subject.QUALIFIED_POLICY,metadata_contract_identity_is_new=True,native_observation_required=True)
    frame=dict(recipe_index=0,raw_sha256='b'*64,compressed_sha256='c'*64,row_count=0,first_ordinal=None,last_ordinal=None,
        whole_data_hash_verified_this_read=False,unrequested_frames_verified=False)
    views=[]
    for event,scope in [('SINGLE_ROOT_METADATA_CONTRACT',[r]) for r in roots]+[('RECIPE_UNION_METADATA_CONTRACT',roots)]:
        contract=subject.previous.finite.build_contract(unit,proof,scope,buckets,{},copy.deepcopy(provenance))
        views.append(dict(schema_version=1,kind='new-cached-metadata-contract',policy_id=subject.QUALIFIED_POLICY,event=event,
            requested_roots=copy.deepcopy(scope),contract=contract,contract_sha256=subject.digest(contract),
            new_metadata_contract_sha256=subject.digest(contract),source_frame_verification=copy.deepcopy(frame),native_observation_required=True,
            **{k:False for k in subject.QUALIFIED_FALSE}))
    return [raw,unit,proof,roots,views,dict(qualified_request_sha256='a'*64)]


def run(values):return list(subject.observe_recipe_contracts(*values))
def rehash(view):view['contract_sha256']=view['new_metadata_contract_sha256']=subject.digest(view['contract'])


def context_fixture():
    """Saved-envelope isolation atop MAIN's genuine new/old same-unit fixture."""
    items,request,request_sha=whole_authored_fixture();prepared,rows,_,_=qualified_fixture_bytes(items)
    groups=prepared['groups'];providers={};native_records={};native_summaries=[]
    historical=[item['historical_root'] for item in items]
    for i in range(136):
        historical.append(dict(original_address='0x%08x'%(0x06000000+i*32),recipe_id='authored-old-%d'%(i%33),recipe_index=44+i%33,
            object_sha256='b'*64,source_sha256='c'*64,symbol='_authored_old_%d'%i,symbol_index=i+2,section=1,value=i*32,size=16))
    for i,root in enumerate(historical,1):
        summary=dict(event='SINGLE_ROOT_OBSERVATION',recipe_id=root['recipe_id'],recipe_index=root['recipe_index'],roots=[root['original_address']],
            ordinal=i,qualified_record_ordinal=i,record_sha256='%064x'%(1000+i),certificate_sha256='%064x'%(2000+i),
            contract_identity_sha256='%064x'%(3000+i),qualified_metadata_row_sha256='%064x'%(4000+i),closure_observed=True,graph_observation_complete=True,blocker_codes={})
        native_summaries.append(summary);native_records[root['original_address']]=dict(root=root,summary=copy.deepcopy(summary),
            authority=dict(kind='cached-native',receipt_sha256=subject.ARTIFACT_PINS['old_native_receipt']))
    native_summaries.extend(dict(event='RECIPE_ROOT_UNION_OBSERVATION') for _ in range(77))
    registry=dict(roots=708,records={**{'old-opaque-%d'%i:dict(authority=dict(kind='cached-central')) for i in range(528)},**native_records})
    for root in request['roots']+historical:providers[root['original_address']]={k:root[k] for k in ('recipe_id','object_sha256','symbol_index')}
    for i in range(68657-len(providers)):providers['unused-%d'%i]=dict(recipe_id='unused',object_sha256='e'*64,symbol_index=i)
    current=[];inventory=[]
    for root in request['roots']:
        name='_fnv_code_'+subject.digest(providers[root['original_address']])
        current.append(dict(symbol=name,classification='CODE',observed_roles=['code'],included_provenance_is_extraction_proof=False,original_bases=[root['original_address']]))
        inventory.append(dict(symbol=name,root=root,inventory_action='REQUEST_CACHED_METADATA',new_metadata=prepared['singleton_index'][root['original_address']]))
    for i in range(521):
        current.append(dict(symbol='authored-existing-%d'%i,classification='CODE'))
        inventory.append(dict(symbol='authored-existing-%d'%i,inventory_action='LEDGER_ONLY'))
    receipt=dict(policy_id=subject.QUALIFIED_POLICY,status='metadata-only',qualified_metadata_roots=72,qualified_recipes=44,generated_contract_records=116,
        code_demands=593,registry_roots=708,certificate_created=False,native_observation_required=True,metadata_fingerprints_stable=True,
        provider_selected=False,runtime_eligible=False,native_tools_run=False,original_objects_read=False,source_bodies_read=False,code_emission_performed=False,
        requested_recipe2768=False,requested_recipe_indices=sorted(groups),recipe_frame_verifications=[dict(recipe_index=i,requested_roots=len(rs),verification=prepared['frames'][i]['verification']) for i,rs in groups.items()])
    qualified=dict(metadata_requests=request['roots'],records=inventory)
    current=dict(kind='actual-unresolved-LNK-target-groups',executable_execution=False,runtime_eligible=False,groups=current)
    planned=dict(providers=providers,materialized_exports=0,provider_selected=False,runtime_eligible=False)
    manifest=dict(units=[item['unit'] for item in items]);proof=dict(units=[item['proof'] for item in items],inputs=dict(image_sha256='f'*64))
    selection=dict(selections={a:{} for a in providers})
    imports=dict(inputs=dict(manifest=subject.ARTIFACT_PINS['manifest'],retained=subject.ARTIFACT_PINS['retained'],reference='f'*64),imports=[dict(import_id=175)])
    epoch,latest,_,uuid_providers=owner_epoch_fixture()
    providers.pop('unused-0');providers[subject.UUID_ROOT['original_address']]=uuid_providers[subject.UUID_ROOT['original_address']]
    selection['selections'].pop('unused-0');selection['selections'][subject.UUID_ROOT['original_address']]={}
    old=dict(policy_id=subject.previous.POLICY,source_sha256=subject.PREVIOUS_SOURCE_SHA256,qualified_contracts_preserved=True,input_stability=True,
        optional_function_index_present=False,summary=dict(roots=180,recipes=77,records=257),observations=native_summaries)
    return [receipt,request,qualified,registry,current,planned,manifest,proof,selection,imports,epoch,old,latest],groups,items


def context(values,groups):
    with patch.object(subject.finite,'validate_request',return_value=groups):return subject.validate_saved_context(*values)


def operation_fixture():
    return dict(schema_version=1,kind='whole-qualified-contract-native-observation',policy_id=subject.POLICY,epoch='authored-V13-only',
        roots=72,recipes=44,records=116,limits=copy.deepcopy(subject.LIMITS),source_sha256='a'*64,
        artifacts={k:dict(path='build/rebuild/authored-v13-%s.json'%k,sha256=v) for k,v in subject.ARTIFACT_PINS.items()})


class IndependentV13ObserverAuthorityTests(unittest.TestCase):
    def test_new_profile_preserves_qualified_contracts_and_legacy_globals(self):
        values=fixture();before=copy.deepcopy(values)
        legacy=(subject.previous.POLICY,subject.previous.QUALIFIED_POLICY,subject.previous.MAX_ROOTS,subject.previous.MAX_RECIPES,subject.previous.MAX_RECORDS)
        records=run(values)
        self.assertEqual(values,before);self.assertEqual(len(records),3)
        self.assertEqual((subject.previous.POLICY,subject.previous.QUALIFIED_POLICY,subject.previous.MAX_ROOTS,subject.previous.MAX_RECIPES,subject.previous.MAX_RECORDS),legacy)
        for record,qualified in zip(records,values[4]):
            self.assertEqual(record['policy_id'],subject.POLICY);self.assertEqual(record['contract'],qualified['contract'])
            self.assertEqual(record['qualified_metadata_row_sha256'],subject.digest(qualified));self.assertTrue(record['fresh_certificate_created'])
            self.assertNotIn('certificate',qualified);self.assertFalse(qualified['certificate_created'])
            self.assertEqual(record['certificate']['contract_identity_sha256'],qualified['contract_sha256'])
            for key in subject.FALSE:self.assertIs(record[key],False)

    def test_old_qualification_policy_is_not_restamped_or_accepted(self):
        values=fixture()
        for view in values[4]:view['policy_id']=subject.previous.QUALIFIED_POLICY
        before=copy.deepcopy(values)
        with self.assertRaises(ValueError):run(values)
        self.assertEqual(values,before)

    def test_native_negatives_and_unions_receive_no_typed_or_metadata_waiver(self):
        values=fixture(safeseh=True);records=run(values)
        self.assertFalse(records[1]['closure_observed']);self.assertFalse(records[2]['closure_observed'])
        self.assertIn('LIVE_SAFESEH_HANDLER_REQUIRES_ADAPTER',{b['code'] for b in records[1]['blockers']})
        self.assertEqual(records[1]['contract'],values[4][1]['contract']);self.assertFalse(records[1]['typed_waiver_applied'])

    def test_borrowed_qualified_root_source_request_or_original_certificate_rejected(self):
        for mode in ('root','source','request','certificate','equal-old-certificate'):
            values=fixture();view=values[4][0]
            if mode=='root':view['requested_roots'][0]=copy.deepcopy(values[3][1])
            elif mode=='source':view['contract']['provenance']['source_sha256']='e'*64;rehash(view)
            elif mode=='request':view['contract']['provenance']['request_sha256']='e'*64;rehash(view)
            elif mode=='certificate':view['certificate']={'closure_observed':True}
            else:view['historical_certificate_contract_identity_equal_claimed']=True
            with self.subTest(mode=mode),self.assertRaises(ValueError):run(values)

    def test_missing_duplicate_or_union_before_singletons_is_not_a_complete_recipe(self):
        for mode in ('missing','duplicate','union-first'):
            values=fixture()
            if mode=='missing':values[4].pop()
            elif mode=='duplicate':values[4][1]=copy.deepcopy(values[4][0])
            else:values[4].insert(0,values[4].pop())
            with self.subTest(mode=mode),self.assertRaises(ValueError):run(values)

    def test_source_identity_and_frame_integer_aliases_or_malformed_hashes_rejected(self):
        for mode in ('unit-index','proof-index','root-value','frame-index','frame-hash','request-hash'):
            values=fixture()
            if mode=='unit-index':values[1]['recipe_index']=False
            elif mode=='proof-index':values[2]['recipe_index']=False
            elif mode=='root-value':values[3][0]['value']=False
            elif mode=='frame-index':
                for view in values[4]:view['source_frame_verification']['recipe_index']=False
            elif mode=='frame-hash':
                for view in values[4]:view['source_frame_verification']['raw_sha256']='g'*64
            else:
                values[5]['qualified_request_sha256']='bad'
                for view in values[4]:view['contract']['provenance']['request_sha256']='bad';rehash(view)
            with self.subTest(mode=mode),self.assertRaises(ValueError):run(values)

    def test_new72_roots_can_share44_old_recipe_units_without_reobserving_old_roots(self):
        values,groups,items=context_fixture();before=copy.deepcopy(values);prepared=context(values,groups)
        self.assertEqual(prepared['previous_native_recipe_overlap'],list(range(44)));self.assertEqual(values,before)
        self.assertTrue({r['original_address'] for r in values[1]['roots']}.isdisjoint(values[3]['records']))
        self.assertTrue(all(item['historical_root'] not in prepared['groups'][i] for i,item in enumerate(items)))

    def test_saved_context_rejects_old_root_replay_truncation_and_metadata_certificate_claim(self):
        for mode in ('old-root','truncated','certificate','frame-bool','ordinal-bool'):
            values,groups,items=context_fixture()
            if mode=='old-root':values[1]['roots'][0]=copy.deepcopy(items[0]['historical_root'])
            elif mode=='truncated':values[0]['generated_contract_records']=115
            elif mode=='certificate':values[0]['certificate_created']=True
            elif mode=='frame-bool':values[0]['recipe_frame_verifications'][0]['recipe_index']=False
            else:values[2]['records'][0]['new_metadata']['contract_record_ordinal']=True
            with self.subTest(mode=mode),self.assertRaises(ValueError):context(values,groups)

    def test_old_native_summary_authority_must_match_registry_without_loading_old_body(self):
        for mode in ('source','summary','receipt','recipe-bool'):
            values,groups,_=context_fixture()
            if mode=='source':values[11]['source_sha256']='e'*64
            elif mode=='summary':values[11]['observations'][0]['record_sha256']='e'*64
            else:
                old=next(r for r in values[3]['records'].values() if r['authority']['kind']=='cached-native')
                if mode=='receipt':old['authority']['receipt_sha256']='e'*64
                else:old['root']['recipe_index']=False
            with self.subTest(mode=mode),self.assertRaises(ValueError):context(values,groups)

    def test_current593_demand_cannot_hide_duplicate_or_borrowed_names(self):
        for mode in ('duplicate','foreign'):
            values,groups,_=context_fixture()
            if mode=='duplicate':values[4]['groups'].append(copy.deepcopy(values[4]['groups'][0]))
            else:values[4]['groups'][0]['symbol']='borrowed-current-demand'
            with self.subTest(mode=mode),self.assertRaises(ValueError):context(values,groups)

    def test_unset_or_legacy_operation_profile_fails_before_any_metadata_open(self):
        for profile in (None,dict(roots=180,recipes=77,records=257)):
            with self.subTest(profile=profile),patch.object(subject,'ACTUAL_OPERATION_PROFILE',profile),patch.object(Path,'open',side_effect=AssertionError('unexpected read')) as opened:
                with self.assertRaises(ValueError):subject.run(object())
                opened.assert_not_called()
        for key,bad in (('roots',180),('records',115)):
            operation=operation_fixture();operation[key]=bad
            with self.subTest(key=key),self.assertRaises(ValueError):subject.validate_operation(operation)
        operation=operation_fixture();operation['artifacts']['qualified_registry']['sha256']=subject.previous.ARTIFACT_PINS['qualified_registry']
        with self.assertRaises(ValueError):subject.validate_operation(operation)

    def test_qualification_output_hashes_are_bound_before_saved_context_validation(self):
        operation=operation_fixture();refs=operation['artifacts']
        receipt=dict(output_sha256={filename:refs[role]['sha256'] for role,filename in
            [('qualified_inventory','inventory.json'),('qualified_request','metadata-request.json'),('qualified_registry','cache-registry.json'),
             ('qualified_records','metadata-contracts.jsonl.gz'),('prepared_epoch','prepared-epoch.json')]})
        receipt['output_sha256']['prepared-epoch.json']='e'*64
        def fake_read(path,expected):return receipt if Path(path).name=='authored-v13-qualified_receipt.json' else {}
        with patch.object(subject,'bind_dependency_epoch'),patch.object(subject,'read_bound_json',side_effect=fake_read),patch.object(subject,'validate_saved_context') as checked:
            with self.assertRaises(ValueError):subject.prepare_operation(operation,{})
            checked.assert_not_called()

    def test_latest_epoch_preserves_historical_order_and_only_typed_uuid_without_mutation(self):
        historical,latest,requested,providers=owner_epoch_fixture();before=copy.deepcopy([historical,latest])
        joined=subject.validate_epoch_successor(historical,latest,requested,providers)
        self.assertEqual([historical,latest],before);self.assertEqual(joined['preserved_records'],14534)
        self.assertEqual(joined['typed_uuid_appended'],1);self.assertFalse(joined['ordinary_closure_inferred'])
        self.assertNotIn('application_manifest_adopted',historical);self.assertNotIn('application_manifest_adopted',latest)
        self.assertNotEqual(joined['historical_qualified_epoch_sha256'],joined['historical_parent_manifest_sha256'])

    def test_latest_epoch_borrow_reorder_extra_names_and_unqualified_uuid_promotion_rejected(self):
        for mode in ('reorder','extra-record','extra-name','borrowed-identity','negative','composition','mode','app-state','parent-role','counter-bool','request-collision','peer-ref'):
            if mode=='peer-ref':
                operation=operation_fixture();operation['artifacts']['latest_prepared_review']['sha256']=subject.ARTIFACT_PINS['qualification_authority_review']
                with self.subTest(mode=mode),self.assertRaises(ValueError):subject.validate_operation(operation)
                continue
            historical,latest,requested,providers=owner_epoch_fixture();row=latest['records'][-1]
            if mode=='reorder':latest['records'][0],latest['records'][1]=latest['records'][1],latest['records'][0]
            elif mode=='extra-record':latest['records'].append(copy.deepcopy(row))
            elif mode=='extra-name':latest['exclusion_names'].append('extra-unreviewed-name')
            elif mode=='borrowed-identity':row['namespace_identity']['object_sha256']='e'*64
            elif mode=='negative':row['original_negative_certificate_sha256']='e'*64
            elif mode=='composition':row['qualified_composition_sha256']=None
            elif mode=='mode':row['identity_mode']='ordinary-unqualified-closure'
            elif mode=='app-state':latest['application_manifest_adopted']=False
            elif mode=='parent-role':latest['parent_manifest_sha256']=subject.ARTIFACT_PINS['prepared_epoch']
            elif mode=='counter-bool':latest['ordinary_prepared_count']=True
            else:requested=[copy.deepcopy(subject.UUID_ROOT)]
            with self.subTest(mode=mode),self.assertRaises(ValueError):subject.validate_epoch_successor(historical,latest,requested,providers)


if __name__=='__main__':unittest.main()
