"""Reviewed-call-site-only, one-shot Windows Job wrapper for a factory child.

No factory operation is configured here. A future reviewed caller must bind the
exact command, input hashes, lease, output allowlist and accepted reviews. This
module does not itself certify a factory result or authorize a native operation.
"""
from __future__ import annotations
import ctypes
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import time

SECONDS=900
JOB_MEMORY=1024**3
OUTPUT_BYTES=128*1024**2
CONTROL_RESERVE=8*1024**2
SAMPLE_BYTES=4*1024**2
MAX_FILES=1024
REGISTRY=Path(__file__).resolve().parents[2]/'build/rebuild/application-frontier-dispatch-v1/resource-leases.json'
DWORD=ctypes.c_uint32; SIZE=ctypes.c_size_t; HANDLE=ctypes.c_void_p
def need(ok,why):
    if not ok: raise ValueError(why)
def file_hash(p,maximum=128*1024**2):
    p=Path(p);before=p.stat();need(before.st_size<=maximum,'input bound');h=hashlib.sha256();size=0
    with p.open('rb') as f:
        while True:
            b=f.read(1024*1024)
            if not b:break
            size+=len(b);need(size<=maximum,'growing input');h.update(b)
    after=p.stat();need((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns),'input drift');return h.hexdigest()
def save_new(path,value):
    data=(json.dumps(value,sort_keys=True,indent=2)+'\n').encode()
    with Path(path).open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
def control_guard(control,expected):
    actual={p.name for p in control.iterdir()};need(actual==set(expected),'control names drift');size=0
    for name,pin in expected.items():
        p=control/name;st=p.lstat();need(stat.S_ISREG(st.st_mode) and not getattr(st,'st_file_attributes',0)&0x400,'control file type');size+=st.st_size;need(file_hash(p,1024*1024)==pin,'control content drift')
    return size
def verify_inputs(binding):
    need(type(binding['inputs']) is dict and binding['inputs'],'exact input pins required')
    for path,pin in binding['inputs'].items():
        need(type(path) is str and Path(path).is_absolute() and type(pin) is str and re.fullmatch('[0-9a-f]{64}',pin),'invalid pin');need(file_hash(path)==pin,'input hash drift')
def lease(binding):
    path=REGISTRY;lock=path.with_name('resource-leases.lock');need(not lock.exists(),'lease registry locked');before=path.stat();need(before.st_size<=4*1024**2,'lease registry bound')
    with path.open('rb') as f:raw=f.read(4*1024**2+1)
    after=path.stat();need(len(raw)<=4*1024**2 and (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns) and not lock.exists(),'lease registry unsafe');data=json.loads(raw)
    need(type(data.get('schema_version')) is int and data['schema_version']==1 and type(data.get('CPU_heavy_capacity')) is int and data['CPU_heavy_capacity']==2,'lease schema')
    owner=binding['owner'];slot=binding['slot'];pins=binding['lease_pins'];review=binding['review_sha256']
    need(type(owner) is str and owner.startswith('/root/') and type(slot) is int and slot in (1,2),'lease identity')
    need(type(pins) is dict and len(pins)>=3 and all(type(k) is str and Path(k).name==k and type(v) is str and re.fullmatch('[0-9a-f]{64}',v) for k,v in pins.items()),'lease pin schema')
    need(type(review) is str and re.fullmatch('[0-9a-f]{64}',review) and review in pins.values(),'review pin')
    rows=[x for x in data['leases'] if x.get('owner')==owner and x.get('resource')=='CPU_heavy' and type(x.get('slot')) is int and x['slot']==slot]
    need(len(rows)==1,'unique CPU lease required');row=rows[0]
    need(row.get('state') in ('granted','running') and row.get('input_pins')==pins and row.get('review_sha256')==review and type(row.get('max_seconds')) is int and row['max_seconds']>0,'lease pins/state')
    granted=dt.datetime.fromisoformat(row['granted_utc'].replace('Z','+00:00'));need(granted.tzinfo is not None and granted.utcoffset()==dt.timedelta(0),'UTC lease required');now=dt.datetime.now(dt.timezone.utc);end=granted+dt.timedelta(seconds=row['max_seconds']);need(granted<=now<end,'lease expired')
    return {k:row[k] for k in ('owner','resource','slot','granted_utc','max_seconds','review_sha256','input_pins')}
def lease_remaining(grant):
    start=dt.datetime.fromisoformat(grant['granted_utc'].replace('Z','+00:00'));return (start+dt.timedelta(seconds=grant['max_seconds'])-dt.datetime.now(dt.timezone.utc)).total_seconds()
def owned_size(output,allowed):
    output=Path(output)
    allowed=set(allowed);dirs={''}
    for name in allowed:
        need(type(name) is str and name and '\\' not in name,'invalid allowed path');p=PurePosixPath(name);need(not p.is_absolute() and all(part not in ('','.','..') for part in p.parts) and p.as_posix()==name,'invalid allowed path')
        for i in range(1,len(p.parts)):dirs.add('/'.join(p.parts[:i]))
    if not output.exists():return 0
    root_stat=output.lstat();need(stat.S_ISDIR(root_stat.st_mode) and not stat.S_ISLNK(root_stat.st_mode) and not getattr(root_stat,'st_file_attributes',0)&0x400,'output directory invalid')
    total=0; count=0; todo=[('',output)]
    while todo:
        prefix,directory=todo.pop()
        with os.scandir(directory) as it:
            for e in it:
                count+=1;need(count<=MAX_FILES,'output file count');name=(prefix+'/' if prefix else '')+e.name;st=e.stat(follow_symlinks=False)
                need(not stat.S_ISLNK(st.st_mode) and not getattr(st,'st_file_attributes',0)&0x400,'output reparse')
                if stat.S_ISDIR(st.st_mode):need(name in dirs,'unexpected output directory');todo.append((name,Path(e.path)))
                else:need(stat.S_ISREG(st.st_mode) and name in allowed,'unexpected output file');total+=st.st_size;need(total<=OUTPUT_BYTES,'output limit')
    return total

class Basic(ctypes.Structure):
    _fields_=[('process_time',ctypes.c_int64),('job_time',ctypes.c_int64),('flags',DWORD),('minimum',SIZE),('maximum',SIZE),('active',DWORD),('affinity',SIZE),('priority',DWORD),('scheduling',DWORD)]
class IO(ctypes.Structure):_fields_=[(n,ctypes.c_uint64) for n in ('read_ops','write_ops','other_ops','read_bytes','write_bytes','other_bytes')]
class Extended(ctypes.Structure):_fields_=[('basic',Basic),('io',IO),('process_memory',SIZE),('job_memory',SIZE),('peak_process',SIZE),('peak_job',SIZE)]
class Startup(ctypes.Structure):
    _fields_=[('cb',DWORD),('reserved',ctypes.c_wchar_p),('desktop',ctypes.c_wchar_p),('title',ctypes.c_wchar_p),('x',DWORD),('y',DWORD),('xsize',DWORD),('ysize',DWORD),('xchars',DWORD),('ychars',DWORD),('fill',DWORD),('flags',DWORD),('show',ctypes.c_uint16),('reserved2_count',ctypes.c_uint16),('reserved2',ctypes.c_void_p),('stdin',HANDLE),('stdout',HANDLE),('stderr',HANDLE)]
class StartupEx(ctypes.Structure):_fields_=[('startup',Startup),('attributes',ctypes.c_void_p)]
class ProcessInfo(ctypes.Structure):_fields_=[('process',HANDLE),('thread',HANDLE),('pid',DWORD),('tid',DWORD)]
class FileTime(ctypes.Structure):_fields_=[('low',DWORD),('high',DWORD)]
class ProcessIds(ctypes.Structure):_fields_=[('assigned',DWORD),('count',DWORD),('pids',SIZE*MAX_FILES)]

class Windows:
    def __init__(self):
        need(os.name=='nt','Windows Job containment required');self.k=ctypes.WinDLL('kernel32',use_last_error=True)
        prototypes={'CreateJobObjectW':([HANDLE,ctypes.c_wchar_p],HANDLE),'SetInformationJobObject':([HANDLE,ctypes.c_int,ctypes.c_void_p,DWORD],ctypes.c_int),'QueryInformationJobObject':([HANDLE,ctypes.c_int,ctypes.c_void_p,DWORD,ctypes.c_void_p],ctypes.c_int),'IsProcessInJob':([HANDLE,HANDLE,ctypes.POINTER(ctypes.c_int)],ctypes.c_int),'InitializeProcThreadAttributeList':([ctypes.c_void_p,DWORD,DWORD,ctypes.POINTER(SIZE)],ctypes.c_int),'UpdateProcThreadAttribute':([ctypes.c_void_p,DWORD,SIZE,ctypes.c_void_p,SIZE,ctypes.c_void_p,ctypes.c_void_p],ctypes.c_int),'DeleteProcThreadAttributeList':([ctypes.c_void_p],None),'TerminateJobObject':([HANDLE,DWORD],ctypes.c_int),'TerminateProcess':([HANDLE,DWORD],ctypes.c_int),'CloseHandle':([HANDLE],ctypes.c_int),'GetHandleInformation':([HANDLE,ctypes.POINTER(DWORD)],ctypes.c_int),'GetCurrentProcess':([],HANDLE),'ResumeThread':([HANDLE],DWORD),'WaitForSingleObject':([HANDLE,DWORD],DWORD),'GetExitCodeProcess':([HANDLE,ctypes.POINTER(DWORD)],ctypes.c_int),'GetProcessTimes':([HANDLE,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p],ctypes.c_int),'CreateProcessW':([ctypes.c_wchar_p,ctypes.c_wchar_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,DWORD,ctypes.c_void_p,ctypes.c_wchar_p,ctypes.c_void_p,ctypes.POINTER(ProcessInfo)],ctypes.c_int)}
        for name,(args,result) in prototypes.items():f=getattr(self.k,name);f.argtypes=args;f.restype=result
    def in_job(self,process,job=None):
        v=ctypes.c_int();need(self.k.IsProcessInJob(process,job,ctypes.byref(v)),'Job membership query failed');return bool(v.value)
    def create_job(self,nested_parent_allowed,memory_limit):
        self.parent_in_job=self.in_job(self.k.GetCurrentProcess());need(not self.parent_in_job or nested_parent_allowed is True,'preexisting parent Job requires reviewed nested capability');h=self.k.CreateJobObjectW(None,None);need(h,'Job creation failed')
        try:
            flags=DWORD();need(self.k.GetHandleInformation(h,ctypes.byref(flags)) and not flags.value&1,'inheritable Job handle')
            v=Extended();v.basic.flags=0x2000|0x200;v.job_memory=memory_limit
            need(self.k.SetInformationJobObject(h,9,ctypes.byref(v),ctypes.sizeof(v)),'Job limit failed');actual=Extended();need(self.k.QueryInformationJobObject(h,9,ctypes.byref(actual),ctypes.sizeof(actual),None),'Job limit query failed')
            need(actual.basic.flags==v.basic.flags and actual.job_memory==memory_limit,'Job limits differ');need(self.census(h)==[],'new Job not empty');return h
        except BaseException:self.k.CloseHandle(h);raise
    def census(self,job):
        v=ProcessIds();need(self.k.QueryInformationJobObject(job,3,ctypes.byref(v),ctypes.sizeof(v),None),'Job census failed');need(v.count<=MAX_FILES and v.assigned==v.count,'incomplete Job census');return sorted(int(v.pids[i]) for i in range(v.count))
    def start_suspended(self,command,cwd,job):
        # The Job-list attribute requests assignment as part of process
        # creation, before the suspended child can run. Creator-death behavior
        # remains unverified by this source or mocked tests. No handles inherit.
        size=SIZE();ok=self.k.InitializeProcThreadAttributeList(None,1,0,ctypes.byref(size));need(not ok and ctypes.get_last_error()==122 and 0<size.value<=1024*1024,'attribute list sizing failed');buf=ctypes.create_string_buffer(size.value);ptr=ctypes.cast(buf,ctypes.c_void_p);need(self.k.InitializeProcThreadAttributeList(ptr,1,0,ctypes.byref(size)),'attribute list initialization failed')
        try:
            handles=(HANDLE*1)(job);need(self.k.UpdateProcThreadAttribute(ptr,0,0x0002000d,ctypes.byref(handles),ctypes.sizeof(handles),None,None),'atomic Job attribute unsupported')
            s=StartupEx();s.startup.cb=ctypes.sizeof(s);s.attributes=ptr;p=ProcessInfo();cmd=ctypes.create_unicode_buffer(subprocess.list2cmdline(command));need(self.k.CreateProcessW(command[0],cmd,None,None,False,0x4|0x08000000|0x00080000,None,str(cwd),ctypes.byref(s),ctypes.byref(p)),'contained suspended CreateProcess failed');return p
        finally:self.k.DeleteProcThreadAttributeList(ptr)
    def creation(self,p):
        v=[FileTime() for _ in range(4)];need(self.k.GetProcessTimes(p.process,*[ctypes.byref(i) for i in v]),'creation identity query');return (v[0].high<<32)|v[0].low
    def assign(self,job,p):
        need(self.in_job(self.k.GetCurrentProcess())==self.parent_in_job,'parent Job presence changed');need(self.in_job(p.process,job),'atomic Job assignment not verified');need(self.census(job)==[p.pid],'initial Job census differs')
    def resume(self,p):need(self.k.ResumeThread(p.thread)!=0xffffffff,'resume failed')
    def poll(self,p):
        result=self.k.WaitForSingleObject(p.process,0);need(result in (0,0x102),'process wait failed')
        if result==0:
            v=DWORD();need(self.k.GetExitCodeProcess(p.process,ctypes.byref(v)),'exit query failed');return int(v.value)
        return None
    def terminate_job(self,job):need(self.k.TerminateJobObject(job,2),'Job termination failed')
    def terminate_process(self,p):need(self.k.TerminateProcess(p.process,2),'suspended process termination failed')
    def wait(self,p):need(self.k.WaitForSingleObject(p.process,10000)==0,'owned process wait timeout');return self.poll(p)
    def close_process(self,p):
        # Once a close is attempted, the numeric handle is never used again:
        # a failed CloseHandle is not safe evidence that retrying is harmless.
        thread=p.thread;process=p.process;p.thread=None;p.process=None
        ok1=self.k.CloseHandle(thread) if thread else False
        ok2=self.k.CloseHandle(process) if process else False
        need(ok1 and ok2,'process handle close failed; handle state uncertain')
    def close_job(self,job):need(self.k.CloseHandle(job),'Job handle close failed')

def run_contained(binding, *, backend=None, clock=time.monotonic, sleep=time.sleep):
    """One reviewed command, one leased job; no retry or uncontained fallback."""
    need(type(binding) is dict and set(binding)=={'owner','slot','lease_pins','review_sha256','inputs','command','cwd','control','output','allowed_outputs','nested_parent_allowed','profile','job_memory_bytes','time_limit_seconds'},'binding schema');need(type(binding['nested_parent_allowed']) is bool,'nested capability must be explicit bool')
    need(type(binding['job_memory_bytes']) is int and type(binding['time_limit_seconds']) is int,'limit types')
    if binding['profile']=='factory-v14':need(binding['job_memory_bytes']==JOB_MEMORY and binding['time_limit_seconds']==SECONDS,'factory bounds')
    elif binding['profile']=='authored-smoke-v1':need(binding['job_memory_bytes']==64*1024**2 and binding['time_limit_seconds'] in (2,10),'authored smoke bounds')
    else:raise ValueError('unknown operation profile')
    memory_limit=binding['job_memory_bytes'];time_limit=binding['time_limit_seconds']
    command=binding['command'];need(type(command) is list and command and all(type(s) is str and s and '\x00' not in s for s in command) and Path(command[0]).is_absolute(),'command schema')
    need(str(Path(command[0])) in binding['inputs'],'executable must be pinned');need(type(binding['allowed_outputs']) is list and len(binding['allowed_outputs'])==len(set(binding['allowed_outputs'])),'output allowlist')
    control=Path(binding['control']);output=Path(binding['output']);cwd=Path(binding['cwd']);private=Path(__file__).resolve().parents[2]/'build/rebuild';cp=control.resolve();op=output.resolve();need(all(p.is_absolute() for p in (control,output,cwd)) and cp.is_relative_to(private.resolve()) and op.is_relative_to(private.resolve()) and not cp.is_relative_to(op) and not op.is_relative_to(cp) and not control.exists() and not output.exists(),'fresh private paths')
    need(len(json.dumps(binding,sort_keys=True).encode())<=1024*1024,'binding size');owned_size(output,binding['allowed_outputs'])
    verify_inputs(binding);grant=lease(binding);need(lease_remaining(grant)>2.5,'lease deadline too close');real_backend=backend is None;backend=Windows() if real_backend else backend;control.mkdir();start=clock();job=None;child=None;child_handles_closed=False;assigned=False;termination_wait_complete=False;creation=None;reason=None;exitcode=None;observations=[];sample_bytes=0
    save_new(control/'prelaunch.json',{'state':'once-only-intent','binding_sha256':hashlib.sha256(json.dumps(binding,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'lease':grant,'command':command});controls={'prelaunch.json':file_hash(control/'prelaunch.json',1024*1024)}
    try:
        job=backend.create_job(binding['nested_parent_allowed'],memory_limit);need(lease(binding)==grant and lease_remaining(grant)>2.5,'lease changed before child');verify_inputs(binding)
        child=backend.start_suspended(command,cwd,job);creation=backend.creation(child);save_new(control/'started.json',{'pid':int(child.pid),'creation_time':creation,'state':'suspended-created-in-Job-before-execution'});controls['started.json']=file_hash(control/'started.json',1024*1024)
        backend.assign(job,child);assigned=True;need(backend.creation(child)==creation,'child identity changed');need(lease(binding)==grant and lease_remaining(grant)>2.5,'lease changed before resume');verify_inputs(binding);control_guard(control,controls);backend.resume(child)
        while True:
            need(clock()-start<time_limit and lease_remaining(grant)>2.5,'deadline');need(lease(binding)==grant,'lease changed');used=owned_size(output,binding['allowed_outputs']);need(used+control_guard(control,controls)<=OUTPUT_BYTES-CONTROL_RESERVE,'aggregate output limit');sample={'pids':backend.census(job),'output_bytes':used};sample_bytes+=len(json.dumps(sample).encode());need(sample_bytes<=SAMPLE_BYTES,'sample byte bound');observations.append(sample);need(len(observations)<=20000,'sample bound')
            if exitcode is None:
                exitcode=backend.poll(child)
                if exitcode is not None:child_handles_closed=True;backend.close_process(child)
            if exitcode is not None and not observations[-1]['pids']:break
            sleep(.05)
        need(exitcode==0,'factory child failed');need(lease(binding)==grant,'lease changed after exit');verify_inputs(binding);owned_size(output,binding['allowed_outputs'])
    except BaseException as exc:
        reason=type(exc).__name__+':'+str(exc)
        if child is not None:
            try:
                if assigned:backend.terminate_job(job)
                elif not child_handles_closed:backend.terminate_process(child)
                if not child_handles_closed:exitcode=backend.wait(child)
                if assigned:
                    stop_start=clock()
                    while backend.census(job):need(clock()-stop_start<10,'Job descendant wait timeout');sleep(.05)
                    termination_wait_complete=True
            except BaseException as stop:reason+='; termination/wait uncertain: '+type(stop).__name__
    finally:
        if child is not None and not child_handles_closed:
            child_handles_closed=True
            try:backend.close_process(child)
            except BaseException as error:reason=reason or 'process close uncertain: '+type(error).__name__
        if job is not None:
            try:backend.close_job(job)
            except BaseException as error:reason=reason or 'Job close uncertain: '+type(error).__name__
    if reason is None:
        try:need(clock()-start<time_limit and lease(binding)==grant and lease_remaining(grant)>0,'terminal lease/deadline');verify_inputs(binding);need(owned_size(output,binding['allowed_outputs'])+control_guard(control,controls)<=OUTPUT_BYTES-CONTROL_RESERVE,'aggregate output limit')
        except BaseException as error:reason='terminal guard: '+type(error).__name__+':'+str(error)
    receipt={'status':'completed-unreviewed' if reason is None else 'failed','reason':reason,'pid':int(child.pid) if child else None,'creation_time':creation,'returncode':exitcode,'elapsed_seconds':clock()-start,'profile':binding['profile'],'time_limit_seconds':time_limit,'kernel_job_commit_limit_bytes':memory_limit,'kernel_limit_configured_query_verified':bool(real_backend and job and assigned),'kill_on_close_configured_query_verified':bool(real_backend and job and assigned),'termination_wait_empty_census':termination_wait_complete,'parent_crash_kill_observed':False,'parent_job_presence':getattr(backend,'parent_in_job',None),'parent_job_hierarchy_identity_verified':False,'job_exit_drain_real_smoke_verified':False,'mock_backend':not real_backend,'job_census_samples':observations,'output_limit_bytes':OUTPUT_BYTES,'serialized_output_is_not_RSS':True,'provider_selected':False,'runtime_eligible':False}
    need(len(json.dumps(receipt).encode())<=CONTROL_RESERVE,'terminal receipt bound');save_new(control/'terminal.json',receipt);return receipt
