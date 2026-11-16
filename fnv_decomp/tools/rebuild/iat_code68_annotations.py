"""Additive CODE68 full-proof annotations using the frozen CODE59 validators."""
import copy
import iat_field_annotations as frozen

FROZEN_HELPER_SHA256 = '5ce0b3ae5069cde206b334bddc94515b308e611ef1cc269783cbd386fd778ae6'
require = frozen.require
digest = frozen.digest
location = frozen.location


def annotate(mapped_fields, full_proofs, catalog_plan, expected_locations):
    catalog = frozen.imports.catalog(catalog_plan)
    expected = set(map(tuple, expected_locations))
    require(expected and len(expected) == len(expected_locations), 'expected CODE68 set empty or duplicated')
    selected = [r for r in mapped_fields if r['component'] == 'CODE68' and r['proof'].get('role') == 'iat-cell']
    actual = [location(r) for r in selected]
    require(len(actual) == len(set(actual)) and set(actual) == expected, 'CODE68 IAT field coverage differs')
    require(set(full_proofs) == {r['proof']['field_proof_sha256'] for r in selected}, 'CODE68 full proof coverage differs')
    result = copy.deepcopy(mapped_fields)
    for row in result:
        if row['component'] != 'CODE68' or row['proof'].get('role') != 'iat-cell':
            continue
        full = full_proofs[row['proof']['field_proof_sha256']]
        frozen.validate_full(row, full)
        base = row['proof']['original_base']; cell = catalog.get(base)
        require(cell is not None and full['import_id'] == cell['import_id'], 'CODE68 original proof/catalog identity differs')
        annotation = dict(schema_version=1, kind='exact-original-IAT-field-annotation',
            catalog_sha256=frozen.CATALOG_SHA256, original_IAT_va=base, import_id=full['import_id'],
            classification=frozen.CLASSIFICATION, dll=cell['dll'], export=cell['export'],
            field_proof_sha256=row['proof']['field_proof_sha256'], provider_selected=False, ABI_verified=False)
        for key, value in dict(original_field_proof=full, IAT_annotation=annotation,
                               import_id=full['import_id'], classification=frozen.CLASSIFICATION).items():
            require(key not in row or row[key] == value, 'existing CODE68 annotation conflicts')
            row[key] = copy.deepcopy(value)
    return result


def census_view(annotated_fields, catalog_plan):
    for row in annotated_fields:
        if row['component'] == 'CODE68' and row['proof'].get('role') == 'iat-cell':
            require('IAT_annotation' in row and 'original_field_proof' in row, 'CODE68 IAT proof not hydrated')
    return frozen.census_view(annotated_fields, catalog_plan)
