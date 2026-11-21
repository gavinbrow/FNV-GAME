"""Compiler-free safety checks for the bounded post-simulation override."""
import hashlib,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import rtti_hkp_postsim_overlay as m

class PostSim(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=(m.BASE/'hkpconstraintviewer.cpp').read_bytes()
  if hashlib.sha256(cls.raw).hexdigest()!=m.BASE_SHA:raise RuntimeError('input changed')
 def test_method_moved_once_and_prior_destructor_retained(self):
  x=m.transform(self.raw);self.assertEqual(x.count(b'void hkpConstraintViewer::FUN_00d69730(World* world)'),1)
  self.assertNotIn(b'void ConstraintViewer::FUN_00d69730(World* world)',x)
  self.assertEqual(x.count(b'hkpConstraintViewer::~hkpConstraintViewer()'),1)
 def test_duplicate_target_rejected(self):
  with self.assertRaisesRegex(ValueError,'already defined'):m.transform(self.raw+b'\r\nvoid hkpConstraintViewer::FUN_00d69730(World* w) {}')
 def test_missing_method_rejected(self):
  with self.assertRaisesRegex(ValueError,'method definition'):m.transform(self.raw.replace(b'void ConstraintViewer::FUN_00d69730(World* world)',b'',1))
 def test_changed_field_anchor_rejected(self):
  with self.assertRaisesRegex(ValueError,'operation type'):m.transform(self.raw.replace(b'class hkProcess',b'class hkProcessChanged',1))

if __name__=='__main__':unittest.main(verbosity=2)
