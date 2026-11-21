"""Isolated screenshot and state-guard tests; never sends real input."""
import importlib.util
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from PIL import Image

DIRECT = Path(__file__).resolve().parents[2] / 'direct-v1'
spec = importlib.util.spec_from_file_location('guard_harness_test', DIRECT / 'harness.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='harness_guard_')
        self.addCleanup(self.tmp.cleanup)
        self.verdict = {'shots': []}
        self.proc = Mock(); self.proc.poll.return_value = None

    def test_unknown_then_world_never_sends_input(self):
        with patch.object(h, 'snap', side_effect=['unknown', 'world']), patch.object(h, 'is_pause', return_value=False), patch.object(h, 'is_world', side_effect=[False, True]), patch.object(h, 'foreground') as focus, patch.object(h, 'tap') as tap, patch.object(h.time, 'sleep'):
            self.assertTrue(h.require_world(1, self.proc, self.tmp.name, self.verdict, 'unknown', 10))
        focus.assert_not_called(); tap.assert_not_called(); self.assertNotIn('recoveries', self.verdict)

    def test_pause_escape_once_then_world(self):
        with patch.object(h, 'snap', side_effect=['pause', 'pause', 'world']), patch.object(h, 'is_pause', side_effect=[True, True, False]), patch.object(h, 'is_world', return_value=True), patch.object(h, 'foreground') as focus, patch.object(h, 'tap') as tap, patch.object(h.time, 'sleep'):
            self.assertTrue(h.require_world(1, self.proc, self.tmp.name, self.verdict, 'pause', 10))
        focus.assert_called_once_with(1)
        tap.assert_called_once_with('esc', gap=1.5)
        self.assertEqual(self.verdict['recoveries'], [{'stage': 'pause', 'action': 'escape_pause', 'hud_restored': True}])

    def test_unknown_timeout_saves_screenshot_and_fails(self):
        with patch.object(h, 'snap', return_value='unknown'), patch.object(h, 'is_pause', return_value=False), patch.object(h, 'is_world', return_value=False), patch.object(h, 'foreground') as focus, patch.object(h, 'tap') as tap, patch.object(h, 'shot', return_value={'test': True}) as shot, patch.object(h.time, 'monotonic', side_effect=[0, 0, 2]), patch.object(h.time, 'sleep'):
            with self.assertRaisesRegex(RuntimeError, 'world HUD not detected'):
                h.require_world(1, self.proc, self.tmp.name, self.verdict, 'unknown', 1)
        focus.assert_not_called(); tap.assert_not_called(); shot.assert_called_once(); self.assertEqual(self.verdict['shots'][0][0], 'guard_failure_unknown.png')

    def test_saved_predicate_examples(self):
        root = DIRECT / 'harness-out' / 'build-all-937740-1795049441781226400'
        if not root.exists(): self.skipTest('saved evidence unavailable')
        for name in ('04_world.png', '06_world_1.png', '06_world_2.png'):
            with Image.open(root / name) as im: self.assertTrue(h.is_world(im), name); self.assertFalse(h.is_pause(im), name)
        for name in ('05_pipboy_1.png', '05_pipboy_2.png'):
            with Image.open(root / name) as im: self.assertFalse(h.is_world(im), name); self.assertFalse(h.is_pause(im), name)
        for name in ('05_pipboy_3.png', '06_world_3.png', '10_after_quicksave.png'):
            with Image.open(root / name) as im: self.assertFalse(h.is_world(im), name); self.assertTrue(h.is_pause(im), name)

    def test_console_unknown_then_world_never_toggles(self):
        with patch.object(h, 'snap', side_effect=['loading', 'world']), patch.object(h, 'is_console', return_value=False), patch.object(h, 'is_world', side_effect=[False, True]), patch.object(h, 'foreground') as focus, patch.object(h, 'tap') as tap, patch.object(h.time, 'sleep'):
            self.assertTrue(h.finish_console(1, self.proc, self.tmp.name, self.verdict, 'console', 10))
        focus.assert_not_called(); tap.assert_not_called()

    def test_console_already_world_never_toggles(self):
        with patch.object(h, 'snap', return_value='world'), patch.object(h, 'is_console', return_value=False), patch.object(h, 'is_world', return_value=True), patch.object(h, 'foreground') as focus, patch.object(h, 'tap') as tap:
            self.assertTrue(h.finish_console(1, self.proc, self.tmp.name, self.verdict, 'console', 10))
        focus.assert_not_called(); tap.assert_not_called()
        self.assertEqual(self.verdict['console_transitions'][0]['action'], 'world_without_toggle')

    def test_confirmed_console_closed_once_then_world(self):
        with patch.object(h, 'snap', side_effect=['console', 'console', 'world']), patch.object(h, 'is_console', side_effect=[True, True, False]), patch.object(h, 'is_world', return_value=True), patch.object(h, 'foreground') as focus, patch.object(h, 'tap') as tap, patch.object(h.time, 'sleep'):
            self.assertTrue(h.finish_console(1, self.proc, self.tmp.name, self.verdict, 'console', 10))
        focus.assert_called_once_with(1); tap.assert_called_once_with('grave', gap=1.5)
        self.assertTrue(self.verdict['recoveries'][0]['hud_restored'])
        self.assertEqual(self.verdict['console_transitions'][0]['action'], 'closed_confirmed_console')

    def test_console_unknown_timeout_saves_failure(self):
        with patch.object(h, 'snap', return_value='unknown'), patch.object(h, 'is_console', return_value=False), patch.object(h, 'is_world', return_value=False), patch.object(h, 'foreground') as focus, patch.object(h, 'tap') as tap, patch.object(h, 'shot', return_value={'test': True}) as shot, patch.object(h.time, 'monotonic', side_effect=[0, 0, 2]), patch.object(h.time, 'sleep'):
            with self.assertRaisesRegex(RuntimeError, 'world HUD not detected'):
                h.finish_console(1, self.proc, self.tmp.name, self.verdict, 'console', 1)
        focus.assert_not_called(); tap.assert_not_called(); shot.assert_called_once()

    def test_saved_console_and_nonconsole_frames(self):
        root = DIRECT / 'harness-out'
        console = root / 'batch8-guard-check-20261118' / 'guard_failure_console_after_coc.png'
        if not console.exists(): self.skipTest('saved console evidence unavailable')
        with Image.open(console) as im: self.assertTrue(h.is_console(im))
        prior = root / 'build-all-937740-1795049441781226400'
        for name in ('04_world.png', '05_pipboy_1.png', '05_pipboy_3.png', '18_time_changed.png', '22_after_quickload.png'):
            with Image.open(prior / name) as im: self.assertFalse(h.is_console(im), name)

    def _run_quit(self, polls, clock):
        self.proc.poll.side_effect = polls
        self.verdict['steps'] = {}
        with patch.object(h, 'foreground') as focus, patch.object(h, 'require_world') as world, patch.object(h, 'tap') as tap, patch.object(h, 'type_text') as typed, patch.object(h.time, 'monotonic', side_effect=clock), patch.object(h.time, 'sleep'):
            result = h.quit_game_console(1, self.proc, self.tmp.name, self.verdict, timeout=1)
        focus.assert_called_once_with(1); world.assert_called_once(); typed.assert_called_once_with('qqq')
        self.assertEqual([call.args[0] for call in tap.call_args_list], ['grave', 'enter'])
        self.assertEqual(self.verdict['steps']['exit_method'], 'console_quitgame')
        return result

    def test_quit_returns_actual_zero(self):
        self.assertEqual(self._run_quit([None, 0, 0], [0, 0]), 0)

    def test_quit_returns_actual_nonzero(self):
        self.assertEqual(self._run_quit([None, 7, 7], [0, 0]), 7)

    def test_quit_timeout_is_not_success(self):
        self.assertIsNone(self._run_quit([None, None, None], [0, 2]))

    def test_isolated_binding_decode(self):
        ini = Path(self.tmp.name) / 'FalloutPrefs.ini'
        ini.write_text('[Controls]\nQuickSave=003FFFFF\nQuickLoad=0040FFFF\n[Other]\nThis may result in errors.\n', encoding='ascii')
        self.assertEqual(h.configured_scan_code(ini, 'QuickSave'), 0x3f)
        self.assertEqual(h.configured_scan_code(ini, 'QuickLoad'), 0x40)
        with self.assertRaisesRegex(ValueError, 'missing or duplicate'):
            h.configured_scan_code(ini, 'Missing')
        for value in ('FFFFFFFF', '0000FFFF', '007FFFFF', '0080FFFF', 'nothex'):
            ini.write_text('[Controls]\nQuickLoad=' + value + '\n', encoding='ascii')
            with self.assertRaises(ValueError): h.configured_scan_code(ini, 'QuickLoad')
        ini.write_text('[Controls]\nQuickLoad=0040FFFF\nQuickLoad=0040FFFF\n', encoding='ascii')
        with self.assertRaisesRegex(ValueError, 'duplicate'): h.configured_scan_code(ini, 'QuickLoad')
        actual = DIRECT / 'run' / 'FalloutPrefs.ini'
        if actual.exists():
            self.assertGreater(h.configured_scan_code(actual, 'QuickSave'), 0)
            self.assertGreater(h.configured_scan_code(actual, 'QuickLoad'), 0)

    def test_cell_wait_retries_unavailable_and_wrong_then_accepts_matching_hud(self):
        class Unavailable(RuntimeError): pass
        probe = Mock(); probe.read_cell_id.side_effect = [Unavailable('loading'), 2, 1, 1]
        with patch.dict(sys.modules, {'game_state': types.SimpleNamespace(StateUnavailable=Unavailable)}), patch.object(h, 'snap', return_value='frame'), patch.object(h, 'is_world', side_effect=[False, True]), patch.object(h.time, 'sleep'):
            self.assertEqual(h.wait_for_cell(1, self.proc, probe, self.tmp.name, self.verdict, 'restore', lambda cell: cell == 1, 10), 1)
        self.assertEqual(probe.read_cell_id.call_count, 4)

    def test_cell_wait_timeout_is_failure_with_screenshot(self):
        class Unavailable(RuntimeError): pass
        probe = Mock(); probe.read_cell_id.side_effect = Unavailable('loading')
        with patch.dict(sys.modules, {'game_state': types.SimpleNamespace(StateUnavailable=Unavailable)}), patch.object(h, 'shot', return_value={'test': True}) as shot, patch.object(h.time, 'monotonic', side_effect=[0, 0, 2]), patch.object(h.time, 'sleep'):
            with self.assertRaisesRegex(RuntimeError, 'matching world cell not observed'):
                h.wait_for_cell(1, self.proc, probe, self.tmp.name, self.verdict, 'restore', lambda cell: cell == 1, 1)
        shot.assert_called_once(); self.assertEqual(self.verdict['shots'][0][0], 'guard_failure_restore.png')


if __name__ == '__main__': unittest.main(verbosity=2)
