import hashlib,json,shutil,sys,tempfile,unittest
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path(__file__).resolve().parent));import next_data_promotion_apply as t
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();p=Path(self.tmp.name);self.saved=(t.ROOT,t.T,t.PIN);t.ROOT=p/'root';t.T=p/'txn';shutil.copytree(self.saved[1],t.T)
  self.m=json.loads((t.T/'manifest.provisional.json').read_text());self.m['required_inputs']={};self.m['source_snapshot']='snapshot.json';raw=json.dumps(self.m).encode();(t.T/'manifest.final.json').write_bytes(raw);t.PIN=hashlib.sha256(raw).hexdigest()
  t.ROOT.mkdir();(t.ROOT/'snapshot.json').write_text('{}')
  for x in self.m['files']:
   q=t.ROOT/x['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((t.T/x['original']).read_bytes())
  self.lock=mock.patch.object(t.locks,'acquire_guard',return_value=[]);self.lock.start()
 def tearDown(self):self.lock.stop();t.ROOT,t.T,t.PIN=self.saved;self.tmp.cleanup()
 def originals(self):
  for x in self.m['files']:self.assertEqual((t.ROOT/x['path']).read_bytes(),(t.T/x['original']).read_bytes())
 def test_apply_restore_and_duplicate_refusal(self):
  t.run('apply')
  with self.assertRaises(FileExistsError):t.run('apply')
  t.run('restore');self.originals()
 def test_preimage_and_evidence_refusal(self):
  x=self.m['files'][0];p=t.ROOT/x['path'];p.write_bytes(b'bad')
  with self.assertRaises(ValueError):t.run('apply')
  p.write_bytes((t.T/x['original']).read_bytes());(t.T/'0.candidate').write_bytes(b'bad')
  with self.assertRaisesRegex(ValueError,'payload'):t.run('apply')
  self.originals()
 def test_rollback_and_mixed_recovery(self):
  real=t.atomic;calls=[]
  def fail(p,d):
   calls.append(p)
   if len(calls)==3:raise OSError('injected')
   return real(p,d)
  with mock.patch.object(t,'atomic',side_effect=fail):
   with self.assertRaises(OSError):t.run('apply')
  self.originals();x=self.m['files'][1];(t.ROOT/x['path']).write_bytes((t.T/x['candidate']).read_bytes());t.run('recover');self.originals()
 def test_lock_precedes_manifest(self):
  with mock.patch.object(t.locks,'acquire_guard',side_effect=ValueError('locked')):
   with mock.patch.object(t,'read_manifest',side_effect=AssertionError('early read')):
    with self.assertRaisesRegex(ValueError,'locked'):t.run('apply')
if __name__=='__main__':unittest.main()
