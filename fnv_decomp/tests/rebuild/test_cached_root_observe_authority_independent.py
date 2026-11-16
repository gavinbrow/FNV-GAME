"""Independent authored authority cases; no actual qualified/native inputs."""
import copy
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_root_observe as observer
from test_scalableordinary_root_collect import fixture as ordinary_fixture


def fixture():
    raw,unit,proof,roots,_,_,bindings=ordinary_fixture()
    provenance=dict(object_sha256=unit['object_sha256'],source_sha256=unit['source_sha256'],request_sha256='a'*64,
        metadata_contract_identity_is_new=True,native_observation_required=True,collector_policy_id=observer.QUALIFIED_POLICY)
    frame=dict(recipe_index=0,raw_sha256='b'*64,compressed_sha256='c'*64,row_count=0,first_ordinal=None,last_ordinal=None,
        whole_data_hash_verified_this_read=False,unrequested_frames_verified=False)
    views=[]
    for event,scope in [('SINGLE_ROOT_METADATA_CONTRACT',[roots[0]]),('SINGLE_ROOT_METADATA_CONTRACT',[roots[1]]),('RECIPE_UNION_METADATA_CONTRACT',roots)]:
        contract=observer.finite.build_contract(unit,proof,scope,bindings,{},copy.deepcopy(provenance))
        views.append(dict(schema_version=1,kind='new-cached-metadata-contract',policy_id=observer.QUALIFIED_POLICY,event=event,
            requested_roots=copy.deepcopy(scope),contract=contract,contract_sha256=observer.digest(contract),
            new_metadata_contract_sha256=observer.digest(contract),source_frame_verification=copy.deepcopy(frame),
            native_observation_required=True,**{k:False for k in observer.QUALIFIED_FALSE}))
    return raw,unit,proof,roots,views,dict(qualified_request_sha256='a'*64)


def run(values):return list(observer.observe_recipe_contracts(*values))
def rehash(view):view['contract_sha256']=view['new_metadata_contract_sha256']=observer.digest(view['contract'])


def context_fixture():
    """Envelope-only universe; native validator is patched by its isolated tests."""
    roots=[];groups={i:[] for i in range(77)};providers={}
    for i in range(180):
        root=dict(original_address='0x%08x'%(0x03000000+32*i),recipe_id='authored-%d'%(i%77),recipe_index=i%77,
            object_sha256='b'*64,source_sha256='c'*64,symbol='_authored_%d'%i,symbol_index=i+1,section=1,value=i*16,size=16)
        roots.append(root);groups[i%77].append(root);providers[root['original_address']]={k:root[k] for k in ('recipe_id','object_sha256','symbol_index')}
    providers['0x008d8520']=dict(recipe_id='authored-typed-prepared',object_sha256='d'*64,symbol_index=7)
    for i in range(68657-len(providers)):providers['unused-%d'%i]=dict(recipe_id='unused',object_sha256='e'*64,symbol_index=i)
    code=[dict(symbol='_fnv_code_'+observer.digest(providers[r['original_address']]),classification='CODE',observed_roles=['code'],
        included_provenance_is_extraction_proof=False,original_bases=[r['original_address']]) for r in roots]
    code.extend(dict(symbol='authored-other-%d'%i,classification='CODE') for i in range(397))
    removed='_fnv_code_'+observer.digest(providers['0x008d8520'])
    records=[dict(symbol=g['symbol'],inventory_action='LEDGER_ONLY') for g in code]+[dict(symbol=removed,inventory_action='LEDGER_ONLY')]
    frames=[dict(recipe_index=i,requested_roots=len(rs),verification=dict(recipe_index=i,compressed_sha256='a'*64)) for i,rs in groups.items()]
    receipt=dict(policy_id=observer.QUALIFIED_POLICY,status='metadata-only',qualified_metadata_roots=180,qualified_recipes=77,
        generated_contract_records=257,code_demands=578,registry_roots=528,certificate_created=False,native_observation_required=True,
        recipe_frame_verifications=frames,provider_selected=False,runtime_eligible=False,native_tools_run=False,original_objects_read=False,
        source_bodies_read=False,code_emission_performed=False)
    rows=[];singletons={}
    for i,rs in groups.items():
        for event,scope in [('SINGLE_ROOT_METADATA_CONTRACT',[r]) for r in rs]+[('RECIPE_UNION_METADATA_CONTRACT',rs)]:
            contract=dict(provenance=dict(request_sha256='a'*64))
            row=dict(event=event,requested_roots=copy.deepcopy(scope),contract=contract,contract_sha256=observer.digest(contract),
                new_metadata_contract_sha256=observer.digest(contract),source_frame_verification=frames[i]['verification'])
            rows.append(row)
            if event=='SINGLE_ROOT_METADATA_CONTRACT':singletons[scope[0]['original_address']]=dict(contract_record_ordinal=len(rows),
                generated_record_sha256=observer.digest(row),new_metadata_contract_sha256=row['contract_sha256'],source_frame_verification=row['source_frame_verification'])
    for i,r in enumerate(roots):records[i].update(root=r,inventory_action='REQUEST_CACHED_METADATA',new_metadata=singletons[r['original_address']])
    request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=roots)
    qualified=dict(metadata_requests=roots,records=records)
    registry=dict(roots=528,records={'historical-%d'%i:{} for i in range(528)})
    current=dict(kind='actual-unresolved-LNK-target-groups',executable_execution=False,runtime_eligible=False,groups=code)
    planned=dict(providers=providers,materialized_exports=0,provider_selected=False,runtime_eligible=False)
    manifest=dict(units=[dict(recipe_index=i) for i in groups]);proof=dict(units=[dict(recipe_index=i) for i in groups],inputs=dict(image_sha256='f'*64))
    selection=dict(selections={a:{} for a in providers})
    imports=dict(inputs=dict(manifest=observer.ARTIFACT_PINS['manifest'],retained=observer.ARTIFACT_PINS['retained'],reference='f'*64),imports=[dict(import_id=175)])
    return [receipt,request,qualified,registry,current,planned,manifest,proof,selection,imports],groups,rows


def context(values,groups):
    with patch.object(observer.finite,'validate_request',return_value=groups):return observer.validate_saved_context(*values)


def operation_fixture():
    return dict(schema_version=1,kind='whole-qualified-contract-native-observation',policy_id=observer.POLICY,epoch='authored-only-V11-to-V12',
        roots=180,recipes=77,records=257,limits=copy.deepcopy(observer.LIMITS),source_sha256='a'*64,
        artifacts={k:dict(path='build/rebuild/authored-only-%s.json'%k,sha256=observer.ARTIFACT_PINS.get(k,'b'*64)) for k in observer.ARTIFACT_KEYS})


class IndependentCachedObservationAuthorityTests(unittest.TestCase):
    def test_fresh_certificates_are_outside_unchanged_new_metadata_contracts(self):
        values=fixture();before=copy.deepcopy(values);rows=run(values)
        self.assertEqual(values,before);self.assertEqual(len(rows),3)
        for row,qualified in zip(rows,values[4]):
            self.assertEqual(row['contract'],qualified['contract']);self.assertEqual(row['qualified_metadata_row_sha256'],observer.digest(qualified))
            self.assertEqual(row['contract_identity_sha256'],qualified['contract_sha256'])
            self.assertTrue(row['fresh_certificate_created']);self.assertTrue(row['qualified_contract_unchanged'])
            self.assertEqual(row['certificate_sha256'],observer.digest(row['certificate']))
            self.assertNotIn('certificate',qualified);self.assertFalse(qualified['certificate_created'])
            for flag in observer.FALSE:self.assertIs(row[flag],False)

    def test_missing_duplicate_extra_or_reordered_views_cannot_publish_complete_recipe(self):
        for mode in ('missing-single','missing-union','duplicate-single','duplicate-union','union-first'):
            values=list(fixture());views=values[4]
            if mode=='missing-single':views.pop(0)
            elif mode=='missing-union':views.pop()
            elif mode=='duplicate-single':views[1]=copy.deepcopy(views[0])
            elif mode=='duplicate-union':views.append(copy.deepcopy(views[-1]))
            else:views.insert(0,views.pop())
            with self.subTest(mode=mode),self.assertRaises(ValueError):run(values)

    def test_borrowed_contract_root_source_request_and_digest_are_fatal(self):
        for mode in ('root','source','request','digest','native-root'):
            values=list(fixture());view=values[4][0]
            if mode=='root':view['requested_roots'][0]=copy.deepcopy(values[3][1])
            elif mode=='source':view['contract']['provenance']['source_sha256']='f'*64;rehash(view)
            elif mode=='request':view['contract']['provenance']['request_sha256']='f'*64;rehash(view)
            elif mode=='digest':view['contract_sha256']='f'*64
            else:view['contract']['roots'][0]['symbol_index']=5;rehash(view)
            with self.subTest(mode=mode),self.assertRaises(ValueError):run(values)

    def test_qualified_envelope_cannot_claim_old_certificate_or_promote_metadata(self):
        for key,value in [('schema_version',True),('policy_id','old-negative-certificate'),('certificate_created',True),
            ('historical_certificate_contract_identity_equal_claimed',True),('native_observation_required',False),('runtime_eligible',True),
            ('certificate',{'closure_observed':True}),('certificate_sha256','f'*64)]:
            values=list(fixture());values[4][0][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):run(values)

    def test_requested_physical_boolean_alias_and_wrong_native_slot_are_rejected(self):
        for key,value in [('value',False),('section',True),('symbol_index',5),('recipe_index',False)]:
            values=list(fixture());values[3][0][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):run(values)

    def test_qualified_frame_borrowing_or_whole_cache_claim_is_rejected(self):
        for mode in ('borrowed','whole','unrequested'):
            values=list(fixture());frame=values[4][1]['source_frame_verification']
            frame['compressed_sha256']='e'*64 if mode=='borrowed' else frame['compressed_sha256']
            if mode=='whole':frame['whole_data_hash_verified_this_read']=True
            if mode=='unrequested':frame['unrequested_frames_verified']=True
            with self.subTest(mode=mode),self.assertRaises(ValueError):run(values)

    def test_union_cannot_hide_missing_or_extra_original_reference_partition(self):
        values=list(fixture());union=values[4][-1];union['contract']['provenance']['binding_row_references'].append(dict(ordinal=9,sha256='f'*64));rehash(union)
        with self.assertRaises(ValueError):run(values)

    def test_raw_original_hash_cannot_be_replaced_by_metadata_or_unknown_body(self):
        values=list(fixture());values[0]=b'changed-authored-original'
        with self.assertRaises(ValueError):run(values)

    def test_unit_and_proof_recipe_indices_do_not_alias_boolean_zero(self):
        for index in (1,2):
            values=list(fixture());values[index]['recipe_index']=False
            with self.subTest(index=index),self.assertRaises(ValueError):run(values)

    def test_matching_malformed_request_digest_is_not_authority(self):
        for bad in ('not-a-sha256','g'*64,True):
            values=list(fixture());values[5]['qualified_request_sha256']=bad
            for view in values[4]:view['contract']['provenance']['request_sha256']=bad;rehash(view)
            with self.subTest(value=bad),self.assertRaises(ValueError):run(values)

    def test_frame_recipe_identity_is_typed_even_when_all_views_agree(self):
        values=list(fixture())
        for view in values[4]:view['source_frame_verification']['recipe_index']=False
        with self.assertRaises(ValueError):run(values)

    def test_agreeing_malformed_frame_hashes_or_row_counts_are_rejected(self):
        for key,value in [('raw_sha256','g'*64),('compressed_sha256','bad'),('row_count',False),('row_count',-1)]:
            values=list(fixture())
            for view in values[4]:view['source_frame_verification'][key]=value
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):run(values)

    def test_saved_context_rejects_truncated_request_or_historical_root_reuse(self):
        for mode in ('truncated','historical','scope','promoted','wrong-removal'):
            values,groups,_=context_fixture()
            if mode=='truncated':values[1]['roots']=values[1]['roots'][:-1]
            elif mode=='historical':values[3]['records'].pop('historical-0');values[3]['records'][values[1]['roots'][0]['original_address']]={}
            elif mode=='scope':values[0]['generated_contract_records']=256
            elif mode=='promoted':values[0]['certificate_created']=True
            else:values[4]['groups'][-1]['symbol']='foreign-current-demand'
            with self.subTest(mode=mode),self.assertRaises(ValueError):context(values,groups)

    def test_current_demand_duplicates_cannot_hide_behind_577_symbol_dict(self):
        values,groups,_=context_fixture();values[4]['groups'].append(copy.deepcopy(values[4]['groups'][0]))
        with self.assertRaises(ValueError):context(values,groups)

    def test_saved_singleton_ordinal_cannot_alias_boolean_one(self):
        values,groups,rows=context_fixture()
        address=rows[0]['requested_roots'][0]['original_address']
        next(r for r in values[2]['records'] if r.get('root',{}).get('original_address')==address)['new_metadata']['contract_record_ordinal']=True
        with self.assertRaises(ValueError):context(values,groups)

    def test_saved_context_frame_index_cannot_alias_boolean_zero(self):
        values,groups,_=context_fixture();values[0]['recipe_frame_verifications'][0]['recipe_index']=False
        with self.assertRaises(ValueError):context(values,groups)

    def test_whole_operation_cannot_truncate_or_borrow_old_or_current_authority(self):
        observer.validate_operation(operation_fixture())
        for mode in ('roots','records','receipt','current','path-collision','foreign','extra'):
            value=operation_fixture()
            if mode=='roots':value['roots']=179
            elif mode=='records':value['records']=256
            elif mode=='receipt':value['artifacts']['qualified_receipt']['sha256']='f'*64
            elif mode=='current':value['artifacts']['current_groups']['sha256']='e'*64
            elif mode=='path-collision':value['artifacts']['qualified_inventory']['path']=value['artifacts']['qualified_request']['path']
            elif mode=='foreign':value['artifacts']['qualified_inventory']['path']='../foreign.json'
            else:value['borrowed_negative_certificate']='a'*64
            with self.subTest(mode=mode),self.assertRaises(ValueError):observer.validate_operation(value)

    def test_dynamic_inventory_reference_must_match_sealed_qualification_receipt_before_context(self):
        operation=operation_fixture();refs=operation['artifacts']
        receipt=dict(output_sha256={'inventory.json':'c'*64,'metadata-request.json':refs['qualified_request']['sha256'],
            'cache-registry.json':refs['qualified_registry']['sha256'],'metadata-contracts.jsonl.gz':refs['qualified_records']['sha256']})
        def fake_read(path,expected):return receipt if Path(path).name=='authored-only-qualified_receipt.json' else {}
        with patch.object(observer,'read_bound_json',side_effect=fake_read),patch.object(observer,'validate_saved_context') as checker:
            with self.assertRaises(ValueError):observer.prepare_operation(operation,{})
            checker.assert_not_called()


if __name__=='__main__':unittest.main()
