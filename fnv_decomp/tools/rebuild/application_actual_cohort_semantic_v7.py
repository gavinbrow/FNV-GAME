"""V7 semantic member/field join, derived from exact COFF bytes and full proofs.

No I/O or native invocation. This is not an admission or operation authority.
"""
import application_link_actual_cohort as ledger
import application_link_cohort as cohort
import runtime_code_pool as pool


def require(ok, message):
    if not ok:
        raise ValueError(message)


def exact(a, b):
    return cohort.canonical(a) == cohort.canonical(b)


def derive(*, wrappers, members, handoff, member_count, field_count, member_bytes,
           namespace_by_member, expected_providers, expected_fields, component, selected_providers):
    checked = ledger.verify_proof_ledger(wrappers, members, handoff,
                                         member_count=member_count, field_count=field_count)
    require(type(member_bytes) is dict and set(member_bytes) == set(checked['members']) and
            type(namespace_by_member) is dict and set(namespace_by_member) == set(checked['members']),
            'exact member bytes and namespace required')
    require(type(selected_providers) is dict, 'complete authenticated selected provider map required')
    providers, fields = [], []
    for member in members:
        name, p = member['name'], member['projection']
        data = member_bytes[name]
        require(type(data) is bytes and cohort.digest(data) == p['output_sha256'], 'member bytes differ')
        require(len(p['requested_roots']) == 1 and len(p['exports']) == 1, 'one physical root/export per member')
        root = p['requested_roots'][0]
        require(root['object_sha256'] == p['original_object_sha256'], 'original object ancestry differs')
        obligations = []
        occupied = set()
        for compact in p['fields']:
            full = checked['fullproofs'][compact['field_proof_sha256']]
            require(type(compact['section']) is int and type(compact['offset']) is int and
                    compact['section'] > 0 and compact['offset'] >= 0, 'physical field range differs')
            span={(compact['section'], compact['offset']+i) for i in range(4)}
            require(not occupied.intersection(span), 'overlapping physical relocation fields')
            occupied.update(span)
            cr=full['coff_relocation']
            require(full.get('physical_field_overlap_count') == 1 and type(full.get('physical_field_overlap_count')) is int and
                    cr.get('width') == 4 and type(cr.get('width')) is int and
                    full['recipe_id'] == root['recipe_id'] and type(cr['addend']) is int and
                    (cr['addend'] & 0xffffffff) == compact['addend_bits'], 'source proof recipe/addend differs')
            require(full.get('expected_original_target_va') == full.get('exact_original_target_va') == compact['original_target'] and
                    full.get('derived_source_symbol_base_va') == compact['original_base'] and
                    full.get('source_resolution_basis') == 'OWN_RECIPE_BINDING' and
                    full.get('proof_consistency') == 'EXACT_OWN_SOURCE_RESOLUTION' and
                    full.get('function_symbol') == root['symbol'] and
                    type(full.get('recipe_index')) is int and full['recipe_index'] == root['recipe_index'] and
                    type(full.get('source_field_offset')) is int and type(full.get('original_operand')) is int and
                    0 <= full['original_operand'] <= 0xffffffff and
                    type(cr.get('kind')) is int and cr['kind'] in (6,20), 'source target ancestry differs')
            field_va=int(root['original_address'],16)+full['source_field_offset']
            require(0 <= field_va <= 0xffffffff and full.get('original_field_va') == '0x%08x' % field_va and
                    ((full['original_operand'] + (field_va+4 if cr['kind']==20 else 0)) & 0xffffffff) ==
                    int(compact['original_target'],16), 'source operand target differs')
            role=compact['role']; cls=full.get('classification'); base=compact['original_base']; target=compact['original_target']
            require(full.get('code_ownership_ambiguous') is False and type(full.get('code_owners')) is list,
                    'ownership observation required')
            if role == 'code':
                require(cls in ('SELECTED_CODE_ENTRY','UNSELECTED_EXECUTABLE_TARGET_UNCLASSIFIED') and
                        cr.get('symbol_type') == 32, 'code classification differs')
                if cls == 'SELECTED_CODE_ENTRY':
                    require(target == base and full['code_owners'] == [dict(address=base,offset=0)] and
                            base in selected_providers, 'selected CODE ownership differs')
                    canonical=pool.canonical(selected_providers[base])
                else:
                    require(not full['code_owners'] and base not in selected_providers and target not in selected_providers,
                            'unselected CODE ownership differs')
                    canonical=pool.unresolved(base,role)
            else:
                allowed={'data':('ORIGINAL_IMAGE_DATA_REQUIRES_CANONICAL_OWNER','COMPILER_LITERAL_FULL_READONLY_NONPOINTER_EQUALITY'),
                         'iat-cell':('IAT_POINTER_CELL_NOT_FUNCTION_BODY',),
                         'crt-contract':('EXPLICIT_NORMAL_CRT_CONTRACT_CANDIDATE',)}
                require(role in allowed and cls in allowed[role] and not full['code_owners'] and
                        base not in selected_providers and target not in selected_providers and
                        cr.get('symbol_type') == (32 if role == 'crt-contract' else 0),
                        'non-CODE role/classification/owner differs')
                if role == 'iat-cell':
                    require(type(full.get('import_id')) is int and full['import_id'] >= 0 and
                            full.get('import_pointer_source_conflict') is not True, 'IAT source identity differs')
                canonical=pool.unresolved(base,role)
            require(compact['canonical_name'] == canonical, 'source canonical symbol differs')
            obligations.append(dict(compact, physical_section=compact['section'], field_offset=compact['offset']))
        ps, fs = cohort.mapped_member(data, component=component, member=name,
            recipe_id=root['recipe_id'], object_sha256=root['object_sha256'], roots=[root],
            maps=p['maps'], namespace=namespace_by_member[name], obligations=obligations,
            retained_bases={}, expected_exports=p['exports'])
        require(len(ps) == 1 and len(fs) == len(p['fields']), 'member serialized census differs')
        # mapped_member reads the actual symbol, relocation kind/target and addend;
        # compare every complete compact proof, including unrecognized fields.
        parsed=cohort.coff.parse(data)
        for f in fs:
            require(type(f['undefined']) is bool and f['undefined'] and 'proof' in f,
                    'unsupported retained member relocation')
            compact = next((x for x in p['fields'] if x['section'] == f['proof']['physical_section'] and
                            x['offset'] == f['offset'] and x['symbol_index'] == f['physical_symbol_index']), None)
            require(compact is not None and exact(f['proof'], dict(compact, physical_section=compact['section'],
                    field_offset=compact['offset'])), 'full physical proof differs')
            full=checked['fullproofs'][compact['field_proof_sha256']]
            target=parsed['symbols'][f['symbol_index']]
            require(type(full['coff_relocation'].get('symbol_type')) is int and
                    target['type'] == full['coff_relocation']['symbol_type'] and
                    target['storage'] == 2 and target['section'] == 0, 'serialized target type differs')
        providers.extend(ps); fields.extend(fs)
    require(len(fields) == field_count and exact(providers, expected_providers) and exact(fields, expected_fields),
            'observed provider/field records differ from actual COFF derivation')
    return dict(providers=providers, fields=fields, admission_approved=False, link_approved=False)
