import ctypes
from concurrent.futures import ThreadPoolExecutor
import threading
import importlib.util
from pathlib import Path
import subprocess
import types
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
m=load('adapter_fixture','tools/rebuild/successor_windows_held_link_adapter_v4.py')
b=load('factory_fixture','tools/rebuild/factory_job_launcher.py')

class Pipes:
    def __init__(self,fail=None,k=None):self.next=10;self.closed=[];self.cleared=[];self.fail=fail;self.k=k
    def pipe(self):
        x=self.next;self.next+=2;return (x,x+1)
    def clear_inherit(self,h):
        self.cleared.append(h)
        if h==self.fail:raise OSError('fixture')
    def close(self,h):self.closed.append(h)

class FakeK:
    def __init__(self):self.attrs={};self.calls=[];self.fail_attr=None;self.fail_cleanup=False
    def GetHandleInformation(self,handle,flags):
        flags._obj.value=1 if handle in (10,13,15) else 0;return 1
    def InitializeProcThreadAttributeList(self,pointer,count,flags,size):
        size._obj.value=256;return 0 if pointer is None else 1
    def UpdateProcThreadAttribute(self,pointer,flags,kind,buf,size,a,z):
        count=1 if kind==0x2000d else 3
        self.attrs[kind]=list(ctypes.cast(buf,ctypes.POINTER(b.HANDLE*count)).contents)
        return 0 if self.fail_attr==kind else 1
    def CreateProcessW(self,app,cmd,p1,p2,inherit,flags,env,cwd,startup,process):
        ss=ctypes.cast(startup,ctypes.POINTER(b.StartupEx)).contents
        self.calls.append({'app':app,'command':cmd.value,'inherit':inherit,'flags':flags,'cwd':cwd,
            'stdio':(ss.startup.stdin,ss.startup.stdout,ss.startup.stderr),
            'environment':ctypes.wstring_at(env,len('LIB=C:\\lib\0SYSTEMROOT=C:\\Windows\0\0'))})
        process._obj.pid=222;process._obj.process=200;process._obj.thread=201;return 1
    def DeleteProcThreadAttributeList(self,pointer):
        if self.fail_cleanup:raise RuntimeError('fixture')
class Kernel:
    def __init__(self):self.k=FakeK();self.fail=False
    def job_check(self,job):pass
    def assign(self,job,process):pass
    def identity(self,handle,pid):
        if self.fail:raise OSError('fixture')
        return {'pid':pid,'creation':123,'image':r'C:\Tool Dir\link.exe'}
    def census(self,job):return [222]

class Tests(unittest.TestCase):
    def setUp(self):
        self.kernel=Kernel();self.pipes=Pipes(k=self.kernel.k);self.bundle=m._open_pipe_bundle_fixture(self.pipes)
        self.args={'linker_path':r'C:\Tool Dir\link.exe','response_path':r'C:\Work Dir\link.rsp',
             'cwd':r'C:\Work Dir','environment':{'LIB':r'C:\lib','SYSTEMROOT':r'C:\Windows'},
             'expected_lib':r'C:\lib','job':50,'job_name':'fixture','bundle':self.bundle}
    def create(self):
        with patch.object(ctypes,'get_last_error',return_value=122):return m._create_suspended_fixture(b,self.kernel,**self.args)
    def test_disabled_entry_and_suspended_job_stdio_wiring(self):
        with self.assertRaises(RuntimeError):m.run()
        result=self.create();self.assertEqual(result['status'],'suspended-unreviewed');self.assertFalse(result['started'])
        self.assertEqual(self.kernel.k.attrs[0x2000d],[50]);self.assertEqual(self.kernel.k.attrs[0x20002],[10,13,15])
        call=self.kernel.k.calls[0];self.assertEqual(call['app'],self.args['linker_path'])
        self.assertEqual(call['command'],subprocess.list2cmdline([self.args['linker_path'],'@'+self.args['response_path']]))
        self.assertEqual(call['stdio'],(10,13,15));self.assertTrue(call['inherit']);self.assertEqual(call['flags'],0x08080404)
        self.assertEqual(call['environment'],'LIB=C:\\lib\0SYSTEMROOT=C:\\Windows\0\0')
        self.assertFalse(result['native_link_authorized']);self.assertEqual(result['process_identity']['pid'],222)
    def test_pipe_bundle_and_all_handle_cleanup(self):
        pipes=Pipes();bundle=m._open_pipe_bundle_fixture(pipes)
        self.assertEqual(dict(bundle.handles),dict(self.bundle.handles));self.assertEqual(pipes.cleared,[12,14]);self.assertEqual(pipes.closed,[11])
        m._close_parent_child_ends_fixture(pipes,bundle);self.assertEqual(pipes.closed,[11,15,13,10])
        pipes=Pipes(fail=14)
        with self.assertRaises(OSError):m._open_pipe_bundle_fixture(pipes)
        self.assertEqual(set(pipes.closed),{10,11,12,13,14,15});self.assertEqual(len(pipes.closed),6)
    def test_reject_inherited_parent_handle_and_environment(self):
        self.args['bundle']=dict(self.bundle.handles)
        with self.assertRaises(ValueError):self.create()
        self.args['bundle']=self.bundle;self.args['environment']['LINK']='bad'
        with self.assertRaises(ValueError):self.create()
        with self.assertRaises(ValueError):m._environment_block_fixture({'LIB':'x','X':'a\0b'},'x')
        self.assertEqual(self.kernel.k.calls,[])
    def test_parent_end_close_is_once_even_if_called_twice(self):
        m._close_parent_child_ends_fixture(self.pipes,self.bundle)
        before=list(self.pipes.closed)
        with self.assertRaises(ValueError):m._close_parent_child_ends_fixture(self.pipes,self.bundle)
        self.assertEqual(self.pipes.closed,before)
        with self.assertRaises(ValueError):self.create()
        self.assertEqual(self.kernel.k.calls,[])

    def test_close_failure_tracks_all_attempts_and_quarantines_bundle(self):
        original=self.pipes.close
        def fail(handle):
            original(handle)
            if handle==13:raise OSError('close result uncertain')
        self.pipes.close=fail
        with self.assertRaises(ExceptionGroup):m._close_parent_child_ends_fixture(self.pipes,self.bundle)
        self.assertEqual(self.pipes.closed,[11,15,13,10])
        before=list(self.pipes.closed)
        with self.assertRaises(ValueError):m._close_parent_child_ends_fixture(self.pipes,self.bundle)
        with self.assertRaises(ValueError):self.create()
        self.assertEqual(self.pipes.closed,before);self.assertEqual(self.kernel.k.calls,[])

    def test_precreate_attribute_failure_has_no_process(self):
        self.kernel.k.fail_attr=0x20002
        with self.assertRaises(ValueError):self.create()
        self.assertEqual(self.kernel.k.calls,[])
    def test_duplicate_read_handles_and_job_alias_rejected(self):
        class Duplicate(Pipes):
            def __init__(self):super().__init__();self.pairs=iter([(10,11),(12,13),(12,15)])
            def pipe(self):return next(self.pairs)
        pipes=Duplicate()
        with self.assertRaises(ValueError):m._open_pipe_bundle_fixture(pipes)
        self.assertEqual(len(pipes.closed),len(set(pipes.closed)))
        self.args['job']=12
        with self.assertRaises(ValueError):self.create()
        self.assertEqual(self.kernel.k.calls,[])

    def test_unissued_wrong_backend_and_reused_bundle_rejected(self):
        with self.assertRaises(ValueError):m._PipeBundle(self.pipes,dict(self.bundle.handles),object())
        other=Kernel();self.kernel=other
        with self.assertRaises(ValueError):self.create()
        self.kernel=Kernel();self.pipes=Pipes(k=self.kernel.k);self.args['bundle']=m._open_pipe_bundle_fixture(self.pipes)
        self.assertEqual(self.create()['status'],'suspended-unreviewed')
        with self.assertRaises(ValueError):self.create()
        self.assertEqual(len(self.kernel.k.calls),1)

    def test_concurrent_create_consumes_bundle_exactly_once(self):
        barrier=threading.Barrier(2);original=m._environment_block_fixture
        def held_environment(*args):
            value=original(*args);barrier.wait(timeout=2);return value
        def attempt(_):
            try:return m._create_suspended_fixture(b,self.kernel,**self.args)['status']
            except ValueError:return 'rejected'
        with patch.object(m,'_environment_block_fixture',side_effect=held_environment), \
             patch.object(ctypes,'get_last_error',return_value=122):
            with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(attempt,range(2)))
        self.assertCountEqual(results,['suspended-unreviewed','rejected'])
        self.assertEqual(len(self.kernel.k.calls),1)

    def test_close_rejected_while_create_is_inflight_then_allowed_after_known_boundary(self):
        entered=threading.Event();release=threading.Event();original=self.kernel.k.GetHandleInformation
        def block(handle,flags):
            entered.set();release.wait(2);return original(handle,flags)
        self.kernel.k.GetHandleInformation=block
        try:
            with patch.object(ctypes,'get_last_error',return_value=122),ThreadPoolExecutor(max_workers=1) as pool:
                future=pool.submit(m._create_suspended_fixture,b,self.kernel,**self.args)
                self.assertTrue(entered.wait(1));before=list(self.pipes.closed)
                with self.assertRaises(ValueError):m._close_parent_child_ends_fixture(self.pipes,self.bundle)
                self.assertEqual(self.pipes.closed,before)
                release.set();self.assertEqual(future.result(timeout=2)['status'],'suspended-unreviewed')
            m._close_parent_child_ends_fixture(self.pipes,self.bundle)
            self.assertEqual(self.pipes.closed,[11,15,13,10])
        finally:release.set()

    def test_unknown_create_quarantines_child_handle_cleanup(self):
        self.kernel.k.CreateProcessW=lambda *args:0
        self.assertEqual(self.create()['status'],'UNKNOWN');before=list(self.pipes.closed)
        with self.assertRaises(ValueError):m._close_parent_child_ends_fixture(self.pipes,self.bundle)
        self.assertEqual(self.pipes.closed,before)

    def test_precreate_failure_allows_one_known_boundary_cleanup(self):
        self.kernel.k.fail_attr=0x20002
        with self.assertRaises(ValueError):self.create()
        m._close_parent_child_ends_fixture(self.pipes,self.bundle)
        self.assertEqual(self.pipes.closed,[11,15,13,10])

    def test_createprocess_failure_is_unknown_and_never_retried(self):
        calls=[]
        def fail(*args):calls.append(1);return 0
        self.kernel.k.CreateProcessW=fail
        result=self.create();self.assertEqual(result['status'],'UNKNOWN')
        self.assertEqual(calls,[1]);self.assertFalse(result['native_link_authorized'])

    def test_windows_argument_quoting_keeps_exact_application_argument(self):
        self.args['response_path']='C:\\Work Dir\\backslash\\quoted \"name\".rsp'
        result=self.create();self.assertEqual(result['status'],'suspended-unreviewed')
        self.assertEqual(self.kernel.k.calls[0]['command'],subprocess.list2cmdline(
            [self.args['linker_path'],'@'+self.args['response_path']]))

    def test_process_identity_or_cleanup_failure_preserves_unknown_handles(self):
        self.kernel.fail=True;result=self.create()
        self.assertEqual(result['status'],'UNKNOWN');self.assertEqual(result['process_info'].pid,222)
        self.kernel=Kernel();self.pipes=Pipes(k=self.kernel.k);self.args['bundle']=m._open_pipe_bundle_fixture(self.pipes)
        self.kernel.k.fail_cleanup=True;result=self.create()
        self.assertEqual(result['status'],'UNKNOWN');self.assertEqual(result['process_info'].pid,222)

if __name__=='__main__':unittest.main()
