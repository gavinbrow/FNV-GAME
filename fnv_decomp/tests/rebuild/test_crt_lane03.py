"""Synthetic relocation accounting; no private inputs."""
import importlib.util
from pathlib import Path
import struct
import sys
import unittest

TOOLS=Path(__file__).resolve().parents[2]/'tools/rebuild'
sys.path.insert(0,str(TOOLS))
import crt_lane03 as lane

class CompareTests(unittest.TestCase):
    def row(self,relocs):
        return dict(target='0x00100000',relocations=relocs)
    def reloc(self,offset=1,kind=20):
        return dict(offset=offset,kind=kind,symbol=dict(name='_synthetic'))
    def test_rel32_signed_addend(self):
        data=b'A'+struct.pack('<i',-4)+b'Z'
        original=b'A'+struct.pack('<i',0x200-5-4)+b'Z'
        r=lane.compare(data,original,self.row([self.reloc()]))
        self.assertTrue(r['all_nonrelocation_bytes_equal'])
        self.assertEqual(r['relocations'][0]['observed_destination'],'0x00100200')
        self.assertFalse(r['relocation_identity_verified'])
        self.assertFalse(r['ABI_verified'])
    def test_dir32_addend(self):
        r=lane.compare(b'A'+struct.pack('<I',8),b'A'+struct.pack('<I',0x12340008),
                       self.row([self.reloc(kind=6)]))
        self.assertEqual(r['relocations'][0]['observed_destination'],'0x12340000')
    def test_mismatch_not_hidden(self):
        r=lane.compare(b'ABC',b'AXC',self.row([]))
        self.assertEqual(r['nonrelocation_mismatch_count'],1)
        self.assertFalse(r['all_nonrelocation_bytes_equal'])
    def test_overlap_rejected(self):
        with self.assertRaises(ValueError):lane.compare(bytes(8),bytes(8),self.row([self.reloc(),self.reloc(2)]))
    def test_unknown_kind_rejected(self):
        with self.assertRaises(ValueError):lane.compare(bytes(8),bytes(8),self.row([self.reloc(kind=7)]))
    def test_outside_rejected(self):
        with self.assertRaises(ValueError):lane.compare(bytes(4),bytes(4),self.row([self.reloc()]))
    def test_span_limit(self):
        with self.assertRaises(ValueError):lane.compare(bytes(4097),bytes(4097),self.row([]))
    def test_single_entry_gate(self):
        s=dict(value=0,type=32,storage=2)
        section=dict(data=bytes(16),flags=0x20000000)
        self.assertTrue(lane.eligible(s,section,[s,s]))
        self.assertFalse(lane.eligible(s,section,[s,dict(value=8,type=32)]))
        self.assertFalse(lane.eligible(s,dict(data=bytes(16),flags=0),[s]))

if __name__=='__main__':unittest.main()
