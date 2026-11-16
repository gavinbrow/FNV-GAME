import importlib.util
import io
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
m=load('held_fixture','tools/rebuild/application_successor_held_link_v1.py')
coop=load('coop_fixture','tools/rebuild/application_successor_cooperative_link_v3.py')
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
    def wait_with_deadline(self,seconds):return 1120

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.reserve=self.root/'reserve';self.reserve.mkdir();self.out=self.root/'out';self.out.mkdir()
        self.profile={'forecast_bytes':1,'existing_bytes':0,'reservation_root':str(self.reserve),'operation_id':'fixture',
         'profile_sha256':'c'*64,'response_sha256':'a'*64,'response_path':'response.rsp','input_bindings':[{'fixture':1}],
         'output_directory':str(self.out),'compiler_lib':'compiler','sdk_lib':'sdk','default_libraries':{'crt':'fixture'},
         'allowed_outputs':[],'capture_bytes':100,'timeout_seconds':1,'cleanup_seconds':.2,'provenance':{}}
        self.guard=Guard();self.diag=Diagnostic();self.process=Process();self.job=types.SimpleNamespace(owned_size=lambda *a:0)
    def invoke(self):
        with patch.object(m,'_verify_peers',return_value=None),patch.object(m,'_require_successor_held_guard',return_value=None), \
             patch.object(m,'_start_held_link',return_value=self.process):
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
        self.assertTrue((self.out/'terminal.json').is_file());self.assertEqual((self.out/'link.stdout.txt').read_bytes(),b'LINK fixture')
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
