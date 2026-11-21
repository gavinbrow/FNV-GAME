"""Frozen generator fail-closed behavior with temporary inputs and mocks."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gen_m3 as g


class FailClosed(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='m3_fail_closed_')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        flags = {name: False for name in ('NEG', 'NEGP', 'NEG4V', 'NEG4P', 'NEG7V', 'NEG7P', 'NEG8V', 'NEG8P', 'ANYNEG')}
        flags_patch = patch.multiple(g, **flags)
        flags_patch.start()
        self.addCleanup(flags_patch.stop)

    def test_missing_explicit_selection_never_selects(self):
        with patch.object(g, 'SELF', str(self.root/'missing.json')), patch.object(g, 'select', side_effect=AssertionError('fallback')), patch.dict(os.environ, {'FNV_M3_SEL':'missing.json'}), patch.object(sys, 'argv', ['gen_m3.py']):
            with self.assertRaisesRegex(SystemExit, 'configured M3 selection is missing'):
                g.main()
        self.assertEqual(list(self.root.iterdir()), [])

    def test_frozen_failed_coff_refuses_prune(self):
        selected=self.root/'selection.json'; selected.write_text(json.dumps({'entries':[{'va':0x01199494,'tc':'M'}]}),encoding='utf8')
        with patch.object(g, 'SELF', str(selected)), patch.object(g, 'GEN', str(self.root)), patch.object(g, 'compile_obj', return_value=None) as compile_mock, patch.object(g, 'check', return_value={'bad':'synthetic COFF failure'}) as check_mock, patch.dict(os.environ, {'FNV_M3_SEL':'selection.json'}), patch.object(sys, 'argv', ['gen_m3.py']):
            with self.assertRaisesRegex(SystemExit, 'refusing to prune'):
                g.main()
        self.assertEqual(compile_mock.call_count, 1); self.assertEqual(check_mock.call_count, 1)
        self.assertEqual(list(self.root.iterdir()), [selected])


if __name__ == '__main__':
    unittest.main(verbosity=2)
