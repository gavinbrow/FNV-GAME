"""Synthetic full-output receipt publication checks."""
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/rebuild'))
from v14_factory_output_publication import publish_complete as _publish_complete

def publish_complete(*args, **kwargs):
    kwargs.setdefault('summary', {'requested': 1, 'emitted': 1, 'blocked': 0})
    return _publish_complete(*args, **kwargs)


def sha(b): return hashlib.sha256(b).hexdigest()


class OutputPublicationTests(unittest.TestCase):
    def make(self, parent):
        root = Path(parent) / 'stage'; root.mkdir()
        (root / 'nested').mkdir()
        (root / 'nested' / 'member.obj').write_bytes(b'object')
        journal = (root / 'progress.jsonl').open('wb')
        journal.write(b'done\n'); journal.close()
        return root, journal, {'nested/member.obj': sha(b'object'), 'progress.jsonl': sha(b'done\n')}

    def test_complete_hash_bound_receipt(self):
        with tempfile.TemporaryDirectory() as t:
            root, journal, pins = self.make(t)
            r = publish_complete(root, pins, 'a'*64, journal, lambda: None)
            self.assertEqual(r['status'], 'completed-unreviewed')
            self.assertTrue((root / 'receipt.json').samefile(root / 'receipt.pending.json'))
            self.assertEqual(r['output_sha256'], pins)

    def test_quarantine_is_explicit_in_receipt(self):
        with tempfile.TemporaryDirectory() as t:
            root, journal, pins = self.make(t)
            r = publish_complete(root, pins, 'a'*64, journal, lambda: None,
                                 summary={'requested': 2, 'emitted': 1, 'blocked': 1})
            self.assertEqual(r['status'], 'completed-incomplete')
            self.assertEqual(r['summary']['blocked'], 1)

    def test_extra_file_or_hash_mismatch_blocks_publication(self):
        with tempfile.TemporaryDirectory() as t:
            root, journal, pins = self.make(t)
            (root / 'extra').write_bytes(b'x')
            with self.assertRaises(ValueError): publish_complete(root, pins, 'a'*64, journal, lambda: None)
            self.assertFalse((root / 'receipt.json').exists())
            (root / 'extra').unlink()
            pins['progress.jsonl'] = '0'*64
            with self.assertRaises(ValueError): publish_complete(root, pins, 'a'*64, journal, lambda: None)
            self.assertFalse((root / 'receipt.json').exists())

    def test_late_guard_failure_retracts_canonical_only(self):
        with tempfile.TemporaryDirectory() as t:
            root, journal, pins = self.make(t); calls = []
            def stable():
                calls.append(1)
                if len(calls) == 3: raise ValueError('late input drift')
            with self.assertRaises(ValueError): publish_complete(root, pins, 'a'*64, journal, stable)
            self.assertFalse((root / 'receipt.json').exists())
            self.assertTrue((root / 'receipt.pending.json').exists())
            self.assertTrue((root / 'nested' / 'member.obj').exists())

    def test_callback_mutation_or_new_output_prevents_commit(self):
        with tempfile.TemporaryDirectory() as t:
            root, journal, pins = self.make(t); calls = []
            def stable():
                calls.append(1)
                if len(calls) == 2: (root / 'nested' / 'member.obj').write_bytes(b'change')
            with self.assertRaises(ValueError): publish_complete(root, pins, 'a'*64, journal, stable)
            self.assertFalse((root / 'receipt.json').exists())
            self.assertTrue((root / 'receipt.pending.json').exists())

    def test_closed_journal_and_exact_budget_required(self):
        with tempfile.TemporaryDirectory() as t:
            root, journal, pins = self.make(t)
            open_journal = (root / 'other').open('wb')
            try:
                with self.assertRaises(ValueError): publish_complete(root, pins, 'a'*64, open_journal, lambda: None)
            finally: open_journal.close()
            (root / 'other').unlink()
            with self.assertRaises(ValueError): publish_complete(root, pins, 'a'*64, journal, lambda: None, max_bytes=1)
            self.assertFalse((root / 'receipt.json').exists())

    def test_existing_receipt_cannot_be_replaced(self):
        with tempfile.TemporaryDirectory() as t:
            root, journal, pins = self.make(t)
            (root / 'receipt.json').write_bytes(b'keep')
            with self.assertRaises(FileExistsError): publish_complete(root, pins, 'a'*64, journal, lambda: None)
            self.assertEqual((root / 'receipt.json').read_bytes(), b'keep')

    def test_foreign_closed_journal_is_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            root, _, pins = self.make(t)
            foreign = (Path(t) / 'foreign').open('wb'); foreign.close()
            with self.assertRaises(ValueError): publish_complete(root, pins, 'a'*64, foreign, lambda: None)
            self.assertFalse((root / 'receipt.json').exists())

    def test_guard_cannot_mutate_caller_pins_into_new_authority(self):
        with tempfile.TemporaryDirectory() as t:
            root, journal, pins = self.make(t)
            def stable(): pins['nested/member.obj'] = '0'*64
            result = publish_complete(root, pins, 'a'*64, journal, stable)
            self.assertEqual(result['output_sha256']['nested/member.obj'], sha(b'object'))

    def test_external_hardlink_before_commit_is_not_unlinked(self):
        import os
        with tempfile.TemporaryDirectory() as t:
            root, journal, pins = self.make(t); calls = []
            def stable():
                calls.append(1)
                if len(calls) == 2:
                    os.link(root / 'receipt.pending.json', root / 'receipt.json')
            with self.assertRaises(ValueError):
                publish_complete(root, pins, 'a'*64, journal, stable)
            self.assertTrue((root / 'receipt.json').samefile(root / 'receipt.pending.json'))


if __name__ == '__main__': unittest.main()
