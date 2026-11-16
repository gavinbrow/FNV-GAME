import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import crt_v15_job_launcher as m

class Child:
    pid=123
class Backend:
    def __init__(self,code=0): self.code=code;self.terminated=False
    def create_job(self,*args): return 1
    def start_logged(self,*args): return Child()
    def creation(self,*args): return 456
    def assign(self,*args): pass
    def resume(self,*args): pass
    def poll(self,*args): return self.code
    def census(self,*args): return []
    def terminate_job(self,*args): self.terminated=True
    def wait(self,*args): return self.code
    def close_process(self,*args): pass
    def close_job(self,*args): pass

class PhaseTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.old=m.OUT;m.OUT=Path(self.tmp.name)
        self.orig=(m.base.lease,m.base.lease_remaining,m.base.verify_inputs)
        m.base.lease=lambda b: 'grant';m.base.lease_remaining=lambda g: 200;m.base.verify_inputs=lambda b: None
    def tearDown(self):
        m.OUT=self.old;m.base.lease,m.base.lease_remaining,m.base.verify_inputs=self.orig;self.tmp.cleanup()
    def test_success_records_job_exit(self):
        b=Backend();r=m.phase(0,{'inputs':{},'nested_parent_allowed':False,'environment':{}},{'review_sha256':'a'},'grant',b)
        self.assertEqual(r['state'],'completed-unreviewed');self.assertTrue(r['job_empty_observed']);self.assertFalse(b.terminated)
        self.assertTrue((m.OUT/'compile-intent.json').exists());self.assertTrue((m.OUT/'compile-terminal.json').exists())
    def test_failure_terminates_and_stays_terminal(self):
        b=Backend(1);r=m.phase(0,{'inputs':{},'nested_parent_allowed':False,'environment':{}},{'review_sha256':'a'},'grant',b)
        self.assertEqual(r['state'],'failed-or-unknown');self.assertTrue(b.terminated)
        with self.assertRaises(FileExistsError): m.phase(0,{'inputs':{},'nested_parent_allowed':False,'environment':{}},{'review_sha256':'a'},'grant',b)
    def test_environment_is_explicit(self):
        env=m.environment('C:/Windows');self.assertNotIn('CL',env);self.assertNotIn('LINK',env);self.assertEqual(set(env),{'SystemRoot','PATH','INCLUDE','LIB','TMP','TEMP'})
if __name__=='__main__':unittest.main()
