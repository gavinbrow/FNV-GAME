from concurrent.futures import ThreadPoolExecutor
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import threading
import time
import types
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
m=load('cooperative_fixture','tools/rebuild/application_successor_cooperative_link_v3.py')
c=load('capture_fixture','tools/rebuild/successor_bounded_capture_v3.py')

class Tests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
    def test_entry_disabled_and_forecast_fixed_caps(self):
        with self.assertRaises(RuntimeError):m.run()
        self.assertEqual(m._forecast_fixture(forecast_bytes=1,existing_bytes=0)['enforcement'],'MONITORED')
        with self.assertRaises(ValueError):m._forecast_fixture(forecast_bytes=m.MAX_OUTPUT_BYTES,existing_bytes=0)
        with self.assertRaises(ValueError):m._forecast_fixture(forecast_bytes=0,existing_bytes=0,output_cap=m.MAX_OUTPUT_BYTES+1)
    def test_reservation_is_operation_id_only_and_conflicts(self):
        def reserve(i):
            try:return m._reserve_fixture(self.root,'same',str(i%10)*64,'a'*64)
            except FileExistsError:return None
        with ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(reserve,range(8)))
        self.assertEqual(sum(x is not None for x in results),1)
        record=json.loads((self.root/'same.json').read_bytes());self.assertEqual(record['operation_id'],'same')
        self.assertEqual(record['state'],'UNKNOWN')
        with self.assertRaises(FileExistsError):m._reserve_fixture(self.root,'same','f'*64,'b'*64)
        with self.assertRaises(ValueError):m._reserve_fixture(self.root,'Same','f'*64,'b'*64)
    def test_normal_capture_has_sample_and_no_success_claim(self):
        job=types.SimpleNamespace(owned_size=lambda output,allowed:17)
        result=m._monitor_capture_fixture(io.BytesIO(b'a'),io.BytesIO(b'b'),output='fixture',allowed_outputs=[],
            capture_module=c,job_module=job,terminate=lambda reason:None,byte_cap=10,timeout_seconds=1)
        self.assertEqual(result['status'],'capture_and_samples_complete');self.assertTrue(result['samples'])
        self.assertEqual(result['monitor_state'],'MONITORED');self.assertFalse(result['hard_disk_quota'])
        self.assertFalse(result['process_success_established']);self.assertFalse(result['between_samples_growth_bounded'])
    def test_watermark_stops_and_keeps_captured_partial(self):
        job=types.SimpleNamespace(owned_size=lambda output,allowed:m.MAX_OUTPUT_BYTES)
        calls=[];result=m._monitor_capture_fixture(io.BytesIO(b'partial'),io.BytesIO(b''),output='fixture',allowed_outputs=[],
            capture_module=c,job_module=job,terminate=calls.append,byte_cap=100,timeout_seconds=1)
        self.assertEqual(result['status'],'incomplete');self.assertEqual(calls,['output_watermark'])
        self.assertEqual(result['capture']['stdout'],b'partial');self.assertFalse(result['hard_disk_quota'])
    def test_capture_reserve_counts_against_sampled_output_watermark(self):
        job=types.SimpleNamespace(owned_size=lambda output,allowed:m.MAX_OUTPUT_BYTES-m.CONTROL_RESERVE_BYTES-4)
        calls=[];result=m._monitor_capture_fixture(io.BytesIO(b'a'),io.BytesIO(),output='fixture',allowed_outputs=[],
            capture_module=c,job_module=job,terminate=calls.append,byte_cap=5,timeout_seconds=1)
        self.assertEqual(result['termination_reason'],'output_watermark')
        self.assertEqual(result['capture_reserve_bytes'],5);self.assertEqual(calls,['output_watermark'])

    def test_monitor_start_after_launch_exception_reports_live_attempt(self):
        entered=threading.Event();release=threading.Event();calls=[];original=threading.Thread.start
        def blocked(output,allowed):entered.set();release.wait();return 0
        def start(thread):
            if thread.name=='successor-output-monitor':
                original(thread);entered.wait(1);raise RuntimeError('after launch')
            return original(thread)
        try:
            with patch.object(threading.Thread,'start',start):
                result=m._monitor_capture_fixture(io.BytesIO(),io.BytesIO(),output='fixture',allowed_outputs=[],
                    capture_module=c,job_module=types.SimpleNamespace(owned_size=blocked),
                    terminate=calls.append,byte_cap=1,timeout_seconds=1,cleanup_seconds=.02)
            self.assertEqual(result['status'],'incomplete');self.assertTrue(result['monitor_start_uncertain'])
            self.assertTrue(result['monitor_thread_alive']);self.assertEqual(calls,['monitor_start_failure'])
        finally:release.set()

    def test_blocked_termination_is_reported_without_waiting_forever(self):
        release=threading.Event();entered=threading.Event()
        def terminate(reason):entered.set();release.wait()
        try:
            job=types.SimpleNamespace(owned_size=lambda output,allowed:m.MAX_OUTPUT_BYTES)
            result=m._monitor_capture_fixture(io.BytesIO(),io.BytesIO(),output='fixture',allowed_outputs=[],
                capture_module=c,job_module=job,terminate=terminate,byte_cap=1,timeout_seconds=.1,cleanup_seconds=.02)
            self.assertTrue(entered.is_set());self.assertTrue(result['termination_requested'])
            self.assertFalse(result['termination_returned']);self.assertFalse(result['process_success_established'])
        finally:release.set()

    def test_termination_dispatch_failure_is_not_callback_return(self):
        job=types.SimpleNamespace(owned_size=lambda output,allowed:m.MAX_OUTPUT_BYTES)
        captured={'status':'captured','stdout':b'fixture','stderr':b''}
        fake_capture=types.SimpleNamespace(capture=lambda *args,**kwargs:captured)
        with patch.object(m._thread,'start_new_thread',side_effect=RuntimeError('fixture')):
            result=m._monitor_capture_fixture(io.BytesIO(),io.BytesIO(),output='fixture',allowed_outputs=[],
                capture_module=fake_capture,job_module=job,terminate=lambda reason:None,byte_cap=1,timeout_seconds=1)
        self.assertTrue(result['termination_requested']);self.assertTrue(result['termination_dispatch_resolved'])
        self.assertFalse(result['termination_callback_started']);self.assertFalse(result['termination_returned'])
        self.assertEqual(result['termination_error'],'ThreadStart:RuntimeError');self.assertEqual(result['outcome'],'UNKNOWN')
        self.assertEqual(result['capture']['stdout'],b'fixture')

    def test_capture_exception_requests_termination_and_reports_unknown(self):
        job=types.SimpleNamespace(owned_size=lambda output,allowed:0);calls=[]
        def fail(*args,**kwargs):raise OSError('fixture exception')
        result=m._monitor_capture_fixture(io.BytesIO(),io.BytesIO(),output='fixture',allowed_outputs=[],
            capture_module=types.SimpleNamespace(capture=fail),job_module=job,terminate=calls.append,
            byte_cap=1,timeout_seconds=1)
        self.assertEqual(result['status'],'incomplete');self.assertEqual(result['outcome'],'UNKNOWN')
        self.assertEqual(result['capture_error'],'OSError');self.assertFalse(result['partial_capture_available'])
        self.assertIsNone(result['capture']);self.assertEqual(calls,['capture_exception'])
        self.assertTrue(result['termination_callback_started']);self.assertTrue(result['termination_callback_finished'])
        self.assertTrue(result['termination_returned'])

    def test_malformed_capture_return_requests_termination(self):
        job=types.SimpleNamespace(owned_size=lambda output,allowed:0);calls=[]
        result=m._monitor_capture_fixture(io.BytesIO(),io.BytesIO(),output='fixture',allowed_outputs=[],
            capture_module=types.SimpleNamespace(capture=lambda *a,**k:None),job_module=job,
            terminate=calls.append,byte_cap=1,timeout_seconds=1)
        self.assertEqual(result['outcome'],'UNKNOWN');self.assertEqual(result['capture_error'],'ValueError')
        self.assertFalse(result['partial_capture_available']);self.assertEqual(calls,['capture_exception'])

    def test_invalid_limits_reject_before_start_capture_or_termination(self):
        job=types.SimpleNamespace(owned_size=lambda *a: self.fail('monitor ran'))
        def capture_fail(*a,**k):self.fail('capture ran')
        fake=types.SimpleNamespace(capture=capture_fail);calls=[]
        cases=[('timeout_seconds',x) for x in ('bad',True,0,-1,181,float('nan'),float('inf'))]
        cases += [('cleanup_seconds',x) for x in ('bad',True,-1,5.1,float('nan'),float('inf'))]
        cases += [('sample_seconds',x) for x in ('bad',True,0,2,float('nan'),float('inf'))]
        cases += [('byte_cap',x) for x in (True,-1,m.MAX_OUTPUT_BYTES,1.0)]
        for key,value in cases:
            args={'output':'fixture','allowed_outputs':[],'capture_module':fake,'job_module':job,
                  'terminate':calls.append,'byte_cap':1,'timeout_seconds':1,'cleanup_seconds':1,'sample_seconds':.05}
            args[key]=value
            with self.subTest(key=key,value=value),patch.object(threading.Thread,'start',side_effect=AssertionError('worker started')):
                with self.assertRaises(ValueError):m._monitor_capture_fixture(io.BytesIO(),io.BytesIO(),**args)
        self.assertEqual(calls,[])

    def test_valid_limits_capture_exception_remains_unknown(self):
        calls=[]
        def fail(*args,**kwargs):raise RuntimeError('capture error')
        result=m._monitor_capture_fixture(io.BytesIO(),io.BytesIO(),output='fixture',allowed_outputs=[],
            capture_module=types.SimpleNamespace(capture=fail),job_module=types.SimpleNamespace(owned_size=lambda *a:0),
            terminate=calls.append,byte_cap=1,timeout_seconds=1,cleanup_seconds=.05)
        self.assertEqual(result['outcome'],'UNKNOWN');self.assertEqual(result['capture_error'],'RuntimeError')
        self.assertEqual(calls,['capture_exception'])

    def test_monitor_error_and_capture_limit_request_at_most_once(self):
        def bad(output,allowed):raise OSError('fixture')
        calls=[];result=m._monitor_capture_fixture(io.BytesIO(b'xx'),io.BytesIO(b''),output='fixture',allowed_outputs=[],
            capture_module=c,job_module=types.SimpleNamespace(owned_size=bad),terminate=calls.append,byte_cap=1,timeout_seconds=1)
        self.assertEqual(result['status'],'incomplete');self.assertEqual(len(calls),1)
        self.assertEqual(result['monitor_error'],'OSError')

if __name__=='__main__':unittest.main()
