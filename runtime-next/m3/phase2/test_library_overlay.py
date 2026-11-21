import hashlib,json,sys,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parent));from library_overlay import select_library
h=lambda b:hashlib.sha256(b).hexdigest()
class LibraryOverlayTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.dir=Path(self.tmp.name);(self.dir/'libcmt.lib').write_bytes(b'archive1');(self.dir/'libcpmt.lib').write_bytes(b'archive2');self.blob=b'object1';self.lib=SimpleNamespace(LIB=self.dir,U=SimpleNamespace(read_ar=lambda p:[('x',self.blob)] if p.name=='libcmt.lib' else []))
  self.s={'units':[100001],'k':3,'data':b'abcd','relocs':[],'flags':0x00300040,'kind':'data-unit','name':'.data','defs':[('sym',0,2)]};self.st=SimpleNamespace(placed={'key':(0x1000,'B')},SEC={'key':self.s},KEYOF={(100001,3):'key'});self.lib.lib_units=lambda:{100001:{'secs':[dict(self.s)]}};self.c={'va':0x1000,'size':4,'kind':'data-unit','unit':100001,'library':'libcmt.lib','archive_sha256':h(b'archive1'),'object_sha256':h(self.blob),'unit_section_index':3,'tier':'B','section_name':'.data','section_flags':self.s['flags'],'compiler_bytes_sha256':h(b'abcd'),'alignment':4,'symbol_offsets':{'sym':0},'chunk':'data_0','section':'.data'}
 def tearDown(self):self.tmp.cleanup()
 def run_case(self,*,claim=(),fields=(),original=(),expected=None):
  p=self.dir/'selection.json';raw=json.dumps({'candidate_count':1,'candidate_bytes':4,'candidates':[self.c]}).encode();p.write_bytes(raw)
  return select_library(p,expected or h(raw),self.st,[],list(claim),[(0x1000,0x1100,'.data','data_0')],fields,original,lambda a,n:b'abcd',self.lib)
 def test_accept_exact(self):
  pieces,meta=self.run_case();self.assertEqual((len(pieces),meta['bytes'],pieces[0]['data']),(1,4,b'abcd'))
 def test_reject_overlaps_and_fields(self):
  for kwargs in ({'claim':[{'va':0x1002,'size':1}]},{'fields':[0xfff]},{'original':[0x1000]}):
   with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):self.run_case(**kwargs)
 def test_reject_digest_reloc_symbol_and_alignment(self):
  with self.assertRaises(ValueError):self.run_case(expected='0'*64)
  self.s['relocs']=[(0,)];
  with self.assertRaises(ValueError):self.run_case()
  self.s['relocs']=[];self.c['symbol_offsets']={'sym':1}
  with self.assertRaises(ValueError):self.run_case()
  self.c['symbol_offsets']={'sym':0};self.c['alignment']=8
  with self.assertRaises(ValueError):self.run_case()
 def test_reject_wrong_deduplicated_owner_section(self):
  self.st.KEYOF[(100001,3)]='different-key'
  with self.assertRaises(ValueError):self.run_case()
 def test_reject_mismatched_archive_object(self):
  self.c['object_sha256']='0'*64
  with self.assertRaisesRegex(ValueError,'archive/member'):self.run_case()
 def test_reject_wrong_candidate_count(self):
  p=self.dir/'bad.json';raw=json.dumps({'candidate_count':2,'candidate_bytes':4,'candidates':[self.c]}).encode();p.write_bytes(raw)
  with self.assertRaisesRegex(ValueError,'count mismatch'):
   select_library(p,h(raw),self.st,[],[],[(0x1000,0x1100,'.data','data_0')],[],[],lambda a,n:b'abcd',self.lib)
 def test_reject_duplicate_candidates(self):
  p=self.dir/'dup.json';raw=json.dumps({'candidate_count':2,'candidate_bytes':8,'candidates':[self.c,self.c]}).encode();p.write_bytes(raw)
  with self.assertRaisesRegex(ValueError,'overlap'):
   select_library(p,h(raw),self.st,[],[],[(0x1000,0x1100,'.data','data_0')],[],[],lambda a,n:b'abcd',self.lib)
 def test_reject_boolean_integer_fields(self):
  for key in ('va','size','unit'):
   with self.subTest(key=key):
    old=self.c[key];self.c[key]=True
    with self.assertRaises(ValueError):self.run_case()
    self.c[key]=old
 def test_reject_empty_or_boolean_count(self):
  for doc in ({'candidate_count':0,'candidate_bytes':0,'candidates':[]}, {'candidate_count':True,'candidate_bytes':4,'candidates':[self.c]}):
   p=self.dir/'invalid.json';raw=json.dumps(doc).encode();p.write_bytes(raw)
   with self.subTest(doc=doc),self.assertRaises(ValueError):
    select_library(p,h(raw),self.st,[],[],[(0x1000,0x1100,'.data','data_0')],[],[],lambda a,n:b'abcd',self.lib)
if __name__=='__main__':unittest.main()
