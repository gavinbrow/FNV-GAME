"""Synthetic COFF record chains with broken references and relocation layouts."""
import struct
import unittest

from class_metadata_compare import ObjectRecords
from native_class_inventory import InvalidRecord


class FakeCoff:
    def __init__(self):
        self.data = bytearray(176)
        struct.pack_into('<IIII', self.data, 64, 0, 0, 1, 0)
        struct.pack_into('<IIiiiII', self.data, 100, 0, 0, 0, -1, 0, 0x40, 0)
        self.data[8:23] = b'.?AVInvented@@\0'
        self.symbols = {
            0: dict(name='??_7type_info@@6B@', section=0, value=0),
            1: dict(name='td', section=1, value=0),
            2: dict(name='chd', section=1, value=64),
            3: dict(name='array', section=1, value=80),
            4: dict(name='bcd', section=1, value=100),
            5: dict(name='col', section=1, value=140),
            6: dict(name='??_7Invented@@6B@', section=1, value=164),
            7: dict(name='virtualMethod', section=0, value=0),
        }
        self.by_name = {s['name']: [s] for s in self.symbols.values()}
        self.sections = [None, dict(data=self.data, relocs=[
            (0, 0, 6), (76, 3, 6), (80, 4, 6), (100, 1, 6), (124, 2, 6),
            (152, 1, 6), (156, 2, 6), (160, 5, 6),
            (164, 7, 6), (168, 7, 6), (172, 7, 6)])]

    def named(self, name):
        hits = [s for s in self.by_name.get(name, []) if s['section'] > 0]
        if len(hits) != 1:
            raise ValueError('expected one definition')
        return hits[0]


class ObjectRecordTests(unittest.TestCase):
    def test_full_synthetic_graph_and_slots(self):
        tables = ObjectRecords(FakeCoff()).tables('.?AVInvented@@')
        self.assertEqual(len(tables), 1)
        self.assertEqual(len(tables[0]['slots']), 3)
        graph = tables[0]['locator']['graph']
        self.assertEqual(graph['bases'][0]['type_name'], '.?AVInvented@@')
        self.assertEqual(graph['bases'][0]['pmd'], [0, -1, 0])

    def test_missing_and_wrong_kind_relocation(self):
        for rows in ([], [(0, 0, 20)]):
            coff = FakeCoff()
            coff.sections[1]['relocs'] = rows
            with self.subTest(rows=rows), self.assertRaises(InvalidRecord):
                ObjectRecords(coff).type_name((1, 0))

    def test_overlapping_relocation_rejected(self):
        coff = FakeCoff()
        coff.sections[1]['relocs'].append((2, 0, 6))
        with self.assertRaises(InvalidRecord):
            ObjectRecords(coff).type_name((1, 0))

    def test_unexpected_relocation_in_scalar_field(self):
        coff = FakeCoff()
        coff.sections[1]['relocs'].append((104, 1, 6))
        with self.assertRaises(InvalidRecord):
            ObjectRecords(coff).hierarchy((1, 64))

    def test_local_metadata_target_must_be_defined_unambiguously(self):
        coff = FakeCoff()
        coff.symbols[4]['section'] = 0
        with self.assertRaises(InvalidRecord):
            ObjectRecords(coff).hierarchy((1, 64))

    def test_metadata_target_addend_cannot_escape_section(self):
        coff = FakeCoff()
        struct.pack_into('<I', coff.data, 80, 512)
        with self.assertRaises(InvalidRecord):
            ObjectRecords(coff).hierarchy((1, 64))

    def test_table_type_filter_does_not_admit_other_class(self):
        self.assertEqual(ObjectRecords(FakeCoff()).tables('.?AVOtherInvented@@'), [])


if __name__ == '__main__':
    unittest.main()
