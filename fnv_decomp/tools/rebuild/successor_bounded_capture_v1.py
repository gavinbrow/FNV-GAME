"""Bounded two-stream capture primitive for future held LINK; not authority.

No process creation, filesystem writes, LINK invocation or production entry.
Callers must own/authenticate pipes, Job, termination and process outcome. Reader
threads continue draining after the shared retained-byte cap, while a once-only
termination request is dispatched. If a blocking read or termination callback
cannot finish by the bounded deadline, daemon workers may remain alive and the
result explicitly says capture/termination is uncertain. An OS-specific owner
must close/cancel its own handles and reconcile before release. This memory cap
is not an output-directory or disk quota.
"""
import threading
import time

MAX_RETAINED_BYTES=128*1024*1024
MAX_SECONDS=180.0
MAX_CHUNK_BYTES=64*1024
MAX_CLEANUP_SECONDS=5.0


def require(ok,message):
    if not ok:raise ValueError(message)


def capture(stdout, stderr, *, byte_cap, timeout_seconds, terminate, chunk_bytes=65536, cleanup_seconds=2.0):
    """Capture at most byte_cap combined bytes; never certify process success.

    terminate(reason) is a teardown request, not an approval. It is called at
    most once in a daemon thread after limit, timeout or read failure. Retention
    order is scheduling-dependent; discarded data is disclosed. Read objects
    must obey read(n) <= n, return immutable bytes and be owned by the caller.
    The caller must hold the Job/lease, independently observe exit and enforce a
    separate output-tree storage quota. This method never closes caller handles.
    """
    require(stdout is not stderr and callable(getattr(stdout,'read',None)) and callable(getattr(stderr,'read',None)) and
            callable(terminate),'two distinct streams and termination request required')
    require(type(byte_cap) is int and 0<=byte_cap<=MAX_RETAINED_BYTES and type(chunk_bytes) is int and
            0<chunk_bytes<=MAX_CHUNK_BYTES,'capture byte bounds')
    require(type(timeout_seconds) in (int,float) and 0<timeout_seconds<=MAX_SECONDS and
            type(cleanup_seconds) in (int,float) and 0<=cleanup_seconds<=MAX_CLEANUP_SECONDS,'time bounds')
    lock=threading.Lock();complete=threading.Event();wake=threading.Event();stop=threading.Event()
    state={'chunks':{'stdout':bytearray(),'stderr':bytearray()},'retained':0,'discarded':0,'seen':0,
           'eof':{'stdout':False,'stderr':False},'errors':{},'reason':None,
           'termination_started':False,'termination_finished':False,'termination_error':None,'closed':False}
    workers=[];term_thread=[None]
    def dispatch(reason):
        with lock:
            if state['closed'] or state['termination_started']:return
            state['termination_started']=True;state['reason']=reason
        def run_termination():
            error=None
            try:terminate(reason)
            except BaseException as exc:error=type(exc).__name__
            with lock:
                if not state['closed']:
                    state['termination_finished']=True;state['termination_error']=error
        t=threading.Thread(target=run_termination,name='bounded-capture-terminate',daemon=True)
        term_thread[0]=t;t.start();wake.set()
    def read_stream(name,stream):
        try:
            while not stop.is_set():
                data=stream.read(chunk_bytes)
                if type(data) is not bytes or len(data)>chunk_bytes:raise ValueError('read contract')
                if not data:
                    with lock:
                        if not state['closed']:state['eof'][name]=True
                    break
                with lock:
                    if state['closed']:break
                    take=min(len(data),byte_cap-state['retained'])
                    if take:state['chunks'][name].extend(data[:take])
                    state['retained']+=take;state['seen']+=len(data);state['discarded']+=len(data)-take
                    exceeded=take<len(data)
                if exceeded:dispatch('byte_cap')
        except BaseException as exc:
            with lock:
                if not state['closed']:state['errors'][name]=type(exc).__name__
            dispatch('read_error')
        finally:
            with lock:
                if not state['closed']:
                    state.setdefault('done',set()).add(name)
                    if len(state['done'])==2:complete.set();wake.set()
    deadline=time.monotonic()+float(timeout_seconds)
    for name,stream in (('stdout',stdout),('stderr',stderr)):
        thread=threading.Thread(target=read_stream,args=(name,stream),name='bounded-capture-'+name,daemon=True)
        workers.append(thread);thread.start()
    remaining=max(0.0,deadline-time.monotonic())
    if not wake.wait(remaining):dispatch('deadline')
    # Wait only to a fixed cleanup deadline; no reader may extend this budget.
    cleanup_deadline=time.monotonic()+float(cleanup_seconds)
    for thread in workers:
        thread.join(max(0.0,cleanup_deadline-time.monotonic()))
    t=term_thread[0]
    if t is not None:t.join(max(0.0,cleanup_deadline-time.monotonic()))
    stop.set()
    with lock:
        state['closed']=True
        alive=[thread.name for thread in workers if thread.is_alive()]
        term_alive=bool(t and t.is_alive())
        complete_capture=all(state['eof'].values()) and not state['errors'] and state['reason'] is None and not alive
        return {'status':'captured' if complete_capture else 'incomplete',
                'stdout':bytes(state['chunks']['stdout']),'stderr':bytes(state['chunks']['stderr']),
                'retained_bytes':state['retained'],'observed_bytes':state['seen'],'discarded_bytes':state['discarded'],
                'eof':dict(state['eof']),'read_errors':dict(state['errors']),'stop_reason':state['reason'],
                'reader_threads_alive':alive,'termination_requested':state['termination_started'],
                'termination_returned':state['termination_finished'],'termination_error':state['termination_error'],
                'termination_thread_alive':term_alive,'process_success_established':False,
                'output_disk_quota_established':False}
