import copy,json,sys,tempfile,unittest
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path(__file__).resolve().parent));import tesform_load_typed_correction as c
class Tests(unittest.TestCase):
 def docs(self):
  unit={'source':'x','functions':[{'address':'0x1','size':1}],'symbols':{'old':'0x10'}};a={'units':[{} for _ in range(998)]+[unit]};b=copy.deepcopy(a);b['units'][998]['symbols']['new']='0x10';e={'literal_facts':[{'production_label':'new','binding':'0x10'}]};return a,b,e
 def test_delta_accepts_exact_binding_and_rejects_function_change(self):
  a,b,e=self.docs();c.delta(json.dumps(a).encode(),json.dumps(b).encode(),e);b['units'][998]['functions'][0]['size']=2
  with self.assertRaises(ValueError):c.delta(json.dumps(a).encode(),json.dumps(b).encode(),e)
 def test_delta_rejects_unlisted_binding(self):
  a,b,e=self.docs();b['units'][998]['symbols']['extra']='0x20'
  with self.assertRaises(ValueError):c.delta(json.dumps(a).encode(),json.dumps(b).encode(),e)
 def test_guarded_apply_and_rollback_in_temp(self):
  a,b,e=self.docs();old=json.dumps(a).encode();new=json.dumps(b).encode()
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);oldF,oldT,oldC=c.F,c.T,c.C;c.F=p/'fn';c.T=p/'tx';c.C=c.T/'production-correction';(c.F/'build').mkdir(parents=True);c.C.mkdir(parents=True);(c.T/'applied.json').touch();target=c.F/'build/units.json';target.write_bytes(old)
   try:
    with mock.patch.object(c.tx.lock,'acquire_guard',return_value=[]),mock.patch.object(c,'proof',return_value=(old,new)):
     c.run('apply','a'*64);self.assertEqual(target.read_bytes(),new);c.run('restore','a'*64);self.assertEqual(target.read_bytes(),old)
   finally:c.F,c.T,c.C=oldF,oldT,oldC
if __name__=='__main__':unittest.main()
