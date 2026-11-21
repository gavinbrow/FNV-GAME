import importlib.util
import tempfile
import json
import subprocess
import sys
import unittest
from pathlib import Path

MODULE = Path(__file__).with_name('inventory_symbol_forms.py')
spec = importlib.util.spec_from_file_location('inventory_symbol_forms', MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class InventoryTests(unittest.TestCase):
    def test_names_evidence_and_lexical_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'fixture.cpp'
            path.write_text('''extern int *PTR_0012ABCD, OFF_0012abcd[4];
extern float PTR_0012abcd;
extern struct Unknown _DAT_0012abce;
int x = DAT_0012abcf + PTR_0012ABCD;
// PTR_11111111
/* OFF_22222222
DAT_33333333 */
const char *s = "DAT_44444444";
int prefixDAT_55555555, DAT_66666666_suffix;
''', encoding='utf-8')
            rows = mod.inventory_files([path])
        by_name = {row['name']: row for row in rows}
        self.assertEqual(set(by_name), {'PTR_0012abcd', 'OFF_0012abcd', '_DAT_0012abce', 'DAT_0012abcf'})
        self.assertEqual(by_name['PTR_0012abcd']['references'], 3)
        self.assertEqual(len(by_name['PTR_0012abcd']['declarations']), 2)
        self.assertEqual(by_name['OFF_0012abcd']['declarations'][0]['line'], 1)
        self.assertNotIn('declared_types', by_name['PTR_0012abcd'])

    def test_multiline_evidence_and_ambiguous_constructs(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'fixture.cpp'
            path.write_text("""extern int
    DAT_00001000, /* original comment */
    *PTR_00001004;
extern int DAT_00001008; // original comment
extern struct S {
    int DAT_0000100c;
};
extern int
#if FLAG
    DAT_00001010;
#endif
extern int
    DAT_00001014; int DAT_00001018;
""", encoding='utf-8')
            rows = {row['name']: row for row in mod.inventory_files([path])}
            expected = {'file': str(path), 'line': 1,
                        'text': 'extern int\n    DAT_00001000, /* original comment */\n    *PTR_00001004;'}
            self.assertEqual(rows['DAT_00001000']['declarations'], [expected])
            self.assertEqual(rows['PTR_00001004']['declarations'], [expected])
            self.assertEqual(rows['DAT_00001008']['declarations'][0]['text'],
                             'extern int DAT_00001008; // original comment')
            for name in ('DAT_0000100c', 'DAT_00001010', 'DAT_00001014', 'DAT_00001018'):
                self.assertEqual(rows[name]['declarations'], [])

    def test_cli_file_list_and_deduplication(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'fixture with spaces.cpp'
            source.write_text('extern int PTR_00001000;\n', encoding='utf-8')
            listing = Path(tmp) / 'files.txt'
            listing.write_text(str(source) + '\n', encoding='utf-8')
            output = subprocess.check_output([sys.executable, str(MODULE), '--files-from',
                                              str(listing), str(source)], text=True)
            rows = json.loads(output)['symbols']
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['references'], 1)
            bad = subprocess.run([sys.executable, str(MODULE)], capture_output=True)
            self.assertNotEqual(bad.returncode, 0)

    def test_saved_section_bounds_and_aliases(self):
        rows = [{'address': '0x1000'}, {'address': '0x1000'},
                {'address': '0x1004'}, {'address': '0x1008'}]
        metadata = {'meta': {'sections': [{'name': '.data', 'va': '0x1000',
                                          'raw_end': '0x1004', 'end': '0x1008'}]}}
        mod.annotate_sections(rows, metadata)
        self.assertEqual([r['storage'] for r in rows],
                         ['file_resident', 'file_resident', 'memory_only', 'unmapped'])
        metadata['meta']['sections'].append(metadata['meta']['sections'][0])
        with self.assertRaises(ValueError):
            mod.annotate_sections(rows, metadata)


if __name__ == '__main__':
    unittest.main()
