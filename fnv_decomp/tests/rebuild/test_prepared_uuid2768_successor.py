"""Fully authored metadata fixtures; no game, SDK, archive, or native reads."""
import copy
import hashlib
import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('prepared_uuid2768',Path(__file__).resolve().parents[2]/'tools/rebuild/prepared_uuid2768_successor.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


def fixture():
    records=[]
    for i in range(14534):
        identity=dict(recipe_id='fixture-'+str(i),object_sha256=hashlib.sha256(str(i).encode()).hexdigest(),symbol_index=i)
        records.append(dict(canonical=m.physical(identity),original_address='0x%08x'%(0x10000000+i),
                            category='ordinary' if i<14528 else 'application-candidate',namespace_identity=identity,origin_identity=identity))
    names,ordinary=m.census(records)
    parent=dict(schema_version=7,kind='prepared-CODE-collision-exclusions',policy_id='prepared-CODE56-successor-v1',
                ordinary_prepared_count=14528,collision_exclusion_count=14534,application_selected_code_count=None,
                application_selection_inferred_from_counts=False,historical_records_preserved=True,
                records=records,exclusion_names=names,ordinary_names=ordinary)
    originals=[dict(physical_section=131,coff_relocation=dict(offset=i*4,symbol_index=100+i,kind=20)) for i in range(9)]
    mapped=[dict(ordinal=i+1,original_field_sha256=m.digest(f),original_section=131,original_symbol_index=100+i,
                 original_offset=i*4,kind=20,serialized_section=2,serialized_symbol_index=10+i,
                 canonical_name='fixture'+str(i),role='code') for i,f in enumerate(originals)]
    maps=dict(section_map={'131':2},symbol_map=dict({'553':6},**{str(100+i):10+i for i in range(9)}))
    occurrences=[dict(ordinal=i,blocker_id=b,directive_ordinals=o) for i,b,o in
                 [(1,m.UUID,[1]),(2,m.UUID,[2]),(3,m.DIFF,[1,2,3,4])]]
    row=dict(root=copy.deepcopy(m.ROOT),canonical_export=m.physical({k:m.ROOT[k] for k in ('recipe_id','object_sha256','symbol_index')}),
             code_bytes=58,fields=9,serialized_section=2,serialized_symbol_index=6,original_negative_certificate_sha256=m.NEGATIVE,
             qualified_composition_sha256=m.COMPOSED,original_fields=originals,normalized_fields=mapped,namespace_maps=maps,
             namespace_maps_sha256=m.digest(maps),original_negative_occurrences=occurrences,
             qualified_assessment_sha256='a'*64,projection_sha256='b'*64,field_ledger_sha256='c'*64)
    raw=b'   '+b' '.join(x.encode() for x in m.TOKENS)+b' '
    directive=dict(extent=93,payload_hex=raw.hex(),payload_sha256=hashlib.sha256(raw).hexdigest(),ordered_tokens=copy.deepcopy(m.TOKENS))
    flags=dict(native_archive_conformance_verified=False,provider_selected=False,runtime_eligible=False,ABI_verified=False,
               namespace_approved=False,library_selected=False,library_loaded=False,executable_link_performed=False)
    handoff=dict(schema_version=1,kind='accepted-qualified-UUID-CODE-export-handoff',sealed=True,records=[row],
                 object=dict(sha256=m.OBJECT),archive=dict(sha256=m.ARCHIVE),field_proofs=dict(sha256=m.PROOFS,fields=9),
                 producer_receipt=dict(sha256='d'*64),directive=directive,
                 declaration=dict(canonical_sha256='26e13ca4ee534ef4dd7df52b5b31b388dfd49ba79a4099561ffe2bf9fa8c73d9'),
                 future_uuid_response_token=r'C:\Projects\Decompilation\FNV\tools\vc2008\VC\PlatformSDK\Lib\Uuid.Lib',**flags)
    peer=dict(status='accepted-qualified-metadata-handoff',handoff_sha256=m.HANDOFF,whole_payload_matches_independently_reviewed_draft=True,
              complete_fields=9,native_conformance_claim_created=False,namespace_adoption_authorized=False,provider_selected=False,runtime_eligible=False)
    directive_facts=dict(payload_bytes=93,tokens=copy.deepcopy(m.TOKENS),exact_directive_token_sequence_matches=True,
        original_negative_occurrences=3,original_negative_preserved=True,qualified_witness_is_separate=True,
        UUID_selected_or_loaded=False,duplicate_semantics_proved=False,ordinary_two_library_fallback_used=False)
    native=dict(kind='uuid2768-native-conformance-v1',status='pass',input_stability_verified=True,
        typed_producer_evidence=dict(base_closure_observed=False,original_negative_preserved=True,
            nested_sha256=dict(assessment='a'*64,projection='b'*64,field_ledger='c'*64)),
        components=[dict(input_sha256=m.ARCHIVE,native_metadata_matches=True,receipt_sha256='d'*64,
                         facts=dict(members=1,exports=1,LIB_membership_exact=True,complete_native_linker_index=True,
                                    qualified_directive_evidence=directive_facts))],
        UUID_selected_or_loaded=False,duplicate_semantics_proved=False,ordinary_two_library_policy_applied=False,
        provider_selected=False,runtime_eligible=False,ABI_verified=False,executable_linked=False,Game_execution=False)
    np=dict(kind='uuid2768-native-independent-review-v1',status='accepted',receipt_sha256=m.NATIVE,archive_sha256=m.ARCHIVE,
            object_sha256=m.OBJECT,UUID_selected_or_loaded=False,duplicate_semantics_proved=False,ordinary_two_library_policy_applied=False,
            provider_selected=False,runtime_eligible=False,ABI_verified=False,link_performed=False,game_execution=False)
    return parent,handoff,peer,native,np


class SuccessorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.inputs=fixture()
    def test_append_preserves_every_parent_record_and_unknown_app_state(self):
        result=m.build(*self.inputs);parent=self.inputs[0]
        self.assertEqual(result['records'][:-1],parent['records']);self.assertEqual(result['ordinary_prepared_count'],14529)
        self.assertEqual(result['collision_exclusion_count'],14535);self.assertNotIn('application_manifest_adopted',result)
        row=result['records'][-1];self.assertEqual(row['original_negative_certificate_sha256'],m.NEGATIVE)
        self.assertEqual(row['qualified_composition_sha256'],m.COMPOSED);self.assertIn('qualified-UUID',row['identity_mode'])
    def test_original_negative_duplicate_not_collapsed(self):
        inputs=list(copy.deepcopy(self.inputs));inputs[1]['records'][0]['original_negative_occurrences'].pop(1)
        with self.assertRaises(ValueError):m.build(*inputs)
    def test_no_provider_native_or_handoff_promotion(self):
        for index,key in [(1,'provider_selected'),(2,'namespace_adoption_authorized'),(3,'UUID_selected_or_loaded'),(4,'duplicate_semantics_proved')]:
            inputs=list(copy.deepcopy(self.inputs));inputs[index][key]=True
            with self.subTest(key=key),self.assertRaises(ValueError):m.build(*inputs)
    def test_mapping_field_or_dependency_drift_rejected(self):
        for mutation in ('mapping','field','token','raw'):
            inputs=list(copy.deepcopy(self.inputs));h=inputs[1]
            if mutation=='mapping':h['records'][0]['normalized_fields'][0]['serialized_symbol_index']=True
            if mutation=='field':h['records'][0]['original_fields'][0]['coff_relocation']['offset']=99
            if mutation=='token':h['future_uuid_response_token']='uuid.lib'
            if mutation=='raw':h['directive']['payload_hex']='00'*93
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):m.build(*inputs)
    def test_duplicate_root_or_parent_application_promotion_rejected(self):
        inputs=list(copy.deepcopy(self.inputs));inputs[0]['records'][0]['original_address']=m.ROOT['original_address']
        with self.assertRaises(ValueError):m.build(*inputs)
        inputs=list(copy.deepcopy(self.inputs));inputs[0]['application_manifest_adopted']=False
        with self.assertRaises(ValueError):m.build(*inputs)
    def test_fixed_from_bytes_rejects_unreviewed_inputs(self):
        with self.assertRaises(ValueError):m.from_bytes(*(b'{}' for _ in range(5)))


if __name__=='__main__':unittest.main()
