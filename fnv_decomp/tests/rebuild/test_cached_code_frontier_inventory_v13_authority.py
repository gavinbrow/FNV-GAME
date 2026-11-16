"""Synthetic saved authority envelopes only; literal pins confer no real proof."""
import copy
from collections import Counter
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_code_frontier_inventory_v13 as subject
from test_cached_code_frontier_inventory_authority import universe,routing_fixture
from test_cached_code_frontier_inventory_v13 import fixture as small_fixture,registry as small_registry


def full_fixture():
    providers,units,roots,_=universe(720);old=routing_fixture()[3]
    for i,r in enumerate(roots[528:708]):
        old_address=r['original_address'];p=providers.pop(old_address)
        address=['0x009781d0','0x00452580','0x004e6370'][i] if i<3 else old_address
        rid='native-authored-%d'%(i%77);h='%064x'%(9000+i%77)
        p.update(recipe_id=rid,object_sha256=h,value=(i//77)*32)
        r.update(original_address=address,recipe_id=rid,recipe_index=528+i%77,object_sha256=h,value=(i//77)*32)
        p['planned_canonical_name']=subject.base.pool.canonical({k:p[k] for k in ('recipe_id','object_sha256','symbol_index')})
        providers[address]=p;units[rid]=dict(recipe_index=r['recipe_index'],object_sha256=h,source_sha256=r['source_sha256'])
    requested=roots[528:708];summaries=[];counts=Counter({k:0 for k in ('singleton_closure','singleton_blocked','union_closure','union_blocked')})
    for i in range(77):
        rs=[r for r in requested if r['recipe_index']==528+i]
        scopes=[('SINGLE_ROOT_OBSERVATION',[r],requested.index(r)<5) for r in rs]+[('RECIPE_ROOT_UNION_OBSERVATION',rs,i%2==0)]
        for event,scope,positive in scopes:
            ordinal=len(summaries)+1;summaries.append(dict(ordinal=ordinal,event=event,recipe_id=rs[0]['recipe_id'],recipe_index=528+i,
                roots=[r['original_address'] for r in scope],qualified_record_ordinal=ordinal,record_sha256='%064x'%(10000+ordinal),
                qualified_metadata_row_sha256='%064x'%(11000+ordinal),contract_identity_sha256='%064x'%(12000+ordinal),
                certificate_sha256='%064x'%(13000+ordinal),closure_observed=positive,graph_observation_complete=True,
                blocker_codes={} if positive else {'AUTHORED_BLOCKER':1}))
            counts[('singleton_' if event=='SINGLE_ROOT_OBSERVATION' else 'union_')+('closure' if positive else 'blocked')]+=1
    receipt=dict(schema_version=1,policy_id=subject.native.POLICY,status='metadata-only',operation_sha256=subject.KNOWN['native_operation'],
        source_sha256=subject.PINS['tools/rebuild/cached_root_observe.py'],inputs=dict(qualified_request=dict(sha256=subject.QUALIFIED_REQUEST)),
        qualified_contracts_preserved=True,input_stability=True,optional_function_index_present=False,native_object_observation_reads=77,native_object_parse_attempts=77,
        historical_roots_reobserved=0,original_binding_stream_traversals=0,owner_stream_traversals=0,cache_frame_reads=0,
        observations=summaries,summary=dict(roots=180,recipes=77,records=257,**dict(counts)),**subject.native.FALSE)
    request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=requested)
    chosen=list(range(580))+[600]+list(range(708,720));groups=[]
    for i in chosen:
        r=roots[i];name=subject.base.pool.canonical({k:r[k] for k in ('recipe_id','object_sha256','symbol_index')})
        groups.append(dict(symbol=name,classification='CODE',observed_roles=['code'],original_bases=[r['original_address']],
            original_targets=[r['original_address']],included_provenance_is_extraction_proof=False))
    current=dict(kind='actual-unresolved-LNK-target-groups',groups=groups,classifications=dict(CODE=593),executable_execution=False,runtime_eligible=False)
    quarantines=[dict(root=copy.deepcopy(roots[i]),fresh_body_compared=False,blockers=[dict(code='CANONICAL_REFERENCE_GROUP_REQUIRES_REVIEWED_V2')]) for i in (0,1,2,528,529,530)]
    exclusions={subject.base.pool.canonical({k:roots[i][k] for k in ('recipe_id','object_sha256','symbol_index')}) for i in (3,531)}
    return old,receipt,request,providers,units,current,quarantines,exclusions


class IndependentV13AuthorityTests(unittest.TestCase):
    def test_708_registry_preserves_four_old_authorities_and_distinct_native_contract_identity(self):
        values=full_fixture();before=copy.deepcopy(values);result=subject.extend_registry(*values[:5])
        self.assertEqual(values,before);self.assertEqual(result['roots'],708)
        self.assertEqual({a:result['records'][a] for a in values[0]['records']},values[0]['records'])
        for root in values[2]['roots']:
            row=result['records'][root['original_address']];authority=row['authority']
            self.assertEqual(authority['kind'],'cached-native');self.assertEqual(authority['receipt_sha256'],subject.NATIVE_RECEIPT)
            self.assertEqual(authority['contract_identity_sha256'],row['summary']['contract_identity_sha256'])
            self.assertIs(authority['qualification_certificate_created'],False)
        self.assertFalse(result['certificate_created']);self.assertEqual(result['native_union_summaries_evidence_only'],77)

    def test_593_routing_hydrates_genuine_missing_and_unprepared_positive_not_delta(self):
        values=full_fixture();registry=subject.extend_registry(*values[:5]);before=copy.deepcopy(registry)
        result=subject.classify_demands(values[5],values[3],values[4],registry,values[7],values[6])
        self.assertEqual(registry,before);self.assertEqual(result['code_demands'],593);self.assertEqual(result['registry_roots'],708)
        self.assertEqual(result['counts'],dict(PRESERVED_REFERENCE_GROUP_QUARANTINE=6,PREPARED_SKIP=2,
            CACHED_BARE_POSITIVE_REQUIRES_FRESH_CLASSIFICATION=2,CACHED_ORIGINAL_OMISSION_BLOCKED=571,NEW_SELECTED_ROOT_REQUIRES_OBSERVATION=12))
        self.assertEqual(len(result['metadata_requests']),14);self.assertNotEqual(len(result['metadata_requests']),72)
        for row in result['records']:
            if row['state'] in ('PRESERVED_REFERENCE_GROUP_QUARANTINE','PREPARED_SKIP','CACHED_ORIGINAL_OMISSION_BLOCKED'):self.assertEqual(row['inventory_action'],'LEDGER_ONLY')

    def test_borrowed_source_request_operation_and_qualified_native_locators_rejected(self):
        for mode in ('source','request','operation','ordinal','qualified-ordinal','contract-hash','certificate-hash','bool-root'):
            args=small_fixture();receipt=args[1]
            if mode=='source':receipt['source_sha256']='e'*64
            elif mode=='request':receipt['inputs']['qualified_request']['sha256']='e'*64
            elif mode=='operation':receipt['operation_sha256']='e'*64
            elif mode=='ordinal':receipt['observations'][0]['ordinal']=True
            elif mode=='qualified-ordinal':receipt['observations'][0]['qualified_record_ordinal']=2
            elif mode=='contract-hash':receipt['observations'][0]['contract_identity_sha256']='g'*64
            elif mode=='certificate-hash':receipt['observations'][0]['certificate_sha256']='g'*64
            else:args[2]['roots'][0]['value']=False
            with self.subTest(mode=mode),self.assertRaises(ValueError):small_registry(args)

    def test_missing_duplicate_union_or_singleton_summaries_cannot_extend_registry(self):
        for mode in ('missing','duplicate','union-scope'):
            args=small_fixture()
            if mode=='missing':args[1]['observations'].pop()
            elif mode=='duplicate':args[1]['observations'][1]=copy.deepcopy(args[1]['observations'][0]);args[1]['observations'][1]['ordinal']=args[1]['observations'][1]['qualified_record_ordinal']=2
            else:args[1]['observations'][-1]['roots']=args[1]['observations'][-1]['roots'][:1]
            with self.subTest(mode=mode),self.assertRaises(ValueError):small_registry(args)

    def test_six_quarantines_cannot_be_reclassified_prepared_or_freshly_compared(self):
        for mode in ('missing','prepared','fresh','bool'):
            values=full_fixture();registry=subject.extend_registry(*values[:5])
            if mode=='missing':values[6].pop()
            elif mode=='prepared':values[7].add(values[5]['groups'][0]['symbol'])
            elif mode=='fresh':values[6][0]['fresh_body_compared']=True
            else:values[6][0]['root']['value']=False
            with self.subTest(mode=mode),self.assertRaises(ValueError):subject.classify_demands(values[5],values[3],values[4],registry,values[7],values[6])

    def test_historical_namespace_roles_and_missing_application_state_are_preserved(self):
        providers,units,_,_=universe(1);rows=[]
        for i,category in enumerate(('ordinary','application-candidate')):
            identity=dict(recipe_id='historic-role-%d'%i,object_sha256='a'*64,symbol_index=i+9)
            rows.append(dict(category=category,canonical=subject.base.pool.canonical(identity),namespace_identity=identity,
                original_address='0x0086beb0',identity_mode='historic-reviewed-role',opaque_future_marker=[True,1,False,0]))
        epoch=dict(kind='prepared-CODE-collision-exclusions',ordinary_prepared_count=1,collision_exclusion_count=2,records=rows,
            exclusion_names=[r['canonical'] for r in rows],ordinary_names=[rows[0]['canonical']],application_selection_inferred_from_counts=False,
            application_selected_code_count=None,**subject.FALSE)
        before=copy.deepcopy(epoch);result=subject.validate_epoch(epoch,providers,units,expected=(1,2))
        self.assertEqual(epoch,before);self.assertEqual(result,before);self.assertNotIn('application_manifest_adopted',result)
        epoch['application_manifest_adopted']=True
        with self.assertRaises(ValueError):subject.validate_epoch(epoch,providers,units,expected=(1,2))

    def test_native_unsupported_format_keeps_missing_certificate_as_negative_not_qualification_cert(self):
        args=small_fixture()
        for summary in args[1]['observations']:
            summary.update(certificate_sha256=None,closure_observed=False,graph_observation_complete=False,
                blocker_codes={'UNSUPPORTED_ORIGINAL_COFF_FORMAT':1})
        args[1]['summary'].update(singleton_closure=0,singleton_blocked=2,union_closure=0,union_blocked=1)
        result=small_registry(args)
        for row in result['records'].values():
            self.assertIsNone(row['authority']['certificate_sha256']);self.assertFalse(row['authority']['qualification_certificate_created'])
        ledger=subject.classify_demands(args[5],args[3],args[4],result,set(),[],expected_code_count=2,expected_quarantines=set())
        self.assertEqual(ledger['metadata_requests'],[])
        self.assertEqual(ledger['counts'],{'CACHED_ORIGINAL_OMISSION_BLOCKED':2})

    def test_explicit_zero_summary_counters_stay_typed(self):
        args=small_fixture();result=small_registry(args);self.assertEqual(len(result['records']),2)
        for key,value,original in (('singleton_blocked',False,0),('union_blocked',False,0),('union_closure',True,1)):
            altered=small_fixture();self.assertEqual(altered[1]['summary'][key],original);altered[1]['summary'][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):small_registry(altered)


if __name__=='__main__':unittest.main()
