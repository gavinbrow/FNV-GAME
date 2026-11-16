import importlib.util
import io
import os
from pathlib import Path
import threading
import time
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('capture_fixture',ROOT/'tools/rebuild/successor_bounded_capture_v2.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Tests(unittest.TestCase):
    def test_both_streams_shared_cap_and_no_process_success(self):
        calls=[];result=m.capture(io.BytesIO(b'abc'),io.BytesIO(b'def'),byte_cap=6,timeout_seconds=1,terminate=calls.append,chunk_bytes=2)
        self.assertEqual(result['status'],'captured');self.assertEqual(result['stdout'],b'abc');self.assertEqual(result['stderr'],b'def')
        self.assertEqual(result['retained_bytes'],6);self.assertEqual(result['discarded_bytes'],0);self.assertEqual(calls,[])
        self.assertFalse(result['process_success_established']);self.assertFalse(result['output_disk_quota_established'])
    def test_over_cap_drains_both_and_terminates_once(self):
        calls=[];result=m.capture(io.BytesIO(b'a'*100),io.BytesIO(b'b'*100),byte_cap=7,timeout_seconds=1,terminate=calls.append,chunk_bytes=3)
        self.assertEqual(result['status'],'incomplete');self.assertEqual(result['stop_reason'],'byte_cap')
        self.assertEqual(result['retained_bytes'],7);self.assertEqual(result['observed_bytes'],200);self.assertEqual(result['discarded_bytes'],193)
        self.assertEqual(sum(map(len,(result['stdout'],result['stderr']))),7);self.assertEqual(calls,['byte_cap'])
        self.assertEqual(result['eof'],{'stdout':True,'stderr':True})
    def test_read_error_keeps_partial_and_reports(self):
        class Bad:
            def __init__(self):self.calls=0
            def read(self,n):
                self.calls+=1
                if self.calls==1:return b'abc'
                raise OSError('fixture')
        calls=[];result=m.capture(Bad(),io.BytesIO(b'def'),byte_cap=10,timeout_seconds=1,terminate=calls.append,chunk_bytes=4)
        self.assertEqual(result['stdout'],b'abc');self.assertEqual(result['read_errors'],{'stdout':'OSError'})
        self.assertEqual(result['stop_reason'],'read_error');self.assertEqual(calls,['read_error'])
    def test_timeout_does_not_claim_blocked_reader_or_termination_complete(self):
        release=threading.Event();started=threading.Event()
        class Block:
            def read(self,n):started.set();release.wait();return b''
        def terminate(reason):release.wait()
        result=m.capture(Block(),io.BytesIO(b''),byte_cap=1,timeout_seconds=.02,cleanup_seconds=.02,terminate=terminate)
        self.assertTrue(started.is_set());self.assertEqual(result['stop_reason'],'deadline')
        self.assertTrue(result['reader_threads_alive']);self.assertTrue(result['termination_thread_alive'])
        self.assertFalse(result['process_success_established']);release.set()
    def test_termination_failure_is_reported(self):
        def terminate(reason):raise OSError('fixture')
        result=m.capture(io.BytesIO(b'xx'),io.BytesIO(b''),byte_cap=1,timeout_seconds=1,terminate=terminate)
        self.assertEqual(result['termination_error'],'OSError');self.assertTrue(result['termination_returned'])
    def test_real_synthetic_pipes_are_drained_concurrently(self):
        pairs=[os.pipe(),os.pipe()];readers=[os.fdopen(pair[0],'rb',buffering=0) for pair in pairs]
        def write(fd,data):
            with os.fdopen(fd,'wb',buffering=0) as stream:stream.write(data)
        threads=[threading.Thread(target=write,args=(pair[1],data)) for pair,data in zip(pairs,(b'a'*200000,b'b'*200000))]
        for t in threads:t.start()
        try:
            result=m.capture(*readers,byte_cap=4096,timeout_seconds=3,terminate=lambda reason:None,chunk_bytes=4096)
            self.assertEqual(result['observed_bytes'],400000);self.assertEqual(result['retained_bytes'],4096)
            self.assertEqual(result['discarded_bytes'],395904);self.assertEqual(result['eof'],{'stdout':True,'stderr':True})
        finally:
            for t in threads:t.join(2)
            for stream in readers:stream.close()
        self.assertTrue(all(not t.is_alive() for t in threads))
    def test_first_reader_start_failure_requests_once_and_returns_incomplete(self):
        original=threading.Thread.start;calls=[]
        def start(thread):
            if thread.name=='bounded-capture-stdout':raise RuntimeError('fixture')
            return original(thread)
        with patch.object(threading.Thread,'start',start):
            result=m.capture(io.BytesIO(b'a'),io.BytesIO(b'b'),byte_cap=2,timeout_seconds=1,
                             terminate=calls.append,cleanup_seconds=.1)
        self.assertEqual(result['status'],'incomplete')
        self.assertEqual(result['reader_start_errors'],{'stdout':'RuntimeError'})
        self.assertEqual(result['stop_reason'],'reader_start_error');self.assertEqual(calls,['reader_start_error'])
        self.assertFalse(result['process_success_established'])

    def test_second_reader_start_failure_retains_partial_and_bounds_cleanup(self):
        original=threading.Thread.start;release=threading.Event();calls=[]
        class Partial:
            def __init__(self):self.first=True
            def read(self,n):
                if self.first:self.first=False;return b'abc'
                release.wait();return b''
        def start(thread):
            if thread.name=='bounded-capture-stderr':raise RuntimeError('fixture')
            return original(thread)
        with patch.object(threading.Thread,'start',start):
            result=m.capture(Partial(),io.BytesIO(b'b'),byte_cap=8,timeout_seconds=1,
                             terminate=calls.append,cleanup_seconds=.02)
        self.assertEqual(result['stdout'],b'abc');self.assertEqual(result['reader_start_errors'],{'stderr':'RuntimeError'})
        self.assertEqual(calls,['reader_start_error']);self.assertTrue(result['reader_threads_alive']);release.set()

    def test_termination_thread_start_failure_is_explicit(self):
        original=threading.Thread.start;calls=[]
        def start(thread):
            if thread.name=='bounded-capture-terminate':raise RuntimeError('fixture')
            return original(thread)
        with patch.object(threading.Thread,'start',start):
            result=m.capture(io.BytesIO(b'xx'),io.BytesIO(b''),byte_cap=1,timeout_seconds=1,
                             terminate=calls.append,cleanup_seconds=.1)
        self.assertEqual(result['status'],'incomplete');self.assertTrue(result['termination_requested'])
        self.assertFalse(result['termination_thread_started']);self.assertFalse(result['termination_returned'])
        self.assertEqual(result['termination_error'],'ThreadStart:RuntimeError');self.assertEqual(calls,[])

    def test_delayed_termination_thread_start_is_bounded_and_never_joined_unstarted(self):
        original=threading.Thread.start;entered=threading.Event();release=threading.Event();calls=[]
        def start(thread):
            if thread.name=='bounded-capture-terminate':entered.set();release.wait()
            return original(thread)
        try:
            with patch.object(threading.Thread,'start',start):
                result=m.capture(io.BytesIO(b'xx'),io.BytesIO(b''),byte_cap=1,timeout_seconds=.02,
                                 terminate=calls.append,cleanup_seconds=.02)
            self.assertTrue(entered.is_set());self.assertEqual(result['status'],'incomplete')
            self.assertTrue(result['termination_start_pending']);self.assertFalse(result['termination_returned'])
            self.assertEqual(calls,[])
        finally:release.set()

    def test_delayed_termination_start_after_first_reader_failure_is_bounded(self):
        original=threading.Thread.start;entered=threading.Event();release=threading.Event();calls=[]
        def start(thread):
            if thread.name=='bounded-capture-stdout':raise RuntimeError('fixture')
            if thread.name=='bounded-capture-terminate':entered.set();release.wait()
            return original(thread)
        try:
            with patch.object(threading.Thread,'start',start):
                result=m.capture(io.BytesIO(),io.BytesIO(),byte_cap=1,timeout_seconds=.1,
                                 terminate=calls.append,cleanup_seconds=.02)
            self.assertTrue(entered.is_set());self.assertEqual(result['reader_start_errors'],{'stdout':'RuntimeError'})
            self.assertTrue(result['termination_start_pending']);self.assertFalse(result['termination_returned'])
            self.assertEqual(calls,[])
        finally:release.set()

    def test_termination_starter_failure_is_explicit(self):
        calls=[]
        with patch.object(m._thread,'start_new_thread',side_effect=RuntimeError('fixture')):
            result=m.capture(io.BytesIO(b'xx'),io.BytesIO(b''),byte_cap=1,timeout_seconds=1,
                             terminate=calls.append,cleanup_seconds=.1)
        self.assertTrue(result['termination_requested']);self.assertFalse(result['termination_thread_started'])
        self.assertEqual(result['termination_error'],'StarterStart:RuntimeError');self.assertEqual(calls,[])

    def test_validation_rejects_unbounded_or_shared_streams(self):
        stream=io.BytesIO()
        with self.assertRaises(ValueError):m.capture(stream,stream,byte_cap=1,timeout_seconds=1,terminate=lambda x:None)
        with self.assertRaises(ValueError):m.capture(io.BytesIO(),io.BytesIO(),byte_cap=m.MAX_RETAINED_BYTES+1,timeout_seconds=1,terminate=lambda x:None)
        with self.assertRaises(ValueError):m.capture(io.BytesIO(),io.BytesIO(),byte_cap=1,timeout_seconds=float('nan'),terminate=lambda x:None)

if __name__=='__main__':unittest.main()
