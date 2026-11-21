import sys,unittest
from pathlib import Path
M=Path(__file__).resolve().parents[1];sys.path.insert(0,str(M));sys.path.insert(0,str(M/'tools'))
from config import configure,validate_driver_options,validate_library_result
from verify_saved_runs import check_library_consistency
class LibraryProvenance(unittest.TestCase):
 def setUp(self):
  self.h='a'*64;self.raw={'FNV_M3_LIB_SELECTION':'selection.json','FNV_M3_LIB_SHA256':self.h};self.arch={'libcmt.lib':'b'*64,'libcpmt.lib':'c'*64}
 def test_raw_pair_and_effective_mode(self):
  env=configure(self.raw,True);validate_driver_options(env,raw_environment=self.raw)
  for raw in ({'FNV_M3_LIB_SELECTION':'x'},dict(self.raw,FNV_M3='0'),dict(self.raw,FNV_M3_DV1='0'),dict(self.raw,FNV_M3_LIB_SHA256='z'*64)):
   with self.subTest(raw=raw),self.assertRaises(ValueError):validate_driver_options(configure(raw,True),raw_environment=raw)
  with self.assertRaises(ValueError):validate_driver_options(env,skip_data_v1=True,raw_environment=self.raw)
 def test_log_rejects_bad_counts_and_digests(self):
  good={'selection_sha256':self.h,'archive_sha256':self.arch,'selected':1,'bytes':4};self.assertEqual(validate_library_result(good,self.h)['bytes'],4)
  for changes in ({'selection_sha256':'d'*64},{'archive_sha256':{'libcmt.lib':'z'*64,'libcpmt.lib':'c'*64}},{'archive_sha256':{}},{'selected':True},{'selected':0},{'bytes':False},{'bytes':0}):
   with self.subTest(changes=changes),self.assertRaises(ValueError):validate_library_result(dict(good,**changes),self.h)
 def test_crossrun_and_legacy(self):
  item={'enabled':True,'selection_sha256':self.h,'archive_sha256':self.arch,'selected':1,'bytes':4};run={'provenance':{'library_overlay':item}}
  self.assertEqual(check_library_consistency({},[{},{}]),[]);self.assertEqual(check_library_consistency(run,[run,run],self.h),[])
  self.assertTrue(check_library_consistency(run,[{},run],self.h));self.assertTrue(check_library_consistency(run,[run,run],'f'*64))
 def test_bool_rejected_by_checker(self):
  item={'enabled':True,'selection_sha256':self.h,'archive_sha256':self.arch,'selected':True,'bytes':4};run={'provenance':{'library_overlay':item}}
  self.assertTrue(check_library_consistency(run,[run,run]))
if __name__=='__main__':unittest.main(verbosity=2)
