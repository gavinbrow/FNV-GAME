import json,os,sys,tempfile,unittest
from unittest import mock
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import rtti_tesform_bindings_transaction as t
class TxTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();p=Path(self.tmp.name);self.saved={k:getattr(t,k) for k in ('T','E','TARGET','LOCK','GLOBAL_LOCK')};self.override=os.environ.pop('FNV_BUILD_LOCK',None);t.T=p/'txn';t.E=p/'evidence';t.T.mkdir();t.E.mkdir();real=Path(__file__).resolve().parents[1]/'out';
  for n in ('units.original','units.generated','manifest.json'):(t.T/n).write_bytes((real/'phase2-tesform-bindings-transaction'/n).read_bytes())
  (t.E/'manifest.json').write_bytes((real/'phase2-tesform-binding-repair-v2/manifest.json').read_bytes());t.TARGET=p/'units.json';t.LOCK=p/'build.lock';t.GLOBAL_LOCK=t.LOCK
 def tearDown(self):
  for k,v in self.saved.items():setattr(t,k,v)
  if self.override is not None:os.environ['FNV_BUILD_LOCK']=self.override
  self.tmp.cleanup()
 def test_semantic_scope(self):
  old=(t.T/'units.original').read_bytes();new=(t.T/'units.generated').read_bytes();e=json.loads((t.E/'manifest.json').read_text());t.validate_payloads(old,new,e)
  with self.assertRaises(ValueError):t.validate_payloads(old,new+b' ',e)
 def test_active_lock_refuses_recovery(self):
  t.TARGET.write_bytes((t.T/'units.generated').read_bytes());t.LOCK.write_text('active');before=t.TARGET.read_bytes()
  with self.assertRaises(ValueError):t.run('recover')
  self.assertEqual(before,t.TARGET.read_bytes());self.assertEqual(t.LOCK.read_text(),'active')
 def test_failed_lock_write_releases_created_lock(self):
  with mock.patch.object(t.os,'write',side_effect=OSError('simulated lock write failure')):
   with self.assertRaises(ValueError):t.acquire_guard()
  self.assertFalse(t.LOCK.exists())
 def test_recovery_from_known_new_state(self):
  t.TARGET.write_bytes((t.T/'units.generated').read_bytes());t.run('recover');self.assertEqual(t.TARGET.read_bytes(),(t.T/'units.original').read_bytes());t.run('recover');self.assertEqual(len(list(t.T.glob('recover-result-*.json'))),2);self.assertFalse(t.LOCK.exists())
 def test_recovery_refuses_unknown_state(self):
  t.TARGET.write_bytes(b'other')
  with self.assertRaises(ValueError):t.run('recover')
  self.assertEqual(t.TARGET.read_bytes(),b'other');self.assertFalse(t.LOCK.exists())
 def test_restore_requires_apply_record(self):
  t.TARGET.write_bytes((t.T/'units.generated').read_bytes())
  with self.assertRaises(ValueError):t.run('restore')
 def test_apply_partial_marker_failure_rolls_back_and_cleans_marker(self):
  old=(t.T/'units.original').read_bytes();t.TARGET.write_bytes(old);original_dump=json.dump;calls=[]
  def fail_second(value,stream,*args,**kwargs):
   calls.append(1)
   if len(calls)==2:stream.write('{');raise OSError('simulated partial marker write')
   return original_dump(value,stream,*args,**kwargs)
  with mock.patch.object(t,'validate_current_inputs'),mock.patch.object(t.json,'dump',side_effect=fail_second):
   with self.assertRaises(OSError):t.run('apply')
  self.assertEqual(t.TARGET.read_bytes(),old);self.assertFalse((t.T/'applied.json').exists());self.assertFalse((t.T/'apply-result.json').exists());self.assertFalse(t.LOCK.exists())
if __name__=='__main__':unittest.main()
