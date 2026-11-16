import copy
from datetime import datetime, timedelta, timezone
import importlib.util
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('native_link_fixture',ROOT/'tools/rebuild/application_successor_native_link_v3.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.folder=Path(self.tmp.name)/'once'
        self.now=datetime.now(timezone.utc);self.response=b'fixture response'
        self.identity={'requested_path':r'C:\fixture\bin\link.exe','path':r'C:\fixture\bin\link.exe','sha256':'a'*64,'size':1,'device':1,'inode':1}
        self.binding={'requested_path':r'C:\fixture\input.obj','path':r'C:\fixture\input.obj','sha256':'b'*64,'size':1,'device':1,'inode':2}
        row={'owner':'owner','resource':'CPU_heavy','slot':1,'state':'running',
             'granted_utc':(self.now-timedelta(seconds=1)).isoformat(),'max_seconds':60,'request':'c'*64}
        self.registry={'schema_version':1,'CPU_heavy_capacity':2,'leases':[row]}
        lease_sha=m.sha(m.canonical({k:v for k,v in row.items() if k!='state'}))
        self.profile={'kind':'successor-diagnostic-native-link','version':1,
          'operation':{'id':'fixture','linker_identity':self.identity,'command':[r'C:\fixture\bin\link.exe',r'@C:\fixture\link.rsp'],'working_directory':r'C:\fixture','control_directory':str(self.folder)},
          'response':{'path':r'C:\fixture\link.rsp','sha256':m.sha(self.response)},
          'preparation':{'manifest_sha256':'d'*64,'semantic_sha256':'e'*64,'publication_sha256':'f'*64,
                         'preparation_terminal_sha256':'0'*64,'input_bindings':[self.binding]},
          'source_pins':{r'C:\fixture\src.py':'1'*64},'runtime_pins':{r'C:\fixture\python.exe':'2'*64},
          'peer_pins':{'preparation':'3'*64,'semantic':'4'*64,'operation':'5'*64,'watchdog':'6'*64},
          'watchdog':{'source_sha256':'7'*64,'protocol_sha256':'8'*64},
          'lease':{'owner':'owner','resource':'CPU_heavy','slot':1,'row_sha256':lease_sha},
          'outputs':{'stdout':r'C:\fixture\out.log','stderr':r'C:\fixture\err.log','executable':r'C:\fixture\diag.exe','map':r'C:\fixture\diag.map'}}
        self.parent={'pid':1,'creation':100,'image':'python'};self.child={'pid':2,'creation':200,'image':r'C:\fixture\bin\link.exe'}
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
        intent=m._begin_fixture(self.folder,self.profile,self.response,[self.binding],self.registry,self.now,watch,self.observed)
        with self.assertRaises(ValueError):m._begin_fixture(self.folder,self.profile,self.response,[self.binding],self.registry,self.now,watch,self.observed)
        result={'returncode':1,'stdout_sha256':'a'*64,'stderr_sha256':'b'*64,'timed_out':False}
        changed=copy.deepcopy(watch);changed['child']['creation']+=1
        with self.assertRaises(ValueError):m._finish_fixture(self.folder,self.profile,intent,self.response,[self.binding],self.registry,self.now,changed,self.observed,result)
        m._finish_fixture(self.folder,self.profile,intent,self.response,[self.binding],self.registry,self.now,watch,self.observed,result)
        with self.assertRaises(FileExistsError):m._finish_fixture(self.folder,self.profile,intent,self.response,[self.binding],self.registry,self.now,watch,self.observed,result)
    def test_independent_peers_and_scope_cannot_be_omitted(self):
        for field in ('preparation','semantic','operation','watchdog'):
            profile=copy.deepcopy(self.profile);del profile['peer_pins'][field]
            with self.assertRaises(ValueError):m._validate_profile(profile)
        profile=copy.deepcopy(self.profile);profile['operation']['command'].append('/alter')
        with self.assertRaises(ValueError):m._validate_profile(profile)
        profile=copy.deepcopy(self.profile);profile['lease']['slot']=True
        with self.assertRaises(ValueError):m._validate_profile(profile)
    def test_missing_live_guards_block_begin_and_finish(self):
        for registry,watch,observed in ((None,self.watch,self.observed),(self.registry,None,self.observed),
                                        (self.registry,self.watch,None)):
            with self.subTest(registry=registry is None,watch=watch is None,observed=observed is None):
                with self.assertRaises(ValueError):
                    m._begin_fixture(self.folder,self.profile,self.response,[self.binding],registry,self.now,watch,observed)
                self.assertFalse(self.folder.exists())
        intent=m._begin_fixture(self.folder,self.profile,self.response,[self.binding],self.registry,self.now,self.watch,self.observed)
        result={'returncode':1,'stdout_sha256':'a'*64,'stderr_sha256':'b'*64,'timed_out':False}
        for registry,now,watch,observed in ((None,self.now,self.watch,self.observed),
                                             (self.registry,self.now+timedelta(seconds=60),self.watch,self.observed),
                                             (self.registry,self.now,None,self.observed),
                                             (self.registry,self.now,self.watch,None)):
            with self.assertRaises(ValueError):
                m._finish_fixture(self.folder,self.profile,intent,self.response,[self.binding],registry,now,watch,observed,result)
        self.assertFalse((self.folder/'terminal.json').exists())

    def test_global_slot_collision_and_capacity_rejected(self):
        other=copy.deepcopy(self.registry['leases'][0]);other['owner']='other'
        collision=copy.deepcopy(self.registry);collision['leases'].append(other)
        with self.assertRaisesRegex(ValueError,'collision or capacity'):m._lease_fixture(self.profile,collision,self.now)
        with self.assertRaises(ValueError):m._begin_fixture(self.folder,self.profile,self.response,[self.binding],collision,self.now,self.watch,self.observed)
        intent=m._begin_fixture(self.folder,self.profile,self.response,[self.binding],self.registry,self.now,self.watch,self.observed)
        result={'returncode':1,'stdout_sha256':'a'*64,'stderr_sha256':'b'*64,'timed_out':False}
        with self.assertRaises(ValueError):m._finish_fixture(self.folder,self.profile,intent,self.response,[self.binding],collision,self.now,self.watch,self.observed,result)
        self.assertFalse((self.folder/'terminal.json').exists())
        other['slot']=2;other2=copy.deepcopy(other);other2['owner']='third'
        capacity=copy.deepcopy(self.registry);capacity['leases'].extend([other,other2])
        with self.assertRaisesRegex(ValueError,'collision or capacity'):m._lease_fixture(self.profile,capacity,self.now)
        collision=copy.deepcopy(self.registry);collision['leases'].append(dict(other,slot=True))
        with self.assertRaisesRegex(ValueError,'collision or capacity'):m._lease_fixture(self.profile,collision,self.now)

    def test_output_and_control_protected_path_aliases_rejected(self):
        for category,alias in (('response',r'c:/FIXTURE/./LINK.RSP'),('input',r'C:\fixture\INPUT.obj'),
                               ('source',r'C:\fixture\SRC.py'),('runtime',r'C:\fixture\PYTHON.EXE'),
                               ('linker',r'C:\fixture\bin\LINK.EXE')):
            for target in ('stdout','control_directory'):
                profile=copy.deepcopy(self.profile)
                if target=='stdout':profile['outputs'][target]=alias
                else:profile['operation'][target]=alias
                with self.subTest(category=category,target=target),self.assertRaises(ValueError):m._validate_profile(profile)
        profile=copy.deepcopy(self.profile);profile['outputs']['stdout']=r'C:\fixture\OUT.log'
        profile['outputs']['stderr']=r'c:/fixture/./out.LOG'
        with self.assertRaises(ValueError):m._validate_profile(profile)
        profile=copy.deepcopy(self.profile);profile['outputs']['stdout']=str(self.folder / 'log.txt')
        with self.assertRaises(ValueError):m._validate_profile(profile)

    def test_ambiguous_windows_alias_forms_rejected(self):
        for alias in (r'C:\fixture\link.rsp.',r'C:\fixture\link.rsp ',
                      r'\\?\C:\fixture\link.rsp',r'\\.\C:\fixture\link.rsp',
                      r'C:\fixture\foo\..\link.rsp',r'C:\fixture\link.rsp:stream'):
            profile=copy.deepcopy(self.profile);profile['outputs']['stdout']=alias
            with self.subTest(alias=alias),self.assertRaises(ValueError):m._validate_profile(profile)

    def test_begin_finish_require_exact_control_folder(self):
        other=self.folder.parent/'other'
        with self.assertRaisesRegex(ValueError,'control directory differs'):
            m._begin_fixture(other,self.profile,self.response,[self.binding],self.registry,self.now,self.watch,self.observed)
        self.assertFalse(other.exists())
        intent=m._begin_fixture(self.folder,self.profile,self.response,[self.binding],self.registry,self.now,self.watch,self.observed)
        result={'returncode':1,'stdout_sha256':'a'*64,'stderr_sha256':'b'*64,'timed_out':False}
        with self.assertRaisesRegex(ValueError,'control directory differs'):
            m._finish_fixture(other,self.profile,intent,self.response,[self.binding],self.registry,self.now,self.watch,self.observed,result)
        self.assertFalse((self.folder/'terminal.json').exists())

    def test_timeout_cannot_be_terminal_success(self):
        lease=m._lease_fixture(self.profile,self.registry,self.now);watch=m._watchdog_fixture(self.profile,self.watch,self.observed)
        intent=m._begin_fixture(self.folder,self.profile,self.response,[self.binding],self.registry,self.now,watch,self.observed)
        with self.assertRaises(ValueError):m._finish_fixture(self.folder,self.profile,intent,self.response,[self.binding],self.registry,self.now,watch,self.observed,
             {'returncode':1,'stdout_sha256':'a'*64,'stderr_sha256':'b'*64,'timed_out':True})
        self.assertFalse((self.folder/'terminal.json').exists())

if __name__=='__main__':unittest.main()
