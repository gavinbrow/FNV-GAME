"""V2 semantic member/field join, derived from exact COFF bytes and full proofs.

No I/O or native invocation. This is not an admission or operation authority.
"""
import application_link_actual_cohort as ledger
import application_link_cohort as cohort


def require(ok, message):
    if not ok:
        raise ValueError(message)


def exact(a, b):
    return cohort.canonical(a) == cohort.canonical(b)


def derive(*, wrappers, members, handoff, member_count, field_count, member_bytes,
           namespace_by_member, expected_providers, expected_fields, component):
    checked = ledger.verify_proof_ledger(wrappers, members, handoff,
                                         member_count=member_count, field_count=field_count)
    require(type(member_bytes) is dict and set(member_bytes) == set(checked['members']) and
            type(namespace_by_member) is dict and set(namespace_by_member) == set(checked['members']),
            'exact member bytes and namespace required')
    providers, fields = [], []
    for member in members:
        name, p = member['name'], member['projection']
        data = member_bytes[name]
        require(type(data) is bytes and cohort.digest(data) == p['output_sha256'], 'member bytes differ')
        require(len(p['requested_roots']) == 1 and len(p['exports']) == 1, 'one physical root/export per member')
        root = p['requested_roots'][0]
        require(root['object_sha256'] == p['original_object_sha256'], 'original object ancestry differs')
        obligations = []
        for compact in p['fields']:
            full = checked['fullproofs'][compact['field_proof_sha256']]
            require(full['recipe_id'] == root['recipe_id'] and
                    (full['coff_relocation']['addend'] & 0xffffffff) == compact['addend_bits'],
                    'source proof recipe/addend differs')
            obligations.append(dict(compact, physical_section=compact['section'], field_offset=compact['offset']))
        ps, fs = cohort.mapped_member(data, component=component, member=name,
            recipe_id=root['recipe_id'], object_sha256=root['object_sha256'], roots=[root],
            maps=p['maps'], namespace=namespace_by_member[name], obligations=obligations,
            retained_bases={}, expected_exports=p['exports'])
        require(len(ps) == 1 and len(fs) == len(p['fields']), 'member serialized census differs')
        # mapped_member reads the actual symbol, relocation kind/target and addend;
        # compare every complete compact proof, including unrecognized fields.
        for f in fs:
            require(type(f['undefined']) is bool and f['undefined'] and 'proof' in f,
                    'unsupported retained member relocation')
            compact = next((x for x in p['fields'] if x['section'] == f['proof']['physical_section'] and
                            x['offset'] == f['offset'] and x['symbol_index'] == f['physical_symbol_index']), None)
            require(compact is not None and exact(f['proof'], dict(compact, physical_section=compact['section'],
                    field_offset=compact['offset'])), 'full physical proof differs')
        providers.extend(ps); fields.extend(fs)
    require(len(fields) == field_count and exact(providers, expected_providers) and exact(fields, expected_fields),
            'observed provider/field records differ from actual COFF derivation')
    return dict(providers=providers, fields=fields, admission_approved=False, link_approved=False)
