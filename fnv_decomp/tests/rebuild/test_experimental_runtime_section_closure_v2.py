from pathlib import Path
import hashlib
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools/rebuild'))
from test_coff_code_archive import section, symbol, aux, object_bytes
import coff_code_archive as coff
import experimental_runtime_section_closure_v2 as closure


def fixture(directive=b' /DEFAULTLIB:"LIBCMT" ', weak=False):
    # Deliberately place an unused section before the root to force index remapping.
    sections = [section('.data', b'x'), section('.text', b'1234', relocs=[(0,13,20)]),
        section('.text$x', b'eh', flags=0x60501020), section('.CRT$XCU', b'abcd', flags=0x40300040, relocs=[(0,4,6)]),
        section('.sxdata', struct.pack('<I',7), flags=0x00300200), section('.drectve', directive, flags=0x00100a00)]
    symbols = [symbol('.data',1,storage=3,auxiliary=aux(1)),
        symbol('.text',2,storage=3,auxiliary=aux(4,1)), symbol('_root',2,typ=32),
        symbol('.text$x',3,storage=3,auxiliary=aux(2,selection=5,association=2)), symbol('_handler',3,typ=32,storage=3),
        symbol('.CRT$XCU',4,storage=3,auxiliary=aux(4,1,selection=0)), symbol('_initializer',4),
        symbol('.sxdata',5,storage=3,auxiliary=struct.pack('<IHHIhBBH',4,0,0,0x12345678,0,0,0,0)), symbol('_outside',0,typ=32),
        symbol('.drectve',6,storage=3,auxiliary=aux(len(directive),selection=0))]
    if weak:
        symbols.append(symbol('_weak',0,storage=105,auxiliary=b'\0'*18))
    return object_bytes(sections,symbols)


class RuntimeSectionClosure(unittest.TestCase):
    def run_fixture(self, raw):
        return closure.project(raw,4,hashlib.sha256(raw).hexdigest())

    def test_initializer_association_relocation_and_safeseh_survive(self):
        raw=fixture(); out, receipt=self.run_fixture(raw); old=coff.parse(raw); new=coff.parse(out)
        self.assertNotIn(1,receipt['retained_sections'])
        self.assertEqual(set(receipt['retained_sections']),{2,3,4,5,6})
        sm,ym=receipt['section_map'],receipt['symbol_map']
        self.assertEqual(new['sections'][sm[2]]['relocs'],[(0,ym[13],20)])
        self.assertEqual(new['sections'][sm[4]]['relocs'],[(0,ym[4],6)])
        self.assertEqual(struct.unpack('<I',new['sections'][sm[5]]['payload']), (ym[7],))
        self.assertEqual(struct.unpack_from('<I',new['symbols'][ym[11]]['aux'],8)[0],0)
        self.assertEqual(new['sections'][sm[6]]['payload'],old['sections'][6]['payload'])
        self.assertEqual(struct.unpack_from('<h',new['symbols'][ym[5]]['aux'],12)[0],sm[2])
        self.assertFalse(receipt['application_initializer_closure_proved'])

    def test_unknown_directive_and_weak_external_fail_closed(self):
        with self.assertRaisesRegex(ValueError,'DIRECTIVE_OPERATION_UNSUPPORTED'):
            self.run_fixture(fixture(b' /INCLUDE:_other '))
        with self.assertRaisesRegex(ValueError,'WEAK_EXTERNAL_UNSUPPORTED'):
            self.run_fixture(fixture(weak=True))

    def test_identity_and_corrupt_safeseh_rejected(self):
        raw=fixture()
        with self.assertRaisesRegex(ValueError,'identity'):
            closure.project(raw,4,'0'*64)
        raw=bytearray(raw); obj=coff.parse(bytes(raw)); sec=5
        offset=struct.unpack_from('<I',raw,20+40*(sec-1)+20)[0]
        struct.pack_into('<I',raw,offset,9999)
        with self.assertRaisesRegex(ValueError,'SAFESEH_ABSENT_SYMBOL'):
            self.run_fixture(bytes(raw))

    def test_noncomdat_is_retained_and_unknown_section_rejected(self):
        raw = fixture()
        obj = coff.parse(raw)
        # Turn the otherwise unreachable first section into ordinary non-COMDAT.
        changed = bytearray(raw)
        struct.pack_into('<I', changed, 20+36, 0x40300040)
        aux_offset = obj['symbol_pointer'] + 18
        changed[aux_offset+14] = 0
        output, receipt = self.run_fixture(bytes(changed))
        self.assertIn(1, receipt['retained_sections'])
        self.assertEqual(coff.parse(output)['sections'][receipt['section_map'][1]]['payload'], b'x')
        # An unrecognized ordinary section cannot be silently discarded.
        changed[20:28] = b'.mystery'
        changed[obj['symbol_pointer']:obj['symbol_pointer']+8] = b'.mystery'
        with self.assertRaisesRegex(ValueError, 'UNKNOWN_SECTION_METADATA'):
            self.run_fixture(bytes(changed))

    def test_missing_section_definition_and_comdat_mismatch_rejected(self):
        raw = fixture(); obj = coff.parse(raw)
        changed = bytearray(raw)
        # Remove first section definition's auxiliary count; the resulting malformed
        # symbol stream must be rejected rather than interpreted as an omitted root.
        changed[obj['symbol_pointer'] + 17] = 0
        with self.assertRaises((ValueError, UnicodeDecodeError)):
            self.run_fixture(bytes(changed))
        changed = bytearray(raw)
        struct.pack_into('<I', changed, 20+36, 0x40300040)
        with self.assertRaisesRegex(ValueError, 'COMDAT_FLAG_SELECTION_MISMATCH'):
            self.run_fixture(bytes(changed))


if __name__=='__main__': unittest.main()
