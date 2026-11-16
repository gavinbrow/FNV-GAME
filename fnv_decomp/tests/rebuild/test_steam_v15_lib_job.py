import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/rebuild'))
SPEC = importlib.util.spec_from_file_location('steam_v15_lib_job', ROOT / 'tools/rebuild/steam_v15_lib_job.py')
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class SteamJobTests(unittest.TestCase):
    def test_disabled_without_fixed_policy(self):
        self.assertIsNone(M.REVIEW_PATH)
        self.assertIsNone(M.LEASE_SCOPE)
        with self.assertRaisesRegex(ValueError, 'fixed review'):
            M.validate({}, '0' * 64)
        with self.assertRaisesRegex(ValueError, 'disabled'):
            M.run('missing', '0' * 64)

    def test_command_is_exact_and_excludes_link(self):
        cmd = M.command()
        self.assertEqual(Path(cmd[0]).name.lower(), 'lib.exe')
        self.assertEqual(cmd[1:3], ['/NOLOGO', '/MACHINE:X86'])
        self.assertEqual(len(cmd), 5)
        self.assertTrue(cmd[3].endswith('steam-api-callbacks.def'))
        self.assertTrue(cmd[4].endswith('steam-api-callbacks.lib'))
        self.assertNotIn('/FORCE', ' '.join(cmd).upper())

    def test_environment_has_no_external_library_search_path(self):
        env = M.environment(r'C:\Windows')
        self.assertNotIn('LIB', env)
        self.assertEqual(env['TEMP'], str(M.OUT))
        self.assertEqual(env['TMP'], str(M.OUT))


if __name__ == '__main__':
    unittest.main()
