"""New-policy authored authority tests; copied pins are not real artifacts."""
import copy,io
from pathlib import Path
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_frontier_code_factory_v13 as subject
from test_cached_frontier_code_factory_v13 import fixture,select,reseal


def reseal_record(args,index):
    row=args[1][index]
    if 'certificate' in row:row['certificate_sha256']=subject.digest(row['certificate'])
    reseal(args[0],args[1])


class IndependentV13FactoryAuthorityTests(unittest.TestCase):
    def test_all_positive_singletons_selected_and_original_metadata_unmodified(self):
        args=fixture(field=False);before=copy.deepcopy(args);request,selected,ledger=select(args)
        self.assertEqual(args,before);self.assertEqual(len(selected),2);self.assertEqual(request['roots'],args[2]['roots'])
        self.assertEqual([r['state'] for r in ledger],['ALL_POSITIVE_SINGLETON_REQUESTED']*2+['RECIPE_UNION_EVIDENCE_ONLY'])

    def test_old_native_or_qualification_policy_cannot_be_resealed_into_new_admission(self):
        for mode in ('native','qualification'):
            args=fixture(field=False);row=args[1][0]
            if mode=='native':row['policy_id']=subject.previous.native.POLICY
            else:
                row['qualified_metadata_identity']['policy_id']=subject.previous.native.QUALIFIED_POLICY
                q=dict(row['qualified_metadata_identity'],requested_roots=row['requested_roots'],contract=row['contract'],
                    contract_sha256=row['contract_identity_sha256'],new_metadata_contract_sha256=row['contract_identity_sha256'])
                for key in subject.native.QUALIFIED_FALSE:q.setdefault(key,False)
                row['qualified_metadata_row_sha256']=subject.digest(q)
            reseal_record(args,0)
            with self.subTest(mode=mode),self.assertRaises(ValueError):select(args)

    def test_borrowed_source_operation_request_or_certificate_provenance_rejected(self):
        for mode in ('source','operation','qualified-request','certificate-provenance','record-row'):
            args=fixture(field=False);row=args[1][0]
            if mode=='source':row['observation_provenance']['collector_sha256']='e'*64
            elif mode=='operation':row['observation_provenance']['operation_sha256']='e'*64
            elif mode=='qualified-request':row['observation_provenance']['qualified_request_sha256']='e'*64
            elif mode=='certificate-provenance':row['certificate']['provenance']=dict(row['certificate']['provenance'],source_sha256='e'*64)
            else:row['qualified_metadata_row_sha256']='e'*64
            reseal_record(args,0)
            with self.subTest(mode=mode),self.assertRaises(ValueError):select(args)

    def test_original_safeseh_negative_and_union_stay_evidence_without_typed_promotion(self):
        args=fixture(field=False,safeseh=True);request,selected,ledger=select(args)
        self.assertEqual(len(selected),1);self.assertEqual(ledger[1]['state'],'ORIGINAL_NEGATIVE_PRESERVED')
        self.assertEqual(ledger[2]['state'],'RECIPE_UNION_EVIDENCE_ONLY')
        self.assertIn('LIVE_SAFESEH_HANDLER_REQUIRES_ADAPTER',ledger[1]['blocker_codes'])
        args[1][1]['certificate']['policy_id']='typed-composed-special-policy';reseal_record(args,1)
        with self.assertRaises(ValueError):select(args)

    def test_selected_native_and_qualified_ordinals_cannot_borrow_union_or_boolean_alias(self):
        for key,value in (('ordinal',3),('ordinal',True),('qualified_record_ordinal',True),('certificate_sha256','e'*64),('qualified_metadata_row_sha256','e'*64)):
            args=fixture(field=False);_,selected,_=select(args);selection=copy.deepcopy(selected[0]);selection['authority'][key]=value
            stream=io.BytesIO()
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):subject.write_context(stream,args[1][0],selection)
            self.assertEqual(stream.getvalue(),b'')

    def test_current_duplicate_prepared_and_quarantined_names_refused(self):
        args=fixture(field=False);args[3]['groups'].append(copy.deepcopy(args[3]['groups'][0]))
        with self.assertRaises(ValueError):select(args)
        args=fixture(field=False);args[4].update(collision_exclusion_count=1,exclusion_names=[args[3]['groups'][0]['symbol']])
        with self.assertRaises(ValueError):subject.select_candidates(*args,expected_census=(2,1,3),expected_current_codes=2,expected_prepared=(0,1))
        args=fixture(field=False)
        with patch.object(subject,'QUARANTINES',{args[2]['roots'][0]['original_address']}):
            with self.assertRaises(ValueError):select(args)

    def test_latest_uuid_schema_missing_application_state_is_preserved_not_fabricated(self):
        args=fixture(field=False);epoch=args[4];epoch.pop('application_manifest_adopted')
        epoch.update(schema_version=8,policy_id='prepared-UUID2768-successor-v1',application_selected_code_count=None,**subject.metadata.FALSE)
        before=copy.deepcopy(epoch);_,selected,_=select(args);self.assertEqual(len(selected),2);self.assertEqual(epoch,before)
        for value in (True,None,0):
            epoch['application_manifest_adopted']=value
            with self.subTest(value=value),self.assertRaises(ValueError):select(args)

    def test_partial_or_duplicate_records_and_invented_metadata_certificate_cannot_select(self):
        for mode in ('partial','duplicate','certificate'):
            args=fixture(field=False)
            if mode=='partial':args[1].pop()
            elif mode=='duplicate':args[1][1]=copy.deepcopy(args[1][0]);args[1][1]['qualified_record_ordinal']=2;reseal_record(args,1)
            else:args[1][0]['qualified_metadata_identity']['certificate_created']=True;reseal_record(args,0)
            with self.subTest(mode=mode),self.assertRaises(ValueError):select(args)

    def test_operation_cannot_borrow_image_role_or_truncate_physical_identity(self):
        roots=fixture(field=False)[2]['roots']
        artifacts={name:dict(path='build/rebuild/authored-'+name+'.json',sha256=h) for name,h in subject.KNOWN.items()}
        artifacts['image_check']['path']=subject.IMAGE_CHECK_PATH
        op=dict(schema_version=1,kind='cached-native-positive-CODE-production-operation',epoch='authored-V13',
            roots=roots,artifacts=artifacts,output_relative=subject.OUTPUT,resource_limits=copy.deepcopy(subject.LIMITS))
        subject.validate_operation(op)  # Schema-only: no artifact is read.
        for mode in ('image-path','image-hash','bool-root','duplicate-root','foreign-output','extra-role'):
            bad=copy.deepcopy(op)
            if mode=='image-path':bad['artifacts']['image_check']['path']='build/rebuild/authored-doctor-all.json'
            elif mode=='image-hash':bad['artifacts']['image_check']['sha256']='e'*64
            elif mode=='bool-root':bad['roots'][0]['symbol_index']=True
            elif mode=='duplicate-root':bad['roots'].append(copy.deepcopy(bad['roots'][0]))
            elif mode=='foreign-output':bad['output_relative']='build/rebuild/cached-frontier-code-v12-v1'
            else:bad['artifacts']['typed-witness']=dict(path='build/rebuild/authored.json',sha256='e'*64)
            with self.subTest(mode=mode),self.assertRaises(ValueError):subject.validate_operation(bad)

    def test_review_cannot_borrow_owner_old_policy_operation_or_permissions(self):
        args=SimpleNamespace(review='build/rebuild/authored-review.json',review_sha256='a'*64,operation_sha256='b'*64)
        review=dict(schema_version=1,kind='cached-frontier-CODE-factory-v13-review-v1',reviewer='/root/independent-authored',
            approved=True,root_authorized=True,independent_source_schema_review_pass=True,artifact_input_review_pass=True,
            operation_sha256=args.operation_sha256,source_sha256={p:'c'*64 for p in subject.OWNED},producer_sha256=copy.deepcopy(subject.PINS),
            allow_original_objects_read=True,allow_source_hashing=True,allow_reference_image_read=True,allow_code_emission=True,
            allow_native_tools=False,allow_executable_link=False,allow_game_execution=False)
        for mode in ('owner','old-policy','operation','source-set','producer','native','bool-schema','unknown-permission'):
            bad=copy.deepcopy(review)
            if mode=='owner':bad['reviewer']='/root/code_lane_02'
            elif mode=='old-policy':bad['kind']='cached-frontier-CODE-factory-v12-review-v1'
            elif mode=='operation':bad['operation_sha256']='d'*64
            elif mode=='source-set':bad['source_sha256'].pop(subject.OWNED[0])
            elif mode=='producer':bad['producer_sha256'][next(iter(subject.PINS))]='d'*64
            elif mode=='native':bad['allow_native_tools']=True
            elif mode=='bool-schema':bad['schema_version']=True
            else:bad['allow_typed_promotion']=True
            with self.subTest(mode=mode),patch.object(subject,'load_ref',return_value=bad),patch.object(subject.base,'observe') as observe:
                with self.assertRaises(ValueError):subject.review_gate(args,{})
                observe.assert_not_called()


if __name__=='__main__':unittest.main()
