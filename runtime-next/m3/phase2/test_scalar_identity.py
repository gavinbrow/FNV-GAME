import sys,unittest
from pathlib import Path
M=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(M));import gen_m3 as G
class ScalarIdentityTest(unittest.TestCase):
 def setUp(self):self.r={'va':0x104f2a8,'tc':'M','scalar_namespace':'fnv_00641830','scalar_const':False,'scalar_symbol':'?DAT_0104f2a8@fnv_00641830@@3MA','decl':['?DAT_0104f2a8@fnv_00641830@@3MA']}
 def test_exact_identity(self):self.assertEqual(G.explicit_scalar_identity(self.r),('fnv_00641830',False,self.r['scalar_symbol']))
 def test_reject_malformed(self):
  for k,v in [('scalar_namespace','bad::name'),('scalar_const',1),('scalar_symbol','?DAT_0104f2a8@@3MA'),('decl',[]),('generated_name','M3_0104f2a8')]:
   with self.subTest(k=k),self.assertRaises(ValueError):G.explicit_scalar_identity(dict(self.r,**{k:v}))
 def test_opt_in_emits_namespace_mutable_in_rdata(self):
  e={'va':self.r['va'],'tc':'M','section':'.rdata','type':'float','name':'DAT_0104f2a8','ns':self.r['scalar_namespace'],'scalar_const':False,'file_backed':True,'init':'1.0f'}
  s=G.cpp([e]);self.assertIn('namespace fnv_00641830 { extern __declspec(allocate(".rdata")) float DAT_0104f2a8 = 1.0f; }',s)
 def test_legacy_identity_remains_untouched(self):self.assertIsNone(G.explicit_scalar_identity({'va':1,'tc':'H'}))
 def test_const_scalar_in_data(self):
  e={'va':0x1184000,'size':4,'tc':'H','section':'.data','type':'int','name':'DAT_01184000','ns':'Example','scalar_const':True,'file_backed':True,'init':'7'}
  self.assertIn('namespace Example { extern __declspec(allocate(".data")) const int DAT_01184000 = 7; }',G.cpp([e]))
 def test_namespaced_host_rejected(self):
  scalar={'va':0x1184000,'size':4,'tc':'H','section':'.data','type':'int','name':'DAT_01184000','ns':'Example','scalar_const':False,'file_backed':True,'init':'7'}
  table={'va':0x1185000,'tc':'T','section':'.data','type':'void*','name':'DAT_01185000','n':1,'size':4,'elems':[('p',0x1184000)]}
  with self.assertRaisesRegex(ValueError,'table host'):G.cpp([scalar,table])
if __name__=='__main__':unittest.main()

