import copy
from datetime import datetime, timedelta, timezone
import importlib
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
m=load('successor3','tools/rebuild/application_successor_operation_v4.py')
stable=load('stability3','tools/rebuild/exact_binding_stability.py')

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
    def put(self,name,data):
        path=self.root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
        return {'path':name,'sha256':m.digest(data)}
    def operation(self):
        return {'id':'fixture','journal':'journal','phases':[{'name':'one','artifact':'one.json'},
                {'name':'two','artifact':'two.json'}], 'lease':{},'watchdog':{}}
    def test_review_manifest_and_change(self):
        manifest={'kind':'successor-operation-manifest','version':1,'sources':{'a':{'path':'a','sha256':'a'*64}},
                  'inputs':{'b':{'path':'b','sha256':'b'*64}},'operation':self.operation()}
        ref=self.put('manifest',m.canonical(manifest));reviews={};reviewers={}
        for scope,key in (('source','sources'),('input','inputs'),('operation','operation')):
            reviewers[scope]=scope+'-reviewer'
            review={'kind':'successor-independent-review','scope':scope,'reviewer':reviewers[scope],
                    'manifest_sha256':ref['sha256'],'subject_sha256':m.digest(m.canonical(manifest[key]))}
            reviews[scope]=self.put(scope,m.canonical(review))
        policy={'manifest':ref,'reviews':reviews,'expected':manifest,'reviewers':reviewers}
        ledger=[];self.assertEqual(m.verify_manifest(self.root,policy,ledger),manifest);self.assertEqual(len(ledger),4)
        (self.root/'source').write_bytes(b'{}')
        with self.assertRaises(ValueError):m.verify_manifest(self.root,policy,[])
        bad=copy.deepcopy(policy);bad['reviewers']['input']=bad['reviewers']['source']
        with self.assertRaises(ValueError):m.verify_manifest(self.root,bad,[])
    def test_source_snapshot_and_finder(self):
        ref=self.put('x.py',b'value=42\n');finder=m.source_finder(self.root,{'fixture_unique_mod':ref},[],Path(sys.base_prefix))
        (self.root/'x.py').write_bytes(b'value=99\n')
        with m.SnapshotSession(finder):
            module=importlib.import_module('fixture_unique_mod');self.assertEqual(module.value,42)
            with self.assertRaises(ValueError):finder.find_spec('unreviewed_external_xyz')
        self.assertNotIn('fixture_unique_mod',sys.modules)
    def test_lease_watchdog_expiry_and_identity(self):
        now=datetime.now(timezone.utc);nonce='a'*64;os.environ['FNV_TEST_NONCE_3']=nonce
        self.addCleanup(os.environ.pop,'FNV_TEST_NONCE_3',None)
        class Proc:
            pid=os.getpid()
            def ppid(self):return os.getppid()
            def create_time(self):return 123.0
            def exe(self):return 'fixture-python'
        child={'pid':os.getpid(),'parent_pid':os.getppid(),'create_time':123.0,'executable':'fixture-python'}
        record={'kind':'successor-watchdog-started','child':child,'pins':{'m':'b'*64},'slot':1,'nonce':nonce}
        ref=self.put('watch',m.canonical(record))
        lease={'lock':'lock','registry':'registry','owner':'owner','resource':'cpu','slot':1,
               'input_pins':{'request':'c'*64},'review_sha256':'d'*64}
        row={k:lease[k] for k in ('owner','resource','slot','input_pins','review_sha256')}
        row.update(state='running',granted_utc=(now-timedelta(seconds=1)).isoformat(),max_seconds=60)
        self.put('registry',m.canonical({'schema_version':1,'leases':[row]}))
        op={'lease':lease,'watchdog':{'record':'watch','record_sha256':ref['sha256'],
            'nonce_env':'FNV_TEST_NONCE_3','executable':'fixture-python','pins':record['pins']}}
        self.assertEqual(m.lease_watchdog(self.root,op,Proc(),now)['child'],child)
        with self.assertRaises(ValueError):m.lease_watchdog(self.root,op,Proc(),now+timedelta(seconds=60))
        (self.root/'lock').touch()
        with self.assertRaises(ValueError):m.lease_watchdog(self.root,op,Proc(),now)
    def test_journal_phase_full_ledger_no_replay(self):
        op=self.operation();calls=[];guard=lambda:None
        row={'requested_path':'a','path':'a','sha256':'a'*64,'size':1,'device':1,'inode':1};ledger=[row,row.copy()]
        sha=m.begin(self.root,op,'f'*64,guard)
        with self.assertRaises(ValueError):m.begin(self.root,op,'f'*64,guard)
        with self.assertRaises((ValueError,FileNotFoundError)):m.phase(self.root,op,1,ledger,stable.stable_phase,lambda x:None,guard,sha)
        for i in range(2):m.phase(self.root,op,i,ledger,stable.stable_phase,lambda x:calls.append(copy.deepcopy(x)),guard,sha)
        self.assertEqual(len(calls),4);self.assertTrue(all(len(c)==1 for c in calls))
        result=m.parse((self.root/'one.json').read_bytes());self.assertEqual(result['input_bindings'],ledger)
        m.finish(self.root,op,sha,guard)
        with self.assertRaises(FileExistsError):m.finish(self.root,op,sha,guard)
        with self.assertRaises(ValueError):m.phase(self.root,op,0,ledger,stable.stable_phase,lambda x:None,guard,sha)
    def test_changed_operation_cannot_skip_or_redirect_phases(self):
        op=self.operation(); guard=lambda:None
        sha=m.begin(self.root,op,'f'*64,guard)
        row={'requested_path':'a','path':'a','sha256':'a'*64,'size':1,'device':1,'inode':1}
        empty=copy.deepcopy(op);empty['phases']=[]
        with self.assertRaises(ValueError):m.finish(self.root,empty,sha,guard)
        truncated=copy.deepcopy(op);truncated['phases']=truncated['phases'][:1]
        with self.assertRaises(ValueError):m.phase(self.root,truncated,0,[row],stable.stable_phase,lambda x:None,guard,sha)
        redirected=copy.deepcopy(op);redirected['phases'][0]['artifact']='other.json'
        with self.assertRaises(ValueError):m.phase(self.root,redirected,0,[row],stable.stable_phase,lambda x:None,guard,sha)
        changed=copy.deepcopy(op);changed['lease']={'owner':'other'}
        with self.assertRaises(ValueError):m.finish(self.root,changed,sha,guard)
        self.assertFalse((self.root/'journal'/'terminal.json').exists())
        self.assertFalse((self.root/'other.json').exists())

    def test_begin_rejects_empty_operation(self):
        op=self.operation();op['phases']=[]
        with self.assertRaises(ValueError):m.begin(self.root,op,'f'*64,lambda:None)
        self.assertFalse((self.root/'journal').exists())

    def test_changed_artifact_blocks_completion(self):
        op=self.operation();sha=m.begin(self.root,op,'f'*64,lambda:None)
        row={'requested_path':'a','path':'a','sha256':'a'*64,'size':1,'device':1,'inode':1}
        for i in range(2):m.phase(self.root,op,i,[row],stable.stable_phase,lambda x:None,lambda:None,sha)
        (self.root/'one.json').write_text('{}')
        with self.assertRaises(ValueError):m.finish(self.root,op,sha,lambda:None)

if __name__=='__main__':unittest.main()
