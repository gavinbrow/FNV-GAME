"""Pure transform tests for BGSE source-backed slot 5/8 hypothesis."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import rtti_bgse_init_load_overlay as m

class OverrideTransform(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.src=(m.PRIOR/'bgsencounterzone.cpp').read_text();cls.hdr=(m.PRIOR/'bgsencounterzone_decls.h').read_text()
 def test_targeted_methods_and_direct_ctor_call(self):
  s,h=m.transform(self.src,self.hdr)
  self.assertIn('BGSEncounterZone::InitializeComponent();',s);self.assertIn('bool BGSEncounterZone::LoadForm(TESFile* file)',s)
  self.assertIn('virtual void InitializeComponent();',h);self.assertIn('virtual bool LoadForm(TESFile* file);',h)
  self.assertEqual(s.count('BGSEncounterZone::~BGSEncounterZone()'),1)
 def test_existing_override_rejected(self):
  with self.assertRaisesRegex(ValueError,'already exists'):m.transform(self.src+'\nvoid BGSEncounterZone::InitializeComponent() {}',self.hdr)
 def test_duplicate_header_anchor_rejected(self):
  with self.assertRaisesRegex(ValueError,'exactly one'):m.transform(self.src,self.hdr+'\n    void ResetFormData();\n')
 def test_missing_call_anchor_rejected(self):
  with self.assertRaisesRegex(ValueError,'constructor call'):m.transform(self.src.replace('    ResetFormData();\n',''),self.hdr)

if __name__=='__main__':unittest.main(verbosity=2)
