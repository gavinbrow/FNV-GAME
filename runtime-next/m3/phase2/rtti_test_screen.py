"""Pure conservative RTTI screening checks; no reference/game reads."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));from rtti_screen_candidates import screen_reasons

class Screening(unittest.TestCase):
 def setUp(self):
  self.args=dict(kind='V',new='Original',old='FUN_01234567',src='src/a.cpp',occurrences={'FUN_01234567':{'src/a.cpp'}},recipe_count=1,data=b'class FUN_01234567 : public Base {};',includes=['<windows.h>'],source_exists=True)
 def test_narrow_candidate(self):self.assertEqual(screen_reasons(**self.args),[])
 def test_name_collision_and_ambiguous_identity_deferred(self):
  self.args['occurrences']={'Original':{'src/b.cpp'},'FUN_01234567':{'src/a.cpp','src/c.cpp'}}
  r=screen_reasons(**self.args);self.assertIn('native_name_mentioned_in_source_or_include',r);self.assertIn('synthetic_name_not_confined_to_unit_source',r)
 def test_struct_mismatch_and_local_include_deferred(self):
  self.args.update(data=b'struct FUN_01234567 : Base {};',includes=['"local.h"'])
  r=screen_reasons(**self.args);self.assertIn('class_struct_discriminator_differs',r);self.assertIn('local_include_closure_requires_review',r)
 def test_duplicate_recipe_and_missing_source_deferred(self):
  self.args.update(recipe_count=2,source_exists=False,data=b'')
  r=screen_reasons(**self.args);self.assertIn('source_recipe_count_not_one',r);self.assertIn('source_missing',r)

if __name__=='__main__':unittest.main(verbosity=2)
