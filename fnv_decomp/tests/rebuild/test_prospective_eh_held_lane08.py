"""Pure held-token/timeout mock cases; no process, kernel or semantic producer."""
import copy,importlib.util,json,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
P=Path(__file__).resolve().parents[2]/'build/rebuild/uuid-seven-prospective-eh-held-child-v1.py';s=importlib.util.spec_from_file_location('prospective_held_peer_target',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class HeldBootstrapIndependentTests(unittest.TestCase):
 def test_proceed_binds_every_identity_and_job_confirmation(self):
  context=dict(profile_raw_sha256='a'*64,child_raw_sha256='b'*64,grant_id='c'*64,raw_child_canonical_sha256='d'*64,runtime_child_canonical_sha256='e'*64);good=dict(nonce='authored-nonce',pid=123,creation_time=456,job_assigned=True,watch_profile_sha256='a'*64,child_request_sha256='b'*64,**{k:context[k] for k in ('grant_id','raw_child_canonical_sha256','runtime_child_canonical_sha256')})
  m.check_proceed(good,123,456,'authored-nonce',context)
  for key in good:
   bad=copy.deepcopy(good);bad[key]=None
   with self.subTest(key=key),self.assertRaises(ValueError):m.check_proceed(bad,123,456,'authored-nonce',context)
 def test_proceed_rejects_numeric_equal_float_identities(self):
  context=dict(profile_raw_sha256='a'*64,child_raw_sha256='b'*64,grant_id='c'*64,raw_child_canonical_sha256='d'*64,runtime_child_canonical_sha256='e'*64);good=dict(nonce='nonce',pid=123,creation_time=456,job_assigned=True,watch_profile_sha256='a'*64,child_request_sha256='b'*64,**{k:context[k] for k in ('grant_id','raw_child_canonical_sha256','runtime_child_canonical_sha256')})
  for key in ('pid','creation_time'):
   bad=copy.deepcopy(good);bad[key]=float(bad[key])
   with self.subTest(key=key),self.assertRaises(ValueError):m.check_proceed(bad,123,456,'nonce',context)
 def test_held_timeout_expires_without_producers_or_writes(self):
  with tempfile.TemporaryDirectory() as directory:
   control=Path(directory);ticks=iter([0,0,11]);leases=[];watch=SimpleNamespace(lease=lambda *args:(leases.append(args) or {'authored':True}))
   with patch.object(m.os,'getppid',return_value=42):
    with self.assertRaisesRegex(ValueError,'expired'):m.wait_held(dict(control=control,stable_grant={'authored':True}),123,456,42,'nonce',1,watch,clock=lambda:next(ticks),sleep=lambda _:None)
   self.assertEqual(list(control.iterdir()),[]);self.assertEqual(len(leases),1)
 def test_expired_lease_blocks_even_a_present_token_before_read(self):
  with tempfile.TemporaryDirectory() as directory:
   control=Path(directory);(control/'proceed.json').write_text('{}');ticks=iter([0,0])
   def expired(*args):raise ValueError('authored expired lease')
   with patch.object(m.os,'getppid',return_value=42),patch.object(m,'bounded',side_effect=AssertionError('must not read token')):
    with self.assertRaisesRegex(ValueError,'expired lease'):m.wait_held(dict(control=control,stable_grant={'authored':True}),123,456,42,'nonce',1,SimpleNamespace(lease=expired),clock=lambda:next(ticks),sleep=lambda _:None)
 def test_parent_identity_change_precedes_control_access(self):
  with tempfile.TemporaryDirectory() as directory:
   ticks=iter([0,0]);watch=SimpleNamespace(lease=lambda *_:self.fail('must stop before lease/control'))
   with patch.object(m.os,'getppid',return_value=99),patch.object(m,'bounded',side_effect=AssertionError('must not read token')):
    with self.assertRaisesRegex(ValueError,'parent identity'):m.wait_held(dict(control=Path(directory),stable_grant={'authored':True}),123,456,42,'nonce',1,watch,clock=lambda:next(ticks),sleep=lambda _:None)
 def test_absolute_bootstrap_deadline_is_not_reset_after_authentication(self):
  with tempfile.TemporaryDirectory() as directory:
   watch=SimpleNamespace(lease=lambda *_:self.fail('expired bootstrap cannot query lease or proceed'))
   with patch.object(m.os,'getppid',return_value=42),patch.object(m,'bounded',side_effect=AssertionError('no expired token read')):
    with self.assertRaisesRegex(ValueError,'expired'):m.wait_held(dict(control=Path(directory),stable_grant={'authored':True}),123,456,42,'nonce',1,watch,clock=lambda:11,sleep=lambda _:None,deadline=10)
 def test_foreign_proceed_nonce_never_releases_hold(self):
  with tempfile.TemporaryDirectory() as directory:
   control=Path(directory);(control/'proceed.json').write_text(json.dumps(dict(nonce='foreign',pid=123,creation_time=456,job_assigned=True,watch_profile_sha256='a'*64,child_request_sha256='b'*64)));ticks=iter([0,0]);context=dict(control=control,profile_raw_sha256='a'*64,child_raw_sha256='b'*64,stable_grant={'authored':True},grant_id='c'*64,raw_child_canonical_sha256='d'*64,runtime_child_canonical_sha256='e'*64)
   with patch.object(m.os,'getppid',return_value=42):
    with self.assertRaisesRegex(ValueError,'proceed token'):m.wait_held(context,123,456,42,'nonce',1,SimpleNamespace(lease=lambda *_:{'authored':True}),clock=lambda:next(ticks),sleep=lambda _:None)
if __name__=='__main__':unittest.main()
