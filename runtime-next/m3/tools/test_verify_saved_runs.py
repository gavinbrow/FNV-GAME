import copy
import importlib.util
import unittest
import tempfile
from pathlib import Path

spec = importlib.util.spec_from_file_location('verify_saved_runs', Path(__file__).with_name('verify_saved_runs.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class SavedRunTests(unittest.TestCase):
    def setUp(self):
        self.steps = dict(main_menu_reached=True, world_loaded=True, alive_after_play=True,
                          extended_ok=True, exited_cleanly=True, exit_code=0, play_secs=1,
                          extended=dict(new_save_written=True, world_after_coc=True,
                                        world_after_time=True, world_after_load=True))
        self.base = dict(status='ok', steps=[dict(rc=0)], exe=dict(path='positive', sha256='a'*64),
                         provenance=dict(m3=dict(negctl=False)),
                         harness=dict(rc=0, pass_=True, steps=self.steps))
        self.default = copy.deepcopy(self.base)
        self.default['provenance'] = {}
        self.controls = [copy.deepcopy(self.base), copy.deepcopy(self.base)]
        for run, letter in zip(self.controls, 'bc'):
            run['exe']['sha256'] = letter*64
            run['provenance']['m3']['negctl'] = True
        self.verdict = dict(pass_=True, exe='positive', steps=copy.deepcopy(self.steps))

    def test_recorded_config_is_strict_and_opt_in(self):
        selection = 'selection.txt'
        ids = ['value', 'pointer']
        self.base['provenance']['m3_config'] = dict(selection=selection, dv1=True,
                                                    dv1_ext=True, negative_control=None)
        for run, identity in zip(self.controls, ids):
            run['provenance']['m3_config'] = dict(selection=selection, dv1=True,
                                                   dv1_ext=True, negative_control=identity)
        def check():
            return m.check_recorded_config(self.base, self.default, self.controls, selection, ids)
        self.assertEqual(check(), [])
        for key, bad in [('selection', 'other'), ('dv1', 1), ('dv1_ext', False),
                         ('negative_control', 'unknown')]:
            config = self.controls[0]['provenance']['m3_config']
            old = config[key]
            config[key] = bad
            self.assertTrue(check(), key)
            config[key] = old
        del self.controls[0]['provenance']['m3_config']['negative_control']
        self.assertTrue(check())
        self.assertTrue(m.check_recorded_config(self.base, self.default, self.controls, selection, ['unknown', 'pointer']))
        self.assertTrue(m.check_recorded_config(self.base, self.default, self.controls, selection, ['value']))
        self.assertTrue(m.check_recorded_config(self.base, self.default, self.controls, selection, ['value', 'value']))
        self.default['provenance']['m3_config'] = {}
        self.assertTrue(check())
        # Existing summary-only checks do not require the new field.
        self.assertEqual(m.check(self.base, self.default, self.controls, self.verdict), [])

    def test_selection_digest_evidence(self):
        digest = 'ab' * 32
        runs = [self.base] + self.controls
        for run in runs:
            run['provenance']['m3_config'] = {'selection_sha256': digest.upper()}
        def check(expected=digest):
            return m.check_selection_sha256(self.base, self.controls, expected)
        self.assertEqual(check(), [])
        self.assertTrue(check('bad'))
        self.controls[0]['provenance']['m3_config']['selection_sha256'] = 'cd' * 32
        self.assertIn('control 1', check()[0])
        self.controls[0]['provenance']['m3_config']['selection_sha256'] = 'z' * 64
        self.assertIn('invalid', check()[0])
        del self.controls[0]['provenance']['m3_config']
        self.assertIn('missing recorded M3 configuration', check()[0])
        del self.base['provenance']['m3_config']['selection_sha256']
        self.assertIn('positive', check()[0])
        # Older summaries are still accepted by the original check.
        self.assertEqual(m.check(self.base, self.default, self.controls, self.verdict), [])

    def test_control_log_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            summary = {'steps': [{'name': 'm3-gen', 'log': 'gen.log'},
                                 {'name': 'data-v3', 'log': 'verify.log'}]}
            gen, verify = root / 'gen.log', root / 'verify.log'
            gen.write_text('NEGATIVE CONTROL (b7 value): change', encoding='utf-8')
            verify.write_text(' DIFFERENT relocs 1\nROUND TRIP FAILED\nnegative control: failure is expected', encoding='utf-8')
            self.assertEqual(m.check_control_logs(root / 'summary.json', summary), 'value')
            verify.write_text('ROUND TRIP FAILED', encoding='utf-8')
            with self.assertRaises(ValueError):
                m.check_control_logs(root / 'summary.json', summary)
            summary['steps'][0]['log'] = '../escape.log'
            with self.assertRaises(ValueError):
                m.check_control_logs(root / 'summary.json', summary)

    def test_code_provenance_consistency(self):
        prov = {'code_coverage_pct_of_nonpadding_text': 100.0,
                'borrowed_relocation_field_bytes': 0, 'undecompiled_bytes': 0,
                'code_bytes_taken_from_filled_image': 0, 'filled_equals_reference': True,
                'rel32_fields': 3, 'dir32_fields': 4, 'data_pointer_fields': {'code': 5}}
        positive = {'provenance': prov}
        other = {'provenance': copy.deepcopy(prov)}
        self.assertEqual(m.check_provenance(positive, [('default', other)]), [])
        other['provenance']['rel32_fields'] += 1
        self.assertTrue(m.check_provenance(positive, [('default', other)]))
        other['provenance']['rel32_fields'] -= 1
        del other['provenance']['undecompiled_bytes']
        self.assertTrue(m.check_provenance(positive, [('default', other)]))
        prov['borrowed_relocation_field_bytes'] = 1
        self.assertTrue(m.check_provenance(positive, [('default', other)]))

    def test_extended_mode_and_default_mixing(self):
        run = {'steps': [{'name': 'm3-gen'}, {'name': 'm3-dv1'}],
               'provenance': {'m3_dv1': {'ext': {'enabled': True}}}}
        self.assertEqual(m.check_extended_mode(run, 'run'), [])
        run['provenance']['m3_dv1']['ext']['enabled'] = False
        self.assertTrue(m.check_extended_mode(run, 'run'))
        self.default['steps'].append({'name': 'm3-gen', 'rc': 0})
        self.assertTrue(m.check(self.base, self.default, self.controls, self.verdict))

    def test_valid_and_negative_cases(self):
        self.assertEqual(m.check(self.base, self.default, self.controls, self.verdict), [])
        self.controls[0]['provenance']['m3']['negctl'] = False
        self.assertTrue(m.check(self.base, self.default, self.controls, self.verdict))
        self.controls[0]['provenance']['m3']['negctl'] = True
        self.controls[0]['exe']['sha256'] = 'a'*64
        self.assertTrue(m.check(self.base, self.default, self.controls, self.verdict))
        self.controls[0]['exe']['sha256'] = 'c'*64
        self.assertTrue(m.check(self.base, self.default, self.controls, self.verdict))
        self.controls[0]['exe']['sha256'] = 'b'*64
        self.verdict['steps']['exited_cleanly'] = False
        self.assertTrue(m.check(self.base, self.default, self.controls, self.verdict))
        self.verdict['steps'] = copy.deepcopy(self.steps)
        self.default['exe']['sha256'] = 'invalid'
        self.assertTrue(m.check(self.base, self.default, self.controls, self.verdict))


if __name__ == '__main__':
    unittest.main()
