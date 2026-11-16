"""Authored buffers and reference-map attacks; no original image/object inputs."""
import importlib.util,struct,sys,unittest
from pathlib import Path
T=Path(__file__).resolve().parents[2]/'tools/rebuild';sys.path.insert(0,str(T))
import prospective_eh_observe as m
import prospective_eh_collect as c
class Backend:
 def __init__(self,blocks):self.blocks=blocks;self.reads=[]
 def read(self,address,size):
  self.reads.append((address,size))
  for base,data in self.blocks:
   if base<=address and address+size<=base+len(data):return data[address-base:address-base+size]
  return bytes(size)  # authored unrelated image bytes; the scope must reject these

def fixture():
 native_parent=bytearray(157);original_parent=bytearray(157);struct.pack_into('<I',original_parent,10,0x7000)
 native_code=bytearray(35);original_handler=bytearray(27);struct.pack_into('<I',original_handler,7,0x3000)
 native_meta=bytearray(44);original_meta=bytearray(44);struct.pack_into('<I',original_meta,40,0x4000)
 obj=dict(sections={1:dict(name='.text',flags=0x60000020,payload=bytes(native_parent),size=157,relocs=[(10,10,6)]),2:dict(name='.text$x',flags=0x60000020,payload=bytes(native_code),size=35,relocs=[(15,20,6)]),3:dict(name='.xdata$x',flags=0x40000040,payload=bytes(native_meta),size=44,relocs=[(40,11,6)])},symbols={10:dict(name='handler',section=2,value=8),11:dict(name='funclet',section=2,value=0),20:dict(name='info',section=3,value=0)})
 view=dict(root=dict(section=1,value=0,size=157,original_address='0x00001000'),owned_sections=[dict(section=2,name='.text$x'),dict(section=3,name='.xdata$x')],pieces=[dict(section=2,start=0,end=8),dict(section=2,start=8,end=35)])
 backend=Backend([(0x1000,bytes(original_parent)),(0x7000,bytes(original_handler)),(0x3000,bytes(original_meta)),(0x4000,bytes(8))]);return obj,view,backend,[(0x1000,0x2000),(0x4000,0x5000),(0x6f00,0x8000)]
class ProspectiveEHIndependentTests(unittest.TestCase):
 def test_noncontiguous_piece_does_not_grant_section_base_gap(self):
  obj,view,backend,executable=fixture();ref,_=m.prepare_scope(obj,view,backend,executable)
  self.assertEqual(ref.read(0x7000,27),bytes(7)+struct.pack('<I',0x3000)+bytes(16))
  self.assertEqual(ref.read(0x4000,8),bytes(8))
  with self.assertRaisesRegex(ValueError,'SCOPE'):ref.read(0x6ff8,1)
 def test_action_interior_native_cut_rejected(self):
  obj,view,backend,executable=fixture();obj['symbols'][11]['value']=1
  with self.assertRaises(ValueError):m.prepare_scope(obj,view,backend,executable)
 def test_metadata_in_executable_domain_rejected(self):
  obj,view,backend,executable=fixture();handler=bytearray(backend.blocks[1][1]);struct.pack_into('<I',handler,7,0x7000);backend.blocks[1]=(0x7000,bytes(handler))
  with self.assertRaisesRegex(ValueError,'domain'):m.prepare_scope(obj,view,backend,executable)
 def test_reference_read_budget_precedes_backend(self):
  b=Backend([]);r=m.ScopedReference(b,[(0x1000,0x2000)]);r.allow(0x1000,16,'code','authored');r.total=1024**2
  with self.assertRaisesRegex(ValueError,'budget'):r.read(0x1000,1)
  self.assertEqual(b.reads,[])
 def test_metadata_addend_crosses_to_noncontiguous_native_cut(self):
  path=Path(__file__).with_name('test_prospective_eh_observe.py');spec=importlib.util.spec_from_file_location('prospective_authored_crosscut_lane08',path);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
  def edit(obj):
   sec=obj['sections'][6];sec['payload']+=struct.pack('<I',8);sec['size']=len(sec['payload']);sec['relocs'].append((44,12,6))
   for symbol in obj['symbols'].values():
    if symbol['section']==6 and symbol['aux_count']==1:
     raw=bytearray(symbol['aux']);struct.pack_into('<I',raw,0,sec['size']);struct.pack_into('<H',raw,4,len(sec['relocs']));symbol['aux']=bytes(raw)
  with helper.valid_case(edit) as (case,root,obj,core):
   class CrossCutReference:
    def read(self,address,size):
     raw=bytearray(case['reference'].read(address,size));target=struct.pack('<I',0x20001000)
     for i in range(size):
      if 0x3000002c<=address+i<0x30000030:raw[i]=target[address+i-0x3000002c]
     return bytes(raw)
   result=m.compare_parent(core,obj,m.inventory_parent(obj,root),case['recipe'],[case['recipe']],CrossCutReference(),case['executable_ranges'])
   self.assertTrue(result['metadata_comparisons'][0]['full_MATCH']);field=next(f for f in result['metadata_comparisons'][0]['fields'] if f['offset']==44);self.assertEqual(field['expected_target'],0x20001000)
 def test_native_execution_domain_mismatches_remain_unsupported(self):
  path=Path(__file__).with_name('test_prospective_eh_observe.py');spec=importlib.util.spec_from_file_location('prospective_authored_domains_lane08',path);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
  for section,executable in ((3,False),(4,False),(6,True)):
   def edit(obj):
    if executable:obj['sections'][section]['flags']|=0x20000000
    else:obj['sections'][section]['flags']&=~0x20000000
   with self.subTest(section=section),helper.valid_case(edit) as (_,root,obj,_):
    view=m.inventory_parent(obj,root);self.assertTrue(any('EXEC' in reason or 'DOMAIN' in reason for reason in view['unsupported']));self.assertFalse(view['full_closure_verified'])
 def test_declared_allocation_rejected_before_core_parser(self):
  raw=bytearray(60);struct.pack_into('<HH',raw,0,0x14c,1);struct.pack_into('<I',raw,36,256*1024**2+1)
  with self.assertRaisesRegex(ValueError,'allocation'):c.allocation_preflight(bytes(raw))
if __name__=='__main__':unittest.main()
