"""Pure CODE56 collision-exclusion successor; no application selection.

The caller authenticates input bytes and the independent handoff review before
publication. This module reads no files, imports no producer, and emits no COFF.
"""
import copy
import hashlib
import json
import re

PARENT_SHA256 = '934aa32fd6945ab28a364beba623e347c6c9311120e057e36e126a7d67a3ea7e'
HANDOFF_SHA256 = '5150b751ae74e19c7850ddcc8608f0935afea984d22b907d950154963a0debcb'
MEMBERS_SHA256 = '5c39833286b1b37f3fcbf9f483daaa8f5852b3bfc1620b9bb2b0732d2fd2581d'
FALSE = ('provider_selected', 'runtime_eligible', 'ABI_verified', 'link_ready',
         'application_manifest_adopted', 'executable_link_performed',
         'game_execution_performed', 'native_tools_run', 'code_emission_performed')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def physical(value):
    require(type(value) is dict and set(value) == {'recipe_id', 'object_sha256', 'symbol_index'},
            'exact namespace identity required')
    require(type(value['recipe_id']) is str and value['recipe_id'] and
            type(value['object_sha256']) is str and
            re.fullmatch('[0-9a-f]{64}', value['object_sha256']) and
            type(value['symbol_index']) is int and value['symbol_index'] >= 0,
            'invalid namespace identity')
    return '_fnv_code_' + digest(value)


def census(records):
    names, addresses = set(), set()
    ordinary = set()
    for record in records:
        name, address = record['canonical'], record['original_address']
        require(name == physical(record['namespace_identity']) and name not in names,
                'duplicate or incorrect namespace canonical')
        physical(record['origin_identity'])
        require(type(address) is str and re.fullmatch('0x[0-9a-f]{8}', address) and
                address not in addresses, 'duplicate or invalid original address')
        require(record['category'] in ('ordinary', 'application-candidate'), 'unknown exclusion category')
        names.add(name)
        addresses.add(address)
        if record['category'] == 'ordinary':
            ordinary.add(name)
    return sorted(names), sorted(ordinary)


def build(parent, handoff, members):
    """Append every accepted export, preserving every historical record verbatim.

    This is a metadata consistency transform, not independent producer replay.
    Authority is supplied by a separately reviewed caller with exact raw hashes.
    """
    require(type(parent.get('schema_version')) is int and parent['schema_version'] == 6 and
            parent.get('kind') == 'prepared-CODE-collision-exclusions', 'parent schema differs')
    require(parent.get('ordinary_prepared_count') == 14472 and
            parent.get('collision_exclusion_count') == 14478 and
            len(parent['records']) == 14478 and parent.get('broader_application_candidate_count') == 6,
            'parent count differs')
    require(parent.get('application_selected_code_count') is None and
            parent.get('application_selection_inferred_from_counts') is False and
            'application_manifest_adopted' not in parent, 'parent application state differs')
    old_names, old_ordinary = census(parent['records'])
    require(old_names == parent['exclusion_names'] and old_ordinary == parent['ordinary_names'] and
            len(old_ordinary) == 14472, 'parent full namespace census differs')
    require(type(handoff.get('schema_version')) is int and handoff['schema_version'] == 1 and
            handoff.get('kind') == 'accepted-prepared-CODE-export-handoff' and
            handoff.get('requires_successor_exclusion_epoch') is True and
            handoff.get('new_distinct_exports') == 56 and len(handoff['records']) == 56 and
            handoff.get('upstream_ordinary_prepared_count') == 14472 and
            handoff.get('upstream_collision_exclusion_count') == 14478 and
            handoff.get('successor_ordinary_prepared_count') == 14528 and
            handoff.get('successor_collision_exclusion_count') == 14534 and
            handoff.get('full_field_proof_rows') == 290, 'handoff scope differs')
    require(all(handoff.get(k) is False for k in ('application_cohort_adopted',
            'application_manifest_adopted', 'provider_selected', 'runtime_eligible',
            'ABI_verified', 'link_ready')), 'handoff promotion differs')
    require(type(members) is list and len(members) == 56, 'complete member ledger required')
    by_name = {row['name']: row['projection'] for row in members}
    require(len(by_name) == 56, 'duplicate member name')
    records = copy.deepcopy(parent['records'])
    field_count = 0
    for ordinal, row in enumerate(handoff['records'], 1):
        root = row['root']
        p = by_name[row['member']]
        namespace = {k: root[k] for k in ('recipe_id', 'object_sha256', 'symbol_index')}
        require(physical(namespace) == row['canonical'] and p['requested_roots'] == [root] and
                p['exports'] == [row['canonical']] and p['output_sha256'] == row['member_sha256'] and
                p['authority'] == row['authority'] and
                all(p[k] == row[k] for k in ('certificate_sha256', 'contract_identity_sha256')),
                'member root/canonical/authority differs')
        require(type(row['field_proof_ordinal']) is int and row['field_proof_ordinal'] == ordinal and
                type(row['fields']) is int and row['fields'] == len(p['fields']) and
                p['maps']['section_map'][str(root['section'])] == row['serialized_section'] and
                p['maps']['symbol_map'][str(root['symbol_index'])] == row['serialized_symbol_index'],
                'field ordinal/count or serialized root maps differ')
        field_count += row['fields']
        records.append(dict(canonical=row['canonical'], original_address=root['original_address'],
            category='ordinary', cohort='V12-cache-qualified-native-positive-56',
            identity_mode='original-selected-physical', namespace_identity=namespace,
            origin_identity=copy.deepcopy(namespace), logical_binding_applied=True,
            member=row['member'], member_sha256=row['member_sha256'],
            original_root=copy.deepcopy(root), serialization_maps=copy.deepcopy(p['maps']),
            serialized_section=row['serialized_section'], serialized_symbol_index=row['serialized_symbol_index'],
            source_ledger_sha256=HANDOFF_SHA256, source_record_ordinal=ordinal,
            source_record_sha256=digest(row), member_ledger_sha256=MEMBERS_SHA256,
            full_field_proof_ledger_sha256=handoff['field_proofs']['sha256'],
            field_proof_ordinal=ordinal, field_proof_record_sha256=row['field_proof_record_sha256'],
            original_fields_sha256=row['original_fields_sha256'], original_field_count=row['fields']))
    names, ordinary = census(records)
    require(field_count == 290 and len(names) == 14534 and len(ordinary) == 14528,
            'complete successor census differs')
    result = copy.deepcopy(parent)
    result.update(schema_version=7, policy_id='prepared-CODE56-successor-v1',
                  parent_manifest_sha256=PARENT_SHA256, records=records,
                  exclusion_names=names, ordinary_names=ordinary,
                  ordinary_prepared_count=14528, collision_exclusion_count=14534,
                  successor_handoff_sha256=HANDOFF_SHA256, successor_member_ledger_sha256=MEMBERS_SHA256,
                  successor_export_count=56, successor_field_count=290,
                  historical_records_preserved=True, fresh_original_stability_verified=False)
    # Deliberately preserve the ABSENCE of an application adoption flag: unknown.
    require('application_manifest_adopted' not in result and
            result['records'][:14478] == parent['records'], 'historical scope changed')
    return result


def from_bytes(parent_bytes, handoff_bytes, member_bytes):
    for value, expected in ((parent_bytes, PARENT_SHA256), (handoff_bytes, HANDOFF_SHA256),
                            (member_bytes, MEMBERS_SHA256)):
        require(hashlib.sha256(value).hexdigest() == expected, 'fixed input SHA differs')
    return build(json.loads(parent_bytes), json.loads(handoff_bytes), json.loads(member_bytes))
