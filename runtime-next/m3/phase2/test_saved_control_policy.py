"""Exercise the saved-run CLI with extra controls and adversarial evidence.

Pass an isolated candidate checker path while build inputs are frozen.
"""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


CHECKER = Path(sys.argv.pop(1)) if len(sys.argv) > 1 else Path(__file__).parents[1] / 'tools/verify_saved_runs.py'
spec = importlib.util.spec_from_file_location('saved_policy_candidate', CHECKER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ControlPolicyCLITests(unittest.TestCase):
    def run_cli(self, ids, edit=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            steps = dict(main_menu_reached=True, world_loaded=True, alive_after_play=True,
                         extended_ok=True, exited_cleanly=True, exit_code=0, play_secs=72,
                         extended=dict(new_save_written=True, world_after_coc=True,
                                       world_after_time=True, world_after_load=True))
            prov = dict(code_coverage_pct_of_nonpadding_text=100.0,
                        borrowed_relocation_field_bytes=0, undecompiled_bytes=0,
                        code_bytes_taken_from_filled_image=0, filled_equals_reference=True,
                        rel32_fields=3, dir32_fields=4, data_pointer_fields={'code': 5})
            positive = dict(status='ok', steps=[dict(name='m3-gen', rc=0), dict(name='m3-dv1', rc=0)],
                            exe=dict(path='positive.exe', sha256='a'*64),
                            provenance=copy.deepcopy(prov),
                            harness=dict(rc=0, pass_=True, steps=steps))
            positive['provenance'].update(
                m3=dict(negctl=False), m3_dv1=dict(ext=dict(enabled=True)),
                m3_config=dict(selection='fixture.json', selection_sha256='f'*64,
                               dv1=True, dv1_ext=True, negative_control=None))
            default = dict(status='ok', steps=[dict(name='compile', rc=0)],
                           exe=dict(path='default.exe', sha256='a'*64), provenance=prov)
            verdict = dict(pass_=True, exe='positive.exe', steps=copy.deepcopy(steps))
            labels = {'b8v': 'b8 value', 'b8p': 'b8 pointer',
                      'p2sv': 'p2 scalar value', 'p2av': 'p2 array value',
                      'p2wp': 'p2 tail pointer', 'p2lv': 'p2 library value'}
            controls = []
            for i, identity in enumerate(ids):
                folder = root / str(i)
                folder.mkdir()
                run = copy.deepcopy(positive)
                run['exe']['sha256'] = format(i+11, 'x')*64
                run['provenance']['m3']['negctl'] = True
                run['provenance']['m3_config']['negative_control'] = identity
                run['steps'] = [dict(name='m3-gen', rc=0, log='gen.log'),
                                dict(name='m3-dv1', rc=0),
                                dict(name='data-v3', rc=0, log='verify.log')]
                label = labels[identity]
                marker = 'NEGATIVE CONTROL (%s): change\n' % label
                gen = '' if identity == 'p2lv' else marker
                verify = marker if identity == 'p2lv' else ''
                verify += ('M3 RELOC VALUE MISMATCH\n' if label.endswith('pointer') else ' DIFFERENT relocs 1\n')
                verify += 'ROUND TRIP FAILED\nnegative control: failure is expected\n'
                (folder/'gen.log').write_text(gen, encoding='utf-8')
                (folder/'verify.log').write_text(verify, encoding='utf-8')
                controls.append(run)
            if edit:
                edit(root, positive, controls)
            def save(path, obj):
                path.write_text(json.dumps(obj), encoding='utf-8')
            save(root/'positive.json', positive)
            save(root/'default.json', default)
            save(root/'verdict.json', verdict)
            argv = ['verify_saved_runs.py', '--positive', str(root/'positive.json'),
                    '--default', str(root/'default.json'), '--verdict', str(root/'verdict.json'),
                    '--check-control-logs', '--require-extended-mode',
                    '--expected-selection', 'fixture.json', '--expected-selection-sha256', 'f'*64]
            for i, (identity, control) in enumerate(zip(ids, controls)):
                path = root/str(i)/'summary.json'
                save(path, control)
                argv += ['--control', str(path), '--expected-control', identity]
            output = io.StringIO()
            with patch.object(sys, 'argv', argv), contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                rc = m.main()
            return rc, output.getvalue()

    def test_three_individually_valid_controls(self):
        self.assertEqual(self.run_cli(['p2av', 'p2wp', 'p2lv'])[0], 0)

    def test_two_legacy_controls_still_pass(self):
        self.assertEqual(self.run_cli(['b8v', 'b8p'])[0], 0)

    def test_control_order_is_irrelevant_to_kind_coverage(self):
        self.assertEqual(self.run_cli(['p2wp', 'p2lv', 'p2av'])[0], 0)

    def test_missing_pointer_rejected(self):
        rc, output = self.run_cli(['p2sv', 'p2av', 'p2lv'])
        self.assertEqual(rc, 1)
        self.assertIn('at least one value and one pointer', output)

    def test_missing_value_rejected(self):
        self.assertEqual(self.run_cli(['b8p', 'p2wp'])[0], 1)

    def test_extra_control_requires_distinct_hash(self):
        def edit(root, positive, controls):
            controls[2]['exe']['sha256'] = controls[0]['exe']['sha256']
        rc, output = self.run_cli(['p2av', 'p2wp', 'p2lv'], edit)
        self.assertEqual(rc, 1)
        self.assertIn('control hashes are not distinct', output)

    def test_extra_control_requires_distinct_id(self):
        rc, output = self.run_cli(['p2av', 'p2wp', 'p2av'])
        self.assertEqual(rc, 1)
        self.assertIn('control identifiers must be distinct', output)

    def test_extra_control_must_differ_from_positive(self):
        def edit(root, positive, controls):
            controls[2]['exe']['sha256'] = positive['exe']['sha256']
        self.assertEqual(self.run_cli(['p2av', 'p2wp', 'p2lv'], edit)[0], 1)

    def test_extra_control_requires_expected_failure(self):
        def edit(root, positive, controls):
            (root/'2/verify.log').write_text('NEGATIVE CONTROL (p2 library value): change\n DIFFERENT relocs 1\n', encoding='utf-8')
        rc, output = self.run_cli(['p2av', 'p2wp', 'p2lv'], edit)
        self.assertEqual(rc, 2)
        self.assertIn('missing expected round-trip failure evidence', output)

    def test_extra_control_requires_supported_single_mutation(self):
        def edit(root, positive, controls):
            (root/'2/gen.log').write_text('NEGATIVE CONTROL (mystery): change\n', encoding='utf-8')
        self.assertEqual(self.run_cli(['p2av', 'p2wp', 'p2sv'], edit)[0], 2)

    def test_extra_control_requires_corresponding_diagnostic(self):
        def edit(root, positive, controls):
            path = root/'2/verify.log'
            path.write_text(path.read_text(encoding='utf-8').replace(' DIFFERENT relocs 1', 'M3 RELOC VALUE MISMATCH'), encoding='utf-8')
        rc, output = self.run_cli(['p2av', 'p2wp', 'p2lv'], edit)
        self.assertEqual(rc, 2)
        self.assertIn('missing value mutation diagnostic', output)


if __name__ == '__main__':
    unittest.main()
