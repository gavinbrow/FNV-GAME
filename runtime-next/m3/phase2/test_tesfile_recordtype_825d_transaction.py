import json,sys,tempfile,unittest
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path(__file__).resolve().parent));import tesfile_recordtype_825d_transaction as t
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();p=Path(self.tmp.name);self.saved=t.F,t.D;self.real_f=t.F;self.real_d=t.D;t.F=p/'fn';t.D=p/'txn';t.D.mkdir();m=json.loads((self.real_d/'manifest.json').read_text());self.m=m
  for n in ('manifest.json','0.original','0.generated','1.original','1.generated'):(t.D/n).write_bytes((self.real_d/n).read_bytes())
  paths=set(m['source_closure_sha256']);q=json.loads((t.P/'manifest.json').read_text());paths.add(q['source_other_unit_path'])
  for rel in paths:
   x=t.F/rel;x.parent.mkdir(parents=True,exist_ok=True);x.write_bytes((self.real_f/rel).read_bytes())
  (t.F/'build').mkdir(parents=True,exist_ok=True);(t.F/'build/units.json').write_bytes((t.D/'0.original').read_bytes());self.lock=mock.patch.object(t.locks,'acquire_guard',return_value=[]);self.lock.start()
 def tearDown(self):self.lock.stop();t.F,t.D=self.saved;self.tmp.cleanup()
 def originals(self):
  for x in self.m['files']:self.assertEqual((t.F/x['path']).read_bytes(),(t.D/x['original']).read_bytes())
 def test_ack_apply_restore(self):
  with self.assertRaises(ValueError):t.run('apply')
  t.run('apply',True);t.run('restore');self.originals()
 def test_second_write_rollback(self):
  real=t.atomic;calls=[]
  def fail(path,data):
   calls.append(1)
   if len(calls)==2:raise OSError('simulated')
   return real(path,data)
  with mock.patch.object(t,'atomic',side_effect=fail):
   with self.assertRaises(OSError):t.run('apply',True)
  self.originals();self.assertFalse((t.D/'applied.json').exists())
 def test_partial_marker_rollback(self):
  real=json.dump;calls=[]
  def fail(v,stream,*a,**k):
   calls.append(1)
   if len(calls)==2:stream.write('{');raise OSError('simulated')
   return real(v,stream,*a,**k)
  with mock.patch.object(t.json,'dump',side_effect=fail):
   with self.assertRaises(OSError):t.run('apply',True)
  self.originals();self.assertFalse((t.D/'apply-result.json').exists());self.assertFalse((t.D/'applied.json').exists())
 def test_mixed_recovery(self):
  x=self.m['files'][1];(t.F/x['path']).write_bytes((t.D/x['generated']).read_bytes());t.run('recover');t.run('recover');self.originals()
 def test_unknown_rejected(self):
  x=self.m['files'][1];(t.F/x['path']).write_text('unknown')
  with self.assertRaises(ValueError):t.run('recover')
  self.assertEqual((t.F/x['path']).read_text(),'unknown')
if __name__=='__main__':unittest.main()
