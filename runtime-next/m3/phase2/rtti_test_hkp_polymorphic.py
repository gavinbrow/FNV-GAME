import hashlib,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import rtti_hkp_polymorphic_overlay as m

class Transform(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=(m.BASE/'hkpconstraintviewer.cpp').read_bytes()
  if hashlib.sha256(cls.raw).hexdigest()!=m.BASE_SHA:raise RuntimeError('base hash changed')
 def test_adds_polymorphic_base_preserves_prior(self):
  out=m.transform(self.raw);self.assertIn(b'virtual ~hkBaseObject();',out);self.assertIn(b'hkpConstraintViewer::FUN_00d69730',out)
 def test_missing_anchor_fails(self):
  with self.assertRaisesRegex(ValueError,'anchor'):m.transform(self.raw.replace(b'class hkBaseObject',b'class Changed',1))
 def test_duplicate_anchor_fails(self):
  with self.assertRaisesRegex(ValueError,'anchor'):m.transform(self.raw+b'\r\nclass hkBaseObject\r\n{\r\n};')

if __name__=='__main__':unittest.main(verbosity=2)
