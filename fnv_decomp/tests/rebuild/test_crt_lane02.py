import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import crt_lane02 as lane
from types import SimpleNamespace
import struct
import json
import tempfile
from unittest.mock import patch

def fake(value=0,peers=1,size=8,relocs=()):
    header=bytearray(60); struct.pack_into('<I',header,40,60)
    symbols={i:dict(name='_memset' if i==0 else 'peer',section=1,type=32,value=value,index=i,storage=2) for i in range(peers)}
    return SimpleNamespace(symbols=symbols,sections={1:dict(index=1,size=size,flags=0x20000000,relocs=relocs)},
        data=bytes(header)+bytes(size),take=lambda raw,n:bytes(n))

class ContractTests(unittest.TestCase):
    def test_complete(self):
        contract,pattern=lane.section_contract(fake(),'_memset')
        self.assertEqual(contract['size'],8); self.assertEqual(contract['fixed_spans'],[(0,8)])
    def test_no_interior(self):
        with self.assertRaises(ValueError): lane.section_contract(fake(value=1),'_memset')
    def test_no_multi_function(self):
        with self.assertRaises(ValueError): lane.section_contract(fake(peers=2),'_memset')
    def test_no_large(self):
        with self.assertRaises(ValueError): lane.section_contract(fake(size=4097),'_memset')
    def test_no_unsupported_field(self):
        with self.assertRaises(ValueError): lane.section_contract(fake(relocs=[(0,0,7)]),'_memset')
    def test_no_overlap(self):
        with self.assertRaises(ValueError): lane.section_contract(fake(relocs=[(0,0,6),(2,0,6)]),'_memset')
    def test_no_outside(self):
        with self.assertRaises(ValueError): lane.section_contract(fake(relocs=[(7,0,6)]),'_memset')
    def test_hypotheses_bounded(self):
        self.assertEqual(len(lane.HYPOTHESES),23)
        self.assertNotIn('0x0043b9d0',lane.HYPOTHESES)
    def test_metadata_output_with_contract_list(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); out=root/'build/rebuild/result.json'; out.parent.mkdir(parents=True)
            args=SimpleNamespace(out=out,mode='contracts',doctor='unused',packet='unused')
            with patch.object(lane.base,'ROOT',root), patch.object(lane,'sources',return_value={}), \
                 patch.object(lane,'prepare',return_value=({'sources':{},'contracts':[]},{},[])):
                lane.run(args)
            self.assertTrue(out.exists())
    def test_contract_span_json_roundtrip(self):
        contract,_=lane.section_contract(fake(),'_memset')
        self.assertEqual(json.loads(json.dumps(contract))['fixed_spans'],[[0,8]])

if __name__=='__main__': unittest.main()
