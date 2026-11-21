"""Unit-level safety checks for the bounded BGSE destructor merge."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import rtti_bgse_merge as m

class MergeTests(unittest.TestCase):
 def test_exact_block_replacement_preserves_other_text(self):
  raw='before\n'+m.OLD+'\nafter\n';self.assertEqual(m.merge_destructor(raw),'before\n'+m.NEW+'\nafter\n')
 def test_duplicate_surrogate_rejected(self):
  with self.assertRaisesRegex(ValueError,'exactly once'):m.merge_destructor(m.OLD+'\n'+m.OLD)
 def test_existing_native_destructor_rejected(self):
  with self.assertRaisesRegex(ValueError,'already exists'):m.merge_destructor(m.OLD+'\nBGSEncounterZone::~BGSEncounterZone() {}')
 def test_missing_block_rejected(self):
  with self.assertRaisesRegex(ValueError,'exactly once'):m.merge_destructor('class BGSEncounterZone {};')
 def test_real_override_overlay_merges_once(self):
  data=(m.PRIOR/'bgsencounterzone.cpp').read_text(encoding='utf8');out=m.merge_destructor(data)
  self.assertEqual(out.count('BGSEncounterZone::~BGSEncounterZone()'),1);self.assertEqual(out.count('FUN_00525ce0::~FUN_00525ce0()'),0)

if __name__=='__main__':unittest.main(verbosity=2)
