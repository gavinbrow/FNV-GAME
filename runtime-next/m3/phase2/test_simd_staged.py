import sys,json,unittest,importlib.util
from pathlib import Path
M=Path(__file__).resolve().parent.parent;D=M/'out/phase2-align16';sys.path.insert(0,str(M));sp=importlib.util.spec_from_file_location('simd_gen_test',D/'candidate-gen_m3.py');G=importlib.util.module_from_spec(sp);sys.modules[sp.name]=G;sp.loader.exec_module(G)
class Simd(unittest.TestCase):
 def setUp(self):self.q=next(x for x in json.loads((D/'selection.json').read_text())['entries'] if x['tc']=='V')
 def test_native_render_and_type(self):
  e=G.build_entries([self.q]);self.assertEqual((e[0]['sym'],e[0]['align']),(self.q['class_symbol'],16));s=G.cpp(e);self.assertIn('__declspec(align(16)) __m128',s);self.assertIn('namespace fnv_00cd9d10 { extern __declspec(allocate(".rdata")) __m128 DAT_',s)
 def test_reject_bad_metadata(self):
  for k,v in (('align',8),('size',20),('class_symbol','bad'),('class_namespace','bad')):
   with self.subTest(k=k),self.assertRaises(ValueError):G.build_entries([dict(self.q,**{k:v})])
 def test_reject_nonfinite(self):
  old=G.refbytes;G.refbytes=lambda a,n:b'\0\0\xc0\x7f'+b'\0'*12
  try:
   with self.assertRaisesRegex(ValueError,'unsupported source SIMD float'):G.build_entries([self.q])
  finally:G.refbytes=old
if __name__=='__main__':unittest.main()

