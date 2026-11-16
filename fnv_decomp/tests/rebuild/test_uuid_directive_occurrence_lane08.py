"""Independent UUID multiplicity/header/binding attacks; authored fixtures only."""
import copy
import unittest
from unittest.mock import patch
from test_uuid_directive_occurrence_witness import fixture,repin,call,m


class UUIDOccurrenceIndependentTests(unittest.TestCase):
    def reject_rebound(self,mutate):
        a=fixture();mutate(a);repin(a)
        with self.assertRaises(ValueError):call(a)

    def test_duplicate_ids_are_distinct_injective_byte_occurrences(self):
        for address in m.ROOTS:
            a=fixture(address);w=call(a)
            first,second,whole=w['proposed_blocker_occurrences']
            self.assertEqual(first['blocker_id'],second['blocker_id'])
            self.assertEqual(first['blocker_sha256'],second['blocker_sha256'])
            self.assertEqual((first['ordinal'],second['ordinal'],whole['ordinal']),(1,2,3))
            self.assertEqual(first['directive_ordinals'],[1]);self.assertEqual(second['directive_ordinals'],[2])
            self.assertEqual(whole['directive_ordinals'],[1,2,3,4])
            one,two=w['directive_occurrences'][:2]
            self.assertLess(one['end'],two['start'])
            for occurrence in (one,two):self.assertEqual(a[3][occurrence['start']:occurrence['end']],m.UUID.encode())
            self.assertEqual(whole['blocker']['evidence'],m.TOKENS)

    def test_full_header_table_must_precede_raw_section(self):
        for key,value in (('raw_data_offset',1),('raw_data_offset',59),('raw_data_offset',6019),
                          ('section_count',31),('section_count',65536),('optional_header_size',1),
                          ('object_size',8092)):
            with self.subTest(key=key,value=value):self.reject_rebound(lambda a,k=key,v=value:a[4].__setitem__(k,v))
        a=fixture();end=20+40*a[4]['section_count'];a[4]['raw_data_offset']=end;a[4]['object_size']=end+93
        repin(a);self.assertTrue(call(a)['original_negative_unchanged'])

    def test_path_cannot_claim_uuid_for_another_library_or_control_path(self):
        for value in ('fixture/other.lib','fixture/uuid.dll','fixture/uuid.lib/','fixture/uuid.lib ',
                      'fixture/\x00/uuid.lib','fixture/\n/uuid.lib','fixture/\x7f/uuid.lib'):
            with self.subTest(path=value):self.reject_rebound(lambda a,v=value:a[5].__setitem__('path',v))
        for value in ('','fixture/selection\n.json','fixture/\x00/selection.json'):
            self.reject_rebound(lambda a,v=value:a[5].__setitem__('candidate_manifest_path',v))
        a=fixture();a[5]['path']='C:\\SDK\\Lib\\UUID.LIB';repin(a)
        self.assertIs(call(a)['library_dependencies_proved'],False)

    def test_raw_bytes_and_line_authority_cannot_be_reconstructed_from_tokens(self):
        for value in (None,b'',m.TOKENS,' '.join(m.TOKENS)):
            a=fixture();a[3]=value
            with self.assertRaises(ValueError):call(a)
        for key in ('line_number_count','line_number_pointer','section_count','optional_header_size'):
            a=fixture();a[4].pop(key);repin(a)
            with self.assertRaises(ValueError):call(a)
        a=fixture();a[6].pop('section_sha256')
        with self.assertRaises(ValueError):call(a)

    def test_real_certificate_pin_is_not_replaced_by_self_consistency(self):
        a=fixture()
        with self.assertRaisesRegex(ValueError,'original certificate pin'):m.assess(*a)

    def test_no_io_or_input_mutation_and_no_shared_duplicate_dicts(self):
        a=fixture();before=copy.deepcopy(a)
        with patch('builtins.open',side_effect=AssertionError('I/O forbidden')):w=call(a)
        self.assertEqual(a,before)
        w['proposed_blocker_occurrences'][0]['blocker']['evidence']='changed output only'
        w['header']['size']=-1;w['original_negative']['blockers'][0]['evidence']='changed copy'
        self.assertEqual(w['proposed_blocker_occurrences'][1]['blocker']['evidence'],m.UUID)
        self.assertEqual(a,before)

    def test_no_id_set_collapse_or_extra_non_uuid_occurrence(self):
        self.reject_rebound(lambda a:a[2].__setitem__('blockers',[a[2]['blockers'][0],a[2]['blockers'][2]]))
        self.reject_rebound(lambda a:a[2]['blockers'].append(dict(code='UNKNOWN_OTHER',evidence='unmodeled',blocker_id='0'*64)))
        self.reject_rebound(lambda a:a[2]['blockers'][2].__setitem__('evidence',list(reversed(m.TOKENS))))

    def test_inventory_candidate_cannot_establish_request_selection_or_load(self):
        a=fixture();w=call(a)
        self.assertEqual(w['binding']['kind'],'bound-normal-sdk-search-candidate')
        for flag in ('library_request_proved','library_selection_proved','library_loaded_proved',
                     'library_dependencies_proved','duplicate_linker_semantics_proved'):
            self.assertIs(w[flag],False)
        self.reject_rebound(lambda a:a[5].__setitem__('kind','already-selected-normal-static-library'))
        self.reject_rebound(lambda a:a[5].__setitem__('library_selected',True))
        self.reject_rebound(lambda a:a[5].__setitem__('selection_manifest_path','fixture/selected.json'))


if __name__=='__main__':unittest.main()
