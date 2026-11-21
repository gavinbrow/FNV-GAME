"""Check BGSE symbol remapping never silently merges conflicting addresses."""
import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import rtti_bgse_compare as c

class MappingTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.meta=json.loads((c.OUT/'manifest.json').read_text());cls.unit=json.loads((c.PROJECT/'fnv_decomp/build/units.json').read_text())['units'][2]
 def test_exact_remaps_preserve_input(self):
  unit=copy.deepcopy(self.unit);before=copy.deepcopy(unit);mapped,norm=c.make_unit(unit,self.meta)
  self.assertEqual(unit,before);self.assertEqual(len(mapped['functions']),24)
  self.assertEqual(mapped['symbols']['??1TESForm@@UAE@XZ'],'0x00483630')
  self.assertNotIn('??1TESForm@@UAE@XZ',norm)
 def test_vtable_coaddress_mismatch_rejected(self):
  unit=copy.deepcopy(self.unit);unit['symbols']['??_7FUN_00525ce0@@6B@']='0x01000000'
  with self.assertRaisesRegex(ValueError,'vtable key evidence'):c.make_unit(unit,self.meta)
 def test_alias_conflict_rejected(self):
  unit=copy.deepcopy(self.unit);unit['symbols']['??1TESForm@@UAE@XZ']='0x01000000'
  with self.assertRaisesRegex(ValueError,'alias collision'):c.make_unit(unit,self.meta)
 def test_vtable_normalization_is_scoped_to_destructor(self):
  native='??_7BGSEncounterZone@@6B@';self.assertNotIn(native,c.normalization_for_function('??0BGSEncounterZone@@QAE@XZ',{}))
  self.assertEqual(c.normalization_for_function('??1FUN_00525ce0@@UAE@XZ',{})[native],'??_7FUN_00525ce0@@6B@')
  self.assertEqual(c.normalization_for_function('??1FUN_00525ce0@@UAE@XZ',{})['??1TESForm@@UAE@XZ'],'??1Base5a@@UAE@XZ')

if __name__=='__main__':unittest.main(verbosity=2)
