import importlib.util
import io
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
m=load('held_fixture','tools/rebuild/application_successor_held_link_v4.py')
coop=load('coop_fixture','tools/rebuild/application_successor_cooperative_link_v4.py')
capture=load('capture_fixture','tools/rebuild/successor_bounded_capture_v3.py')

class Guard:
    def __init__(self):self.checks=[]
    def check(self,phase):self.checks.append(phase)
class Diagnostic:
    def __init__(self):self.calls=0;self.change=False
    def stable(self,bindings):self.calls+=1
    def identity(self,path):
        return {'requested_path':path,'path':path,'sha256':'a'*64 if not (self.change and self.calls>1) else 'b'*64,
                'size':1,'device':1,'inode':1}
    def select_libraries(self,*args):return {'crt':'fixture'}
    def diagnostic_errors(self,text,provenance):return [{'code':'LNK1120','text':text}]
    def classify(self,returncode,errors):return 'expected-unresolved-link-diagnostic' if returncode==1120 else 'other'
class Process:
    def __init__(self):self.stdout=io.BytesIO(b'LINK fixture');self.stderr=io.BytesIO(b'LNK1120');self.terminations=[]
    def terminate_job(self,reason):self.terminations.append(reason)
    def wait_for_job_exit(self,seconds):return {'returncode':1120,'job_empty':True,'cleanup_complete':True}

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.reserve=self.root/'reserve';self.reserve.mkdir();self.out=self.root/'out';self.out.mkdir()
        self.profile={'forecast_bytes':1,'existing_bytes':0,'reservation_root':str(self.reserve),'operation_id':'fixture',
         'profile_sha256':'c'*64,'response_sha256':'a'*64,'response_path':'response.rsp','input_bindings':[{'fixture':1}],
         'output_directory':str(self.out),'compiler_lib':'compiler','sdk_lib':'sdk','default_libraries':{'crt':'fixture'},
         'allowed_outputs':['link.stdout.txt','link.stderr.txt','terminal.json','completion.json','final.json'],
         'control_directory':str(self.reserve),'control_expected':{},'capture_bytes':100,'timeout_seconds':1,'cleanup_seconds':.2,'provenance':{}}
        self.guard=Guard();self.diag=Diagnostic();self.process=Process()
        def owned(output,allowed):return sum(p.stat().st_size for p in Path(output).iterdir() if p.is_file())
        def control(directory,expected):
            actual={p.name for p in Path(directory).iterdir()};self.assertEqual(actual,set(expected))
            return sum(p.stat().st_size for p in Path(directory).iterdir())
        self.job=types.SimpleNamespace(owned_size=owned,control_guard=control)
    def invoke(self):
        with patch.object(m,'_verify_peers',return_value=None),patch.object(m,'_require_successor_held_guard',return_value=None), \
             patch.object(m,'_start_held_link',return_value=self.process),patch.object(m,'_verify_job_terminal',return_value=None):
            return m._run_fixture(self.profile,diagnostic=self.diag,guard=self.guard,cooperative=coop,
                                  capture_module=capture,job_module=self.job)
    def test_real_entry_and_unaccepted_peers_fail_before_reservation(self):
        with self.assertRaises(RuntimeError):m.run()
        with self.assertRaises(RuntimeError):m._run_fixture(self.profile,diagnostic=self.diag,guard=self.guard,cooperative=coop,
                                                          capture_module=capture,job_module=self.job)
        self.assertEqual(list(self.reserve.iterdir()),[])
    def test_fixture_success_binds_prepost_logs_and_exit_not_game_success(self):
        result=self.invoke();self.assertEqual(result['status'],'observed-unreviewed');self.assertEqual(result['returncode'],1120)
        self.assertEqual(result['classification'],'expected-unresolved-link-diagnostic');self.assertEqual(self.diag.calls,2)
        self.assertEqual(result['response_pre'],result['response_post']);self.assertFalse(result['hard_disk_quota'])
        self.assertFalse(result['executable_execution']);self.assertFalse(result['runtime_eligible'])
        self.assertTrue((self.out/'final.json').is_file());self.assertTrue((self.out/'completion.json').is_file());self.assertTrue((self.out/'terminal.json').is_file());self.assertEqual((self.out/'link.stdout.txt').read_bytes(),b'LINK fixture')
        with self.assertRaises(FileExistsError):self.invoke()
    def test_response_drift_leaves_unknown_no_terminal(self):
        self.diag.change=True;result=self.invoke()
        self.assertEqual(result['status'],'UNKNOWN');self.assertFalse((self.out/'terminal.json').exists())
        self.assertTrue((self.reserve/'fixture.json').exists());self.assertEqual(self.process.terminations,[])
    def test_incomplete_capture_requests_job_termination_once(self):
        self.profile['capture_bytes']=1;result=self.invoke()
        self.assertEqual(result['status'],'UNKNOWN');self.assertEqual(len(self.process.terminations),1)
        self.assertFalse((self.out/'terminal.json').exists());self.assertTrue((self.reserve/'fixture.json').exists())
    def test_existing_log_blocks_terminal_and_retains_prior_file(self):
        (self.out/'link.stdout.txt').write_bytes(b'prior')
        result=self.invoke();self.assertEqual(result['status'],'UNKNOWN');self.assertFalse((self.out/'terminal.json').exists())
        self.assertEqual((self.out/'link.stdout.txt').read_bytes(),b'prior')
    def test_eof_then_growth_before_job_exit_blocks_publication(self):
        growing=threading.Event()
        def wait_job(seconds):growing.set();time.sleep(.12);return {'returncode':1120,'job_empty':True,'cleanup_complete':True}
        self.process.wait_for_job_exit=wait_job
        self.job=types.SimpleNamespace(owned_size=lambda *a:coop.MAX_OUTPUT_BYTES if growing.is_set() else 0,control_guard=lambda *a:0)
        result=self.invoke()
        self.assertEqual(result['status'],'UNKNOWN');self.assertFalse((self.out/'terminal.json').exists())
        self.assertFalse((self.out/'completion.json').exists());self.assertEqual(len(self.process.terminations),1)

    def test_oversized_serialized_terminal_rejected_before_logs(self):
        self.diag.diagnostic_errors=lambda *args:[{'code':'LNK1120','large':'x'*(9*1024*1024)}]
        result=self.invoke()
        self.assertEqual(result['status'],'UNKNOWN');self.assertFalse((self.out/'terminal.json').exists())
        self.assertFalse((self.out/'link.stdout.txt').exists());self.assertFalse((self.out/'completion.json').exists())

    def test_final_actual_sample_growth_blocks_completion(self):
        after=threading.Event();original=self.guard.check
        def check(phase):
            original(phase)
            if phase=='publish-after-terminal':after.set()
        self.guard.check=check
        owned=self.job.owned_size
        self.job.owned_size=lambda *args: m.MAX_OUTPUT_BYTES if after.is_set() else owned(*args)
        result=self.invoke()
        self.assertEqual(result['status'],'UNKNOWN');self.assertTrue((self.out/'terminal.json').exists())
        self.assertFalse((self.out/'completion.json').exists())

    def test_final_control_guard_failure_blocks_completion(self):
        calls=[];base=self.job.control_guard
        def control(*args):
            calls.append(1)
            if len(calls)>1:raise ValueError('control changed')
            return base(*args)
        self.job.control_guard=control;result=self.invoke()
        self.assertEqual(result['status'],'UNKNOWN');self.assertTrue((self.out/'terminal.json').exists())
        self.assertFalse((self.out/'completion.json').exists())

    def test_growth_after_completion_candidate_blocks_final_authority(self):
        after=threading.Event();original=self.guard.check
        def check(phase):
            original(phase)
            if phase=='publish-after-completion':after.set()
        self.guard.check=check;owned=self.job.owned_size
        self.job.owned_size=lambda *args:m.MAX_OUTPUT_BYTES if after.is_set() else owned(*args)
        result=self.invoke()
        self.assertEqual(result['status'],'UNKNOWN');self.assertTrue((self.out/'completion.json').exists())
        self.assertFalse((self.out/'final.json').exists())

    def test_post_completion_guard_failure_blocks_final_authority(self):
        original=self.guard.check
        def check(phase):
            original(phase)
            if phase=='publish-after-completion':raise RuntimeError('fixture')
        self.guard.check=check;result=self.invoke()
        self.assertEqual(result['status'],'UNKNOWN');self.assertTrue((self.out/'completion.json').exists())
        self.assertFalse((self.out/'final.json').exists())

    def test_post_completion_sample_guard_failure_blocks_final_authority(self):
        original=self.guard.check
        def check(phase):
            original(phase)
            if phase=='publish-after-post-completion-sample':raise RuntimeError('fixture')
        self.guard.check=check;result=self.invoke()
        self.assertEqual(result['status'],'UNKNOWN');self.assertTrue((self.out/'completion.json').exists())
        self.assertFalse((self.out/'final.json').exists())

    def test_unverified_job_exit_never_publishes(self):
        with patch.object(m,'_verify_peers',return_value=None),patch.object(m,'_require_successor_held_guard',return_value=None), \
             patch.object(m,'_start_held_link',return_value=self.process):
            result=m._run_fixture(self.profile,diagnostic=self.diag,guard=self.guard,cooperative=coop,
                                  capture_module=capture,job_module=self.job)
        self.assertEqual(result['status'],'UNKNOWN');self.assertFalse((self.out/'terminal.json').exists())
        self.assertFalse((self.out/'completion.json').exists())

    def test_termination_exception_preserved_without_retry(self):
        self.profile['capture_bytes']=1;calls=[]
        def fail(reason):calls.append(reason);raise OSError('fixture')
        self.process.terminate_job=fail
        result=self.invoke();self.assertEqual(result['status'],'UNKNOWN')
        self.assertEqual(len(calls),1);self.assertEqual(result['termination']['error'],'OSError')
        self.assertFalse(result['termination']['returned'])

    def test_blocked_termination_remains_unconfirmed(self):
        self.profile['capture_bytes']=1;self.profile['cleanup_seconds']=.02
        release=__import__('threading').Event();entered=__import__('threading').Event()
        def blocked(reason):entered.set();release.wait()
        self.process.terminate_job=blocked
        try:
            result=self.invoke();self.assertEqual(result['status'],'UNKNOWN');self.assertTrue(entered.is_set())
            self.assertTrue(result['termination']['requested']);self.assertFalse(result['termination']['returned'])
        finally:release.set()

    def test_postpublication_guard_failure_has_no_completion(self):
        original=self.guard.check
        def guard(phase):
            original(phase)
            if phase=='publish-after-terminal':raise RuntimeError('fixture')
        self.guard.check=guard;result=self.invoke()
        self.assertEqual(result['status'],'UNKNOWN');self.assertTrue((self.out/'terminal.json').exists())
        self.assertFalse((self.out/'completion.json').exists())

    def test_failed_preflight_keeps_once_reservation_unknown(self):
        self.profile['response_sha256']='b'*64
        with patch.object(m,'_verify_peers',return_value=None),patch.object(m,'_require_successor_held_guard',return_value=None), \
             patch.object(m,'_start_held_link') as launch:
            result=m._run_fixture(self.profile,diagnostic=self.diag,guard=self.guard,cooperative=coop,
                                  capture_module=capture,job_module=self.job)
        self.assertEqual(result['status'],'UNKNOWN');self.assertTrue((self.reserve/'fixture.json').exists())
        self.assertFalse((self.out/'terminal.json').exists());launch.assert_not_called()

    def test_unavailable_held_adapter_is_unknown_after_reservation(self):
        with patch.object(m,'_verify_peers',return_value=None),patch.object(m,'_require_successor_held_guard',return_value=None):
            result=m._run_fixture(self.profile,diagnostic=self.diag,guard=self.guard,cooperative=coop,
                                  capture_module=capture,job_module=self.job)
        self.assertEqual(result['status'],'UNKNOWN');self.assertTrue((self.reserve/'fixture.json').exists())
        self.assertFalse((self.out/'terminal.json').exists())

if __name__=='__main__':unittest.main()
