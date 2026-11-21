import sys,json,unittest,importlib.util
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;sys.path.insert(0,str(M));import gen_m3 as G
D=M/'out/phase2-cost245-proposal';sp=importlib.util.spec_from_file_location('cost_helper_staged',D/'candidate-cost245_records.py');C=importlib.util.module_from_spec(sp);sys.modules[sp.name]=C;sp.loader.exec_module(C)
class CostFields(unittest.TestCase):
 def setUp(self):self.q=next(x for x in json.loads((D/'selection.json').read_text())['entries'] if x['tc']=='Y')
 def test_original_58_allowed(self):self.assertEqual(len(C.build_entry(self.q,G)['fields']),58)
 def test_reject_extra_original_field_in_bool_or_unaligned_int(self):
  old=G.ORIG_SET
  try:
   for off in (0,1,5):
    G.ORIG_SET=set(old)|{C.HEAD+off}
    with self.subTest(offset=off),self.assertRaisesRegex(ValueError,'unsupported Cost245 field'):C.build_entry(self.q,G)
  finally:G.ORIG_SET=old
if __name__=='__main__':unittest.main()

