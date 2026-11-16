"""Authored V14 contracts and synthetic COFF; no saved/native Game inputs."""
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_root_observe_v14 as current
import cached_root_observe as previous
from test_cached_root_observe import fixture as authored_fixture


def fixture(**kwargs):
    args=list(authored_fixture(**kwargs))
    for view in args[4]:
        view['policy_id']=current.QUALIFIED_POLICY
        view['contract']['provenance'].update(collector_policy_id=current.QUALIFIED_POLICY,metadata_operation_sha256='e'*64)
        view['contract_sha256']=view['new_metadata_contract_sha256']=current.digest(view['contract'])
    return args


class V14CoreTests(unittest.TestCase):
    def test_preparation_orchestration_rejects_wrong_reference(self):
        roles=('qualified_receipt','qualified_inventory','qualified_request','qualified_registry','qualified_records','prepared_epoch',
            'qualification_main_review','qualification_authority_review','qualification_operation','current_groups','current_review',
            'prepared_review','read_reuse_plan','imports','retained','manifest','recipes')
        refs={k:dict(path='build/rebuild/authored/'+k,sha256=('a' if k!='qualified_receipt' else 'b')*64) for k in roles}
        roots=[dict(recipe_index=i%34,original_address=f'0x{i:08x}') for i in range(55)]
        receipt=dict(output_sha256={filename:refs[role]['sha256'] for role,filename in (
            ('qualified_inventory','inventory.json'),('qualified_request','metadata-request.json'),('qualified_registry','cache-registry.json'),
            ('qualified_records','metadata-contracts.jsonl.gz'),('prepared_epoch','prepared-epoch.json'))})
        main=dict(approved=True,status='accepted-metadata-only',independent_saved_output_review_pass=True,receipt_sha256='b'*64,
            operation_sha256='a'*64,complementary_outcome_review_sha256='a'*64,saved_epoch_sha256='a'*64,
            request_artifact_sha256='a'*64,metadata_contracts_sha256='a'*64,native_observation_required=True,
            zero_binding_roots_remain_native_UNKNOWN=True,certificate_created=False,provider_selected=False,runtime_eligible=False)
        peer=dict(approved=True,all_requested_roots_and_union_records_present=True,receipt_sha256='b'*64,operation_sha256='a'*64,
            certificate_created=False,provider_selected=False,runtime_eligible=False)
        data={k:{} for k in roles};data.update(qualified_receipt=receipt,qualified_request=dict(roots=roots),
            qualification_main_review=main,qualification_authority_review=peer,
            manifest=dict(units=[dict(recipe_index=i) for i in range(34)]),
            retained=dict(inputs=dict(image_sha256='image',tools_sha256={}),units=[dict(recipe_index=i) for i in range(34)]),
            imports=dict(inputs=dict(manifest='a'*64,retained='a'*64,reference='image'),imports=[dict(import_id=175)]))
        def read(path,sha):return data[path.name]
        op=dict(artifacts=refs,source_sha256='c'*64)
        with patch.object(current,'require_actual_authority'),patch.object(current,'validate_operation'),patch.object(current,'read_bound_json',side_effect=read),\
             patch.object(current,'validate_current_reviews'),patch.object(current,'validate_frontier_context'),patch.object(current,'validate_roots'),\
             patch.object(current,'validate_qualification_scope',return_value=dict(frames={},singleton_index={})),\
             patch.object(current,'validate_structural_overlap',return_value={}),patch.object(current.finite,'reconcile_recipes',return_value={'verified':True}),\
             patch.object(current.finite,'pin'):
            result=current.prepare_operation(op,{})
            self.assertEqual((sum(map(len,result['groups'].values())),len(result['groups'])),(55,34))
            data['imports']['inputs']['reference']='wrong'
            with self.assertRaisesRegex(ValueError,'reference'):current.prepare_operation(op,{})

    def test_reference_identity_and_publication_retraction(self):
        imports=dict(inputs=dict(manifest='a',retained='b',reference='c'),imports=[dict(import_id=175)])
        proof=dict(inputs=dict(image_sha256='c'))
        self.assertEqual(current.validate_import_authority(imports,proof,'a','b')['import_id'],175)
        with self.assertRaises(ValueError):current.validate_import_authority(imports,dict(inputs=dict(image_sha256='wrong')),'a','b')
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory);out,details,index=base/'out',base/'details',base/'index';published=[]
            result={'details_sha256':hashlib.sha256(b'new').hexdigest()}
            with patch.object(current.finite,'stable',side_effect=[None,ValueError('drift')]),patch.object(previous,'budget',return_value=1),self.assertRaises(ValueError):
                current.publish_outputs(out,details,io.BytesIO(b'new'),result,{},index,published,time.monotonic())
            self.assertFalse(out.exists());self.assertFalse(details.exists())

    def test_complete_stream_census_and_truncated_stream(self):
        groups={i:[] for i in range(34)}
        for i in range(55):groups[i%34].append(dict(recipe_index=i%34,original_address=f'0x{i:08x}'))
        frames={i:dict(verification=dict(recipe_index=i)) for i in groups};rows=[];singles={}
        for i,roots in groups.items():
            for root in roots:
                contract=dict(provenance=dict(request_sha256='a'*64));h=current.digest(contract)
                row=dict(requested_roots=[root],event='SINGLE_ROOT_METADATA_CONTRACT',contract=contract,
                    contract_sha256=h,new_metadata_contract_sha256=h,source_frame_verification=frames[i]['verification'])
                rows.append(row);singles[root['original_address']]=dict(contract_record_ordinal=len(rows),generated_record_sha256=current.digest(row),
                    new_metadata_contract_sha256=h,source_frame_verification=frames[i]['verification'])
            contract=dict(provenance=dict(request_sha256='a'*64));h=current.digest(contract)
            rows.append(dict(requested_roots=roots,event='RECIPE_UNION_METADATA_CONTRACT',contract=contract,
                contract_sha256=h,new_metadata_contract_sha256=h,source_frame_verification=frames[i]['verification']))
        prepared=dict(groups=groups,frames=frames,singleton_index=singles,units={i:i for i in groups},proofs={i:i for i in groups})
        def fake_observer(raw,unit,proof,roots,views,provenance):
            for view in views:yield dict(event=view['event'])
        def run(selected):
            stream=io.BytesIO(b''.join(current.canonical(r)+b'\n' for r in selected));reader=current.QualifiedReader(stream,prepared,'a'*64)
            reads=[]
            with patch.object(current,'observe_recipe_contracts',side_effect=fake_observer):
                out=list(current.stream_observations(prepared,reader,lambda unit:reads.append(unit) or b'fixture',{}))
            return out,reads
        out,reads=run(rows);self.assertEqual((len(out),len(reads)),(89,34))
        self.assertEqual([r['qualified_record_ordinal'] for r in out],list(range(1,90)))
        with self.assertRaises(ValueError):run(rows[:-1])

    def test_bounded_frontier_uses_requested_identities_and_collision_epoch(self):
        roots=[dict(original_address=f'0x{i:08x}',recipe_id=f'unit{i}',object_sha256='a'*64,symbol_index=i) for i in range(55)]
        names=['_fnv_code_'+current.digest({k:r[k] for k in ('recipe_id','object_sha256','symbol_index')}) for r in roots]
        names += [f'other{i}' for i in range(571)]
        rows=[dict(classification='CODE',symbol=n,observed_roles=['code'],included_provenance_is_extraction_proof=False,
            original_bases=[roots[i]['original_address']] if i<55 else []) for i,n in enumerate(names)]
        groups=dict(kind='actual-unresolved-LNK-target-groups',executable_execution=False,runtime_eligible=False,groups=rows)
        inventory=dict(records=[dict(symbol=n) for n in names]);request=dict(roots=roots)
        epoch=dict(schema_version=9,kind='prepared-CODE-collision-exclusions',policy_id='prepared-cached-V13-successor-v1',
            ordinary_prepared_count=14550,collision_exclusion_count=14556,records=[None]*14556,
            exclusion_names=[f'exclusion{i}' for i in range(14556)],ordinary_names=[f'ordinary{i}' for i in range(14550)],
            application_selected_code_count=None,application_selection_inferred_from_counts=False,provider_selected=False,runtime_eligible=False)
        self.assertEqual(len(current.validate_frontier_context(request,inventory,groups,epoch)),55)
        for kind in ('collision','wrong_owner','duplicate_demand','adoption'):
            rq,inv,gr,ep=copy.deepcopy((request,inventory,groups,epoch))
            if kind=='collision':ep['exclusion_names'][0]=names[0]
            elif kind=='wrong_owner':gr['groups'][0]['original_bases']=['0xffffffff']
            elif kind=='duplicate_demand':gr['groups'][1]['symbol']=gr['groups'][0]['symbol']
            else:ep['application_manifest_adopted']=False
            with self.subTest(kind=kind),self.assertRaises(ValueError):current.validate_frontier_context(rq,inv,gr,ep)

    def test_current_reviews_bind_exact_subject_and_nonadoption(self):
        prepared=dict(kind='independent-prepared-cached-v13-successor-outcome-review',status='accepted-derived-metadata-only',epoch_sha256='a'*64)
        current_review=dict(kind='independent-wave14-combined-diagnostic-link-outcome-review',status='accepted-failed-link-diagnostic-only',
            groups_sha256='b'*64,link_exit_code=1120,executable_execution=False,provider_adopted=False,runtime_eligible=False,
            loaded_member_enumeration_claimed=False)
        current.validate_current_reviews(prepared,current_review,'a'*64,'b'*64)
        for kind in ('epoch','groups','execution','adoption'):
            p,r=copy.deepcopy((prepared,current_review))
            if kind=='epoch':p['epoch_sha256']='c'*64
            elif kind=='groups':r['groups_sha256']='c'*64
            elif kind=='execution':r['executable_execution']=True
            else:r['provider_adopted']=True
            with self.subTest(kind=kind),self.assertRaises(ValueError):current.validate_current_reviews(p,r,'a'*64,'b'*64)

    def test_operation_whitelist_binds_roles_paths_and_limits(self):
        allowed=dict(request=dict(path='build/rebuild/request.json',sha256='a'*64),
            receipt=dict(path='build/rebuild/receipt.json',sha256='b'*64))
        operation=dict(schema_version=1,kind='whole-qualified-contract-native-observation',policy_id=current.POLICY,
            epoch='synthetic',roots=55,recipes=34,records=89,limits=copy.deepcopy(current.LIMITS),
            artifacts=copy.deepcopy(allowed),source_sha256='c'*64)
        self.assertEqual(current.validate_operation_envelope(operation,allowed),operation)
        for kind in ('swapped','extra','traversal','bool','limits'):
            op,permitted=copy.deepcopy((operation,allowed))
            if kind=='swapped':op['artifacts']['request'],op['artifacts']['receipt']=op['artifacts']['receipt'],op['artifacts']['request']
            elif kind=='extra':op['artifacts']['extra']=op['artifacts']['request']
            elif kind=='traversal':op['artifacts']['request']['path']=permitted['request']['path']='build/../request.json'
            elif kind=='bool':op['roots']=True
            else:op['limits']['seconds']+=1
            with self.subTest(kind=kind),self.assertRaises(ValueError):current.validate_operation_envelope(op,permitted)

    def test_qualification_scope_rejects_replay_partial_and_promotions(self):
        groups={i:[] for i in range(34)}
        for i in range(55):groups[i%34].append(dict(recipe_index=i%34,original_address=f'0x{i:08x}'))
        roots=[r for rows in groups.values() for r in rows]
        request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=roots)
        receipt=dict(policy_id=current.QUALIFIED_POLICY,status='metadata-only',qualified_metadata_roots=55,
            qualified_recipes=34,generated_contract_records=89,code_demands=626,registry_roots=780,
            certificate_created=False,native_observation_required=True,metadata_fingerprints_stable=True,
            provider_selected=False,runtime_eligible=False,native_tools_run=False,original_objects_read=False,
            source_bodies_read=False,code_emission_performed=False,requested_recipe_indices=list(range(34)),requested_recipe2768=False,
            recipe_frame_verifications=[dict(recipe_index=i,requested_roots=len(rows),verification=dict(recipe_index=i)) for i,rows in groups.items()])
        records=[dict(inventory_action='REQUEST_CACHED_METADATA',root=r,new_metadata=dict(contract_record_ordinal=i+1,
            generated_record_sha256='a'*64,new_metadata_contract_sha256='b'*64)) for i,r in enumerate(roots)]
        records.extend({} for _ in range(626-len(records)))
        inventory=dict(metadata_requests=copy.deepcopy(roots),records=records)
        registry=dict(roots=780,records={f'old{i}':{} for i in range(780)})
        self.assertEqual(len(current.validate_qualification_scope(receipt,request,inventory,registry,groups)['singleton_index']),55)
        for kind in ('replay','promotion','missing_frame','duplicate_ordinal','bool_count','borrowed'):
            rc,rq,inv,reg,gr=copy.deepcopy((receipt,request,inventory,registry,groups))
            if kind=='replay':reg['records'][roots[0]['original_address']]={};reg['records'].pop('old0')
            elif kind=='promotion':rc['certificate_created']=True
            elif kind=='missing_frame':rc['recipe_frame_verifications'].pop()
            elif kind=='duplicate_ordinal':inv['records'][1]['new_metadata']['contract_record_ordinal']=1
            elif kind=='bool_count':rc['qualified_metadata_roots']=True
            else:gr[0][0]['original_address']='0xffffffff'
            with self.subTest(kind=kind),self.assertRaises(ValueError):current.validate_qualification_scope(rc,rq,inv,reg,gr)

    def test_structural_overlap_policy_rejects_widening_and_false_history(self):
        groups={i:[dict(recipe_index=i,recipe_id=str(i),original_address=a) for a in roots]
                for i,roots in current.PROSPECTIVE_OVERLAP.items()}
        plan=dict(kind='V14-broad55-prospective-seven-read-reuse-plan',schema_version=1,
            status='source-plan-not-original-operation-approval',
            broad_request=dict(sha256='c15ea262418bfd23cea06a4e5cf2c24dbe9bb3a019af7c2f454af0d209bd771c',requested_roots=55,requested_recipes=34),
            prior_actual=dict(raw_byte_cache_reusable=False,source_derived_integrity_passes=3,reported_integrity_passes=2,
                exact_two_pass_conformance=False,CPP_content_read=False,CPP_SHA_authority='declared-retained-context-only'),
            reuse_policy=dict(reuse_prior_facts_as_fresh_broad_graph_validation=False,silent_frozen_observer_widening_allowed=False,
                parallel_optional_four_unit_capture_allowed=False,reuse_prior_selected_structural_facts_as_supplement=True,
                future_overlap_payload_observation='one necessary broad55 observation under its own exact accepted operation/input/CPU gate'),
            overlap_units=[dict(recipe_id=str(i),roots=list(roots)) for i,roots in current.PROSPECTIVE_OVERLAP.items()])
        result=current.validate_structural_overlap(groups,plan)
        self.assertEqual((len(result['roots']),len(result['recipes'])),(7,4))
        for change in ('extra_root','bool_index','false_history','reuse','foreign_recipe','duplicate'):
            g,p=copy.deepcopy(groups),copy.deepcopy(plan)
            if change=='extra_root':g[1445].append(dict(recipe_index=1445,recipe_id='1445',original_address='0x00000000'))
            elif change=='bool_index':g[1445][0]['recipe_index']=True
            elif change=='false_history':p['prior_actual']['source_derived_integrity_passes']=2
            elif change=='reuse':p['reuse_policy']['reuse_prior_facts_as_fresh_broad_graph_validation']=True
            elif change=='foreign_recipe':p['overlap_units'][0]['recipe_id']='foreign'
            else:p['overlap_units'][0]['roots'].append(p['overlap_units'][0]['roots'][0])
            with self.subTest(change=change),self.assertRaises(ValueError):current.validate_structural_overlap(g,p)

    def test_honest_v14_envelopes_and_direct_frozen_semantics(self):
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

    def test_v1_and_v14_policies_are_not_interchangeable(self):
        with self.assertRaises(ValueError):list(current.observe_recipe_contracts(*authored_fixture()))
        with self.assertRaises(ValueError):list(previous.observe_recipe_contracts(*fixture()))
        self.assertEqual(previous.QUALIFIED_POLICY,'cached-CODE-frontier-inventory-v1')
        self.assertEqual(previous.MAX_ROOTS,180)

    def test_unapproved_operation_is_rejected_without_any_input_open(self):
        with patch.object(Path,'open',side_effect=AssertionError('unexpected input read')) as opened:
            with self.assertRaises(ValueError):current.validate_operation({})
            opened.assert_not_called()

    def test_measured_forecast_is_not_an_operation_or_a_positive(self):
        self.assertEqual((current.MAX_ROOTS,current.MAX_RECIPES,current.MAX_RECORDS),(55,34,89))
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


if __name__ == '__main__':
    unittest.main()
