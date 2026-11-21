import json,shutil,sys,tempfile,unittest
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path(__file__).resolve().parent));import combined_source_apply as t
class TransactionTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();root=Path(self.tmp.name);self.old=(t.R,t.F,t.T,t.PIN);realroot,realf,realt,_=self.old;t.R=root;t.F=root/'fnv_decomp';t.T=root/'txn';shutil.copytree(realt,t.T);m=json.loads((t.T/'manifest.json').read_text());self.m=m;t.PIN=t.sha(t.T/'manifest.json')
  for rel in m['required_inputs']:
   dst=root/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(realroot/rel,dst)
  for rel in m['source_closure']:
   dst=t.F/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(realf/rel,dst)
  for x in m['files']:
   p=t.F/x['path'];p.parent.mkdir(parents=True,exist_ok=True)
   if x['original'] is None:p.unlink(missing_ok=True)
   else:shutil.copyfile(t.T/x['original'],p)
  self.lock=mock.patch.object(t.locks,'acquire_guard',return_value=[]);self.lock.start()
 def tearDown(self):self.lock.stop();t.R,t.F,t.T,t.PIN=self.old;self.tmp.cleanup()
 def assert_originals(self):
  for x in self.m['files']:
   p=t.F/x['path'];self.assertEqual(t.read(p),(t.T/x['original']).read_bytes() if x['original'] else None,x['path'])
 def test_unknown_preimage_refused(self):
  x=next(x for x in self.m['files'] if x['original'] is None);p=t.F/x['path'];p.write_bytes(b'unknown')
  with self.assertRaisesRegex(ValueError,'unknown target state'):t.run('apply')
  self.assertEqual(p.read_bytes(),b'unknown');self.assertFalse((t.T/'applied.json').exists())
 def test_midwrite_rollback_new_headers(self):
  real=t.atomic;calls=[]
  def fail(p,data):
   calls.append((p,data))
   if len(calls)==14:raise OSError('injected midwrite')
   real(p,data)
  with mock.patch.object(t,'atomic',side_effect=fail):
   with self.assertRaises(OSError):t.run('apply')
  self.assertTrue(any(data is not None and str(p).endswith('_native.h') for p,data in calls));self.assert_originals();self.assertFalse((t.T/'applied.json').exists())
 def test_marker_failure_rolls_back(self):
  with mock.patch.object(t.json,'dump',side_effect=OSError('marker fail')):
   with self.assertRaises(OSError):t.run('apply')
  self.assert_originals();self.assertFalse((t.T/'applied.json').exists());self.assertFalse((t.T/'apply-result.json').exists())
 def test_apply_restore_and_mixed_recover(self):
  t.run('apply');t.run('restore');self.assert_originals()
  for x in self.m['files'][::2]:
   p=t.F/x['path'];p.write_bytes((t.T/x['candidate']).read_bytes())
  t.run('recover');self.assert_originals()
 def test_unknown_mixed_recovery_refused(self):
  x=self.m['files'][0];p=t.F/x['path'];p.write_bytes(b'unknown')
  with self.assertRaisesRegex(ValueError,'unknown target state'):t.run('recover')
  self.assertEqual(p.read_bytes(),b'unknown')
 def test_lock_before_manifest(self):
  with mock.patch.object(t.locks,'acquire_guard',side_effect=ValueError('locked')):
   with self.assertRaisesRegex(ValueError,'locked'):t.run('apply')
if __name__=='__main__':unittest.main()
