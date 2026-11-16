"""Two-root UUID directive occurrence proposal. No I/O, native parsing or admission.

Authority is supplied and authenticated independently by the caller; matching
hashes here establish consistency, not authority or linker-selection semantics.
"""
import copy
import hashlib
import json
import re

POLICY = 'finite-uuid-directive-occurrence-proposal-v1'
UUID = '/DEFAULTLIB:"uuid.lib"'
TOKENS = [UUID, UUID, '/DEFAULTLIB:"LIBCMT"', '/DEFAULTLIB:"OLDNAMES"']
UUID_ID = '500b64d35a879017b6e729c7264954dafd1722389e78fe47ff618916fb537d35'
DIFF_ID = '771cd50e84e5996d8fda1470742f71fe7d99f887e03ad7338a4dd10d753ef094'
ROOTS = {
 '0x00c5d4e0': dict(recipe_id='2768-7a8853c4310f459f', recipe_index=2768, size=58, section=131,
    symbol='?FUN_00c5d4e0@@YAXXZ', symbol_index=553, value=0,
    object_sha256='a7280d36e8d796a5689c8b61adac4be327eb17d55e12d734600b0ede46cafb88',
    source_sha256='376782096fdbabae4c10fb175023317d58fcbd8930596abea1008d8628bffe02',
    certificate_sha256='7c4704d0c777585656272cd2a39a06437d124e34d4cea712236b982641cf9a26'),
 '0x0045b020': dict(recipe_id='0950-3034f4bb10207776', recipe_index=950, size=35, section=32,
    symbol='?FUN_0045b020@@YAXXZ', symbol_index=160, value=0,
    object_sha256='55f97d37531c3a396a4d4143f05512639089bfb5f05a8266e2dc3267f1a8ede8',
    source_sha256='66d46b132e101463fe3483ade0e63bcabcafea4d5261bd9bbf46f4dac152f5fe',
    certificate_sha256='bed5fec32a338aab551d640cbf3e11c8f25242fdcae060247baa4afcd03a73b8')}
ROOT_FIELDS = ('original_address','symbol','symbol_index','section','value','size')
HEADER_KEYS = {'index','name','size','flags','virtual_size','virtual_address','object_size','raw_data_offset',
               'section_count','optional_header_size','relocation_count','relocation_pointer',
               'line_number_count','line_number_pointer'}
BINDING_KEYS = {'kind','library_name','path','sha256','candidate_manifest_path','candidate_manifest_sha256'}
AUTH_KEYS = {'root_sha256','contract_sha256','certificate_sha256','section_sha256','header_sha256',
             'binding_sha256','candidate_manifest_path','candidate_manifest_sha256'}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True,
                                     allow_nan=False).encode('ascii')).hexdigest()


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(s):
    return type(s) is str and re.fullmatch('[0-9a-f]{64}', s) is not None


def safe_path(s):
    return type(s) is str and bool(s) and all(ord(ch) >= 32 and ord(ch) != 127 for ch in s)


def assess(root, contract, original_negative, raw_section, header, uuid_binding, authority):
    """Return a proposal for exact occurrences; caller must authenticate pins.

    The caller supplies already-observed full section bytes/header and an
    independently bound normal SDK library search candidate. No object, path or library is
    opened. Inputs are copied into the result only after all checks succeed.
    """
    need(type(root) is dict and root.get('original_address') in ROOTS, 'unsupported root')
    spec = ROOTS[root['original_address']]
    expected_root = dict(original_address=root['original_address'], **{k:v for k,v in spec.items() if k != 'certificate_sha256'})
    need(root == expected_root and digest(root) == digest(expected_root), 'root identity differs')
    need(type(contract) is dict and type(original_negative) is dict, 'contract and certificate required')
    need(type(authority) is dict and set(authority) == AUTH_KEYS, 'authority schema')
    need(all(sha(authority[k]) for k in AUTH_KEYS if k.endswith('_sha256')), 'invalid authority hash')
    need(authority['root_sha256'] == digest(root) and authority['contract_sha256'] == digest(contract), 'root/contract pin differs')
    need(authority['certificate_sha256'] == spec['certificate_sha256'] == digest(original_negative), 'original certificate pin differs')
    native_root = {k:root[k] for k in ROOT_FIELDS}
    prov = contract.get('provenance')
    need(type(prov) is dict and prov.get('object_sha256') == root['object_sha256'] and
         prov.get('source_sha256') == root['source_sha256'] and prov.get('recipe_id') == root['recipe_id'] and
         type(prov.get('recipe_index')) is int and prov['recipe_index'] == root['recipe_index'], 'provenance differs')
    need(contract.get('recipe_id') == root['recipe_id'] and contract.get('roots') == [native_root] and
         digest(contract['roots']) == digest([native_root]), 'contract root differs')
    need(original_negative.get('recipe_id') == root['recipe_id'] and
         original_negative.get('roots') == [native_root] and digest(original_negative['roots']) == digest([native_root]) and
         original_negative.get('contract_identity_sha256') == digest(contract), 'certificate scope differs')
    need(original_negative.get('closure_observed') is False and original_negative.get('graph_observation_complete') is False and
         original_negative.get('root_closure_candidate') is False, 'original negative promoted')
    blockers = original_negative.get('blockers')
    expected = [dict(code='UNSUPPORTED_IMPLICIT_LINKER_DIRECTIVE', evidence=UUID, blocker_id=UUID_ID),
                dict(code='UNSUPPORTED_IMPLICIT_LINKER_DIRECTIVE', evidence=UUID, blocker_id=UUID_ID),
                dict(code='DIRECTIVE_CONTRACT_DIFFERS', evidence=TOKENS, blocker_id=DIFF_ID)]
    need(type(blockers) is list and blockers == expected and digest(blockers) == digest(expected), 'original occurrences differ')
    need(type(raw_section) is bytes and len(raw_section) == 93 and
         hashlib.sha256(raw_section).hexdigest() == authority['section_sha256'], 'raw section differs')
    need(type(header) is dict and set(header) == HEADER_KEYS and digest(header) == authority['header_sha256'], 'header pin/schema differs')
    for k in HEADER_KEYS - {'name'}:
        need(type(header[k]) is int and 0 <= header[k] <= 0xffffffff, 'invalid header integer')
    need((header['index'],header['name'],header['size'],header['flags'],header['virtual_size'],header['virtual_address'],header['relocation_count'],
          header['relocation_pointer'],header['line_number_count'],header['line_number_pointer']) ==
         (1,'.drectve',93,0x100a00,0,0,0,0,0,0) and root['section'] <= header['section_count'] <= 65535 and
         header['optional_header_size'] == 0 and
         header['raw_data_offset'] >= 20 + header['optional_header_size'] + 40 * header['section_count'] and
         header['raw_data_offset'] + header['size'] <= header['object_size'], 'unsupported section header')
    need(type(uuid_binding) is dict and set(uuid_binding) == BINDING_KEYS and
         digest(uuid_binding) == authority['binding_sha256'], 'binding pin/schema differs')
    need(uuid_binding['kind'] == 'bound-normal-sdk-search-candidate' and uuid_binding['library_name'] == 'uuid.lib' and
         safe_path(uuid_binding['path']) and uuid_binding['path'].replace('\\','/').split('/')[-1].casefold() == 'uuid.lib' and
         sha(uuid_binding['sha256']) and safe_path(uuid_binding['candidate_manifest_path']) and
         sha(uuid_binding['candidate_manifest_sha256']) and
         uuid_binding['candidate_manifest_path'] == authority['candidate_manifest_path'] and
         uuid_binding['candidate_manifest_sha256'] == authority['candidate_manifest_sha256'], 'normal library binding differs')
    # Token spans are exact; only ASCII whitespace is allowed between literals.
    token_bytes = [s.encode('ascii') for s in TOKENS]
    pos = 0
    spans = []
    for token in token_bytes:
        while pos < len(raw_section) and raw_section[pos] in b' \t\r\n': pos += 1
        start = pos
        need(raw_section[pos:pos+len(token)] == token, 'directive token differs')
        pos += len(token)
        spans.append(dict(ordinal=len(spans)+1, start=start, end=pos, token=token.decode('ascii')))
        need(pos == len(raw_section) or raw_section[pos] in b' \t\r\n', 'missing token boundary')
    need(all(ch in b' \t\r\n' for ch in raw_section[pos:]), 'unparsed directive bytes')
    occurrences = [dict(ordinal=i, blocker_id=b['blocker_id'], blocker_sha256=digest(b), blocker=copy.deepcopy(b))
                   for i,b in enumerate(blockers,1)]
    occurrences[0]['directive_ordinals'] = [1]
    occurrences[1]['directive_ordinals'] = [2]
    occurrences[2]['directive_ordinals'] = [1,2,3,4]
    return dict(schema_version=1, kind='typed-uuid-directive-occurrence-discharge-proposal', policy_id=POLICY,
                root=copy.deepcopy(root), original_negative=copy.deepcopy(original_negative),
                original_negative_sha256=digest(original_negative), original_negative_unchanged=True,
                contract_sha256=digest(contract), raw_section_sha256=hashlib.sha256(raw_section).hexdigest(),
                raw_section_hex=raw_section.hex(), header=copy.deepcopy(header), binding=copy.deepcopy(uuid_binding),
                authority=copy.deepcopy(authority), directive_occurrences=spans, proposed_blocker_occurrences=occurrences,
                caller_authority_authentication_required=True, duplicate_linker_semantics_proved=False,
                library_request_proved=False, library_selection_proved=False, library_loaded_proved=False,
                library_dependencies_proved=False, ordinary_graph_closure=False, certificate_rewritten=False,
                provider_selected=False, runtime_eligible=False, ABI_verified=False, admission_approved=False,
                namespace_approved=False, full_serialization_eligible=False, materialization_approved=False,
                link_ready=False, native_tools_run=False, emission_performed=False, object_write_performed=False)
