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
import cached_frontier_code_factory_v13 as factory
from test_cached_frontier_code_factory_v13 import fixture,select,authored_args
from test_cached_root_observe_v13_operational_independent import whole_authored_fixture
from test_ordinary_relocation_projection_independent import authored
from test_coff_code_archive import section,symbol,aux,object_bytes


def physical_values(*,fields=False):
    """One genuine frozen4bf root plus a singleton-sized recipe union."""
    raw,contract,_,roots,providers=authored() if fields else authored(classes=())
    root=roots[0];contract=copy.deepcopy(contract);contract['provenance']['request_sha256']='a'*64
    contract['iat_import_observation']=dict(import_id=175,dll='USER32.dll',function='GetActiveWindow',original_cell='0x00fdf2fc')
    certificate=factory.base.ordinary.assess_object(factory.base.coff.parse(raw),contract)
    identity=dict(schema_version=1,kind='new-cached-metadata-contract',policy_id=factory.native.QUALIFIED_POLICY,
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
        q=dict(qidentity,requested_roots=copy.deepcopy(roots),contract=copy.deepcopy(contract),contract_sha256=factory.digest(contract),
            new_metadata_contract_sha256=factory.digest(contract))
        for key in factory.native.QUALIFIED_FALSE:q.setdefault(key,False)
        records.append(dict(schema_version=1,kind='fresh-root-observation-from-qualified-contract',policy_id=factory.native.POLICY,event=event,
            recipe_id=root['recipe_id'],recipe_index=0,requested_roots=copy.deepcopy(roots),contract=copy.deepcopy(contract),
            contract_identity_sha256=factory.digest(contract),qualified_metadata_row_sha256=factory.digest(q),qualified_metadata_identity=qidentity,
            observation_provenance=copy.deepcopy(provenance),native_object_sha256=root['object_sha256'],native_parse_performed=True,
            qualified_contract_unchanged=True,fresh_certificate_created=True,certificate=copy.deepcopy(certificate),certificate_sha256=factory.digest(certificate),
            qualified_record_ordinal=ordinal,closure_observed=certificate['closure_observed'],graph_observation_complete=certificate['graph_observation_complete'],
            root_closure_candidate=certificate['root_closure_candidate'],blockers=copy.deepcopy(certificate['blockers']),**factory.native.FALSE))
    summaries=[factory.native.summary_row(r,i) for i,r in enumerate(records,1)]
    receipt=dict(policy_id=factory.native.POLICY,status='metadata-only',input_stability=True,optional_function_index_present=False,
        qualified_contracts_preserved=True,historical_roots_reobserved=0,original_binding_stream_traversals=0,owner_stream_traversals=0,cache_frame_reads=0,
        native_object_observation_reads=1,native_object_parse_attempts=1,operation_sha256='d'*64,source_sha256='e'*64,inputs=inputs,
        summary=dict(roots=1,recipes=1,records=2,singleton_closure=1,singleton_blocked=0,union_closure=1,union_blocked=0),observations=summaries,**factory.native.FALSE)
    name=factory.base.pool.canonical({k:root[k] for k in ('recipe_id','object_sha256','symbol_index')})
    groups=dict(kind='actual-unresolved-LNK-target-groups',executable_execution=False,runtime_eligible=False,classifications=dict(CODE=1),
        groups=[dict(symbol=name,classification='CODE',observed_roles=['code'],included_provenance_is_extraction_proof=False,original_bases=[root['original_address']])])
    prepared=dict(kind='prepared-CODE-collision-exclusions',ordinary_prepared_count=0,collision_exclusion_count=0,exclusion_names=[],
        application_selection_inferred_from_counts=False,provider_selected=False,runtime_eligible=False,application_manifest_adopted=False)
    request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=copy.deepcopy(roots))
    return dict(raw=raw,records=records,receipt=receipt,request=request,groups=groups,prepared=prepared,providers=providers)


def whole_authored_field_fixture():
    """Add one authored DIR32 before any qualification/native observation exists."""
    items,_,_=whole_authored_fixture();item=items[2];u,p,roots=item['unit'],item['proof'],item['roots'];target=roots[1]
    sections=[section('.text',bytes(16),0x60501020,relocs=[(4,5,6)]),section('.text',bytes(16),0x60501020),section('.text',bytes(16),0x60501020)]
    symbols=[]
    for j,f in enumerate(p['verified_functions']):symbols.extend([symbol('.text',j+1,storage=3,auxiliary=aux(16,1 if j==0 else 0,1)),symbol(f['symbol'],j+1,typ=32)])
    directives=b' /DEFAULTLIB:"LIBCMT" /DEFAULTLIB:"OLDNAMES" '
    sections.append(section('.drectve',directives,0x100a00));symbols.extend([symbol('.drectve',4,storage=3,auxiliary=aux(len(directives),selection=0)),symbol('@feat.00',-1,value=1,storage=3)])
    raw=object_bytes(sections,symbols);h=hashlib.sha256(raw).hexdigest();u['object_sha256']=p['object_sha256']=h
    for r in roots+[item['historical_root']]:r['object_sha256']=h
    u['recipe']['symbols']={target['symbol']:target['original_address']};p['recipe_unit_sha256']=factory.digest(u['recipe']);item['raw']=raw
    row=copy.deepcopy(authored(kinds=(6,))[1]['fields'][0]);root=roots[0]
    row.update(recipe_id=u['recipe_id'],recipe_index=2,function_va=root['original_address'],function_symbol=root['symbol'],physical_section=1,physical_offset=4,source_field_offset=4,original_field_va='0x%08x'%(int(root['original_address'],16)+4),derived_source_symbol_base_va=target['original_address'],exact_original_target_va=target['original_address'],expected_original_target_va=target['original_address'],original_operand=int(target['original_address'],16),code_owners=[dict(address=target['original_address'],offset=0)])
    row['coff_relocation'].update(symbol_index=target['symbol_index'],symbol=target['symbol'],symbol_section=target['section'],symbol_value=0,symbol_type=32,symbol_storage=2,kind=6,addend=0)
    request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=[r for it in items for r in it['roots']]);rh=hashlib.sha256(factory.native.canonical(request)+b'\n').hexdigest()
    for it in items:
        unit,proof,rr=it['unit'],it['proof'],it['roots'];buckets={root['original_address']:dict(fields=[row],missing_fields=[],row_identities=[dict(ordinal=1,sha256=factory.digest(row))])} if unit['recipe_index']==2 else {}
        provenance=dict(object_sha256=unit['object_sha256'],source_sha256=unit['source_sha256'],request_sha256=rh,recipe_unit_sha256=proof['recipe_unit_sha256'],recipe_id=unit['recipe_id'],recipe_index=unit['recipe_index'],future_opaque={'typed':[True,1,False,0]})
        verification=dict(recipe_index=unit['recipe_index'],raw_sha256='b'*64,compressed_sha256='c'*64,row_count=int(bool(buckets)),first_ordinal=1 if buckets else None,last_ordinal=1 if buckets else None,whole_data_hash_verified_this_read=False,unrequested_frames_verified=False)
        views=[]
        for event,scope in [('SINGLE_ROOT_METADATA_CONTRACT',[r]) for r in rr]+[('RECIPE_UNION_METADATA_CONTRACT',rr)]:
            contract=factory.native.finite.build_contract(unit,proof,scope,buckets,None,copy.deepcopy(provenance));ch=factory.digest(contract)
            views.append(dict(schema_version=1,kind='new-cached-metadata-contract',policy_id=factory.native.QUALIFIED_POLICY,event=event,requested_roots=copy.deepcopy(scope),contract=contract,contract_sha256=ch,new_metadata_contract_sha256=ch,source_frame_verification=copy.deepcopy(verification),native_observation_required=True,**{k:False for k in factory.native.QUALIFIED_FALSE}))
        it['views']=views
    return items,request,rh


def whole_saved_fixture(directory):
    items,request,request_sha=whole_authored_field_fixture();records=[]
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
        native_object_observation_reads=44,native_object_parse_attempts=44,inputs=authority,
        operation_sha256='b'*64,source_sha256='c'*64,**factory.native.FALSE)
    receipt['observations']=[factory.native.summary_row(r,i) for i,r in enumerate(records,1)]
    receipt['summary']=dict(roots=72,recipes=44,records=116,singleton_closure=sum(r['closure_observed'] for r in records if r['event']=='SINGLE_ROOT_OBSERVATION'),singleton_blocked=sum(not r['closure_observed'] for r in records if r['event']=='SINGLE_ROOT_OBSERVATION'),union_closure=sum(r['closure_observed'] for r in records if r['event']=='RECIPE_ROOT_UNION_OBSERVATION'),union_blocked=sum(not r['closure_observed'] for r in records if r['event']=='RECIPE_ROOT_UNION_OBSERVATION'))
    rows=[]
    for root in request['roots']:
        rows.append(dict(classification='CODE',symbol=factory.base.pool.canonical({k:root[k] for k in ('recipe_id','object_sha256','symbol_index')}),
            observed_roles=['code'],included_provenance_is_extraction_proof=False,original_bases=[root['original_address']]))
    rows.extend(dict(classification='CODE',symbol='_authored_unrequested_%d'%i,original_bases=[]) for i in range(593-len(rows)))
    groups=dict(kind='actual-unresolved-LNK-target-groups',executable_execution=False,runtime_eligible=False,classifications={'CODE':593},groups=rows)
    prepared=dict(kind='prepared-CODE-collision-exclusions',ordinary_prepared_count=14529,collision_exclusion_count=14535,
        exclusion_names=['_fnv_code_%064x'%i for i in range(14535)],application_selection_inferred_from_counts=False,
        provider_selected=False,runtime_eligible=False,application_manifest_adopted=False)
    selected_request,_,_=factory.select_candidates(receipt,iter(records),request,groups,prepared)
    raw=b''.join(factory.native.canonical(r)+b'\n' for r in records);packed=gzip.compress(raw,mtime=0)
    path=Path(directory)/'authored-native.jsonl.gz';path.write_bytes(packed)
    receipt.update(details_sha256=hashlib.sha256(packed).hexdigest(),details_bytes=len(packed))
    return dict(receipt=receipt,qualification_request=request,current_groups=groups,prepared=prepared,
        expected_request=selected_request,native_details=path),items


class IndependentPhysicalTests(unittest.TestCase):
    def test_singleton_sized_positive_union_remains_evidence_only(self):
        values=physical_values(fields=True);callbacks=[]
        request,selected,ledger=factory.select_candidates(values['receipt'],values['records'],values['request'],values['groups'],values['prepared'],expected_census=(1,1,2),expected_current_codes=1,expected_prepared=(0,0),on_selected=lambda *a:callbacks.append(a))
        self.assertEqual((len(request['roots']),len(selected),len(callbacks)),(1,1,1))
        self.assertEqual(ledger[-1]['state'],'RECIPE_UNION_EVIDENCE_ONLY')

    def material(self,directory,fields=False):
        values=physical_values(fields=fields);_,selected,_=factory.select_candidates(values['receipt'],values['records'],values['request'],values['groups'],values['prepared'],expected_census=(1,1,2),expected_current_codes=1,expected_prepared=(0,0));record=values['records'][0]
        root=selected[0]['root'];payload=bytearray(factory.base.coff.parse(values['raw'])['sections'][root['section']]['payload'])
        for row in record['contract']['fields']:struct.pack_into('<I',payload,row['physical_offset'],row['original_operand'])
        payload=bytes(payload)
        pe=SimpleNamespace(data=payload,read=lambda address,size:payload[address-int(root['original_address'],16):address-int(root['original_address'],16)+size])
        original=Path(directory)/'authored-original.obj';stage=Path(directory)/'authored-stage.obj';original.write_bytes(values['raw'])
        recipe=dict(symbols={f['coff_relocation']['symbol']:f['derived_source_symbol_base_va'] for f in record['contract']['fields']})
        providers=values['providers']
        return values['raw'],record,selected[0],providers,set(),original,stage,pe,recipe

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


class IndependentWholeStreamTests(unittest.TestCase):
    def test_whole116_stream_spools_every_positive_singleton_once_and_protects_artifacts(self):
        with tempfile.TemporaryDirectory() as td:
            prepared,_=whole_saved_fixture(td);out=Path(td)/'out';out.mkdir();inputs={}
            spool,index,selections,ledger,hashes=factory.spool_contexts(out,prepared,inputs,time.monotonic())
            self.assertEqual(len(selections),70);self.assertEqual(len(index),70);self.assertEqual(len(ledger),116)
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
        operation=dict(schema_version=1,kind='cached-native-positive-CODE-production-operation',epoch='authored-whole72',
            roots=prepared['expected_request']['roots'],artifacts=artifacts,output_relative=factory.OUTPUT,resource_limits=factory.LIMITS)
        operation_path=control/'operation.json';operation_path.write_bytes(factory.native.canonical(operation)+b'\n')
        prepared.update(operation=operation,artifacts=dict(manifest=dict(units=list(units.values()),object_root_relative='objects')),
            units=units,proofs=proofs,providers=providers,exports=set(prepared['prepared']['exclusion_names']),current_successor_join={'authored_metadata_admission_stub':True})
        reference=control/'authored-reference.bin';reference.write_bytes(b'AUTHORED REFERENCE ONLY')
        operand_site=int(items[2]['roots'][0]['original_address'],16)+4;operand=int(items[2]['roots'][1]['original_address'],16)
        def read(address,size):
            result=bytearray(size)
            for j,b in enumerate(struct.pack('<I',operand)):
                if address<=operand_site+j<address+size:result[operand_site+j-address]=b
            return bytes(result)
        pe=SimpleNamespace(data=reference.read_bytes(),read=read)
        snapshot=SimpleNamespace(base=0x400000,relocations=lambda:list(range(351930))+[operand_site-0x400000],close=lambda:None,section=lambda *a,**kw:dict(executable=True),read_rva=lambda rva,size,**kw:read(rva+0x400000,size))
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
            self.assertEqual((result['requested'],result['emitted'],result['blocked']),(70,70,0))
            self.assertEqual(result['full_field_proof_records'],70);self.assertEqual(result['coverage_counts']['PROJECTED'],70)
            self.assertEqual(result['fields'],1);self.assertEqual(result['full_field_proof_rows'],1)
            self.assertEqual(json.loads((args.out/'original-field-audit.json').read_bytes())['retained_fields'],1)
            self.assertFalse(result['union_providers_created']);self.assertTrue(result['original_bare_certificates_unmodified'])
            self.assertEqual(len(json.loads((args.out/'native-ledger.json').read_text())),116)
            self.assertEqual(len(json.loads((args.out/'current-frontier-ledger.json').read_text())),593)
            self.assertTrue((args.out/'receipt.json').exists());self.assertFalse((args.out/'abort.json').exists())
            recovered=factory.base.coff.read_archive((args.out/'CACHED-code.lib').read_bytes())
            self.assertEqual(len(recovered['members']),70)
            for name,body in recovered['members']:
                self.assertEqual((args.out/('recovered-'+name)).read_bytes(),body)
            with gzip.open(args.out/'coverage.jsonl.gz','rt') as stream:
                self.assertEqual(sum(1 for _ in stream),68657)
            with gzip.open(args.out/'field-proofs.jsonl.gz','rt') as stream:
                full=[json.loads(line) for line in stream]
            self.assertEqual(len(full),70);self.assertEqual(sum(len(p['fields']) for p in full),1)

    def test_whole_requested_set_retains_policy_quarantine_as_explicit_terminal(self):
        with tempfile.TemporaryDirectory() as td,ExitStack() as stack:
            args,_=self.harness(td,stack);real=factory.verify_member;calls=[]
            def project(*a,**kw):
                calls.append(1)
                if len(calls)==1:return None,None,dict(eligible=False,blockers=[dict(code='AUTHORED_UNSUPPORTED_POLICY')])
                return real(*a,**kw)
            with patch.object(factory,'verify_member',side_effect=project):result=factory.run(args)
            self.assertEqual((result['requested'],result['emitted'],result['blocked']),(70,69,1))
            self.assertEqual(result['status'],'completed-incomplete')
            ledger=json.loads((args.out/'native-ledger.json').read_bytes())
            self.assertEqual(sum(r.get('production_status')=='EMITTED' for r in ledger),69)
            self.assertEqual(sum(r.get('production_status')=='QUARANTINED_UNSUPPORTED_POLICY' for r in ledger),1)

    def test_fresh_highlow_mismatch_is_integrity_failure_before_any_success(self):
        with tempfile.TemporaryDirectory() as td,ExitStack() as stack:
            args,_=self.harness(td,stack)
            factory.audit.SnapshotPe.return_value.relocations=lambda:range(351931)
            with self.assertRaisesRegex(ValueError,'HIGHLOW'):factory.run(args)
            self.assertFalse((args.out/'receipt.json').exists());self.assertFalse((args.out/'CACHED-code.lib').exists())
            self.assertTrue((args.out/'abort.json').exists())

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
