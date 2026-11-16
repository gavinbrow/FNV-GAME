import copy
import importlib.util
import pathlib
import unittest
from types import SimpleNamespace
p=pathlib.Path(__file__).resolve().parents[2]/'tools/rebuild/application_wave14_diagnostic.py'
s=importlib.util.spec_from_file_location('wave14_compose_fixture',p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class CoreTest(unittest.TestCase):
    def fixture(self):
        old=[{'canonical':'old','unknown':False}]
        new=[{'canonical':'u'+str(i),'normative_field':{'ordinal':i},'unknown':None} for i in range(9)]
        uuid={'providers':[{'canonical':'u'}], 'mapped_fields':new,'base_closure_observed':False,
          'full_serialization_eligible':False,'provider_selected':False,'runtime_eligible':False,
          'ABI_verified':False,'link_ready':False,'UUID_selected_or_loaded':False}
        namespace={'physical_owners':3,'original_addresses':3,'symbols':{'old':'code'}}
        fixed_namespace=copy.deepcopy(namespace)
        calls=[]
        modules={'uuid':SimpleNamespace(consume=lambda evidence:copy.deepcopy(uuid)),
          'cohort':SimpleNamespace(disjoint_providers=lambda *a,**k:copy.deepcopy(fixed_namespace)),
          'crt':SimpleNamespace(validate=lambda *a:{'inherited_tokens_to_remove':['c'],'tokens':['c']}),
          'response':SimpleNamespace(transform=lambda *a,**k:(calls.append(k) or {'response_sha256':'x'}))}
        data=dict(report={'provenance':{'old':[{'canonical':'old','unknown':False}]},
          'selected_supplementary_providers':[], 'command':['link.exe'], 'unknown':{'retained':None}},old_fields=old,
          observation={'provider_namespace':namespace},fields=old+new,uuid_evidence={},
          old_providers=[{'canonical':'old'}],noncode_definitions=[],code21_providers=[{'canonical':'batch'}],
          prior_iat=['i'],current_iat=['i'],iat_rows=[{'canonical':'i'}],prior_crt=['c'],crt_bytes={'plan':b'','review':b'','response':b''},
          crt_validation={'inherited_tokens_to_remove':['c'],'tokens':['c']},
          baseline_response=b'',fresh_identity={},paths={'old_out':'o','new_out':'n','batch_archive':'b','uuid_archive':'u'},
          modules=modules,expected={'old_fields':1,'fields':10,'old_providers':1,'batch_providers':1,'providers':3})
        return data,calls

    def test_composes_without_mutating_old_report_and_retains_unknown(self):
        data,calls=self.fixture();old=copy.deepcopy(data['report']);result,_=m._compose(**data)
        self.assertEqual(old,data['report']);self.assertEqual(result['unknown'],{'retained':None})
        self.assertEqual(len(result['provenance']['u0']),1);self.assertEqual(calls[0]['current_crt'],['c'])
        self.assertIs(result['provider_adopted'],False)

    def test_rejects_changed_old_or_uuid_proof_before_transform(self):
        data,calls=self.fixture();data['fields'][0]={'canonical':'old','unknown':True}
        with self.assertRaisesRegex(ValueError,'old fields changed'):m._compose(**data)
        data,calls=self.fixture();data['fields'][-1]=dict(data['fields'][-1],unknown=True)
        with self.assertRaisesRegex(ValueError,'normative'):m._compose(**data)
        self.assertFalse(calls)

    def test_rejects_namespace_and_unapproved_iat(self):
        data,calls=self.fixture();data['observation']['provider_namespace']['symbols']['extra']='code'
        with self.assertRaisesRegex(ValueError,'namespace'):m._compose(**data)
        data,calls=self.fixture();data['current_iat']=['unreviewed']
        with self.assertRaisesRegex(ValueError,'IAT'):m._compose(**data)
        self.assertFalse(calls)



class IATGateTest(unittest.TestCase):
    def test_full_census_and_alias_scope(self):
        rows=[{'canonical':'c'+str(i),'native_pointer':'p'+str(i),'use_count':int(i==0),'enabled':i!=1,'complete_actual_uses':[]} for i in range(34)]
        proposal=['/ALTERNATENAME:'+r['canonical']+'='+r['native_pointer'] for r in rows]
        old=SimpleNamespace(native_evidence=lambda *a:{'proposed_pointer_aliases':[],
             'library':{'file':'k','sha256':'h','bytes':1},'unchanged_libraries':[{'file':str(i),'sha256':'h','bytes':1} for i in range(3)]},
             joins=SimpleNamespace(import34_alias_census=lambda *a:copy.deepcopy(rows)))
        ann=SimpleNamespace(census_view=lambda fields,catalog:fields)
        kwargs=dict(old=old,producer=None,annotations=ann,native={},request={},request_sha256='',parsed={},
                    originals={},expected_sources={},fields=[{'canonical':'c0','unknown':None}],catalog={},libraries={k:{} for k in ['k','0','1','2']},
                    library_refs={k:{'sha256':'h','bytes':1} for k in ['k','0','1','2']},prior_iat=proposal)
        enriched,tokens=m._iat_gate(**kwargs)
        self.assertEqual(len(tokens),33);self.assertEqual(enriched[0]['complete_actual_uses'][0]['unknown'],None)
        changed=dict(kwargs,prior_iat=proposal[:-1]+['/ALTERNATENAME:fake=x'])
        with self.assertRaisesRegex(ValueError,'changed IAT'):m._iat_gate(**changed)
        changed=dict(kwargs,fields=[])
        with self.assertRaisesRegex(ValueError,'census'):m._iat_gate(**changed)
        bad_refs=copy.deepcopy(kwargs['library_refs']);bad_refs['k']['sha256']='wrong'
        with self.assertRaisesRegex(ValueError,'provenance'):m._iat_gate(**dict(kwargs,library_refs=bad_refs))



class GuardTest(unittest.TestCase):
    def test_started_nonce_process_and_expired_or_revoked_lease(self):
        import datetime, json, os, tempfile
        from unittest import mock
        now=datetime.datetime.now(datetime.timezone.utc)
        pins={'application-wave14-prepare-request-v2.json':'r', 'application_wave14_diagnostic.py':'s',
              'application-wave14-prepare-independent-review-v2.json':'v'}
        row={'owner':'/root/rebuild_startup_host','resource':'lightweight_metadata','slot':1,'state':'granted',
             'review_sha256':'v','input_pins':pins,'granted_utc':(now-datetime.timedelta(seconds=1)).isoformat(),
             'max_seconds':60}
        review={'tests_sha256':'t','watchdog_tests_sha256':'wtest','watchdog_sha256':'w'}
        sp={'request':'r','source':'s','source_tests':'t','watchdog_tests':'wtest','inputs':'i','review':'v',
            'watchdog':'w','interpreter':m.EXPECTED_INTERPRETER['sha256']}
        child={'pid':23,'parent_pid':24,'create_time':1.0,'executable':m.EXPECTED_INTERPRETER['path']}
        record={'kind':'wave14-prepare-watchdog-child-started','child':child,'pins':sp,'slot':1,'handshake_nonce':'a'*64}
        process=SimpleNamespace(pid=23,ppid=lambda:24,create_time=lambda:1.0,exe=lambda:child['executable'])
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(m,'ROOT',pathlib.Path(temp)), \
             mock.patch.object(m.os,'getpid',return_value=23),mock.patch.object(m.os,'getppid',return_value=24), \
             mock.patch.dict(os.environ,{'FNV_WAVE14_PREPARE_HANDSHAKE_NONCE':'a'*64}):
            started=m.ROOT/m.WATCHDOG_STARTED_PATH;started.parent.mkdir(parents=True);started.write_text(json.dumps(record))
            registry=m.ROOT/m.LEASE_REGISTRY_PATH;registry.parent.mkdir(parents=True);registry.write_text(json.dumps({'schema_version':1,'leases':[row]}))
            self.assertEqual(m._watchdog_started(review,'s','i','v','r',SimpleNamespace(Process=lambda:process))[0],record)
            m._active_lease(1,'r','s','v')
            record['handshake_nonce']='b'*64;started.write_text(json.dumps(record))
            with self.assertRaisesRegex(ValueError,'nonce'):m._watchdog_started(review,'s','i','v','r',SimpleNamespace(Process=lambda:process))
            row['state']='revoked';registry.write_text(json.dumps({'schema_version':1,'leases':[row]}))
            with self.assertRaisesRegex(ValueError,'active metadata lease'):m._active_lease(1,'r','s','v')
            row['state']='granted';row['granted_utc']=(now-datetime.timedelta(seconds=90)).isoformat()
            registry.write_text(json.dumps({'schema_version':1,'leases':[row]}))
            with self.assertRaisesRegex(ValueError,'lease not live'):m._active_lease(1,'r','s','v')



class PublishTest(unittest.TestCase):
    def test_rechecks_each_stage_and_rejects_late_revocation(self):
        import tempfile
        from unittest import mock
        class Utility:
            def __init__(self):self.phases=[]
            def stable_phase(self,bindings,*,phase,stable_fn):
                self.phases.append(phase);stable_fn(bindings);return {'phase':phase}
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(m,'ROOT',pathlib.Path(temp)):
            out=m.ROOT/m.OUTPUT_PATH;out.parent.mkdir(parents=True)
            utility=Utility();checks=[]
            result,phases=m._publish_private(out=out,report={'unknown':None},response=b'"x"\n',bindings=[],
                guard=lambda:checks.append('guard'),stable_utility=utility,stable_fn=lambda rows:None,start=0,clock=lambda:1)
            self.assertEqual(len(phases),6);self.assertEqual(utility.phases,['pre']+['post']*5)
            self.assertEqual(len(checks),12);self.assertEqual(result['unknown'],None)
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(m,'ROOT',pathlib.Path(temp)):
            out=m.ROOT/m.OUTPUT_PATH;out.parent.mkdir(parents=True);calls=[]
            def revoked():
                calls.append(1)
                if len(calls)==4:raise ValueError('revoked')
            with self.assertRaisesRegex(ValueError,'revoked'):
                m._publish_private(out=out,report={},response=b'x',bindings=[],guard=revoked,
                  stable_utility=Utility(),stable_fn=lambda rows:None,start=0,clock=lambda:1)
            self.assertFalse((out/'receipt.json').exists())



class BaselineTest(unittest.TestCase):
    def test_rebuild_namespace_and_reject_extra_provider(self):
        ns={'symbols':{'system':'existing-noncode'},'physical_owners':2}
        report={'provenance':{'x':[{'component':'current-CODE-definition','canonical':'x'}]},
                'selected_supplementary_providers':[]}
        diag=SimpleNamespace(partial=SimpleNamespace(CANONICAL='entry',IDENTITY={'recipe_id':'r','object_sha256':'o','symbol_index':1}))
        cohort=SimpleNamespace(disjoint_providers=lambda a,**k:copy.deepcopy(ns))
        baseline,noncode=m._baseline_namespace(report,{'provider_namespace':ns},diag,cohort,2)
        self.assertEqual(len(baseline),2);self.assertEqual(noncode,['system'])
        with self.assertRaisesRegex(ValueError,'census'):m._baseline_namespace(report,{'provider_namespace':ns},diag,cohort,3)



class ObservationTest(unittest.TestCase):
    def test_observer_keeps_original_negative_and_exact_old_records(self):
        import hashlib
        old=[{'n':i} for i in range(46237)];fields=old+[{'n':i} for i in range(46237,46292)]
        receipt=dict(kind='wave14-CODE21-UUID-field-observation',status='observed-not-adopted',
            complete_field_count=46292,selected_Game_function_candidates=14555,ordinary_prepared_count=14550,
            baseline_field_count=46237,code21_field_count=46,uuid_field_count=9,
            baseline_ordered_digest=hashlib.sha256(m._canonical(old)).hexdigest(),
            fields_canonical_sha256='08106a9552e9fe8fbe43a5bd224a212409b00228c26654432b715223eb0d6da4',
            uuid_base_closure_observed=False,uuid_full_serialization_eligible=False,providers=[{}]*22,
            uuid_original_negative_occurrences=[{},{},{}],producer_prior_quarantines=['0x00452580','0x004e6370','0x004e6620','0x0086beb0','0x0086ff70','0x009781d0'],producer_new_blocked=[],source_ABI_verified=False,provider_selected=False,
            runtime_eligible=False,link_ready=False,application_cohort_adopted=False,native_tools_run=False,
            executable_link_performed=False,game_execution_performed=False)
        d=SimpleNamespace(canonical=m._canonical,digest=lambda raw:receipt['fields_canonical_sha256'])
        m._validate_observation(receipt,old,fields,d)
        bad=dict(receipt,uuid_base_closure_observed=True)
        with self.assertRaisesRegex(ValueError,'negative'):m._validate_observation(bad,old,fields,d)
        bad_fields=list(fields);bad_fields[0]={'n':-1}
        with self.assertRaisesRegex(ValueError,'ordered'):m._validate_observation(receipt,old,bad_fields,d)



class SourceLoaderTest(unittest.TestCase):
    def test_lazy_only_and_snapshot_bytes(self):
        import importlib, sys
        name='_wave14_fixture_a';unused='_wave14_fixture_unused'
        snapshots={name:b'value=3\n',unused:b'raise RuntimeError("unexpected execution")\n'}
        finder=m._SnapshotFinder(snapshots,{name:'fixture_a.py',unused:'unused.py'},pathlib.Path.cwd())
        with __import__('unittest.mock',fromlist=['patch']).patch.object(sys,'meta_path',[finder]+sys.meta_path):
            try:
                loaded=importlib.import_module(name)
                self.assertEqual(loaded.value,3);self.assertNotIn(unused,sys.modules)
            finally:sys.modules.pop(name,None)
    def test_restrict_workspace_fallback(self):
        root=pathlib.Path.cwd()
        paths=['',str(root),str(root/'tools'/'rebuild'),str(root.parent)]
        self.assertEqual(m._restricted_project_search_paths(paths,root),[str(root.parent)])



class ManifestTest(unittest.TestCase):
    def test_review_and_fixed_graph_are_mandatory(self):
        pin='a'*64;inputs={'v':{'path':'v','sha256':pin}};sources={'s':{'path':'tools/s.py','sha256':pin}}
        third={'version':'fixture'}
        manifest=dict(kind='wave14-fixed-prepare-inputs-v1',schema_version=1,inputs=inputs,source_pins=sources,
          limits={'seconds':480,'rss_bytes':1073741824,'output_bytes':134217728},output=m.OUTPUT_PATH,
          interpreter=m.EXPECTED_INTERPRETER,third_party_runtime=third)
        review=dict(kind='independent-wave14-combined-prepare-source-input-review',schema_version=1,
          status='accepted-metadata-only',source_sha256=pin,tests_sha256=pin,inputs_sha256=pin,
          request_sha256=pin,watchdog_sha256=pin,watchdog_tests_sha256=pin,third_party_runtime=third)
        kwargs=dict(source_sha=pin,tests_sha=pin,inputs_sha=pin,expected_inputs=inputs,expected_sources=sources,third_party=third)
        m._verify_fixed_manifest(manifest,review,**kwargs)
        for bad in (dict(review,status='pending'),dict(review,source_sha256='b'*64)):
            with self.assertRaisesRegex(ValueError,'review'):m._verify_fixed_manifest(manifest,bad,**kwargs)
        bad=dict(manifest,source_pins={})
        with self.assertRaisesRegex(ValueError,'scope'):m._verify_fixed_manifest(bad,review,**kwargs)



class ReinsertedPathTest(unittest.TestCase):
    def test_unknown_workspace_module_rejected_after_path_reinsertion(self):
        import importlib, sys, tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as tmp:
            root=pathlib.Path(tmp);name='_wave14_forbidden_module'
            (root/(name+'.py')).write_text('raise RuntimeError("must not execute")')
            finder=m._SnapshotFinder({'_wave14_allowed':b'value=1\n'},
                                     {'_wave14_allowed':str(root/'allowed.py')},root)
            with mock.patch.object(sys,'meta_path',[finder]+sys.meta_path), mock.patch.object(sys,'path',[str(root)]+sys.path):
                with self.assertRaisesRegex(ImportError,'unreviewed project source'):
                    importlib.import_module(name)
                self.assertNotIn(name,sys.modules)



class PreloadedTest(unittest.TestCase):
    def test_preloaded_workspace_module_rejected(self):
        import sys, tempfile, types
        from unittest import mock
        with tempfile.TemporaryDirectory() as tmp:
            root=pathlib.Path(tmp);fake=types.ModuleType('_wave14_preloaded');fake.__file__=str(root/'bad.py')
            with mock.patch.dict(sys.modules,{'_wave14_preloaded':fake}):
                with self.assertRaisesRegex(ValueError,'preloaded workspace'):
                    m._reject_preloaded_workspace(root,root/'entry.py')



class SnapshotAuthTest(unittest.TestCase):
    def test_exact_bytes_bound_before_import_and_tamper_rejected(self):
        import hashlib, tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as tmp,mock.patch.object(m,'ROOT',pathlib.Path(tmp)):
            path=m.ROOT/'tools'/'rebuild'/'fixture.py';path.parent.mkdir(parents=True);path.write_bytes(b'x=1\n')
            digest=hashlib.sha256(path.read_bytes()).hexdigest()
            graph={'_wave14_snapshot_fixture':{'path':'tools/rebuild/fixture.py','sha256':digest}}
            snapshots,paths=m._source_snapshots(graph,[])
            self.assertEqual(snapshots['_wave14_snapshot_fixture'],b'x=1\n')
            path.write_bytes(b'x=2\n')
            with self.assertRaisesRegex(ValueError,'hash differs'):
                m._source_snapshots(graph,[])



class CRTBindingTest(unittest.TestCase):
    def test_missing_and_conflicting_crt_inputs_fail(self):
        plan={'sources':{'tools/s.py':'a'},'inputs':{'old.json':'b'},
              'own_sources':{'src/a.cpp':'c'},'units_sha256':'d'}
        inputs={'s':{'path':'tools/s.py','sha256':'a'},'old':{'path':'build/rebuild/old.json','sha256':'b'},
                'src':{'path':'src/a.cpp','sha256':'c'},'units':{'path':'build/units.json','sha256':'d'}}
        m._validate_crt_bound_inputs(plan,inputs)
        missing=dict(inputs);del missing['src']
        with self.assertRaisesRegex(ValueError,'not bound'):m._validate_crt_bound_inputs(plan,missing)
        with self.assertRaisesRegex(ValueError,'conflicting'):m._validate_crt_bound_inputs(plan,inputs,{'x':{'path':'src/a.cpp','sha256':'changed'}})



class DisabledEntryTest(unittest.TestCase):
    def test_unbound_pins_fail_before_any_read(self):
        from unittest import mock
        with mock.patch.object(m,'FIXED_INPUTS',None), mock.patch.object(m,'bind',side_effect=AssertionError('unexpected read')):
            with self.assertRaisesRegex(ValueError,'authority not yet bound'):
                m._startup_authority(inputs_path='x',inputs_sha256='x',source_sha256='x',tests_sha256='x',review_path='x',review_sha256='x')



class EndToEndFixtureTest(unittest.TestCase):
    def test_authored_large_cohort_wiring_and_baseline_immutability(self):
        import hashlib
        old=[{'canonical':'f'+str(i),'proof':{'role':'code'},'unknown':None} for i in range(46237)]
        code=[{'canonical':'b'+str(i),'proof':{'role':'code'},'original_field_proof':{'row':i}} for i in range(46)]
        ufields=[{'canonical':'u'+str(i),'proof':{'role':'code'},'normative_field':{'row':i}} for i in range(9)]
        extra=[{'canonical':'bp'+str(i)} for i in range(21)];up=[{'canonical':'uuid-provider'}]
        expected={'path':'C:\\sdk\\Uuid.Lib','sha256':'a'*64,'size':3,'device':7,'inode':9}
        uq=dict(providers=up,mapped_fields=ufields,base_closure_observed=False,full_serialization_eligible=False,
            provider_selected=False,runtime_eligible=False,ABI_verified=False,link_ready=False,UUID_selected_or_loaded=False,
            future_uuid_response_token=expected['path'],dependency_identity=expected)
        base_ns={'symbols':{'existing':'existing-noncode'},'physical_owners':14533,'original_addresses':14533}
        full_ns={'symbols':{'existing':'existing-noncode'},'physical_owners':14555,'original_addresses':14555}
        definitions=[{'component':'current-CODE-definition','canonical':'provider'+str(i)} for i in range(14532)]
        aliases=[{'canonical':'i'+str(i),'native_pointer':'p'+str(i),'enabled':True} for i in range(34)]
        iatrows=[dict(r,use_count=0,complete_actual_uses=[]) for r in aliases]
        native=[{'file':str(i),'sha256':'x','bytes':1} for i in range(4)]
        report={'provenance':{'definitions':definitions},'selected_supplementary_providers':[],
          'aliases':aliases,'CRT_diagnostic_bindings':{'tokens':['c']},'command':['link.exe'],
          'default_libraries':{'libcmt.lib':{'sha256':'lib'}},'unknown':{'preserved':None}}
        old_report=copy.deepcopy(report)
        observation=dict(kind='wave14-CODE21-UUID-field-observation',status='observed-not-adopted',
          complete_field_count=46292,selected_Game_function_candidates=14555,ordinary_prepared_count=14550,
          baseline_field_count=46237,code21_field_count=46,uuid_field_count=9,
          baseline_ordered_digest=hashlib.sha256(m._canonical(old)).hexdigest(),
          fields_canonical_sha256='08106a9552e9fe8fbe43a5bd224a212409b00228c26654432b715223eb0d6da4',
          uuid_base_closure_observed=False,uuid_full_serialization_eligible=False,providers=extra+up,
          uuid_original_negative_occurrences=[{},{},{}],uuid_source_evidence=uq,provider_namespace=full_ns,IAT_fields=0,
          producer_prior_quarantines=['0x00452580','0x004e6370','0x004e6620','0x0086beb0','0x0086ff70','0x009781d0'],
          producer_new_blocked=[],source_ABI_verified=False,provider_selected=False,runtime_eligible=False,
          link_ready=False,application_cohort_adopted=False,native_tools_run=False,executable_link_performed=False,
          game_execution_performed=False)
        calls=[]
        diag=SimpleNamespace(canonical=m._canonical,digest=lambda x:observation['fields_canonical_sha256'],
             partial=SimpleNamespace(CANONICAL='entry',IDENTITY={'recipe_id':'r','object_sha256':'x','symbol_index':1}))
        cohort=SimpleNamespace(disjoint_providers=lambda added,**k:copy.deepcopy(full_ns if added else base_ns))
        oldmod=SimpleNamespace(native_evidence=lambda *a:{'proposed_pointer_aliases':[],'library':native[0],
             'unchanged_libraries':native[1:]},joins=SimpleNamespace(import34_alias_census=lambda *a:copy.deepcopy(iatrows)))
        modules={'diagnostic':diag,'cohort':cohort,'uuid':SimpleNamespace(consume=lambda x:copy.deepcopy(uq)),
          'crt':SimpleNamespace(validate=lambda *a:{'inherited_tokens_to_remove':['c'],'tokens':['c']}),
          'response':SimpleNamespace(transform=lambda *a,**k:(calls.append(k) or {'response_sha256':'h'})),
          'import34':oldmod,'producer':None,'annotations':SimpleNamespace(census_view=lambda f,c:f)}
        refs={str(i):{'sha256':'x','bytes':1} for i in range(4)}
        plan=m._canonical({'bindings':[{'normal_provider':{'archive_sha256':'lib'}}]})
        data={'v13_report':report,'v13_observation':{'provider_namespace':base_ns},'v14_observation':observation,
          'v13_fields':old,'v14_fields':old+code+ufields,'uuid_evidence':{},'iat_native':{},'iat_request':{},
          'iat_request_sha256':'z','iat_parsed_archive':{},'iat_originals':{},'iat_expected_sources':{},
          'iat_catalog':{},'iat_libraries':{k:{} for k in refs},'iat_library_refs':refs,
          'crt_bytes':{'plan':plan,'review':b'','response':b''},
          'crt_consumer_peer':{'validation':{'inherited_tokens_to_remove':['c'],'tokens':['c']}},'baseline_response':b'baseline'}
        paths={'old_out':'old','new_out':'new','batch_archive':'batch','uuid_archive':'uuid'}
        result,_=m._assemble_private(data=data,modules=modules,sdk_identity=dict(expected,requested_path=expected['path']),paths=paths)
        self.assertEqual(report,old_report);self.assertEqual(result['unknown'],{'preserved':None})
        self.assertEqual(len(result['aliases']),34);self.assertEqual(len(calls[0]['current_iat']),34)
        self.assertIs(result['provider_selected'],False);self.assertEqual(result['IAT_actual_fields'],0)
        bad=copy.deepcopy(observation);bad['producer_new_blocked']=['unexpected']
        with self.assertRaisesRegex(ValueError,'terminal outcome'):
            m._assemble_private(data=dict(data,v14_observation=bad),modules=modules,
              sdk_identity=dict(expected,requested_path=expected['path']),paths=paths)



class MergePinsTest(unittest.TestCase):
    def test_equal_duplicates_and_conflict(self):
        x='a'*64;y='b'*64
        self.assertEqual(m._merge_pins({'p':x},{'p':x,'q':y}),{'p':x,'q':y})
        with self.assertRaisesRegex(ValueError,'conflicting'):m._merge_pins({'p':x},{'p':y})



class PeerTest(unittest.TestCase):
    def test_observer_peer_accepts_exact_and_rejects_bool_integer(self):
        peer={'kind':'independent-wave14-combined-observer-outcome-review','schema_version':1,
          'status':'accepted-derived-metadata-only',
          'receipt_sha256':'b6538d8aa9aff10826da60703500a7cc8b374d5efed6cced3e41debba7332185',
          'fields_sha256':'73a57a716b97cf116e625f2a585039a494b7d8a06293be5810672d229b211075',
          'fields_canonical_sha256':'08106a9552e9fe8fbe43a5bd224a212409b00228c26654432b715223eb0d6da4',
          'source_input_review_sha256':'c068b0d4d82a7f65d32adde62c48cf2fa22173d350754c372deb2e6c6e440f14',
          'terminal_sha256':'e32cfe071bb5f161df795528432f8c0170ca85b2976cff1412b3535a69df1d5d',
          'stdout_sha256':'aceb68ac8ec9574c9d04728fa669363d90ed389e8f9c1368ad000c8638f364bf',
          'complete_field_count':46292,'selected_game_function_candidates':14555,'iat_field_count':416,'binding_rows':29428,
          'application_cohort_adopted':False,'native_tools_run':False,'runtime_eligible':False}
        m._validate_observation_peer(peer)
        with self.assertRaises(ValueError):m._validate_observation_peer(dict(peer,schema_version=True))
        with self.assertRaises(ValueError):m._validate_observation_peer(dict(peer,fields_sha256='f'*64))



class InputAssemblyTest(unittest.TestCase):
    def test_each_inherited_ledger_rechecked_and_preserved(self):
        import gzip,hashlib,json,tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(m,'ROOT',pathlib.Path(tmp)):
            b=m.ROOT/'build'/'rebuild';b.mkdir(parents=True)
            paths={'iat_kernel':'kernel.lib','iat_user32':'user.lib','iat_provider000':'a.lib','iat_provider002':'b.lib'}
            payload=b'authored archive';h=hashlib.sha256(payload).hexdigest()
            refs={key:{'path':'build/rebuild/'+name,'sha256':h} for key,name in paths.items()}
            refs.update({'iat_ancestry_catalog':{'path':'build/rebuild/catalog.json','sha256':'a'*64},
               'iat_request':{'path':'build/rebuild/request.json','sha256':'b'*64},
               'iat_native':{'path':'build/rebuild/native.json','sha256':'c'*64}})
            bindings=[{'requested_path':str(b/name),'path':str(b/name),'sha256':h} for name in paths.values()]
            report={'input_bindings':bindings+[{}]*(18669-len(bindings))}
            raw={key:payload for key in paths}
            raw.update(v13_report=json.dumps(report).encode(),v13_observation=json.dumps({'input_bindings':[{}]*10667}).encode(),
              v14_observation=json.dumps({'input_bindings':[{}]*29428}).encode(),v14_observation_peer=b'{}',crt_consumer_peer=b'{}',
              v13_fields=gzip.compress(b'[]'),v14_fields=gzip.compress(b'[]'),iat_ancestry_catalog=b'{}',
              iat_native=b'{}',iat_request=b'{}',crt_plan=b'{}',crt_review=b'{}',crt_response=b'',
              baseline_response=('\n'.join('"'+str(b/name)+'"' for name in paths.values())).encode())
            old=SimpleNamespace(IMPORT_ANCESTRY={'catalog':'build/rebuild/catalog.json'},
               INPUT_PATHS={'import_request':'build/rebuild/request.json','import_native':'build/rebuild/native.json',
                            'kernel_library':'build/rebuild/kernel.lib'},
               import_archive=SimpleNamespace(read_archive=lambda path:{'archive_sha256':h}))
            producer=SimpleNamespace(PINS={'catalog':'a'*64},HELPER_PINS={})
            diag=SimpleNamespace(stable=lambda x:None,partial=SimpleNamespace(native_archive=lambda x:{}))
            phases=[];utility=SimpleNamespace(stable_phase=lambda ledger,**kw:phases.append(len(ledger)))
            state={'raw':raw,'bindings':[],'guard':lambda:None,'stable_utility':utility}
            mods={'diagnostic':diag,'import34':old,'producer':producer,'uuid':SimpleNamespace(PINS={})}
            sources={'import_kernel32_fifteen':{'path':'tools/rebuild/import_kernel32_fifteen.py','sha256':'d'*64}}
            with mock.patch.object(m,'FIXED_INPUTS',refs),mock.patch.object(m,'SOURCE_PINS',sources),mock.patch.object(m,'_validate_observation_peer'),mock.patch.object(m,'_validate_crt_consumer_peer'):
                result=m._load_semantics(state,mods)
            self.assertEqual(phases,[18669,10667,29428]);self.assertEqual(len(state['bindings']),58764)
            self.assertEqual(set(result['iat_libraries']),{'kernel32-fifteen.lib','user32-sixteen.lib','provider-000.lib','provider-002.lib'})



class CRTPeerTest(unittest.TestCase):
    def test_consumer_peer_exact_scope(self):
        peer={'kind':'V14-existing-four-CRT-pure-consumer-review','status':'approved','reviewer':'crt_lane_04',
          'plan_sha256':'e832d09148559e859cb4358530407edb0be39fa678d5ad4e0c524dc587e2a7be',
          'review_sha256':'e18ef6adc4c878240c4daad02e1d2fbaaed925a59740916ad298569d548f9e25',
          'response_sha256':'aaec970cae1dcf32699bda75317afbbcd4551c67252fca0d508d47eec997024a',
          'complete_input_fields':46292,'potential_alias_field_count':204,'enabled_alias_field_count':204,
          'enabled_alias_count':4,'inherited_tokens_to_remove_count':4,'alias_use_counts':[103,97,1,3],
          'actual_full_field_validation':True,'actual_namespace_validation':True,'actual_cookie_collision_rejected':True,
          'unapproved_framehandler_dynamiccast_unaliased':True,'qualified_UUID_negative_flags_preserved':True,
          'third_own_source_bound':True,'allow_native':False,'allow_game_execution':False,'runtime_ABI_approved':False}
        m._validate_crt_consumer_peer(peer)
        with self.assertRaises(ValueError):m._validate_crt_consumer_peer(dict(peer,enabled_alias_count=True))
        with self.assertRaises(ValueError):m._validate_crt_consumer_peer(dict(peer,alias_use_counts=[103,97,1,2]))



class StdlibOriginTest(unittest.TestCase):
    def test_stdlib_name_from_untrusted_site_package_rejected(self):
        import importlib.machinery,tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as tmp:
            root=pathlib.Path(tmp);external=root/'site-packages'/'json.py'
            spec=importlib.machinery.ModuleSpec('json',loader=None,origin=str(external))
            finder=m._SnapshotFinder({'_fixture':b'x=1\n'},{'_fixture':str(root/'ok.py')},root/'workspace')
            with mock.patch.object(importlib.machinery.PathFinder,'find_spec',return_value=spec):
                with self.assertRaisesRegex(ImportError,'stdlib origin'):
                    finder.find_spec('json')



class ActualCRTPlanShapeTest(unittest.TestCase):
    def test_all_four_inherited_plan_tests_are_bound(self):
        expected={
          'tests/rebuild/test_crt_v8_four_alias_plan.py':'747bca44a7c8c41ae74cc38bc145d7d1c5f4516130d5a77e58ddc7efe79d6ec0',
          'tests/rebuild/test_crt_v9_four_alias_plan.py':'00a1c7ffb348cb8f05e9839756e4e3484bdb4cc5ab6de12e3d2183d9957eb3ea',
          'tests/rebuild/test_crt_v10_four_alias_plan.py':'ea52bccf6ed00d82a7162a22112fc106869362993f2d1920675f18980c17a94d',
          'tests/rebuild/test_crt_v13_four_alias_plan.py':'b3faba93a02bd47b25849c69d22343685e9fd36602c6419dc5f80dd4f1b818d3'}
        paths={row['path']:row['sha256'] for row in m.FIXED_INPUTS.values()}
        self.assertTrue(all(paths.get(path)==sha for path,sha in expected.items()))
        plan={'sources':expected,'inputs':{'field.json':'x'},'own_sources':{'src/a.cpp':'y'},
              'units_sha256':paths['build/units.json']}
        fixtures={'field':{'path':'build/rebuild/field.json','sha256':'x'},
                  'own':{'path':'src/a.cpp','sha256':'y'},
                  'units':{'path':'build/units.json','sha256':paths['build/units.json']}}
        m._validate_crt_bound_inputs(plan,m.FIXED_INPUTS,fixtures)
        for omitted in expected:
            missing={k:v for k,v in m.FIXED_INPUTS.items() if v['path']!=omitted}
            with self.assertRaisesRegex(ValueError,'not bound'):
                m._validate_crt_bound_inputs(plan,missing,fixtures)

if __name__=='__main__':unittest.main()

