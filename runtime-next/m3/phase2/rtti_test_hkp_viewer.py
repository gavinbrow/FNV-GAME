import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import rtti_hkp_viewer_overlay as o

class RenameSafety(unittest.TestCase):
 def test_exact_rename_and_preservation(self):
  raw=b'class FUN_00d698b0 : public B { FUN_00d698b0(); }; FUN_00d698b0::FUN_00d698b0() {}\n'
  got=o.rename_source(raw);self.assertEqual(got,raw.replace(b'FUN_00d698b0',b'hkpConstraintViewer'))
 def test_collision_rejected(self):
  with self.assertRaisesRegex(ValueError,'already exists'):o.rename_source(b'class hkpConstraintViewer {}; class FUN_00d698b0 : B {};')
 def test_wrong_count_rejected(self):
  with self.assertRaisesRegex(ValueError,'token count'):o.rename_source(b'class FUN_00d698b0 : B {};')
 def test_missing_class_rejected(self):
  with self.assertRaisesRegex(ValueError,'declaration absent'):o.rename_source(b'struct FUN_00d698b0 : B {};')

if __name__=='__main__':unittest.main(verbosity=2)
