import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import crt_v14_four_alias_plan as plan

class V14DraftTests(unittest.TestCase):
    def fixture(self):
        before=[dict(old=dict(unknown=False))]
        uuid=[dict(component='qualified-uuid',root='uuid-root',canonical='uuid'+str(i),offset=i,
            proof=dict(role='code' if i<7 else 'data',original_base='unapproved'+str(i),unknown=False)) for i in range(9)]
        ordinary=[dict(component='accepted-subset',root='emitted-root',canonical='ordinary',proof={'unknown':False})]
        actual=dict(complete_field_count=11,all21_component='accepted-subset',uuid_component='qualified-uuid',
            all21_roots=['emitted-root','zero-field-emitted-root'],uuid_root='uuid-root')
        return before,copy.deepcopy(before)+ordinary+uuid,actual
    def test_actual_subset_and_zero_field_owner_do_not_assume_requested46(self):
        self.assertEqual(len(plan.cohort_delta(*self.fixture())),10)
    def test_requested_but_unaccepted_root_rejected(self):
        b=self.fixture();b[1][1]['root']='requested-only-root'
        with self.assertRaises(ValueError):plan.cohort_delta(*b)
    def test_unknown_old_flags_are_not_normalized(self):
        b=self.fixture();b[1][0]['old']['unknown']=True
        with self.assertRaises(ValueError):plan.cohort_delta(*b)
    def test_saved_tuple_and_list_forms_compare_as_complete_JSON(self):
        b=self.fixture();b[0][0]['saved']=(1,False,{'unknown':'retained'})
        b[1][0]['saved']=[1,False,{'unknown':'retained'}]
        self.assertEqual(len(plan.cohort_delta(*b)),10)
    def test_boolean_unknown_is_not_replaced_by_numeric_zero(self):
        b=self.fixture();b[1][0]['old']['unknown']=0
        with self.assertRaises(ValueError):plan.cohort_delta(*b)
    def test_uuid_roles_and_nine_full_fields_are_required(self):
        b=self.fixture();b[1][-1]['proof']['role']='code'
        with self.assertRaises(ValueError):plan.cohort_delta(*b)
    def test_input_mismatch_stops_before_artifact_parsing(self):
        with patch.object(plan.old,'sha',side_effect=ValueError('input mismatch')):
            with self.assertRaisesRegex(ValueError,'input mismatch'):plan.prepare()
    def test_UUID_comparison_retains_all_fields_and_JSON_tuple_semantics(self):
        self.assertTrue(plan.same_record_multiset([{'original_field_proof':{'unknown':(False,1)},'normative_field':{'role':'data'}}],
            [{'original_field_proof':{'unknown':[False,1]},'normative_field':{'role':'data'}}]))
        self.assertFalse(plan.same_record_multiset([{'original_field_proof':{'unknown':False},'normative_field':{'role':'data'}}],
            [{'original_field_proof':{'unknown':0},'normative_field':{'role':'data'}}]))

if __name__=='__main__':unittest.main()
