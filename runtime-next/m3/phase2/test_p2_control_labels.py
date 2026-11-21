import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from verify_saved_runs import check_control_logs
class P2ControlLabels(unittest.TestCase):
 def run_label(self,label,control,kind,*,library=False,extra=''):
  with tempfile.TemporaryDirectory(prefix='p2labels_') as d:
   p=Path(d);gen='' if library else 'NEGATIVE CONTROL (%s): fixture\n'%label
   verify=('NEGATIVE CONTROL (%s): fixture\n'%label if library else '')+extra+'ROUND TRIP FAILED\nnegative control: failure is expected\n'+('M3 RELOC VALUE MISMATCH\n' if kind=='pointer' else ' DIFFERENT relocs \n')
   (p/'gen.log').write_text(gen);(p/'verify.log').write_text(verify)
   summary={'steps':[{'name':'m3-gen','log':'gen.log'},{'name':'data-v3','log':'verify.log'}],'provenance':{'m3_config':{'negative_control':control}}}
   return check_control_logs(p/'summary.json',summary)
 def test_new_value_and_pointer_labels(self):
  for label,control,kind in [('p2 scalar value','p2sv','value'),('p2 array value','p2av','value'),('p2 tail pointer','p2wp','pointer')]:
   with self.subTest(label=label):self.assertEqual(self.run_label(label,control,kind),kind)
 def test_library_value_from_verify_log(self):self.assertEqual(self.run_label('p2 library value','p2lv','value',library=True),'value')
 def test_wrong_id_and_ambiguous_label_rejected(self):
  with self.assertRaises(ValueError):self.run_label('p2 array value','p2sv','value')
  with self.assertRaises(ValueError):self.run_label('p2 library value','p2lv','value',library=True,extra='NEGATIVE CONTROL (p2 library value): different\n')
if __name__=='__main__':unittest.main(verbosity=2)
