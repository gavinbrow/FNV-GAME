"""Authored synthetic tests; no native, original, SDK or image access."""
import importlib.util
from pathlib import Path
import unittest
import copy
import hashlib
import tempfile
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('uuid_factory',Path(__file__).resolve().parents[2]/'tools/rebuild/uuid_directive_factory.py')
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)


class Checks(unittest.TestCase):
    def row(self):
        return dict(address=f.ROOT['original_address'],symbol=f.ROOT['symbol'],size=58,compiled_extent=58,
                    verdict='match',errors=[],relocations=[{'match':True} for _ in range(9)])

    def test_full_match(self):
        self.assertTrue(f.comparison_rows([self.row()],f.ROOT['symbol']))

    def test_match_rejects_false_missing_or_extra_relocations(self):
        for mutation in ('false','bool','missing','extra','size','verdict','difference'):
            row=self.row()
            if mutation=='false': row['relocations'][0]['match']=False
            if mutation=='bool': row['relocations'][0]['match']=1
            if mutation=='missing': row['relocations'].pop()
            if mutation=='extra': row['relocations'].append({'match':True})
            if mutation=='size': row['compiled_extent']=True
            if mutation=='verdict': row['verdict']='mismatch'
            if mutation=='difference': row['byte_differences']=[1]
            with self.subTest(mutation=mutation),self.assertRaises(ValueError): f.comparison_rows([row],f.ROOT['symbol'])

    def test_field_ledger_complete_exact_order(self):
        contract={'fields':[{'physical_section':1,'coff_relocation':{'offset':i*4,'symbol_index':i,'kind':20}}
                            for i in range(9)]};negative={'blocked':True};composed={'preserved':True}
        p={'fields':[{'field_proof_sha256':f.digest(x),'section':1,'offset':i*4,'symbol_index':i,'kind':20,
                     'role':'code','canonical_name':f'sym{i}','original_base':'0x00000000',
                     'original_target':'0x00000000','addend_bits':0} for i,x in enumerate(contract['fields'])],
           'maps':{'section_map':{1:2},'symbol_map':{i:i+10 for i in range(9)}},
           'original_negative_certificate_sha256':f.digest(negative),'contract_identity_sha256':f.digest(contract),
           'composed_certificate_sha256':f.digest(composed),'output_sha256':'f'*64,'original_negative_certificate_preserved':True}
        with patch.object(f,'CERT',f.digest(negative)),patch.object(f,'CONTRACT',f.digest(contract)):
            result=f.field_ledger(contract,p,negative,composed,'f'*64)
            self.assertEqual(result['fields'],contract['fields']);self.assertFalse(result['provider_selected'])
            p['fields'].reverse()
            with self.assertRaises(ValueError):f.field_ledger(contract,p,negative,composed,'f'*64)

    def test_reject_nonfinite_epoch(self):
        with self.assertRaises(ValueError): f.validate_epoch({}, {}, lambda x:'name')

    def test_epoch_does_not_infer_application_provider_and_root_must_be_absent(self):
        names=['fixture-%05d'%i for i in range(14534)]
        records=[dict(canonical=n,namespace_identity={'name':n},category='ordinary' if i<14528 else 'application-candidate',
                      original_address='other') for i,n in enumerate(names)]
        epoch=dict(schema_version=7,kind='prepared-CODE-collision-exclusions',policy_id='prepared-CODE56-successor-v1',
                   parent_manifest_sha256='934aa32fd6945ab28a364beba623e347c6c9311120e057e36e126a7d67a3ea7e',
                   historical_records_preserved=True,successor_export_count=56,successor_field_count=290,
                   ordinary_prepared_count=14528,collision_exclusion_count=14534,application_selected_code_count=None,
                   application_selection_inferred_from_counts=False,records=records,exclusion_names=names,ordinary_names=names[:14528],
                   provider_selected=False,runtime_eligible=False,ABI_verified=False,admission_decision_created=False,
                   emission_performed=False,namespace_approved=False,link_ready=False)
        providers={'fake-%05d'%i:{} for i in range(68656)}
        providers[f.ROOT['original_address']]={k:f.ROOT[k] for k in ('recipe_id','object_sha256','symbol_index')}
        canonical=lambda identity:identity.get('name','root-canonical')
        self.assertEqual(len(f.validate_epoch(epoch,providers,canonical)),14534)
        with self.assertRaises(ValueError): f.validate_epoch(epoch,providers,lambda identity:identity.get('name',names[0]))
        epoch['collision_exclusion_count']=True
        with self.assertRaises(ValueError):f.validate_epoch(epoch,providers,canonical)

    def test_reject_fake_negative_metadata(self):
        with self.assertRaises(ValueError): f.saved_context({}, {}, {}, {})

    def test_successor_epoch_requires_matching_receipt_and_peer(self):
        epoch={'successor_handoff_sha256':'a'*64,'successor_member_ledger_sha256':'b'*64}
        receipt=dict(kind='prepared-code56-successor-collector-receipt-v1',epoch_sha256=f.ARTIFACT_PINS['prepared_epoch'],
                     input_sha256=dict(parent='934aa32fd6945ab28a364beba623e347c6c9311120e057e36e126a7d67a3ea7e',
                                       handoff='a'*64,members='b'*64),exports_added=56,field_rows=290,
                     provider_selected=False,runtime_eligible=False,application_selection_inferred=False)
        peer=dict(kind='independent-prepared-code56-successor-outcome-review',status='accepted-derived-metadata-only',
                  epoch_sha256=f.ARTIFACT_PINS['prepared_epoch'],receipt_sha256=f.ARTIFACT_PINS['prepared_epoch_receipt'])
        f.validate_epoch_authority(epoch,receipt,peer)
        for key,value in [('exports_added',True),('field_rows',289),('provider_selected',True)]:
            bad=copy.deepcopy(receipt);bad[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):f.validate_epoch_authority(epoch,bad,peer)
        bad=copy.deepcopy(peer);bad['receipt_sha256']='c'*64
        with self.assertRaises(ValueError):f.validate_epoch_authority(epoch,receipt,bad)

    def test_review_cannot_authorize_other_root_or_native(self):
        refs={k:{'path':'fixture/'+k,'sha256':v} for k,v in f.ARTIFACT_PINS.items()}
        refs.update({k:{'path':'fixture/'+k,'sha256':'1'*64} for k in f.EXTRA_ARTIFACTS})
        producers={k:'2'*64 for k in f.PRODUCER_NAMES};producers.update(f.FIXED_PRODUCERS)
        op=dict(schema_version=1,kind='finite-uuid2768-factory-operation-v1',roots=[f.ROOT.copy()],artifacts=refs,
                producer_sha256=producers,output_relative='build/rebuild/fixture',
                resource_limits={'seconds':900,'peak_memory_bytes':1073741824,'output_bytes':134217728})
        review=dict(schema_version=1,kind='finite-uuid2768-factory-input-review-v1',reviewer='fixture',approved=True,
                    root_authorized=True,independent_source_schema_review_pass=True,artifact_input_review_pass=True,
                    operation_sha256=f.digest(op),source_sha256={k:'3'*64 for k in f.OWNED},producer_sha256=op['producer_sha256'],
                    allow_original_objects_read=True,allow_source_hashing=True,allow_reference_image_read=True,
                    allow_code_emission=True,allow_native_tools=False,allow_executable_link=False,allow_game_execution=False)
        self.assertTrue(f.validate_operation(op,review))
        for key in ('allow_native_tools','allow_executable_link','allow_game_execution'):
            altered=copy.deepcopy(review);altered[key]=True
            with self.assertRaises(ValueError):f.validate_operation(op,altered)
        bad=copy.deepcopy(op);bad['roots'].append(f.ROOT.copy()); altered=copy.deepcopy(review);altered['operation_sha256']=f.digest(bad)
        with self.assertRaises(ValueError):f.validate_operation(bad,altered)
        bad=copy.deepcopy(op);bad['artifacts']['image_check']['sha256']='9'*64;altered=copy.deepcopy(review);altered['operation_sha256']=f.digest(bad)
        with self.assertRaises(ValueError):f.validate_operation(bad,altered)

    def test_unsupported_never_writes_or_compares(self):
        class Composer:
            POLICY='fixture'
            def compose(self,*a,**k):
                return dict(base_certificate_sha256=f.CERT,base_certificate=a[2],structural_composition_complete=True,
                    discharged_blocker_occurrences=[dict(ordinal=i,blocker_id=b) for i,b in
                        [(1,f.UUID_ID),(2,f.UUID_ID),(3,f.DIFF_ID)]],remaining_blocker_occurrences=[],original_negative_unchanged=True)
        class Projector:
            POLICY='fixture'
            def assess_member(self,*a,**k):return dict(eligible=False,blockers=[{'code':'unsupported'}],serialization_performed=False)
            def project_member(self,*a,**k):self.fail('projection called on unsupported')
        class Never:
            def __getattr__(self,name):raise AssertionError('unexpected writer/compare '+name)
        raw=b'authored';root=dict(f.ROOT,object_sha256=hashlib.sha256(raw).hexdigest())
        w={k:{} for k in ('header','binding','witness_authority','declaration','review','declaration_authority')}
        with patch.object(f,'ROOT',root):
            result=f._produce_member_after_gates(raw,dict(contract={},negative={}),w,{},set(),None,None,None,None,
                                                 Composer(),Projector(),Never(),{})
        self.assertEqual(result['status'],'unsupported');self.assertFalse(result['emitted'])
        class MutatingProjector(Projector):
            def assess_member(self,*a,**k):
                a[1]['tampered']=True
                return super().assess_member(*a,**k)
        with patch.object(f,'ROOT',root),self.assertRaisesRegex(ValueError,'inputs changed'):
            f._produce_member_after_gates(raw,dict(contract={},negative={}),w,{},set(),None,None,None,None,
                                          Composer(),MutatingProjector(),Never(),{})

    def test_owned_output_drift_and_replacement_cleanup(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'receipt.json';replacement=Path(tmp)/'replacement';owned={}
            f._write_owned(p,b'original',owned)
            f._check_owned(owned,{p:hashlib.sha256(b'original').hexdigest()})
            p.write_bytes(b'drift')
            with self.assertRaises(ValueError):f._check_owned(owned,{p:hashlib.sha256(b'original').hexdigest()})
            replacement.write_bytes(b'foreign');replacement.replace(p)
            f._remove_owned(owned)
            self.assertEqual(p.read_bytes(),b'foreign')

    def test_owned_cleanup_removes_only_registered_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'owned';foreign=Path(tmp)/'foreign';owned={}
            f._write_owned(p,b'data',owned);foreign.write_bytes(b'foreign')
            f._remove_owned(owned)
            self.assertFalse(p.exists());self.assertEqual(foreign.read_bytes(),b'foreign')

    def test_graph_rejects_unreviewed_tools_sibling(self):
        with tempfile.TemporaryDirectory() as tmp:
            tools=Path(tmp)/'tools';rebuild=tools/'rebuild';rebuild.mkdir(parents=True)
            (rebuild/'producer.py').write_text('import intruder\n')
            for name in ('compare','build_and_match','function_spans','intruder'):
                (tools/(name+'.py')).write_text('pass\n')
            pins={'producer':f._sha_file(rebuild/'producer.py')}
            retained={'tools/'+n+'.py':f._sha_file(tools/(n+'.py')) for n in ('compare','build_and_match','function_spans')}
            with patch.object(f,'PRODUCER_NAMES',frozenset({'producer'})):
                with self.assertRaisesRegex(ValueError,'unreviewed'):f._source_graph(rebuild,pins,{},retained)

    def test_optional_index_appearance_blocks_stability(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'function_index.json'
            with patch.object(f,'OPTIONAL_INDEX',p):
                f._stable({})
                p.write_text('{}')
                with self.assertRaisesRegex(ValueError,'optional function index'):f._stable({})

    def test_manifest_resolution_base_is_not_entire_object_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo=Path(tmp).resolve();base=repo/'build/rebuild'
            manifest_path=base/'objects-20261103T030230Z-7cfc935c.json'
            rel='objects/20261103T030230Z-7cfc935c/2768-7a8853c4310f459f/unit.obj'
            unit=dict(recipe_id=f.ROOT['recipe_id'],recipe_index=2768,object=rel,
                      source='src/staging/blk_00c40000_od.cpp',object_sha256=f.ROOT['object_sha256'],
                      source_sha256=f.ROOT['source_sha256'])
            obj=base/rel;source=repo/unit['source'];safe=base/'uuid2768-factory-result-v2'
            self.assertEqual(f.validate_output_scope(repo,manifest_path,{},unit,safe,source,obj),(base/'objects').resolve())
            for bad in (base/'objects',base/'objects/foreign',repo/'src',repo/'src/other',base,repo):
                with self.subTest(path=bad),self.assertRaises(ValueError):
                    f.validate_output_scope(repo,manifest_path,{},unit,bad,source,obj)
            with self.assertRaises(ValueError):f.validate_output_scope(repo,manifest_path,{'object_root_relative':'.'},unit,safe,source,obj)
            altered=dict(unit,object='objects/../unit.obj')
            with self.assertRaises(ValueError):f.validate_output_scope(repo,manifest_path,{},altered,safe,source,obj)
            with self.assertRaises(ValueError):f.validate_output_scope(repo,manifest_path,{},unit,safe,source,base/'other.obj')


if __name__=='__main__': unittest.main()
