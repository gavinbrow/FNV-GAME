"""Independent factory tests over authored COFF only; no saved Game inputs."""
import copy
from pathlib import Path
import sys
import io
import gzip
import hashlib
import json
import struct
import tempfile
import time
from types import SimpleNamespace
from contextlib import ExitStack
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_frontier_code_factory as factory
from test_cached_root_observe import fixture as authored


def fixture(field=True,safeseh=False):
    args=list(authored(field=field,safeseh=safeseh))
    authorities={'qualified_request':dict(sha256='a'*64)}
    args[-1]=dict(qualified_request_sha256='a'*64,operation_sha256='b'*64,collector_sha256='c'*64,
        saved_authorities={'qualified_request':'a'*64},optional_function_index_present=False,
        qualified_contract_provenance_restamped=False)
    records=list(factory.native.observe_recipe_contracts(*args))
    for i,r in enumerate(records,1):r['qualified_record_ordinal']=i
    receipt=dict(policy_id=factory.native.POLICY,status='metadata-only',input_stability=True,
        optional_function_index_present=False,qualified_contracts_preserved=True,historical_roots_reobserved=0,
        original_binding_stream_traversals=0,owner_stream_traversals=0,cache_frame_reads=0,
        native_object_observation_reads=1,native_object_parse_attempts=1,inputs=authorities,
        operation_sha256='b'*64,source_sha256='c'*64,**factory.native.FALSE)
    request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=copy.deepcopy(args[3]))
    groups=[]
    for root in args[3]:
        name=factory.base.pool.canonical({k:root[k] for k in ('recipe_id','object_sha256','symbol_index')})
        groups.append(dict(classification='CODE',symbol=name,observed_roles=['code'],
            included_provenance_is_extraction_proof=False,original_bases=[root['original_address']]))
    current=dict(kind='actual-unresolved-LNK-target-groups',executable_execution=False,runtime_eligible=False,
        classifications={'CODE':2},groups=groups)
    prepared=dict(kind='prepared-CODE-collision-exclusions',ordinary_prepared_count=0,collision_exclusion_count=0,
        exclusion_names=[],application_selection_inferred_from_counts=False,provider_selected=False,
        runtime_eligible=False,application_manifest_adopted=False)
    reseal(receipt,records)
    return receipt,records,request,current,prepared


def reseal(receipt,records):
    receipt['observations']=[factory.native.summary_row(r,i) for i,r in enumerate(records,1)]
    receipt['summary']=dict(roots=2,recipes=1,records=3,
        singleton_closure=sum(r['closure_observed'] for r in records if r['event']=='SINGLE_ROOT_OBSERVATION'),
        singleton_blocked=sum(not r['closure_observed'] for r in records if r['event']=='SINGLE_ROOT_OBSERVATION'),
        union_closure=sum(r['closure_observed'] for r in records if r['event']=='RECIPE_ROOT_UNION_OBSERVATION'),
        union_blocked=sum(not r['closure_observed'] for r in records if r['event']=='RECIPE_ROOT_UNION_OBSERVATION'))


def select(args):
    return factory.select_candidates(*args,expected_census=(2,1,3),expected_current_codes=2,expected_prepared=(0,0))


def whole_saved_fixture(directory):
    from test_cached_root_observe_operational_independent import whole_authored_fixture
    items,request,request_sha=whole_authored_fixture();records=[]
    authority=dict(qualified_request=dict(sha256=request_sha))
    provenance=dict(qualified_request_sha256=request_sha,operation_sha256='b'*64,collector_sha256='c'*64,
        saved_authorities={'qualified_request':request_sha},optional_function_index_present=False,
        qualified_contract_provenance_restamped=False)
    for item in items:
        for view in item['views']:
            view['contract']['provenance']['recipe_unit_sha256']=item['proof']['recipe_unit_sha256']
            view['contract']['provenance']['recipe_index']=item['unit']['recipe_index']
            view['contract']['provenance']['recipe_id']=item['unit']['recipe_id']
            view['contract_sha256']=view['new_metadata_contract_sha256']=factory.digest(view['contract'])
        for r in factory.native.observe_recipe_contracts(item['raw'],item['unit'],item['proof'],item['roots'],item['views'],provenance):
            r['qualified_record_ordinal']=len(records)+1;records.append(r)
    receipt=dict(policy_id=factory.native.POLICY,status='metadata-only',input_stability=True,
        optional_function_index_present=False,qualified_contracts_preserved=True,historical_roots_reobserved=0,
        original_binding_stream_traversals=0,owner_stream_traversals=0,cache_frame_reads=0,
        native_object_observation_reads=77,native_object_parse_attempts=77,inputs=authority,
        operation_sha256='b'*64,source_sha256='c'*64,**factory.native.FALSE)
    reseal(receipt,records);receipt['summary'].update(roots=180,recipes=77,records=257)
    rows=[]
    for root in request['roots']:
        rows.append(dict(classification='CODE',symbol=factory.base.pool.canonical({k:root[k] for k in ('recipe_id','object_sha256','symbol_index')}),
            observed_roles=['code'],included_provenance_is_extraction_proof=False,original_bases=[root['original_address']]))
    rows.extend(dict(classification='CODE',symbol='_authored_unrequested_%d'%i,original_bases=[]) for i in range(577-len(rows)))
    groups=dict(kind='actual-unresolved-LNK-target-groups',executable_execution=False,runtime_eligible=False,classifications={'CODE':577},groups=rows)
    prepared=dict(kind='prepared-CODE-collision-exclusions',ordinary_prepared_count=14472,collision_exclusion_count=14478,
        exclusion_names=['_fnv_code_%064x'%i for i in range(14478)],application_selection_inferred_from_counts=False,
        provider_selected=False,runtime_eligible=False,application_manifest_adopted=False)
    selected_request,_,_=factory.select_candidates(receipt,iter(records),request,groups,prepared)
    raw=b''.join(factory.native.canonical(r)+b'\n' for r in records);packed=gzip.compress(raw,mtime=0)
    path=Path(directory)/'authored-native.jsonl.gz';path.write_bytes(packed)
    receipt.update(details_sha256=hashlib.sha256(packed).hexdigest(),details_bytes=len(packed))
    return dict(receipt=receipt,qualification_request=request,current_groups=groups,prepared=prepared,
        expected_request=selected_request,native_details=path),items


class IndependentSelectorTests(unittest.TestCase):
    def test_authored_fields_all_positive_singletons_selected_union_evidence_only(self):
        args=fixture();before=copy.deepcopy(args);request,selected,ledger=select(args)
        self.assertEqual(args,before);self.assertEqual(len(selected),2);self.assertEqual(len(ledger),3)
        self.assertEqual(request['roots'],sorted(args[2]['roots'],key=lambda r:r['original_address']))
        self.assertEqual(ledger[-1]['state'],'RECIPE_UNION_EVIDENCE_ONLY')
        self.assertEqual([s['authority']['ordinal'] for s in selected],[1,2])
        self.assertEqual(len(args[1][0]['contract']['fields']),1)

    def test_safeseh_negative_singleton_and_union_never_become_providers(self):
        args=fixture(field=False,safeseh=True);request,selected,ledger=select(args)
        self.assertEqual(len(selected),1);self.assertEqual(ledger[1]['state'],'ORIGINAL_NEGATIVE_PRESERVED')
        self.assertFalse(ledger[-1]['closure_observed']);self.assertEqual(len(request['roots']),1)

    def test_all_records_consumed_and_truncated_extra_reordered_streams_rejected(self):
        for change in ('missing','extra','unionfirst','duplicate'):
            args=list(fixture());records=args[1]
            if change=='missing':records.pop()
            elif change=='extra':records.append(copy.deepcopy(records[0]))
            elif change=='unionfirst':records[:]=[records[-1],*records[:-1]]
            else:records[1]=copy.deepcopy(records[0])
            with self.subTest(change=change),self.assertRaises(ValueError):select(args)

    def test_full_receipt_commitment_detects_opaque_unknown_payload_drift(self):
        args=list(fixture());args[1][0]['contract']['provenance']['future']={'x':[False,0,True,1]}
        with self.assertRaises(ValueError):select(args)

    def test_prepared_and_quarantined_positive_requests_rejected(self):
        args=list(fixture());name=args[3]['groups'][0]['symbol'];args[4].update(ordinary_prepared_count=1,
            collision_exclusion_count=1,exclusion_names=[name])
        with self.assertRaises(ValueError):factory.select_candidates(*args,expected_census=(2,1,3),expected_current_codes=2,expected_prepared=(1,1))
        args=list(fixture());from unittest.mock import patch
        with patch.object(factory,'QUARANTINES',{args[2]['roots'][0]['original_address']}),self.assertRaises(ValueError):select(args)

    def test_receipt_count_and_summary_boolean_aliases_rejected(self):
        for key in ('roots','recipes','records','singleton_closure','union_closure'):
            args=list(fixture());args[0]['summary'][key]=True
            with self.subTest(key=key),self.assertRaises(ValueError):select(args)

    def test_collision_epoch_legacy_absence_is_preserved_but_explicit_adoption_refused(self):
        args=list(fixture());del args[4]['application_manifest_adopted']
        args[4].update(schema_version=6,policy_id=factory.metadata.POLICY,application_selected_code_count=None,**factory.metadata.FALSE)
        request,selected,_=select(args)
        self.assertEqual(len(selected),2);self.assertEqual(request['roots'],args[2]['roots'])
        self.assertNotIn('application_manifest_adopted',args[4])
        for value in (True,None,0):
            args=list(fixture());args[4]['application_manifest_adopted']=value
            with self.subTest(value=value),self.assertRaises(ValueError):select(args)
        for key,value in (('schema_version',True),('schema_version',7),('policy_id','unknown-producer'),
                          ('application_selected_code_count',0),('reference_image_read',True)):
            bad=copy.deepcopy(args[4]);bad.pop('application_manifest_adopted',None)
            bad.update(schema_version=6,policy_id=factory.metadata.POLICY,application_selected_code_count=None,**factory.metadata.FALSE)
            bad[key]=value;changed=list(fixture());changed[4]=bad
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):select(changed)


class IndependentPhysicalTests(unittest.TestCase):
    def material(self,directory,fields=False):
        from test_cached_frontier_code_factory import fixture as owner_fixture,select as owner_select
        values=owner_fixture(fields=fields);_,selected,_=owner_select(values);record=values['records'][0]
        root=selected[0]['root'];payload=bytearray(factory.base.coff.parse(values['raw'])['sections'][root['section']]['payload'])
        for row in record['contract']['fields']:
            struct.pack_into('<I',payload,row['physical_offset'],row['original_operand'])
        payload=bytes(payload)
        pe=SimpleNamespace(data=payload,read=lambda address,size:payload[address-int(root['original_address'],16):address-int(root['original_address'],16)+size])
        original=Path(directory)/'authored-original.obj';stage=Path(directory)/'authored-stage.obj';original.write_bytes(values['raw'])
        recipe=dict(symbols={f['coff_relocation']['symbol']:f['derived_source_symbol_base_va'] for f in record['contract']['fields']})
        return values['raw'],record,selected[0],values['providers'],set(),original,stage,pe,recipe

    def test_real_zero_and_field_projection_plain_comparison_and_independent_reparse(self):
        for fields in (False,True):
            with self.subTest(fields=fields),tempfile.TemporaryDirectory() as td:
                args=self.material(td,fields);out,projection,assessment=factory.verify_member(*args)
                self.assertTrue(assessment['eligible']);self.assertEqual(args[6].read_bytes(),out)
                self.assertEqual(projection['before_comparison'][0]['verdict'],'match')
                self.assertEqual(projection['after_comparison'][0]['verdict'],'match')
                self.assertEqual(projection['native_observation_record_sha256'],factory.digest(args[1]))
                proof=factory.field_proof_record('authored.obj',args[1],args[2],projection,out)
                self.assertEqual(factory.digest(proof['fields']),factory.digest(args[1]['contract']['fields']))
                self.assertFalse(proof['source_evidence_enriched'])

    def test_original_plain_mismatch_aborts_before_serialization(self):
        with tempfile.TemporaryDirectory() as td:
            args=self.material(td);args[7].read=lambda a,n:b'\xff'*n
            with patch.object(factory.base,'project_member',wraps=factory.base.project_member) as writer:
                with self.assertRaises(ValueError):factory.verify_member(*args)
                writer.assert_not_called()
            self.assertFalse(args[6].exists())

    def test_selected_native_frame_preserves_row_and_uses_exact_frozen_reader(self):
        with tempfile.TemporaryDirectory() as td:
            args=self.material(td,True);before=copy.deepcopy(args[1]);stream=io.BytesIO()
            index=factory.write_context(stream,args[1],args[2]);stream.seek(0)
            self.assertEqual(factory.frozen.read_context(stream,index,args[2]),before)
            self.assertEqual(args[1],before);self.assertNotIn('provenance',args[1])
            packed=bytearray(stream.getvalue());packed[-1]^=1
            with self.assertRaises(ValueError):factory.frozen.read_context(io.BytesIO(packed),index,args[2])

    def test_stale_selection_authority_never_writes_or_serializes(self):
        for key in ('record_sha256','certificate_sha256','contract_identity_sha256','qualified_metadata_row_sha256'):
            with self.subTest(key=key),tempfile.TemporaryDirectory() as td:
                args=list(self.material(td));args[2]=copy.deepcopy(args[2]);args[2]['authority'][key]='f'*64
                with patch.object(factory.frozen,'verify_candidate',wraps=factory.frozen.verify_candidate) as replay:
                    with self.assertRaises(ValueError):factory.verify_member(*args)
                    replay.assert_not_called()
                with self.assertRaises(ValueError):factory.write_context(io.BytesIO(),args[1],args[2])

    def test_field_proof_rejects_output_and_source_hash_substitution(self):
        with tempfile.TemporaryDirectory() as td:
            args=self.material(td,True);output,projection,_=factory.verify_member(*args)
            for key in ('output_sha256','original_object_sha256','certificate_sha256','contract_identity_sha256','central_record_sha256'):
                bad=copy.deepcopy(projection);bad[key]='f'*64
                with self.subTest(key=key),self.assertRaises(ValueError):factory.field_proof_record('authored.obj',args[1],args[2],bad,output)
            with self.assertRaises(ValueError):factory.field_proof_record('authored.obj',args[1],args[2],projection,output+b'changed')

    def test_expected_field_policy_boundary_quarantines_without_writer(self):
        with tempfile.TemporaryDirectory() as td:
            args=self.material(td,True);blocked=dict(eligible=False,blockers=[dict(code='AUTHORED_POLICY_BOUNDARY')])
            with patch.object(factory.frozen.fields.core,'assess_member',return_value=blocked), \
                 patch.object(factory.frozen,'verify_candidate',wraps=factory.frozen.verify_candidate) as writer:
                self.assertEqual(factory.verify_member(*args),(None,None,blocked));writer.assert_not_called()
            self.assertFalse(args[6].exists())

    def test_integrity_failure_is_fatal_and_cannot_be_policy_quarantine(self):
        with tempfile.TemporaryDirectory() as td:
            args=self.material(td,True)
            with patch.object(factory.frozen.fields.core,'assess_member',side_effect=ValueError('authored corrupted physical evidence')):
                with self.assertRaisesRegex(ValueError,'corrupted physical'):factory.verify_member(*args)
            self.assertFalse(args[6].exists())

    def test_after_comparison_and_independent_reparse_errors_remain_fatal(self):
        for mode in ('after','reparse'):
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as td:
                args=self.material(td,True);real=factory.base.bulk.compare_functions;calls=[]
                def compare(*a,**kw):
                    calls.append(1)
                    if len(calls)==2:raise ValueError('authored projected mismatch')
                    return real(*a,**kw)
                target=patch.object(factory.base.bulk,'compare_functions',side_effect=compare) if mode=='after' else \
                    patch.object(factory.base.bulk,'strict_reparse',side_effect=ValueError('authored independent reparse mismatch'))
                with target,self.assertRaises(ValueError):factory.verify_member(*args)


class IndependentSelectorStrictnessTests(unittest.TestCase):
    def test_exact_retained_imagecheck_authority_cannot_be_replaced_by_doctor(self):
        image='c03da09d39b8fd22283792c3dc1fbb6ac1e526d8afadd832fabc4071f1720cb1'
        doctor='9b24d10209fe0361a5e6b16b11a072e8e0ebc6505cd4b5e1bd782fe23854f29f'
        self.assertEqual(factory.KNOWN['image_check'],image)
        refs={k:dict(path='build/rebuild/authored-'+k+'.json',sha256=h) for k,h in factory.KNOWN.items()}
        refs['recipes']['path']='build/units.json';refs['image_check']['path']='build/image_check.json'
        op=dict(schema_version=1,kind='cached-native-positive-CODE-production-operation',epoch='authored-role-check',
            roots=fixture()[2]['roots'],artifacts=refs,output_relative=factory.OUTPUT,resource_limits=factory.LIMITS)
        factory.validate_operation(op)
        for change in ('hash','path'):
            altered=copy.deepcopy(op)
            if change=='hash':altered['artifacts']['image_check']['sha256']=doctor
            else:altered['artifacts']['image_check']['path']='build/rebuild/doctor-all.json'
            with self.subTest(change=change),self.assertRaises(ValueError):factory.validate_operation(altered)

    def test_request_physical_boolean_and_duplicate_current_namespace_rejected(self):
        args=list(fixture());args[2]['roots'][0]['value']=False
        with self.assertRaises(ValueError):select(args)
        args=list(fixture());args[3]['groups'][1]['symbol']=args[3]['groups'][0]['symbol']
        with self.assertRaises(ValueError):select(args)

    def test_certificate_digest_and_qualified_ordinal_cannot_be_borrowed(self):
        for key in ('certificate','ordinal'):
            args=list(fixture());record=args[1][0]
            if key=='certificate':record['certificate']['provenance']['changed']=True
            else:record['qualified_record_ordinal']=2
            reseal(args[0],args[1])
            with self.subTest(key=key),self.assertRaises(ValueError):select(args)

    def test_positive_requires_original_root_candidate_true(self):
        args=list(fixture());r=args[1][0];r['root_closure_candidate']=r['certificate']['root_closure_candidate']=False
        r['certificate_sha256']=factory.digest(r['certificate']);reseal(args[0],args[1])
        with self.assertRaises(ValueError):select(args)

    def test_certificate_provenance_and_export_policy_must_match_contract(self):
        for key in ('provenance','export_policy'):
            args=list(fixture());r=args[1][0]
            if key=='provenance':r['certificate']['provenance']=dict(r['certificate']['provenance'],object_sha256='f'*64)
            else:r['certificate']['export_policy']='unknown-future-policy'
            r['certificate_sha256']=factory.digest(r['certificate']);reseal(args[0],args[1])
            with self.subTest(key=key),self.assertRaises(ValueError):select(args)

    def test_all_certificate_no_admission_flags_remain_false(self):
        for key in factory.base.ordinary.FALSE:
            args=list(fixture());r=args[1][0];r['certificate'][key]=True
            r['certificate_sha256']=factory.digest(r['certificate']);reseal(args[0],args[1])
            with self.subTest(key=key),self.assertRaises(ValueError):select(args)

    def test_receipt_physical_counters_and_record_index_are_exact_ints(self):
        for key in ('native_object_observation_reads','native_object_parse_attempts',
                    'historical_roots_reobserved','original_binding_stream_traversals','owner_stream_traversals','cache_frame_reads'):
            args=list(fixture());args[0][key]=bool(args[0][key])
            with self.subTest(key=key),self.assertRaises(ValueError):select(args)
        args=list(fixture());args[1][0]['recipe_index']=False;reseal(args[0],args[1])
        with self.assertRaises(ValueError):select(args)

    def test_qualified_identity_has_frozen_typed_schema_kind_and_policy(self):
        for key,value in (('schema_version',True),('kind','future-unknown-kind'),('policy_id','other-metadata-policy')):
            args=list(fixture());r=args[1][0];r['qualified_metadata_identity'][key]=value
            q=dict(r['qualified_metadata_identity'],requested_roots=r['requested_roots'],contract=r['contract'],
                contract_sha256=r['contract_identity_sha256'],new_metadata_contract_sha256=r['contract_identity_sha256'])
            for flag in factory.native.QUALIFIED_FALSE:q.setdefault(flag,False)
            r['qualified_metadata_row_sha256']=factory.digest(q);reseal(args[0],args[1])
            with self.subTest(key=key),self.assertRaises(ValueError):select(args)


class IndependentWholeStreamTests(unittest.TestCase):
    def test_whole257_stream_spools_every_positive_singleton_once_and_protects_artifacts(self):
        with tempfile.TemporaryDirectory() as td:
            prepared,_=whole_saved_fixture(td);out=Path(td)/'out';out.mkdir();inputs={}
            spool,index,selections,ledger,hashes=factory.spool_contexts(out,prepared,inputs,time.monotonic())
            self.assertEqual(len(selections),178);self.assertEqual(len(index),178);self.assertEqual(len(ledger),257)
            self.assertEqual([len(h) for h in hashes],[64,64]);self.assertIn(spool.resolve(),inputs)
            self.assertIn((out/'contexts-index.json').resolve(),inputs);self.assertIn(prepared['native_details'].resolve(),inputs)
            with spool.open('rb') as stream:
                for selected in selections:
                    row=factory.frozen.read_context(stream,index[selected['root']['original_address']],selected)
                    self.assertEqual(row['requested_roots'],[selected['root']]);self.assertNotIn('provenance',row)
                    self.assertTrue(row['closure_observed']);self.assertTrue(row['event']=='SINGLE_ROOT_OBSERVATION')

    def test_late_compressed_integrity_failure_cannot_publish_context_index(self):
        with tempfile.TemporaryDirectory() as td:
            prepared,_=whole_saved_fixture(td);path=prepared['native_details'];raw=bytearray(path.read_bytes());raw[-1]^=1;path.write_bytes(raw)
            out=Path(td)/'out';out.mkdir()
            with self.assertRaises((ValueError,OSError,EOFError)):factory.spool_contexts(out,prepared,{},time.monotonic())
            self.assertFalse((out/'contexts-index.json').exists())


class IndependentAuthoredRunTests(unittest.TestCase):
    def harness(self,td,stack):
        root=Path(td);control=root/'build/rebuild';control.mkdir(parents=True)
        prepared,items=whole_saved_fixture(control)
        providers={r['original_address']:{k:r[k] for k in ('recipe_id','object_sha256','symbol_index')} for item in items for r in item['roots']}
        for a in factory.QUARANTINES:providers.setdefault(a,dict(recipe_id='authored-quarantine',object_sha256='d'*64,symbol_index=len(providers)))
        for i in range(68657-len(providers)):
            providers['0x%08x'%(0x30000000+i*16)]=dict(recipe_id='authored-outside',object_sha256='e'*64,symbol_index=i)
        units={};proofs={}
        for item in items:
            unit=item['unit'];rid=unit['recipe_id'];source=root/unit['source'];source.parent.mkdir(parents=True,exist_ok=True);source.write_bytes(item['source_bytes'])
            obj=control/'objects'/unit['object'];obj.parent.mkdir(parents=True,exist_ok=True);obj.write_bytes(item['raw'])
            units[rid]=unit;proofs[rid]=item['proof']
        artifacts={k:dict(path=('build/'+k+'.json' if k in ('recipes','image_check') else 'build/rebuild/'+k+'.json'),sha256=v) for k,v in factory.KNOWN.items()}
        operation=dict(schema_version=1,kind='cached-native-positive-CODE-production-operation',epoch='authored-whole180',
            roots=prepared['expected_request']['roots'],artifacts=artifacts,output_relative=factory.OUTPUT,resource_limits=factory.LIMITS)
        operation_path=control/'operation.json';operation_path.write_bytes(factory.native.canonical(operation)+b'\n')
        prepared.update(operation=operation,artifacts=dict(manifest=dict(units=list(units.values()),object_root_relative='objects')),
            units=units,proofs=proofs,providers=providers,exports=set(prepared['prepared']['exclusion_names']))
        reference=control/'authored-reference.bin';reference.write_bytes(b'AUTHORED REFERENCE ONLY')
        pe=SimpleNamespace(data=reference.read_bytes(),read=lambda address,size:bytes(size))
        snapshot=SimpleNamespace(base=0x400000,relocations=lambda:range(351931),close=lambda:None)
        def admit(operation,inputs,*,start=None):return prepared
        stack.enter_context(patch.object(factory,'ROOT',root));stack.enter_context(patch.object(factory,'OWNED',()))
        stack.enter_context(patch.object(factory,'PINS',{}));stack.enter_context(patch.object(factory,'review_gate',return_value={}))
        stack.enter_context(patch.object(factory,'prepare_operation',side_effect=admit))
        stack.enter_context(patch.dict(factory.base.pool.PINS,reference=hashlib.sha256(reference.read_bytes()).hexdigest()))
        stack.enter_context(patch.object(factory,'checked_reference',return_value=pe))
        stack.enter_context(patch.object(factory.audit,'SnapshotPe',return_value=snapshot))
        args=SimpleNamespace(operation=operation_path,operation_sha256=hashlib.sha256(operation_path.read_bytes()).hexdigest(),
            review=control/'unused-review.json',review_sha256='f'*64,reference=reference,out=root/factory.OUTPUT)
        return args,prepared

    def test_real_whole_authored_run_publishes_every_positive_and_full_ledgers(self):
        with tempfile.TemporaryDirectory() as td,ExitStack() as stack:
            args,prepared=self.harness(td,stack);result=factory.run(args)
            self.assertEqual((result['requested'],result['emitted'],result['blocked']),(178,178,0))
            self.assertEqual(result['full_field_proof_records'],178);self.assertEqual(result['coverage_counts']['PROJECTED'],178)
            self.assertFalse(result['union_providers_created']);self.assertTrue(result['original_bare_certificates_unmodified'])
            self.assertEqual(len(json.loads((args.out/'native-ledger.json').read_text())),257)
            self.assertEqual(len(json.loads((args.out/'current-frontier-ledger.json').read_text())),577)
            self.assertTrue((args.out/'receipt.json').exists());self.assertFalse((args.out/'abort.json').exists())

    def test_foreign_output_refused_before_admission_or_reference_access(self):
        with tempfile.TemporaryDirectory() as td,ExitStack() as stack:
            args,_=self.harness(td,stack);args.out=Path(td)/'foreign'
            with patch.object(factory,'prepare_operation',wraps=factory.prepare_operation) as admission:
                with self.assertRaises(ValueError):factory.run(args)
                admission.assert_not_called();factory.checked_reference.assert_not_called()
            self.assertFalse(args.out.exists())

    def test_late_saved_stream_failure_aborts_before_original_reference_gate(self):
        with tempfile.TemporaryDirectory() as td,ExitStack() as stack:
            args,prepared=self.harness(td,stack);path=prepared['native_details'];data=bytearray(path.read_bytes());data[-1]^=1;path.write_bytes(data)
            with self.assertRaises((OSError,EOFError,ValueError)):factory.run(args)
            factory.checked_reference.assert_not_called();self.assertFalse((args.out/'receipt.json').exists())
            self.assertTrue((args.out/'abort.json').exists());self.assertFalse((args.out/'CACHED-code.lib').exists())

    def test_first_member_integrity_failure_is_terminal_without_success(self):
        with tempfile.TemporaryDirectory() as td,ExitStack() as stack:
            args,_=self.harness(td,stack)
            with patch.object(factory,'verify_member',side_effect=ValueError('authored first member corruption')):
                with self.assertRaises(ValueError):factory.run(args)
            self.assertFalse((args.out/'receipt.json').exists());self.assertFalse((args.out/'CACHED-code.lib').exists())
            self.assertEqual(json.loads((args.out/'abort.json').read_text())['completed_members'],[])

    def test_postpublication_output_drift_retracts_own_success_link(self):
        with tempfile.TemporaryDirectory() as td,ExitStack() as stack:
            args,_=self.harness(td,stack);real=factory.base.finalize_success
            def finalize(*a,**kw):
                result=real(*a,**kw)
                with (args.out/'coverage.jsonl.gz').open('ab') as f:f.write(b'authored drift')
                return result
            with patch.object(factory.base,'finalize_success',side_effect=finalize):
                with self.assertRaises(ValueError):factory.run(args)
            self.assertFalse((args.out/'receipt.json').exists());self.assertTrue((args.out/'abort.json').exists())

    def test_postpublication_foreign_receipt_replacement_is_preserved(self):
        with tempfile.TemporaryDirectory() as td,ExitStack() as stack:
            args,_=self.harness(td,stack);real=factory.base.finalize_success
            def finalize(*a,**kw):
                result=real(*a,**kw);path=args.out/'receipt.json';path.unlink();path.write_bytes(b'FOREIGN REPLACEMENT')
                return result
            with patch.object(factory.base,'finalize_success',side_effect=finalize):
                with self.assertRaises(ValueError):factory.run(args)
            self.assertEqual((args.out/'receipt.json').read_bytes(),b'FOREIGN REPLACEMENT')
            self.assertTrue((args.out/'abort.json').exists())


class IndependentPublicationTests(unittest.TestCase):
    def test_journal_close_failure_prevents_any_success_receipt(self):
        class Journal:
            def close(self):raise OSError('authored durable close failure')
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)
            with self.assertRaises(OSError):factory.publish_result(out,dict(emitted=0,blocked=0),{},time.monotonic(),Journal(),lambda *a,**kw:None)
            self.assertFalse((out/'receipt.json').exists());self.assertFalse((out/'receipt.pending.json').exists())


if __name__=='__main__':unittest.main()
