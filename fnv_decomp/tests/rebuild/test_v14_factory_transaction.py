"""Synthetic atomic staging tests; no original or protected inputs."""
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/rebuild'))
from v14_factory_transaction import stage_and_publish


class TransactionTests(unittest.TestCase):
    def test_full_set_published(self):
        with tempfile.TemporaryDirectory() as temp:
            facts = stage_and_publish(temp, 'result', [1, 2], lambda n: (f'{n}.obj', bytes([n])),
                                      lambda rows: len(rows) == 2, max_bytes=1024)
            self.assertEqual(len(facts), 2)
            self.assertEqual((Path(temp) / 'result' / '2.obj').read_bytes(), b'\x02')
            self.assertEqual(len(list(Path(temp).iterdir())), 1)

    def test_callback_failure_discards_all_private_staging(self):
        with tempfile.TemporaryDirectory() as temp:
            def produce(n):
                if n == 2:
                    raise RuntimeError('deliberate')
                return '1.obj', b'x'
            with self.assertRaises(RuntimeError):
                stage_and_publish(temp, 'result', [1, 2], produce, lambda _: True, max_bytes=1024)
            self.assertEqual(list(Path(temp).iterdir()), [])

    def test_rejection_and_limits_discard_staging(self):
        with tempfile.TemporaryDirectory() as temp:
            for producer, validator, limit in [(lambda _: ('a.obj', b'a'), lambda _: False, 1024),
                                               (lambda _: ('a.obj', b'aa'), lambda _: True, 1),
                                               (lambda _: ('../escape.obj', b'a'), lambda _: True, 1024)]:
                with self.assertRaises(ValueError):
                    stage_and_publish(temp, 'result', [1], producer, validator, max_bytes=limit)
                self.assertEqual(list(Path(temp).iterdir()), [])

    def test_existing_destination_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            dst = Path(temp) / 'result'
            dst.mkdir()
            (dst / 'existing').write_text('keep')
            with self.assertRaises(FileExistsError):
                stage_and_publish(temp, 'result', [1], lambda _: ('a.obj', b'a'), lambda _: True, max_bytes=1024)
            self.assertEqual((dst / 'existing').read_text(), 'keep')

    def test_mutation_and_destination_race_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            def mutate(_):
                scratch = next(Path(temp).glob('.v14-stage-*'))
                (scratch / 'a.obj').write_bytes(b'z')
                return True
            with self.assertRaises(ValueError):
                stage_and_publish(temp, 'result', [1], lambda _: ('a.obj', b'a'), mutate, max_bytes=1024)
            self.assertEqual(list(Path(temp).iterdir()), [])
            def race(_):
                (Path(temp) / 'result').mkdir()
                return True
            with self.assertRaises(FileExistsError):
                stage_and_publish(temp, 'result', [1], lambda _: ('a.obj', b'a'), race, max_bytes=1024)
            self.assertTrue((Path(temp) / 'result').is_dir())

    def test_producer_receives_detached_selection(self):
        with tempfile.TemporaryDirectory() as temp:
            selected = [{'root': 'original'}]
            def produce(item):
                item['root'] = 'changed'
                return 'a.obj', b'a'
            stage_and_publish(temp, 'result', selected, produce, lambda _: True, max_bytes=1024)
            self.assertEqual(selected, [{'root': 'original'}])


if __name__ == '__main__':
    unittest.main()
