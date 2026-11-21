import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import rtti_skyobject_overlay as s
import rtti_bodypart_overlay as b
class OverlayTests(unittest.TestCase):
 def test_sky_exact_transform(self):
  source=s.S.read_bytes(); result=s.transform(source)
  self.assertEqual(result,(s.O/'skyobject.cpp').read_bytes());self.assertIn(b'SkyObject::~SkyObject()',result)
 def test_sky_rejects_changed_body(self):
  with self.assertRaises(ValueError):s.transform(s.S.read_bytes().replace(b'm_mem.Reset(0);',b'm_mem.Reset(1);'))
 def test_bodypart_evidence_scoped(self):
  self.assertIn(b'QueueResourceLoad',b.class_body(b.EVIDENCE.read_bytes()))
  with self.assertRaises(ValueError):b.class_body(b'class BGSBodyPart; class Other {};')
 def test_transaction_rejects_unreviewed_payload(self):
  old=(b.TRANSITION/'2.original').read_bytes();new=(b.TRANSITION/'2.generated').read_bytes()
  b.validate_units_transition(old,new,new)
  with self.assertRaises(ValueError):b.validate_units_transition(old,new,new+b' ')
if __name__=='__main__':unittest.main()
