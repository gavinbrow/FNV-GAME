"""Independent two-group authored EH fixture and namespace attacks."""
import copy
import struct
import unittest

from test_parent_eh_adapter import valid_case
from test_parent_eh_adapter_lane08 import encode
import parent_eh_adapter as adapter


def group_case():
    case = valid_case()
    obj = adapter.coff.parse(case['raw'])
    additions = [(25, 26, 20, 0x10012000), (34, 27, 6, 0x10012000),
                 (78, 28, 20, 0x10011000), (88, 29, 6, 0x10011000)]
    for offset, index, kind, base in additions:
        name = '_authored_alias_' + str(index)
        obj['symbols'][index] = dict(name=name, section=0, value=0, type=32,
                                    storage=2, aux_count=0, aux=b'')
        obj['sections'][3]['relocs'].append((offset, index, kind))
        case['recipe']['symbols'][name] = hex(base)
        case['contract']['fields'].append(dict(recipe_id=case['contract']['recipe_id'],
            function_va='0x10000000', physical_section=3, physical_offset=offset,
            source_field_offset=offset, original_field_va='0x%08x' % (0x10000000 + offset),
            coff_relocation=dict(offset=offset, symbol_index=index, kind=kind, width=4,
                symbol=name, symbol_section=0, symbol_value=0, symbol_type=32,
                symbol_storage=2, addend=0), derived_source_symbol_base_va=hex(base),
            exact_original_target_va=hex(base), expected_original_target_va=hex(base),
            physical_field_overlap_count=1, proof_consistency='EXACT_OWN_SOURCE_RESOLUTION',
            classification='SELECTED_CODE_ENTRY', code_ownership_ambiguous=False,
            code_owners=[dict(address='0x%08x' % base, offset=0)]))
        if kind == 6:
            case['original_highlow_sites'].append(0x10000000 + offset)
    obj['sections'][3]['relocs'].sort()
    aux = bytearray(obj['symbols'][6]['aux'])
    struct.pack_into('<H', aux, 4, len(obj['sections'][3]['relocs']))
    obj['symbols'][6]['aux'] = bytes(aux)
    case['raw'] = encode(obj)
    case['unit_proof']['object_sha256'] = case['contract']['provenance']['object_sha256'] = adapter.sha(case['raw'])
    case['unit_proof']['recipe_unit_sha256'] = adapter.digest(case['recipe'])
    for row in case['contract']['fields']:
        if row['classification'] == 'SELECTED_CODE_ENTRY':
            base = int(row['derived_source_symbol_base_va'], 16)
            row['code_ownership_ambiguous'] = False
            row['code_owners'] = [dict(address='0x%08x' % base, offset=0)]
            row['expected_original_target_va'] = '0x%08x' % base
            row['coff_relocation']['width'] = 4
    original = case['reference']

    class Reference:
        def read(self, address, size):
            data = bytearray(original.read(address, size))
            for offset, _, kind, base in additions:
                field = 0x10000000 + offset
                if address <= field and field + 4 <= address + size:
                    operand = base if kind == 6 else base - field - 4
                    struct.pack_into('<I', data, field - address, operand & 0xffffffff)
            return bytes(data)

    case['reference'] = Reference()
    return case


class EHReferenceGroupFixtureTests(unittest.TestCase):
    def test_two_three_member_groups_have_complete_fifteen_field_EH_graph(self):
        case = group_case()
        result = adapter.observe_parent(**case)
        self.assertTrue(result['structural_projection_candidate'], result)
        self.assertEqual(len(result['semantic']['fields']), 15)
        for indices in ({17, 26, 27}, {13, 28, 29}):
            fields = [f for f in result['semantic']['fields'] if f['target_index'] in indices]
            self.assertEqual({f['target_index'] for f in fields}, indices)
            self.assertEqual(len({f['original_base'] for f in fields}), 1)
        self.assertFalse(result['runtime_eligible'])


if __name__ == '__main__':
    unittest.main()
