import ctypes
import importlib.util
from pathlib import Path
import types
import unittest
ROOT=Path(__file__).resolve().parents[2]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
m=load('whole_job_fixture','tools/rebuild/successor_whole_job_terminal_v1.py')
b=load('factory_fixture','tools/rebuild/factory_job_launcher.py')
class Kernel:
    def __init__(self):self.k=self;self.codes=[1120,1120];self.censuses=[[],[]];self.creations=[123,123];self.closes=[];self.failure=None
    def QueryFullProcessImageNameW(self,handle,flags,buffer,size):
        path=r'C:\fixture\link.exe';buffer.value=path;size._obj.value=len(path);return 1
    def job_check(self,job):
        if self.failure=='job':raise OSError('fixture')
    def creation(self,process):return self.creations.pop(0)
    def poll(self,process):return self.codes.pop(0)
    def census(self,job):return self.censuses.pop(0)
    def close_process(self,process):
        self.closes.append('process')
        if self.failure=='process_close':raise OSError('fixture')
    def close_job(self,job):
        self.closes.append('job')
        if self.failure=='job_close':raise OSError('fixture')
class Tests(unittest.TestCase):
    def setUp(self):
        self.kernel=Kernel();self.process=types.SimpleNamespace(pid=42,process=400,thread=401)
        self.child={'pid':42,'creation':123,'image':r'C:\fixture\link.exe'}
    def observer(self,job=99):return m.TerminalObserverFixture(b,self.kernel,self.process,job,expected_child=self.child,
                                                                job_name='fixture-job',session_nonce='a'*64)
    def test_disabled_and_reject_missing_handles(self):
        with self.assertRaises(RuntimeError):m.run()
        for value in (None,0,-1,True):
            with self.subTest(value=value),self.assertRaises(ValueError):self.observer(value)
    def test_exit_and_empty_job_are_only_sampled_evidence(self):
        observer=self.observer();result=observer.observe()
        self.assertEqual(result['returncode'],1120);self.assertEqual(result['empty_job_samples'],2)
        self.assertFalse(result['process_success_established']);self.assertFalse(result['future_job_state_guaranteed'])
        self.assertEqual(result['cleanup_status'],'NOT_ATTEMPTED')
        self.assertFalse(result['native_link_authorized'])
        with self.assertRaises(ValueError):observer.observe()
        cleanup=observer.cleanup();self.assertEqual(cleanup['status'],'CLOSE_CALLS_RETURNED')
        self.assertFalse(cleanup['all_job_handles_globally_closed_established'])
        self.assertEqual(self.kernel.closes,['process','job'])
        with self.assertRaises(ValueError):observer.cleanup()
    def test_active_process_or_descendant_fails_closed_no_retry(self):
        for mode in ('active','descendant','later_descendant','drift','job_failure'):
            self.setUp()
            if mode=='active':self.kernel.codes=[None]
            if mode=='descendant':self.kernel.censuses=[[99]]
            if mode=='later_descendant':self.kernel.censuses=[[],[99]]
            if mode=='drift':self.kernel.creations=[123,124]
            if mode=='job_failure':self.kernel.failure='job'
            observer=self.observer()
            with self.subTest(mode=mode),self.assertRaises((ValueError,OSError)):observer.observe()
            with self.assertRaises(ValueError):observer.observe()
            with self.assertRaises(ValueError):observer.cleanup()
    def test_cleanup_failure_attempts_both_and_is_unknown_no_retry(self):
        observer=self.observer();observer.observe();self.kernel.failure='process_close'
        result=observer.cleanup();self.assertEqual(result['status'],'UNKNOWN')
        self.assertEqual(result['errors'],{'process':'OSError'});self.assertEqual(self.kernel.closes,['process','job'])
        with self.assertRaises(ValueError):observer.cleanup()
    def test_image_query_failure_and_identity_change_fail(self):
        self.kernel.k.QueryFullProcessImageNameW=lambda *a:0;observer=self.observer()
        with self.assertRaises(ValueError):observer.observe()
        self.kernel=Kernel();self.child['image']=r'C:\fixture\other.exe'
        with self.assertRaises(ValueError):self.observer().observe()

if __name__=='__main__':unittest.main()
