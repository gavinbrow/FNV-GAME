"""Check the slot5/8 overlay recipe without compiling or editing protected files."""
import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import rtti_bgse_init_load_compare as c

class Remapping(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.meta=json.loads((c.OUT/'manifest.json').read_text());cls.unit=json.loads((c.PROJECT/'fnv_decomp/build/units.json').read_text())['units'][2]
 def test_exactly_five_function_remaps(self):
  initial=copy.deepcopy(self.unit);mapped,_=c.make_unit(self.unit,self.meta)
  self.assertEqual(self.unit,initial);self.assertEqual(sum(a['symbol']!=b['symbol'] for a,b in zip(initial['functions'],mapped['functions'])),5)
 def test_competing_vtable_binding_rejected(self):
  u=copy.deepcopy(self.unit);u['symbols']['??_7FUN_00525ce0@@6B@']='0x01000000'
  with self.assertRaisesRegex(ValueError,'vtable key evidence'):c.make_unit(u,self.meta)
 def test_wrong_mapping_count_rejected(self):
  m=copy.deepcopy(self.meta);m['proposed_function_symbol_changes'].pop()
  with self.assertRaisesRegex(ValueError,'five'):c.make_unit(self.unit,m)

if __name__=='__main__':unittest.main(verbosity=2)
