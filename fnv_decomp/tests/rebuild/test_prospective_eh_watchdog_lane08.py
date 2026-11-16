"""Independent mocked lifecycle/kernel attacks. Never creates a real process/Job."""
import copy,ctypes,importlib.util,os,stat,struct,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
P=Path(__file__).resolve().parents[2]/'build/rebuild/uuid-seven-prospective-eh-watchdog-v1.py';s=importlib.util.spec_from_file_location('prospective_watchdog_peer_target',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Kernel:
 def __init__(self,assign=True,nested=False):self.assignment=assign;self.nested=nested;self.assignments=[];self.closed=[];self.terminated=[];self.limits=None;self.memberships=[];self.censuses=[];self.own_member=True;self.census_pid=123
 def CreateJobObjectW(self,*args):return 0xabc
 def SetInformationJobObject(self,handle,kind,pointer,size):
  value=ctypes.cast(pointer,ctypes.POINTER(m.ExtendedLimits)).contents;self.limits=(value.basic.flags,value.basic.active,value.process_memory);return 1
 def IsProcessInJob(self,process,job,result):
  self.memberships.append(job);result._obj.value=int(self.nested if job is None else self.own_member and self.assignment and bool(self.assignments));return 1
 def QueryInformationJobObject(self,job,kind,pointer,size,returned):
  self.censuses.append(job.value if hasattr(job,'value') else job);raw=struct.pack('<II',1,1)+self.census_pid.to_bytes(ctypes.sizeof(m.SIZE),'little');ctypes.memmove(pointer,raw,len(raw));
  if returned is not None and hasattr(returned,'_obj'):returned._obj.value=len(raw)
  return 1
 def AssignProcessToJobObject(self,job,process):self.assignments.append((job,process.value));return int(self.assignment)
 def TerminateJobObject(self,handle,code):self.terminated.append((handle,code));return 1
 def CloseHandle(self,handle):self.closed.append(handle);return 1
class Child:
 pid=123;_handle=0xdef
 def __init__(self):self.code=None;self.killed=False;self.waited=False
 def poll(self):return self.code
 def kill(self):self.killed=True;self.code=2
 def wait(self,timeout=None):self.waited=True;return self.code
class IndependentWatchdogTests(unittest.TestCase):
 def test_handshake_all_identity_dimensions_are_bound(self):
  context=dict(child_raw_sha256='a'*64,profile_raw_sha256='b'*64,grant_id='c'*64,raw_child_canonical_sha256='d'*64,runtime_child_canonical_sha256='e'*64);child=Child();good=dict(state='held-before-semantic-imports',pid=123,parent_pid=456,nonce='authored-nonce',creation_time=789,child_request_sha256='a'*64,watch_profile_sha256='b'*64,**{k:context[k] for k in ('grant_id','raw_child_canonical_sha256','runtime_child_canonical_sha256')})
  m.check_handshake(good,child,456,'authored-nonce',context,789)
  for key in good:
   bad=copy.deepcopy(good);bad[key]=None
   with self.subTest(key=key),self.assertRaises(ValueError):m.check_handshake(bad,child,456,'authored-nonce',context,789)
  self.assertFalse(child.killed)
 def test_handshake_rejects_numeric_equal_float_identities(self):
  context=dict(child_raw_sha256='a'*64,profile_raw_sha256='b'*64,grant_id='c'*64,raw_child_canonical_sha256='d'*64,runtime_child_canonical_sha256='e'*64);good=dict(state='held-before-semantic-imports',pid=123,parent_pid=456,nonce='nonce',creation_time=789,child_request_sha256='a'*64,watch_profile_sha256='b'*64,**{k:context[k] for k in ('grant_id','raw_child_canonical_sha256','runtime_child_canonical_sha256')})
  for key in ('pid','parent_pid','creation_time'):
   bad=copy.deepcopy(good);bad[key]=float(bad[key])
   with self.subTest(key=key),self.assertRaises(ValueError):m.check_handshake(bad,Child(),456,'nonce',context,789)
 def test_job_has_single_process_kill_on_close_and_memory_limit(self):
  kernel=Kernel();job=m.OwnedJob(SimpleNamespace(k=kernel))
  flags,active,memory=kernel.limits;self.assertEqual(flags&(0x2000|0x8),0x2000|0x8);self.assertEqual(flags&(0x800|0x1000),0);self.assertEqual(active,1);self.assertEqual(memory,m.LIMITS['memory']);job.assign(Child());job.terminate();job.close();self.assertEqual(kernel.assignments,[(0xabc,0xdef)]);self.assertEqual(kernel.closed,[0xabc])
 def test_assignment_failure_never_marks_contained(self):
  kernel=Kernel(assign=False);job=m.OwnedJob(SimpleNamespace(k=kernel))
  try:
   with self.assertRaises(ValueError):job.assign(Child())
   self.assertFalse(job.assigned);job.terminate();self.assertEqual(kernel.terminated,[])
  finally:job.close()
 def test_preexisting_job_requires_new_owned_membership_and_single_child(self):
  kernel=Kernel(nested=True);job=m.OwnedJob(SimpleNamespace(k=kernel))
  try:
   job.assign(Child());self.assertTrue(job.assigned);self.assertIn(None,kernel.memberships);self.assertTrue(any(value not in (None,0) for value in kernel.memberships));self.assertEqual(kernel.censuses,[0xabc])
  finally:job.close()
 def test_own_membership_or_foreign_census_fails_without_foreign_process_control(self):
  for own_member,census_pid in ((False,123),(True,999)):
   kernel=Kernel(nested=True);kernel.own_member=own_member;kernel.census_pid=census_pid;job=m.OwnedJob(SimpleNamespace(k=kernel))
   try:
    with self.subTest(own_member=own_member,census_pid=census_pid),self.assertRaises(ValueError):job.assign(Child())
    job.terminate();self.assertTrue(all(handle==0xabc for handle,_ in kernel.terminated));self.assertEqual(kernel.assignments,[(0xabc,0xdef)])
   finally:job.close()
 def test_stop_before_assignment_uses_only_owned_Popen(self):
  child=Child();m.stop_owned(child,None);self.assertTrue(child.killed);self.assertTrue(child.waited)
 def test_root_reparse_point_rejected_before_census(self):
  with tempfile.TemporaryDirectory() as directory:
   control=Path(directory)/'control';output=Path(directory)/'output';control.mkdir();output.mkdir();original=Path.lstat
   def observed(path,*args,**kwargs):
    if path in (control,output):return SimpleNamespace(st_mode=stat.S_IFDIR,st_file_attributes=0x400)
    return original(path,*args,**kwargs)
   with patch.object(Path,'lstat',observed),patch.object(Path,'iterdir',side_effect=AssertionError('must not enumerate foreign root')):
    with self.assertRaisesRegex(ValueError,'reparse'):m.owned_size(control,output)
 def test_unexpected_control_file_is_not_an_allowed_member(self):
  with tempfile.TemporaryDirectory() as directory:
   control=Path(directory)/'control';output=Path(directory)/'output';control.mkdir();output.mkdir();(control/'unrelated-user-file.txt').write_bytes(b'authored')
   with self.assertRaises(ValueError):m.owned_size(control,output)
 def test_unknown_collector_writer_identity_never_quarantines_foreign_content(self):
  with tempfile.TemporaryDirectory() as directory:
   control=Path(directory)/'control';output=Path(directory)/'output';control.mkdir();output.mkdir();report=output/'observation.json';raw=b'{"status":"authored-unqualified"}';report.write_bytes(raw)
   try:m.quarantine(dict(control=control,output=output),Child(),456,'nonce')
   except ValueError:pass
   self.assertEqual(report.read_bytes(),raw);self.assertFalse((output/'observation.json.failed').exists())
 def test_late_terminal_validation_failure_quarantines_only_own_receipt(self):
  with tempfile.TemporaryDirectory() as directory:
   control=Path(directory)/'control';output=Path(directory)/'output';control.mkdir();output.mkdir();context=dict(control=control,output=output,profile_raw_sha256='a'*64);calls=[0]
   def verify():
    calls[0]+=1
    if calls[0]==2:raise ValueError('authored late lease drift')
   self.assertFalse(m.publish_terminal(context,dict(status='completed-not-admission'),verify,None,None,'nonce'));self.assertEqual(calls[0],2);self.assertFalse((control/'receipt.json').exists());self.assertTrue((control/'receipt.json.failed').exists());self.assertTrue((control/'watch-failure.json').exists())
 def test_foreign_terminal_replacement_is_retained_but_never_accepted(self):
  with tempfile.TemporaryDirectory() as directory:
   control=Path(directory)/'control';output=Path(directory)/'output';control.mkdir();output.mkdir();foreign=Path(directory)/'foreign';foreign.write_bytes(b'authored foreign content');context=dict(control=control,output=output,profile_raw_sha256='a'*64);calls=[0]
   def verify():
    calls[0]+=1
    if calls[0]==2:os.replace(foreign,control/'receipt.json')
   self.assertFalse(m.publish_terminal(context,dict(status='completed-not-admission'),verify,None,None,'nonce'));self.assertEqual((control/'receipt.json').read_bytes(),b'authored foreign content');self.assertTrue((control/'watch-failure.json').exists());self.assertFalse((control/'receipt.json.failed').exists())
 def test_source_only_profile_refuses_before_kernel_or_Popen(self):
  units=[dict(recipe_index=i,roots=[dict(original_address=a,size=157) for a in sorted(addresses)]) for i,addresses in m.EXPECTED.items()]
  child=dict(kind='prospective-UUID-seven-parent-EH-v1',authority_kind='qualified-caller-prospective-only',measured_V13_or_593_authority=False,units=units,DATA01204364_materialization_approved=False,permissions=dict(root_original_scope_confirmed=False),reference=None,reference_image_gate=None,output_directory='build/rebuild/prospective-uuid-seven-original-authored')
  profile=dict(kind='finite-UUID-seven-watch-profile-v1',limits=m.LIMITS,child_request={},control_directory='build/rebuild/prospective-uuid-seven-control-authored',output_directory=child['output_directory'],execution_permitted=False)
  answers=[(profile,m.ROOT/'build/rebuild/authored-profile.json',b'profile'),(child,m.ROOT/'build/rebuild/authored-child.json',b'child')]
  with patch.object(m,'pinned_json',side_effect=answers),patch.object(m,'check_roots',return_value=None),patch.object(m,'read_bound',side_effect=AssertionError('no protected hash')),patch.object(m,'Windows',side_effect=AssertionError('no kernel')),patch.object(m.subprocess,'Popen',side_effect=AssertionError('no child')):
   with self.assertRaisesRegex(ValueError,'SOURCE_ONLY'):m.run({},None,None,1)
if __name__=='__main__':unittest.main()
