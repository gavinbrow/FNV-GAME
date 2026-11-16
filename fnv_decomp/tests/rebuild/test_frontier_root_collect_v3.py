"""Synthetic three-authority registry and 259-root bound; no original inputs."""
import copy
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import frontier_root_collect_v3 as c
import frontier_root_collect as old
import frontier_root_collect_v2 as old2
from test_scalableordinary_root_collect import fixture


def registry_fixture():
    records={}
    for i in range(269):
        address='0x%08x'%(0x700000+i);a=c.AUTHORITIES[0 if i<205 else 1 if i<215 else 2]
        root=dict(original_address=address,recipe_id='cached%03d'%i,recipe_index=i,object_sha256='a'*64,
            source_sha256='b'*64,symbol='_cached'+str(i),symbol_index=i,section=i+1,value=0,size=4)
        h=c.digest(root);summary=dict(event='SINGLE_ROOT_OBSERVATION',roots=[address],recipe_id=root['recipe_id'],
            closure_observed=i%2==0,graph_observation_complete=i%2==0,record_sha256=h,certificate_sha256=h)
        authority=dict(kind=a['kind'],receipt_sha256=a['receipt_sha256'],request_sha256=a['request_sha256'],
            record_sha256=h,certificate_sha256=h,contract_identity_sha256=None,contract_identity_is_bound_through_record_hash=True)
        records[address]=dict(root=root,authority=authority,summary=summary)
    r=dict(schema_version=1,kind='distinct-authority-original-root-registry',authorities=copy.deepcopy(c.AUTHORITIES),roots=269,records=records)
    r.update({k:False for k in ('provider_selected','runtime_eligible','ABI_verified','link_ready','materialization_approved',
        'native_tools_run','code_emission_performed','compiler_performed','executable_link_performed','game_execution_performed',
        'original_image_read','original_objects_read','source_bodies_read')})
    return r


def context_for(request):
    return dict(schema_version=3,kind='new-original-frontier-root-context-v3',epoch='application-link-v8-original-selected',
        request_sha256='a'*64,frontier_join_sha256='b'*64,planned_map_sha256=c.MAP_PIN,cache_registry_sha256=c.REGISTRY_PIN,
        new_original_addresses=[r['original_address'] for r in request['roots']],provider_selected=False,runtime_eligible=False,emission_performed=False)


class RegistryCollectorTests(unittest.TestCase):
    def test_three_authorities_preserved_without_fabricated_contract_digests(self):
        registry=registry_fixture();before=copy.deepcopy(registry)
        self.assertEqual(len(c.validate_registry(registry)),269);self.assertEqual(registry,before)
        self.assertEqual(registry['authorities'][0]['roots'],205);self.assertEqual(registry['authorities'][1]['roots'],10)
        self.assertEqual(registry['authorities'][2]['roots'],54)
        self.assertEqual(registry['authorities'][1]['kind'],registry['authorities'][2]['kind'])
        self.assertNotEqual(registry['authorities'][1]['receipt_sha256'],registry['authorities'][2]['receipt_sha256'])

    def test_259_new_roots_fit_but_260_do_not(self):
        rows=[]
        for i in range(259):rows.append(dict(original_address='0x%08x'%(0x500000+i)))
        request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=rows)
        self.assertEqual(c.validate_context(context_for(request),request,registry_fixture(),'a'*64,'b'*64),'application-link-v8-original-selected')
        request['roots'].append(dict(original_address='0x00510000'))
        with self.assertRaises(ValueError):c.validate_context(context_for(request),request,registry_fixture(),'a'*64,'b'*64)

    def test_cached_roots_from_either_authority_are_rejected(self):
        for address in ('0x00700000','0x007000d6','0x0070010c'):
            request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=[dict(original_address=address)])
            with self.subTest(address=address),self.assertRaises(ValueError):
                c.validate_context(context_for(request),request,registry_fixture(),'a'*64,'b'*64)

    def test_wrong_registry_count_or_authority_and_status_hash_fail(self):
        mutations=[lambda r:r.update(roots=214),lambda r:r['authorities'][0].update(request_sha256='f'*64),
            lambda r:r['records']['0x00700000']['authority'].update(receipt_sha256='f'*64),
            lambda r:r['records']['0x00700000']['summary'].update(record_sha256='f'*64),
            lambda r:r['records']['0x00700000']['authority'].update(contract_identity_sha256='f'*64),
            lambda r:r.update(provider_selected=True)]
        for mutate in mutations:
            r=registry_fixture();mutate(r)
            with self.assertRaises(ValueError):c.validate_registry(r)

    def test_duplicate_cached_physical_identity_fails(self):
        r=registry_fixture();a=r['records']['0x00700000']['root'];b=r['records']['0x00700001']['root']
        for k in ('recipe_id','object_sha256','symbol_index'):b[k]=a[k]
        r['records']['0x00700001']['summary']['recipe_id']=a['recipe_id']
        with self.assertRaises(ValueError):c.validate_registry(r)

    def test_cached_selected_and_planned_physical_joins(self):
        r=registry_fixture();selections={};providers={}
        for a,row in r['records'].items():
            root=row['root'];selections[a]={k:root[k] for k in ('recipe_index','symbol','section','value','size')}
            providers[a]={k:root[k] for k in ('recipe_id','object_sha256','source_sha256','symbol_index')}
        self.assertEqual(len(c.validate_registry(r,selections,dict(providers=providers))),269)
        providers['0x00700000']['symbol_index']=999
        with self.assertRaises(ValueError):c.validate_registry(r,selections,dict(providers=providers))

    def test_wrong_context_epoch_pins_duplicates_and_unknown_keys_fail(self):
        request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=fixture()[3])
        for key,value in [('cache_registry_sha256','f'*64),('planned_map_sha256','f'*64),('request_sha256','f'*64),
                          ('frontier_join_sha256','f'*64),('schema_version',1),('epoch',''),('runtime_eligible',True),('unknown',True)]:
            context=context_for(request);context[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):c.validate_context(context,request,registry_fixture(),'a'*64,'b'*64)
        request['roots'].append(request['roots'][0])
        with self.assertRaises(ValueError):c.validate_context(context_for(request),request,registry_fixture(),'a'*64,'b'*64)

    def test_frozen_v1_still_has_its_original_policy_and_32_cap(self):
        self.assertEqual(old.MAX_ROOTS,32);self.assertEqual(old.POLICY,'new-frontier-ordinary-root-observation-v1')
        self.assertEqual(c.file_hash(old.__file__),'751cf4fb09d94a41abcb37778fcdd194484cb498a465aaa9eb9c22e7438705f8')
        self.assertEqual(old2.MAX_ROOTS,54);self.assertEqual(old2.POLICY,'new-frontier-ordinary-root-observation-v2')
        self.assertEqual(c.file_hash(old2.__file__),'5ef81ff45b7959d75b9c2bc2289cb1af28c2c271de7d8432b1cc6c5dc38c1b79')

    def test_same_kind_authority_cannot_borrow_another_receipt(self):
        r=registry_fixture();row=r['records']['0x0070010c']
        row['authority']['receipt_sha256']=c.AUTHORITIES[1]['receipt_sha256']
        with self.assertRaises(ValueError):c.validate_registry(r)

    def test_shared_observer_retains_complete_singleton_union_and_scope(self):
        raw,u,p,rows,_,_,bucket=fixture(safeseh=True)
        records=list(c.central.observe_recipe(raw,u,p,rows,bucket,{},dict(object_sha256=u['object_sha256'],source_sha256=u['source_sha256'],prior_authorities=c.AUTHORITIES)))
        self.assertEqual(len(records),3)
        for i,r in enumerate(records,1):
            summary=c.summary_row(r,i)
            self.assertEqual(summary['graph_observation_complete'],r['graph_observation_complete'])
            self.assertEqual(r['contract']['provenance']['prior_authorities'],c.AUTHORITIES)
            self.assertFalse(r['namespace_approved']);self.assertFalse(r['runtime_eligible'])


if __name__=='__main__':unittest.main()
