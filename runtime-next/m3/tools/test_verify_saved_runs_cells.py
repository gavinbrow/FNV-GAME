import importlib.util, unittest, copy
from pathlib import Path
spec=importlib.util.spec_from_file_location('verify',Path(__file__).with_name('verify_saved_runs.py')); v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class CellState(unittest.TestCase):
 def setUp(self):
  self.verdict={'steps':{'quick_bindings':{'quicksave_scan':63,'quickload_scan':64},'extended':{'cell_before_save':1,'cell_after_save':1,'cell_after_coc':2,'cell_before_load':2,'cell_after_load':1,'cell_changed':True,'cell_restored':True}}}
 def test_valid(self): self.assertEqual(v.check_cell_state(self.verdict),[])
 def test_missing(self): del self.verdict['steps']['extended']['cell_before_save']; self.assertTrue(v.check_cell_state(self.verdict))
 def test_wrong(self): self.verdict['steps']['extended']['cell_after_load']=3; self.assertTrue(v.check_cell_state(self.verdict))
 def test_unchanged(self): self.verdict['steps']['extended']['cell_after_coc']=self.verdict['steps']['extended']['cell_before_load']=1; self.assertTrue(v.check_cell_state(self.verdict))
 def test_bool(self): self.verdict['steps']['extended']['cell_before_save']=True; self.assertTrue(v.check_cell_state(self.verdict))
 def test_binding(self): self.verdict['steps']['quick_bindings']['quickload_scan']=True; self.assertTrue(v.check_cell_state(self.verdict))
if __name__=='__main__': unittest.main()
