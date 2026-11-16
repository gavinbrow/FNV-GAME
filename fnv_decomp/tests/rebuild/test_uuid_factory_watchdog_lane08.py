"""Mocked watchdog launch failures; no real processes or protected inputs."""
import importlib.util,json,sys,tempfile,types,unittest
from pathlib import Path
from unittest.mock import patch

SOURCE=Path(__file__).resolve().parents[2]/'build/rebuild/uuid2768-factory-watchdog-v3.py'
spec=importlib.util.spec_from_file_location('uuid_watchdog_lane08_target',SOURCE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Child:
    pid=12345;_handle=123
    def __init__(self,code=None):self.code=code;self.killed=False;self.waited=False
    def poll(self):return self.code
    def kill(self):self.killed=True;self.code=1
    def wait(self):self.waited=True;return self.code

class UUIDWatchdogIndependentTests(unittest.TestCase):
    def setup_case(self,root):
        build=root/'build/rebuild';build.mkdir(parents=True)
        req=build/'uuid2768-factory-watch-request-v3.json';inp=build/'uuid2768-factory-input-review-v2.json';peer=build/'uuid2768-factory-watchdog-review-v3.json'
        op=build/'uuid2768-factory-operation-v2.json';factory=root/'tools/rebuild/uuid_directive_factory.py'
        request=dict(schema_version=1,kind='uuid2768-factory-watch-request-v3',operation_sha256='1'*64,
            factory_sha256='2'*64,factory_tests_sha256='3'*64,factory_doc_sha256='4'*64,watchdog_sha256='5'*64,
            watchdog_tests_sha256='6'*64,interpreter_sha256='7'*64,max_seconds=900,max_memory_bytes=1073741824,max_output_bytes=134217728)
        review=dict(kind='finite-uuid2768-factory-input-review-v1',approved=True,root_authorized=True,
            source_sha256={'tools/rebuild/uuid_directive_factory.py':'2'*64})
        wr=dict(kind='uuid2768-factory-watchdog-independent-review-v1',status='accepted',watch_request_sha256='a'*64,
            watchdog_sha256='5'*64,watchdog_tests_sha256='6'*64,input_review_sha256='b'*64)
        for p,v in ((req,request),(inp,review),(peer,wr)):p.write_text(json.dumps(v))
        hashes={req:'a'*64,inp:'b'*64,peer:'c'*64,op:'1'*64,factory:'2'*64,
            root/'tests/rebuild/test_uuid_directive_factory.py':'3'*64,root/'docs/rebuild/UUID-DIRECTIVE-FACTORY.md':'4'*64,
            Path(m.__file__):'5'*64,build/'uuid2768-factory-watchdog-v3-tests.py':'6'*64,Path(sys.executable):'7'*64}
        argv=['--watch-request',str(req),'--watch-request-sha256','a'*64,'--input-review',str(inp),
              '--input-review-sha256','b'*64,'--watch-review',str(peer),'--watch-review-sha256','c'*64,'--slot','1']
        patches=dict(ROOT=root,OP=op,FACTORY=factory,CONTROL=build/'uuid2768-factory-control-v3',OUTPUT=build/'uuid2768-factory-result-v2')
        return build,argv,hashes,patches,inp

    def contexts(self,patches,hashes):
        return patch.multiple(m,**patches),patch.object(m,'sha',side_effect=lambda p:hashes[Path(p)]),patch.object(m,'lease',return_value={'fixture':'exact grant'})

    def test_launch_failure_has_durable_intent_and_failed_terminal(self):
        with tempfile.TemporaryDirectory() as tmp:
            build,argv,hashes,paths,_=self.setup_case(Path(tmp));a,b,c=self.contexts(paths,hashes)
            def fail(*args,**kwargs):
                intent=json.loads((paths['CONTROL']/'prelaunch.json').read_text())
                self.assertEqual(intent['state'],'launch-intent-no-replay');raise OSError('authored spawn failure')
            with a,b,c,patch.object(m.subprocess,'Popen',side_effect=fail):self.assertEqual(m.main(argv),2)
            result=json.loads((paths['CONTROL']/'receipt.json').read_text())
            self.assertEqual(result['reason'],'process-launch-failed');self.assertFalse(paths['OUTPUT'].exists())

    def test_pid_record_failure_kills_and_waits_only_owned_child(self):
        with tempfile.TemporaryDirectory() as tmp:
            _,argv,hashes,paths,_=self.setup_case(Path(tmp));a,b,c=self.contexts(paths,hashes);child=Child();save=m.save_new
            def write(path,value):
                if path.name=='started.json':raise OSError('authored PID record failure')
                return save(path,value)
            with a,b,c,patch.object(m.subprocess,'Popen',return_value=child),patch.object(m,'save_new',side_effect=write):self.assertEqual(m.main(argv),2)
            self.assertTrue(child.killed and child.waited)
            self.assertEqual(json.loads((paths['CONTROL']/'receipt.json').read_text())['reason'],'start-or-monitor-failed')

    def test_wrong_input_review_rejects_before_child_or_control_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            _,argv,hashes,paths,inp=self.setup_case(Path(tmp));v=json.loads(inp.read_text());v['approved']=False;inp.write_text(json.dumps(v))
            a,b,c=self.contexts(paths,hashes)
            with a,b,c,patch.object(m.subprocess,'Popen',side_effect=AssertionError('must not launch')):
                with self.assertRaisesRegex(ValueError,'input review differs'):m.main(argv)
            self.assertFalse(paths['CONTROL'].exists())

    def test_fast_exit_without_any_memory_sample_is_failed_not_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            _,argv,hashes,paths,_=self.setup_case(Path(tmp));a,b,c=self.contexts(paths,hashes);child=Child(0)
            api=types.SimpleNamespace(psapi=types.SimpleNamespace(GetProcessMemoryInfo=lambda *a:0))
            with a,b,c,patch.object(m.subprocess,'Popen',return_value=child),patch.object(m.ctypes,'windll',api):self.assertEqual(m.main(argv),2)
            result=json.loads((paths['CONTROL']/'receipt.json').read_text())
            self.assertEqual(result['reason'],'no-memory-sample');self.assertEqual(result['status'],'failed')

if __name__=='__main__':unittest.main()
