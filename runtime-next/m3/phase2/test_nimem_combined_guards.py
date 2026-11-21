"""Exercise environment and transitive tool guards without a compiler."""
import hashlib, json, tempfile, unittest
from pathlib import Path
import nimem_combined_825d_compile as compiler
import nimem_combined_825d_run as runner
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class Guards(unittest.TestCase):
 def test_child_environment_removes_inherited_flags(self):
  source={'CL':'/O1','_cl_':'/DWRONG','Fnv_M3':'1','CODEX_NEGATIVE':'b8v','codex_negative_extra':'x','PATH':'safe','TMP':'x'}
  self.assertEqual(compiler.clean_env(source),{'PATH':'safe','TMP':'x'})
  self.assertEqual(source['CL'],'/O1')
 def test_changed_transitive_rejected_before_any_command(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);helper=p/'transitive.py';helper.write_text('good');self_file=p/'runner.py';self_file.write_text('runner')
   manifest=p/'closure.json';manifest.write_text(json.dumps({'files':{'transitive.py':sha(helper)}}))
   pin=sha(manifest);own=sha(self_file);runner.verify_tool_closure(p,manifest,pin,self_file,own)
   helper.write_text('changed')
   with self.assertRaises(runner.ToolDrift):runner.verify_tool_closure(p,manifest,pin,self_file,own)
 def test_changed_runner_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);manifest=p/'closure.json';manifest.write_text('{"files":{}}');f=p/'runner.py';f.write_text('old');pin=sha(f);f.write_text('new')
   with self.assertRaises(runner.ToolDrift):runner.verify_tool_closure(p,manifest,sha(manifest),f,pin)
if __name__=='__main__':unittest.main()
