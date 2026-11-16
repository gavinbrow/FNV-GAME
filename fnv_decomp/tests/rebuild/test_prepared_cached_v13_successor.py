"""Authored 21-root metadata fixtures; no game or producer data is read."""
import copy
import hashlib
import importlib.util
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v13_successor',HERE.parents[1]/'tools/rebuild/prepared_cached_v13_successor.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
prior_spec=importlib.util.spec_from_file_location('uuid_fixture',HERE/'test_prepared_uuid2768_successor.py')
prior=importlib.util.module_from_spec(prior_spec);prior_spec.loader.exec_module(prior)


def fixture():
    parent=prior.m.build(*prior.fixture());rows=[];members=[];proofs=[]
    for i in range(21):
        count=3 if i<4 else 2;address='0x%08x'%(0x20000000+i)
        obj=hashlib.sha256(('object'+str(i)).encode()).hexdigest();source=hashlib.sha256(('source'+str(i)).encode()).hexdigest()
        root=dict(original_address=address,recipe_id='fixture-'+str(i),recipe_index=i,object_sha256=obj,source_sha256=source,
                  symbol='fixture_symbol_'+str(i),symbol_index=1000+i,section=1,value=0,size=48)
        ident={k:root[k] for k in ('recipe_id','object_sha256','symbol_index')};name=m.physical(ident)
        authority=dict(record_sha256=hashlib.sha256(('record'+str(i)).encode()).hexdigest());cert='c'*64;contract='d'*64
        fields=[dict(physical_section=1,coff_relocation=dict(offset=j*4,symbol_index=100+j,kind=20)) for j in range(count)]
        observed=[dict(section=1,offset=j*4,symbol_index=100+j,kind=20,field_proof_sha256=m.digest(field)) for j,field in enumerate(fields)]
        smap={str(100+j):10+j for j in range(count)};smap[str(root['symbol_index'])]=6
        maps=dict(section_map={'1':2},symbol_map=smap)
        compare=lambda symbol:dict(address=address,symbol=symbol,size=48,compiled_extent=48,verdict='match',errors=[],
                                   relocations=[{'match':True} for _ in fields])
        member_name='fixture-%02d.obj'%i;outsha=hashlib.sha256(('member'+str(i)).encode()).hexdigest()
        projection=dict(requested_roots=[root],exports=[name],output_sha256=outsha,original_object_sha256=obj,authority=authority,
                        certificate_sha256=cert,contract_identity_sha256=contract,fields=observed,maps=maps,
                        before_comparison=[compare(root['symbol'])],after_comparison=[compare(name)])
        proof=dict(schema_version=1,source_evidence_enriched=False,member=member_name,requested_root=root,authority=authority,
                   output_object_sha256=outsha,certificate_sha256=cert,contract_identity_sha256=contract,
                   fields_sha256=m.digest(fields),central_record_sha256=authority['record_sha256'],fields=fields)
        row=dict(root=root,member=member_name,canonical=name,member_sha256=outsha,original_object_sha256=obj,authority=authority,
                 certificate_sha256=cert,contract_identity_sha256=contract,fields=count,field_proof_ordinal=i+1,
                 field_proof_record_sha256=m.digest(proof),original_fields_sha256=m.digest(fields),serialized_section=2,serialized_symbol_index=6)
        rows.append(row);members.append(dict(name=member_name,projection=projection));proofs.append(proof)
    handoff=dict(schema_version=1,kind='accepted-prepared-CODE-export-handoff',cohort='V13-cache-qualified-native-positive-21',
        operation_status='completed',requires_successor_exclusion_epoch=True,requested_candidates=21,new_distinct_exports=21,
        quarantined_candidates=0,full_field_proof_records=21,full_field_proof_rows=46,upstream_ordinary_prepared_count=14529,
        upstream_collision_exclusion_count=14535,successor_ordinary_prepared_count=14550,successor_collision_exclusion_count=14556,
        upstream_prepared_epoch=dict(sha256=m.PARENT),members=dict(sha256=m.MEMBERS),field_proofs=dict(sha256=m.PROOFS),records=rows,
        application_cohort_adopted=False,application_manifest_adopted=False,provider_selected=False,runtime_eligible=False,
        ABI_verified=False,link_ready=False,native_tools_run=False,native_archive_conformance_verified=False)
    peer=dict(kind='independent-final21-metadata-handoff-review',status='accepted-conditional-metadata-handoff',handoff_sha256=m.HANDOFF,
              full21_root_canonical_serialized_map_and_proofordinal_join=True,exports=21,fields=46,successor_epoch_created=False,
              requires_successor_exclusion_epoch=True,provider_selected=False,runtime_eligible=False)
    return parent,handoff,peer,members,proofs


class SuccessorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.values=fixture()
    def test_complete_parent_prefix_and_uuid_qualification_preserved(self):
        result=m.build(*self.values);parent=self.values[0]
        self.assertEqual(result['records'][:14535],parent['records']);self.assertEqual(result['records'][14534],parent['records'][-1])
        self.assertEqual(result['ordinary_prepared_count'],14550);self.assertEqual(result['collision_exclusion_count'],14556)
        self.assertNotIn('application_manifest_adopted',result);self.assertIsNone(result['application_selected_code_count'])
        self.assertEqual(sum(x['original_field_count'] for x in result['records'][14535:]),46)
    def test_partial_duplicate_or_wrong_peer_rejected(self):
        for mutation in ('missing','duplicate','peer','bool'):
            values=list(copy.deepcopy(self.values))
            if mutation=='missing':values[4].pop()
            if mutation=='duplicate':values[3][1]['name']=values[3][0]['name']
            if mutation=='peer':values[2]['handoff_sha256']='0'*64
            if mutation=='bool':values[1]['new_distinct_exports']=True
            with self.subTest(mutation=mutation),self.assertRaises((ValueError,KeyError)):m.build(*values)
    def test_field_proof_mapping_and_match_drift_rejected(self):
        for mutation in ('proof','ordinal','map','bool-map','match'):
            values=list(copy.deepcopy(self.values))
            if mutation=='proof':values[4][0]['fields'][0]['coff_relocation']['offset']+=1
            if mutation=='ordinal':values[1]['records'][0]['field_proof_ordinal']=2
            if mutation=='map':values[3][0]['projection']['maps']['section_map']['1']=3
            if mutation=='bool-map':values[3][0]['projection']['maps']['symbol_map']['100']=True
            if mutation=='match':values[3][0]['projection']['after_comparison'][0]['relocations'][0]['match']=False
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):m.build(*values)
    def test_existing_uuid_and_unknown_adoption_preserved(self):
        values=list(copy.deepcopy(self.values));values[0]['records'][-1]['qualified_composition_sha256']='0'*64
        with self.assertRaises(ValueError):m.build(*values)
        values=list(copy.deepcopy(self.values));values[0]['application_manifest_adopted']=False
        with self.assertRaises(ValueError):m.build(*values)
    def test_unpinned_raw_inputs_rejected(self):
        with self.assertRaises(ValueError):m.from_bytes(*(b'{}' for _ in range(5)))


if __name__=='__main__':unittest.main()
