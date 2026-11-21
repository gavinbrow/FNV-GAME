import sys,unittest
from pathlib import Path
from unittest.mock import patch
M=Path(__file__).resolve().parents[1];sys.path.insert(0,str(M));sys.path.insert(0,str(M/'tools'))
from config import configure,validate_driver_options
from verify_saved_runs import check_weak_coff,check_weak_consistency
class WeakProvenance(unittest.TestCase):
 def test_option_validation(self):
  for value in ('', '2','yes'):
   with self.subTest(value=value),self.assertRaises(ValueError):validate_driver_options(configure({'FNV_COFF_WEAK':value},True))
  with self.assertRaises(ValueError):validate_driver_options(configure({'FNV_COFF_WEAK':'1'},True),skip_data_v1=True)
  validate_driver_options(configure({'FNV_COFF_WEAK':'0'},True),skip_data_v1=False)
 def test_cross_run_consistency_and_legacy(self):
  h='a'*64; r='b'*64
  make=lambda enabled=True,helper=h,resolver=r:{'provenance':{'weak_coff':{'enabled':enabled,'helper_sha256':helper,'resolver_sha256':resolver}}}
  self.assertEqual(check_weak_consistency({},[{},{}]),[])
  self.assertEqual(check_weak_consistency(make(),[make(),make()]),[])
  for controls in ([{},make()],[make(False),make()],[make(helper='c'*64),make()],[make(resolver=None),make()]):
   self.assertTrue(check_weak_consistency(make(),controls))
 def test_mode_hash_requires_real_boolean_and_digests(self):
  h='a'*64;r='b'*64; run={'provenance':{'weak_coff':{'enabled':True,'helper_sha256':h,'resolver_sha256':r}}}
  self.assertEqual(check_weak_coff(run,'x','1',h,r),[])
  self.assertTrue(check_weak_coff(run,'x','1',None,r))
  run['provenance']['weak_coff']['enabled']=1
  self.assertTrue(check_weak_coff(run,'x','1',h,r))
if __name__=='__main__':unittest.main(verbosity=2)
