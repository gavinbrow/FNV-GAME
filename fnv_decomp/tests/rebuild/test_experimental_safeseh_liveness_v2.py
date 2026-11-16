from pathlib import Path
import hashlib
import struct
import sys
import unittest
import zlib
sys.path.insert(0,str(Path(__file__).resolve().parent))
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
from test_coff_code_archive import section,symbol,aux,object_bytes
import experimental_safeseh_liveness_v2 as live


def fixture():
    handler=struct.pack('<I',8);checksum=zlib.crc32(handler,0xffffffff)^0xffffffff
    directive=b' /DEFAULTLIB:"LIBCMT" '
    sections=[section('.text',b'root'),section('.text',b'body'),
              section('.text$x',b'handler'),section('.sxdata',handler,flags=0x00300200),
              section('.drectve',directive,flags=0x00100a00)]
    symbols=[symbol('.text',1,storage=3,auxiliary=aux(4)),symbol('_root',1,typ=32),
             symbol('.text',2,storage=3,auxiliary=aux(4)),symbol('_other',2,typ=32),
             symbol('.text$x',3,storage=3,auxiliary=aux(7,selection=5,association=2)),symbol('_handler',3,typ=32,storage=3),
             symbol('.sxdata',4,storage=3,auxiliary=struct.pack('<IHHIhBBH',4,0,0,checksum,0,0,0,0)),
             symbol('.drectve',5,storage=3,auxiliary=aux(len(directive),selection=0))]
    return object_bytes(sections,symbols)


class SafesehLiveness(unittest.TestCase):
    def test_unreferenced_parent_is_candidate_only(self):
        raw=fixture();r=live.analyze(raw,2,hashlib.sha256(raw).hexdigest(),[])
        self.assertEqual((r['full_sections'],r['candidate_sections'],r['handler_count'],r['retained_handler_count']),(5,3,1,0))
        self.assertFalse(r['omission_approved']);self.assertFalse(r['archive_demands_proved'])

    def test_cross_object_demand_preserves_parent_and_handler(self):
        raw=fixture();r=live.analyze(raw,2,hashlib.sha256(raw).hexdigest(),['_other'])
        self.assertEqual((r['candidate_sections'],r['retained_handler_count']),(5,1))
        self.assertEqual(r['handlers'][0]['parent_section'],2)

    def test_changed_input_rejected(self):
        with self.assertRaisesRegex(ValueError,'object identity'):
            live.analyze(fixture(),2,'0'*64,[])

if __name__=='__main__':unittest.main()
