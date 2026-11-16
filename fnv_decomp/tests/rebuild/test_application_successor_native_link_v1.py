import copy
from datetime import datetime, timedelta, timezone
import importlib.util
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('native_link_fixture',ROOT/'tools/rebuild/application_successor_native_link_v1.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.folder=Path(self.tmp.name)/'once'
        self.now=datetime.now(timezone.utc);self.response=b'fixture response'
        self.identity={'requested_path':'link.exe','path':'link.exe','sha256':'a'*64,'size':1,'device':1,'inode':1}
        self.binding={'requested_path':'input','path':'input','sha256':'b'*64,'size':1,'device':1,'inode':2}
        row={'owner':'owner','resource':'CPU_heavy','slot':1,'state':'running',
             'granted_utc':(self.now-timedelta(seconds=1)).isoformat(),'max_seconds':60,'request':'c'*64}
        self.registry={'schema_version':1,'CPU_heavy_capacity':2,'leases':[row]}
        lease_sha=m.sha(m.canonical({k:v for k,v in row.items() if k!='state'}))
        self.profile={'kind':'successor-diagnostic-native-link','version':1,
          'operation':{'id':'fixture','linker_identity':self.identity,'command':['link.exe','@link.rsp'],'working_directory':'out'},
          'response':{'path':'link.rsp','sha256':m.sha(self.response)},
          'preparation':{'manifest_sha256':'d'*64,'semantic_sha256':'e'*64,'publication_sha256':'f'*64,
                         'preparation_terminal_sha256':'0'*64,'input_bindings':[self.binding]},
          'source_pins':{'source':'1'*64},'runtime_pins':{'runtime':'2'*64},
          'peer_pins':{'preparation':'3'*64,'semantic':'4'*64,'operation':'5'*64,'watchdog':'6'*64},
          'watchdog':{'source_sha256':'7'*64,'protocol_sha256':'8'*64},
          'lease':{'owner':'owner','resource':'CPU_heavy','slot':1,'row_sha256':lease_sha},
          'outputs':{'stdout':'out.log','stderr':'err.log','executable':'diag.exe','map':'diag.map'}}
        self.parent={'pid':1,'creation':100,'image':'python'};self.child={'pid':2,'creation':200,'image':'link.exe'}
        self.watch={'kind':'successor-link-watchdog-started','profile_sha256':m.sha(m.canonical(self.profile)),
                    'parent':self.parent,'child':self.child,'job':'job-fixture','nonce':'9'*64}
        self.observed={'parent':self.parent,'child':self.child,'job':'job-fixture'}
    def test_hard_disabled(self):
        with self.assertRaises(RuntimeError):m.run()
    def test_lease_pid_and_unchanged_response(self):
        m._validate_profile(self.profile);lease=m._lease_fixture(self.profile,self.registry,self.now)
        m._watchdog_fixture(self.profile,self.watch,self.observed)
        m._response_fixture(self.profile,self.response,[self.binding])
        with self.assertRaises(ValueError):m._lease_fixture(self.profile,self.registry,self.now+timedelta(seconds=60))
        stale=copy.deepcopy(self.observed);stale['child']['creation']+=1
        with self.assertRaises(ValueError):m._watchdog_fixture(self.profile,self.watch,stale)
        with self.assertRaises(ValueError):m._response_fixture(self.profile,b'changed',[self.binding])
        self.assertEqual(lease['owner'],'owner')
    def test_once_unknown_and_terminal_no_replay(self):
        lease=m._lease_fixture(self.profile,self.registry,self.now);watch=m._watchdog_fixture(self.profile,self.watch,self.observed)
        intent=m._begin_fixture(self.folder,self.profile,self.response,[self.binding],lease,watch)
        with self.assertRaises(ValueError):m._begin_fixture(self.folder,self.profile,self.response,[self.binding],lease,watch)
        result={'returncode':1,'stdout_sha256':'a'*64,'stderr_sha256':'b'*64,'timed_out':False}
        changed=copy.deepcopy(watch);changed['child']['creation']+=1
        with self.assertRaises(ValueError):m._finish_fixture(self.folder,self.profile,intent,self.response,[self.binding],lease,changed,result)
        m._finish_fixture(self.folder,self.profile,intent,self.response,[self.binding],lease,watch,result)
        with self.assertRaises(FileExistsError):m._finish_fixture(self.folder,self.profile,intent,self.response,[self.binding],lease,watch,result)
    def test_independent_peers_and_scope_cannot_be_omitted(self):
        for field in ('preparation','semantic','operation','watchdog'):
            profile=copy.deepcopy(self.profile);del profile['peer_pins'][field]
            with self.assertRaises(ValueError):m._validate_profile(profile)
        profile=copy.deepcopy(self.profile);profile['operation']['command'].append('/alter')
        with self.assertRaises(ValueError):m._validate_profile(profile)
        profile=copy.deepcopy(self.profile);profile['lease']['slot']=True
        with self.assertRaises(ValueError):m._validate_profile(profile)
    def test_timeout_cannot_be_terminal_success(self):
        lease=m._lease_fixture(self.profile,self.registry,self.now);watch=m._watchdog_fixture(self.profile,self.watch,self.observed)
        intent=m._begin_fixture(self.folder,self.profile,self.response,[self.binding],lease,watch)
        with self.assertRaises(ValueError):m._finish_fixture(self.folder,self.profile,intent,self.response,[self.binding],lease,watch,
             {'returncode':1,'stdout_sha256':'a'*64,'stderr_sha256':'b'*64,'timed_out':True})
        self.assertFalse((self.folder/'terminal.json').exists())

if __name__=='__main__':unittest.main()
