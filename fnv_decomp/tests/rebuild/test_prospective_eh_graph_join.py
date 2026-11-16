import copy,importlib.util,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[2]
s=importlib.util.spec_from_file_location('join',ROOT/'tools/rebuild/prospective_eh_graph_join.py');j=importlib.util.module_from_spec(s);s.loader.exec_module(j)
def fixture():
 a=next(iter(j.ROOTS));recipe,obj=j.ROOTS[a]
 root=dict(original_address=a,recipe_index=recipe,recipe_id='authored-recipe',object_sha256=obj,symbol_index=5,section=1,value=0,size=157,symbol='parent')
 native={k:root[k] for k in ('original_address','symbol','symbol_index','section','value','size')}
 contract=dict(recipe_id=root['recipe_id'],roots=[native],provenance=dict(object_sha256=obj));cid=j.digest(contract)
 sections=[dict(index=1,extent=157),dict(index=2,extent=38),dict(index=3,extent=44),dict(index=4,extent=27)]
 symbols=[dict(index=5,name='parent',section=1,value=0,type=32,storage=2,aux_count=0),dict(index=6,name='child',section=2,value=0,type=32,storage=3,aux_count=0),dict(index=7,name='foreign',section=4,value=0,type=32,storage=3,aux_count=0)]
 edges=[dict(kind='ASSOCIATION_CHILD',source=1,target=2),dict(kind='ASSOCIATION_CHILD',source=99,target=3),dict(kind='PHYSICAL_SECTION_RELOCATION',source=dict(section=2,offset=4,kind=20),target=7)]
 scope=dict(object_sha256=obj,contract_identity_sha256=cid,edges_sha256=j.digest(edges));sub=dict(scope=scope,scope_sha256=j.digest(scope),disposition_sha256=j.digest(dict(sections=sections,symbols=symbols)))
 cert=dict(recipe_id=root['recipe_id'],provenance=dict(object_sha256=obj),roots=[{k:root[k] for k in ('original_address','symbol','symbol_index','section','value','size')}],contract_identity_sha256=cid,omission_subcertificate=sub,sections=sections,symbols=symbols,edges=edges,safeseh=[dict(symbol_index=7,target_section=4,target_value=0)],blockers=[dict(code='UNKNOWN')])
 record=dict(recipe_id=root['recipe_id'],kind='fresh-root-observation-from-qualified-contract',event='SINGLE_ROOT_OBSERVATION',native_parse_performed=True,fresh_certificate_created=True,recipe_index=recipe,native_object_sha256=obj,requested_roots=[root],certificate=cert,certificate_sha256=j.digest(cert),contract_identity_sha256=cid,contract=contract)
 return a,record
def seal(r):
 c=r['certificate'];c['omission_subcertificate']['scope']['edges_sha256']=j.digest(c['edges']);c['omission_subcertificate']['scope_sha256']=j.digest(c['omission_subcertificate']['scope']);c['omission_subcertificate']['disposition_sha256']=j.digest(dict(sections=c['sections'],symbols=c['symbols']));r['certificate_sha256']=j.digest(c)
def run(a,r):return j.join_saved_singleton(r,a,expected_record_sha256=j.digest(r),expected_certificate_sha256=r['certificate_sha256'])
class Tests(unittest.TestCase):
 def setUp(self):self.a,self.r=fixture()
 def test_pure_candidates_keep_all_approvals_false(self):
  before=copy.deepcopy(self.r);out=run(self.a,self.r);self.assertEqual(before,self.r);self.assertEqual([x['index'] for x in out['direct_association_candidates']],[2]);self.assertEqual(len(out['physical_relocation_candidates']),1);self.assertEqual(out['discharged'],[]);self.assertIs(out['recipe_id_and_physical_descriptor_authenticity_require_external_review'],True)
  for k in j.FALSE:self.assertIs(out[k],False)
 def test_other_root_same_object_rejected(self):
  with self.assertRaises(j.JoinError):run('0x00c50610',self.r)
 def test_stale_record_certificate_and_inventory_rejected(self):
  with self.assertRaises(j.JoinError):j.join_saved_singleton(self.r,self.a,expected_record_sha256='0'*64,expected_certificate_sha256=self.r['certificate_sha256'])
  self.r['certificate']['sections'][0]['extent']=156;self.r['certificate_sha256']=j.digest(self.r['certificate'])
  with self.assertRaises(j.JoinError):run(self.a,self.r)
 def test_bool_indices_and_mismatched_safeseh_rejected(self):
  self.r['requested_roots'][0]['symbol_index']=True;seal(self.r)
  with self.assertRaises(j.JoinError):run(self.a,self.r)
  self.a,self.r=fixture();self.r['certificate']['safeseh'][0]['target_value']=1;seal(self.r)
  with self.assertRaises(j.JoinError):run(self.a,self.r)
 def test_union_or_foreign_object_rejected(self):
  self.r['event']='RECIPE_ROOT_UNION_OBSERVATION'
  with self.assertRaises(j.JoinError):run(self.a,self.r)
  self.a,self.r=fixture();self.r['native_object_sha256']='0'*64
  with self.assertRaises(j.JoinError):run(self.a,self.r)
 def test_contract_scope_and_parent_extent_are_strict(self):
  self.r['certificate']['sections'][0]['extent']=157.0;seal(self.r)
  with self.assertRaises(j.JoinError):run(self.a,self.r)
  self.a,self.r=fixture();self.r['contract']['roots']=[];cid=j.digest(self.r['contract']);self.r['contract_identity_sha256']=cid;self.r['certificate']['contract_identity_sha256']=cid;self.r['certificate']['omission_subcertificate']['scope']['contract_identity_sha256']=cid;seal(self.r)
  with self.assertRaises(j.JoinError):run(self.a,self.r)
 def test_physical_bool_values_do_not_alias_integers(self):
  for case in ('symbol','association','relocation','safeseh'):
   a,r=fixture();c=r['certificate']
   if case=='symbol':c['symbols'][0]['value']=False
   elif case=='association':c['edges'][0]['source']=True
   elif case=='relocation':c['edges'][2]['source']['section']=True
   else:c['safeseh'][0]['target_value']=False
   seal(r)
   with self.subTest(case=case),self.assertRaises(j.JoinError):run(a,r)
if __name__=='__main__':unittest.main()
