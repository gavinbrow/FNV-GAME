import copy
from datetime import datetime, timedelta, timezone
import os
import importlib.util
from pathlib import Path
import tempfile
import unittest
import sys
import types

ROOT=Path(__file__).resolve().parents[2]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path); module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module);return module
m=load('fixed_fixture','tools/rebuild/application_successor_fixed_v3.py')
v=load('v5_fixture','tools/rebuild/application_successor_operation_v7.py')

class Tests(unittest.TestCase):
    def setUp(self):
        self.old={k:getattr(m,k) for k in ('ROOT','PINNED_POLICY','BOOTSTRAP_PIN','WRAPPER_PIN','INTERPRETER_PIN','STDLIB_ROOT','PROCESS_RUNTIME_PIN','REQUIRED_ROLE_PINS')}
        self.addCleanup(self.restore)
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        m.ROOT=self.root
        self.old_main=sys.modules['__main__'];self.addCleanup(sys.modules.__setitem__,'__main__',self.old_main)
        main=types.ModuleType('__main__');main.__file__=str(self.root/'tools/rebuild/application_successor_fixed_v3.py')
        sys.modules['__main__']=main
    def restore(self):
        for k,value in self.old.items():setattr(m,k,value)
    def put(self,name,data):
        p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        return {'path':name,'sha256':v.digest(data)}
    def policy(self):
        m.BOOTSTRAP_PIN=self.put('tools/rebuild/application_successor_operation_v7.py',
                                  (ROOT/'tools/rebuild/application_successor_operation_v7.py').read_bytes())
        m.WRAPPER_PIN=self.put('tools/rebuild/application_successor_fixed_v3.py',b'fixture main')
        m.INTERPRETER_PIN={'pending':'fixture'};m.PROCESS_RUNTIME_PIN={'pending':'fixture'};m.STDLIB_ROOT=str(Path(__file__).anchor)
        diagnostic=self.put('tools/rebuild/application_link_diagnostic.py',b'def stable(rows): pass\n')
        stability=self.put('tools/rebuild/exact_binding_stability.py',b'def stable_phase(*a, **k): pass\n')
        resource=self.put('resource',b'fixture');m.REQUIRED_ROLE_PINS=(('resource',copy.deepcopy(resource)),);ledger=[];v.read_bound(self.root,resource,ledger)
        operation={'id':'fixture','journal':'journal','phases':[{'name':'one','artifact':'one'}],
                   'lease':{},'watchdog':{},'input_bindings':ledger}
        manifest={'kind':'successor-operation-manifest','version':1,
                  'sources':{'runtime':m.BOOTSTRAP_PIN,'application_link_diagnostic':diagnostic,'exact_binding_stability':stability},
                  'inputs':[{'role':'resource','pin':resource}],'operation':operation}
        manifest_ref=self.put('manifest',v.canonical(manifest)); reviews={};reviewers={}
        for scope,key in (('source','sources'),('input','inputs'),('operation','operation')):
            reviewers[scope]=scope+'-reviewer'
            record={'kind':'successor-independent-review','scope':scope,'reviewer':reviewers[scope],
                    'manifest_sha256':manifest_ref['sha256'],'subject_sha256':v.digest(v.canonical(manifest[key]))}
            reviews[scope]=self.put(scope,v.canonical(record))
        m.PINNED_POLICY={'manifest':manifest_ref,'reviews':reviews,'expected':manifest,'reviewers':reviewers}
        return manifest
    def test_unconfigured_entry_closed(self):
        m.PINNED_POLICY=None
        with self.assertRaises(ValueError):m.run()
    def test_valid_fixture_stops_at_process_gate_without_journal(self):
        self.policy();state=m._startup();self.assertEqual(state[2],{'resource':b'fixture'})
        with self.assertRaisesRegex(RuntimeError,'process runtime loader'):m.run()
        self.assertFalse((self.root/'journal').exists())
    def test_tampered_input_or_review_rejected(self):
        self.policy();(self.root/'resource').write_bytes(b'changed')
        with self.assertRaises(ValueError):m._startup()
        self.policy();(self.root/'operation').write_bytes(b'{}')
        with self.assertRaises(ValueError):m._startup()
    def test_roles_and_ledger_not_caller_approval(self):
        manifest=self.policy();bad=copy.deepcopy(manifest)
        bad['inputs'].append(copy.deepcopy(bad['inputs'][0]))
        with self.assertRaises(ValueError):m._validate_roles(bad,m.BOOTSTRAP_PIN['sha256'])
        bad=copy.deepcopy(manifest);bad['sources']['application_link_diagnostic']['path']='other.py'
        with self.assertRaises(ValueError):m._validate_roles(bad,m.BOOTSTRAP_PIN['sha256'])
        manifest['operation']['input_bindings'][0]['sha256']='0'*64
        with self.assertRaises(ValueError):m._startup()
    def test_synthetic_guarded_wiring_and_no_replay(self):
        manifest=self.policy(); nonce='a'*64;os.environ['FNV_FIXED_TEST_NONCE']=nonce
        self.addCleanup(os.environ.pop,'FNV_FIXED_TEST_NONCE',None)
        class Process:
            pid=os.getpid()
            def ppid(self):return os.getppid()
            def create_time(self):return 123.0
            def exe(self):return 'fixture-python'
        stable=self.put('tools/rebuild/exact_binding_stability.py',
                        (ROOT/'tools/rebuild/exact_binding_stability.py').read_bytes())
        manifest['sources']['exact_binding_stability']=stable
        child={'pid':os.getpid(),'parent_pid':os.getppid(),'create_time':123.0,'executable':'fixture-python'}
        record={'kind':'successor-watchdog-started','child':child,'pins':{'request':'b'*64},'slot':1,'nonce':nonce}
        watch=self.put('watch',v.canonical(record))
        lease={'lock':'lock','registry':'registry','owner':'owner','resource':'cpu','slot':1,
               'input_pins':{'request':'b'*64},'review_sha256':'c'*64}
        row={k:lease[k] for k in ('owner','resource','slot','input_pins','review_sha256')}
        row.update(state='running',granted_utc=(datetime.now(timezone.utc)-timedelta(seconds=1)).isoformat(),max_seconds=60)
        self.put('registry',v.canonical({'schema_version':1,'leases':[row]}))
        manifest['operation']['lease']=lease
        manifest['operation']['watchdog']={'record':'watch','record_sha256':watch['sha256'],
             'nonce_env':'FNV_FIXED_TEST_NONCE','executable':'fixture-python','pins':record['pins']}
        manifest_ref=self.put('manifest',v.canonical(manifest));reviews={};reviewers={}
        for scope,key in (('source','sources'),('input','inputs'),('operation','operation')):
            reviewers[scope]=scope+'-reviewer'
            reviews[scope]=self.put(scope,v.canonical({'kind':'successor-independent-review','scope':scope,
                  'reviewer':reviewers[scope],'manifest_sha256':manifest_ref['sha256'],
                  'subject_sha256':v.digest(v.canonical(manifest[key]))}))
        m.PINNED_POLICY={'manifest':manifest_ref,'reviews':reviews,'expected':manifest,'reviewers':reviewers}
        state=m._startup();m._perform(state,Process())
        self.assertTrue((self.root/'journal'/'terminal.json').is_file())
        with self.assertRaises(ValueError):m._perform(m._startup(),Process())

    def test_hostile_workspace_preload_and_main_tamper_rejected(self):
        self.policy(); self.assertIsNotNone(m._startup())
        hostile=types.ModuleType('hostile_fixture');hostile.__file__=str(self.root/'hostile.py')
        sys.modules['hostile_fixture']=hostile
        try:
            with self.assertRaisesRegex(ValueError,'workspace module preloaded'):m._startup()
        finally:sys.modules.pop('hostile_fixture',None)
        sys.modules['__main__'].__file__=str(self.root/'other.py')
        with self.assertRaisesRegex(ValueError,'main wrapper identity'):m._startup()
        sys.modules['__main__'].__file__=str(self.root/'tools/rebuild/application_successor_fixed_v3.py')
        (self.root/m.WRAPPER_PIN['path']).write_bytes(b'changed')
        with self.assertRaises(ValueError):m._startup()

    def test_closed_roles_reject_missing_extra_substitute_path_and_hash(self):
        original=self.policy();runtime_sha=m.BOOTSTRAP_PIN['sha256']
        variants=[]
        x=copy.deepcopy(original);x['inputs']=[];variants.append(x)
        x=copy.deepcopy(original);x['inputs'].append({'role':'extra','pin':{'path':'extra.lib','sha256':'a'*64}});variants.append(x)
        x=copy.deepcopy(original);x['inputs'][0]['role']='other_archive';variants.append(x)
        x=copy.deepcopy(original);x['inputs'][0]['pin']['path']='substitute.lib';variants.append(x)
        x=copy.deepcopy(original);x['inputs'][0]['pin']['sha256']='b'*64;variants.append(x)
        for value in variants:
            with self.subTest(value=value['inputs']):
                with self.assertRaises(ValueError):m._validate_roles(value,runtime_sha)
        m.REQUIRED_ROLE_PINS=None
        with self.assertRaises(ValueError):m._startup()

    def test_bootstrap_pin_tamper_rejected(self):
        self.policy();(self.root/m.BOOTSTRAP_PIN['path']).write_text('pass')
        with self.assertRaises(ValueError):m._startup()

if __name__=='__main__':unittest.main()
