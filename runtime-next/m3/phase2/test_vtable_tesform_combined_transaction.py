import json,sys,tempfile,unittest
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path(__file__).resolve().parent));import vtable_tesform_combined_transaction as t
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();p=Path(self.tmp.name);self.saved={k:getattr(t,k) for k in ('F','T')};realF=t.F;realT=t.T;t.F=p/'fn';t.T=p/'txn';t.T.mkdir();self.m=json.loads((realT/'manifest.json').read_bytes())
  for x in ('manifest.json',*[str(i)+'.'+z for i in range(5) for z in ('original','generated')]):(t.T/x).write_bytes((realT/x).read_bytes())
  closure=set()
  for folder in ('phase2-tesform-two-flagpairs-mirror','phase2-bgs-two-flagpairs-mirror'):closure.update(json.loads((t.O/folder/'mirror-manifest.json').read_bytes())['original_inputs'])
  sm=json.loads((t.O/'phase2-tescontainer-script-removal/manifest.json').read_bytes())
  for i in ('1111','1112'):closure.update(sm['original_closures'][i]['original_project_files'])
  for rel in closure:
   q=t.F/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((realF/rel).read_bytes())
  for x in self.m['files']:
   q=t.F/x['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((t.T/x['original']).read_bytes())
  self.p=mock.patch.object(t.locks,'acquire_guard',return_value=[]);self.p.start()
 def tearDown(self):
  self.p.stop()
  for k,v in self.saved.items():setattr(t,k,v)
  self.tmp.cleanup()
 def originals(self):
  for x in self.m['files']:self.assertEqual((t.F/x['path']).read_bytes(),(t.T/x['original']).read_bytes())
 def test_apply_restore(self):t.run('apply',True);t.run('restore');self.originals()
 def test_ack(self):
  with self.assertRaises(ValueError):t.run('apply')
 def test_partial_write(self):
  real=t.atomic;calls=[]
  def fail(p,d):
   calls.append(1)
   if len(calls)==3:raise OSError('simulated')
   return real(p,d)
  with mock.patch.object(t,'atomic',side_effect=fail):
   with self.assertRaises(OSError):t.run('apply',True)
  self.originals()
 def test_marker_partial(self):
  real=json.dump;calls=[]
  def fail(value,stream,*a,**kw):
   calls.append(1)
   if len(calls)==2:stream.write('{');raise OSError('simulated')
   return real(value,stream,*a,**kw)
  with mock.patch.object(t.json,'dump',side_effect=fail):
   with self.assertRaises(OSError):t.run('apply',True)
  self.originals();self.assertFalse((t.T/'applied.json').exists());self.assertFalse((t.T/'apply-result.json').exists())
 def test_recovery(self):
  x=self.m['files'][2];p=t.F/x['path'];p.write_bytes((t.T/x['generated']).read_bytes());t.run('recover');t.run('recover');self.originals();p.write_text('unknown')
  with self.assertRaises(ValueError):t.run('recover')
if __name__=='__main__':unittest.main()
