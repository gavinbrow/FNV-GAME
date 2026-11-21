import json,shutil,sys,tempfile,unittest
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path(__file__).resolve().parent));import next_data_batch_apply as t
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();p=Path(self.tmp.name);self.oldroot=t.ROOT;self.oldtxn=t.T;real=t.ROOT;tx=t.T;t.ROOT=p/'root';t.T=p/'txn';shutil.copytree(tx,t.T)
  self.manifest=json.loads((t.T/'manifest.json').read_text());e=json.loads((real/'runtime-next/m3/phase2/next_batch_manifest.json').read_text())
  paths=['fnv_decomp/build/units.json','runtime-next/m3/phase2/selection.json','runtime-next/m3/phase2/library_candidates.json','runtime-next/m3/config.py','runtime-next/m3/phase2/next_batch_manifest.json']+[x['path'] for x in e['source_evidence']]+list(t.FIXTURES.values())
  for n in paths:
   dst=t.ROOT/n;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(real/n,dst)
  for x in self.manifest['files']:
   dst=t.ROOT/x['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(t.T/x['original'],dst)
  self.lock=mock.patch.object(t.locks,'acquire_guard',return_value=[]);self.lock.start()
 def tearDown(self):self.lock.stop();t.ROOT=self.oldroot;t.T=self.oldtxn;self.tmp.cleanup()
 def originals(self):
  for x in self.manifest['files']:self.assertEqual((t.ROOT/x['path']).read_bytes(),(t.T/x['original']).read_bytes())
 def test_apply_restore_defaults_unchanged(self):
  before=(t.ROOT/'runtime-next/m3/phase2/selection.json').read_bytes();t.run('apply');t.run('restore');self.originals();self.assertEqual(before,(t.ROOT/'runtime-next/m3/phase2/selection.json').read_bytes())
 def test_bad_target_and_second_apply_refused(self):
  q=t.ROOT/self.manifest['files'][0]['path'];q.write_bytes(b'unknown')
  with self.assertRaises(ValueError):t.run('apply')
  q.write_bytes((t.T/'0.original').read_bytes());t.run('apply')
  with self.assertRaises(FileExistsError):t.run('apply')
 def test_rollback_on_midwrite_and_marker_failure(self):
  original=t.atomic;calls=[]
  def fail(p,d):
   calls.append(p)
   if len(calls)==3:raise OSError('simulated')
   return original(p,d)
  with mock.patch.object(t,'atomic',side_effect=fail):
   with self.assertRaises(OSError):t.run('apply')
  self.originals();self.assertFalse((t.T/'apply-result.json').exists())
  with mock.patch.object(t.json,'dump',side_effect=OSError('marker')):
   with self.assertRaises(OSError):t.run('apply')
  self.originals();self.assertFalse((t.T/'applied.json').exists())
 def test_mixed_recovery_and_unknown_refusal(self):
  x=self.manifest['files'][2];p=t.ROOT/x['path'];p.write_bytes(b'unknown')
  with self.assertRaisesRegex(ValueError,'unknown target state'):t.run('recover')
  self.assertEqual(p.read_bytes(),b'unknown');p.write_bytes((t.T/x['generated']).read_bytes());t.run('recover');self.originals()
  with self.assertRaises(FileExistsError):t.run('recover')
 def test_lock_before_any_input_check(self):
  with mock.patch.object(t.locks,'acquire_guard',side_effect=ValueError('locked')):
   with mock.patch.object(t,'read_manifest',side_effect=AssertionError('must not read')):
    with self.assertRaisesRegex(ValueError,'locked'):t.run('apply')
 def test_changed_selection_refused(self):
  (t.ROOT/'runtime-next/m3/phase2/selection.json').write_bytes(b'changed')
  with self.assertRaisesRegex(ValueError,'accepted preimage'):t.run('apply')
  self.originals()
if __name__=='__main__':unittest.main()
