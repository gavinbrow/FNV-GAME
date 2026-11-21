"""No-compiler tests for hkp post-simulation recipe remapping."""
import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import rtti_hkp_postsim_compare as c

class UnitMap(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.meta=json.loads((c.OUT/'manifest.json').read_text());cls.unit=json.loads((c.PROJECT/'fnv_decomp/build/units.json').read_text())['units'][2501]
 def test_method_and_helper_alias_preserve_input(self):
  before=copy.deepcopy(self.unit);mapped,norm=c.make_unit(self.unit,self.meta)
  self.assertEqual(self.unit,before);self.assertEqual(len(mapped['functions']),16)
  alias=self.meta['proposed_helper_alias'];self.assertEqual(mapped['symbols'][alias['after']],alias['address']);self.assertEqual(norm[alias['after']],alias['before'])
  self.assertEqual(sum(f['symbol']==self.meta['proposed_method']['after'] for f in mapped['functions']),1)
 def test_old_helper_address_drift_rejected(self):
  unit=copy.deepcopy(self.unit);unit['symbols'][self.meta['proposed_helper_alias']['before']]='0x01000000'
  with self.assertRaisesRegex(ValueError,'helper alias changed'):c.make_unit(unit,self.meta)
 def test_new_helper_conflict_rejected(self):
  unit=copy.deepcopy(self.unit);unit['symbols'][self.meta['proposed_helper_alias']['after']]='0x01000000'
  with self.assertRaisesRegex(ValueError,'collision'):c.make_unit(unit,self.meta)
 def test_method_recipe_drift_rejected(self):
  m=copy.deepcopy(self.meta);m['proposed_method']['size']+=1
  with self.assertRaisesRegex(ValueError,'method changed'):c.make_unit(self.unit,m)

if __name__=='__main__':unittest.main(verbosity=2)
