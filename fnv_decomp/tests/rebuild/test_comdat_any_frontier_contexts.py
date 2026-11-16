"""Full-sized authored metadata fixtures; no files, COFF, or original inputs."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import comdat_any_frontier_contexts as c


def fixture():
    registry=dict(schema_version=1,kind='distinct-authority-original-root-registry',policy_id=c.FRONTIER_POLICY,
        roots=269,authorities=copy.deepcopy(c.producer.AUTHORITIES),records={},
        contract_digest_loaded_only_from_authenticated_body=True)
    registry.update({k:False for k in c.REGISTRY_FALSE})
    def root(i,base):
        return dict(original_address='0x%08x'%(base+i*32),recipe_id='authored_%04d'%i,
            recipe_index=i,object_sha256='%064x'%(i+1),source_sha256='%064x'%(i+2000),
            symbol='_authored_%d'%i,symbol_index=i,section=1,value=0,size=16)
    def summ(r,ordinal,positive=False):
        return dict(ordinal=ordinal,event='SINGLE_ROOT_OBSERVATION',recipe_id=r['recipe_id'],
            roots=[r['original_address']],record_sha256='%064x'%(ordinal+3000),certificate_sha256='%064x'%(ordinal+4000),
            closure_observed=positive,graph_observation_complete=True,
            blocker_codes={} if positive else {c.ROOT_BLOCKER if ordinal%3==0 else 'UNSUPPORTED_SECTION_SEMANTICS':1})
    for i in range(269):
        r=root(i,0x800000)
        if i==179:r['original_address']='0x0086beb0'
        authority=c.producer.AUTHORITIES[0 if i<205 else 1 if i<215 else 2]
        s=summ(r,i+1)
        if i<205:
            s['lane']=1;s['lane_record_ordinal']=s.pop('ordinal')
        a={k:authority[k] for k in ('kind','receipt_sha256','request_sha256')}
        a.update(record_sha256=s['record_sha256'],certificate_sha256=s['certificate_sha256'],
            contract_identity_sha256=None,contract_identity_is_bound_through_record_hash=True,ordinal=i+1)
        if i<205:a['lane']=1
        registry['records'][r['original_address']]=dict(root=r,summary=s,authority=a)
    frontier=dict(schema_version=1,kind='current-CODE-frontier-reconciliation',policy_id=c.FRONTIER_POLICY,
        frontier='accepted-V8',code_demands=467,counts=copy.deepcopy(c.COUNTS),records=[],new_roots=[],cached_positive_roots=[],
        eligibility_not_inferred_from_closure=True)
    frontier.update({k:False for k in ('provider_selected','runtime_eligible','ABI_verified','link_ready',
        'application_manifest_adopted','executable_link_performed','game_execution_performed','native_tools_run',
        'code_emission_performed','original_objects_read','original_image_read','source_bodies_read')})
    def demand(r,state):
        i=len(frontier['records'])+1
        d=dict(symbol=c.pool.canonical(c.root_identity(r)),group_ordinal=i,group_sha256='%064x'%(i+5000),
            original_bases=[r['original_address']],original_targets=[r['original_address']],state=state,root=r)
        frontier['records'].append(d);return d
    for i,row in enumerate(list(registry['records'].values())[:180]):
        d=demand(row['root'],'CACHED_ORIGINAL_OMISSION_BLOCKED' if i<179 else 'PRESERVED_REFERENCE_GROUP_QUARANTINE')
        d.update(cached_observation=row['summary'],cache_authority=row['authority'])
        if i==179:d['quarantine_sha256']='e'*64
    observations=[]
    for i in range(259):
        r=root(i+269,0x900000);frontier['new_roots'].append(r)
        demand(r,'NEW_SELECTED_ROOT_REQUIRES_OBSERVATION')
        s=summ(r,len(observations)+1,positive=i%7==0);observations.append(s)
        u=copy.deepcopy(s);u['ordinal']+=1;u['event']='RECIPE_ROOT_UNION_OBSERVATION';observations.append(u)
    for i in range(28):
        frontier['records'].append(dict(symbol='_unproved_%d'%i,group_ordinal=440+i,group_sha256='%064x'%(6000+i),
            original_bases=[],original_targets=[],state='PREPARED_SKIP' if i<3 else 'UNSELECTED_OR_NAMESPACE_UNPROVED'))
    receipt=dict(schema_version=1,policy_id=c.producer.POLICY,status='metadata-only',epoch='authored-V8',
        inputs={},context_sha256='c'*64,baseline_binding_census={},collector_sha256=c.COLLECTOR_PIN,details_bytes=1234,
        original_native_epoch='retained-full-v3',
        authority_kind='new-frontier-v3',prior_authorities=copy.deepcopy(c.producer.AUTHORITIES),cached_roots=269,
        planned_map_sha256=c.producer.MAP_PIN,details_sha256='d'*64,observations=observations,
        summary=dict(roots=259,recipes=259,events={'SINGLE_ROOT_OBSERVATION':259,'RECIPE_ROOT_UNION_OBSERVATION':259},
            singleton_closure=37,singleton_blocked=222),owner_stream_traversals=0,binding_stream_traversals=1,
        cached_roots_reobserved=0,input_stability=True,optional_function_index_present=False,game_fixups_approved=0,
        **c.producer.FALSE)
    return rebind(frontier,registry,receipt)


def rebind(frontier,registry,receipt):
    receipt['cache_registry_sha256']=c.document_hash(registry)
    receipt['frontier_join_sha256']=c.document_hash(frontier)
    receipt['request_sha256']=c.document_hash(dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=frontier['new_roots']))
    return frontier,registry,receipt,c.document_hash(receipt,sort_keys=False)


class ContextSelectorTests(unittest.TestCase):
    def test_complete_current_profile_and_deferred_no_promotion(self):
        args=fixture();before=copy.deepcopy(args);result=c.select_candidates(*args)
        self.assertEqual(args,before);self.assertGreater(len(result['roots']),0)
        self.assertEqual(len(result['audit']),467)
        self.assertEqual(result['counts']['selected']+result['counts']['preserved'],467)
        self.assertFalse(result['selection2_inferred']);self.assertFalse(result['candidate_policy_evaluated'])
        for r in result['candidates']:
            self.assertIsNone(r['authority']['contract_identity_sha256'])
            self.assertFalse(r['summary']['closure_observed'])
            self.assertIn(c.ROOT_BLOCKER,r['summary']['blocker_codes'])
        result['roots'][0]['size']=900
        self.assertEqual(args,before)

    def test_preserves_prepared_unproved_and_reference_quarantine(self):
        result=c.select_candidates(*fixture())
        preserved=[a for a in result['audit'] if a['original_state'] in
            ('PREPARED_SKIP','UNSELECTED_OR_NAMESPACE_UNPROVED','PRESERVED_REFERENCE_GROUP_QUARANTINE')]
        self.assertEqual(len(preserved),29);self.assertTrue(all(not a['selected'] for a in preserved))

    def test_hash_bindings_and_missing_coverage_fail(self):
        for key in ('cache_registry_sha256','request_sha256','frontier_join_sha256'):
            f,r,n,h=fixture();n[key]='f'*64
            with self.subTest(key=key),self.assertRaises(ValueError):c.select_candidates(f,r,n,c.document_hash(n,sort_keys=False))
        f,r,n,h=fixture();n['observations'].pop()
        with self.assertRaises(ValueError):c.select_candidates(*rebind(f,r,n))

    def test_typed_root_and_summary_boolean_aliases_fail(self):
        for key in ('section','value','symbol_index','recipe_index'):
            f,r,n,h=fixture();f['new_roots'][0][key]=False
            with self.subTest(key=key),self.assertRaises(ValueError):c.select_candidates(*rebind(f,r,n))
        f,r,n,h=fixture();n['observations'][1]['ordinal']=True
        with self.assertRaises(ValueError):c.select_candidates(*rebind(f,r,n))

    def test_cache_source_locator_cannot_be_borrowed(self):
        f,r,n,h=fixture();row=f['records'][0];row['cache_authority']=copy.deepcopy(f['records'][1]['cache_authority'])
        with self.assertRaises(ValueError):c.select_candidates(*rebind(f,r,n))

    def test_positive_new_summaries_never_selected(self):
        f,r,n,h=fixture();result=c.select_candidates(f,r,n,h)
        selected={c['root']['original_address'] for c in result['candidates']}
        for s in n['observations']:
            if s['closure_observed']:self.assertTrue(selected.isdisjoint(s['roots']))

    def test_windows_receipt_bytes_and_unknown_promotions_are_strict(self):
        f,r,n,h=fixture()
        lf=hashlib.sha256((json.dumps(n,separators=(',',':'))+'\n').encode()).hexdigest()
        self.assertNotEqual(lf,h)
        with self.assertRaises(ValueError):c.select_candidates(f,r,n,lf)
        n=dict(reversed(list(n.items())))
        with self.assertRaises(ValueError):c.select_candidates(f,r,n,h)
        for which in ('frontier','registry','receipt'):
            f,r,n,h=fixture();{'frontier':f,'registry':r,'receipt':n}[which]['future_approval']=True
            with self.subTest(which=which),self.assertRaises(ValueError):c.select_candidates(*rebind(f,r,n))


if __name__=='__main__':unittest.main()
