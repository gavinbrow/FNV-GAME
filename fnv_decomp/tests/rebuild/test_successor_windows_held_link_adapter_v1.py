import ctypes
import importlib.util
from pathlib import Path
import subprocess
import types
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
m=load('adapter_fixture','tools/rebuild/successor_windows_held_link_adapter_v1.py')
b=load('factory_fixture','tools/rebuild/factory_job_launcher.py')

class Pipes:
    def __init__(self,fail=None):self.next=10;self.closed=[];self.cleared=[];self.fail=fail
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
        self.bundle={'stdin_read':10,'stdout_read':12,'stdout_write':13,'stderr_read':14,'stderr_write':15}
        self.kernel=Kernel();self.args={'linker_path':r'C:\Tool Dir\link.exe','response_path':r'C:\Work Dir\link.rsp',
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
        self.assertEqual(bundle,self.bundle);self.assertEqual(pipes.cleared,[12,14]);self.assertEqual(pipes.closed,[11])
        m._close_parent_child_ends_fixture(pipes,bundle);self.assertEqual(pipes.closed,[11,15,13,10])
        pipes=Pipes(fail=14)
        with self.assertRaises(OSError):m._open_pipe_bundle_fixture(pipes)
        self.assertEqual(set(pipes.closed),{10,11,12,13,14,15});self.assertEqual(len(pipes.closed),6)
    def test_reject_inherited_parent_handle_and_environment(self):
        self.args['bundle']=dict(self.bundle,stdout_write=12)
        with self.assertRaises(ValueError):self.create()
        self.args['bundle']=self.bundle;self.args['environment']['LINK']='bad'
        with self.assertRaises(ValueError):self.create()
        with self.assertRaises(ValueError):m._environment_block_fixture({'LIB':'x','X':'a\0b'},'x')
        self.assertEqual(self.kernel.k.calls,[])
    def test_precreate_attribute_failure_has_no_process(self):
        self.kernel.k.fail_attr=0x20002
        with self.assertRaises(ValueError):self.create()
        self.assertEqual(self.kernel.k.calls,[])
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
        self.kernel=Kernel();self.kernel.k.fail_cleanup=True;result=self.create()
        self.assertEqual(result['status'],'UNKNOWN');self.assertEqual(result['process_info'].pid,222)

if __name__=='__main__':unittest.main()
