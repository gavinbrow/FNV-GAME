"""Held Windows LINK creation adapter draft; no enabled operation entry.

Adapted from factory_held_launcher_v1.native(...).Kernel.start_held and
factory_job_launcher structures. All helper arguments are fixture seams, not
authority. No profile, peer, runtime, lease, process or filesystem is trusted by
this module. run() always fails. A future fixed caller must authenticate source,
Job/handles/environment/identities, hold the lease and reconcile UNKNOWN states.
"""
import ctypes
import ntpath
import os
import subprocess
import types
import weakref

FIXED_PROFILE=None
SOURCE_REVIEW=None
PEER_PINS=None
RUNTIME_PINS=None


def need(ok,message):
    if not ok:raise ValueError(message)


def _close_all(backend, handles):
    failures=[];seen=set()
    for handle in reversed(handles):
        if handle in seen:continue
        seen.add(handle)
        try:backend.close(handle)
        except BaseException as exc:failures.append(exc)
    if failures:raise BaseExceptionGroup('handle cleanup uncertain',failures)


_ISSUER=object()
_ISSUED=weakref.WeakSet()


class _PipeBundle:
    """Process-local capability only; authenticated wrapper still required."""
    __slots__=('_owner','_handles','_consumed','__weakref__')
    def __init__(self,owner,handles,issuer):
        need(issuer is _ISSUER,'pipe issuer differs')
        object.__setattr__(self,'_owner',owner)
        object.__setattr__(self,'_handles',types.MappingProxyType(dict(handles)))
        object.__setattr__(self,'_consumed',False)
        _ISSUED.add(self)
    def __setattr__(self,name,value):raise AttributeError('immutable pipe capability')
    @property
    def handles(self):return self._handles


def _bundle_auth(bundle,backend):
    need(type(bundle) is _PipeBundle and bundle in _ISSUED and bundle._owner is backend,
         'unissued or wrong-backend pipe capability')
    handles=bundle.handles
    need(set(handles)=={'stdin_read','stdout_read','stdout_write','stderr_read','stderr_write'} and
         all(type(h) is int and h>0 for h in handles.values()) and len(set(handles.values()))==5,
         'distinct typed pipe handles required')
    return handles


def _open_pipe_bundle_fixture(backend):
    """Create inherited stdin/out/err ends; parent stdout/stderr reads private."""
    opened=[]
    try:
        stdin_read,stdin_write=backend.pipe();opened.extend([stdin_read,stdin_write])
        stdout_read,stdout_write=backend.pipe();opened.extend([stdout_read,stdout_write])
        stderr_read,stderr_write=backend.pipe();opened.extend([stderr_read,stderr_write])
        need(len(set(opened))==6 and all(type(h) is int and h>0 for h in opened),'pipe handles differ')
        backend.clear_inherit(stdout_read);backend.clear_inherit(stderr_read)
        # Closing the only stdin writer produces EOF, without inheriting it.
        opened.remove(stdin_write);backend.close(stdin_write)
        return _PipeBundle(backend,{'stdin_read':stdin_read,'stdout_read':stdout_read,'stdout_write':stdout_write,
                'stderr_read':stderr_read,'stderr_write':stderr_write},_ISSUER)
    except BaseException as original:
        try:_close_all(backend,opened)
        except BaseException as cleanup:raise BaseExceptionGroup('pipe setup and cleanup failed',[original,cleanup]) from None
        raise


def _close_parent_child_ends_fixture(backend,bundle):
    """After process creation close the three child-side copies exactly once."""
    handles=_bundle_auth(bundle,backend)
    _close_all(backend,[handles['stdin_read'],handles['stdout_write'],handles['stderr_write']])


class WindowsPipeBackend:
    """Thin Win32 pipe operations; no call is made until a future caller uses it."""
    def __init__(self,kernel32,base):
        self.k=kernel32;self.base=base
        class Security(ctypes.Structure):
            _fields_=[('length',base.DWORD),('descriptor',ctypes.c_void_p),('inherit',ctypes.c_int)]
        self.Security=Security
        self.k.CreatePipe.argtypes=[ctypes.POINTER(base.HANDLE),ctypes.POINTER(base.HANDLE),ctypes.POINTER(Security),base.DWORD]
        self.k.CreatePipe.restype=ctypes.c_int
        self.k.SetHandleInformation.argtypes=[base.HANDLE,base.DWORD,base.DWORD]
        self.k.SetHandleInformation.restype=ctypes.c_int
    def pipe(self):
        read=self.base.HANDLE();write=self.base.HANDLE();security=self.Security(ctypes.sizeof(self.Security),None,1)
        need(self.k.CreatePipe(ctypes.byref(read),ctypes.byref(write),ctypes.byref(security),0),'CreatePipe failed')
        return int(read.value),int(write.value)
    def clear_inherit(self,handle):need(self.k.SetHandleInformation(handle,1,0),'clear inheritance failed')
    def close(self,handle):need(self.k.CloseHandle(handle),'handle close failed')


def _environment_block_fixture(environment,expected_lib):
    need(type(environment) is dict and environment and type(expected_lib) is str and expected_lib and
         all(type(k) is str and k and '=' not in k and '\0' not in k and type(v) is str and '\0' not in v
             for k,v in environment.items()),'environment schema')
    names={k.upper():v for k,v in environment.items()}
    need(len(names)==len(environment) and not {'CL','_CL_','LINK','_LINK_','LIBPATH'}&set(names) and
         names.get('LIB')==expected_lib,'environment policy differs')
    return '\0'.join(k+'='+environment[k] for k in sorted(environment,key=str.upper))+'\0\0'


def _create_suspended_fixture(base,kernel,*,linker_path,response_path,cwd,environment,expected_lib,job,job_name,bundle):
    """Perform exactly one CreateProcessW call under fixture-supplied authority.

    Windows implementation is real API wiring, but cannot itself authorize an
    invocation. On any creation/identity failure the caller must quarantine the
    attempt; it must reconcile/terminate using owned handles, never retry.
    """
    need(all(type(p) is str and ntpath.isabs(p) and '\0' not in p for p in (linker_path,response_path,cwd)) and
         type(job) is int and job>0 and type(job_name) is str and job_name,'fixed process/Job scope')
    need(type(bundle) is _PipeBundle and getattr(bundle._owner,'k',None) is kernel.k, 'pipe backend differs')
    handles=_bundle_auth(bundle,bundle._owner)
    need(not bundle._consumed and job not in handles.values(), 'pipe capability consumed or aliases Job')
    inherited=[handles['stdin_read'],handles['stdout_write'],handles['stderr_write']]
    need(all(type(h) is int and h>0 for h in inherited) and len(set(inherited))==3 and
         job not in inherited and handles['stdout_read'] not in inherited and handles['stderr_read'] not in inherited,
         'stdio handle allowlist differs')
    env=_environment_block_fixture(environment,expected_lib)
    object.__setattr__(bundle,'_consumed',True)
    k=kernel.k
    for handle,expect in [(job,False)]+[(h,True) for h in inherited]+[(handles['stdout_read'],False),(handles['stderr_read'],False)]:
        flags=base.DWORD();need(k.GetHandleInformation(handle,ctypes.byref(flags)) and bool(flags.value&1)==expect,
                                'handle inheritability differs')
    size=base.SIZE();ok=k.InitializeProcThreadAttributeList(None,2,0,ctypes.byref(size))
    need(not ok and ctypes.get_last_error()==122 and 0<size.value<=1024*1024,'attribute list sizing failed')
    memory=ctypes.create_string_buffer(size.value);pointer=ctypes.cast(memory,ctypes.c_void_p)
    need(k.InitializeProcThreadAttributeList(pointer,2,0,ctypes.byref(size)),'attribute initialization failed')
    process=base.ProcessInfo();attempted=False;result=None;failure=None
    try:
        jobs=(base.HANDLE*1)(job);inherit_handles=(base.HANDLE*3)(*inherited)
        need(k.UpdateProcThreadAttribute(pointer,0,0x2000d,ctypes.byref(jobs),ctypes.sizeof(jobs),None,None),'JOB_LIST failed')
        need(k.UpdateProcThreadAttribute(pointer,0,0x20002,ctypes.byref(inherit_handles),ctypes.sizeof(inherit_handles),None,None),'HANDLE_LIST failed')
        startup=base.StartupEx();startup.startup.cb=ctypes.sizeof(startup);startup.attributes=pointer
        startup.startup.flags=0x100;startup.startup.stdin=inherited[0]
        startup.startup.stdout=inherited[1];startup.startup.stderr=inherited[2]
        command=ctypes.create_unicode_buffer(subprocess.list2cmdline([linker_path,'@'+response_path]))
        envbuf=ctypes.create_unicode_buffer(env)
        # Suspended, no window, extended startup, Unicode environment.
        attempted=True
        need(k.CreateProcessW(linker_path,command,None,None,True,0x4|0x08000000|0x80000|0x400,
                              ctypes.cast(envbuf,ctypes.c_void_p),cwd,ctypes.byref(startup),ctypes.byref(process)),
             'CreateProcessW outcome unknown')
        kernel.job_check(job);kernel.assign(job,process)
        identity=kernel.identity(process.process,process.pid)
        need(identity['pid']==process.pid and ntpath.normcase(identity['image'])==ntpath.normcase(linker_path) and
             kernel.census(job)==[process.pid],'process/Job identity differs')
        result={'status':'suspended-unreviewed','process_info':process,'process_identity':identity,
                'job_name':job_name,'job_handle':job,'capture_read_handles':[handles['stdout_read'],handles['stderr_read']],
                'started':False,'native_link_authorized':False}
    except BaseException as exc:failure=exc
    try:k.DeleteProcThreadAttributeList(pointer)
    except BaseException as exc:
        failure=BaseExceptionGroup('creation and attribute cleanup uncertain',[failure,exc]) if failure else exc
    if failure:
        if not attempted:raise failure
        # Keep any returned process handles for external bounded reconciliation.
        # A failed CreateProcessW call also remains UNKNOWN; never replay it.
        return {'status':'UNKNOWN','reason':type(failure).__name__,'process_info':process,
                'job_name':job_name,'job_handle':job,'native_link_authorized':False}
    return result



def run():
    raise RuntimeError('held LINK adapter disabled pending exact independent profile, peers, source, lease and watchdog')


if __name__=='__main__':run()
