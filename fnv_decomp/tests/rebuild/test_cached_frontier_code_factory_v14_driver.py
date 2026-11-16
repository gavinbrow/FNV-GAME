import gzip
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools' / 'rebuild'))
import cached_frontier_code_factory_v14_driver as driver


class BoundedObservationTests(unittest.TestCase):
    def read(self, raw, n=1, expected=None):
        body = gzip.compress(raw, mtime=0)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'details.gz'
            path.write_bytes(body)
            return driver.read_observations(path, expected_sha256=expected or hashlib.sha256(body).hexdigest(),
                expected_bytes=len(body), expected_records=n)

    def test_valid_and_authenticated_before_return(self):
        self.assertEqual(self.read(b'{"a":1}\n'), [{'a': 1}])
        with self.assertRaises(ValueError): self.read(b'{"a":1}\n', expected='0'*64)

    def test_rejects_duplicate_nonfinite_partial_extra_and_nonobject(self):
        for raw in (b'{"a":1,"a":2}\n', b'{"a":NaN}\n', b'{"a":1}', b'{}\n{}\n', b'[]\n'):
            with self.subTest(raw=raw), self.assertRaises(ValueError): self.read(raw)

    def test_exact_census(self):
        with self.assertRaises(ValueError): self.read(b'{}\n', n=2)


class TerminalOutcomeTests(unittest.TestCase):
    def setUp(self):
        self.roots = [{'root': {'original_address':'0x1','size':1}}, {'root': {'original_address':'0x2','size':2}}]
        self.outcomes = [dict(root=self.roots[0]['root'].copy(), status='emitted', evidence=dict(original_plain_match=True,
            staged_plain_match=True,strict_reparse=True,complete_field_proof=True)),
            dict(root=self.roots[1]['root'].copy(),status='quarantined-unsupported-policy',evidence=dict(blockers=['unsupported'],integrity_failure=False))]

    def test_full_partition_and_incomplete_status(self):
        self.assertEqual(driver.reconcile_outcomes(self.roots,self.outcomes)['status'], 'completed-incomplete')

    def test_reject_missing_duplicate_altered_and_unproved(self):
        import copy
        cases = [self.outcomes[:1], self.outcomes + [self.outcomes[0]], copy.deepcopy(self.outcomes), copy.deepcopy(self.outcomes)]
        cases[2][0]['root']['size'] = 99
        cases[3][0]['evidence']['staged_plain_match'] = False
        for outcomes in cases:
            with self.subTest(outcomes=outcomes), self.assertRaises(ValueError): driver.reconcile_outcomes(self.roots,outcomes)

    def test_integrity_failure_is_not_quarantine(self):
        self.outcomes[1]['evidence']['integrity_failure'] = True
        with self.assertRaises(ValueError): driver.reconcile_outcomes(self.roots,self.outcomes)


class SavedReviewTests(unittest.TestCase):
    def fixtures(self):
        roots = [{'original_address': str(i), 'size': i} for i in range(15)]
        receipt = dict(policy_id='cached-context-root-observation-v14',status='metadata-only',
            details_sha256=driver.ACCEPTED['details'][1],input_stability=True,qualified_contracts_preserved=True,
            summary=dict(roots=55,recipes=34,records=89,singleton_closure=15,singleton_blocked=40,union_closure=8,union_blocked=26))
        main = dict(approved=True,status='accepted-observation-only',receipt_sha256=driver.ACCEPTED['receipt'][1],
            details_sha256=driver.ACCEPTED['details'][1],saved_output_hashes_and_progress_reconciled=True,
            native_replay_or_original_payload_read_in_review=False,provider_selected=False,runtime_eligible=False)
        peer = dict(status='accepted-derived-observation-only',counts=dict(positive=15,union_positive=8,blocked=40,union_blocked=26),
            factory_or_runtime_approved=False,positive_singletons=[{'root':r.copy()} for r in roots])
        request = dict(kind='v14-positive-singletons-observation-request-metadata-only',status='proposed-not-admission',
            observer_receipt_sha256=driver.ACCEPTED['receipt'][1],main_outcome_review_sha256=driver.ACCEPTED['main_review'][1],
            complement_review_sha256=driver.ACCEPTED['complement_review'][1],roots=roots)
        return receipt,main,peer,request

    def test_matching_reviews_and_tampered_request(self):
        parts = self.fixtures()
        self.assertTrue(driver.validate_saved_reviews(*parts))
        parts[3]['roots'][0]['size'] = 999
        with self.assertRaises(ValueError): driver.validate_saved_reviews(*parts)

    def test_wrong_epoch_and_false_claim_of_admission(self):
        for index,key,value in [(0,'details_sha256','0'*64),(1,'provider_selected',True),(2,'factory_or_runtime_approved',True)]:
            parts = self.fixtures(); parts[index][key] = value
            with self.assertRaises(ValueError): driver.validate_saved_reviews(*parts)


class FrozenMemberTests(unittest.TestCase):
    def test_rejects_a_nonmatching_staged_comparison(self):
        from unittest.mock import patch
        import cached_frontier_code_factory_v14 as selector
        import cached_frontier_code_factory_v13 as v13
        root = dict(symbol='before', original_address='0x1', size=2)
        record = dict(contract=dict(fields=[]),certificate={},qualified_metadata_row_sha256='a')
        chosen = dict(root=root,authority={})
        def comparison(symbol, verdict):
            return dict(verdict=verdict,address='0x1',symbol=symbol,size=2,compiled_extent=2,errors=[],relocations=[])
        projection = dict(exports=['after'],fields=[],before_comparison=[comparison('before','match')],
                          after_comparison=[comparison('after','mismatch')])
        with patch.object(selector,'validate_selected'), patch.object(v13.frozen,'verify_candidate', return_value=(b'x',projection)):
            with self.assertRaises(ValueError):
                driver.verify_member(b'x',record,chosen,{},set(),None,None,None,None)

    def test_unsupported_fields_must_have_blockers(self):
        from unittest.mock import patch
        import cached_frontier_code_factory_v14 as selector
        import cached_frontier_code_factory_v13 as v13
        record = dict(contract=dict(fields=[{}]),certificate={})
        with patch.object(selector,'validate_selected'), patch.object(v13.frozen.fields.core,'assess_member',return_value=dict(eligible=False,blockers=[])):
            with self.assertRaises(ValueError):
                driver.verify_member(b'x',record,dict(root={},authority={}),{},set(),None,None,None,None)


class ProducerGuardTests(unittest.TestCase):
    def test_rejects_wrong_retained_source_proof_before_original_open(self):
        from unittest.mock import patch
        import cached_frontier_code_factory_v14 as selector
        record = {'contract': {'unit_verified_functions':[1], 'provenance':{'recipe_unit_sha256':'a'}}}
        with patch.object(selector, 'validate_selected'), patch('pathlib.Path.open', side_effect=AssertionError('opened original')):
            with self.assertRaises(ValueError):
                driver.produce_selected(record, {'root':{}}, {}, {'verified_functions':[2], 'recipe_unit_sha256':'a'},
                    'original.obj','stage.obj',{},set(),None,None,set(),{})


class ProviderAuthenticationTests(unittest.TestCase):
    def test_modified_provider_metadata_rejected_before_parsing(self):
        import cached_root_observe_v14 as native
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            selection=root / driver.PROVIDER_INPUTS['selection'][0]
            selection.parent.mkdir(parents=True); selection.write_text('{}',encoding='utf-8')
            saved={'receipt':{'inputs':{k:native.ARTIFACT_PINS[k] for k in ('manifest','retained','recipes')}}}
            with self.assertRaises(ValueError):
                driver.load_provider_inputs(root,saved,{'qualified_receipt':{'inputs':{}}})


class ArchiveGuardTests(unittest.TestCase):
    def test_archive_rejects_traversal_before_writes(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                driver.stage_archive(d, {'members':[('../foreign.obj',b'x')]}, {}, remaining_bytes=1024)
            self.assertEqual(list(Path(d).iterdir()), [])


class LedgerTests(unittest.TestCase):
    def test_positive_union_and_missing_blocker_rejected(self):
        roots=[{'original_address':str(i)} for i in range(15)]
        ledger=[dict(state='ALL_POSITIVE_SINGLETON_REQUESTED',event='SINGLE_ROOT_OBSERVATION',roots=[r]) for r in roots]
        outcomes=[dict(root=r.copy(),status='emitted') for r in roots]
        result=driver.annotate_native_ledger(ledger,outcomes)
        self.assertTrue(all(r['production_status']=='EMITTED' for r in result))
        ledger[0]['event']='RECIPE_ROOT_UNION_OBSERVATION'
        with self.assertRaises(ValueError): driver.annotate_native_ledger(ledger,outcomes)
        ledger[0]['event']='SINGLE_ROOT_OBSERVATION'
        outcomes[0].update(status='quarantined-unsupported-policy',assessment={'blockers':[]})
        with self.assertRaises(ValueError): driver.annotate_native_ledger(ledger,outcomes)


class ProductionGateTests(unittest.TestCase):
    def test_unbound_profile_rejects_before_any_filesystem_access(self):
        from unittest.mock import patch
        with patch('pathlib.Path.open',side_effect=AssertionError('unexpected file read')):
            with self.assertRaisesRegex(ValueError,'not bound'): driver.run(None)
            with self.assertRaisesRegex(ValueError,'not authenticated'): driver._run_authorized(None,{},None)


class BatchSummaryTests(unittest.TestCase):
    def test_unbacked_emission_cannot_be_published(self):
        selections=[{'root':{'original_address':str(i)}} for i in range(15)]
        contexts={str(i):{} for i in range(15)}
        outcomes=[{'root':s['root'],'status':'emitted'} for s in selections]
        with self.assertRaises(ValueError):
            driver.summarize_batch({'outcomes':outcomes,'members':[],'field_proofs':[]},selections,contexts)


class CliTests(unittest.TestCase):
    def test_cli_returns_nonzero_when_production_is_unbound(self):
        from unittest.mock import patch
        with patch('pathlib.Path.open',side_effect=AssertionError('unexpected read')):
            with self.assertRaises(SystemExit) as result:
                driver.main(['--operation','fake','--review','fake','--reference','fake','--out','fake'])
        self.assertEqual(result.exception.code,2)


class HeldIntegrationTests(unittest.TestCase):
    def test_profile_requires_matching_metadata_and_output(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); op=dict(operation_path=str(root/'op'),operation_sha256='a'*64,
                review_path=str(root/'review'),review_sha256='b'*64,reference_path=str(root/'reference'),
                output_path=str(root/'out'),output_relative='build/rebuild/out',limits={})
            import cached_root_observe_v14 as native
            project=native.ROOT.resolve()
            metadata={str((project/path).resolve()):h for path,h in driver.ACCEPTED.values()}
            metadata.update({str((project/path).resolve()):h for path,h in driver.PROVIDER_INPUTS.values()})
            for role in ('qualified_receipt','qualified_inventory','qualified_request','qualified_registry',
                    'prepared_epoch','prepared_review','current_groups','current_review','manifest','retained','recipes'):
                ref=native.ARTIFACT_PINS[role];metadata[str((project/ref['path']).resolve())]=ref['sha256']
            metadata.update({op['operation_path']:'a'*64,op['review_path']:'b'*64})
            profile=dict(operation=op,metadata_inputs=metadata,output=op['output_path'])
            guard=type('Guard',(),{})();guard.profile=profile
            driver._validate_held_metadata(profile,op,native)
            profile['metadata_inputs'][op['reference_path']]='c'*64
            with self.assertRaises(ValueError): driver._validate_held_metadata(profile,op,native)
            with self.assertRaisesRegex(ValueError,'not authenticated'):
                driver.held_entry(profile,guard)
            with self.assertRaisesRegex(ValueError,'not authenticated'):
                driver._run_authorized(None,profile,guard)

    def test_publisher_last_callback_checks_post_publication(self):
        from unittest.mock import patch
        import cached_frontier_code_factory_v13 as v13
        import v14_factory_output_publication as publication
        class Guard:
            def __init__(self):self.calls=[]
            def check(self,phase):self.calls.append(phase)
            def refresh(self):self.calls.append('refresh')
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)
            names=['selected-contexts.jsonl.gz','field-proofs.jsonl.gz','members.json','blocked.json',
                'native-ledger.json','current-frontier-ledger.json','original-field-audit.json','coverage.jsonl.gz']
            for name in names: (out/name).write_bytes(b'x')
            snap=out/'source-snapshots'/'driver.py';snap.parent.mkdir();snap.write_bytes(b's')
            journal=(out/'progress.jsonl').open('w');journal.write('terminal');journal.close()
            guard=Guard()
            def publish(_out,_hashes,_operation,_journal,stable,**kwargs):
                stable();stable();stable();return kwargs['summary']
            with patch.object(driver,'summarize_batch',return_value={'requested':15,'emitted':0,'blocked':15}), \
                    patch.object(publication,'publish_complete',side_effect=publish), patch.object(v13.base,'stable'), \
                    patch.object(v13.base,'budget'):
                driver.publish_batch(out,'a'*64,journal,{'members':[]},[],{}, {},start=0,
                    source_snapshots={'source-snapshots/driver.py':hashlib.sha256(b's').hexdigest()},guard=guard,small_metadata=())
            self.assertEqual(guard.calls,['before-publication','refresh','refresh','refresh','refresh','refresh','after-publication'])


class GuardScheduleTests(unittest.TestCase):
    def test_fifteen_quarantines_still_check_every_source_and_object_phase(self):
        from unittest.mock import patch
        import cached_frontier_code_factory_v13 as v13
        class Guard:
            def __init__(self): self.phases=[]
            def check(self,phase):self.phases.append(phase)
        class Highlow:
            def __len__(self):return 351931
        roots=[dict(original_address='0x%08x'%i,recipe_id=str(i),recipe_index=i,source_sha256='a'*64,object_sha256='b'*64) for i in range(15)]
        choices=[dict(root=r,authority=dict(ordinal=i+1)) for i,r in enumerate(roots)]
        state=dict(providers={},units={str(i):dict(source='src/example.cpp',object='file.obj',recipe={}) for i in range(15)},
                   proofs={str(i):{} for i in range(15)})
        def produce(record,selected,*args):
            return dict(root=selected['root'],status='quarantined-unsupported-policy',assessment={'blockers':['x']})
        with tempfile.TemporaryDirectory(dir=v13.ROOT/'build/rebuild') as directory:
            out=Path(directory)/'out';out.mkdir();guard=Guard()
            with patch.object(v13.base,'observe'),patch.object(driver,'produce_selected',side_effect=produce):
                result=driver.project_batch(out,choices,{r['original_address']:{} for r in roots},state,{'exclusion_names':[]},
                    directory,None,None,Highlow(),{},lambda *a,**kw:None,guard)
            self.assertEqual(len(result['outcomes']),15)
            self.assertEqual(guard.phases,['before-source','after-source','before-object','after-object']*15)


class PublicationRetractionIntegrationTests(unittest.TestCase):
    def test_failed_post_publication_guard_retracts_canonical(self):
        from unittest.mock import patch
        import os
        import cached_frontier_code_factory_v13 as v13
        if os.name!='nt': self.skipTest('reviewed publisher requires Windows')
        class Guard:
            def check(self,phase):
                if phase=='after-publication': raise ValueError('guard lost')
            def refresh(self):pass
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)
            names=['selected-contexts.jsonl.gz','field-proofs.jsonl.gz','members.json','blocked.json',
                'native-ledger.json','current-frontier-ledger.json','original-field-audit.json','coverage.jsonl.gz']
            for name in names:(out/name).write_bytes(b'x')
            snap=out/'source-snapshots'/'driver.py';snap.parent.mkdir();snap.write_bytes(b's')
            journal=(out/'progress.jsonl').open('w');journal.write('terminal');journal.close()
            with patch.object(driver,'summarize_batch',return_value={'requested':15,'emitted':0,'blocked':15}), \
                    patch.object(v13.base,'stable'),patch.object(v13.base,'budget'):
                with self.assertRaisesRegex(ValueError,'guard lost'):
                    driver.publish_batch(out,'a'*64,journal,{'members':[]},[],{}, {},start=0,
                        source_snapshots={'source-snapshots/driver.py':hashlib.sha256(b's').hexdigest()},guard=Guard(),small_metadata=())
            self.assertFalse((out/'receipt.json').exists())
            self.assertTrue((out/'receipt.pending.json').exists())


class NoImportOnUnboundTest(unittest.TestCase):
    def test_direct_call_does_not_import_before_guard(self):
        from unittest.mock import patch
        with patch('pathlib.Path.open',side_effect=AssertionError('unexpected source access')):
            with self.assertRaisesRegex(ValueError,'not authenticated'):
                driver._run_authorized(None,{},None)


class HeldForgeryTests(unittest.TestCase):
    def test_forged_registered_noop_runtime_rejected_before_protected_reads(self):
        import types
        from unittest.mock import patch
        fake=types.ModuleType('_fnv_verified_held_bootstrap_v3')
        fake.__file__=str(Path(driver.__file__).parent/'factory_held_launcher_v4.py')
        class FakeGuard:
            def check(self,phase):pass
            def refresh(self):pass
        fake.Guard=FakeGuard
        fake.require_held_guard=lambda profile,guard:guard
        guard=FakeGuard();profile={'parent_sha256':driver.HELD_PARENT_SHA256}
        original=Path.open
        def only_verifier(path,*args,**kwargs):
            if Path(path).name!='factory_held_launcher_v4.py':
                raise AssertionError('unexpected protected read')
            return original(path,*args,**kwargs)
        with patch.dict(sys.modules,{'_fnv_verified_held_bootstrap_v3':fake}), patch.object(Path,'open',only_verifier):
            with self.assertRaises(ValueError): driver._authenticate_held(profile,guard)


class AbsentIndexGuardTests(unittest.TestCase):
    def test_existing_index_stops_before_guard(self):
        from unittest.mock import Mock
        with tempfile.TemporaryDirectory() as d:
            index=Path(d)/'function_index.json';index.write_text('{}')
            inner=Mock();guard=driver._AbsentIndexGuard(inner,index)
            with self.assertRaises(ValueError):guard.check('before-reference')
            inner.check.assert_not_called()

    def test_index_created_during_guard_stops_before_work(self):
        from unittest.mock import Mock
        with tempfile.TemporaryDirectory() as d:
            index=Path(d)/'function_index.json'
            inner=Mock();inner.check.side_effect=lambda _:index.write_text('{}')
            guard=driver._AbsentIndexGuard(inner,index)
            with self.assertRaises(ValueError):guard.check('before-object')

    def test_lstat_detects_entry_even_if_exists_is_false(self):
        from unittest.mock import patch
        with patch.object(Path,'exists',return_value=False),patch.object(Path,'lstat',return_value=object()):
            with self.assertRaises(ValueError):driver._require_absent_index('function_index.json')

    def test_dangling_index_symlink_is_not_absent(self):
        with tempfile.TemporaryDirectory() as d:
            index=Path(d)/'function_index.json'
            try:
                index.symlink_to(Path(d)/'missing')
            except OSError:
                self.skipTest('file symlink privilege unavailable')
            self.assertFalse(index.exists())
            with self.assertRaises(ValueError):driver._require_absent_index(index)

    def test_refresh_checks_before_and_after(self):
        from unittest.mock import Mock
        with tempfile.TemporaryDirectory() as d:
            index=Path(d)/'function_index.json';inner=Mock()
            inner.refresh.side_effect=lambda:index.write_text('{}')
            with self.assertRaises(ValueError):driver._AbsentIndexGuard(inner,index).refresh()


class ReviewLeasePolicyTests(unittest.TestCase):
    def test_review_requires_future_lease_policy_not_false_claim_of_bound_lease(self):
        review={k:True for k in ('approved','root_authorized','source_review_pass','input_review_pass',
            'resource_lease_required','allow_original_objects_read','allow_source_hashing',
            'allow_reference_image_read','allow_code_emission')}
        review.update({k:False for k in ('allow_native_tools','allow_executable_link','allow_game_execution')})
        review.update(schema_version=1,kind='v14-factory-source-input-review-v1',operation_sha256='a'*64,reviewer='independent',peer_review_path='build/rebuild/peer.json',peer_review_sha256='d'*64,source_sha256={
            'tools/rebuild/cached_frontier_code_factory_v14_driver.py':'b'*64,
            'tests/rebuild/test_cached_frontier_code_factory_v14_driver.py':'c'*64})
        self.assertTrue(driver.validate_operation_review(review,'a'*64))
        peer=dict(schema_version=1,kind='v14-factory-input-complement-review-v1',reviewer='peer',approved=True,
            operation_sha256='a'*64,source_sha256=review['source_sha256'].copy(),profile_packet_path='build/rebuild/packet.json',profile_packet_sha256='e'*64,provider_selected=False,runtime_eligible=False)
        self.assertTrue(driver.validate_complementary_review(peer,review,'a'*64))
        peer['reviewer']='independent'
        with self.assertRaises(ValueError):driver.validate_complementary_review(peer,review,'a'*64)
        peer['reviewer']='peer';peer['provider_selected']=True
        with self.assertRaises(ValueError):driver.validate_complementary_review(peer,review,'a'*64)
        peer['provider_selected']=False;peer['source_sha256'][next(iter(peer['source_sha256']))]='e'*64
        with self.assertRaises(ValueError):driver.validate_complementary_review(peer,review,'a'*64)
        review['resource_lease_required']=False
        with self.assertRaises(ValueError):driver.validate_operation_review(review,'a'*64)
        review['resource_lease_required']=True;review['resource_lease_bound']=True
        with self.assertRaises(ValueError):driver.validate_operation_review(review,'a'*64)


class ReviewedProfileTests(unittest.TestCase):
    def test_only_four_review_and_fresh_lease_values_may_change(self):
        import copy
        draft={'operation':{'review_path':'review','review_sha256':None},'metadata_inputs':{'review':None},
            'slot':None,'lease_sha256':None,'scope':'exact'}
        packet={'kind':'v14-factory-exact-profile-packet','status':'pending-review-and-fresh-lease-NOT-LAUNCHABLE',
                'profile_draft':draft}
        actual=copy.deepcopy(draft);actual['operation']['review_sha256']='a'*64
        actual['metadata_inputs']['review']='a'*64;actual['slot']=1;actual['lease_sha256']='b'*64
        self.assertTrue(driver.validate_profile_binding(packet,actual,'a'*64))
        for key,value in [('scope','altered'),('slot',True),('lease_sha256','x'*64)]:
            tampered=copy.deepcopy(actual);tampered[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):driver.validate_profile_binding(packet,tampered,'a'*64)
        tampered=copy.deepcopy(actual);tampered['metadata_inputs']['review']='c'*64
        with self.assertRaises(ValueError):driver.validate_profile_binding(packet,tampered,'a'*64)


class SmallMetadataTests(unittest.TestCase):
    def test_small_metadata_drift_fails_full_stability(self):
        from unittest.mock import patch
        import cached_frontier_code_factory_v13 as v13
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'peer.json';path.write_bytes(b'{}')
            inputs={path:hashlib.sha256(b'{}').hexdigest()}
            with patch.object(v13.base,'stable'):
                driver.stable_with_small_metadata(inputs,(path,))
                path.write_bytes(b'{ }')
                with self.assertRaises(ValueError):driver.stable_with_small_metadata(inputs,(path,))

    def test_small_input_rejects_oversize_and_wrong_hash(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'metadata.json';path.write_bytes(b'{}')
            self.assertEqual(driver.read_small_bound_json(path,hashlib.sha256(b'{}').hexdigest()),{})
            with self.assertRaises(ValueError):driver.read_small_bound_json(path,'0'*64)
            body=b' '* (1024*1024+1);path.write_bytes(body)
            with self.assertRaises(ValueError):driver.read_small_bound_json(path,hashlib.sha256(body).hexdigest())


class FutureAnnotationVerifierRegressionTests(unittest.TestCase):
    def test_actual_parent_guard_identity_reaches_unissued_session_rejection(self):
        """Real parent bytecode must match the future-annotations caller's copy."""
        import types
        from unittest.mock import patch
        path=Path(driver.__file__).resolve().parent/'factory_held_launcher_v4.py'
        source=path.read_bytes()
        self.assertEqual(hashlib.sha256(source).hexdigest(),driver.HELD_PARENT_SHA256)
        runtime=types.ModuleType('_fnv_verified_held_bootstrap_v3');runtime.__file__=str(path)
        # This matches the child bootstrap: source compilation does not inherit
        # the driver's future-annotations setting.
        exec(compile(source,str(path),'exec',dont_inherit=True),runtime.__dict__)
        guard=runtime.Guard.__new__(runtime.Guard)
        profile={'parent_sha256':driver.HELD_PARENT_SHA256}
        with patch.dict(sys.modules,{'_fnv_verified_held_bootstrap_v3':runtime}):
            # An authentic class must pass all code-object identity checks, then
            # still fail closed because this synthetic Guard was never issued.
            with self.assertRaisesRegex(ValueError,'authentic issued Guard required'):
                driver._authenticate_held(profile,guard)

if __name__ == '__main__': unittest.main()
