"""Independent authored factory metadata helpers; no real epoch/native inputs."""
from pathlib import Path
import copy
import sys
import unittest
import gzip
import json
import tempfile
from types import SimpleNamespace
from unittest.mock import patch
from contextlib import ExitStack
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import comdat_any_frontier_factory as factory
from test_comdat_any_frontier_factory import cohort_fixture,evidence_fixture


class IndependentEligibleTests(unittest.TestCase):
    def test_whole_source_set_and_all_unsupported_occurrences_preserved(self):
        receipt,rows,request,_=evidence_fixture();before=copy.deepcopy((receipt,rows,request))
        selected,ledger=factory.select_eligible(receipt,rows,request)
        self.assertEqual(len(selected),1);self.assertEqual(len(ledger),2)
        self.assertEqual(sum(x['selected'] for x in ledger),1);self.assertEqual((receipt,rows,request),before)
        for item,row in zip(ledger,rows):self.assertEqual(item['unsupported_summary'],row['unsupported_summary'])

    def test_subset_duplicate_request_counter_or_boolean_cannot_be_adopted(self):
        for mode in ('subset','duplicate','request','complete_bool','blocked_bool','promoted'):
            receipt,rows,request,_=evidence_fixture()
            if mode=='subset':rows.pop()
            elif mode=='duplicate':rows[1]=copy.deepcopy(rows[0])
            elif mode=='request':request['roots'].pop()
            elif mode=='complete_bool':receipt['composed_complete']=True
            elif mode=='blocked_bool':receipt['blocked']=True
            else:receipt['provider_selected']=True
            with self.subTest(mode=mode),self.assertRaises(ValueError):factory.select_eligible(receipt,rows,request)

    def test_changed_negative_and_typed_discharge_scope_are_fatal(self):
        for mode in ('base','authority','discharge','occurrence','preflight','witness'):
            receipt,rows,request,_=evidence_fixture();e=rows[0]
            if mode=='base':e['original_negative_certificate']['closure_observed']=True
            elif mode=='authority':e['authority']['record_sha256']='f'*64
            elif mode=='discharge':e['composed']['discharged_blockers'][0]['blocker']['code']='unrelated'
            elif mode=='occurrence':e['unsupported_summary']['original_occurrences']=True
            elif mode=='preflight':e['native_preflight']['candidate_policy_evaluated']=True
            else:e['witnesses'][0]['observation']['witness_complete']=False
            with self.subTest(mode=mode),self.assertRaises(ValueError):factory.select_eligible(receipt,rows,request)


class IndependentLatestEpochTests(unittest.TestCase):
    def test_preserves_every_parent_record_and_appends_actual_original_identities(self):
        args=cohort_fixture();before=copy.deepcopy(args);latest=factory.rebuild_latest_exclusions(*args)
        self.assertEqual(args,before);old={r['canonical']:r for r in args[0]['records']};new={r['canonical']:r for r in latest['records']}
        self.assertEqual({k:new[k] for k in old},old);self.assertEqual(len(new),14477)
        added=[r for name,r in new.items() if name not in old];self.assertEqual(len(added),68)
        for record in added:
            self.assertEqual(record['serialized_symbol_index'],0)
            self.assertGreaterEqual(record['namespace_identity']['symbol_index'],31)
            self.assertEqual(record['namespace_identity'],record['origin_identity'])
            self.assertEqual(record['source_ledger_sha256'],args[4])
        self.assertIs(latest['application_selection_inferred_from_counts'],False)
        for key in ('provider_selected','runtime_eligible','application_manifest_adopted'):self.assertIs(latest[key],False)

    def test_all68_members_and_parent_epoch_are_required(self):
        for mode in ('subset','duplicate','parent_count','parent_names','categories','ledger_sha'):
            args=list(cohort_fixture())
            if mode=='subset':args[1].pop()
            elif mode=='duplicate':args[1][1]=copy.deepcopy(args[1][0])
            elif mode=='parent_count':args[0]['ordinary_prepared_count']=True
            elif mode=='parent_names':args[0]['exclusion_names'][0]='unrelated'
            elif mode=='categories':args[0]['records'][0]['category']='application-candidate'
            else:args[4]='wrong'
            with self.subTest(mode=mode),self.assertRaises(ValueError):factory.rebuild_latest_exclusions(*args)

    def test_root_source_provider_export_and_native_map_are_bound(self):
        for mode in ('source','unit','provider','export','map_bool','map_alias','origin'):
            args=cohort_fixture();p=args[1][0]['projection'];r=p['requested_roots'][0]
            if mode=='source':r['source_sha256']='f'*64
            elif mode=='unit':args[3][r['recipe_id']]['recipe_index']=False
            elif mode=='provider':args[2][r['original_address']]['symbol_index']+=1
            elif mode=='export':p['exports']=['unrelated']
            elif mode=='map_bool':p['maps']['symbol_map'][str(r['symbol_index'])]=False
            elif mode=='map_alias':p['maps']['symbol_map']['99']=0
            else:p['original_object_sha256']='f'*64
            with self.subTest(mode=mode),self.assertRaises(ValueError):factory.rebuild_latest_exclusions(*args)

    def test_original_and_projected_plain_MATCH_receipts_are_both_mandatory(self):
        for mode in ('before','after','extent','relocation','errors'):
            args=cohort_fixture();p=args[1][0]['projection']
            if mode=='before':p['before_comparison'][0]['verdict']='mismatch'
            elif mode=='after':p['after_comparison'][0]['symbol']='wrong'
            elif mode=='extent':p['after_comparison'][0]['compiled_extent']=True
            elif mode=='relocation':p['after_comparison'][0]['relocations']=[dict(match=1)]
            else:p['before_comparison'][0]['errors']=['authored mismatch']
            with self.subTest(mode=mode),self.assertRaises(ValueError):factory.rebuild_latest_exclusions(*args)


class IndependentProjectionTests(unittest.TestCase):
    def material(self,directory):
        receipt,rows,request,original=evidence_fixture();raw,row,candidate=original[0];root=candidate['root']
        payload=factory.base.coff.parse(raw)['sections'][root['section']]['payload']
        pe=SimpleNamespace(data=payload,read=lambda address,size:payload if (address,size)==(int(root['original_address'],16),root['size']) else b'')
        before=Path(directory)/'original.obj';after=Path(directory)/'projected.obj';before.write_bytes(raw)
        args=(raw,row,candidate,rows[0],{root['original_address']:factory.observer.selector.root_identity(root)},set(),before,after,pe,{})
        return args

    def test_real_projection_preserves_negative_selection_and_field_proof(self):
        with tempfile.TemporaryDirectory() as td:
            args=self.material(td);output,p,a=factory.verify_member(*args)
            self.assertTrue(a['eligible']);self.assertEqual(args[7].read_bytes(),output)
            self.assertTrue(p['selection2_auxiliary_preserved']);self.assertTrue(p['original_negative_certificate_preserved'])
            self.assertFalse(p['selection_rewritten']);self.assertEqual(p['before_comparison'][0]['verdict'],'match')
            self.assertEqual(p['after_comparison'][0]['verdict'],'match')
            record=factory.field_proof_record('authored.obj',args[1],args[2],args[3],p,output)
            self.assertEqual(record['original_negative_certificate_sha256'],factory.digest(args[1]['certificate']))
            self.assertFalse(record['original_base_closure_observed']);self.assertFalse(record['source_evidence_enriched'])

    def test_stale_witness_and_prepared_owner_never_serialize(self):
        for mode in ('witness','prepared'):
            with tempfile.TemporaryDirectory() as td:
                args=list(self.material(td))
                if mode=='witness':args[3]=copy.deepcopy(args[3]);args[3]['native_preflight']['eligible']=False
                else:args[5]={factory.base.pool.canonical(args[4][args[2]['root']['original_address']])}
                with patch.object(factory.core,'project_member',wraps=factory.core.project_member) as writer:
                    with self.subTest(mode=mode),self.assertRaises(ValueError):factory.verify_member(*args)
                    writer.assert_not_called()
                self.assertFalse(args[7].exists())

    def test_failed_plain_comparison_or_independent_reparse_is_fatal(self):
        for mode in ('before','after','reparse'):
            with tempfile.TemporaryDirectory() as td:
                args=self.material(td);real=factory.base.bulk.compare_functions;calls=[]
                def compare(*a,**kw):
                    result=real(*a,**kw);calls.append(1)
                    if len(calls)==(1 if mode=='before' else 2):result[0]['verdict']='mismatch'
                    return result
                with ExitStack() as stack:
                    if mode=='reparse':stack.enter_context(patch.object(factory.base.bulk,'strict_reparse',side_effect=ValueError('authored strict reparse failure')))
                    else:stack.enter_context(patch.object(factory.base.bulk,'compare_functions',side_effect=compare))
                    with self.subTest(mode=mode),self.assertRaises(ValueError):factory.verify_member(*args)

    def test_original_plain_mismatch_cannot_serialize_or_write_stage(self):
        with tempfile.TemporaryDirectory() as td:
            args=self.material(td)
            with patch.object(factory.base.bulk,'compare_functions',return_value=[dict(verdict='mismatch')]), \
                 patch.object(factory.core,'project_member',wraps=factory.core.project_member) as writer:
                with self.assertRaises(ValueError):factory.verify_member(*args)
                writer.assert_not_called()
            self.assertFalse(args[7].exists())

    def test_field_proof_rejects_output_source_or_negative_identity_substitution(self):
        with tempfile.TemporaryDirectory() as td:
            args=self.material(td);output,p,_=factory.verify_member(*args)
            for key in ('output_sha256','original_object_sha256','original_negative_certificate_sha256',
                        'composed_certificate_sha256','contract_identity_sha256','central_record_sha256','observer_record_sha256'):
                q=copy.deepcopy(p);q[key]='f'*64
                with self.subTest(key=key),self.assertRaises(ValueError):factory.field_proof_record('authored.obj',args[1],args[2],args[3],q,output)
            with self.assertRaises(ValueError):factory.field_proof_record('authored.obj',args[1],args[2],args[3],p,output+b'changed')

    def test_coverage_accounts_whole_map_and_does_not_infer_historical_projection(self):
        providers={'0x%08x'%(0x04000000+i*16):dict(recipe_id='authored',object_sha256='a'*64,symbol_index=i) for i in range(68657)}
        addresses=list(providers);eligible=[dict(root=dict(original_address=a)) for a in addresses[:2]]
        request=dict(candidates=[dict(root=dict(original_address=a)) for a in addresses[:3]])
        exports={factory.base.pool.canonical(providers[addresses[3]])}
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'coverage.gz';counts=factory.write_coverage(path,providers,exports,eligible,[addresses[0]],request)
            self.assertEqual(counts,dict(PROJECTED=1,QUARANTINED=1,NOT_REQUESTED=68655))
            with gzip.open(path,'rt') as f:rows=[json.loads(line) for line in f]
            self.assertEqual(len(rows),68657);self.assertEqual(rows[3]['projection_status'],'NOT_REQUESTED')
            self.assertTrue(rows[3]['prepared_before']);self.assertTrue(rows[2]['observer_requested'])
            self.assertTrue(all(r['historical_status_inferred'] is False for r in rows))
            self.assertEqual(sum(r['emission_performed'] for r in rows),1)
            with self.assertRaises(ValueError):factory.write_coverage(Path(td)/'bad.gz',providers,exports|{factory.base.pool.canonical(providers[addresses[0]])},eligible,[],request)


class IndependentEvidenceReaderTests(unittest.TestCase):
    def use(self,data,count,callback=lambda:None):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'authored.gz'
            with gzip.open(path,'wb') as f:f.write(data)
            return factory.read_evidence(path,dict(roots=count),callback)

    def test_reader_preserves_entire_authored_evidence_and_checks_each_row(self):
        receipt,rows,_,_=evidence_fixture();calls=[]
        data=b''.join(factory.observer.selector.canonical(r)+b'\n' for r in rows)
        self.assertEqual(self.use(data,receipt['roots'],lambda:calls.append(1)),rows)
        self.assertEqual(calls,[1,1])

    def test_missing_extra_unterminated_malformed_or_oversize_rows_are_fatal(self):
        for data,count in ((b'{}\n',2),(b'{}\n{}\n',1),(b'{}',1),(b'broken\n',1)):
            with self.subTest(data=data,count=count),self.assertRaises((ValueError,json.JSONDecodeError)):self.use(data,count)
        with patch.object(factory.observer,'MAX_ROW',3):
            with self.assertRaises(ValueError):self.use(b'{"long":1}\n',1)

    def test_sampled_reader_budget_exception_is_not_swallowed(self):
        def stop():raise ValueError('authored resource exhaustion')
        with self.assertRaisesRegex(ValueError,'authored resource'):self.use(b'{}\n',1,stop)


class IndependentAuthoredPipelineTests(unittest.TestCase):
    def setup_context(self,directory):
        from test_comdat_any_frontier_observer_independent import IndependentAuthoredOperationTests
        root,_,sources=IndependentAuthoredOperationTests().setup_context(directory)
        source=next(iter(sources.values()));area=root/'build/rebuild/authored'
        with gzip.open(source['details'][0]['path'],'rt') as f:row=json.loads(f.readline())
        original_request=json.loads(Path(source['request']['path']).read_text());r=original_request['roots'][0]
        # Reuse only the authored locator, then reconstruct its candidate from
        # the authored original receipt and physical row.
        source_receipt=json.loads(Path(source['receipt']['path']).read_text())
        _,_,request,original=evidence_fixture();candidate=copy.deepcopy(original[0][2])
        candidate['root']=r;candidate['summary']=source_receipt['observations'][0]
        candidate['authority'].update(receipt_sha256=source['receipt']['sha256'],request_sha256=source['request']['sha256'],
            details_sha256=source['details'][0]['sha256'],record_sha256=factory.digest(row),
            certificate_sha256=factory.digest(row['certificate']))
        raw=(area/'authored.obj').read_bytes();evidence=factory.observer.observe_member(raw,row,candidate)
        payload=factory.base.coff.parse(raw)['sections'][r['section']]['payload']
        pe=SimpleNamespace(data=payload,read=lambda address,size:payload if (address,size)==(int(r['original_address'],16),r['size']) else b'')
        def save(name,value):
            p=area/name;p.write_text(json.dumps(value,sort_keys=True)+'\n');return dict(path=str(p),sha256=factory.base.file_hash(p))
        image=save('image-check.json',{})
        units=[dict(recipe_id=r['recipe_id'],source='src/authored.cpp',object='authored.obj',recipe={})]
        proofs=[dict(recipe_id=r['recipe_id'],verified_functions=row['contract']['unit_verified_functions'],
            recipe_unit_sha256=row['contract']['provenance']['recipe_unit_sha256'])]
        manifest=save('manifest-full-authored.json',dict(units=units))
        retained=save('retained-full-authored.json',dict(units=proofs,inputs=dict(tools_sha256={},image_check_sha256=image['sha256'])))
        selection=save('selection-authored.json',dict(selections=[]));recipes=save('recipes-authored.json',{})
        request=save('observer-request-authored.json',dict(roots=[r],candidates=[candidate]))
        context=save('observer-context-authored.json',dict(request_sha256=request['sha256'],
            artifacts=dict(manifest=manifest,retained=retained,selection=selection,recipes=recipes),sources=[source]))
        review=save('observer-review-authored.json',{})
        details=area/'observer-details-authored.gz'
        with gzip.open(details,'wb') as f:f.write(factory.observer.selector.canonical(evidence)+b'\n')
        detailref=dict(path=str(details),sha256=factory.base.file_hash(details))
        receipt=save('observer-receipt-authored.json',dict(policy_id=factory.observer.POLICY,status='metadata-only',
            input_stability=True,optional_function_index_present=False,emitted=0,roots=1,observed_addresses=[r['original_address']],
            composed_complete=1,unsupported=0,blocked=0,request_sha256=request['sha256'],context_sha256=context['sha256'],
            review_sha256=review['sha256'],details_sha256=detailref['sha256'],details_bytes=details.stat().st_size,**factory.observer.FALSE))
        refs={name:save('placeholder-'+name+'.json',{}) for name in factory.ARTIFACTS}
        refs.update(observer_receipt=receipt,observer_request=request,observer_context=context,observer_input_review=review,
            observer_details=detailref,manifest=manifest,retained=retained,selection=selection,recipes=recipes,image_check=image)
        latest=dict(exclusion_names=[]);refs['latest_prepared_epoch']=save('latest-authored.json',latest)
        latest_path=Path(refs['latest_prepared_epoch']['path'])
        latest_path.write_bytes(factory.observer.selector.canonical(latest)+b'\n')
        refs['latest_prepared_epoch']['sha256']=factory.base.file_hash(latest_path)
        archive=area/'upstream-authored.lib';archive.write_bytes(b'authored upstream archive identity only')
        archive_ref=dict(path=str(archive),sha256=factory.base.file_hash(archive))
        refs['code68_handoff']=save('handoff-authored.json',dict(archive=archive_ref))
        refs['code68_receipt']=save('code68-receipt-authored.json',dict(archive_sha256=archive_ref['sha256']))
        # Full epoch/provider admission has independent tests; this harness is
        # plumbing-only and explicitly substitutes those production gates.
        provider={r['original_address']:factory.observer.selector.root_identity(r)}
        planned=save('planned-authored.json',dict(providers={}))
        reference=area/'reference-authored.bin';reference.write_bytes(payload)
        op=save('operation-authored.json',dict(epoch='authored-only',artifacts=refs,acceptances={},roots=[r],
            source_contexts=[source],output_relative='build/rebuild/projection-authored'))
        args=SimpleNamespace(operation=Path(op['path']),operation_sha256=op['sha256'],review=area/'unused-review.json',
            review_sha256='0'*64,provider_map=Path(planned['path']),reference=reference,out=root/'build/rebuild/projection-authored')
        return root,args,provider,latest,planned['sha256'],pe

    def run_authored(self,context,*,drift=False,blocked=False):
        root,args,provider,latest,map_sha,pe=context
        class AuthoredMetadata:
            base=0
            def __init__(self,*args):pass
            def relocations(self):return range(351931)
            def close(self):pass
        with ExitStack() as stack:
            for module in (factory,factory.observer,factory.base):stack.enter_context(patch.object(module,'ROOT',root))
            stack.enter_context(patch.object(factory,'OWNED',()));stack.enter_context(patch.object(factory,'PINS',{}))
            stack.enter_context(patch.object(factory,'review_gate',return_value={}))
            stack.enter_context(patch.object(factory.observer,'review_gate',return_value={}))
            stack.enter_context(patch.object(factory,'validate_operation',return_value=None))
            stack.enter_context(patch.object(factory,'validate_code68',return_value=None))
            def basis(reports,*args):
                return ({u['recipe_id']:u for u in reports['manifest']['units']},
                        {p['recipe_id']:p for p in reports['retained']['units']},provider)
            stack.enter_context(patch.object(factory,'validate_original_basis',side_effect=basis))
            stack.enter_context(patch.object(factory,'rebuild_latest_exclusions',return_value=latest))
            stack.enter_context(patch.object(factory.base,'reconcile_recipes',return_value=dict(verified=True)))
            stack.enter_context(patch.object(factory.ordinary_factory,'validate_provider_map',return_value=provider))
            stack.enter_context(patch.object(factory.ordinary_factory,'MAP_PIN',map_sha))
            stack.enter_context(patch.dict(factory.base.pool.PINS,reference=factory.base.file_hash(args.reference)))
            stack.enter_context(patch.object(factory.base.collector,'validate_request',return_value=None))
            stack.enter_context(patch.object(factory.base,'checked_reference',return_value=pe))
            stack.enter_context(patch.object(factory.field_audit,'SnapshotPe',AuthoredMetadata))
            stack.enter_context(patch.object(factory.field_audit,'audit_original_fields',return_value={}))
            # Coverage has a separate real 68657-row test above. Keep the
            # publication harness small without pretending this is admission.
            def coverage(path,providers,exports,eligible,emitted,*args):
                Path(path).write_bytes(b'authored coverage only')
                return dict(PROJECTED=len(emitted),QUARANTINED=len(eligible)-len(emitted))
            stack.enter_context(patch.object(factory,'write_coverage',side_effect=coverage))
            if blocked:
                stack.enter_context(patch.object(factory.core,'assess_member',return_value=dict(eligible=False,blockers=[dict(code='AUTHORED_UNSUPPORTED')])))
            if drift:
                publish=factory.base.finalize_success
                def tamper(out,result,inputs,start,journal,note):
                    (out/'field-proofs.jsonl.gz').write_bytes(b'authored drift')
                    return publish(out,result,inputs,start,journal,note)
                stack.enter_context(patch.object(factory.base,'finalize_success',side_effect=tamper))
            return factory.run(args)

    def test_real_writer_comparison_archive_and_publisher_complete_first_member(self):
        with tempfile.TemporaryDirectory() as td:
            context=self.setup_context(td);result=self.run_authored(context);out=context[1].out
            self.assertEqual((result['requested'],result['emitted'],result['blocked']),(1,1,0))
            self.assertTrue((out/'receipt.json').exists());self.assertFalse((out/'abort.json').exists())
            self.assertTrue(result['original_negative_certificates_preserved']);self.assertTrue(result['selection2_auxiliaries_preserved'])
            self.assertFalse(result['selection_rewritten']);self.assertTrue((out/'COMDAT-ANY-code.lib').exists())
            self.assertIn('member_verified',[json.loads(line)['state'] for line in (out/'journal.jsonl').read_text().splitlines()])

    def test_protected_field_output_drift_rejects_successful_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            context=self.setup_context(td)
            with self.assertRaises(ValueError):self.run_authored(context,drift=True)
            self.assertFalse((context[1].out/'receipt.json').exists());self.assertTrue((context[1].out/'abort.json').exists())

    def test_fresh_consumer_blocker_preserves_quarantine_without_archive_or_code(self):
        with tempfile.TemporaryDirectory() as td:
            context=self.setup_context(td);result=self.run_authored(context,blocked=True);out=context[1].out
            self.assertEqual((result['status'],result['emitted'],result['blocked']),('completed-incomplete',0,1))
            self.assertFalse(result['emission_performed']);self.assertFalse(result['code_emission_performed'])
            self.assertIsNone(result['archive_sha256']);self.assertFalse((out/'COMDAT-ANY-code.lib').exists())
            self.assertEqual(list(out.glob('COMDAT-ANY-*.obj')),[])
            blocked=json.loads((out/'blocked.json').read_text());self.assertEqual(blocked[0]['blockers'],[dict(code='AUTHORED_UNSUPPORTED')])


if __name__=='__main__':unittest.main()
