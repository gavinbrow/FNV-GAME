import json,sys,tempfile,unittest
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path(__file__).resolve().parent));import tescontainer_script_transaction_v2 as t
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();p=Path(self.tmp.name);self.saved=t.F,t.T;t.F=p/'fn';t.T=p/'txn';t.T.mkdir();src=Path(__file__).resolve().parents[1]/'out/phase2-tescontainer-script-transaction-v2'
  for x in ('manifest.json','0.original','0.generated','1.original','1.generated'):(t.T/x).write_bytes((src/x).read_bytes())
  self.m=json.loads((t.T/'manifest.json').read_bytes())
  for x in self.m['files']:
   q=t.F/x['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((t.T/x['original']).read_bytes())
  self.p1=mock.patch.object(t,'evidence',return_value={'original_closures':{'1111':{'original_project_files':{}},'1112':{'original_project_files':{}}}});self.p2=mock.patch.object(t.locks,'acquire_guard',return_value=[]);self.p1.start();self.p2.start()
 def tearDown(self):
  self.p2.stop();self.p1.stop();t.F,t.T=self.saved;self.tmp.cleanup()
 def originals(self):
  for x in self.m['files']:self.assertEqual((t.F/x['path']).read_bytes(),(t.T/x['original']).read_bytes())
 def test_apply_restore_ack(self):
  with self.assertRaises(ValueError):t.run('apply')
  t.run('apply',True);t.run('restore');self.originals()
 def test_write_failure_rollback(self):
  real=t.atomic;calls=[]
  def fail(path,data):
   calls.append(1)
   if len(calls)==2:raise OSError('simulated')
   return real(path,data)
  with mock.patch.object(t,'atomic',side_effect=fail):
   with self.assertRaises(OSError):t.run('apply',True)
  self.originals();self.assertFalse((t.T/'applied.json').exists())
 def test_partial_marker_rollback(self):
  real=json.dump;calls=[]
  def fail(value,stream,*a,**k):
   calls.append(1)
   if len(calls)==2:stream.write('{');raise OSError('simulated')
   return real(value,stream,*a,**k)
  with mock.patch.object(t.json,'dump',side_effect=fail):
   with self.assertRaises(OSError):t.run('apply',True)
  self.originals();self.assertFalse((t.T/'applied.json').exists());self.assertFalse((t.T/'apply-result.json').exists())
 def test_mixed_recover(self):
  x=self.m['files'][0];(t.F/x['path']).write_bytes((t.T/x['generated']).read_bytes());t.run('recover');t.run('recover');self.originals()
 def test_unknown_refused(self):
  x=self.m['files'][1];(t.F/x['path']).write_bytes(b'unknown')
  with self.assertRaises(ValueError):t.run('recover')
  self.assertEqual((t.F/x['path']).read_bytes(),b'unknown')
if __name__=='__main__':unittest.main()
