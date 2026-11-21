import sys,struct,unittest,os
from pathlib import Path
from unittest.mock import patch
PB=Path(__file__).resolve().parents[2]/'pinned-build';sys.path.insert(0,str(PB))
import coff_weak as W
import assemble_v3 as A

class FakeCoff:
 def __init__(self,kind=3):
  self.data=bytearray(20+18*6);struct.pack_into('<II',self.data,8,20,6)
  self.symbols={0:dict(name='weak',section=0,storage=105,value=0,type=0),2:dict(name='fallback',section=0,storage=2,value=0),3:dict(name='fallback',section=4,storage=2,value=0)}
  self.by_name={'weak':[self.symbols[0]],'fallback':[self.symbols[2],self.symbols[3]]}
  self.weak(0,2,kind)
 def weak(self,index,target,kind,aux=1):
  struct.pack_into('<8sIhHBB',self.data,20+18*index,self.symbols[index]['name'].encode(),0,0,0,105,aux)
  struct.pack_into('<II',self.data,20+18*(index+1),target,kind)
 def lookup(self,s): return ('local',0x1234) if s.get('section')==4 else (None,None)

class Tests(unittest.TestCase):
 def test_alias_and_nolibrary(self):
  for kind in (1,3):
   c=FakeCoff(kind);self.assertEqual(W.resolve_fallback(c,0,c.lookup),('weak-fallback/local',0x1234))
 def test_library_search_rejected(self):
  with self.assertRaises(W.WeakResolutionError):W.resolve_fallback(FakeCoff(2),0,lambda s:('bad',1))
 def test_bad_aux_invalid_index_and_cycle(self):
  for target,kind,aux in ((5,3,1),(2,4,1),(2,3,0),(0,3,1)):
   with self.subTest(target=target,kind=kind,aux=aux):
    c=FakeCoff();c.weak(0,target,kind,aux)
    with self.assertRaises(W.WeakResolutionError):W.resolve_fallback(c,0,c.lookup)
 def test_invalid_weak_primary_reserved_and_metadata(self):
  for mutation in ('section','value','type','reserved','name','parsed_type','truncated_table'):
   with self.subTest(mutation=mutation):
    c=FakeCoff()
    if mutation=='section': struct.pack_into('<h',c.data,20+12,1)
    elif mutation=='value': struct.pack_into('<I',c.data,20+8,1)
    elif mutation=='type': struct.pack_into('<H',c.data,20+14,0x40)
    elif mutation=='reserved': c.data[20+18+8]=1
    elif mutation=='name': c.symbols[0]['name']='different'
    elif mutation=='parsed_type': c.symbols[0]['type']=0x20
    else: c.data=c.data[:-1]
    with self.assertRaises(W.WeakResolutionError):W.resolve_fallback(c,0,c.lookup)
 def test_chain_and_cycle(self):
  c=FakeCoff();c.symbols[2]=dict(name='second',section=0,storage=105,value=0,type=0);c.by_name['second']=[c.symbols[2]];c.weak(2,3,3)
  self.assertEqual(W.resolve_fallback(c,0,c.lookup),('weak-fallback/local',0x1234))
  c.weak(2,0,3)
  with self.assertRaises(W.WeakResolutionError):W.resolve_fallback(c,0,c.lookup)
 def test_nonexternal_fallback_rejected_and_local_duplicate_ignored(self):
  c=FakeCoff(); c.symbols[2]['storage']=3
  with self.assertRaises(W.WeakResolutionError):W.resolve_fallback(c,0,c.lookup)
  c=FakeCoff(); c.symbols[3]['storage']=3
  self.assertEqual(W.resolve_fallback(c,0,c.lookup),(None,None))
 def test_conflicting_fallback_rejected(self):
  c=FakeCoff();c.symbols[2]['section']=5
  with self.assertRaises(W.WeakResolutionError): W.resolve_fallback(c,0,lambda s:('mapped',s['section']))
 def test_wrapper_opt_in_direct_first(self):
  c=FakeCoff();sym=c.symbols[0]
  def direct(*args):
   t=args[4];return ('primary',55) if t is sym else c.lookup(t)
  with patch.object(A,'_resolve_field_direct',side_effect=direct),patch.dict(os.environ,{'FNV_COFF_WEAK':'1'}):
   self.assertEqual(A.resolve_field(c,{},[],6,sym,0,0,b''),('primary',55))
  def fallback(*args):return c.lookup(args[4])
  with patch.object(A,'_resolve_field_direct',side_effect=fallback),patch.dict(os.environ,{'FNV_COFF_WEAK':'1'}):
   self.assertEqual(A.resolve_field(c,{},[],6,sym,0,0,b''),('weak-fallback/local',0x1234))
  with patch.object(A,'_resolve_field_direct',side_effect=fallback),patch.dict(os.environ,{'FNV_COFF_WEAK':'0'}):
   self.assertEqual(A.resolve_field(c,{},[],6,sym,0,0,b''),(None,None))
 def test_actual_direct_resolver_with_mapped_fallback_and_addend(self):
  c=FakeCoff(); sym=c.symbols[0]; unit={'_fnmap':{},'symbols':{'fallback':'0x00401000'}}
  fake={'pe':object(),'fn':{},'sym':{},'imp':{},'thunks':{}}
  with patch.dict(A.G,fake,clear=True),patch.dict(os.environ,{'FNV_COFF_WEAK':'1'}):
   self.assertEqual(A.resolve_field(c,unit,[],6,sym,4,0,b''),('weak-fallback/c',0x00401004))
 def test_actual_primary_strong_mapping_precedes_fallback(self):
  c=FakeCoff(); unit={'_fnmap':{},'symbols':{'weak':'0x00402000','fallback':'0x00401000'}}
  fake={'pe':object(),'fn':{},'sym':{},'imp':{},'thunks':{}}
  with patch.dict(A.G,fake,clear=True),patch.dict(os.environ,{'FNV_COFF_WEAK':'1'}):
   self.assertEqual(A.resolve_field(c,unit,[],6,c.symbols[0],0,0,b''),('c',0x00402000))
 def test_strong_primary_requires_valid_weak_metadata_but_accepts_library_mode(self):
  c=FakeCoff(2); unit={'_fnmap':{},'symbols':{'weak':'0x00402000'}}
  fake={'pe':object(),'fn':{},'sym':{},'imp':{},'thunks':{}}
  with patch.dict(A.G,fake,clear=True),patch.dict(os.environ,{'FNV_COFF_WEAK':'1'}):
   self.assertEqual(A.resolve_field(c,unit,[],6,c.symbols[0],0,0,b''),('c',0x00402000))
   c.data[20+18+8]=1
   self.assertEqual(A.resolve_field(c,unit,[],6,c.symbols[0],0,0,b''),(None,None))
 def test_strong_primary_does_not_mask_weak_cycle(self):
  c=FakeCoff();c.weak(0,0,3);unit={'_fnmap':{},'symbols':{'weak':'0x00402000'}}
  fake={'pe':object(),'fn':{},'sym':{},'imp':{},'thunks':{}}
  with patch.dict(A.G,fake,clear=True),patch.dict(os.environ,{'FNV_COFF_WEAK':'1'}):
   self.assertEqual(A.resolve_field(c,unit,[],6,c.symbols[0],0,0,b''),(None,None))
 def test_weak_rejects_name_embedded_class_address(self):
  c=FakeCoff();sym=c.symbols[0]
  with patch.object(A,'_resolve_field_direct',return_value=('b',0x123456)),patch.dict(os.environ,{'FNV_COFF_WEAK':'1'}):
   self.assertEqual(A.resolve_field(c,{},[],6,sym,0,0,b''),(None,None))
 def test_truncated_aux_rejected(self):
  c=FakeCoff();c.data=c.data[:40]
  with self.assertRaises(W.WeakResolutionError): W.resolve_fallback(c,0,c.lookup)
 def test_real_camera_candidate_deferred_library_search(self):
  from compare import Coff
  p=PB/'obj_v3'/'0001.obj'
  if not p.exists():self.skipTest('unit object unavailable')
  c=Coff(p);matches=[i for i,s in c.symbols.items() if s['name'].startswith('??_E?$NiTPrimitiveArray@PAVBGSCameraPath') and s['storage']==105]
  self.assertEqual(len(matches),1)
  with self.assertRaisesRegex(W.WeakResolutionError,'characteristic 2'):W.resolve_fallback(c,matches[0],lambda s:('bad',1))

if __name__=='__main__':unittest.main(verbosity=2)

