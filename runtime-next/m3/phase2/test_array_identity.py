import sys,unittest
from pathlib import Path
M=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(M));import gen_m3 as G
class Arrays(unittest.TestCase):
 def setUp(self):
  self.a=0x11a7440;self.sym='?DAT_011a7440@sa238a0@@3PAEA';self.r={'va':self.a,'tc':'A','et':'E','size':256,'align':4,'array_namespace':'sa238a0','array_const':False,'array_symbol':self.sym,'decl':[self.sym]}
 def test_valid(self):self.assertEqual(G.explicit_array_identity(self.r),('sa238a0',False,self.sym))
 def test_bad_identity(self):
  for key,value in [('va',self.a+1),('size',257),('align',1),('et','D'),('array_const',True),('array_namespace','other'),('array_symbol','bad'),('decl',[])]:
   with self.subTest(key=key),self.assertRaises(ValueError):G.explicit_array_identity(dict(self.r,**{key:value}))
 def test_namespace_render(self):
  e={'va':self.a,'size':256,'tc':'A','section':'.data','type':'unsigned char','name':'DAT_011a7440','ns':'sa238a0','array_const':False,'init':'{1}','n':256}
  self.assertIn('namespace sa238a0 { unsigned char DAT_011a7440[256] = {1}; }',G.cpp([e]))
 def test_array_table_host_rejected(self):
  e={'va':self.a,'size':256,'tc':'A','section':'.data','type':'unsigned char','name':'DAT_011a7440','ns':'sa238a0','array_const':False,'init':'{1}','n':256}
  t={'va':0x1185000,'tc':'T','section':'.data','type':'void*','name':'DAT_01185000','n':1,'size':4,'elems':[('p',self.a)]}
  with self.assertRaisesRegex(ValueError,'table host'):G.cpp([e,t])
if __name__=='__main__':unittest.main()
