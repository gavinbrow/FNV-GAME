import tempfile
import unittest
from pathlib import Path

from run_frozen import changed, paths_to_watch, snapshot


class FreezeTests(unittest.TestCase):
    def test_changed_content_and_file_set_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / 'input'
            first.write_text('before', encoding='utf-8')
            before = snapshot([first])
            first.write_text('after', encoding='utf-8')
            self.assertEqual(changed(before, snapshot([first])), [str(first)])
            self.assertEqual(changed(before, {}), [str(first)])

    def test_generated_outputs_and_independent_analysis_are_excluded(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            files = ['runtime-next/build_all.py', 'runtime-next/m3/gen/out.cpp',
                     'runtime-next/m3/out/private/source.cpp',
                     'runtime-next/m3/phase2/new_analysis.py',
                     'runtime-next/m3/phase2/library_overlay.py',
                     'fnv_decomp/src/native.cpp', 'fnv_decomp/build/units.json']
            for relative in files:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('input', encoding='utf-8')
            actual = {p.relative_to(root).as_posix() for p in paths_to_watch(root, [])}
            self.assertEqual(actual, {'runtime-next/build_all.py',
                                      'runtime-next/m3/phase2/library_overlay.py',
                                      'fnv_decomp/src/native.cpp', 'fnv_decomp/build/units.json'})

    def test_explicit_inputs_are_included(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            extra = root / 'candidate.json'
            extra.write_text('{}', encoding='utf-8')
            self.assertIn(extra, paths_to_watch(root, [extra]))


if __name__ == '__main__':
    unittest.main()
