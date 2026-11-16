"""Pure runtime-context-copy invariants; no files, original inputs or processes."""
import copy,importlib.util,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[2]/'build/rebuild/uuid-seven-prospective-eh-watchdog-v1.py';s=importlib.util.spec_from_file_location('prospective_runtime_peer_target',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def fixture():
 raw=dict(permissions=dict(root_original_scope_confirmed=True,source_input_review_receipt_sha256=None,coordinator_CPU_lease_id=None),units=[dict(recipe_id='authored-only',roots=[dict(symbol='authored',size=157)])],reference=dict(path='not-opened',sha256='a'*64),provider_selected=False)
 context=dict(child=raw,child_raw_sha256='e'*64,child_canonical_sha256=m.canonical(raw),input_review=dict(sha256='b'*64));grant=dict(owner='/root/rebuild_startup_host',resource='CPU_heavy',slot=1,granted_utc='2026-11-04T00:00:00Z',max_seconds=540,review_sha256='c'*64,input_pins={'authored.json':'d'*64},state='reserved-awaiting-process-identity',pid=None)
 return context,grant
class RuntimeCopyIndependentTests(unittest.TestCase):
 def test_only_two_null_fields_change_and_raw_request_stays_immutable(self):
  context,grant=fixture();before=copy.deepcopy(context['child']);rawcanonical=m.canonical(before);runtime=m.bind_runtime_permissions(context,grant)
  self.assertEqual(context['child'],before);self.assertEqual(context['child_raw_sha256'],'e'*64);self.assertEqual(context['child_canonical_sha256'],rawcanonical);self.assertEqual(context['raw_child_canonical_sha256'],rawcanonical);self.assertNotEqual(context['runtime_child_canonical_sha256'],rawcanonical);self.assertIsNot(runtime,context['child']);self.assertIsNot(runtime['permissions'],context['child']['permissions'])
  self.assertEqual(runtime['permissions']['source_input_review_receipt_sha256'],'b'*64);self.assertEqual(runtime['permissions']['coordinator_CPU_lease_id'],m.grant_identifier(grant));self.assertTrue(m.validate_runtime_copy(before,runtime,'b'*64,m.grant_identifier(grant)))
 def test_mutable_lease_status_and_pid_are_excluded(self):
  context,grant=fixture();first=m.grant_identifier(grant);changed=copy.deepcopy(grant);changed.update(state='running',pid=987654,process_identity={'authored':True});self.assertEqual(m.grant_identifier(changed),first)
 def test_stable_lease_core_changes_are_detected(self):
  _,grant=fixture();first=m.grant_identifier(grant)
  for key in ('owner','resource','slot','granted_utc','max_seconds','review_sha256','input_pins'):
   changed=copy.deepcopy(grant);changed[key]=2 if key=='slot' else 539 if key=='max_seconds' else {'changed':'e'*64} if key=='input_pins' else 'changed'
   with self.subTest(key=key):
    try:identifier=m.grant_identifier(changed)
    except ValueError:continue
    self.assertNotEqual(identifier,first)
 def test_non_context_reference_root_recipe_and_flag_changes_are_rejected(self):
  context,grant=fixture();raw=copy.deepcopy(context['child']);runtime=m.bind_runtime_permissions(context,grant)
  edits=[lambda r:r['reference'].update(sha256='f'*64),lambda r:r['units'][0].update(recipe_id='foreign'),lambda r:r['units'][0]['roots'][0].update(size=158),lambda r:r.update(provider_selected=True),lambda r:r['permissions'].update(root_original_scope_confirmed=False)]
  for edit in edits:
   changed=copy.deepcopy(runtime);edit(changed)
   with self.assertRaises(ValueError):m.validate_runtime_copy(raw,changed,'b'*64,m.grant_identifier(grant))
 def test_disabled_or_prepopulated_raw_permissions_never_get_overwritten(self):
  for key,value in (('root_original_scope_confirmed',False),('source_input_review_receipt_sha256','existing'),('coordinator_CPU_lease_id','existing')):
   context,grant=fixture();context['child']['permissions'][key]=value;before=copy.deepcopy(context)
   with self.subTest(key=key),self.assertRaises(ValueError):m.bind_runtime_permissions(context,grant)
   self.assertEqual(context,before)
def report_fixture():
 context,grant=fixture();units=[]
 flags={k:False for k in ('runtime_eligible','provider_selected','ABI_verified','frame_contract_verified','no_catch_family_approved','full_closure_verified','emission_performed')}
 for i,count in enumerate((1,1,2,3)):
  roots=[dict(original_address='0x%08x'%(0x1000+100*i+j),symbol='authored_'+str(i)+'_'+str(j),size=157) for j in range(count)];units.append(dict(recipe_id='authored-'+str(i),object_sha256='d'*64,roots=roots))
 context['child']['units']=units;context['child_canonical_sha256']=m.canonical(context['child']);m.bind_runtime_permissions(context,grant)
 report=dict(kind='prospective-UUID-seven-parent-EH-v1',request_sha256=context['runtime_child_canonical_sha256'],status='observed-not-admission',units=[dict(recipe_id=u['recipe_id'],object_sha256=u['object_sha256'],roots=[dict(root=copy.deepcopy(r),status='UNSUPPORTED_PHYSICAL_GRAPH',**flags) for r in u['roots']]) for u in units],**flags)
 return context,report,flags
class TerminalReportIndependentTests(unittest.TestCase):
 def test_report_binds_runtime_hash_not_authenticated_raw_hash(self):
  context,report,_=report_fixture();self.assertTrue(m.validate_report(context,report));report['request_sha256']=context['child_canonical_sha256']
  with self.assertRaises(ValueError):m.validate_report(context,report)
 def test_equal_count_foreign_physical_root_rejected(self):
  context,report,_=report_fixture();report['units'][2]['roots'][0]['root']['symbol']='foreign'
  with self.assertRaises(ValueError):m.validate_report(context,report)
 def test_nested_root_or_comparison_promotions_rejected(self):
  for where in ('root','comparison'):
   context,report,flags=report_fixture();row=report['units'][0]['roots'][0]
   if where=='comparison':row['comparison']=dict(status='UNSUPPORTED_OR_MISSING_COMPARISON',**flags);row['comparison']['provider_selected']=True
   else:row['provider_selected']=True
   with self.subTest(where=where),self.assertRaises(ValueError):m.validate_report(context,report)
if __name__=='__main__':unittest.main()
