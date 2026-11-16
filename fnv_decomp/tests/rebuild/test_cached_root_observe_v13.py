"""Authored V13 contracts and synthetic COFF; no saved/native Game inputs."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_root_observe_v13 as current
import cached_root_observe as previous
from test_cached_root_observe import fixture as authored_fixture


def fixture(**kwargs):
    args=list(authored_fixture(**kwargs))
    for view in args[4]:
        view['policy_id']=current.QUALIFIED_POLICY
        view['contract']['provenance'].update(collector_policy_id=current.QUALIFIED_POLICY,metadata_operation_sha256='e'*64)
        view['contract_sha256']=view['new_metadata_contract_sha256']=current.digest(view['contract'])
    return args


def epoch_fixture():
    """Authored metadata only; no producer/native evidence or bytes are loaded."""
    records=[dict(canonical='_authored_prepared_'+str(i),original_address='0x%08x'%(0x01000000+i),
        category='ordinary' if i<14528 else 'application-candidate') for i in range(14534)]
    historical=dict(schema_version=7,kind='prepared-CODE-collision-exclusions',policy_id='prepared-CODE56-successor-v1',
        records=records,exclusion_names=sorted(r['canonical'] for r in records),
        ordinary_names=sorted(r['canonical'] for r in records if r['category']=='ordinary'),
        ordinary_prepared_count=14528,collision_exclusion_count=14534,application_selected_code_count=None,
        application_selection_inferred_from_counts=False,historical_records_preserved=True,provider_selected=False,runtime_eligible=False)
    identity={k:current.UUID_ROOT[k] for k in ('recipe_id','object_sha256','symbol_index')}
    name='_fnv_code_'+current.digest(identity)
    row=dict(canonical=name,original_address=current.UUID_ROOT['original_address'],category='ordinary',
        original_root=copy.deepcopy(current.UUID_ROOT),namespace_identity=dict(identity),origin_identity=dict(identity),
        cohort='UUID2768-qualified-directive-projection',identity_mode='original-selected-physical-qualified-UUID-directives',
        logical_binding_applied=True,original_field_count=9,
        original_negative_certificate_sha256='7c4704d0c777585656272cd2a39a06437d124e34d4cea712236b982641cf9a26',
        qualified_composition_sha256='69076d817070c2411fbb8d3dbf9cf1ea0ca3409d6a438360c25dffc19aa7d238',
        source_ledger_sha256=current.UUID_SUCCESSOR_PROVENANCE['qualified_uuid_handoff_sha256'],
        native_receipt_sha256=current.UUID_SUCCESSOR_PROVENANCE['qualified_uuid_native_sha256'],
        native_review_sha256=current.UUID_SUCCESSOR_PROVENANCE['qualified_uuid_native_review_sha256'])
    latest=copy.deepcopy(historical);latest.update(schema_version=8,policy_id='prepared-UUID2768-successor-v1',
        parent_manifest_sha256='250c9cf8be4cd98e805eb81ed89daae989bab6d262cab5cf0f3e8040120693af',records=copy.deepcopy(records)+[row],
        exclusion_names=sorted(historical['exclusion_names']+[name]),ordinary_names=sorted(historical['ordinary_names']+[name]),
        ordinary_prepared_count=14529,collision_exclusion_count=14535,qualified_uuid_export_count=1,qualified_uuid_field_count=9,
        historical_records_preserved=True,fresh_original_stability_verified=False,**current.UUID_SUCCESSOR_PROVENANCE)
    request=[dict(original_address='0x00600000')]
    providers={current.UUID_ROOT['original_address']:identity,'0x00600000':dict(recipe_id='authored-new',object_sha256='c'*64,symbol_index=8)}
    return historical,latest,request,providers


class V13CoreTests(unittest.TestCase):
    def test_honest_v13_envelopes_and_direct_frozen_semantics(self):
        args=fixture();before=copy.deepcopy(args)
        with patch.object(current.coff,'parse',wraps=current.coff.parse) as parser:
            records=list(current.observe_recipe_contracts(*args));self.assertEqual(parser.call_count,1)
        self.assertEqual(args,before)
        obj=current.coff.parse(args[0])
        for record,qualified in zip(records,args[4]):
            self.assertEqual(record['policy_id'],current.POLICY)
            self.assertEqual(record['qualified_metadata_identity']['policy_id'],current.QUALIFIED_POLICY)
            self.assertEqual(record['qualified_metadata_row_sha256'],current.digest(qualified))
            self.assertEqual(record['contract'],qualified['contract'])
            self.assertEqual(record['certificate'],current.ordinary.assess_object(obj,qualified['contract']))
            for key in current.FALSE:self.assertIs(record[key],False)

    def test_v1_and_v13_policies_are_not_interchangeable(self):
        with self.assertRaises(ValueError):list(current.observe_recipe_contracts(*authored_fixture()))
        with self.assertRaises(ValueError):list(previous.observe_recipe_contracts(*fixture()))
        self.assertEqual(previous.QUALIFIED_POLICY,'cached-CODE-frontier-inventory-v1')
        self.assertEqual(previous.MAX_ROOTS,180)

    def test_source_only_actual_gate_fails_before_any_input_open(self):
        with patch.object(current,'ACTUAL_OPERATION_PROFILE',None),patch.object(Path,'open',side_effect=AssertionError('unexpected input read')) as opened:
            with self.assertRaisesRegex(ValueError,'gates remain unset'):current.run(object())
            opened.assert_not_called()

    def test_measured_forecast_is_not_an_operation_or_a_positive(self):
        self.assertEqual((current.MAX_ROOTS,current.MAX_RECIPES,current.MAX_RECORDS),(72,44,116))
        records=list(current.observe_recipe_contracts(*fixture(safeseh=True)))
        self.assertTrue(any(not record['closure_observed'] for record in records))
        self.assertTrue(all(record['full_serialization_eligible'] is False for record in records))

    def test_wrong_span_source_or_raw_bytes_remain_fatal(self):
        for kind in ('span','source','raw','bool'):
            args=fixture()
            if kind=='span':args[2]['verified_functions'][0]['value']+=1
            elif kind=='source':args[1]['source_sha256']='0'*64
            elif kind=='raw':args[0]+=b'changed'
            else:args[1]['recipe_index']=False
            with self.subTest(kind=kind),self.assertRaises(ValueError):list(current.observe_recipe_contracts(*args))

    def test_certificate_bearing_metadata_and_partial_batches_rejected(self):
        for kind in ('certificate','promotion','partial','duplicate'):
            args=fixture()
            if kind=='certificate':args[4][0]['certificate']={}
            elif kind=='promotion':args[4][0]['certificate_created']=True
            elif kind=='partial':args[4].pop()
            else:args[4].insert(1,copy.deepcopy(args[4][0]))
            with self.subTest(kind=kind),self.assertRaises(ValueError):list(current.observe_recipe_contracts(*args))

    def test_incoming_context_and_physical_addends_are_not_weakened(self):
        args=fixture();args[4][0]['contract']['fields'][0]['coff_relocation']['addend']+=1
        view=args[4][0];view['contract_sha256']=view['new_metadata_contract_sha256']=current.digest(view['contract'])
        with self.assertRaises(ValueError):list(current.observe_recipe_contracts(*args))
        args=fixture();args[4][-1]['contract']['iat_import_observation']['function']='GetForegroundWindow'
        view=args[4][-1];view['contract_sha256']=view['new_metadata_contract_sha256']=current.digest(view['contract'])
        with self.assertRaises(ValueError):list(current.observe_recipe_contracts(*args))


class V13OperationalGuardTests(unittest.TestCase):
    def operation(self):
        return dict(schema_version=1,kind='whole-qualified-contract-native-observation',policy_id=current.POLICY,
            epoch='authored-v13',roots=72,recipes=44,records=116,limits=dict(current.LIMITS),source_sha256='9'*64,
            artifacts={k:dict(path='build/rebuild/authored/'+k+'.json',sha256=v) for k,v in current.ARTIFACT_PINS.items()})

    def test_exact_new_profile_and_policy_gate(self):
        current.validate_operation(self.operation())
        for kind in ('old_policy','old_counts','unaccepted_main','foreign_path','collision'):
            op=self.operation()
            if kind=='old_policy':op['policy_id']=previous.POLICY
            elif kind=='old_counts':op['roots']=180
            elif kind=='unaccepted_main':op['artifacts']['qualification_main_review']['sha256']='0'*64
            elif kind=='foreign_path':op['artifacts']['selection']['path']='../foreign.json'
            else:op['artifacts']['selection']['path']=op['artifacts']['manifest']['path']
            with self.subTest(kind=kind),self.assertRaises(ValueError):current.validate_operation(op)

    def test_missing_main_acceptance_fails_before_open(self):
        pins=dict(current.ARTIFACT_PINS,qualification_main_review=None)
        with patch.object(current,'ARTIFACT_PINS',pins),patch.object(current,'QUALIFICATION_ARTIFACTS',pins),patch.object(Path,'open') as opened:
            with self.assertRaises(ValueError):current.run(object())
            opened.assert_not_called()

    def test_helper_drift_fails_before_metadata_helpers(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);helper=root/'tools/rebuild/authored.py';helper.parent.mkdir(parents=True);helper.write_bytes(b'changed authored helper')
            with patch.object(current,'ROOT',root),patch.object(current,'PINS',{'authored.py':'0'*64}),patch.object(current,'read_bound_json') as reader,patch.object(current,'require',return_value=None):
                with self.assertRaisesRegex(ValueError,'helper changed'):current.bind_dependency_epoch({})
                reader.assert_not_called()

    def test_run_orders_dependency_gate_before_operation_read(self):
        args=type('Args',(),dict(operation=Path('build/rebuild/authored-operation.json')))()
        with patch.object(current,'bind_dependency_epoch',side_effect=ValueError('drift')),patch.object(current,'read_bound_json') as reader:
            with self.assertRaisesRegex(ValueError,'drift'):current.run(args)
            reader.assert_not_called()


    def test_direct_prepare_bootstraps_before_aliased_validation(self):
        with patch.object(current,'require',side_effect=AssertionError('tampered helper used before verification')),\
             patch.object(current,'bind_dependency_epoch',side_effect=ValueError('helper drift')),\
             patch.object(current,'read_bound_json') as reader:
            with self.assertRaisesRegex(ValueError,'helper drift'):current.prepare_operation(self.operation(),{})
            reader.assert_not_called()

class V13EpochSuccessorTests(unittest.TestCase):
    def test_exact_prefix_and_typed_uuid_append_without_restamping(self):
        args=epoch_fixture();before=current.digest(args)
        proof=current.validate_epoch_successor(*args)
        self.assertEqual(current.digest(args),before);self.assertEqual(proof['preserved_records'],14534)
        self.assertEqual(proof['historical_qualified_epoch_sha256'],current.ARTIFACT_PINS['prepared_epoch'])
        self.assertNotEqual(proof['historical_qualified_epoch_sha256'],proof['historical_parent_manifest_sha256'])
        self.assertFalse(proof['ordinary_closure_inferred']);self.assertFalse(proof['provider_selected'])

    def test_changed_history_extra_rows_or_application_adoption_rejected(self):
        for kind in ('reorder','role','extra','application','counter'):
            args=list(epoch_fixture());latest=args[1]
            if kind=='reorder':latest['records'][0],latest['records'][1]=latest['records'][1],latest['records'][0]
            elif kind=='role':latest['records'][0]['category']='application-candidate'
            elif kind=='extra':latest['records'].append(copy.deepcopy(latest['records'][-1]))
            elif kind=='application':latest['application_manifest_adopted']=True
            else:latest['ordinary_prepared_count']=True
            with self.subTest(kind=kind),self.assertRaises(ValueError):current.validate_epoch_successor(*args)

    def test_uuid_cannot_be_bare_positive_or_new_requested_root(self):
        for kind in ('negative','qualification','namespace','root','parent'):
            args=list(epoch_fixture());row=args[1]['records'][-1]
            if kind=='negative':row['original_negative_certificate_sha256']='0'*64
            elif kind=='qualification':row['cohort']='bare-ordinary-positive'
            elif kind=='namespace':row['namespace_identity']['symbol_index']+=1
            elif kind=='root':args[2]=[dict(original_address=current.UUID_ROOT['original_address'])]
            else:args[1]['parent_manifest_sha256']=current.ARTIFACT_PINS['prepared_epoch']
            with self.subTest(kind=kind),self.assertRaises(ValueError):current.validate_epoch_successor(*args)




if __name__=='__main__':unittest.main()
