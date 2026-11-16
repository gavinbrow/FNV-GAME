"""Independent factory attacks using authored metadata/files and mocked boundaries."""
import copy
import hashlib
import importlib
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
from test_uuid_directive_factory import f


def ledger_case():
    fields=[dict(physical_section=1,coff_relocation=dict(offset=4*i,symbol_index=i,kind=20)) for i in range(9)]
    contract=dict(fields=fields);negative=dict(blocked=True);composed=dict(preserved=True)
    projection=dict(fields=[dict(field_proof_sha256=f.digest(x),section=1,offset=4*i,symbol_index=i,kind=20,
        role='code',canonical_name='authored_%d'%i,original_base='0x10000000',original_target='0x10000000',addend_bits=0)
        for i,x in enumerate(fields)],maps=dict(section_map={1:2},symbol_map={i:i+10 for i in range(9)}),
        original_negative_certificate_sha256=f.digest(negative),contract_identity_sha256=f.digest(contract),
        composed_certificate_sha256=f.digest(composed),output_sha256='f'*64,original_negative_certificate_preserved=True)
    return contract,projection,negative,composed

class UUIDFactoryIndependentTests(unittest.TestCase):
    def ledger(self,args):
        with patch.object(f,'CERT',f.digest(args[2])),patch.object(f,'CONTRACT',f.digest(args[0])):
            return f.field_ledger(*args,'f'*64)

    def test_all_nine_fields_have_exact_original_and_serialized_identity(self):
        args=ledger_case();out=self.ledger(args)
        self.assertEqual([r['ordinal'] for r in out['mapped_fields']],list(range(1,10)))
        self.assertEqual([r['serialized_symbol_index'] for r in out['mapped_fields']],list(range(10,19)))
        self.assertTrue(all(r['serialized_section']==2 and r['role']=='code' for r in out['mapped_fields']))
        self.assertFalse(out['provider_selected']);self.assertFalse(out['runtime_eligible'])

    def test_field_hash_cannot_cover_a_different_physical_field_or_bad_index(self):
        for key,value in (('offset',99),('section',2),('symbol_index',8),('kind',6)):
            with self.subTest(key=key):
                args=ledger_case();args[1]['fields'][0][key]=value
                with self.assertRaises(ValueError):self.ledger(args)
        for target in (-1,True):
            args=ledger_case();args[1]['maps']['symbol_map'][0]=target
            with self.assertRaises(ValueError):self.ledger(args)
        args=ledger_case();args[1]['fields'].pop()
        with self.assertRaises(ValueError):self.ledger(args)

    def test_preloaded_oracle_is_rejected_before_any_producer_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);prepared=(root,{}, {}, {}, {}, {}, {}, {'compare':root/'tools/compare.py'},root/'out',{})
            with patch.object(f,'_prepare',return_value=prepared),patch.dict(sys.modules,{'compare':types.ModuleType('compare')}),patch.object(importlib,'import_module',side_effect=AssertionError('producer import too early')):
                with self.assertRaisesRegex(ValueError,'already imported'):f.run(None,None,None,None)

    def test_optional_index_appearing_after_initial_gate_rejects(self):
        with tempfile.TemporaryDirectory() as tmp:
            index=Path(tmp)/'index.json'
            with patch.object(f,'OPTIONAL_INDEX',index):
                f._stable({});index.write_text('{}')
                with self.assertRaisesRegex(ValueError,'optional function index'):f._stable({})

    def test_tools_and_rebuild_same_name_cannot_shadow_pinned_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            tools=Path(tmp)/'tools';rebuild=tools/'rebuild';rebuild.mkdir(parents=True)
            (rebuild/'producer.py').write_text('import compare\n')
            for name in ('compare','build_and_match','function_spans'):(tools/(name+'.py')).write_text('pass\n')
            (rebuild/'compare.py').write_text('raise AssertionError("must never execute")\n')
            pins={'producer':f._sha_file(rebuild/'producer.py')}
            retained={'tools/'+name+'.py':f._sha_file(tools/(name+'.py')) for name in ('compare','build_and_match','function_spans')}
            with patch.object(f,'PRODUCER_NAMES',frozenset({'producer'})):
                with self.assertRaisesRegex(ValueError,'ambiguous'):f._source_graph(rebuild,pins,{},retained)

    def test_late_protected_input_drift_and_replaced_receipt_are_distinct(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);inputpath=root/'saved.json';inputpath.write_bytes(b'authored metadata');snapshots={}
            f._snapshot(inputpath,hashlib.sha256(inputpath.read_bytes()).hexdigest(),snapshots)
            with patch.object(f,'OPTIONAL_INDEX',root/'absent-index'):
                f._stable(snapshots);inputpath.write_bytes(b'changed metadata')
                with self.assertRaisesRegex(ValueError,'protected input changed'):f._stable(snapshots)
            receipt=root/'receipt.json';owned={};f._write_owned(receipt,b'owned receipt',owned)
            foreign=root/'foreign';foreign.write_bytes(b'foreign receipt');foreign.replace(receipt)
            self.assertIn('receipt.json',f._remove_owned(owned));self.assertEqual(receipt.read_bytes(),b'foreign receipt')

    def test_application_candidate_name_excludes_root_without_provider_inference(self):
        names=['authored_%05d'%i for i in range(14534)];names[-1]='root-canonical'
        records=[dict(canonical=n,namespace_identity={'name':n},category='ordinary' if i<14528 else 'application-candidate',
                      identity_mode='physical-only-unbound-logical-demand') for i,n in enumerate(names)]
        epoch=dict(schema_version=7,kind='prepared-CODE-collision-exclusions',policy_id='prepared-CODE56-successor-v1',
            parent_manifest_sha256='934aa32fd6945ab28a364beba623e347c6c9311120e057e36e126a7d67a3ea7e',
            historical_records_preserved=True,successor_export_count=56,successor_field_count=290,
            ordinary_prepared_count=14528,collision_exclusion_count=14534,application_selected_code_count=None,
            application_selection_inferred_from_counts=False,records=records,exclusion_names=names,ordinary_names=names[:14528],
            **{key:False for key in ('provider_selected','runtime_eligible','ABI_verified','admission_decision_created',
                                    'emission_performed','namespace_approved','link_ready')})
        providers={'authored_%05d'%i:{} for i in range(68656)}
        providers[f.ROOT['original_address']]={k:f.ROOT[k] for k in ('recipe_id','object_sha256','symbol_index')}
        with self.assertRaisesRegex(ValueError,'already prepared'):
            f.validate_epoch(epoch,providers,lambda identity:identity.get('name','root-canonical'))

    def test_successor_authority_binds_parent_handoff_members_and_peer(self):
        epoch=dict(successor_handoff_sha256='a'*64,successor_member_ledger_sha256='b'*64)
        receipt=dict(kind='prepared-code56-successor-collector-receipt-v1',epoch_sha256=f.ARTIFACT_PINS['prepared_epoch'],
            input_sha256=dict(parent='934aa32fd6945ab28a364beba623e347c6c9311120e057e36e126a7d67a3ea7e',handoff='a'*64,members='b'*64),
            exports_added=56,field_rows=290,provider_selected=False,runtime_eligible=False,application_selection_inferred=False)
        peer=dict(kind='independent-prepared-code56-successor-outcome-review',status='accepted-derived-metadata-only',
            epoch_sha256=f.ARTIFACT_PINS['prepared_epoch'],receipt_sha256=f.ARTIFACT_PINS['prepared_epoch_receipt'])
        f.validate_epoch_authority(epoch,receipt,peer)
        for key in ('parent','handoff','members'):
            changed=copy.deepcopy(receipt);changed['input_sha256'][key]='0'*64
            with self.assertRaises(ValueError):f.validate_epoch_authority(epoch,changed,peer)
        changed=copy.deepcopy(receipt);changed['exports_added']=True
        with self.assertRaises(ValueError):f.validate_epoch_authority(epoch,changed,peer)
        changed=copy.deepcopy(peer);changed['receipt_sha256']='0'*64
        with self.assertRaises(ValueError):f.validate_epoch_authority(epoch,receipt,changed)

    def test_before_match_failure_cannot_reach_writer_or_projection(self):
        class Composer:
            POLICY='authored'
            def compose(self,*args,**kwargs):
                return dict(base_certificate_sha256=f.CERT,base_certificate=args[2],structural_composition_complete=True,
                    discharged_blocker_occurrences=[dict(ordinal=i,blocker_id=b) for i,b in ((1,f.UUID_ID),(2,f.UUID_ID),(3,f.DIFF_ID))],
                    remaining_blocker_occurrences=[],original_negative_unchanged=True)
        class Projector:
            POLICY='authored'
            def assess_member(self,*args,**kwargs):return dict(eligible=True)
            def project_member(self,*args,**kwargs):raise AssertionError('projection before MATCH')
        class Bulk:
            def compare_functions(self,*args,**kwargs):
                return [dict(address=f.ROOT['original_address'],symbol=f.ROOT['symbol'],size=58,compiled_extent=57,
                    verdict='match',errors=[],relocations=[dict(match=True) for _ in range(9)])]
        raw=b'authored metadata, never COFF';root=dict(f.ROOT,object_sha256=hashlib.sha256(raw).hexdigest())
        witness={k:{} for k in ('header','binding','witness_authority','declaration','review','declaration_authority')}
        with patch.object(f,'ROOT',root),patch.object(f,'_write_owned',side_effect=AssertionError('write before MATCH')):
            with self.assertRaisesRegex(ValueError,'ordinary full MATCH'):
                f._produce_member_after_gates(raw,dict(contract={},negative={}),witness,{},set(),None,None,None,None,Composer(),Projector(),Bulk(),{})


if __name__=='__main__':unittest.main()
