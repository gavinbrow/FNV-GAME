"""Independent namespace-group attacks on complete authored parent/EH graphs."""
import copy
import struct
import unittest

from test_eh_reference_groups_lane08 import group_case
from test_parent_eh_adapter_lane08 import encode
import parent_eh_adapter as adapter
import eh_reference_groups as groups
import parent_eh_groups_project as projector


def rebind(case, obj):
    case['raw'] = encode(obj)
    case['unit_proof']['object_sha256'] = adapter.sha(case['raw'])
    case['contract']['provenance']['object_sha256'] = adapter.sha(case['raw'])
    return case


def patch_operand(case, address, value):
    original = case['reference']
    class Reference:
        def read(self, start, size):
            data = bytearray(original.read(start, size))
            if start <= address and address + 4 <= start + size:
                struct.pack_into('<I', data, address-start, value & 0xffffffff)
            return bytes(data)
    case['reference'] = Reference()


class EHReferenceGroupAdversarialTests(unittest.TestCase):
    def observed(self, case):
        result = adapter.observe_parent(**case)
        self.assertTrue(result['structural_projection_candidate'], result)
        return result

    def test_two_three_member_groups_preserve_every_record_and_relocation(self):
        case = group_case(); result = self.observed(case)
        certificate = groups.certify(case['raw'], result, case['contract'])
        self.assertEqual(sorted(g['members'] for g in certificate['groups']),
                         [[13, 28, 29], [17, 26, 27]])
        self.assertEqual(certificate['physical_field_count'], 15)
        named = groups.namespace(case['raw'], result, case['contract'], certificate)
        before, after = adapter.coff.parse(case['raw']), adapter.coff.parse(named)
        self.assertEqual(before['sections'], after['sections'])
        self.assertEqual(before['symbol_count'], after['symbol_count'])
        for index, symbol in before['symbols'].items():
            self.assertEqual({k:v for k,v in symbol.items() if k!='name'},
                             {k:v for k,v in after['symbols'][index].items() if k!='name'})
        output, report = projector.project_parent(case, result)
        self.assertEqual(len(report['after']['fields']), 15)
        self.assertEqual(len(set(report['maps']['symbol_map'].values())),
                         len(report['maps']['symbol_map']))
        self.assertFalse(report['reference_group_certificate']['coalescing_allowed'])
        self.assertFalse(report['reference_group_certificate']['relocation_retargeting_allowed'])
        self.assertEqual(adapter.coff.exports(output), [report['export']])

    def test_complete_universe_includes_unrelated_EH_and_state_fields(self):
        case=group_case(); result=self.observed(case)
        for mutation in ('missing', 'duplicate'):
            with self.subTest(mutation=mutation):
                changed=copy.deepcopy(result)
                index=next(i for i,f in enumerate(changed['semantic']['fields'])
                           if f['proof_family']=='PARENT_OWNED_GENERATED_EH_FIELD')
                if mutation=='missing':changed['semantic']['fields'].pop(index)
                else:changed['semantic']['fields'].append(copy.deepcopy(changed['semantic']['fields'][index]))
                with self.assertRaisesRegex(ValueError,'FIELD_UNIVERSE'):
                    groups.certify(case['raw'],changed,case['contract'])

    def test_generated_EH_use_of_group_member_is_not_a_parent_field_waiver(self):
        case=group_case(); obj=adapter.coff.parse(case['raw'])
        obj['sections'][4]['relocs']=[(off,26 if off==4 else index,kind)
                                    for off,index,kind in obj['sections'][4]['relocs']]
        rebind(case,obj); address=0x20000004
        patch_operand(case,address,0x10012000-address-4)
        result=self.observed(case)
        with self.assertRaisesRegex(ValueError,'GROUP_USE_NOT_ZERO_ADDEND_PARENT_ENTRY'):
            groups.certify(case['raw'],result,case['contract'])

    def test_nonzero_addend_stays_blocked_even_when_original_bytes_match(self):
        case=group_case(); obj=adapter.coff.parse(case['raw'])
        payload=bytearray(obj['sections'][3]['payload']);struct.pack_into('<I',payload,34,1)
        obj['sections'][3]['payload']=bytes(payload);rebind(case,obj)
        row=next(r for r in case['contract']['fields'] if r['coff_relocation']['symbol_index']==27)
        row['coff_relocation']['addend']=1;row['exact_original_target_va']='0x10012001'
        patch_operand(case,0x10000000+34,0x10012001)
        result=self.observed(case)
        with self.assertRaisesRegex(ValueError,'GROUP_USE_NOT_ZERO_ADDEND_PARENT_ENTRY'):
            groups.certify(case['raw'],result,case['contract'])

    def test_defined_physical_member_cannot_enter_an_undefined_reference_group(self):
        case=group_case();obj=adapter.coff.parse(case['raw']);obj['symbols'][26]['section']=17
        rebind(case,obj)
        row=next(r for r in case['contract']['fields'] if r['coff_relocation']['symbol_index']==26)
        row['coff_relocation']['symbol_section']=17
        result=self.observed(case)
        with self.assertRaisesRegex(ValueError,'MEMBER_IS_NOT_UNDEFINED_FUNCTION'):
            groups.certify(case['raw'],result,case['contract'])

    def test_all_omitted_physical_uses_are_reported_without_becoming_runtime_roots(self):
        case=group_case();obj=adapter.coff.parse(case['raw'])
        obj['sections'][17]['relocs']=[(4,26,20)]
        aux=bytearray(obj['symbols'][66]['aux']);struct.pack_into('<H',aux,4,1)
        obj['symbols'][66]['aux']=bytes(aux);rebind(case,obj)
        result=self.observed(case);certificate=groups.certify(case['raw'],result,case['contract'])
        group=next(g for g in certificate['groups'] if 26 in g['members'])
        omitted=[f for f in group['all_physical_uses'] if not f['retained']]
        self.assertEqual(omitted,[dict(section=17,offset=4,target_index=26,kind=20,retained=False)])
        self.assertEqual(len(group['fields']),3)

    def test_any_group_or_graph_certificate_drift_prevents_name_writes(self):
        case=group_case();result=self.observed(case)
        certificate=groups.certify(case['raw'],result,case['contract'])
        for mutation in ('members','fields','states','safeseh','retention','associations'):
            with self.subTest(mutation=mutation):
                bad=copy.deepcopy(certificate)
                if mutation=='members':bad['groups'][0]['members'].pop()
                elif mutation=='fields':bad['groups'][0]['fields'].pop()
                elif mutation=='states':bad['states_sha256']='0'*64
                elif mutation=='safeseh':bad['safeseh_sha256']='0'*64
                elif mutation=='retention':bad['retained_primary_indices'].pop()
                else:bad['associations'][0]['aux'][0]+=1
                with self.assertRaisesRegex(ValueError,'STALE_OR_FORGED'):
                    groups.namespace(case['raw'],result,case['contract'],bad)


if __name__=='__main__':unittest.main()
