import contextlib
import importlib.util
import io
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location('export_repo', pathlib.Path(__file__).with_name('export_repo.py'))
export_repo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(export_repo)


class ExportTests(unittest.TestCase):
    def test_private_and_generated_inputs_are_excluded(self):
        for path in (
            'runtime-next/build-v7/contrib_pieces.json',
            'runtime-next/layout-v2/snapshot/contrib_pieces.json',
            'runtime-next/layout-v2/build/image_G.json',
            'runtime-next/m3/out/private/capture.json',
            'runtime-next/m3/gen/m3_data.cpp',
            'runtime-next/m3/phase2/MCP-CONNECTION-20261119.md',
            'runtime-next/m3/phase2/promotion-staged-v5/selection.json',
            'runtime-next/m3/phase2/accepted_range_partition.before-native-source.json',
        ):
            with self.subTest(path=path):
                self.assertTrue(export_repo.banned(path))
        self.assertFalse(export_repo.banned('fnv_decomp/src/generated/m3_typeid_bulk_0001.cpp'))
        self.assertFalse(export_repo.banned('runtime-next/m3/phase2/selection.json'))

    def test_json_workspace_scrubbing_preserves_json_escaping(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / 'proof.json'
            path.write_text(json.dumps({'path': r'C:\Projects\Decompilation\private\proof'}), encoding='utf-8')
            result = export_repo.scrubbed(str(path))
            self.assertEqual(json.loads(result)['path'], r'C:\path\to\Decompilation\private\proof')

    def test_python_workspace_scrubbing_preserves_literal(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / 'paths.py'
            path.write_bytes(b"ROOT = r'C:\\Projects\\Decompilation'\n")
            result = export_repo.scrubbed(str(path))
            self.assertEqual(result, b"ROOT = r'C:\\path\\to\\Decompilation'\n")
            compile(result, str(path), 'exec')

    def test_export_uses_content_even_when_destination_looks_newer(self):
        import os
        with tempfile.TemporaryDirectory() as temp:
            source = pathlib.Path(temp) / 'source'
            target = pathlib.Path(temp) / 'target'
            relative = 'fnv_decomp/README.md'
            (source / 'fnv_decomp').mkdir(parents=True)
            (target / 'fnv_decomp').mkdir(parents=True)
            (source / relative).write_bytes(b'new content\n')
            (target / relative).write_bytes(b'old content\n')
            os.utime(target / relative, (2_000_000_000, 2_000_000_000))
            with patch.object(export_repo, 'HERE', str(target)), patch.object(export_repo, 'PROJ', str(source)), \
                 patch.object(export_repo, 'DRY', False), patch.object(export_repo, 'fnv_decomp_files', return_value=[relative]), \
                 patch.object(export_repo, 'runtime_files', return_value=[]), patch.object(export_repo, 'extra_files', return_value=[]), \
                 contextlib.redirect_stdout(io.StringIO()):
                export_repo.main()
            self.assertEqual((target / relative).read_bytes(), b'new content\n')


if __name__ == '__main__':
    unittest.main()
