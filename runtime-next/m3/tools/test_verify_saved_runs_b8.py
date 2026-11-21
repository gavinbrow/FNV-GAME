"""Adversarial saved-control evidence tests; no real build logs are modified."""
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_saved_runs import check_control_logs, check_recorded_config


class ControlLogs(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='m3_evidence_test_')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path = self.root / 'summary.json'
        self.summary = {'steps': [{'name': 'm3-gen', 'log': 'gen.log'}, {'name': 'data-v3', 'log': 'verify.log'}],
                        'provenance': {'m3_config': {'negative_control': 'b8v'}}}
        self.write('NEGATIVE CONTROL (b8 value): x', ' DIFFERENT relocs  ROUND TRIP FAILED negative control: failure is expected')

    def write(self, gen, verify):
        (self.root / 'gen.log').write_text(gen, encoding='utf8')
        (self.root / 'verify.log').write_text(verify, encoding='utf8')

    def check_error(self, text):
        with self.assertRaisesRegex(ValueError, text):
            check_control_logs(self.path, self.summary)

    def test_b8_value(self):
        self.assertEqual(check_control_logs(self.path, self.summary), 'value')

    def test_b8_pointer(self):
        self.summary['provenance']['m3_config']['negative_control'] = 'b8p'
        self.write('NEGATIVE CONTROL (b8 pointer): x', 'M3 RELOC VALUE MISMATCH ROUND TRIP FAILED negative control: failure is expected')
        self.assertEqual(check_control_logs(self.path, self.summary), 'pointer')

    def test_incorrect_recorded_id(self):
        self.summary['provenance']['m3_config']['negative_control'] = 'b8p'
        self.check_error('disagrees')

    def test_multiple_labels(self):
        self.write('NEGATIVE CONTROL (b8 value): x\nNEGATIVE CONTROL (b8 pointer): y', ' DIFFERENT relocs  ROUND TRIP FAILED negative control: failure is expected')
        self.check_error('expected one')

    def test_cross_batch_labels(self):
        self.write('NEGATIVE CONTROL (b8 value): x\nNEGATIVE CONTROL (b7 value): y', ' DIFFERENT relocs  ROUND TRIP FAILED negative control: failure is expected')
        self.check_error('expected one')

    def test_additional_other_control_label_is_ambiguous(self):
        self.write('NEGATIVE CONTROL (b8 value): x\nNEGATIVE CONTROL (pointer): y', ' DIFFERENT relocs  ROUND TRIP FAILED negative control: failure is expected')
        self.check_error('expected one')

    def test_missing_mutation_label(self):
        self.write('nothing recorded', ' DIFFERENT relocs  ROUND TRIP FAILED negative control: failure is expected')
        self.check_error('expected one')

    def test_missing_roundtrip(self):
        self.write('NEGATIVE CONTROL (b8 value): x', ' DIFFERENT relocs  negative control: failure is expected')
        self.check_error('round-trip')

    def test_missing_expected_failure_marker(self):
        self.write('NEGATIVE CONTROL (b8 value): x', ' DIFFERENT relocs  ROUND TRIP FAILED')
        self.check_error('round-trip')

    def test_missing_value_diagnostic(self):
        self.write('NEGATIVE CONTROL (b8 value): x', 'ROUND TRIP FAILED negative control: failure is expected')
        self.check_error('value mutation diagnostic')

    def test_missing_pointer_diagnostic(self):
        self.summary['provenance']['m3_config']['negative_control'] = 'b8p'
        self.write('NEGATIVE CONTROL (b8 pointer): x', 'ROUND TRIP FAILED negative control: failure is expected')
        self.check_error('pointer mutation diagnostic')

    def test_b7_without_new_config(self):
        self.summary.pop('provenance')
        self.write('NEGATIVE CONTROL (b7 pointer): x', 'M3 RELOC VALUE MISMATCH ROUND TRIP FAILED negative control: failure is expected')
        self.assertEqual(check_control_logs(self.path, self.summary), 'pointer')

    def test_recorded_config_wrong_id(self):
        def run(ctl): return {'provenance': {'m3_config': {'selection':'batch8.json', 'dv1':True, 'dv1_ext':True, 'negative_control':ctl}}}
        self.assertFalse(check_recorded_config(run(None), {}, [run('b8v'), run('b8p')], 'batch8.json', ['b8v','b8p']))
        self.assertTrue(check_recorded_config(run(None), {}, [run('b8p'), run('b8v')], 'batch8.json', ['b8v','b8p']))


if __name__ == '__main__':
    unittest.main(verbosity=2)
