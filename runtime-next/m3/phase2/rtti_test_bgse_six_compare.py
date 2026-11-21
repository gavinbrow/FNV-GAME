import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import rtti_bgse_six_compare as c
class SixMap(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.meta=json.loads((c.OUT/'manifest.json').read_text());cls.unit=json.loads((c.PROJECT/'fnv_decomp/build/units.json').read_text())['units'][2]
 def test_nine_exact_remaps_without_input_mutation(self):
  before=copy.deepcopy(self.unit);mapped,_=c.make_unit(self.unit,self.meta)
  self.assertEqual(before,self.unit);self.assertEqual(len(mapped['functions']),24);self.assertEqual(sum(a['symbol']!=b['symbol'] for a,b in zip(before['functions'],mapped['functions'])),9)
 def test_missing_proposal_fails_closed(self):
  x=copy.deepcopy(self.meta);x['proposed_function_symbol_changes'].pop()
  with self.assertRaisesRegex(ValueError,'nine'):c.make_unit(self.unit,x)
 def test_conflicting_destructor_alias_rejected(self):
  x=copy.deepcopy(self.unit);x['symbols']['??1TESForm@@UAE@XZ']='0x01000000'
  with self.assertRaisesRegex(ValueError,'alias collision'):c.make_unit(x,self.meta)

if __name__=='__main__':unittest.main(verbosity=2)
