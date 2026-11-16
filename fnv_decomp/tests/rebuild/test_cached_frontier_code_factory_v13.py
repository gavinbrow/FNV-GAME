"""V13 source-owner fixtures: authored COFF and genuinely new native records."""
import ast
import copy
from pathlib import Path
import sys
import subprocess
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_frontier_code_factory_v13 as factory
import test_cached_root_observe as authored


def authored_args(field=True,safeseh=False):
    args=list(authored.fixture(field=field,safeseh=safeseh))
    # These are new authored qualification inputs, before the new observer runs.
    for view in args[4]:view['policy_id']=factory.native.QUALIFIED_POLICY
    args[-1]=dict(qualified_request_sha256='a'*64,operation_sha256='b'*64,collector_sha256='c'*64,
        saved_authorities={'qualified_request':'a'*64},optional_function_index_present=False,
        qualified_contract_provenance_restamped=False)
    return args


def reseal(receipt,records):
    receipt['observations']=[factory.native.summary_row(r,i) for i,r in enumerate(records,1)]
    receipt['summary']=dict(roots=2,recipes=1,records=3,
        singleton_closure=sum(r['closure_observed'] for r in records if r['event']=='SINGLE_ROOT_OBSERVATION'),
        singleton_blocked=sum(not r['closure_observed'] for r in records if r['event']=='SINGLE_ROOT_OBSERVATION'),
        union_closure=sum(r['closure_observed'] for r in records if r['event']=='RECIPE_ROOT_UNION_OBSERVATION'),
        union_blocked=sum(not r['closure_observed'] for r in records if r['event']=='RECIPE_ROOT_UNION_OBSERVATION'))


def fixture(field=True,safeseh=False):
    args=authored_args(field,safeseh);records=list(factory.native.observe_recipe_contracts(*args))
    for i,row in enumerate(records,1):row['qualified_record_ordinal']=i
    receipt=dict(schema_version=1,policy_id=factory.native.POLICY,status='metadata-only',input_stability=True,
        optional_function_index_present=False,qualified_contracts_preserved=True,historical_roots_reobserved=0,
        original_binding_stream_traversals=0,owner_stream_traversals=0,cache_frame_reads=0,
        native_object_observation_reads=1,native_object_parse_attempts=1,
        inputs={'qualified_request':dict(sha256='a'*64)},operation_sha256='b'*64,source_sha256='c'*64,**factory.native.FALSE)
    request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=copy.deepcopy(args[3]))
    groups=[]
    for root in args[3]:
        name=factory.base.pool.canonical({k:root[k] for k in ('recipe_id','object_sha256','symbol_index')})
        groups.append(dict(classification='CODE',symbol=name,observed_roles=['code'],included_provenance_is_extraction_proof=False,
            original_bases=[root['original_address']],original_targets=[root['original_address']]))
    current=dict(kind='actual-unresolved-LNK-target-groups',executable_execution=False,runtime_eligible=False,
        classifications={'CODE':2},groups=groups)
    prepared=dict(kind='prepared-CODE-collision-exclusions',ordinary_prepared_count=0,collision_exclusion_count=0,
        exclusion_names=[],application_selection_inferred_from_counts=False,provider_selected=False,runtime_eligible=False,application_manifest_adopted=False)
    reseal(receipt,records)
    return receipt,records,request,current,prepared


def select(args):return factory.select_candidates(*args,expected_census=(2,1,3),expected_current_codes=2,expected_prepared=(0,0))


class OwnerV13FactoryTests(unittest.TestCase):
    def test_new_native_policy_selects_all_positive_singletons_not_union(self):
        args=fixture();before=copy.deepcopy(args);request,selections,ledger=select(args)
        self.assertEqual(args,before);self.assertEqual(len(request['roots']),2);self.assertEqual(len(selections),2)
        self.assertEqual(len(ledger),3);self.assertEqual(ledger[-1]['state'],'RECIPE_UNION_EVIDENCE_ONLY')
        self.assertTrue(all(r['policy_id']==factory.native.POLICY for r in args[1]))

    def test_zero_fields_do_not_waive_original_safeseh_negative(self):
        args=fixture(field=False,safeseh=True);request,_,ledger=select(args)
        self.assertEqual(len(request['roots']),1)
        self.assertEqual(ledger[1]['state'],'ORIGINAL_NEGATIVE_PRESERVED')
        self.assertTrue(all(not r['contract']['fields'] for r in args[1]))

    def test_old_outer_policy_cannot_be_resealed_into_new_admission(self):
        args=fixture();args[1][0]['qualified_metadata_identity']['policy_id']=factory.previous.native.QUALIFIED_POLICY
        reseal(args[0],args[1])
        with self.assertRaises(ValueError):select(args)

    def test_protocol_leaf_bodies_are_exact_verified_predecessor_copies(self):
        old=ast.parse((ROOT/'tools/rebuild/cached_frontier_code_factory.py').read_text())
        new=ast.parse((ROOT/'tools/rebuild/cached_frontier_code_factory_v13.py').read_text())
        def methods(tree):return {n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
        old=methods(old);new=methods(new)
        for name in ('qualified_view','validate_selected','write_context','verify_member','field_proof_record'):
            self.assertEqual(ast.dump(old[name]),ast.dump(new[name]),name)

    def test_pending_actual_outcome_pins_reject_before_artifact_access(self):
        with patch.dict(factory.KNOWN,native_main_review=None):
            with self.assertRaisesRegex(ValueError,'remain pending'):factory.validate_operation({})

    def test_fresh_process_cli_help(self):
        result=subprocess.run([sys.executable,str(ROOT/'tools/rebuild/cached_frontier_code_factory_v13.py'),'--help'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('--operation',result.stdout)


if __name__=='__main__':unittest.main()
