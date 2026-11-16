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
import json
import os
import threading
from pathlib import Path

FIXED_PROFILE=None
SOURCE_PINS=None
PREPARATION_PEERS=None
WATCHDOG_REVIEW=None


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


def _start_held_link(profile):
    """Actual lpApplicationName/Job/pipe/lease adapter deliberately unimplemented."""
    raise RuntimeError('reviewed successor held LINK process adapter unavailable')


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


def _publish_fixture(profile, result, capture, guard):
    """Save both partial logs before a terminal record; interrupted means UNKNOWN."""
    output=Path(profile['output_directory']);guard.check('publish-before')
    stdout=capture['stdout'];stderr=capture['stderr']
    require(type(stdout) is bytes and type(stderr) is bytes, 'captured logs required')
    stdout_sha=_write_new(output/'link.stdout.txt',stdout)
    stderr_sha=_write_new(output/'link.stderr.txt',stderr)
    guard.check('publish-after-logs')
    receipt=dict(result,stdout_sha256=stdout_sha,stderr_sha256=stderr_sha,
                 logs_complete=True,native_link_operation_approved=False,
                 provider_selected=False,runtime_eligible=False,executable_execution=False)
    terminal_sha=_write_new(output/'terminal.json',canonical(receipt)+b'\n')
    guard.check('publish-after-terminal')
    _write_new(output/'completion.json',canonical({'kind':'successor-link-completion-candidate',
                'terminal_sha256':terminal_sha,'independent_outcome_review_required':True})+b'\n')
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
    try:process=_start_held_link(profile)
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
        return _publish_fixture(profile,result,captured['capture'],guard)
    except BaseException as exc:
        if not exited:terminate_once('workflow-exception')
        return {'status':'UNKNOWN','reservation_sha256':reservation,'capture':captured,
                'reason':'workflow-'+type(exc).__name__,'termination':termination_snapshot(),
                'process_success_established':False}



def run():
    raise RuntimeError('held LINK disabled: exact independent peers, fixed runtime and issued Job adapter unavailable')


if __name__=='__main__':run()
