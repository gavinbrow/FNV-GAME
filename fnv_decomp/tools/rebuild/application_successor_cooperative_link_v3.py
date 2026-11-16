"""Cooperative successor LINK primitives; no configured live operation.

Exact successor prepare/peers, source/runtime pins and held LINK launcher are
not accepted yet. run() is deliberately disabled. The primitives below are
synthetic seams: fixed reviewed callers must authenticate root, paths, modules,
lease and process handles. Filesystem checks are monitored samples, not quota;
no process success, hard disk bound or crash durability is established.
"""
import _thread
import hashlib
import json
import math
import os
from pathlib import Path
import re
import threading
import time

FIXED_PROFILE=None
SOURCE_REVIEW=None
PREPARATION_REVIEW=None
WATCHDOG_REVIEW=None
MAX_OUTPUT_BYTES=128*1024*1024
CONTROL_RESERVE_BYTES=8*1024*1024
MAX_SAMPLE_BYTES=4*1024*1024
MAX_SAMPLES=20000


def require(ok,message):
    if not ok:raise ValueError(message)


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')


def _digest(value):return type(value) is str and re.fullmatch('[0-9a-f]{64}',value) is not None


def _reserve_fixture(root,operation_id,profile_sha256,response_sha256):
    """Exclusive operation-ID key on a cooperative pre-established directory.

    This does not establish cross-host locking, root authenticity or namespace
    durability across power loss; those require independent evidence. Existing
    or partial files block every retry, including a changed profile/response.
    """
    require(type(operation_id) is str and re.fullmatch('[a-z0-9_-]{1,80}',operation_id) and
            _digest(profile_sha256) and _digest(response_sha256), 'exact canonical operation identity required')
    root=Path(root);require(root.is_dir(),'pre-established reservation root required')
    path=root/(operation_id+'.json')
    record={'kind':'successor-link-reservation','operation_id':operation_id,'profile_sha256':profile_sha256,
            'response_sha256':response_sha256,'state':'UNKNOWN'}
    data=canonical(record)+b'\n'
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'wb') as stream:
        stream.write(data);stream.flush();os.fsync(stream.fileno())
    require(path.read_bytes()==data,'reservation readback differs')
    return hashlib.sha256(data).hexdigest()


def _forecast_fixture(*, forecast_bytes,existing_bytes,output_cap=MAX_OUTPUT_BYTES,
                      control_reserve=CONTROL_RESERVE_BYTES):
    """Reject forecasts over the unchanged output budget; forecast is not evidence of a bound."""
    require(all(type(x) is int and x>=0 for x in (forecast_bytes,existing_bytes,output_cap,control_reserve)) and
            output_cap==MAX_OUTPUT_BYTES and control_reserve==CONTROL_RESERVE_BYTES and
            existing_bytes+forecast_bytes+control_reserve<=output_cap, 'forecast exceeds reviewed budget')
    return {'forecast_bytes':forecast_bytes,'existing_bytes':existing_bytes,'output_cap':output_cap,
            'control_reserve':control_reserve,'enforcement':'MONITORED','hard_disk_quota':False}


def _monitor_capture_fixture(stdout,stderr,*,output,allowed_outputs,capture_module,job_module,terminate,
                             byte_cap,timeout_seconds,cleanup_seconds=2.0,sample_seconds=.05):
    """Connect existing capture to sampled `owned_size`; not an authority seam.

    Fixed production source must pin and authenticate modules and own handles.
    Both stop paths share a once-only teardown request. Counts and samples stop
    at return; a blocked sample/callback is reported, never claimed terminated.
    """
    require(callable(terminate) and type(sample_seconds) in (int,float) and 0<sample_seconds<=1 and
            math.isfinite(sample_seconds) and type(timeout_seconds) in (int,float) and
            0<timeout_seconds<=180 and math.isfinite(timeout_seconds) and type(cleanup_seconds) in (int,float) and
            0<=cleanup_seconds<=5 and math.isfinite(cleanup_seconds) and type(allowed_outputs) is list and
            type(byte_cap) is int and 0<=byte_cap<=MAX_OUTPUT_BYTES-CONTROL_RESERVE_BYTES,
            'bounded monitored capture scope required')
    lock=threading.Lock();stop=threading.Event();requested=threading.Event();termination_done=threading.Event()
    state={'reason':None,'samples':[],'sample_bytes':0,'monitor_error':None,'termination_error':None,
           'dispatch_resolved':False,'callback_started':False,'callback_finished':False,
           'callback_returned':False,'closed':False}
    def request_once(reason):
        with lock:
            if state['closed'] or requested.is_set():return
            requested.set();state['reason']=reason
        def execute():
            invoked=False
            try:
                with lock:
                    if state['closed']:return
                    state['callback_started']=True;invoked=True
                terminate(reason)
                with lock:
                    if not state['closed']:state['callback_returned']=True
            except BaseException as exc:
                with lock:
                    if not state['closed']:state['termination_error']=type(exc).__name__
            finally:
                with lock:
                    if invoked and not state['closed']:state['callback_finished']=True
                termination_done.set()
        try:
            _thread.start_new_thread(execute,())
            with lock:state['dispatch_resolved']=True
        except BaseException as exc:
            with lock:
                state['termination_error']='ThreadStart:'+type(exc).__name__
                state['dispatch_resolved']=True
            termination_done.set()

    def monitor():
        try:
            while not stop.is_set():
                observed=job_module.owned_size(output,allowed_outputs)
                require(type(observed) is int and observed>=0,'invalid observed size')
                sample={'output_bytes':observed}
                with lock:
                    if state['closed']:return
                    state['sample_bytes']+=len(canonical(sample));state['samples'].append(sample)
                    require(state['sample_bytes']<=MAX_SAMPLE_BYTES and len(state['samples'])<=MAX_SAMPLES,
                            'sample ledger cap')
                # Reserve the full in-memory capture cap in case it is later
                # persisted beside outputs; samples still do not enforce disk quota.
                if observed+CONTROL_RESERVE_BYTES+byte_cap>MAX_OUTPUT_BYTES:
                    request_once('output_watermark');return
                stop.wait(sample_seconds)
        except BaseException as exc:
            with lock:
                if not state['closed']:state['monitor_error']=type(exc).__name__
            request_once('monitor_failure')
    worker=threading.Thread(target=monitor,name='successor-output-monitor',daemon=True)
    try:worker.start()
    except BaseException as exc:
        # The start may have launched before raising; retain/observe the attempt.
        request_once('monitor_start_failure');stop.set()
        deadline=time.monotonic()+max(0,min(float(cleanup_seconds),5.0))
        if worker.is_alive():worker.join(max(0.0,deadline-time.monotonic()))
        termination_done.wait(max(0.0,deadline-time.monotonic()))
        with lock:
            state['closed']=True
            return {'status':'incomplete','monitor_state':'MONITORED','monitor_start_error':type(exc).__name__,
                    'monitor_thread_alive':worker.is_alive(),'monitor_start_uncertain':True,
                    'termination_requested':requested.is_set(),'termination_dispatch_resolved':state['dispatch_resolved'],
                    'termination_callback_started':state['callback_started'],
                    'termination_callback_finished':state['callback_finished'],
                    'termination_returned':state['callback_returned'],
                    'outcome':'UNKNOWN','partial_capture_available':False,'termination_error':state['termination_error'],
                    'process_success_established':False,'hard_disk_quota':False}

    captured=None;capture_error=None
    try:
        captured=capture_module.capture(stdout,stderr,byte_cap=byte_cap,timeout_seconds=timeout_seconds,
                                        cleanup_seconds=cleanup_seconds,terminate=request_once)
        require(type(captured) is dict and captured.get('status') in ('captured','incomplete'), 'invalid capture result')
    except BaseException as exc:
        capture_error=type(exc).__name__;captured=None
        request_once('capture_exception')
    finally:
        stop.set();deadline=time.monotonic()+max(0,min(float(cleanup_seconds),5.0))
        worker.join(max(0.0,deadline-time.monotonic()))

    if requested.is_set():termination_done.wait(max(0.0,deadline-time.monotonic()))
    with lock:
        state['closed']=True;alive=worker.is_alive()
        return {'status':'incomplete' if requested.is_set() or alive or state['monitor_error'] or
                not state['samples'] or capture_error is not None or captured is None or captured.get('status')!='captured' else 'capture_and_samples_complete',
                'capture':captured,'capture_error':capture_error,'partial_capture_available':captured is not None,
                'outcome':'UNKNOWN','monitor_state':'MONITORED','samples':list(state['samples']),
                'monitor_error':state['monitor_error'],'monitor_thread_alive':alive,
                'termination_requested':requested.is_set(),'termination_reason':state['reason'],
                'termination_error':state['termination_error'],'termination_dispatch_resolved':state['dispatch_resolved'],
                'termination_callback_started':state['callback_started'],
                'termination_callback_finished':state['callback_finished'],'termination_returned':state['callback_returned'],
                'process_success_established':False,
                'hard_disk_quota':False,'capture_reserve_bytes':byte_cap,'between_samples_growth_bounded':False}


def run():
    raise RuntimeError('successor LINK disabled: accepted fixed profile/peers and authenticated launcher unavailable')


if __name__=='__main__':run()
