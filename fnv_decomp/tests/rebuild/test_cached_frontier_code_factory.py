"""Owner authored cached-native fixtures; no saved Game inputs or native tools."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_frontier_code_factory as subject
from test_ordinary_relocation_projection_independent import authored


def fixture(*,fields=False):
    """One genuine frozen4bf root plus a singleton-sized recipe union."""
    raw,contract,_,roots,providers=authored() if fields else authored(classes=())
    root=roots[0];contract=copy.deepcopy(contract);contract['provenance']['request_sha256']='a'*64
    contract['iat_import_observation']=dict(import_id=175,dll='USER32.dll',function='GetActiveWindow',original_cell='0x00fdf2fc')
    certificate=subject.base.ordinary.assess_object(subject.base.coff.parse(raw),contract)
    identity=dict(schema_version=1,kind='new-cached-metadata-contract',policy_id=subject.native.QUALIFIED_POLICY,
        certificate_created=False,native_observation_required=True,historical_certificate_contract_identity_equal_claimed=False,
        source_frame_verification=dict(recipe_index=0,raw_sha256='b'*64,compressed_sha256='c'*64,row_count=len(contract['fields']),
            first_ordinal=1 if fields else None,last_ordinal=1 if fields else None,whole_data_hash_verified_this_read=False,unrequested_frames_verified=False))
    inputs={'qualified_request':dict(path='build/rebuild/authored-request.json',sha256='a'*64)}
    provenance=dict(qualified_request_sha256='a'*64,operation_sha256='d'*64,collector_sha256='e'*64,
        saved_authorities={k:v['sha256'] for k,v in inputs.items()},optional_function_index_present=False,qualified_contract_provenance_restamped=False)
    records=[]
    for ordinal,(event,qevent) in enumerate([('SINGLE_ROOT_OBSERVATION','SINGLE_ROOT_METADATA_CONTRACT'),
            ('RECIPE_ROOT_UNION_OBSERVATION','RECIPE_UNION_METADATA_CONTRACT')],1):
        qidentity=dict(identity,event=qevent)
        q=dict(qidentity,requested_roots=copy.deepcopy(roots),contract=copy.deepcopy(contract),contract_sha256=subject.digest(contract),
            new_metadata_contract_sha256=subject.digest(contract))
        for key in subject.native.QUALIFIED_FALSE:q.setdefault(key,False)
        records.append(dict(schema_version=1,kind='fresh-root-observation-from-qualified-contract',policy_id=subject.native.POLICY,event=event,
            recipe_id=root['recipe_id'],recipe_index=0,requested_roots=copy.deepcopy(roots),contract=copy.deepcopy(contract),
            contract_identity_sha256=subject.digest(contract),qualified_metadata_row_sha256=subject.digest(q),qualified_metadata_identity=qidentity,
            observation_provenance=copy.deepcopy(provenance),native_object_sha256=root['object_sha256'],native_parse_performed=True,
            qualified_contract_unchanged=True,fresh_certificate_created=True,certificate=copy.deepcopy(certificate),certificate_sha256=subject.digest(certificate),
            qualified_record_ordinal=ordinal,closure_observed=certificate['closure_observed'],graph_observation_complete=certificate['graph_observation_complete'],
            root_closure_candidate=certificate['root_closure_candidate'],blockers=copy.deepcopy(certificate['blockers']),**subject.native.FALSE))
    summaries=[subject.native.summary_row(r,i) for i,r in enumerate(records,1)]
    receipt=dict(policy_id=subject.native.POLICY,status='metadata-only',input_stability=True,optional_function_index_present=False,
        qualified_contracts_preserved=True,historical_roots_reobserved=0,original_binding_stream_traversals=0,owner_stream_traversals=0,cache_frame_reads=0,
        native_object_observation_reads=1,native_object_parse_attempts=1,operation_sha256='d'*64,source_sha256='e'*64,inputs=inputs,
        summary=dict(roots=1,recipes=1,records=2,singleton_closure=1,singleton_blocked=0,union_closure=1,union_blocked=0),observations=summaries,**subject.native.FALSE)
    name=subject.base.pool.canonical({k:root[k] for k in ('recipe_id','object_sha256','symbol_index')})
    groups=dict(kind='actual-unresolved-LNK-target-groups',executable_execution=False,runtime_eligible=False,classifications=dict(CODE=1),
        groups=[dict(symbol=name,classification='CODE',observed_roles=['code'],included_provenance_is_extraction_proof=False,original_bases=[root['original_address']])])
    prepared=dict(kind='prepared-CODE-collision-exclusions',ordinary_prepared_count=0,collision_exclusion_count=0,exclusion_names=[],
        application_selection_inferred_from_counts=False,provider_selected=False,runtime_eligible=False,application_manifest_adopted=False)
    request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=copy.deepcopy(roots))
    return dict(raw=raw,records=records,receipt=receipt,request=request,groups=groups,prepared=prepared,providers=providers)


def select(values):
    return subject.select_candidates(values['receipt'],values['records'],values['request'],values['groups'],values['prepared'],
        expected_census=(1,1,2),expected_current_codes=1,expected_prepared=(0,0))


class OwnerSelectorTests(unittest.TestCase):
    def test_fresh_process_cli_help_does_not_load_operation_or_originals(self):
        result=subprocess.run([sys.executable,str(ROOT/'tools/rebuild/cached_frontier_code_factory.py'),'--help'],
            cwd=ROOT,capture_output=True,text=True,timeout=30)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('--reference',result.stdout);self.assertIn('--operation-sha256',result.stdout)

    def test_singleton_sized_positive_union_remains_evidence_only(self):
        values=fixture();before=copy.deepcopy(values);request,selected,ledger=select(values)
        self.assertEqual(len(request['roots']),1);self.assertEqual(len(selected),1);self.assertEqual(len(ledger),2)
        self.assertEqual([r['state'] for r in ledger],['ALL_POSITIVE_SINGLETON_REQUESTED','RECIPE_UNION_EVIDENCE_ONLY'])
        self.assertEqual(values,before)

    def test_original_full_field_rows_and_unit_import_context_do_not_imply_root_iat_use(self):
        for fields in (False,True):
            values=fixture(fields=fields);values['records'][0]['contract']['iat_import_observation']={'import_id':175}
            # Unrestamped original contracts cannot be changed, even to add a
            # legitimate unit context; the sealed receipt record must reject it.
            with self.assertRaises(ValueError):select(values)

    def test_full_proof_records_copy_only_actual_root_fields_including_empty_roots(self):
        for fields in (False,True):
            with self.subTest(fields=fields):
                values=fixture(fields=fields);request,selected,_=select(values);row=values['records'][0];root=request['roots'][0]
                if fields:
                    output,projection=subject.frozen.fields.core.project_member(values['raw'],row['contract'],row['certificate'],[root],values['providers'],existing_exports=set())
                else:
                    output,projection=subject.base.project_member(values['raw'],row['contract'],row['certificate'],[root]);projection['fields']=[]
                projection.update(authority=selected[0]['authority'],central_record_sha256=subject.digest(row))
                record=subject.field_proof_record('authored.obj',row,selected[0],projection,output)
                self.assertEqual(row['contract']['iat_import_observation']['import_id'],175)
                self.assertEqual(record['fields'],row['contract']['fields']);self.assertEqual(len(record['fields']),int(fields))
                self.assertFalse(record['source_evidence_enriched'])
                self.assertTrue(all('import_id' not in field for field in record['fields']))


if __name__=='__main__':unittest.main()
