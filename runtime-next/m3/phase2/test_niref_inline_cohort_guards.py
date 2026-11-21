import sys,tempfile,unittest
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path(__file__).resolve().parent));import niref_inline_cohort_run as d
class Tests(unittest.TestCase):
 def test_clean_env_rejects_injected_flags_and_controls(self):
  z=d.clean({'PATH':'safe','CL':'/O2','_Cl_':'/DHAZARD','FNV_M3':'1','Fnv_x':'x','CODEX_NEGATIVE_INJECT':'1','SAFE':'v'});self.assertEqual(z,{'PATH':'safe','SAFE':'v'})
 def test_bad_runner_pin_fails_before_source_read(self):
  with mock.patch.object(d,'j',side_effect=AssertionError('unexpected read')):
   with self.assertRaisesRegex(ValueError,'runner/tool freeze'):d.validate('0'*64)
 def test_no_lane_ack_fails_before_validation(self):
  with mock.patch.object(sys,'argv',['test','--runner-sha256','x']):
   with mock.patch.object(d,'validate',side_effect=AssertionError('unexpected validation')):
    with self.assertRaisesRegex(ValueError,'acknowledgement'):d.main()
if __name__=='__main__':unittest.main()
