import unittest

from vptr_write_inventory import scan_source


class LeadTests(unittest.TestCase):
    def test_assignment_inside_annotated_function(self):
        source = '// @fnv 0x00401000\nvoid Ctor() { self->table = &DAT_01002000; }'
        rows = scan_source(source, {0x01002000})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['annotated_function_address'], '0x00401000')
        self.assertFalse(rows[0]['destination_is_object_vptr_proven'])

    def test_comments_strings_and_comparisons_are_not_assignments(self):
        source = 'void f() { /* x = DAT_01002000 */ const char* p="x=DAT_01002000"; if (x == DAT_01002000) {} }'
        self.assertEqual(scan_source(source, {0x01002000}), [])

    def test_inline_assembly_and_unknown_address(self):
        rows = scan_source('__asm {\n mov [ecx], offset DAT_01002000\n}', {0x01002000})
        self.assertEqual(rows[0]['syntax'], 'inline_assembly_reference_to_vtable')
        self.assertEqual(scan_source('x = DAT_01002000;', set()), [])


if __name__ == '__main__':
    unittest.main()
