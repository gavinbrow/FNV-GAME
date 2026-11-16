"""Narrow authored lease-state successor tests; no real registry/kernel/process."""
import copy,datetime,importlib.util,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
P=Path(__file__).resolve().parents[2]/'build/rebuild/uuid-seven-prospective-eh-watchdog-v2.py';s=importlib.util.spec_from_file_location('watch_v2_state_peer',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
NOW=datetime.datetime(2026,11,4,12,tzinfo=datetime.timezone.utc)
def fixture(base):
 here=base/'build/rebuild';registry=here/'application-frontier-dispatch-v1/resource-leases.json';registry.parent.mkdir(parents=True)
 c=dict(profile_path=here/'authored-profile.json',profile_raw_sha256='a'*64,child_path=here/'authored-child.json',child_raw_sha256='b'*64,profile={'source_pins':{m.WATCH:'c'*64,m.BOOT:'d'*64}},input_review_path=here/'authored-input.json',input_review={'sha256':'e'*64},watch_review_path=here/'authored-watch-review.json',watch_review={'sha256':'f'*64})
 pins={c['profile_path'].name:'a'*64,c['child_path'].name:'b'*64,Path(m.WATCH).name:'c'*64,Path(m.BOOT).name:'d'*64,c['input_review_path'].name:'e'*64,c['watch_review_path'].name:'f'*64}
 row=dict(owner='/root/rebuild_startup_host',resource='CPU_heavy',slot=1,granted_utc=(NOW-datetime.timedelta(seconds=5)).isoformat(),max_seconds=600,review_sha256='f'*64,input_pins=pins,state='granted')
 state=dict(schema_version=1,CPU_heavy_capacity=2,lightweight_metadata_capacity=2,leases=[row]);return here,registry,c,state
class LeaseSuccessorIndependentTests(unittest.TestCase):
 def test_granted_to_running_preserves_stable_grant_and_readonly_registry(self):
  with tempfile.TemporaryDirectory() as directory:
   here,p,c,state=fixture(Path(directory));p.write_text(json.dumps(state));before=p.read_bytes()
   with patch.object(m,'HERE',here):
    first=m.lease(c,1,NOW);self.assertEqual(before,p.read_bytes());state['leases'][0].update(state='running',pid=12345);p.write_text(json.dumps(state));second=m.lease(c,1,NOW)
   self.assertEqual(first,second);self.assertEqual(m.grant_identifier(first),m.grant_identifier(second))
 def test_all_six_pins_and_foreign_owner_are_rejected(self):
  with tempfile.TemporaryDirectory() as directory:
   here,p,c,state=fixture(Path(directory))
   for key in state['leases'][0]['input_pins']:
    bad=copy.deepcopy(state);bad['leases'][0]['input_pins'][key]='0'*64;p.write_text(json.dumps(bad))
    with patch.object(m,'HERE',here),self.subTest(pin=key),self.assertRaises(ValueError):m.lease(c,1,NOW)
   state['leases'][0]['owner']='/root/rebuild_eh_recovery';p.write_text(json.dumps(state))
   with patch.object(m,'HERE',here),self.assertRaises(ValueError):m.lease(c,1,NOW)
 def test_600_second_capacity_does_not_raise_540_runtime_and_expiry_still_blocks(self):
  self.assertEqual(m.LIMITS['seconds'],540)
  with tempfile.TemporaryDirectory() as directory:
   here,p,c,state=fixture(Path(directory));p.write_text(json.dumps(state))
   with patch.object(m,'HERE',here):
    self.assertEqual(m.lease(c,1,NOW)['max_seconds'],600)
    with self.assertRaises(ValueError):m.lease(c,1,NOW+datetime.timedelta(seconds=601))
    with self.assertRaises(ValueError):m.lease(c,1,NOW-datetime.timedelta(seconds=10))
   for value in (601,600.0):
    bad=copy.deepcopy(state);bad['leases'][0]['max_seconds']=value;p.write_text(json.dumps(bad))
    with patch.object(m,'HERE',here),self.subTest(value=value),self.assertRaises(ValueError):m.lease(c,1,NOW)
 def test_lock_blocks_read_and_boolean_slot_is_not_identity(self):
  with tempfile.TemporaryDirectory() as directory:
   here,p,c,state=fixture(Path(directory));p.write_text(json.dumps(state))
   with patch.object(m,'HERE',here),self.assertRaises(ValueError):m.lease(c,True,NOW)
   p.with_name('resource-leases.lock').write_bytes(b'authored')
   with patch.object(m,'HERE',here),patch.object(m,'read_bound',side_effect=AssertionError('no locked read')):
    with self.assertRaisesRegex(ValueError,'locked'):m.lease(c,1,NOW)
if __name__=='__main__':unittest.main()
