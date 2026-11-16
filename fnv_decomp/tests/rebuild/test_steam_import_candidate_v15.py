import hashlib
import importlib.util
from pathlib import Path
import unittest


PATH = Path(__file__).resolve().parents[2] / 'tools/rebuild/steam_import_candidate_v15.py'
SPEC = importlib.util.spec_from_file_location('steam_candidate_v15', PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SteamCandidateTests(unittest.TestCase):
    def test_fixed_single_named_import_and_digest(self):
        definition, plan = MODULE.candidate()
        self.assertEqual(definition, b'LIBRARY "steam_api.dll"\nEXPORTS\n    SteamAPI_RunCallbacks\n')
        self.assertEqual(plan['definition_sha256'], hashlib.sha256(definition).hexdigest())
        self.assertEqual(plan['identity']['import_id'], 203)
        self.assertEqual(plan['identity']['original_iat_cell'], '0x00fdf488')

    def test_plan_cannot_authorize_native_or_alias(self):
        _, plan = MODULE.candidate()
        for key in ('native_operation_authorized', 'native_library_generated',
                    'dll_inspected_or_loaded', 'export_or_abi_verified',
                    'alias_applied', 'runtime_provider_adopted', 'executable_link_performed'):
            self.assertIs(plan[key], False)
        self.assertTrue(plan['required_before_native_operation'])
        self.assertTrue(plan['required_before_alias_or_link'])

    def test_independent_fresh_plans(self):
        _, first = MODULE.candidate()
        first['native_operation_authorized'] = True
        _, second = MODULE.candidate()
        self.assertIs(second['native_operation_authorized'], False)


if __name__ == '__main__':
    unittest.main()
