from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]


class DirectStartupHost(unittest.TestCase):
    def test_entry_signature_matches_source(self):
        source = (ROOT / 'src/fallout/misc/main.cpp').read_text(encoding='utf-8')
        host = (ROOT / 'runtime/startup/game_startup_host_direct.cpp').read_text(encoding='ascii')
        self.assertRegex(source, r'int __stdcall FUN_0086a850\(unsigned int param_1, unsigned int param_2, unsigned int param_3, unsigned int param_4\)')
        self.assertRegex(host, r'(?m)^int __stdcall FUN_0086a850\(unsigned int, unsigned int, unsigned int, unsigned int\);$')
        self.assertNotIn('extern "C" int __stdcall FUN_0086a850', host)

    def test_original_argument_forwarding_is_unchanged(self):
        old = (ROOT / 'runtime/startup/game_startup_host.cpp').read_text(encoding='utf-8')
        new = (ROOT / 'runtime/startup/game_startup_host_direct.cpp').read_text(encoding='ascii')
        old_body = old[old.index('extern "C" int WINAPI WinMain'):].replace('fnv_game_application_entry(', 'FUN_0086a850(')
        new_body = new[new.index('extern "C" int WINAPI WinMain'):]
        self.assertEqual(old_body, new_body)


if __name__ == '__main__':
    unittest.main()
