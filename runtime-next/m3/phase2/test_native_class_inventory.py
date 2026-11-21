"""Synthetic malformed-record and hierarchy-boundary checks; no game inputs."""
import struct
import unittest

from native_class_inventory import InvalidRecord, Records


class RecordValidationTests(unittest.TestCase):
    def setUp(self):
        self.image = bytearray(1024)
        self.sections = {
            '.rdata': dict(va=0x1000, raw=256, off=0),
            '.data': dict(va=0x2000, raw=256, off=256),
            '.text': dict(va=0x3000, raw=256, off=512),
        }

    def reader(self, relocations=()):
        return Records(bytes(self.image), self.sections, relocations)

    def test_file_backing_not_virtual_extent(self):
        with self.assertRaises(InvalidRecord):
            self.reader().read(0x10fe, 4)

    def test_pointer_requires_relocation(self):
        with self.assertRaises(InvalidRecord):
            self.reader().pointer(0x1000)

    def test_name_requires_class_header_and_terminator(self):
        struct.pack_into('<II', self.image, 256, 0x1000, 0)
        name = b'.?AVInvented@@\0'
        self.image[264:264 + len(name)] = name
        self.assertEqual(self.reader([0x2000]).type_name(0x2000), '.?AVInvented@@')
        struct.pack_into('<I', self.image, 260, 1)
        with self.assertRaises(InvalidRecord):
            self.reader([0x2000]).type_name(0x2000)

    def test_preorder_nested_and_sibling_subtrees(self):
        self.assertEqual(Records.preorder_parents([6, 4, 1, 0, 0, 0, 0]),
                         [None, 0, 1, 2, 1, 1, 0])

    def test_preorder_rejects_crossing_subtrees(self):
        with self.assertRaises(InvalidRecord):
            Records.preorder_parents([4, 1, 2, 0, 0])

    def test_preorder_rejects_disconnected_and_out_of_range(self):
        for counts in ([], [0, 0], [1, 1], [1, -1]):
            with self.subTest(counts=counts), self.assertRaises(InvalidRecord):
                Records.preorder_parents(counts)

    def test_code_prefix_stops_at_noncode_and_unrelocated_cells(self):
        struct.pack_into('<III', self.image, 0, 0x3000, 0x3004, 0x2000)
        self.assertEqual(self.reader([0x1000, 0x1004, 0x1008]).code_pointer_prefix(0x1000),
                         [0x3000, 0x3004])
        self.assertEqual(self.reader([0x1000, 0x1008]).code_pointer_prefix(0x1000), [0x3000])


if __name__ == '__main__':
    unittest.main()
