"""Authored registry/routing authority only; literal pins are not actual proof."""
import copy
from collections import Counter
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_code_frontier_inventory_v14 as subject
from test_cached_code_frontier_inventory_authority import universe
from test_cached_code_frontier_inventory_v13_authority import full_fixture as prior_fixture


def full_fixture():
    previous=prior_fixture();old=subject.previous.extend_registry(*previous[:5])
    providers,units=copy.deepcopy(previous[3:5]);extra,extra_units,roots,_=universe(820)
    for r in roots[720:]:providers[r['original_address']]=extra[r['original_address']];units[r['recipe_id']]=extra_units[r['recipe_id']]
    requested=roots[720:792]
    for i,r in enumerate(requested):
        p=providers[r['original_address']];rid='V14-new-native-authored-%d'%(i%44);h='%064x'%(20000+i%44)
        p.update(recipe_id=rid,object_sha256=h,value=(i//44)*32)
        p['planned_canonical_name']=subject.base.pool.canonical({k:p[k] for k in ('recipe_id','object_sha256','symbol_index')})
        r.update(recipe_id=rid,recipe_index=720+i%44,object_sha256=h,value=(i//44)*32)
        units[rid]=dict(recipe_index=r['recipe_index'],object_sha256=h,source_sha256=r['source_sha256'])
    summaries=[];counts=Counter({k:0 for k in ('singleton_closure','singleton_blocked','union_closure','union_blocked')})
    for i in range(44):
        rs=[r for r in requested if r['recipe_index']==720+i]
        scopes=[('SINGLE_ROOT_OBSERVATION',[r],requested.index(r)<4) for r in rs]+[('RECIPE_ROOT_UNION_OBSERVATION',rs,i%2==0)]
        for event,scope,positive in scopes:
            ordinal=len(summaries)+1;summaries.append(dict(ordinal=ordinal,event=event,recipe_id=rs[0]['recipe_id'],recipe_index=720+i,
                roots=[r['original_address'] for r in scope],qualified_record_ordinal=ordinal,record_sha256='%064x'%(30000+ordinal),
                qualified_metadata_row_sha256='%064x'%(31000+ordinal),contract_identity_sha256='%064x'%(32000+ordinal),
                certificate_sha256='%064x'%(33000+ordinal),closure_observed=positive,graph_observation_complete=True,
                blocker_codes={} if positive else {'AUTHORED_BLOCKER':1}))
            counts[('singleton_' if event=='SINGLE_ROOT_OBSERVATION' else 'union_')+('closure' if positive else 'blocked')]+=1
    receipt=dict(schema_version=1,policy_id=subject.native.POLICY,status='metadata-only',operation_sha256=subject.KNOWN['native_operation'],
        source_sha256=subject.PINS['tools/rebuild/cached_root_observe_v13.py'],inputs=dict(qualified_request=dict(sha256=subject.QUALIFIED_REQUEST)),
        qualified_contracts_preserved=True,input_stability=True,optional_function_index_present=False,native_object_observation_reads=44,native_object_parse_attempts=44,
        historical_roots_reobserved=0,original_binding_stream_traversals=0,owner_stream_traversals=0,cache_frame_reads=0,
        observations=summaries,summary=dict(roots=72,recipes=44,records=116,**dict(counts)),**subject.native.FALSE)
    request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=requested)
    selected=list(old['records'].values())[:610];current_roots=[r['root'] for r in selected]+requested[:5]+roots[792:803]
    groups=[dict(symbol=subject.base.pool.canonical({k:r[k] for k in ('recipe_id','object_sha256','symbol_index')}),classification='CODE',
        observed_roles=['code'],original_bases=[r['original_address']],original_targets=[r['original_address']],included_provenance_is_extraction_proof=False) for r in current_roots]
    current=dict(kind='actual-unresolved-LNK-target-groups',groups=groups,classifications=dict(CODE=626),executable_execution=False,runtime_eligible=False)
    return old,receipt,request,providers,units,current,previous[6],previous[7]


def registry(values):return subject.extend_registry(*values[:5])
def classify(values,reg=None):
    return subject.classify_demands(values[5],values[3],values[4],registry(values) if reg is None else reg,values[7],values[6])


class IndependentV14AuthorityTests(unittest.TestCase):
    def test_780_preserves_old708_and_appends_distinct72_summary_authorities_only(self):
        values=full_fixture();before=copy.deepcopy(values);result=registry(values)
        self.assertEqual(values,before);self.assertEqual(result['roots'],780)
        self.assertEqual({a:result['records'][a] for a in values[0]['records']},values[0]['records'])
        self.assertEqual(result['native_union_summaries_evidence_only'],44)
        for root in values[2]['roots']:
            row=result['records'][root['original_address']];a=row['authority']
            self.assertEqual(a['kind'],'cached-native-v13');self.assertEqual(a['receipt_sha256'],subject.NATIVE_RECEIPT)
            self.assertEqual(a['request_sha256'],subject.QUALIFIED_REQUEST);self.assertEqual(a['contract_identity_sha256'],row['summary']['contract_identity_sha256'])
            self.assertIs(a['qualification_certificate_created'],False)
        self.assertFalse(result['native_certificate_bodies_reloaded']);self.assertFalse(result['certificate_created'])

    def test_626_routing_derives_hydration_not_delta55_and_preserves_six_quarantines(self):
        values=full_fixture();result=classify(values)
        self.assertEqual(len(result['records']),626);self.assertEqual(result['registry_roots'],780)
        self.assertEqual(len(result['metadata_requests']),17);self.assertNotEqual(len(result['metadata_requests']),55)
        self.assertEqual(result['counts']['PRESERVED_REFERENCE_GROUP_QUARANTINE'],6)
        self.assertEqual(result['counts']['NEW_SELECTED_ROOT_REQUIRES_OBSERVATION'],11)
        self.assertEqual(result['counts']['CACHED_BARE_POSITIVE_REQUIRES_FRESH_CLASSIFICATION'],6)
        wanted={r['original_address'] for r in result['metadata_requests']}
        self.assertTrue(wanted.isdisjoint(subject.QUARANTINE_ADDRESSES))
        self.assertFalse(result['certificate_created']);self.assertFalse(result['provider_selected'])

    def test_native_receipt_policy_operation_source_request_and_counters_cannot_borrow(self):
        for key in ('policy','operation','source','request','counter','schema'):
            values=full_fixture();r=values[1]
            if key=='policy':r['policy_id']=subject.previous.native.POLICY
            elif key=='operation':r['operation_sha256']=subject.previous.KNOWN['native_operation']
            elif key=='source':r['source_sha256']=subject.previous.PINS['tools/rebuild/cached_root_observe.py']
            elif key=='request':r['inputs']['qualified_request']['sha256']=subject.previous.QUALIFIED_REQUEST
            elif key=='counter':r['historical_roots_reobserved']=False
            else:r['schema_version']=True
            with self.subTest(key=key),self.assertRaises(ValueError):registry(values)

    def test_native_summary_census_bools_digests_and_ordinals_rejected(self):
        for key in ('ordinal','qualified','recipe','digest','counter-zero','duplicate-root'):
            values=full_fixture();r=values[1];s=r['observations'][0]
            if key=='ordinal':s['ordinal']=True
            elif key=='qualified':s['qualified_record_ordinal']=True
            elif key=='recipe':s['recipe_index']=True
            elif key=='digest':s['contract_identity_sha256']='z'*64
            elif key=='duplicate-root':values[2]['roots'][1]=copy.deepcopy(values[2]['roots'][0])
            else:
                for row in r['observations']:row.update(closure_observed=True,blocker_codes={})
                r['summary'].update(singleton_closure=72,singleton_blocked=False,union_closure=44,union_blocked=0)
            with self.subTest(key=key),self.assertRaises(ValueError):registry(values)

    def test_negative_missing_certificate_and_positive_union_never_promote_singleton(self):
        values=full_fixture();negative=next(s for s in values[1]['observations'] if s['event']=='SINGLE_ROOT_OBSERVATION' and not s['closure_observed'])
        negative.update(certificate_sha256=None,graph_observation_complete=False)
        reg=registry(values);address=negative['roots'][0]
        self.assertIsNone(reg['records'][address]['authority']['certificate_sha256'])
        result=classify(values,reg)
        self.assertNotIn(address,{r['original_address'] for r in result['metadata_requests']})
        negative['closure_observed']=True
        with self.assertRaises(ValueError):registry(values)

    def test_mutated_cached_native_authority_and_summary_cannot_route(self):
        for key in ('receipt','request','ordinal','contract','qualification','graph-type','recipe-index'):
            values=full_fixture();reg=registry(values);root=values[2]['roots'][0];row=reg['records'][root['original_address']];a=row['authority'];s=row['summary']
            if key=='receipt':a['receipt_sha256']=subject.previous.NATIVE_RECEIPT
            elif key=='request':a['request_sha256']=subject.previous.QUALIFIED_REQUEST
            elif key=='ordinal':a['ordinal']=True
            elif key=='contract':a['contract_identity_sha256']='d'*64
            elif key=='qualification':a['qualification_certificate_created']=True
            elif key=='graph-type':s['closure_observed']=1
            else:s['recipe_index']=True
            with self.subTest(key=key),self.assertRaises(ValueError):classify(values,reg)

    def test_quarantine_identity_and_prepared_collision_fail_closed(self):
        for key in ('identity','count','prepared'):
            values=full_fixture()
            if key=='identity':values[6][0]['root']['symbol_index']=True
            elif key=='count':values[6].pop()
            else:
                r=values[6][0]['root'];values[7].add(subject.base.pool.canonical({k:r[k] for k in ('recipe_id','object_sha256','symbol_index')}))
            with self.subTest(key=key),self.assertRaises(ValueError):classify(values)

    def test_epoch_preserves_historical_namespace_roles_and_unknown_app_state(self):
        identities=[dict(recipe_id='authored-historical-role-%d'%i,object_sha256='a'*64,symbol_index=i) for i in range(2)]
        rows=[dict(namespace_identity=p,canonical=subject.base.pool.canonical(p),category='ordinary' if i==0 else 'application-candidate',
                   original_address='0x%08x'%(0x400000+i*32),identity_mode='authored-historical-role',
                   original_negative_certificate_sha256='b'*64,opaque_nested_marker=dict(unchanged=True)) for i,p in enumerate(identities)]
        epoch=dict(kind='prepared-CODE-collision-exclusions',ordinary_prepared_count=1,collision_exclusion_count=2,records=rows,
            exclusion_names=sorted(r['canonical'] for r in rows),ordinary_names=[rows[0]['canonical']],
            application_selection_inferred_from_counts=False,application_selected_code_count=None,**subject.FALSE)
        before=copy.deepcopy(epoch)
        self.assertEqual(subject.validate_epoch(epoch,{}, {},expected=(1,2)),before)
        self.assertEqual(epoch,before);self.assertNotIn('application_manifest_adopted',epoch)
        for mode in ('count','canonical','adoption-true','adoption-none','adoption-zero'):
            bad=copy.deepcopy(epoch)
            if mode=='count':bad['ordinary_prepared_count']=True
            elif mode=='canonical':bad['records'][0]['namespace_identity']['symbol_index']=40
            else:bad['application_manifest_adopted']={'adoption-true':True,'adoption-none':None,'adoption-zero':0}[mode]
            with self.subTest(mode=mode),self.assertRaises(ValueError):subject.validate_epoch(bad,{}, {},expected=(1,2))

    def test_successor_source_is_hash_checked_before_compile(self):
        for poisoned_helper in (False,True):
            with self.subTest(poisoned_helper=poisoned_helper),patch.object(subject.Path,'read_bytes',return_value=b'raise RuntimeError("must not compile")'),patch('builtins.compile') as compile_source:
                if poisoned_helper:
                    with patch.object(subject,'require',return_value=None):
                        with self.assertRaises(ValueError):subject.bind_successor()
                else:
                    with self.assertRaises(ValueError):subject.bind_successor()
                compile_source.assert_not_called()


if __name__=='__main__':unittest.main()
