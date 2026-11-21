import sys,struct,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'direct-v1'))
from game_state import PlayerCellProbe,StateUnavailable,PLAYER_GLOBAL_DATA_OFFSET

class FakeReader:
 def __init__(self, base=0x700000, image='C:/fake/FalloutNV.exe'):
  self.base=base; self.image=image; self.closed=False; self.calls=[]; self.values={}; self.responses={}; self.size=0x1000000
  dos=bytearray(64); dos[:2]=b'MZ'; struct.pack_into('<I',dos,0x3c,0x80); self.values[(base,64)]=bytes(dos)
  pe=bytearray(26); pe[:4]=b'PE\0\0'; struct.pack_into('<H',pe,4,0x14c); struct.pack_into('<H',pe,6,1); struct.pack_into('<H',pe,20,0xe0); struct.pack_into('<H',pe,24,0x10b); self.values[(base+0x80,26)]=bytes(pe)
  sh=bytearray(40); sh[:8]=b'.data\0\0\0'; struct.pack_into('<II',sh,8,0x100000,0x1000); self.values[(base+0x80+24+0xe0,40)]=bytes(sh)
  for a,v in ((base+0x1000+PLAYER_GLOBAL_DATA_OFFSET,0x22000000),(0x22000040,0x33000000),(0x3300000c,0x12345678)): self.values[(a,4)]=struct.pack('<I',v)
 def modules(self): return [(self.image,self.base,self.size)]
 def read(self,a,n):
  self.calls.append((a,n))
  if (a,n) in self.responses:
   v=self.responses[(a,n)].pop(0)
   if isinstance(v,Exception): raise v
   return v
  return self.values[(a,n)]
 def close(self): self.closed=True

class Tests(unittest.TestCase):
 def make(self,reader): return PlayerCellProbe(123,reader.image,_reader_factory=lambda pid:reader)
 def test_relocated_addresses_and_close(self):
  r=FakeReader()
  with self.make(r) as p: self.assertEqual(p.read_cell_id(),0x12345678)
  self.assertTrue(r.closed)
  self.assertEqual(r.calls[3:],[(r.base+0x1000+PLAYER_GLOBAL_DATA_OFFSET,4),(0x22000040,4),(0x3300000c,4)]*2)
  with self.assertRaises(StateUnavailable): p.read_cell_id()
 def test_null_and_zero_and_short_reads(self):
  for key in ('player','cell','id','short','failed'):
   with self.subTest(key=key):
    r=FakeReader(); p=self.make(r); a={'player':r.base+0x1000+PLAYER_GLOBAL_DATA_OFFSET,'cell':0x22000040,'id':0x3300000c,'short':0x3300000c,'failed':0x3300000c}[key]
    r.responses[(a,4)]=[b'\0'*4 if key in ('player','cell','id') else b'\x01' if key=='short' else StateUnavailable('error')]
    with self.assertRaises(StateUnavailable): p.read_cell_id()
    p.close(); self.assertTrue(r.closed)
 def test_transient_pointer_and_form_changes(self):
  for addr,first,second in ((0x700000+0x1000+PLAYER_GLOBAL_DATA_OFFSET,0x22000000,0x22000010),(0x22000040,0x33000000,0x33000010),(0x3300000c,0x12345678,0x12345679)):
   r=FakeReader(); p=self.make(r); r.responses[(addr,4)]=[struct.pack('<I',first),struct.pack('<I',second)]
   # Point an alternate player/cell back into defined fake memory so mismatch is observed.
   r.values[(0x22000050,4)]=struct.pack('<I',0x33000000); r.values[(0x3300001c,4)]=struct.pack('<I',0x12345678)
   with self.assertRaises(StateUnavailable): p.read_cell_id()
   p.close()
 def test_bad_pe_and_wrong_main_module_close(self):
  for mode in ('path','machine','magic','signature','bounds'):
   with self.subTest(mode=mode):
    r=FakeReader()
    if mode=='path': r.image='C:/wrong.exe'; path='C:/fake/FalloutNV.exe'
    else: path=r.image
    if mode in ('machine','magic','signature'):
     x=bytearray(r.values[(r.base+0x80,26)]); off={'machine':4,'magic':24,'signature':0}[mode]; x[off]=0; r.values[(r.base+0x80,26)]=bytes(x)
    if mode=='bounds': r.size=256
    with self.assertRaises(StateUnavailable): PlayerCellProbe(1,path,_reader_factory=lambda pid:r)
    self.assertTrue(r.closed)
 def test_section_layout_rejected_and_handle_closed(self):
  for mode in ('missing','small','short'):
   with self.subTest(mode=mode):
    r=FakeReader(); key=(r.base+0x80+24+0xe0,40); sh=bytearray(r.values[key])
    if mode=='missing': sh[:8]=b'.other\0\0'
    if mode=='small': struct.pack_into('<I',sh,8,0x1000)
    r.values[key]=bytes(sh) if mode!='short' else b'\0'
    with self.assertRaises(StateUnavailable): self.make(r)
    self.assertTrue(r.closed)
 def test_enumeration_failure_closes(self):
  r=FakeReader(); r.modules=lambda: (_ for _ in ()).throw(StateUnavailable('snapshot error'))
  with self.assertRaises(StateUnavailable): self.make(r)
  self.assertTrue(r.closed)

if __name__=='__main__': unittest.main(verbosity=2)
