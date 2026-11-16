"""Synthetic local LABEL proof, isolated from string-literal resolver aliases."""
from pathlib import Path
import hashlib
import struct
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
from coff_inventory import Coff
import local_label_symbol_migration as labels
import runtime_overlay_inputs_v2 as registry

SOURCE=b'// @fnv 0x00401000\r\nvoid f()\r\n{\r\n    goto finished;\r\nfinished:\r\n    return;\r\n}\r\n'
SPEC=dict(function_address='0x00401000',function_symbol='_f',function_size=16,source_label='finished',
          old_name='$finished$1',new_name='$finished$900',source_span_sha256=hashlib.sha256(SOURCE).hexdigest(),
          physical_use_count=1,field_offsets=[8])


def fixture(name, *, value=4, section=1, storage=6, use_offsets=(8,), other='other', parent_change=False):
    payload=bytearray(b'\x90'*16);struct.pack_into('<I',payload,0,0)
    for off in use_offsets:struct.pack_into('<I',payload,off,0)
    if parent_change:payload[-1] ^= 1
    records=bytearray();strings=bytearray(struct.pack('<I',4));names=['_f',name,other]
    for i,n in enumerate(names):
        off=len(strings);strings.extend(n.encode()+b'\0');records.extend(struct.pack('<IIIhHBB',0,off,0 if i!=1 else value,1 if i==0 else section if i==1 else 0,32 if i==0 else 0,2 if i!=1 else storage,0))
    struct.pack_into('<I',strings,0,len(strings));rels=[(0,2,20)]+[(off,1,6) for off in use_offsets]
    count=max(1,section);start=20+count*40;data=payload+b''.join(struct.pack('<IIH',*r) for r in rels)
    headers=[struct.pack('<8sIIIIIIHHI',b'.text',0,0,16,start,start+16,0,len(rels),0,0x60000020)]
    for i in range(2,count+1):headers.append(struct.pack('<8sIIIIIIHHI',b'.text',0,0,0,0,0,0,0,0,0x60000020))
    return struct.pack('<HHIIIHH',0x14c,count,0,start+len(data),3,0,0)+b''.join(headers)+data+records+strings


class Image:
    base=0x400000
    def read_rva(self,rva,size,allow_code=False):return struct.pack('<I',0x401004)


class LabelTests(unittest.TestCase):
    def prove(self, old=None,new=None,**kwargs):
        with tempfile.TemporaryDirectory() as td:
            a,b=Path(td)/'old.obj',Path(td)/'new.obj';a.write_bytes(old or fixture('$finished$1'));b.write_bytes(new or fixture('$finished$900'))
            return labels.prove(Coff(a),Coff(b),dict(functions=[dict(address='0x00401000',symbol='_f',size=16)]),
                SOURCE,kwargs.get('source',SOURCE),kwargs.get('image',Image()),kwargs.get('highlows',[0x401008]),[SPEC])

    def test_positive_exact_source_parent_and_complete_use_proof(self):
        proof=self.prove();w=proof['witnesses'][0]
        self.assertEqual(w['new_name'],'$finished$900')
        self.assertTrue(w['all_other_parent_relocation_facts_equal'])
        self.assertEqual(w['complete_parent_relocation_count'],2)
        self.assertTrue(proof['resolver_recipe_unchanged'])

    def test_cross_parent_changed_value_global_or_extra_use_rejected(self):
        for new in [fixture('$finished$900',section=2),fixture('$finished$900',value=8),fixture('$finished$900',storage=2),fixture('$finished$900',use_offsets=(8,12))]:
            with self.assertRaises(ValueError):self.prove(new=new)

    def test_changed_source_parent_payload_or_other_relocation_rejected(self):
        for new in [fixture('$finished$900',parent_change=True),fixture('$finished$900',other='wrong-other')]:
            with self.assertRaises(ValueError):self.prove(new=new)
        with self.assertRaises(ValueError):self.prove(source=SOURCE+b'// changed\r\n')

    def test_original_highlow_and_exact_interior_target_required(self):
        with self.assertRaises(ValueError):self.prove(highlows=[])
        class Wrong(Image):
            def read_rva(self,*args,**kwargs):return struct.pack('<I',0x401005)
        with self.assertRaises(ValueError):self.prove(image=Wrong())

    def test_proven_local_name_normalizes_only_name_not_storage_or_addend(self):
        def ref(name):return dict(semantic=dict(offset=8,kind=6,addend=0,target=dict(name=name,section=1,value=4,storage=6,type=0,aux_count=0)))
        registry.normalize_fields([ref('$finished$1')],[ref('$finished$900')],[],{'$finished$900':'$finished$1'})
        with self.assertRaises(ValueError):registry.normalize_fields([ref('$finished$1')],[ref('$finished$900')],[],{})


if __name__=='__main__':unittest.main()
