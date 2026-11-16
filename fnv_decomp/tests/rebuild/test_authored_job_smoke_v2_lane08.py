"""Authored-only fixture lease/read checks; no process or kernel calls."""
import copy,datetime,importlib.util,io,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
P=Path(__file__).resolve().parents[2]/'build/rebuild/uuid-seven-authored-job-smoke-v2.py';s=importlib.util.spec_from_file_location('authored_job_smoke_peer',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def fixture(base):
 here=base/'build/rebuild';registry=here/'application-frontier-dispatch-v1/resource-leases.json';registry.parent.mkdir(parents=True)
 request=dict(smoke_source_sha256='a'*64,watchdog_source_sha256='b'*64);rp=here/'authored-request.json';ip=here/'authored-review.json'
 pins={rp.name:'c'*64,Path(m.__file__).name:'a'*64,m.WATCH.name:'b'*64,ip.name:'d'*64}
 row=dict(owner='/root/rebuild_eh_recovery',resource='CPU_heavy',slot=1,review_sha256='d'*64,input_pins=pins,state='granted',max_seconds=60,granted_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 state=dict(schema_version=1,CPU_heavy_capacity=2,leases=[row]);return here,registry,request,rp,ip,state
class AuthoredSmokeIndependentTests(unittest.TestCase):
 def test_exact_lease_is_read_only_and_any_source_pin_drift_rejected(self):
  with tempfile.TemporaryDirectory() as directory:
   here,registry,q,rp,ip,state=fixture(Path(directory));registry.write_text(json.dumps(state));before=registry.read_bytes()
   with patch.object(m,'HERE',here):
    grant=m.current_lease(None,q,rp,'c'*64,ip,'d'*64,1);self.assertEqual(grant['owner'],'/root/rebuild_eh_recovery');self.assertEqual(registry.read_bytes(),before)
    for key in state['leases'][0]['input_pins']:
     bad=copy.deepcopy(state);bad['leases'][0]['input_pins'][key]='e'*64;registry.write_text(json.dumps(bad))
     with self.subTest(key=key),self.assertRaises(ValueError):m.current_lease(None,q,rp,'c'*64,ip,'d'*64,1)
 def test_exact_granted_running_predicate_and_other_states_reject(self):
  with tempfile.TemporaryDirectory() as directory:
   here,registry,q,rp,ip,state=fixture(Path(directory))
   for value in ('granted','running','reserved-awaiting-process-identity','released','completed','expired'):
    candidate=copy.deepcopy(state);candidate['leases'][0]['state']=value;registry.write_text(json.dumps(candidate))
    with patch.object(m,'HERE',here),self.subTest(state=value):
     if value in ('granted','running'):self.assertEqual(m.current_lease(None,q,rp,'c'*64,ip,'d'*64,1)['owner'],'/root/rebuild_eh_recovery')
     else:
      with self.assertRaises(ValueError):m.current_lease(None,q,rp,'c'*64,ip,'d'*64,1)
 def test_foreign_owner_or_duplicate_lease_cannot_authorize_fixture(self):
  with tempfile.TemporaryDirectory() as directory:
   here,registry,q,rp,ip,state=fixture(Path(directory))
   for change in ('owner','duplicate'):
    bad=copy.deepcopy(state)
    if change=='owner':bad['leases'][0]['owner']='/root/rebuild_startup_host'
    else:bad['leases'].append(copy.deepcopy(bad['leases'][0]))
    registry.write_text(json.dumps(bad))
    with patch.object(m,'HERE',here),self.subTest(change=change),self.assertRaises(ValueError):m.current_lease(None,q,rp,'c'*64,ip,'d'*64,1)
 def test_future_expired_and_locked_lease_refuse(self):
  with tempfile.TemporaryDirectory() as directory:
   here,registry,q,rp,ip,state=fixture(Path(directory))
   for offset in (-120,120):
    bad=copy.deepcopy(state);bad['leases'][0]['granted_utc']=(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=offset)).isoformat();registry.write_text(json.dumps(bad))
    with patch.object(m,'HERE',here),self.subTest(offset=offset),self.assertRaises(ValueError):m.current_lease(None,q,rp,'c'*64,ip,'d'*64,1)
   registry.with_name('resource-leases.lock').write_bytes(b'authored')
   with patch.object(m,'HERE',here),patch.object(m,'bounded',side_effect=AssertionError('must not read locked registry')):
    with self.assertRaisesRegex(ValueError,'locked'):m.current_lease(None,q,rp,'c'*64,ip,'d'*64,1)
 def test_growing_source_is_bounded_before_join_or_parse(self):
  with tempfile.TemporaryDirectory() as directory:
   p=Path(directory)/'source';p.write_bytes(b'a')
   with patch.object(Path,'open',return_value=io.BytesIO(b'x'*20)):
    with self.assertRaisesRegex(ValueError,'growing'):m.bounded(p,5)
 def test_late_publication_failure_preserves_failed_owned_receipt(self):
  with tempfile.TemporaryDirectory() as directory:
   control=Path(directory);calls=[0]
   def verify():
    calls[0]+=1
    if calls[0]==2:raise ValueError('authored late source drift')
   self.assertFalse(m.publish_receipt(control,dict(status='pass'),verify));self.assertFalse((control/'receipt.json').exists());self.assertTrue((control/'receipt.json.failed').exists());self.assertTrue((control/'fixture-failure.json').exists())
 def test_foreign_receipt_replacement_never_removed_or_accepted(self):
  with tempfile.TemporaryDirectory() as directory:
   base=Path(directory);control=base/'control';control.mkdir();foreign=base/'foreign';foreign.write_bytes(b'authored foreign content');calls=[0]
   def verify():
    calls[0]+=1
    if calls[0]==2:os.replace(foreign,control/'receipt.json')
   self.assertFalse(m.publish_receipt(control,dict(status='pass'),verify));self.assertEqual((control/'receipt.json').read_bytes(),b'authored foreign content');self.assertFalse((control/'receipt.json.failed').exists());self.assertTrue((control/'fixture-failure.json').exists())
if __name__=='__main__':unittest.main()
