"""Reviewed once-only CRT fixture compiler/linker. Never runs the result.

Monitor limits are sampled, not hard disk quotas. Any interrupted operation or
missing terminal receipt requires reconciliation; output directory blocks retry.
"""
import ctypes, hashlib, json, os, subprocess, sys, time
from pathlib import Path
import factory_job_launcher as base

ROOT=Path(__file__).resolve().parents[2]
SP1=ROOT/'build/rebuild/toolchains/sp1'
SRC=ROOT/'runtime/probes/crt_v15_alias_fixture.cpp'
OUT=ROOT/'build/rebuild/crt-v15-alias-component-v2'
A='_fnv_undefined_86b5006e5d6d2a0348c632bbd16e24c66b0a3804def721a1235e0f2a4af3c7e9'
B='_fnv_undefined_d9896c4c820aa59aae9e417910a0bfa1c7374957003b682c2810dddb89febb3d'
LIMIT=4*1024*1024

def sha(p): return base.file_hash(p)
def need(v,s): base.need(v,s)
def commands():
    obj=OUT/'fixture.obj'; exe=OUT/'fixture.exe'; mapping=OUT/'fixture.map'
    return [[str(SP1/'VC/bin/cl.exe'),'/nologo','/c','/MT','/EHsc','/GR','/Od','/Fo'+str(obj),str(SRC)],
      [str(SP1/'VC/bin/link.exe'),'/nologo','/machine:x86','/subsystem:console','/incremental:no','/verbose:lib','/out:'+str(exe),'/map:'+str(mapping),'/include:'+A,'/include:'+B,'/alternatename:'+A+'=___CxxFrameHandler3','/alternatename:'+B+'=___RTDynamicCast',str(obj)]]

def environment(systemroot):
    return {'SystemRoot':systemroot,'PATH':str(SP1/'VC/bin')+os.pathsep+str(Path(systemroot)/'System32'),
            'INCLUDE':str(SP1/'VC/include')+';'+str(SP1/'SDK/Include'),
            'LIB':str(SP1/'VC/lib')+';'+str(SP1/'SDK/Lib'),'TMP':str(OUT),'TEMP':str(OUT)}

def validate(review,review_hash):
    need(review.get('kind')=='crt-v15-compile-link-review' and review.get('approved') is True and
         review.get('allow_execute') is False and review.get('reviewer'), 'independent exact review absent')
    need(review.get('driver_sha256')==sha(__file__) and review.get('job_helper_sha256')==sha(base.__file__), 'driver/helper identity')
    need(review.get('commands')==commands() and review.get('output')==str(OUT) and review.get('phase_seconds')==90 and
         review.get('job_memory_bytes')==1024**3 and review.get('log_limit_bytes')==LIMIT,'operation scope differs')
    need(review.get('environment')==environment(os.environ['SystemRoot']), 'environment differs')
    pins=review.get('inputs'); need(type(pins) is dict and pins, 'input pins absent')
    required=[SRC,SP1/'VC/bin/cl.exe',SP1/'VC/bin/link.exe',SP1/'VC/bin/c1xx.dll',SP1/'VC/bin/c2.dll',
              SP1/'VC/lib/libcmt.lib',SP1/'VC/lib/oldnames.lib',SP1/'SDK/Lib/kernel32.lib']
    # Pin every compiler-directory DLL and every library that the fixed LIB
    # search path can select; review must also bind their complete roster.
    for folder, suffix in ((SP1/'VC/bin', '.dll'), (SP1/'VC/lib', '.lib'), (SP1/'SDK/Lib', '.lib')):
        required.extend(p for p in folder.iterdir() if p.is_file() and p.suffix.lower()==suffix)
    need(all(str(p) in pins for p in required), 'required input pins absent')
    need(review.get('search_roster')==sorted(str(p) for p in required), 'search roster differs')
    base.verify_inputs({'inputs':pins})
    binding={'owner':review['owner'],'slot':review['slot'],'lease_pins':review['lease_pins'],'review_sha256':review_hash}
    return binding

class Windows(base.Windows):
    def start_logged(self,command,cwd,job,env,stdout,stderr):
        import msvcrt
        # File handles are inherited only through the explicit handle list.
        null=open(os.devnull,'rb'); opened=[null,stdout,stderr]
        handles=[msvcrt.get_osfhandle(x.fileno()) for x in opened]
        for h in handles: os.set_handle_inheritable(h,True)
        size=base.SIZE(); k=self.k; memory=None
        try:
            ok=k.InitializeProcThreadAttributeList(None,2,0,ctypes.byref(size))
            need(not ok and ctypes.get_last_error()==122 and 0<size.value<=1024*1024,'attribute sizing')
            memory=ctypes.create_string_buffer(size.value);ptr=ctypes.cast(memory,ctypes.c_void_p)
            need(k.InitializeProcThreadAttributeList(ptr,2,0,ctypes.byref(size)),'attribute init')
            try:
                jobs=(base.HANDLE*1)(job); inherited=(base.HANDLE*3)(*handles)
                need(k.UpdateProcThreadAttribute(ptr,0,0x2000d,ctypes.byref(jobs),ctypes.sizeof(jobs),None,None),'job list')
                need(k.UpdateProcThreadAttribute(ptr,0,0x20002,ctypes.byref(inherited),ctypes.sizeof(inherited),None,None),'handle list')
                startup=base.StartupEx();startup.startup.cb=ctypes.sizeof(startup);startup.attributes=ptr
                startup.startup.flags=0x100;startup.startup.stdin=handles[0];startup.startup.stdout=handles[1];startup.startup.stderr=handles[2]
                cmd=ctypes.create_unicode_buffer(subprocess.list2cmdline(command))
                block=ctypes.create_unicode_buffer('\0'.join(k+'='+env[k] for k in sorted(env,key=str.upper))+'\0\0')
                p=base.ProcessInfo()
                need(k.CreateProcessW(command[0],cmd,None,None,True,0x4|0x08000000|0x80000|0x400,
                    ctypes.cast(block,ctypes.c_void_p),str(cwd),ctypes.byref(startup),ctypes.byref(p)), 'CreateProcess outcome unknown')
                return p
            finally:k.DeleteProcThreadAttributeList(ptr)
        finally:
            for h in handles: os.set_handle_inheritable(h,False)
            null.close()

def save(name,row): base.save_new(OUT/name,row)
def phase(index,review,binding,grant,backend):
    label=('compile','link')[index]; cmd=commands()[index]
    save(label+'-intent.json',{'state':'UNKNOWN','command':cmd,'review_sha256':binding['review_sha256']})
    job=child=None; closed=False; code=None; reason=None; drained=False; start=time.monotonic()
    try:
        need(base.lease(binding)==grant and base.lease_remaining(grant)>92,'lease too short/changed')
        base.verify_inputs({'inputs':review['inputs']})
        job=backend.create_job(review['nested_parent_allowed'],1024**3)
        with (OUT/(label+'.stdout')).open('xb') as so,(OUT/(label+'.stderr')).open('xb') as se:
            child=backend.start_logged(cmd,OUT,job,review['environment'],so,se)
            created=backend.creation(child);backend.assign(job,child)
            save(label+'-started.json',{'pid':int(child.pid),'creation_time':created,'state':'suspended-in-job'})
            need(base.lease(binding)==grant and backend.creation(child)==created,'lease or identity changed')
            base.verify_inputs({'inputs':review['inputs']});backend.resume(child)
            while True:
                need(time.monotonic()-start<90 and base.lease_remaining(grant)>1,'deadline')
                need(base.lease(binding)==grant,'lease changed')
                need(os.fstat(so.fileno()).st_size+os.fstat(se.fileno()).st_size<=LIMIT,'monitored log limit')
                if code is None: code=backend.poll(child)
                if code is not None and not backend.census(job): drained=True;break
                time.sleep(.05)
            need(code==0,'native command failed')
            need(os.fstat(so.fileno()).st_size+os.fstat(se.fileno()).st_size<=LIMIT,'terminal log limit')
            base.verify_inputs({'inputs':review['inputs']})
    except BaseException as e:
        reason=type(e).__name__+': '+str(e)
        if child is not None:
            try:
                backend.terminate_job(job);code=backend.wait(child)
                until=time.monotonic()+10
                while backend.census(job):
                    need(time.monotonic()<until,'job drain timeout');time.sleep(.05)
                drained=True
            except BaseException as stop:reason+='; termination uncertain: '+type(stop).__name__
    finally:
        if child is not None:
            try:backend.close_process(child);closed=True
            except BaseException as e:reason=(reason or '')+'; process close uncertain: '+type(e).__name__
        if job is not None:
            try:backend.close_job(job)
            except BaseException as e:reason=(reason or '')+'; job close uncertain: '+type(e).__name__
    result={'state':'completed-unreviewed' if reason is None and drained and closed else 'failed-or-unknown',
       'reason':reason,'pid':int(child.pid) if child else None,'returncode':code,'job_empty_observed':drained,
       'elapsed_seconds':time.monotonic()-start,'log_limit_is_sampled':True,'executed_fixture':False}
    save(label+'-terminal.json',result);return result

def run(path,expected_hash):
    need(os.name=='nt','Windows required');path=Path(path).resolve(strict=True)
    need(sha(path)==expected_hash,'review digest differs');review=json.loads(path.read_text())
    binding=validate(review,expected_hash);grant=base.lease(binding)
    need(base.lease_remaining(grant)>185,'lease insufficient for two phases');OUT.mkdir()
    save('operation-intent.json',{'state':'UNKNOWN','review_sha256':expected_hash})
    backend=Windows();r=phase(0,review,binding,grant,backend)
    if r['state']!='completed-unreviewed':return
    need((OUT/'fixture.obj').is_file(),'compiled object absent')
    need(sha(path)==expected_hash and validate(review,expected_hash)==binding,'review drift')
    r=phase(1,review,binding,grant,backend)
    if r['state']=='completed-unreviewed':
        need((OUT/'fixture.exe').is_file() and (OUT/'fixture.map').is_file(),'link output absent')
        save('receipt.json',{'state':'completed-unreviewed','review_sha256':expected_hash,
             'artifact_sha256':{n:sha(OUT/n) for n in ('fixture.obj','fixture.exe','fixture.map','compile.stdout','compile.stderr','link.stdout','link.stderr')},'fixture_executed':False})

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('usage: driver REVIEW_PATH TRUSTED_REVIEW_SHA256')
    run(sys.argv[1],sys.argv[2].lower())
