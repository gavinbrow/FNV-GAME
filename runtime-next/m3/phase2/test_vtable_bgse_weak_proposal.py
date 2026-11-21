import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import vtable_bgse_weak_proposal as p
class T(unittest.TestCase):
 def setUp(self):
  self.proof={k:True for k in ('snapshot_current','weak_metadata_valid','fallback_unique','source_owner_unique','body_and_reloc_equal','strict_reference_match','recipe_primary_absent','placed_global_absent','v7_name_absent','icf_primary_absent','name_overlay_absent','field_overlay_absent','relevant_provider_cohort_checked')};self.proof.update(characteristic=2,fallback=p.FALLBACK,owner_symbol='?Destroy@FUN_00525cb0_shell@@QAEPAU1@I@Z',owner_size=44,owner_address=0x525cb0)
 def test_accept(self):self.assertEqual(p.propose(p.PRIMARY,0x102cbcc,None,self.proof),('private-bgse-fallback',0x525cb0))
 def test_normal_priority(self):self.assertEqual(p.propose(p.PRIMARY,0x102cbcc,('normal',5),{}),('normal',5))
 def test_each_guard(self):
  for k,v in list(self.proof.items()):
   q=dict(self.proof);q.pop(k)
   with self.subTest(k=k),self.assertRaises(ValueError):p.propose(p.PRIMARY,0x102cbcc,None,q)
 def test_wrong_site(self):
  with self.assertRaises(ValueError):p.propose(p.PRIMARY,0x102cbd0,None,self.proof)
if __name__=='__main__':unittest.main()
