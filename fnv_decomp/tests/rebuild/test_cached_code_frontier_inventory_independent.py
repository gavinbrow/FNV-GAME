"""Main independent cached inventory review; authored metadata only."""
import copy
import hashlib
import gzip
import json
from contextlib import ExitStack
from pathlib import Path
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_code_frontier_inventory as inventory
import cached_code_frontier as seam
from test_cached_code_frontier_independent import fixture,AuthoredCache


def contracts(directory):
    unit,proof,selections,roots,_,_,index,data=fixture()
    path=Path(directory)/'authored.frames';path.write_bytes(data)
    result=seam.build_recipe_contexts(AuthoredCache(path,index),0,selections,unit,proof,roots,{},dict(authored=True))
    return [record['contract'] for record in result['records']]


class IndependentMetadataFeatureTests(unittest.TestCase):
    def test_all_overlapping_original_evidence_and_unknowns_preserved_without_admission(self):
        with tempfile.TemporaryDirectory() as td:
            rows=contracts(td);before=copy.deepcopy(rows)
            first,second,union=[inventory.metadata_features(c) for c in rows]
            self.assertEqual(first['primary_planning_cohort'],'OMISSION_FIELD_PROOFS_RECORDED')
            self.assertEqual(second['primary_planning_cohort'],'MISSING_FIELDS_RECORDED')
            self.assertEqual(union['primary_planning_cohort'],'MISSING_FIELDS_RECORDED')
            self.assertEqual((union['field_rows'],union['missing_rows'],union['parent_eh_records'],union['omission_field_proofs']),(2,1,1,1))
            self.assertEqual(union['target_classes'],{'AUTHORED_UNKNOWN_CLASS':1,'AUTHORED_LOCAL_LABEL_UNKNOWN':1})
            self.assertEqual(union['relocation_kinds'],{'11':2});self.assertEqual(union['binding_row_count'],3)
            self.assertTrue(union['overlapping_counts_are_not_additive_unlocks'])
            for row in (first,second,union):
                self.assertFalse(row['native_relocation_coverage_inferred']);self.assertTrue(all(row[k] is False for k in inventory.FALSE))
            self.assertEqual(rows,before)

    def test_empty_root_binding_rows_are_unknown_even_with_other_unit_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            contract=contracts(td)[0];contract['fields']=[];contract['missing_fields']=[]
            contract['provenance']['binding_row_references']=[]
            self.assertEqual(len(contract['omission_field_proofs']),1)
            info=inventory.metadata_features(contract)
            self.assertEqual(info['primary_planning_cohort'],'NO_BINDING_ROWS_NATIVE_COVERAGE_UNKNOWN')
            self.assertEqual(info['binding_row_count'],0);self.assertEqual(info['omission_field_proofs'],1)
            self.assertFalse(info['closure_inferred']);self.assertFalse(info['admission_decision_created'])

    def test_missing_row_census_cannot_be_hidden_by_complete_contract_flags(self):
        with tempfile.TemporaryDirectory() as td:
            contract=contracts(td)[-1]
            self.assertTrue(contract['fields_complete']);self.assertTrue(contract['missing_fields_complete'])
            self.assertEqual(inventory.metadata_features(contract)['missing_rows'],1)
            for mutation in ('drop_reference','drop_field','drop_missing'):
                bad=copy.deepcopy(contract)
                if mutation=='drop_reference':bad['provenance']['binding_row_references'].pop()
                elif mutation=='drop_field':bad['fields'].pop()
                else:bad['missing_fields'].clear()
                with self.subTest(mutation=mutation),self.assertRaises(ValueError):inventory.metadata_features(bad)


class IndependentSelectedRangeTests(unittest.TestCase):
    def guard(self,directory):
        path=Path(directory)/'authored.cache';data=b'selected-frame'+b'unrequested-frame';path.write_bytes(data)
        n=len(b'selected-frame')
        entry=dict(recipe_index=0,offset=0,compressed_bytes=n,compressed_sha256=hashlib.sha256(data[:n]).hexdigest(),
            raw_sha256='a'*64,row_sequence_sha256='b'*64)
        guard=inventory.SelectedRangeGuard(path,dict(data_bytes=len(data),frames=[entry]),[0])
        return path,data,n,guard

    def test_selected_range_hash_is_checked_even_when_stat_identity_is_unchanged(self):
        with tempfile.TemporaryDirectory() as td:
            path,data,n,guard=self.guard(td);guard.verify()
            path.write_bytes(b'X'+data[1:])
            with patch.object(inventory,'data_identity',return_value=guard.initial),self.assertRaises(ValueError):guard.verify()

    def test_unrequested_bytes_are_not_claimed_fresh_and_descriptor_is_honest(self):
        with tempfile.TemporaryDirectory() as td:
            path,data,n,guard=self.guard(td);path.write_bytes(data[:n]+b'X'+data[n+1:])
            with patch.object(inventory,'data_identity',return_value=guard.initial):guard.verify()
            info=guard.descriptor();self.assertFalse(info['whole_data_hash_verified_this_run'])
            self.assertFalse(info['unrequested_frames_verified']);self.assertEqual(len(info['selected_ranges']),1)
            self.assertEqual(info['selected_ranges'][0]['compressed_sha256'],hashlib.sha256(data[:n]).hexdigest())
            self.assertEqual(info['receipt_expected_whole_data_sha256'],inventory.DATA_SHA)

    def test_zero_selected_frames_and_invalid_recipe_types_remain_distinct(self):
        with tempfile.TemporaryDirectory() as td:
            path,data,n,guard=self.guard(td);index=dict(data_bytes=len(data),frames=list(guard.entries))
            empty=inventory.SelectedRangeGuard(path,index,[]);empty.verify();self.assertEqual(empty.descriptor()['selected_ranges'],[])
            for roots in ([True],[0,0],[-1],[1]):
                with self.subTest(roots=roots),self.assertRaises(ValueError):inventory.SelectedRangeGuard(path,index,roots)


class IndependentCacheDigestSemanticsTests(unittest.TestCase):
    def evidence(self):
        cm=inventory.seam.cache_module;raw='c'*64
        receipt=dict(schema_version=1,policy_id=cm.POLICY,status='metadata-cache-only',lossless_cache_complete=True,
            input_stability=True,optional_function_index_present=False,units=2988,selected_functions=68657,rows=490801,
            producer_sha256=inventory.PINS['tools/rebuild/binding_context_cache.py'],inputs=copy.deepcopy(cm.PINS),
            data_sha256=inventory.DATA_SHA,index_sha256=inventory.KNOWN['cache_index'],original_raw_sha256=raw,
            row_sequence_sha256=cm.SEQUENCE,index_bytes=128,data_bytes=256,**cm.FALSE)
        index={k:copy.deepcopy(receipt[k]) for k in ('inputs','data_sha256','data_bytes','row_sequence_sha256',
            'units','selected_functions','rows','original_raw_sha256')};index['data_file']='authored.frames'
        return receipt,index

    def test_original_raw_stream_digest_is_not_compressed_source_gzip_digest(self):
        receipt,index=self.evidence()
        self.assertNotEqual(receipt['original_raw_sha256'],inventory.seam.cache_module.PINS['rows'])
        inventory.validate_cache_receipt(receipt,index,data_name='authored.frames',index_bytes=128,data_bytes=256)

    def test_raw_receipt_index_mismatch_or_malformed_digest_rejected(self):
        for mode in ('raw_mismatch','malformed','data_name','index_hash'):
            receipt,index=self.evidence()
            if mode=='raw_mismatch':index['original_raw_sha256']='d'*64
            elif mode=='malformed':receipt['original_raw_sha256']=index['original_raw_sha256']='not-a-digest'
            elif mode=='data_name':index['data_file']='other.frames'
            else:receipt['index_sha256']='f'*64
            with self.subTest(mode=mode),self.assertRaises(ValueError):inventory.validate_cache_receipt(receipt,index,
                data_name='authored.frames',index_bytes=128,data_bytes=256)


class IndependentInventoryPublisherTests(unittest.TestCase):
    def publish(self,directory,*,tamper_receipt=False,tamper_cache=False,tamper_protected=False):
        root=Path(directory);out=root/'out';out.mkdir();path,data,n,guard=IndependentSelectedRangeTests().guard(root)
        result=dict(emitted=0,blocked=0,status='metadata-only',runtime_eligible=False)
        journal=(out/'journal.jsonl').open('x')
        def note(state,**value):journal.write(json.dumps(dict(state=state,**value))+'\n');journal.flush()
        protected=out/'protected.json';protected.write_bytes(b'{"checked":true}\n')
        inputs={protected:inventory.base.file_hash(protected)}
        if tamper_receipt or tamper_protected:
            verify=guard.verify;calls=[]
            def drift():
                verify();calls.append(1)
                if len(calls)==2:
                    if tamper_receipt:(out/'receipt.json').write_bytes(b'{"runtime_eligible":true}\n')
                    else:protected.write_bytes(b'changed protected output during post-range pass')
            guard.verify=drift
        real=inventory.base.finalize_success
        def finalize(*args):
            answer=real(*args)
            if tamper_cache:path.write_bytes(b'X'+data[1:])
            return answer
        try:
            with patch.object(inventory.base,'ROOT',root),patch.object(inventory.base,'finalize_success',side_effect=finalize):
                return inventory.publish_inventory(out,result,inputs,time.monotonic(),journal,note,guard)
        finally:
            if not journal.closed:journal.close()

    def test_real_frozen_publisher_records_expected_result(self):
        with tempfile.TemporaryDirectory() as td:
            result=self.publish(td);self.assertEqual(json.loads((Path(td)/'out/receipt.json').read_bytes()),result)

    def test_postpublish_selected_frame_drift_retracts_success(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):self.publish(td,tamper_cache=True)
            self.assertFalse((Path(td)/'out/receipt.json').exists())

    def test_postpublish_receipt_payload_drift_retracts_success(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):self.publish(td,tamper_receipt=True)
            self.assertFalse((Path(td)/'out/receipt.json').exists())

    def test_protected_output_drift_during_final_range_pass_retracts_success(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):self.publish(td,tamper_protected=True)
            self.assertFalse((Path(td)/'out/receipt.json').exists())


class IndependentAuthoredInventoryTests(unittest.TestCase):
    def setup_context(self,directory):
        root=Path(directory);area=root/'build/rebuild/authored';area.mkdir(parents=True)
        unit,proof,selections,roots,_,_,index,data=fixture()
        unit.update(source='src/authored.cpp',object='authored.obj',compiler='authored')
        frame=area/'metadata.frames.gz';frame.write_bytes(data)
        def save(name,value):
            path=area/name;path.write_bytes(seam.canonical(value)+b'\n')
            return dict(path=path.relative_to(root).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        manifest=dict(units=[unit]);index_ref=save('index.json',index);manifest_ref=save('manifest.json',manifest)
        ledger=dict(metadata_requests=roots,counts=dict(NEW_SELECTED_ROOT_REQUIRES_OBSERVATION=2),records=[
            dict(root=r,symbol=inventory.base.pool.canonical({k:r[k] for k in ('recipe_id','object_sha256','symbol_index')}),
                inventory_action='REQUEST_CACHED_METADATA',state='NEW_SELECTED_ROOT_REQUIRES_OBSERVATION') for r in roots])
        artifacts=dict(cache_index=index,selection=dict(selections=selections),manifest=manifest,
            owners=dict(details_sha256='a'*64),retained=dict(inputs=dict(image_sha256='b'*64)))
        prepared=dict(artifacts=artifacts,inventory=ledger,groups={0:roots},units={unit['recipe_id']:unit},
            proofs={unit['recipe_id']:proof},data_path=frame,imported={},registry=dict(records={}),epoch=dict(exclusion_names=[]))
        operation=dict(epoch='authored-only',artifacts=dict(cache_index=index_ref,manifest=manifest_ref),output_relative='build/rebuild/authored-output')
        op=save('operation.json',operation)
        args=SimpleNamespace(operation=root/op['path'],operation_sha256=op['sha256'],review=area/'unused-review.json',
            review_sha256='0'*64,out=root/operation['output_relative'])
        return root,args,prepared,AuthoredCache(frame,index),operation

    def run_authored(self,context,*,drift=False):
        root,args,prepared,cache,operation=context
        def admit(operation,inputs,*,start=None):
            # Production review, complete578/528/native-universe/receipt/index
            # admission are explicit stubs here. Pure authorities have separate
            # authored tests; no real saved input is qualified by this harness.
            for name,ref in operation['artifacts'].items():
                observed=inventory.load_ref(ref,inputs)
                expected=prepared['artifacts'][name]
                inventory.require(inventory.exact(observed,expected),'authored loaded metadata buffer differs')
            return prepared
        with ExitStack() as stack:
            stack.enter_context(patch.object(inventory,'ROOT',root));stack.enter_context(patch.object(inventory.base,'ROOT',root))
            stack.enter_context(patch.object(inventory,'OWNED',()));stack.enter_context(patch.object(inventory,'PINS',{}))
            stack.enter_context(patch.object(inventory,'review_gate',return_value={}))
            stack.enter_context(patch.object(inventory,'prepare_metadata',side_effect=admit))
            stack.enter_context(patch.object(inventory.seam.cache_module,'BindingContextCache',return_value=cache))
            if drift:
                publish=inventory.publish_inventory
                def corrupt(out,*a,**kw):
                    (out/'metadata-contracts.jsonl.gz').write_bytes(b'authored protected output drift')
                    return publish(out,*a,**kw)
                stack.enter_context(patch.object(inventory,'publish_inventory',side_effect=corrupt))
            return inventory.run(args)

    def test_real_frames_builder_full_contracts_journal_and_terminal_publish(self):
        with tempfile.TemporaryDirectory() as td:
            context=self.setup_context(td);result=self.run_authored(context);out=context[1].out
            self.assertEqual((result['qualified_metadata_roots'],result['qualified_recipes'],result['generated_contract_records']),(2,1,3))
            self.assertEqual(context[3].calls,[0]);self.assertTrue((out/'receipt.json').exists());self.assertFalse((out/'abort.json').exists())
            self.assertTrue(all(result[k] is False for k in inventory.FALSE));self.assertFalse(result['whole_cache_data_hash_verified_this_run'])
            self.assertEqual(json.loads((out/'receipt.json').read_bytes()),result)
            events=[json.loads(line)['state'] for line in (out/'progress.jsonl').read_text().splitlines()]
            self.assertIn('recipe_metadata_qualified',events)
            request_sha=hashlib.sha256((out/'metadata-request.json').read_bytes()).hexdigest()
            with gzip.open(out/'metadata-contracts.jsonl.gz','rt') as stream:records=[json.loads(line) for line in stream]
            self.assertEqual(len(records),3)
            for record in records:
                self.assertEqual(record['contract']['provenance']['request_sha256'],request_sha)
                self.assertEqual(record['new_metadata_contract_sha256'],seam.digest(record['contract']))
                self.assertFalse(record['historical_certificate_contract_identity_equal_claimed']);self.assertFalse(record['certificate_created'])
            self.assertEqual(records[1]['contract']['missing_fields'][0]['classification'],'MISSING_SOURCE_RELOCATION_NO_SYNTHESIS')

    def test_protected_contract_gzip_drift_cannot_leave_success(self):
        with tempfile.TemporaryDirectory() as td:
            context=self.setup_context(td)
            with self.assertRaises(ValueError):self.run_authored(context,drift=True)
            self.assertFalse((context[1].out/'receipt.json').exists());self.assertTrue((context[1].out/'abort.json').exists())


if __name__=='__main__':unittest.main()
