"""Offline, compiler-free checks of the isolated hierarchy transformation."""
import hashlib,re,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import rtti_hkp_hierarchy_overlay as mod

class TransformTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=(mod.PROJECT/'fnv_decomp'/mod.base.SOURCE_REL).read_bytes()
  if mod.base.sha(cls.raw)!=mod.base.SOURCE_SHA:raise RuntimeError('reviewed source changed')
 def test_expected_seven_named_classes_and_access(self):
  out=mod.transform(self.raw)
  for name in (b'class hkBaseObject', b'class hkReferencedObject : public hkBaseObject',b'class hkpWorldViewerBase : public hkReferencedObject, public hkProcess, protected hkpPhysicsContextWorldListener', b'class hkpConstraintViewer : public hkpWorldViewerBase, protected hkpWorldPostSimulationListener'):
   self.assertIn(name,out)
  for old,_,_ in mod.MAP:self.assertIsNone(re.search(rb'\b'+old.encode()+rb'\b',out))
 def test_rejects_ambiguous_target_name(self):
  with self.assertRaisesRegex(ValueError,'name already present'):
   mod.transform(self.raw+b'\r\nclass hkProcess;\r\n')
 def test_rejects_missing_anchor(self):
  with self.assertRaises(ValueError):mod.transform(self.raw.replace(b'class D698B0BaseA',b'struct D698B0BaseA',1))
 def test_rejects_source_reference_drift(self):
  with self.assertRaisesRegex(ValueError,'token count'):mod.transform(self.raw+b'\r\nD698B0BaseA *unknown;\r\n')

if __name__=='__main__':unittest.main(verbosity=2)
