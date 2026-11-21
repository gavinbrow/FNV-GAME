"""Temporary-only tests for guarded W103 tool transaction."""
import hashlib,importlib.util,tempfile,unittest
from pathlib import Path
p=Path(__file__).with_name('psa_w103_control_transaction.py');sp=importlib.util.spec_from_file_location('tx',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class Tx(unittest.TestCase):
 def setup_tree(self,root):
  pkg=root/'package';work=root/'work';items=[]
  for i in range(3):
   rel='runtime-next/f%d.py'%i;old=('old%d'%i).encode();new=('new%d'%i).encode()
   for base,data in ((work,old),(pkg/'original',old),(pkg/'payload',new)):
    p=base/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
   items.append({'path':rel,'old_sha256':hashlib.sha256(old).hexdigest(),'new_sha256':hashlib.sha256(new).hexdigest()})
  return work,pkg,{'files':items}
 def test_wrong_preimage_no_partial_write(self):
  with tempfile.TemporaryDirectory() as d:
   root,pkg,manifest=self.setup_tree(Path(d));(root/'runtime-next/f2.py').write_text('unknown')
   with self.assertRaises(ValueError):m.execute(root,pkg,manifest,'apply')
   self.assertEqual((root/'runtime-next/f0.py').read_text(),'old0')
 def test_write_failure_rolls_back(self):
  with tempfile.TemporaryDirectory() as d:
   root,pkg,manifest=self.setup_tree(Path(d));calls=[]
   def writer(p,data,tmp):
    calls.append(p)
    if len(calls)==2:raise OSError('simulated failure')
    m.atomic(p,data,tmp)
   with self.assertRaises(OSError):m.execute(root,pkg,manifest,'apply',writer)
   self.assertEqual([(root/('runtime-next/f%d.py'%i)).read_text() for i in range(3)],['old0','old1','old2'])
 def test_apply_restore_and_mixed_recovery(self):
  with tempfile.TemporaryDirectory() as d:
   root,pkg,manifest=self.setup_tree(Path(d));self.assertEqual(m.execute(root,pkg,manifest,'apply'),3);self.assertEqual(m.execute(root,pkg,manifest,'restore'),3);(root/'runtime-next/f1.py').write_text('new1');self.assertEqual(m.execute(root,pkg,manifest,'recover'),3);self.assertEqual((root/'runtime-next/f1.py').read_text(),'old1')
if __name__=='__main__':unittest.main()
