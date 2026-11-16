"""Reviewed once-only CRT fixture compiler/linker. Never runs the result.

Monitor limits are sampled, not hard disk quotas. Any interrupted operation or
missing terminal receipt requires reconciliation; output directory blocks retry.
"""
import ctypes, hashlib, json, os, re, subprocess, sys, time
from pathlib import Path
import factory_job_launcher as base

ROOT=Path(__file__).resolve().parents[2]
SP1=ROOT/'build/rebuild/toolchains/sp1'
SRC=ROOT/'runtime/probes/crt_v15_alias_fixture.cpp'
OUT=ROOT/'build/rebuild/crt-v15-alias-component-v3'
A='_fnv_undefined_86b5006e5d6d2a0348c632bbd16e24c66b0a3804def721a1235e0f2a4af3c7e9'
B='_fnv_undefined_d9896c4c820aa59aae9e417910a0bfa1c7374957003b682c2810dddb89febb3d'
LIMIT=4*1024*1024
TREE_LIMIT=128*1024*1024
RESERVE=8*1024*1024
REVIEW_PATH=None  # Fixed peer-approved path must be installed before any operation.
LEASE_SCOPE=None  # Fixed coordinator scope must be installed before any operation.
REVIEWER='/root/terra_integration_v15/operation_census_review'
LEASE_OWNER='/root/terra_integration_v15/startup_crt_fast'
PEER_PATH=ROOT/'build/rebuild/terra-integration-v15-review-crt-job-launcher-v1-independent-20261104.md'
PEER_SHA='5b9d4260e473b1d583bb56bb235df453fe6c7c376d0e4a3a0b92aca329142d4b'
HELPER_SHA='8bdabc1ae1b7852c0686e754032ecd249ad2b2f1e5e5a6a055eb1f3b10c3c2d7'
SOURCE_SHA='c37f82fea744ad096615ad7b8f4c9be16925063df22f4dda501412520d7a0a59'
CL_SHA='2954bed141f2f283e3109b2187406704a2d5cb6378cb3074f1b09bc5045d65c1'
LINK_SHA='db188969504987decffb77e15f64f1b7eb94215cea12aa6cd7901510bb21e804'
ALLOWED=('operation-intent.json','compile-intent.json','compile-started.json','compile-terminal.json',
 'link-intent.json','link-started.json','link-terminal.json','receipt.json',
 'compile.stdout','compile.stderr','link.stdout','link.stderr','fixture.obj','fixture.exe',
 'fixture.map','fixture.exe.manifest')

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
         review.get('allow_execute') is False and review.get('reviewer')==REVIEWER, 'independent exact review absent')
    need(review.get('driver_sha256')==sha(__file__) and review.get('job_helper_sha256')==HELPER_SHA==sha(base.__file__), 'driver/helper identity')
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
    anchors={str(SRC):SOURCE_SHA,str(SP1/'VC/bin/cl.exe'):CL_SHA,str(SP1/'VC/bin/link.exe'):LINK_SHA,
       str(SP1/'VC/bin/c1xx.dll'):'93380e0bc9505d70896ec06d973cf6e06e4a4f27ee61f5365df1c83353151a45',
       str(SP1/'VC/bin/c2.dll'):'e3dd31ec4cb066fdf27cea24efc37944bb9d6a2720e6310213217e571f288404',
       str(SP1/'VC/lib/libcmt.lib'):'bd9700d126d378f31f32736abc0c88cb08a8e0f0914acb6e2c8cbfd1ab99f411',
       str(SP1/'VC/lib/oldnames.lib'):'586557972e98e688993eb5a0a0f69996cbb2803cce9d276e8bf6ed61473d1048',
       str(SP1/'SDK/Lib/kernel32.lib'):'a739cdc6ebbf16d052ea7a02927081ba0574ea335eaa43b4c14b7ca8b837c15f'}
    need(all(pins.get(k)==v for k,v in anchors.items()),'fixed fixture or VC9 identity differs')
    need(sha(PEER_PATH)==PEER_SHA and review.get('peer_sha256')==PEER_SHA,'independent preliminary peer evidence differs')
    base.verify_inputs({'inputs':pins})
    need(review.get('owner')==LEASE_OWNER and review.get('scope')==LEASE_SCOPE,'fixed lease owner/scope differs')
    # The coordinator registry, not the review body, supplies lease pins.
    # This avoids a self-referential review digest.
    registry=json.loads(base.REGISTRY.read_text());rows=[x for x in registry['leases'] if x.get('owner')==LEASE_OWNER
       and x.get('resource')=='CPU_heavy' and x.get('slot')==review['slot']]
    need(len(rows)==1 and rows[0].get('scope')==LEASE_SCOPE,'coordinator lease scope differs')
    lp=rows[0]['input_pins'];need(lp.get(Path(__file__).name)==sha(__file__) and lp.get(PEER_PATH.name)==PEER_SHA
       and lp.get(Path(REVIEW_PATH).name)==review_hash,'lease must bind driver, peer and review')
    return {'owner':LEASE_OWNER,'slot':review['slot'],'lease_pins':lp,'review_sha256':review_hash}

class Windows(base.Windows):
    def start_logged(self,command,cwd,job,env,stdout,stderr,owned):
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
                # Transfer process handles before any fallible cleanup.
                owned.append(p)
                return p
            finally:k.DeleteProcThreadAttributeList(ptr)
        finally:
            for h in handles: os.set_handle_inheritable(h,False)
            null.close()

def save(name,row): base.save_new(OUT/name,row)
def object_identity():
    p=OUT/'fixture.obj'; st=p.stat(); digest=sha(p); end=p.stat()
    need((st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns)==(end.st_dev,end.st_ino,end.st_size,end.st_mtime_ns), 'object drift')
    return {'sha256':digest,'size':st.st_size,'device':st.st_dev,'inode':st.st_ino,'mtime_ns':st.st_mtime_ns}

def tree_guard():
    used=base.owned_size(OUT,ALLOWED)
    need(used<=TREE_LIMIT-RESERVE,'monitored aggregate output limit')
    return used

def phase(index,review,binding,grant,backend,object_pin=None):
    label=('compile','link')[index]; cmd=commands()[index]
    save(label+'-intent.json',{'state':'UNKNOWN','command':cmd,'review_sha256':binding['review_sha256'], 'object_identity':object_pin})
    job=child=None; owned=[]; closed=False; code=None; reason=None; drained=False; start=time.monotonic()
    try:
        need(base.lease(binding)==grant and base.lease_remaining(grant)>92,'lease too short/changed')
        base.verify_inputs({'inputs':review['inputs']});tree_guard()
        if index==1:need(object_pin is not None and object_identity()==object_pin,'object changed before LINK')
        job=backend.create_job(review['nested_parent_allowed'],1024**3)
        with (OUT/(label+'.stdout')).open('xb') as so,(OUT/(label+'.stderr')).open('xb') as se:
            child=backend.start_logged(cmd,OUT,job,review['environment'],so,se,owned)
            created=backend.creation(child);backend.assign(job,child)
            save(label+'-started.json',{'pid':int(child.pid),'creation_time':created,'state':'suspended-in-job'})
            need(base.lease(binding)==grant and backend.creation(child)==created,'lease or identity changed')
            base.verify_inputs({'inputs':review['inputs']});tree_guard()
            if index==1:need(object_identity()==object_pin,'object changed before LINK resume')
            backend.resume(child)
            while True:
                need(time.monotonic()-start<90 and base.lease_remaining(grant)>1,'deadline')
                need(base.lease(binding)==grant,'lease changed');tree_guard()
                need(os.fstat(so.fileno()).st_size+os.fstat(se.fileno()).st_size<=LIMIT,'monitored log limit')
                if code is None: code=backend.poll(child)
                if code is not None and not backend.census(job): drained=True;break
                time.sleep(.05)
            need(code==0,'native command failed')
            need(os.fstat(so.fileno()).st_size+os.fstat(se.fileno()).st_size<=LIMIT,'terminal log limit')
            base.verify_inputs({'inputs':review['inputs']});tree_guard()
            if index==1:need(object_identity()==object_pin,'object changed after LINK')
    except BaseException as e:
        reason=type(e).__name__+': '+str(e)
        if child is None and owned:child=owned[0]
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
       'elapsed_seconds':time.monotonic()-start,'log_limit_is_sampled':True,
       'aggregate_limit_bytes':TREE_LIMIT-RESERVE,'aggregate_limit_is_sampled':True,'executed_fixture':False}
    save(label+'-terminal.json',result);return result

def run(path,expected_hash):
    need(REVIEW_PATH is not None and LEASE_SCOPE is not None,'fixed reviewed policy not installed')
    need(os.name=='nt','Windows required');path=Path(path).resolve(strict=True)
    need(path==Path(REVIEW_PATH).resolve(strict=True),'fixed review path differs')
    need(sha(path)==expected_hash,'review digest differs');review=json.loads(path.read_text())
    binding=validate(review,expected_hash);grant=base.lease(binding)
    need(base.lease_remaining(grant)>185,'lease insufficient for two phases');OUT.mkdir()
    save('operation-intent.json',{'state':'UNKNOWN','review_sha256':expected_hash})
    backend=Windows();r=phase(0,review,binding,grant,backend)
    if r['state']!='completed-unreviewed':return
    need((OUT/'fixture.obj').is_file(),'compiled object absent')
    need(sha(path)==expected_hash and validate(review,expected_hash)==binding,'review drift')
    object_pin=object_identity()
    r=phase(1,review,binding,grant,backend,object_pin)
    if r['state']=='completed-unreviewed':
        need((OUT/'fixture.exe').is_file() and (OUT/'fixture.map').is_file(),'link output absent')
        raw=(OUT/'link.stdout').read_text(errors='replace')+'\n'+(OUT/'link.stderr').read_text(errors='replace')
        selected=re.findall(r'^\s*Loaded\s+(.+?\.lib)\(([^)]+)\)',raw,re.I|re.M)
        selected_evidence=[{'path':p,'member':member,'pinned_sha256':review['inputs'].get(p)} for p,member in selected]
        save('receipt.json',{'state':'completed-unreviewed','review_sha256':expected_hash,
             'link_object_identity':object_pin,'selected_library_evidence':selected_evidence,
             'selected_libraries_verified':bool(selected_evidence) and all(x['pinned_sha256'] for x in selected_evidence),
             'artifact_sha256':{n:sha(OUT/n) for n in ('fixture.obj','fixture.exe','fixture.map','compile.stdout','compile.stderr','link.stdout','link.stderr')},'fixture_executed':False})

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('usage: driver REVIEW_PATH TRUSTED_REVIEW_SHA256')
    run(sys.argv[1],sys.argv[2].lower())
