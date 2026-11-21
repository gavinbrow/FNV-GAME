import sys,struct,unittest,tempfile,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import vtable_search_library as v

def obj(name=b'weak',section=1):
 sym=name.ljust(8,b'\0')+struct.pack('<IhHBB',0,section,0x20,2,0)
 return struct.pack('<HHIIIHH',0x14c,0,0,20,1,0,0)+sym+struct.pack('<I',4)
def ar(member):
 def entry(name,data):
  hdr=name.ljust(16,b' ')+b'0'.ljust(12,b' ')+b'0'.ljust(6,b' ')+b'0'.ljust(6,b' ')+b'0'.ljust(8,b' ')+str(len(data)).encode().ljust(10,b' ')+b'`\n'
  return hdr+data+(b'\n' if len(data)&1 else b'')
 # Both valid empty symbol indexes still enumerate the sole member.
 first=struct.pack('>I',0); second_size=12
 offset=8+len(entry(b'/',first))+60+second_size
 second=struct.pack('<III',1,offset,0)
 return b'!<arch>\n'+entry(b'/',first)+entry(b'/',second)+entry(b'one.obj/',member)

class T(unittest.TestCase):
 def test_strong(self):self.assertEqual(len(v.scan_coff(obj(b'weak'),b'weak')),1)
 def test_undef(self):self.assertEqual(v.scan_coff(obj(b'weak',0),b'weak'),[])
 def test_truncated(self):
  with self.assertRaises(ValueError):v.scan_coff(obj()[:-2],b'weak')
 def test_complete(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);x=obj(b'other');y=ar(obj(b'other'));(p/'a').write_bytes(x);(p/'b').write_bytes(y);h=lambda b:hashlib.sha256(b).hexdigest();a=[(0,p/'a',h(x))];b=[('lib',p/'b',h(y))]
   self.assertEqual(v.prove_absent('weak',b,['lib'],a,[0])['strong_primary_count'],0)
   with self.assertRaises(ValueError):v.prove_absent('weak',b,['lib','missing'],a,[0])
   with self.assertRaises(ValueError):v.prove_absent('other',b,['lib'],a,[0])
if __name__=='__main__':unittest.main()
