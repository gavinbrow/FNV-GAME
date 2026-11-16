"""Invented COFF payloads and temporary files only."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools/rebuild'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import readonly_section_name_successor as successor
import data_arena_alias_projection as alias
from test_data_arena_alias_projection import fixture


class SuccessorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.input = self.root / 'input'
        self.input.mkdir()
        _, _, rows, payloads = fixture()
        self.inputs = []
        objects = []
        self.originals = []
        for row, payload in zip(rows, payloads):
            fragment = row['fragment']
            data = alias.alias_object(fragment, row['aliases'], payload)
            ident = fragment['fragment_id']
            (self.input / (ident + '.obj')).write_bytes(data)
            self.inputs.append((ident, successor.digest(data), len(payload), len(row['aliases']) + 2))
            objects.append(dict(fragment_id=ident, object_sha256=successor.digest(data)))
            self.originals.append(data)
        receipt = dict(kind='private-entry-raw-alias-projection', initialized_bytes=446, aliases=16,
                       entry_fields=20, relocations=0, objects=objects)
        raw = json.dumps(receipt).encode()
        (self.input / 'projection.json').write_bytes(raw)
        self.receipt_sha = successor.digest(raw)
        self.review = self.root / 'review.json'
        self.review.write_text(json.dumps(dict(kind='readonly-section-name-successor-review', approved=True,
            root_authorized=True, reviewer='synthetic reviewer', source_sha256=successor.digest(Path(successor.__file__).read_bytes()),
            input_receipt_sha256=self.receipt_sha)))
        self.output = self.root / 'output'
        self.patch_inputs = patch.object(successor, 'INPUTS', tuple(self.inputs))
        self.patch_receipt = patch.object(successor, 'RECEIPT_SHA', self.receipt_sha)
        self.patch_inputs.start(); self.addCleanup(self.patch_inputs.stop)
        self.patch_receipt.start(); self.addCleanup(self.patch_receipt.stop)

    def run_project(self):
        return successor.project(self.input, self.review, self.output)

    def test_exact_name_only_and_receipt(self):
        report = self.run_project()
        for original, record in zip(self.originals, report['objects']):
            output = (self.output / (record['fragment_id'] + '.obj')).read_bytes()
            self.assertEqual(output[:20], original[:20])
            self.assertEqual(output[20:28], b'.rdata\0\0')
            self.assertEqual(output[28:], original[28:])
            self.assertEqual(record['output_sha256'], successor.digest(output))
        self.assertEqual((report['aliases'], report['entry_fields'], report['relocations']), (16, 20, 0))
        with self.assertRaises(ValueError): self.run_project()

    def test_bad_shapes_rejected(self):
        data = self.originals[0]
        for offset in (0, 2, 12, 16, 20, 36, 40, 44, 48, 52, 54, 56):
            changed = bytearray(data); changed[offset] ^= 1
            with self.subTest(offset=offset), self.assertRaises(ValueError):
                successor.transform(bytes(changed), 219, 11)
        with self.assertRaises(ValueError): successor.transform(data[:59], 219, 11)

    def test_no_review_or_tampered_inputs_no_output(self):
        self.review.write_text('{}')
        with self.assertRaises(ValueError): self.run_project()
        self.assertFalse(self.output.exists())
        review = dict(kind='readonly-section-name-successor-review', approved=True, root_authorized=True,
            reviewer='reviewer', source_sha256=successor.digest(Path(successor.__file__).read_bytes()), input_receipt_sha256=self.receipt_sha)
        self.review.write_text(json.dumps(review))
        path = self.input / (self.inputs[0][0] + '.obj')
        path.write_bytes(self.originals[0] + b'x')
        with self.assertRaises(ValueError): self.run_project()
        self.assertFalse(self.output.exists())

    def test_input_overlap_rejected(self):
        with self.assertRaises(ValueError): successor.project(self.input, self.review, self.input / 'new')
        self.assertFalse((self.input / 'new').exists())

    def test_late_drift_removes_only_new_outputs(self):
        original_transform = successor.transform
        def tamper(*args):
            result = original_transform(*args)
            self.review.write_text('{}')
            return result
        with patch.object(successor, 'transform', side_effect=tamper):
            with self.assertRaises(ValueError): self.run_project()
        self.assertFalse(self.output.exists())
        self.assertTrue((self.input / 'projection.json').exists())


if __name__ == '__main__': unittest.main()
