"""Independent authored attacks on descriptor and readonly-omission extensions."""
import copy
import struct
import unittest

from test_parent_eh_adapter import valid_case
from test_parent_eh_adapter_lane08 import encode
import parent_eh_adapter as adapter


def descriptor_first(obj, count=1):
    info = struct.pack('<9I', 0x19930522, count, 0, 0, 0, 0, 0, 0, 1)
    unwind = b''.join(struct.pack('<iI', state - 1, 0) for state in range(count))
    data = info + unwind
    obj['sections'][6].update(payload=data, size=len(data),
        relocs=[(8, 25, 6)] + [(40 + 8 * state, 12, 6) for state in range(count)])
    obj['symbols'][24]['value'] = 0
    obj['symbols'][25]['value'] = 36
    aux = bytearray(obj['symbols'][22]['aux'])
    struct.pack_into('<I', aux, 0, len(data))
    struct.pack_into('<H', aux, 4, count + 1)
    obj['symbols'][22]['aux'] = bytes(aux)


def rebind(case, obj):
    case['raw'] = encode(obj)
    digest = adapter.sha(case['raw'])
    case['unit_proof']['object_sha256'] = digest
    case['contract']['provenance']['object_sha256'] = digest
    return case


class ParentEHExtensionAdversarialTests(unittest.TestCase):
    def blocked(self, case):
        result = adapter.observe_parent(**case)
        self.assertFalse(result['structural_projection_candidate'],
                         [row['code'] for row in result['blockers']])
        self.assertFalse(result['runtime_eligible'])
        return result

    def test_descriptor_first_six_states_and_exact_upper_bound(self):
        for count in (1, 6, 64):
            with self.subTest(count=count):
                result = adapter.observe_parent(**valid_case(
                    object_edit=lambda obj: descriptor_first(obj, count)))
                self.assertTrue(result['structural_projection_candidate'], result)
                semantic = result['semantic']
                self.assertEqual(len(semantic['states']), count)
                self.assertEqual(semantic['metadata_descriptors'],
                                 dict(funcinfo=[0, 36], unwind=[36, 36 + 8 * count]))
                self.assertEqual(len({s['role_id'] for s in semantic['states']}), count)
                self.assertFalse(result['frame_contract_verified'])

    def test_descriptor_padding_gaps_and_overlap_never_become_valid_states(self):
        for mutation in ('leading', 'trailing', 'gap', 'overlap'):
            with self.subTest(mutation=mutation):
                def edit(obj):
                    descriptor_first(obj)
                    section = obj['sections'][6]
                    if mutation == 'leading':
                        section['payload'] = bytes(4) + section['payload']
                        section['relocs'] = [(off + 4, index, kind)
                                             for off, index, kind in section['relocs']]
                        obj['symbols'][24]['value'] += 4
                        obj['symbols'][25]['value'] += 4
                    elif mutation in ('trailing', 'gap'):
                        section['payload'] += bytes(4)
                        if mutation == 'gap':
                            obj['symbols'][25]['value'] += 4
                    else:
                        obj['symbols'][25]['value'] = 32
                    section['size'] = len(section['payload'])
                    aux = bytearray(obj['symbols'][22]['aux'])
                    struct.pack_into('<I', aux, 0, section['size'])
                    obj['symbols'][22]['aux'] = bytes(aux)
                self.blocked(valid_case(object_edit=edit))

    @staticmethod
    def generated_data(obj, kind=6):
        obj['sections'][4]['relocs'] = [
            (off, 16 if off == 4 else index, kind if off == 4 else old_kind)
            for off, index, old_kind in obj['sections'][4]['relocs']]

    def test_generated_DATA_basis_is_physical_parent_fields_without_storage_claim(self):
        case = valid_case(object_edit=self.generated_data)
        result = adapter.observe_parent(**case)
        self.assertTrue(result['structural_projection_candidate'], result)
        field = next(f for f in result['semantic']['fields']
                     if f['section'] == 4 and f['offset'] == 4)
        basis = field['generated_data_identity_basis']
        expected = [adapter.digest(row) for row in case['contract']['fields']
                    if row['coff_relocation']['symbol_index'] == 16]
        self.assertEqual(basis['parent_field_sha256'], expected)
        self.assertFalse(basis['original_storage_adopted'])
        self.assertFalse(basis['type_extent_verified'])
        self.assertEqual(field['proof_family'], 'PARENT_OWNED_GENERATED_EH_FIELD')

    def test_same_name_and_address_cannot_borrow_other_physical_DATA_witness(self):
        case = valid_case(object_edit=self.generated_data)
        obj = adapter.coff.parse(case['raw'])
        obj['symbols'][26] = copy.deepcopy(obj['symbols'][16])
        obj['sections'][4]['relocs'] = [
            (off, 26 if off == 4 else index, kind)
            for off, index, kind in obj['sections'][4]['relocs']]
        result = self.blocked(rebind(case, obj))
        self.assertEqual(result['blockers'][0]['code'], 'MISSING_GENERATED_DATA_PARENT_WITNESS')

    def test_generated_DATA_needs_DIR32_and_parent_DATA_domain(self):
        result = self.blocked(valid_case(
            object_edit=lambda obj: self.generated_data(obj, kind=20)))
        self.assertEqual(result['blockers'][0]['code'], 'MISSING_GENERATED_DATA_PARENT_WITNESS')
        case = valid_case(object_edit=self.generated_data)
        row = next(r for r in case['contract']['fields']
                   if r['coff_relocation']['symbol_index'] == 16)
        row['classification'] = 'SELECTED_CODE_ENTRY'
        self.blocked(case)

    def test_readonly_discharge_preserves_unreviewed_BSS_and_LABEL(self):
        from test_parent_eh_omission import case as readonly_case
        for mutation, expected in (('bss', 'UNSUPPORTED_SECTION_SEMANTICS'),
                                   ('label', 'LABEL_OMISSION_NOT_PROVED')):
            with self.subTest(mutation=mutation):
                case, _, _ = readonly_case()
                obj = adapter.coff.parse(case['raw'])
                if mutation == 'bss':
                    obj['sections'][9].update(name='.bss', flags=0xc0400080)
                else:
                    obj['symbols'][73] = dict(name='$LN901', section=17, value=4,
                        type=0, storage=6, aux=b'', aux_count=0)
                    obj['symbol_count'] = 74
                result = self.blocked(rebind(case, obj))
                self.assertIn(expected, [b['code'] for b in result['blockers']])
                witness = result['expanded_readonly_omission']
                self.assertEqual(len(witness['discharge_occurrences']), 1)
                self.assertFalse(witness['original_data_storage_adopted'])


if __name__ == '__main__':
    unittest.main()
