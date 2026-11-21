import ast, json, os, tempfile, shutil, unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import hashlib
P=Path(__file__).resolve().parents[2]/'build_all.py'
tree=ast.parse(P.read_text());node=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='finish');module=ast.Module(body=[node],type_ignores=[]);ast.fix_missing_locations(module)
class ScratchFinish(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();root=Path(self.t.name);self.tmp=root/'scratch'/'build-a';self.tmp.mkdir(parents=True);self.out=root/'out';self.out.mkdir();self.lock=SimpleNamespace(release=lambda x:None);self.ns=dict(os=os,shutil=shutil,hashlib=hashlib,json=json,time=__import__('time'),sys=__import__('sys'),J=os.path.join,TMP_ROOT=str(self.tmp.parent),TMPD=str(self.tmp),OUT=str(self.out),LOCK_HELD=True,buildlock=self.lock,a=SimpleNamespace(keep_lock=False,skip_data_v1=False),summary={},T0=0);exec(compile(module,str(P),'exec'),self.ns)
 def tearDown(self):self.t.cleanup()
 def runfinish(self,status):
  with self.assertRaises(SystemExit) as c:self.ns['finish'](status)
  return c.exception.code
 def test_success_archives_and_removes(self):
  (self.tmp/'dv1_placed.pkl').write_bytes(b'placement');self.assertEqual(self.runfinish('ok'),0);self.assertFalse(self.tmp.exists());self.assertEqual((self.out/'evidence/data-v1-scratch/dv1_placed.pkl').read_bytes(),b'placement')
 def test_archive_failure_preserves_and_unlocks(self):
  (self.tmp/'dv1_placed.pkl').write_bytes(b'placement'); calls=[];self.lock.release=lambda x:calls.append(x)
  with patch.object(shutil,'copy2',side_effect=OSError('injected')):self.assertEqual(self.runfinish('ok'),1)
  self.assertTrue(self.tmp.exists());self.assertEqual(calls,['build-all'])
 def test_missing_success_fails_and_preserves(self):
  self.assertEqual(self.runfinish('ok'),1);self.assertTrue(self.tmp.exists())
 def test_failed_preflight_no_scratch_no_lock_release(self):
  self.ns['TMPD']=None;self.ns['LOCK_HELD']=False;calls=[];self.lock.release=lambda x:calls.append(x);self.assertEqual(self.runfinish('failed'),1);self.assertEqual(calls,[]);self.assertTrue(self.tmp.exists())
if __name__=='__main__':unittest.main()

