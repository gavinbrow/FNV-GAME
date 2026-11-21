import contextlib,io,json,os,sys,tempfile,unittest
from pathlib import Path
M=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(M));import splice
class LibraryControl(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.p=Path(self.tmp.name)/'pieces.json';self.env=os.environ.get('FNV_M3_NEGCTL');os.environ['FNV_M3_NEGCTL']='p2lv'
 def tearDown(self):
  if self.env is None:os.environ.pop('FNV_M3_NEGCTL',None)
  else:os.environ['FNV_M3_NEGCTL']=self.env
  self.tmp.cleanup()
 def run_rows(self,rows):
  self.p.write_text(json.dumps({'pieces':rows}));out=io.StringIO()
  with contextlib.redirect_stdout(out):result=splice.load_dv1(str(self.p))
  return result,out.getvalue()
 def row(self,va,marked=False,relocs=None):
  r={'va':va,'data':'01020304','relocs':relocs or [],'section':'.data','kind':'data-unit','tier':'B','unit':100001,'size':4}
  if marked:r['library_opt_in']=True
  return r
 def test_only_marked_library_mutated(self):
  rs,log=self.run_rows([self.row(0x1000),self.row(0x2000,True),self.row(0x3000,True)])
  self.assertEqual([r['data'] for r in rs],[b'\x01\x02\x03\x04',b'\x00\x02\x03\x04',b'\x01\x02\x03\x04']);self.assertIn('VA 00002000 offset 0 changed from 01 to 00',log)
  again,again_log=self.run_rows([self.row(0x1000),self.row(0x2000,True),self.row(0x3000,True)])
  self.assertEqual([r['data'] for r in rs],[r['data'] for r in again]);self.assertEqual(log,again_log)
 def test_fail_without_unrelocated_marked(self):
  for rows in ([self.row(0x1000)],[self.row(0x1000,True,[[0,0x2000,0]])]):
   with self.subTest(rows=rows),self.assertRaises(ValueError):self.run_rows(rows)
if __name__=='__main__':unittest.main()
