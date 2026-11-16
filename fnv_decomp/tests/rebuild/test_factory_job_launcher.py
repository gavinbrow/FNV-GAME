"""Mocked Job/process and synthetic file tests only; no real process launch."""
import copy
import ctypes
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/rebuild'))
import factory_job_launcher as launcher

class FakeBackend:
    def __init__(self,fail=None):self.fail=fail;self.calls=[];self.child=types.SimpleNamespace(pid=123);self.step=0
    def hit(self,name):
        self.calls.append(name)
        if self.fail==name:raise ValueError(name+' failed')
    def create_job(self,nested_parent_allowed,memory_limit):self.hit('create_job');return 77
    def start_suspended(self,command,cwd,job):self.hit('start_suspended');return self.child
    def creation(self,p):self.hit('creation');return 111
    def assign(self,job,p):self.hit('assign')
    def resume(self,p):self.hit('resume')
    def census(self,job):self.hit('census');return []
    def poll(self,p):self.hit('poll');return 0
    def terminate_job(self,job):self.hit('terminate_job')
    def terminate_process(self,p):self.hit('terminate_process')
    def wait(self,p):self.hit('wait');return 2
    def close_process(self,p):self.hit('close_process')
    def close_job(self,job):self.hit('close_job')

class LauncherTests(unittest.TestCase):
    def run_case(self,backend,lease_effect=None,clock=None,overrides=None):
        base=ROOT/'build/rebuild';base.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='authored-factory-job-',dir=base) as d:
            d=Path(d);exe=d/'python.exe';exe.write_bytes(b'authored');sha=launcher.file_hash(exe)
            b={'owner':'/root/authored','slot':1,'lease_pins':{'review.json':'a'*64,'request.json':'b'*64,'source.py':'c'*64},'review_sha256':'a'*64,'inputs':{str(exe):sha},'command':[str(exe),'authored'], 'cwd':str(d),'control':str(d/'control'),'output':str(d/'out'),'allowed_outputs':['result.json'],'nested_parent_allowed':False,'profile':'factory-v14','job_memory_bytes':launcher.JOB_MEMORY,'time_limit_seconds':launcher.SECONDS}
            if overrides:b.update(overrides)
            grant={'owner':'/root/authored','resource':'CPU_heavy','slot':1,'granted_utc':'synthetic','max_seconds':1000,'review_sha256':'a'*64,'input_pins':b['lease_pins']}
            kwargs={'backend':backend,'sleep':lambda _:None}
            if clock is not None:kwargs['clock']=clock
            with patch.object(launcher,'lease',side_effect=lease_effect or (lambda _:grant)),patch.object(launcher,'lease_remaining',return_value=600):
                result=launcher.run_contained(b,**kwargs)
            self.assertTrue((d/'control/prelaunch.json').exists());self.assertTrue((d/'control/terminal.json').exists())
            if result['pid'] is not None:self.assertTrue((d/'control/started.json').exists() or backend.fail=='creation')
            return result,backend.calls
    def test_success_is_mock_only_and_closes_all_handles(self):
        result,calls=self.run_case(FakeBackend());self.assertEqual(result['status'],'completed-unreviewed');self.assertTrue(result['mock_backend']);self.assertFalse(result['kernel_limit_configured_query_verified']);self.assertFalse(result['parent_crash_kill_observed']);self.assertEqual(calls.count('start_suspended'),1);self.assertIn('close_process',calls);self.assertIn('close_job',calls)
    def test_authored_profile_has_only_exact_small_bounds(self):
        overrides={'profile':'authored-smoke-v1','job_memory_bytes':64*1024**2,'time_limit_seconds':10};result,_=self.run_case(FakeBackend(),overrides=overrides);self.assertEqual(result['kernel_job_commit_limit_bytes'],64*1024**2);self.assertEqual(result['time_limit_seconds'],10)
        with self.assertRaisesRegex(ValueError,'factory bounds'):self.run_case(FakeBackend(),overrides={'job_memory_bytes':64*1024**2})
        with self.assertRaisesRegex(ValueError,'authored smoke bounds'):self.run_case(FakeBackend(),overrides=dict(overrides,time_limit_seconds=900))
    def test_assignment_failure_never_resumes_and_stops_owned_child(self):
        result,calls=self.run_case(FakeBackend('assign'));self.assertEqual(result['status'],'failed');self.assertNotIn('resume',calls);self.assertIn('terminate_process',calls);self.assertIn('wait',calls);self.assertIn('close_job',calls)
    def test_parent_job_or_creation_failure_has_no_fallback(self):
        for fail in ('create_job','start_suspended'):
            with self.subTest(fail=fail):
                result,calls=self.run_case(FakeBackend(fail));self.assertEqual(result['status'],'failed');self.assertNotIn('resume',calls)
    def test_post_assignment_failure_kills_job_and_waits(self):
        for fail in ('resume','census','poll'):
            with self.subTest(fail=fail):
                result,calls=self.run_case(FakeBackend(fail));self.assertEqual(result['status'],'failed');self.assertIn('terminate_job',calls);self.assertIn('wait',calls)
    def test_child_nonzero_exit_remains_failure(self):
        class Failed(FakeBackend):
            def poll(self,p):self.hit('poll');return 42
        result,calls=self.run_case(Failed());self.assertEqual(result['status'],'failed');self.assertIn('terminate_job',calls);self.assertEqual(calls.count('close_process'),1)
    def test_exit_closes_child_handles_before_job_drain(self):
        class Lagged(FakeBackend):
            def census(self,job):self.hit('census');return [123] if self.calls.count('census')==1 else []
        result,calls=self.run_case(Lagged());self.assertEqual(result['status'],'completed-unreviewed');self.assertLess(calls.index('close_process'),len(calls)-1-calls[::-1].index('census'));self.assertFalse(result['job_exit_drain_real_smoke_verified'])
    def test_partial_close_does_not_retry_or_wait_stale_handle(self):
        result,calls=self.run_case(FakeBackend('close_process'));self.assertEqual(result['status'],'failed');self.assertIn('terminate_job',calls);self.assertNotIn('wait',calls);self.assertEqual(calls.count('close_process'),1)
    def test_revocation_stops_owned_job(self):
        calls=[0];grant={'owner':'/root/authored','resource':'CPU_heavy','slot':1,'granted_utc':'synthetic','max_seconds':1000,'review_sha256':'a'*64,'input_pins':{'review.json':'a'*64,'request.json':'b'*64,'source.py':'c'*64}}
        def revoke(_):
            calls[0]+=1
            if calls[0]>=4:raise ValueError('revoked')
            return grant
        result,seen=self.run_case(FakeBackend(),revoke);self.assertEqual(result['status'],'failed');self.assertIn('terminate_job',seen);self.assertIn('wait',seen)
    def test_timeout_kills_tree(self):
        times=iter([0,901,902,903]);result,calls=self.run_case(FakeBackend(),clock=lambda:next(times));self.assertEqual(result['status'],'failed');self.assertIn('terminate_job',calls);self.assertTrue(result['termination_wait_empty_census'])
    def test_unexpected_or_reparse_output_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'unexpected').write_bytes(b'x')
            with self.assertRaisesRegex(ValueError,'unexpected output'):launcher.owned_size(p,['allowed'])
            (p/'unexpected').unlink();(p/'allowed').write_bytes(b'x');self.assertEqual(launcher.owned_size(p,['allowed']),1)
    def test_oversized_sparse_output_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            with (p/'allowed').open('wb') as f:f.truncate(launcher.OUTPUT_BYTES+1)
            with self.assertRaisesRegex(ValueError,'output limit'):launcher.owned_size(p,['allowed'])
    def test_control_drift_detected_before_acceptance(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'prelaunch.json').write_bytes(b'first');expected={'prelaunch.json':launcher.file_hash(p/'prelaunch.json')};self.assertEqual(launcher.control_guard(p,expected),5)
            (p/'prelaunch.json').write_bytes(b'other')
            with self.assertRaisesRegex(ValueError,'content drift'):launcher.control_guard(p,expected)
    def test_unsupported_output_paths_rejected_before_creation(self):
        with tempfile.TemporaryDirectory() as d:
            for name in ('../escape','nested\\escape','/absolute',''):
                with self.subTest(name=name),self.assertRaises(ValueError):launcher.owned_size(Path(d)/'absent',[name])
    def test_lease_exact_pins_state_expiry_and_lock(self):
        import datetime as dt,json
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'resource-leases.json';b={'owner':'/root/authored','slot':1,'review_sha256':'a'*64,'lease_pins':{'request.json':'b'*64,'source.py':'c'*64,'review.json':'a'*64}}
            row={'owner':b['owner'],'resource':'CPU_heavy','slot':1,'state':'granted','review_sha256':b['review_sha256'],'input_pins':b['lease_pins'],'granted_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'max_seconds':100}
            with patch.object(launcher,'REGISTRY',p):
                for change in ('good','boolslot','wrongpin','expired','duplicate','locked'):
                    r=copy.deepcopy(row);data={'schema_version':1,'CPU_heavy_capacity':2,'leases':[r]}
                    if change=='boolslot':r['slot']=True
                    if change=='wrongpin':r['input_pins']=dict(r['input_pins'],extra='d'*64)
                    if change=='expired':r['granted_utc']=(dt.datetime.now(dt.timezone.utc)-dt.timedelta(seconds=200)).isoformat()
                    if change=='duplicate':data['leases'].append(copy.deepcopy(r))
                    p.write_text(json.dumps(data));lock=p.with_name('resource-leases.lock')
                    if change=='locked':lock.write_text('lock')
                    if change=='good':self.assertEqual(launcher.lease(b)['owner'],b['owner'])
                    else:
                        with self.subTest(change=change),self.assertRaises(ValueError):launcher.lease(b)
                    if lock.exists():lock.unlink()

class Win32ContractTests(unittest.TestCase):
    def make_kernel(self,*,inheritable=False,limit_failure=False,query_mismatch=False):
        class K:
            def __init__(self):self.closed=[];self.flags=None;self.limit=None
            def GetCurrentProcess(self):return 5
            def CreateJobObjectW(self,*args):return 77
            def GetHandleInformation(self,h,p):ctypes.cast(p,ctypes.POINTER(launcher.DWORD))[0]=1 if inheritable else 0;return 1
            def SetInformationJobObject(self,h,kind,p,size):
                v=ctypes.cast(p,ctypes.POINTER(launcher.Extended)).contents;self.flags=v.basic.flags;self.limit=v.job_memory;return not limit_failure
            def QueryInformationJobObject(self,h,kind,p,size,returned):
                if kind==9:
                    v=ctypes.cast(p,ctypes.POINTER(launcher.Extended)).contents;v.basic.flags=self.flags;v.job_memory=self.limit-(1 if query_mismatch else 0)
                else:
                    v=ctypes.cast(p,ctypes.POINTER(launcher.ProcessIds)).contents;v.assigned=0;v.count=0
                return 1
            def CloseHandle(self,h):self.closed.append(h);return 1
        return K()
    def test_mock_kernel_configures_commit_cap_and_kill_on_close(self):
        w=launcher.Windows.__new__(launcher.Windows);w.k=self.make_kernel();w.in_job=lambda *_:False
        self.assertEqual(w.create_job(False,launcher.JOB_MEMORY),77);self.assertEqual(w.k.flags,0x2200);self.assertEqual(w.k.limit,1024**3)
        w.close_job(77);self.assertEqual(w.k.closed,[77])
    def test_inheritable_handle_or_bad_limit_fails_and_closes(self):
        for options in ({'inheritable':True},{'limit_failure':True},{'query_mismatch':True}):
            with self.subTest(options=options):
                w=launcher.Windows.__new__(launcher.Windows);w.k=self.make_kernel(**options);w.in_job=lambda *_:False
                with self.assertRaises(ValueError):w.create_job(False,launcher.JOB_MEMORY)
                self.assertEqual(w.k.closed,[77])
    def test_mock_parent_crash_closes_owned_job_and_tree(self):
        class Kernel:
            def __init__(self):self.live={123,124}
            def CloseHandle(self,h):self.live.clear();return 1
        w=launcher.Windows.__new__(launcher.Windows);w.k=Kernel();w.close_job(77);self.assertEqual(w.k.live,set())
        # This only models the required OS contract; it is not a real crash test.
    def test_partial_close_never_reuses_numeric_handles(self):
        class Kernel:
            def __init__(self):self.calls=[]
            def CloseHandle(self,h):self.calls.append(h);return 0 if h==22 else 1
        w=launcher.Windows.__new__(launcher.Windows);w.k=Kernel();p=launcher.ProcessInfo();p.thread=11;p.process=22
        with self.assertRaisesRegex(ValueError,'state uncertain'):w.close_process(p)
        self.assertIsNone(p.thread);self.assertIsNone(p.process);self.assertEqual(w.k.calls,[11,22])
        with self.assertRaises(ValueError):w.close_process(p)
        self.assertEqual(w.k.calls,[11,22])
    def test_atomic_job_attribute_failure_has_no_process_fallback(self):
        class K:
            def __init__(self):self.calls=[]
            def InitializeProcThreadAttributeList(self,p,n,flags,size):
                self.calls.append('init');ctypes.cast(size,ctypes.POINTER(launcher.SIZE))[0]=64;return bool(p)
            def UpdateProcThreadAttribute(self,*a):self.calls.append('update');return 0
            def DeleteProcThreadAttributeList(self,*a):self.calls.append('delete')
            def CreateProcessW(self,*a):self.calls.append('create');return 1
        w=launcher.Windows.__new__(launcher.Windows);w.k=K()
        with patch.object(launcher.ctypes,'get_last_error',return_value=122,create=True):
            with self.assertRaisesRegex(ValueError,'attribute unsupported'):w.start_suspended(['C:\\authored.exe'],Path('C:\\'),77)
        self.assertNotIn('create',w.k.calls);self.assertIn('delete',w.k.calls)
    def test_mock_create_is_suspended_atomically_in_job_without_handle_inheritance(self):
        class K:
            def __init__(self):self.flags=None;self.inherit=None;self.attr=None;self.deleted=False
            def InitializeProcThreadAttributeList(self,p,n,flags,size):ctypes.cast(size,ctypes.POINTER(launcher.SIZE))[0]=64;return bool(p)
            def UpdateProcThreadAttribute(self,p,flags,attr,values,size,prev,ret):self.attr=attr;self.job=ctypes.cast(values,ctypes.POINTER(launcher.HANDLE))[0];return 1
            def DeleteProcThreadAttributeList(self,p):self.deleted=True
            def CreateProcessW(self,exe,cmd,pa,ta,inherit,flags,env,cwd,start,process):
                self.inherit=inherit;self.flags=flags;v=ctypes.cast(process,ctypes.POINTER(launcher.ProcessInfo)).contents;v.pid=123;v.process=2;v.thread=3;return 1
        w=launcher.Windows.__new__(launcher.Windows);w.k=K()
        with patch.object(launcher.ctypes,'get_last_error',return_value=122,create=True):p=w.start_suspended(['C:\\authored.exe'],Path('C:\\'),77)
        self.assertEqual(p.pid,123);self.assertFalse(w.k.inherit);self.assertEqual(w.k.attr,0x2000d);self.assertEqual(w.k.job,77);self.assertEqual(w.k.flags,0x08080004);self.assertTrue(w.k.deleted)
    def test_preexisting_parent_job_fails_before_creation(self):
        class K:
            def GetCurrentProcess(self):return 5
            def CreateJobObjectW(self,*args):raise AssertionError('must not create nested fallback')
        w=launcher.Windows.__new__(launcher.Windows);w.k=K();w.in_job=lambda *_:True
        with self.assertRaisesRegex(ValueError,'preexisting parent Job'):w.create_job(False,launcher.JOB_MEMORY)
    def test_reviewed_nested_parent_attempt_still_configures_own_job(self):
        w=launcher.Windows.__new__(launcher.Windows);w.k=self.make_kernel();w.in_job=lambda *_:True
        self.assertEqual(w.create_job(True,launcher.JOB_MEMORY),77);self.assertTrue(w.parent_in_job);self.assertEqual(w.k.limit,1024**3);w.close_job(77)

if __name__=='__main__':unittest.main()
