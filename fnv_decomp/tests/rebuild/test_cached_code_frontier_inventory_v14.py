"""V14 owner fixtures: synthetic qualification and authored COFF only."""
import copy
from pathlib import Path
import subprocess
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_code_frontier_inventory_v14 as inventory
import test_cached_frontier_code_factory_v13 as authored


def fixture(field=True,safeseh=False):
    args=authored.authored_args(field,safeseh)
    for view in args[4]:
        view['contract']['provenance']['request_sha256']=inventory.QUALIFIED_REQUEST
        view['contract_sha256']=view['new_metadata_contract_sha256']=inventory.digest(view['contract'])
    args[-1]=dict(qualified_request_sha256=inventory.QUALIFIED_REQUEST,operation_sha256=inventory.KNOWN['native_operation'],
        collector_sha256=inventory.PINS['tools/rebuild/cached_root_observe_v13.py'],saved_authorities={'qualified_request':inventory.QUALIFIED_REQUEST},
        optional_function_index_present=False,qualified_contract_provenance_restamped=False)
    records=list(inventory.native.observe_recipe_contracts(*args))
    for i,r in enumerate(records,1):r['qualified_record_ordinal']=i
    receipt=dict(schema_version=1,policy_id=inventory.native.POLICY,status='metadata-only',input_stability=True,
        optional_function_index_present=False,qualified_contracts_preserved=True,historical_roots_reobserved=0,
        original_binding_stream_traversals=0,owner_stream_traversals=0,cache_frame_reads=0,
        native_object_observation_reads=1,native_object_parse_attempts=1,
        inputs={'qualified_request':dict(sha256=inventory.QUALIFIED_REQUEST)},operation_sha256=inventory.KNOWN['native_operation'],
        source_sha256=inventory.PINS['tools/rebuild/cached_root_observe_v13.py'],**inventory.native.FALSE)
    authored.reseal(receipt,records)
    request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=copy.deepcopy(args[3]))
    providers={r['original_address']:{k:v for k,v in r.items() if k not in ('original_address','recipe_index')} for r in request['roots']}
    for value in providers.values():value['planned_canonical_name']=inventory.base.pool.canonical({k:value[k] for k in ('recipe_id','object_sha256','symbol_index')})
    root=request['roots'][0];units={root['recipe_id']:dict(recipe_id=root['recipe_id'],recipe_index=root['recipe_index'],object_sha256=root['object_sha256'],source_sha256=root['source_sha256'])}
    groups=[dict(classification='CODE',symbol=providers[r['original_address']]['planned_canonical_name'],observed_roles=['code'],
        included_provenance_is_extraction_proof=False,original_bases=[r['original_address']],original_targets=[r['original_address']]) for r in request['roots']]
    current=dict(kind='actual-unresolved-LNK-target-groups',executable_execution=False,runtime_eligible=False,classifications={'CODE':2},groups=groups)
    return dict(records={}),receipt,request,providers,units,current,records


def registry(args):return inventory.extend_registry(*args[:5],expected_old=0,expected_new=2,expected_recipes=1)


class OwnerV14InventoryTests(unittest.TestCase):
    def test_new_native_authority_profile_keeps_qualified_and_fresh_identities_distinct(self):
        args=fixture();before=copy.deepcopy(args);result=registry(args)
        self.assertEqual(args,before);self.assertEqual(result['preserved_registry_roots'],0)
        self.assertEqual(result['new_native_singleton_authorities'],2)
        for row in result['records'].values():
            a=row['authority'];s=row['summary']
            self.assertEqual(a['kind'],'cached-native-v13')
            self.assertEqual(a['receipt_sha256'],inventory.NATIVE_RECEIPT)
            self.assertEqual(a['certificate_sha256'],s['certificate_sha256'])
            self.assertEqual(a['qualified_metadata_row_sha256'],s['qualified_metadata_row_sha256'])
            self.assertFalse(a['qualification_certificate_created'])
        self.assertFalse(result['native_certificate_bodies_reloaded'])

    def test_negative_singleton_and_union_are_not_metadata_unlocks(self):
        args=fixture(field=False,safeseh=True);result=registry(args)
        out=inventory.classify_demands(args[5],args[3],args[4],result,set(),[],expected_code_count=2,expected_quarantines=set())
        self.assertEqual(len(out['metadata_requests']),1)
        self.assertEqual(sum(out['counts'].values()),2)
        self.assertFalse(out['certificate_created'])

    def test_old_native_epoch_cannot_be_used_for_new_profile(self):
        args=fixture();args[1]['source_sha256']=inventory.previous.PINS['tools/rebuild/cached_root_observe.py']
        with self.assertRaises(ValueError):registry(args)

    def test_complete_native_summary_census_required(self):
        args=fixture();args[1]['observations'].pop()
        with self.assertRaises(ValueError):registry(args)

    def test_fresh_process_cli_help(self):
        p=subprocess.run([sys.executable,str(ROOT/'tools/rebuild/cached_code_frontier_inventory_v14.py'),'--help'],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr);self.assertIn('--operation',p.stdout)


if __name__=='__main__':unittest.main()
