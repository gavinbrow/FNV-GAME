"""Source-only successor whole-Job terminal observation; real entry disabled.

Uses the existing factory Kernel's poll, creation, job_check, census,
close_process and close_job interfaces and QueryFullProcessImageNameW. The
fixture backend is injectable for synthetic tests and cannot authorize work.
Empty Job census is a time-local observation under a cooperative held-Job owner,
not a guarantee against later assignment or hostile actors. No LINK is launched.
"""
import ctypes
import ntpath
import re
import threading

FIXED_PROFILE=None
SOURCE_PINS=None
WATCHDOG_REVIEW=None
LEASE_REVIEW=None


def need(ok,message):
    if not ok:raise ValueError(message)


def _image_fixture(base,kernel,process):
    """Query the retained process handle; no path-only PID lookup."""
    size=base.DWORD(32768);buffer=ctypes.create_unicode_buffer(size.value)
    need(kernel.k.QueryFullProcessImageNameW(process.process,0,buffer,ctypes.byref(size)), 'process image query failed')
    need(0<size.value<32768 and buffer.value and len(buffer.value)==size.value, 'process image differs')
    return buffer.value


class TerminalObserverFixture:
    """Single-use state; fake backend/data must never be treated as authority."""
    def __init__(self,base,kernel,process,job,*,expected_child,job_name,session_nonce):
        need(type(job) is int and job>0 and process is not None and
             type(getattr(process,'process',None)) is int and process.process>0 and
             type(getattr(process,'pid',None)) is int and process.pid>0, 'retained process and Job handles required')
        need(type(expected_child) is dict and set(expected_child)=={'pid','creation','image'} and
             type(expected_child['pid']) is int and expected_child['pid']>0 and
             type(expected_child['creation']) is int and expected_child['creation']>0 and
             type(expected_child['image']) is str and expected_child['image'] and
             process.pid==expected_child['pid'] and type(job_name) is str and job_name and
             type(session_nonce) is str and re.fullmatch('[0-9a-f]{64}',session_nonce), 'fixed identity required')
        self.base=base;self.kernel=kernel;self.process=process;self.job=job
        self.expected=dict(expected_child);self.job_name=job_name;self.nonce=session_nonce
        self._lock=threading.Lock();self._observe_attempted=False;self._observed=None;self._cleanup_attempted=False
    def _child(self):
        creation=self.kernel.creation(self.process);image=_image_fixture(self.base,self.kernel,self.process)
        need(type(creation) is int and creation>0 and creation==self.expected['creation'] and
             self.process.pid==self.expected['pid'] and
             ntpath.normcase(ntpath.normpath(image))==ntpath.normcase(ntpath.normpath(self.expected['image'])),
             'process birth/image drift')
        return {'pid':self.process.pid,'creation':creation,'image':image}
    def observe(self):
        with self._lock:
            need(not self._observe_attempted,'terminal observation already attempted; reconcile')
            self._observe_attempted=True
        # Any exception leaves the one-shot state unresolved, not retryable.
        self.kernel.job_check(self.job)
        first_child=self._child();code=self.kernel.poll(self.process)
        need(type(code) is int,'held process still active or exit unavailable')
        first=self.kernel.census(self.job)
        need(type(first) is list and first==[],'Job has active or unobserved descendants')
        self.kernel.job_check(self.job)
        second_child=self._child();second_code=self.kernel.poll(self.process);second=self.kernel.census(self.job)
        need(first_child==second_child and type(second_code) is int and second_code==code and
             type(second) is list and second==[], 'terminal Job/process sample drift')
        result={'status':'OBSERVED_UNREVIEWED','job_name':self.job_name,'session_nonce':self.nonce,
                'child':second_child,'returncode':code,'empty_job_samples':2,
                'process_handle_retained':True,'job_handle_retained':True,
                'cleanup_status':'NOT_ATTEMPTED','future_job_state_guaranteed':False,
                'process_success_established':False,'native_link_authorized':False}
        with self._lock:self._observed=result
        return dict(result)
    def cleanup(self):
        """Attempt each owned handle group once and disclose uncertain failures."""
        with self._lock:
            need(self._observed is not None and not self._cleanup_attempted,'cleanup unavailable or already attempted')
            self._cleanup_attempted=True
        errors={};attempted=[]
        for role,action in (('process',lambda:self.kernel.close_process(self.process)),
                            ('job',lambda:self.kernel.close_job(self.job))):
            attempted.append(role)
            try:action()
            except BaseException as exc:errors[role]=type(exc).__name__
        return {'status':'UNKNOWN' if errors else 'CLOSE_CALLS_RETURNED',
                'attempted':attempted,'errors':errors,'observed_child':dict(self.expected),
                'job_name':self.job_name,'session_nonce':self.nonce,
                'all_job_handles_globally_closed_established':False,'native_link_authorized':False}


def run():
    raise RuntimeError('whole-Job observation disabled pending fixed source, held Job, lease and peer authority')


if __name__=='__main__':run()
