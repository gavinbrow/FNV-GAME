import sys,json,hashlib,unittest,importlib.util
from pathlib import Path
H=Path(__file__).resolve().parent;D=H.parent/'out/phase2-library-splits';sys.path.insert(0,str(H))
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
stage=load('library_split_staged',D/'candidate-library_overlay.py');base=load('library_base_tests',H/'test_library_overlay.py');base.select_library=stage.select_library
class SplitTests(base.LibraryOverlayTest):
 def setup_split(self):
  original=dict(self.s);original.update(data=b'xxxxabcd',defs=[('sym',4,2)]);self.lib.lib_units=lambda:{100001:{'secs':[original]}};self.st.PIECES={(100001,3):[(4,8,'key')]};self.c.update(split_section=True,section_start=4,section_end=8,section_size=8,full_section_sha256=hashlib.sha256(b'xxxxabcd').hexdigest());return original
 def test_accept_symbol_boundary_split(self):
  self.setup_split();pieces,meta=self.run_case();self.assertEqual((len(pieces),meta['bytes']),(1,4))
 def test_reject_wrong_piece_boundaries(self):
  self.setup_split();self.st.PIECES[(100001,3)]=[(3,8,'key')]
  with self.assertRaisesRegex(ValueError,'split placement identity'):self.run_case()
 def test_reject_crossing_relocation(self):
  original=self.setup_split();original['relocs']=[(2,6,'x')]
  with self.assertRaisesRegex(ValueError,'relocation crosses'):self.run_case()
 def test_reject_changed_original_or_definitions(self):
  original=self.setup_split();original['data']=b'yyyyabcd'
  with self.assertRaisesRegex(ValueError,'source section changed'):self.run_case()
  original['data']=b'xxxxabcd';original['defs']=[('sym',5,2)]
  with self.assertRaisesRegex(ValueError,'adjacent symbol interval|definitions changed'):self.run_case()
if __name__=='__main__':unittest.main()


