import json,sys,tempfile,unittest
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path(__file__).resolve().parent));import tescontainer_forward_transaction as t
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();p=Path(self.tmp.name);self.saved={k:getattr(t,k) for k in ('F','T')};t.F=p/'fn';t.T=p/'txn';t.T.mkdir();real=Path(__file__).resolve().parents[1]/'out';src=real/'phase2-tescontainer-forward-transaction';self.m=json.loads((real/'phase2-next-source-proposals-v4/manifest.json').read_text());self.m['include_closures']={'unit651':{'original_files':{}},'unit980':{'original_files':{}}};
  for x in ('manifest.json','0.original','0.generated','1.original','1.generated'):(t.T/x).write_bytes((src/x).read_bytes())
  (t.F/'build').mkdir(parents=True);(t.F/'build/units.json').write_bytes((real/'phase2-tesform-binding-repair-v3/units.generated').read_bytes())
  for x in self.m['forward']['files']:
   p=t.F/x['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((t.T/x['original']).read_bytes())
  self.p1=mock.patch.object(t,'evidence',return_value=self.m);self.p2=mock.patch.object(t.locks,'acquire_guard',return_value=[]);self.p1.start();self.p2.start()
 def tearDown(self):
  self.p2.stop();self.p1.stop()
  for k,v in self.saved.items():setattr(t,k,v)
  self.tmp.cleanup()
 def originals(self):
  for x in self.m['forward']['files']:self.assertEqual((t.F/x['path']).read_bytes(),(t.T/x['original']).read_bytes())
 def test_apply_then_restore(self):
  t.run('apply');self.assertTrue((t.T/'applied.json').exists());t.run('restore');self.originals()
 def test_second_file_failure_rolls_back_first(self):
  real=t.atomic_write;calls=[]
  def fail(path,data):
   calls.append(1)
   if len(calls)==2:raise OSError('simulated')
   return real(path,data)
  with mock.patch.object(t,'atomic_write',side_effect=fail):
   with self.assertRaises(OSError):t.run('apply')
  self.originals();self.assertFalse((t.T/'apply-result.json').exists())
 def test_partial_marker_failure_rolls_back_both(self):
  real=json.dump;calls=[]
  def fail(value,stream,*a,**k):
   calls.append(1)
   if len(calls)==2:stream.write('{');raise OSError('simulated')
   return real(value,stream,*a,**k)
  with mock.patch.object(t.json,'dump',side_effect=fail):
   with self.assertRaises(OSError):t.run('apply')
  self.originals();self.assertFalse((t.T/'applied.json').exists());self.assertFalse((t.T/'apply-result.json').exists())
 def test_recover_mixed_state_and_repeat(self):
  x=self.m['forward']['files'][0];(t.F/x['path']).write_bytes((t.T/x['generated']).read_bytes());t.run('recover');t.run('recover');self.originals();self.assertEqual(len(list(t.T.glob('recover-result-*.json'))),2)
 def test_unknown_state_refused(self):
  x=self.m['forward']['files'][1];(t.F/x['path']).write_text('unknown')
  with self.assertRaises(ValueError):t.run('recover')
  self.assertEqual((t.F/x['path']).read_text(),'unknown')
if __name__=='__main__':unittest.main()
