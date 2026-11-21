import json,sys,tempfile,unittest
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path(__file__).resolve().parent));import tesform_typed_transaction as t
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();p=Path(self.tmp.name);self.oldF,self.oldT=t.F,t.T;t.F=p/'fn';t.T=p/'txn';t.T.mkdir();original=Path(__file__).resolve().parents[1]/'out/phase2-tesform-typed-transaction';self.m=json.loads((original/'manifest.json').read_text())
  for x in self.m['files']:
   for k in ('original','generated'):(t.T/x[k]).write_bytes((original/x[k]).read_bytes())
   target=t.F/x['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((t.T/x['original']).read_bytes())
  self.a=mock.patch.object(t,'manifest',return_value=self.m);self.b=mock.patch.object(t.lock,'acquire_guard',return_value=[]);self.c=mock.patch.object(t,'validate_closures');self.a.start();self.b.start();self.c.start()
 def tearDown(self):
  self.c.stop();self.b.stop();self.a.stop();t.F,t.T=self.oldF,self.oldT;self.tmp.cleanup()
 def verify_old(self):
  for x in self.m['files']:self.assertEqual((t.F/x['path']).read_bytes(),(t.T/x['original']).read_bytes())
 def test_apply_requires_explicit_mirror_ack(self):
  with self.assertRaises(ValueError):t.run('apply')
  self.verify_old()
 def test_apply_and_restore(self):
  t.run('apply',True);t.run('restore');self.verify_old()
 def test_late_file_failure_rolls_back(self):
  real=t.atomic_write;count=[]
  def fail(p,d):
   count.append(1)
   if len(count)==6:raise OSError('simulated')
   return real(p,d)
  with mock.patch.object(t,'atomic_write',side_effect=fail):
   with self.assertRaises(OSError):t.run('apply',True)
  self.verify_old()
 def test_partial_apply_marker_rolls_back(self):
  real=json.dump;count=[]
  def fail(v,f,*a,**k):
   count.append(1)
   if len(count)==2:f.write('{');raise OSError('simulated')
   return real(v,f,*a,**k)
  with mock.patch.object(t.json,'dump',side_effect=fail):
   with self.assertRaises(OSError):t.run('apply',True)
  self.verify_old();self.assertFalse((t.T/'applied.json').exists());self.assertFalse((t.T/'apply-result.json').exists())
 def test_mixed_recover_and_unknown_refusal(self):
  x=self.m['files'][0];(t.F/x['path']).write_bytes((t.T/x['generated']).read_bytes());t.run('recover');self.verify_old();(t.F/x['path']).write_text('unknown')
  with self.assertRaises(ValueError):t.run('recover')
if __name__=='__main__':unittest.main()
