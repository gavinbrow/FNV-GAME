"""Consume accepted singleton COMDAT evidence without replaying original policy.

The caller pins saved producer/review/source files before importing this module.
Only the derived archive member is parsed here. The original negative certificate
remains negative; saved composition authentication is not fresh ownership proof.
"""
import hashlib
import struct

import comdat_any_frontier_factory as factory

coff = factory.base.coff
require = factory.require
digest = factory.digest
DIRECTIVES = b'   /DEFAULTLIB:"LIBCMT" /DEFAULTLIB:"OLDNAMES" '
FALSE_FLAGS = ('ABI_verified', 'provider_selected', 'runtime_eligible',
               'materialization_approved', 'namespace_approved', 'link_ready',
               'global_link_uniqueness_proved', 'compiler_performed',
               'executable_link_performed', 'game_execution_performed')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify_member(data, projection, evidence):
    """Check derived physical bytes against an authenticated saved witness."""
    p = projection
    root = evidence['root']
    w = evidence['witnesses'][0]['observation']
    require(p['requested_roots'] == [root] and p['original_object_sha256'] == root['object_sha256'],
            'typed root/original object differs')
    require(p['observer_record_sha256'] == digest(evidence) and
            p['authority'] == evidence['authority'] and
            p['central_record_sha256'] == evidence['source_record_sha256'],
            'typed observer/authority ancestry differs')
    identities = {
        'original_negative_certificate_sha256': digest(evidence['original_negative_certificate']),
        'composed_certificate_sha256': digest(evidence['composed']),
        'definition_census_sha256': digest(evidence['witnesses'][0]['definition_census']),
        'contract_identity_sha256': evidence['contract_identity_sha256'],
    }
    require(all(p[k] == v for k, v in identities.items()), 'typed certificate/census differs')
    require(all(p.get(k) is False for k in FALSE_FLAGS) and
            p.get('original_negative_certificate_preserved') is True and
            p.get('selection2_auxiliary_preserved') is True and
            p.get('selection_rewritten') is False and p.get('serialization_performed') is True,
            'typed projection scope was promoted')
    require(sha(data) == p['output_sha256'] and p['fields'] == p['undefined'] == [] and
            w['root_relocations'] == [], 'typed member hash/zero-field scope differs')
    name = factory.base.pool.canonical(factory.observer.selector.root_identity(root))
    require(p['exports'] == [name] and p['namespace_bindings'] == [[root['symbol_index'], name]] and
            p['comparison_base_view'] == {name: root['original_address']},
            'typed exact canonical binding differs')
    obj = coff.parse(data)
    sections = obj['sections']; symbols = obj['symbols']; maps = p['maps']
    sm = {int(k): v for k, v in maps['section_map'].items()}
    ym = {int(k): v for k, v in maps['symbol_map'].items()}
    am = {int(k): v for k, v in maps['auxiliary_map'].items()}
    require(len(sm) == len(sections) == 2 and set(sm.values()) == set(sections) and
            len(ym) == len(symbols) and set(ym.values()) == set(symbols) and
            len(am) == sum(s['aux_count'] for s in symbols.values()) == 2 and
            len(set(am.values())) == 2 and maps['undefined_conversions'] == [],
            'typed complete section/primary/auxiliary bijections differ')
    require(sorted(set(ym) | set(am)) == w['retained_physical_slots'] and
            not (set(ym) & set(am)), 'typed retained original physical slots differ')
    sec = sections[sm[root['section']]]
    require(sec['name'] == w['root_section_name'] and sec['size'] == w['root_section_extent'] == root['size'] and
            sec['flags'] == w['root_section_flags'] and sec['relocs'] == [] and
            sha(sec['payload']) == w['root_payload_sha256'], 'typed CODE payload/header differs')
    target = symbols[ym[root['symbol_index']]]
    require(target['name'] == name and target['section'] == sm[root['section']] and
            target['value'] == root['value'] and target['storage'] == 2 and target['type'] == 0x20 and
            target['aux_count'] == 0, 'typed exported physical symbol differs')
    definition_index = w['root_section_definition_symbol_index']
    definition = symbols[ym[definition_index]]
    require(definition['section'] == sm[root['section']] and definition['name'] == sec['name'] and
            definition['value'] == 0 and definition['storage'] == 3 and definition['type'] == 0 and
            definition['aux_count'] == 1 and am[definition_index + 1] == ym[definition_index] + 1 and
            list(struct.unpack('<IHHIhBBH', definition['aux'])) == w['root_section_auxiliary'] and
            w['root_section_auxiliary'][5] == 2, 'typed Selection2/checksum/owner differs')
    directives = [s for i, s in sections.items() if i != sm[root['section']]]
    require(len(directives) == 1 and directives[0]['name'] == '.drectve' and
            directives[0]['flags'] == 0x100a00 and directives[0]['payload'] == DIRECTIVES and
            directives[0]['size'] == len(DIRECTIVES) == 47 and directives[0]['relocs'] == [],
            'typed retained default-library directive payload differs')
    require([s['name'] for s in symbols.values() if s['storage'] == 2 and s['section'] > 0] == [name] and
            not any(s['section'] == 0 and s['storage'] == 2 for s in symbols.values()),
            'typed hidden exports/undefined dependencies')
    for key, symbol in [('before_comparison', root['symbol']), ('after_comparison', name)]:
        rows = p[key]
        require(len(rows) == 1 and rows[0]['address'] == root['original_address'] and
                rows[0]['symbol'] == symbol and rows[0]['size'] == root['size'] and
                rows[0]['compiled_extent'] == root['size'] and rows[0]['verdict'] == 'match' and
                rows[0]['errors'] == rows[0]['relocations'] == [], 'saved plain comparison differs')
    return dict(canonical=name, original_address=root['original_address'], recipe_id=root['recipe_id'],
                object_sha256=root['object_sha256'], symbol_index=root['symbol_index'],
                serialized_symbol_index=ym[root['symbol_index']], serialized_section=sm[root['section']],
                value=root['value'], size=root['size'])


def consume(observer_receipt, rows, request, handoff, members, archive_bytes):
    """Authenticate the complete saved set and its single typed derived member."""
    selected, ledger = factory.select_eligible(observer_receipt, rows, request)
    require(len(selected) == len(members) == len(handoff['records']) == 1 and
            handoff.get('kind') == 'accepted-typed-COMDAT-CODE-export-handoff' and
            handoff.get('schema_version') == 1 and handoff.get('original_negative_certificates_preserved') is True and
            handoff.get('selection2_auxiliaries_preserved') is True and handoff.get('selection_rewritten') is False,
            'singleton typed handoff required')
    item = selected[0]; evidence = rows[item['observer_ordinal'] - 1]
    member = members[0]; p = member['projection']; h = handoff['records'][0]
    require(h['root'] == item['root'] and h['authority'] == item['authority'] and
            h['member'] == member['name'] and h['member_sha256'] == p['output_sha256'] and
            h['observer_record_sha256'] == item['observer_record_sha256'] and
            all(h[k] == p[k] for k in ('original_object_sha256', 'original_negative_certificate_sha256',
                'composed_certificate_sha256', 'contract_identity_sha256', 'definition_census_sha256')),
            'typed handoff/member evidence join differs')
    require(sha(archive_bytes) == handoff['archive']['sha256'], 'typed archive identity differs')
    archive = coff.read_archive(archive_bytes)
    require(len(archive['members']) == 1 and archive['members'][0][0] == member['name'],
            'typed archive complete membership differs')
    provider = verify_member(archive['members'][0][1], p, evidence)
    require(h['canonical'] == provider['canonical'] and h['fields'] == h['undefined_records'] == 0 and
            h['serialized_symbol_index'] == provider['serialized_symbol_index'] and
            h['serialized_section'] == provider['serialized_section'], 'typed handoff physical export differs')
    provider.update(component='COMDAT1', member=member['name'])
    return dict(provider=provider, fields=[], observer_ledger=ledger,
                saved_evidence_authenticated=True, fresh_original_policy_replayed=False,
                original_negative_certificate_preserved=True, runtime_approved=False)
