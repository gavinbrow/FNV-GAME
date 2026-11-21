import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import tescontainer_install as transaction


class TransactionTests(unittest.TestCase):
    def test_recipe_unit_replacement_preserves_other_units_and_metadata(self):
        raw = b'{"totals":{"units":2},"units":[{"source":"first"}, {"source":"second"}],"tail":7}'
        actual = transaction.replace_unit(raw, 1, {'source': 'replacement'})
        self.assertEqual(json.loads(actual), {'totals': {'units': 2}, 'units': [
            {'source': 'first'}, {'source': 'replacement'}], 'tail': 7})
        self.assertTrue(actual.startswith(raw[:raw.index(b'{"source":"second"}')]))

    def run_fixture(self, temporary, changed=False, locked=False, marker_failure=False, interrupted=False):
        root = Path(temporary)
        fn = root / 'source-tree'
        output = root / 'private-transaction'
        pilot = root / 'private-pilot'
        fn.mkdir()
        output.mkdir()
        pilot.mkdir()
        (root / 'runtime-next').mkdir()
        path = fn / 'input.h'
        path.write_bytes(b'old')
        (output / 'original').write_bytes(b'old')
        (output / 'generated').write_bytes(b'new')
        evidence = pilot / 'comparison-v2.json'
        evidence.write_text('{}', encoding='utf-8')
        manifest = dict(evidence_sha256=transaction.experiment.digest(evidence), files=[dict(
            path='input.h', old_sha256=transaction.sha(b'old'), new_sha256=transaction.sha(b'new'),
            original='original', generated='generated')])
        (output / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        if changed:
            path.write_bytes(b'another contributor')
        if locked:
            (root / 'runtime-next/build.lock').write_text('live lane', encoding='utf-8')
        with patch.object(transaction, 'PROJECT', root), patch.object(transaction, 'FN', fn), \
                patch.object(transaction, 'OUT', output), patch.object(transaction, 'PILOT', pilot):
            if changed or locked:
                before = path.read_bytes()
                with self.assertRaises(ValueError):
                    transaction.install()
                self.assertEqual(path.read_bytes(), before)
            elif marker_failure:
                with patch.object(transaction.json, 'dump', side_effect=OSError('synthetic marker write failure')):
                    with self.assertRaises(OSError):
                        transaction.install()
                self.assertEqual(path.read_bytes(), b'old')
                self.assertFalse((output / 'applied.json').exists())
            elif interrupted:
                path.write_bytes(b'new')
                stale = output / 'input.h.phase2-interrupted'
                stale.write_bytes(b'partial private temporary file')
                transaction.install(True, True)
                self.assertEqual(path.read_bytes(), b'old')
                self.assertTrue((output / 'recovered.json').exists())
                self.assertEqual(stale.read_bytes(), b'partial private temporary file')
            else:
                transaction.install()
                self.assertEqual(path.read_bytes(), b'new')
                transaction.install(True)
                self.assertEqual(path.read_bytes(), b'old')

    def test_apply_restore_exact_payload(self):
        with tempfile.TemporaryDirectory() as temporary:
            self.run_fixture(temporary)

    def test_other_contributor_change_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            self.run_fixture(temporary, changed=True)

    def test_locked_build_lane_refused(self):
        with tempfile.TemporaryDirectory() as temporary:
            self.run_fixture(temporary, locked=True)

    def test_marker_failure_rolls_back_protected_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            self.run_fixture(temporary, marker_failure=True)

    def test_interrupted_install_can_recover_without_marker(self):
        with tempfile.TemporaryDirectory() as temporary:
            self.run_fixture(temporary, interrupted=True)


if __name__ == '__main__':
    unittest.main()
