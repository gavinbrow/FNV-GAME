"""Successor LINK held-workflow wiring; real entry intentionally disabled.

This source is not an authenticated launcher. It wires test seams to the V14
D.stable/identity/select_libraries/classify interfaces and cooperative V3's
operation-ID reservation, forecast, sampled monitor and bounded capture. The
independent peer verifier, successor held Job process adapter, fixed-source
loader and trusted live lease/handle guards are not yet available. No arbitrary
approval is accepted and run() always fails. No native process is launched here.
All fixture inputs/callbacks are unauthenticated and cannot authorize operation.
"""
import _thread
import hashlib
import importlib
import json
import os
import re
import threading
import sys
from pathlib import Path

FIXED_PROFILE=None
SOURCE_PINS=None
PREPARATION_PEERS=None
WATCHDOG_REVIEW=None
ROOT=Path(__file__).resolve().parents[2]
REQUIRED_MODULE_PATHS={
    'application_link_diagnostic':'tools/rebuild/application_link_diagnostic.py',
    'application_successor_cooperative_link_v4':'tools/rebuild/application_successor_cooperative_link_v4.py',
    'successor_bounded_capture_v3':'tools/rebuild/successor_bounded_capture_v3.py',
    'successor_windows_held_link_adapter_v4':'tools/rebuild/successor_windows_held_link_adapter_v4.py',
    'factory_held_launcher_v1':'tools/rebuild/factory_held_launcher_v1.py',
    'factory_job_launcher':'tools/rebuild/factory_job_launcher.py',
}
MAX_OUTPUT_BYTES=128*1024*1024
CONTROL_RESERVE_BYTES=8*1024*1024
MAX_FINAL_RECEIPT_BYTES=64*1024


def require(ok,message):
    if not ok:raise ValueError(message)


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')


def _verify_peers(profile):
    """Real exact successor schemas and hashes have not been independently accepted."""
    raise RuntimeError('successor peer verifier and accepted pins unavailable')


def _require_successor_held_guard(profile,guard):
    """Factory Guard is 15-selection-specific; no successor capability exists yet."""
    raise RuntimeError('successor issued held Job capability unavailable')


def _verify_job_terminal(profile,process,evidence):
    """Independent held-process, Job-empty and teardown capability unavailable."""
    raise RuntimeError('authenticated whole-Job exit verifier unavailable')


def _fixed_module(name):
    """Verify the fixed snapshot/finder relation; not a whole-runtime proof."""
    require(type(SOURCE_PINS) is dict and set(SOURCE_PINS)==set(REQUIRED_MODULE_PATHS) and
            name in REQUIRED_MODULE_PATHS and sys.meta_path,'exact source pins unavailable')
    pin=SOURCE_PINS[name];finder=sys.meta_path[0]
    require(type(pin) is dict and set(pin)=={'path','sha256'} and pin['path']==REQUIRED_MODULE_PATHS[name] and
            type(pin['sha256']) is str and len(pin['sha256'])==64 and
            all(c in '0123456789abcdef' for c in pin['sha256']), 'fixed module pin differs')
    snapshot=getattr(finder,'snapshots',{}).get(name)
    require(type(snapshot) is bytes and hashlib.sha256(snapshot).hexdigest()==pin['sha256'] and
            getattr(finder,'paths',{}).get(name)==str(ROOT/pin['path']), 'fixed module snapshot differs')
    module=importlib.import_module(name)
    require(getattr(module,'__loader__',None) is finder and sys.meta_path[0] is finder,
            'fixed module loader differs')
    return module


def _verify_start_authority(profile):
    """Independent exact fixed profile, path, source and active lease remain unavailable."""
    raise RuntimeError('authenticated held-start authority unavailable')


def _record_suspended_child(profile,created):
    """Durable child identity and external once-marker protocol remain unavailable."""
    raise RuntimeError('durable suspended-child receipt unavailable')


def _verify_before_resume(profile,created,guard):
    """Fresh actual held Job, lease, source and physical path checks unavailable."""
    raise RuntimeError('authenticated pre-resume verifier unavailable')


def _open_capture_streams(profile,bundle):
    """Owned Win32 read-handle conversion and lifetime remain unavailable."""
    raise RuntimeError('capture read-handle adapter unavailable')


class _HeldProcess:
    """Fixture facade; authentic Job teardown/empty validation remains blocked."""
    def __init__(self,kernel,job,created,stdout,stderr):
        self.kernel=kernel;self.job=job;self.created=created;self.stdout=stdout;self.stderr=stderr
    def terminate_job(self,reason):self.kernel.terminate_job(self.job)
    def wait_for_job_exit(self,seconds):
        raise RuntimeError('authenticated bounded whole-Job exit adapter unavailable')


class _RecoveryOwnerFixture:
    """Strong in-process retention for synthetic returned capabilities only.

    This does not cover a process created inside an adapter that never returns.
    Nothing here resumes, closes, retries or proves operating-system ownership.
    """
    def __init__(self):
        self._lock=threading.Lock();self._owned={}
    def adopt(self,operation_id,*,kernel,job,pipes,bundle,created):
        require(type(operation_id) is str and re.fullmatch('[a-z0-9_-]{1,80}',operation_id) and
                type(created) is dict and created.get('status') in ('UNKNOWN','suspended-unreviewed') and
                'process_info' in created and created.get('job_handle')==job,
                'exact synthetic recovery capability required')
        with self._lock:
            require(operation_id not in self._owned,'operation capability already owned')
            self._owned[operation_id]={'kernel':kernel,'job':job,'pipes':pipes,'bundle':bundle,'created':created}
    def contains_exact(self,operation_id,*,kernel,job,pipes,bundle,created):
        with self._lock:
            item=self._owned.get(operation_id)
            return item is not None and item['kernel'] is kernel and item['job']==job and item['pipes'] is pipes and \
                   item['bundle'] is bundle and item['created'] is created


def _unknown_receipt_fixture(operation_id,profile_sha256,response_sha256,job_name,child_identity):
    """Redacted stable metadata only: no process, Job or pipe handles."""
    require(type(operation_id) is str and re.fullmatch('[a-z0-9_-]{1,80}',operation_id) and
            all(type(x) is str and re.fullmatch('[0-9a-f]{64}',x) for x in (profile_sha256,response_sha256)) and
            type(job_name) is str and job_name, 'unknown receipt binding differs')
    child=None
    if child_identity is not None:
        require(type(child_identity) is dict and set(child_identity)=={'pid','creation','image'} and
                type(child_identity['pid']) is int and child_identity['pid']>0 and
                type(child_identity['creation']) is int and child_identity['creation']>0 and
                type(child_identity['image']) is str and child_identity['image'], 'child identity differs')
        child={'pid':child_identity['pid'],'creation':child_identity['creation'],
               'image_sha256':hashlib.sha256(child_identity['image'].encode('utf-8')).hexdigest()}
    return {'kind':'successor-held-recovery','state':'UNKNOWN','operation_id':operation_id,
            'profile_sha256':profile_sha256,'response_sha256':response_sha256,'job_name':job_name,
            'child':child,'raw_handles_recorded':False,'recovery_authorized':False}


def _persist_unknown_fixture(path,record):
    require(type(record) is dict and set(record)=={'kind','state','operation_id','profile_sha256',
            'response_sha256','job_name','child','raw_handles_recorded','recovery_authorized'} and
            record['kind']=='successor-held-recovery' and record['state']=='UNKNOWN' and
            record['raw_handles_recorded'] is False and record['recovery_authorized'] is False and
            type(record['operation_id']) is str and re.fullmatch('[a-z0-9_-]{1,80}',record['operation_id']) and
            all(type(record[k]) is str and re.fullmatch('[0-9a-f]{64}',record[k]) for k in ('profile_sha256','response_sha256')) and
            type(record['job_name']) is str and 0<len(record['job_name'])<=256, 'exact unknown receipt required')
    child=record['child']
    require(child is None or (type(child) is dict and set(child)=={'pid','creation','image_sha256'} and
            type(child['pid']) is int and child['pid']>0 and type(child['creation']) is int and child['creation']>0 and
            type(child['image_sha256']) is str and re.fullmatch('[0-9a-f]{64}',child['image_sha256'])),
            'redacted child identity required')
    return _write_new(path,canonical(record)+b'\n')


def _require_atomic_recovery_transfer(profile):
    """Hard stop before Job, pipe or process creation.

    Adapter V4 returns handles only after CreateProcessW and can be interrupted
    before an in-process owner receives them. Its API cannot establish atomic
    pre-creation ownership or survive process death. A future independently
    reviewed held launcher must close this gap before replacing this hard stop.
    """
    raise RuntimeError('atomic pre-creation recovery ownership unavailable')


def _start_held_link(profile,guard):
    """Wire exact adapter only after fixed authority; failures remain UNKNOWN."""
    _verify_start_authority(profile)
    _require_atomic_recovery_transfer(profile)
    adapter=_fixed_module('successor_windows_held_link_adapter_v4')
    base=_fixed_module('factory_job_launcher');held=_fixed_module('factory_held_launcher_v1')
    kernel=held.native(base);job=kernel.named_job(profile['job_name'])
    pipes=adapter.WindowsPipeBackend(kernel.k,base)
    bundle=adapter._open_pipe_bundle_fixture(pipes)
    created=adapter._create_suspended_fixture(base,kernel,linker_path=profile['linker_path'],
        response_path=profile['response_path'],cwd=profile['working_directory'],environment=profile['environment'],
        expected_lib=profile['expected_lib'],job=job,job_name=profile['job_name'],bundle=bundle)
    # A failed/uncertain creation is never resumed or retried. Job, process and
    # pipe ownership remain with an external reconciler, not blind close calls.
    require(type(created) is dict and created.get('status')=='suspended-unreviewed','held creation UNKNOWN')
    _record_suspended_child(profile,created)
    _verify_before_resume(profile,created,guard)
    stdout,stderr=_open_capture_streams(profile,bundle)
    adapter._close_parent_child_ends_fixture(pipes,bundle)
    kernel.resume(created['process_info'])
    return _HeldProcess(kernel,job,created,stdout,stderr)


def _run_fixed(profile,guard):
    """Fixed module binding in an externally authenticated source session."""
    diagnostic=_fixed_module('application_link_diagnostic')
    cooperative=_fixed_module('application_successor_cooperative_link_v4')
    capture_module=_fixed_module('successor_bounded_capture_v3')
    job_module=_fixed_module('factory_job_launcher')
    return _run_fixture(profile,diagnostic=diagnostic,guard=guard,cooperative=cooperative,
                        capture_module=capture_module,job_module=job_module)


def _stable_snapshot(profile,diagnostic,guard):
    """Run original V14 stability delegate and recheck response separately."""
    guard.check('snapshot-before')
    diagnostic.stable(profile['input_bindings'])
    response=diagnostic.identity(profile['response_path'])
    require(response['sha256']==profile['response_sha256'] and
            response['requested_path']==profile['response_path'], 'response physical identity differs')
    libraries=diagnostic.select_libraries(Path(profile['output_directory']),Path(profile['compiler_lib']),
                                          Path(profile['sdk_lib']))
    require(libraries==profile['default_libraries'],'default library identity differs')
    guard.check('snapshot-after')
    return {'response':response,'default_libraries':libraries}


def _write_new(path,data):
    with Path(path).open('xb') as stream:
        stream.write(data);stream.flush();os.fsync(stream.fileno())
    require(Path(path).read_bytes()==data,'output readback differs')
    return hashlib.sha256(data).hexdigest()


def _publish_fixture(profile, result, capture, guard, job_module):
    """Prebound serialized payload and sample actual tree before completion.

    Polling is MONITORED, not a hard quota. Existing artifacts are never replaced.
    The final independent outcome review still must verify all samples and pins.
    """
    output=Path(profile['output_directory']);guard.check('publish-before')
    stdout=capture['stdout'];stderr=capture['stderr']
    require(type(stdout) is bytes and type(stderr) is bytes and
            len(stdout)+len(stderr)<=profile['capture_bytes'], 'captured log bound differs')
    required={'link.stdout.txt','link.stderr.txt','terminal.json','completion.json','final.json'}
    require(required.issubset(set(profile['allowed_outputs'])), 'publication paths not monitored')
    receipt=dict(result,stdout_sha256=hashlib.sha256(stdout).hexdigest(),
                 stderr_sha256=hashlib.sha256(stderr).hexdigest(),logs_complete=True,
                 native_link_operation_approved=False,provider_selected=False,runtime_eligible=False,
                 executable_execution=False)
    # This serialization occurs before the size check: no peak-RSS bound is
    # claimed. A reviewed bounded serializer or independent memory sizing is
    # required before enabling the actual launcher.
    terminal=canonical(receipt)+b'\n';terminal_sha=hashlib.sha256(terminal).hexdigest()
    completion=canonical({'kind':'successor-link-completion-candidate','terminal_sha256':terminal_sha,
                          'independent_outcome_review_required':True})+b'\n'
    control_expected=dict(profile['control_expected'])
    reservation_name=profile['operation_id']+'.json'
    require(reservation_name not in control_expected,'reservation control conflict')
    control_expected[reservation_name]=result['reservation_sha256']
    def sample():
        control_used=job_module.control_guard(profile['control_directory'],control_expected)
        output_used=job_module.owned_size(output,profile['allowed_outputs'])
        require(type(control_used) is int and control_used>=0 and type(output_used) is int and output_used>=0,
                'actual monitored aggregate differs')
        return control_used,output_used
    control_used,output_used=sample()
    require(control_used+len(terminal)+len(completion)+MAX_FINAL_RECEIPT_BYTES<=CONTROL_RESERVE_BYTES and
            control_used+output_used+len(stdout)+len(stderr)+len(terminal)+len(completion)+MAX_FINAL_RECEIPT_BYTES<=MAX_OUTPUT_BYTES,
            'serialized publication exceeds reviewed cap or reserve')
    _write_new(output/'link.stdout.txt',stdout)
    _write_new(output/'link.stderr.txt',stderr)
    guard.check('publish-after-logs')
    _write_new(output/'terminal.json',terminal)
    guard.check('publish-after-terminal')
    control_final,output_final=sample()
    require(control_final+len(terminal)+len(completion)+MAX_FINAL_RECEIPT_BYTES<=CONTROL_RESERVE_BYTES and
            control_final+output_final+len(completion)+MAX_FINAL_RECEIPT_BYTES<=MAX_OUTPUT_BYTES, 'final monitored aggregate exceeds cap')
    guard.check('publish-after-final-sample')
    _write_new(output/'completion.json',completion)
    # Completion is a candidate only, never final authority.
    guard.check('publish-after-completion')
    control_post,output_post=sample()
    final=canonical({'kind':'successor-link-final-candidate','terminal_sha256':terminal_sha,
                     'completion_sha256':hashlib.sha256(completion).hexdigest(),
                     'post_completion_control_bytes':control_post,'post_completion_output_bytes':output_post,
                     'monitoring':'MONITORED','independent_outcome_review_required':True})+b'\n'
    require(len(final)<=MAX_FINAL_RECEIPT_BYTES and
            control_post+len(terminal)+len(completion)+len(final)<=CONTROL_RESERVE_BYTES and
            control_post+output_post+len(final)<=MAX_OUTPUT_BYTES, 'post-completion monitored aggregate exceeds cap')
    guard.check('publish-after-post-completion-sample')
    require((output/'link.stdout.txt').read_bytes()==stdout and (output/'link.stderr.txt').read_bytes()==stderr and
            (output/'terminal.json').read_bytes()==terminal and (output/'completion.json').read_bytes()==completion,
            'published candidate drift')
    _write_new(output/'final.json',final)
    return receipt


def _run_fixture(profile,*,diagnostic,guard,cooperative,capture_module,job_module):
    """Synthetic integration seam, NEVER a caller-authorized production entry.

    Future entry must load exact fixed modules through the authenticated finder,
    validate physical path identities, issued held capability and peer schemas,
    and keep the parent Job/lease alive. All parameterized objects here exist
    solely so mock tests can exercise ordering; they are not trust anchors.
    """
    _verify_peers(profile);_require_successor_held_guard(profile,guard)
    cooperative._forecast_fixture(forecast_bytes=profile['forecast_bytes'],existing_bytes=profile['existing_bytes'])
    guard.check('before-reservation')
    reservation=cooperative._reserve_fixture(profile['reservation_root'],profile['operation_id'],
                                             profile['profile_sha256'],profile['response_sha256'])
    try:pre=_stable_snapshot(profile,diagnostic,guard)
    except BaseException as exc:
        return {'status':'UNKNOWN','reservation_sha256':reservation,'capture':None,
                'reason':'preflight-'+type(exc).__name__,'process_success_established':False}
    try:process=_start_held_link(profile,guard)
    except BaseException as exc:
        return {'status':'UNKNOWN','reservation_sha256':reservation,'capture':None,
                'reason':'held-start-'+type(exc).__name__,'process_success_established':False}
    termination_lock=threading.Lock();termination_done=threading.Event()
    termination={'requested':False,'returned':False,'error':None};exited=False;captured=None
    def terminate_once(reason):
        with termination_lock:
            if termination['requested']:return
            termination['requested']=True
        def invoke():
            try:
                process.terminate_job(reason)
                with termination_lock:termination['returned']=True
            except BaseException as exc:
                with termination_lock:termination['error']=type(exc).__name__
            finally:termination_done.set()
        try:_thread.start_new_thread(invoke,())
        except BaseException as exc:
            with termination_lock:termination['error']='ThreadStart:'+type(exc).__name__
            termination_done.set()
    def termination_snapshot():
        if termination['requested']:
            termination_done.wait(max(0,min(float(profile['cleanup_seconds']),5.0)))
        with termination_lock:return dict(termination)
    def wait_and_verify_job(remaining):
        evidence=process.wait_for_job_exit(remaining)
        guard.check('before-job-verification')
        _verify_job_terminal(profile,process,evidence)
        require(type(evidence) is dict and type(evidence.get('returncode')) is int,'unobserved process exit')
        guard.check('after-job-verification')
        return evidence
    try:
        captured=cooperative._monitor_capture_fixture(process.stdout,process.stderr,
            output=profile['output_directory'],allowed_outputs=profile['allowed_outputs'],capture_module=capture_module,
            job_module=job_module,terminate=terminate_once,byte_cap=profile['capture_bytes'],
            timeout_seconds=profile['timeout_seconds'],cleanup_seconds=profile['cleanup_seconds'],
            wait_for_job_exit=wait_and_verify_job)
        # Incomplete monitoring or process ownership uncertainty is never terminal.
        if captured['status']!='capture_and_samples_complete':
            terminate_once('capture-incomplete')
            return {'status':'UNKNOWN','reservation_sha256':reservation,'capture':captured,
                    'reason':'capture-or-monitored-output-incomplete','termination':termination_snapshot(),
                    'process_success_established':False}
        job_evidence=captured['job_exit_evidence']
        returncode=job_evidence['returncode'];exited=True
        post=_stable_snapshot(profile,diagnostic,guard)
        require(post==pre,'response or libraries changed')
        text=captured['capture']['stdout'].decode('utf-8',errors='replace')+'\n'+captured['capture']['stderr'].decode('utf-8',errors='replace')
        errors=diagnostic.diagnostic_errors(text,profile['provenance'])
        classification=diagnostic.classify(returncode,errors)
        result={'kind':'successor-link-observation','status':'observed-unreviewed','reservation_sha256':reservation,
                'returncode':returncode,'job_exit_evidence':job_evidence,'classification':classification,'errors':errors,'response_pre':pre,
                'response_post':post,'input_bindings':profile['input_bindings'],'monitoring':'MONITORED',
                'hard_disk_quota':False,'process_success_established':False}
        return _publish_fixture(profile,result,captured['capture'],guard,job_module)
    except BaseException as exc:
        if not exited:terminate_once('workflow-exception')
        return {'status':'UNKNOWN','reservation_sha256':reservation,'capture':captured,
                'reason':'workflow-'+type(exc).__name__,'termination':termination_snapshot(),
                'process_success_established':False}



def run():
    raise RuntimeError('held LINK disabled: exact independent peers, fixed runtime and issued Job adapter unavailable')


if __name__=='__main__':run()
