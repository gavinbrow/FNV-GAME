"""Compiler-free anchor and collision checks for the private destructor prototype."""
import hashlib,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import rtti_hkp_destructor_overlay as h

class DestructorOverlay(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=(h.BASE/'hkpconstraintviewer.cpp').read_bytes()
  if hashlib.sha256(cls.raw).hexdigest()!=h.BASE_SHA:raise RuntimeError('baseline overlay changed')
 def test_destructor_hypotheses_are_bounded(self):
  out=h.transform(self.raw)
  self.assertEqual(out.count(b'hkpConstraintViewer::~hkpConstraintViewer()'),1)
  self.assertEqual(out.count(b'FUN_00d69920_cls::~FUN_00d69920_cls()'),1)
  self.assertIn(b'virtual ~hkReferencedObject();',out);self.assertIn(b'virtual ~hkpConstraintViewer() throw();',out)
 def test_missing_insertion_anchor_rejected(self):
  with self.assertRaisesRegex(ValueError,'insertion'):h.transform(self.raw.replace(b'}  // namespace fnv_00d69af0',b'}',1))
 def test_duplicate_class_anchor_rejected(self):
  block=b'class hkProcess\r\n{\r\n  public:\r\n    virtual void unk00();'
  with self.assertRaisesRegex(ValueError,'hkProcess'):h.transform(self.raw+b'\r\n'+block)
 def test_missing_required_base_anchor_rejected(self):
  with self.assertRaisesRegex(ValueError,'hkReferencedObject'):h.transform(self.raw.replace(b'class hkReferencedObject : public hkBaseObject',b'class hkReferencedObject',1))

if __name__=='__main__':unittest.main(verbosity=2)
