"""Synthetic complete-use literal migration; no compiler or game inputs."""
from pathlib import Path
import struct
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
from coff_inventory import Coff
import literal_symbol_migration as migration


def fixture(label, *, uses=(0,), changed_payload=False, writable=False, pointer=False, value=0, outside=False):
    text=bytes(12 if outside else 8); payload=(b'b' if changed_payload else b'a')+b'\0'*7+b'a'+b'\0'*7
    names=['_function',label,'$SGduplicate']; strings=bytearray(struct.pack('<I',4));symbols=bytearray()
    for i,name in enumerate(names):
        off=len(strings);strings.extend(name.encode()+b'\0')
        symbols.extend(struct.pack('<IIIhHBB',0,off,0 if i==0 else value if i==1 else 8,1 if i==0 else 2,32 if i==0 else 0,2 if i==0 else 3,0))
    struct.pack_into('<I',strings,0,len(strings));refs=b''.join(struct.pack('<IIH',off,1,6) for off in uses);ptrrefs=struct.pack('<IIH',0,0,6) if pointer else b''
    raw=100;rel=raw+len(text);rdata=rel+len(refs);rrel=rdata+len(payload);symptr=rrel+len(ptrrefs)
    return (struct.pack('<HHIIIHH',0x14c,2,0,symptr,3,0,0)+
        struct.pack('<8sIIIIIIHHI',b'.text',0,0,len(text),raw,rel,0,len(uses),0,0x60000020)+
        struct.pack('<8sIIIIIIHHI',b'.rdata',0,0,len(payload),rdata,rrel,0,int(pointer),0,0xc0000040 if writable else 0x40000040)+
        text+refs+payload+ptrrefs+symbols+strings)


class Image:
    base=0x400000
    def section(self,rva,size):return dict(flags=0x40000040)
    def read_rva(self,rva,size,allow_code=False):
        if rva in (0x1000,0x1004,0x1008):return struct.pack('<I',0x600000)[:size]
        if rva==0x200000:return (b'a'+b'\0'*7)[:size]
        raise ValueError('unexpected synthetic image range')


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.recipe=dict(source='fixture.cpp',compiler='sp1',flags=['/Od'],functions=[dict(address='0x00401000',symbol='_function',size=8)],symbols={'$SGold':'0x00600000'})

    def run_case(self, old=None, new=None, *, recipe=None, highlows=(), image=None):
        with tempfile.TemporaryDirectory() as td:
            before,after=Path(td)/'before.obj',Path(td)/'after.obj'
            before.write_bytes(old or fixture('$SG100'));after.write_bytes(new or fixture('$SG102'))
            r=recipe or dict(self.recipe,symbols={'$SG100':'0x00600000'})
            return migration.supplement(Coff(before),Coff(after),r,image or Image(),highlows)

    def test_full_payload_all_fields_original_binding_and_no_recipe_mutation(self):
        r=dict(self.recipe,symbols={'$SG100':'0x00600000'})
        adapted,proof=self.run_case(old=fixture('$SG100',uses=(0,4)),new=fixture('$SG900',uses=(0,4)),recipe=r)
        self.assertEqual(adapted['symbols']['$SG900'],'0x00600000')
        self.assertNotIn('$SG900',r['symbols'])
        self.assertEqual(len(proof['witnesses'][0]['all_physical_uses']),2)
        self.assertEqual(proof['witnesses'][0]['old_literal']['extent'],8)

    def test_duplicate_equal_payload_requires_field_provenance_not_nearest_bytes(self):
        _,proof=self.run_case()
        self.assertTrue(proof['witnesses'][0]['complete_bijective_field_provenance'])
        for new in (fixture('$SG102',uses=(0,4)),fixture('$SG102',value=8)):
            with self.assertRaises(ValueError):self.run_case(new=new)

    def test_payload_writable_pointer_container_or_original_highlow_rejected(self):
        for new in (fixture('$SG102',changed_payload=True),fixture('$SG102',writable=True),fixture('$SG102',pointer=True)):
            with self.assertRaises(ValueError):self.run_case(new=new)
        with self.assertRaises(ValueError):self.run_case(highlows=[0x600002])

    def test_original_full_payload_and_field_target_must_match(self):
        class BadPayload(Image):
            def read_rva(self,rva,size,allow_code=False):return b'X'*size if rva==0x200000 else super().read_rva(rva,size,allow_code)
        class BadField(Image):
            def read_rva(self,rva,size,allow_code=False):return struct.pack('<I',0x600004) if rva==0x1000 else super().read_rva(rva,size,allow_code)
        for image in (BadPayload(),BadField()):
            with self.assertRaises(ValueError):self.run_case(image=image)

    def test_missing_origin_or_unowned_physical_use_rejected(self):
        with self.assertRaises(ValueError):self.run_case(recipe=self.recipe)
        with self.assertRaises(ValueError):self.run_case(old=fixture('$SG100',uses=(0,8),outside=True),new=fixture('$SG102',uses=(0,8),outside=True))


if __name__=='__main__':unittest.main()
