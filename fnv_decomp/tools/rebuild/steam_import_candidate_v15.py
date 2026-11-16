"""Review-only Steam import proposal. No native tools, DLL access or aliasing."""
from __future__ import annotations

import hashlib
import json


def candidate():
    """Return fixed proposed bytes and a non-authorizing operation plan.

    The DEF describes an intended import; it does not establish that the
    installed DLL exports it, or that the DLL is compatible with this program.
    """
    definition = b'LIBRARY "steam_api.dll"\nEXPORTS\n    SteamAPI_RunCallbacks\n'
    plan = {
        'schema_version': 1,
        'kind': 'steam-import-candidate-v15-review-only',
        'status': 'blocked-pending-scoped-evidence-and-review',
        'identity': {'dll': 'steam_api.dll', 'export': 'SteamAPI_RunCallbacks',
                     'import_id': 203, 'original_iat_cell': '0x00fdf488'},
        'definition_sha256': hashlib.sha256(definition).hexdigest(),
        'source_declaration': 'extern "C" __declspec(dllimport) void __cdecl SteamAPI_RunCallbacks();',
        'operation_plan': [
            {'tool': 'lib.exe', 'arguments': ['/NOLOGO', '/MACHINE:X86',
                '/DEF:<reviewed-saved-def>', '/OUT:<new-exclusive-import-lib>']},
            {'tool': 'dumpbin.exe', 'arguments': ['/HEADERS', '<new-import-lib>']},
            {'tool': 'dumpbin.exe', 'arguments': ['/LINKERMEMBER:2', '<new-import-lib>']},
        ],
        'required_before_native_operation': [
            'review exact source, plan, scoped inputs and lease',
            'bind exact owned DLL hash and verify i386 named export from PE metadata without loading',
            'review applicable declaration and full current cohort cell-use evidence',
        ],
        'required_before_alias_or_link': [
            'independently inspect actual archive and pointer symbol against DLL and catalog identity',
            'independently review full current cohort mappings and provider contracts',
        ],
        'native_operation_authorized': False,
        'native_library_generated': False,
        'dll_inspected_or_loaded': False,
        'export_or_abi_verified': False,
        'alias_applied': False,
        'runtime_provider_adopted': False,
        'executable_link_performed': False,
    }
    return definition, plan


if __name__ == '__main__':
    definition, plan = candidate()
    print(json.dumps({'definition_ascii': definition.decode('ascii'), 'plan': plan},
                     indent=2, sort_keys=True))
