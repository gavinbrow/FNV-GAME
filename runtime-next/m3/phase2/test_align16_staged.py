import importlib.util,sys,struct,unittest,tempfile,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;D=M/'out/phase2-align16';s=importlib.util.spec_from_file_location('staged_splice16',D/'candidate-splice.py');S=importlib.util.module_from_spec(s);sys.modules[s.name]=S;s.loader.exec_module(S)
class Coff:
 def __init__(self,alignment,offset):
  self.data=bytearray(256);struct.pack_into('<II',self.data,36,128,64);self.sections=[None,{'name':'.rdata','flags':alignment<<20,'data':bytes(128),'relocs':[]}];self.symbols={};self.offset=offset
 def named(self,name):return {'section':1,'value':self.offset,'storage':2}
class Alignment16(unittest.TestCase):
 def test_aligned_file_backed(self):self.assertEqual(len(S.slice_entry(Coff(5,16),{'sym':'x','size':16,'align':16})[0]),16)
 def test_bad_section_or_symbol_alignment(self):
  for bits,offset in ((4,16),(0,16),(15,16),(5,4)):
   with self.subTest(bits=bits,offset=offset),self.assertRaises(ValueError):S.slice_entry(Coff(bits,offset),{'sym':'x','size':16,'align':16})
 def test_rawless_rejected(self):
  c=Coff(5,16);struct.pack_into('<I',c.data,40,0)
  with self.assertRaises(ValueError):S.slice_entry(c,{'sym':'x','size':16,'align':16})
 def test_bad_destination_and_overlap_fail_before_object_loading(self):
  for entries in ([{'sym':'x','va':0x1004,'size':16,'align':16}],
                  [{'sym':'x','va':0x1000,'size':16,'align':True}],
                  [{'sym':'x','va':0x1000,'size':32,'align':16},{'sym':'y','va':0x1010,'size':16,'align':16}]):
   with self.subTest(entries=entries),tempfile.TemporaryDirectory() as d:
    p=Path(d)/'manifest.json';p.write_text(json.dumps({'entries':entries}))
    with self.assertRaises(ValueError):S.load(str(p))
if __name__=='__main__':unittest.main()
