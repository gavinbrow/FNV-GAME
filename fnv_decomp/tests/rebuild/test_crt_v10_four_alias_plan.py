from pathlib import Path
import sys
import unittest
import copy
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import crt_v10_four_alias_plan as plan

class V10MemberProofTests(unittest.TestCase):
    def fixture(self):
        root=dict(recipe_id='recipe',original_address='0x00401030')
        full=dict(recipe_id='recipe',coff_relocation=dict(addend=0),runtime_eligible=False)
        compact=dict(field_proof_sha256=plan.old.digest(full),addend_bits=0,
            original_base='0x00401020',canonical_name='ordinary-code')
        member=dict(name='ordinary.obj',projection=dict(requested_roots=[root],fields=[compact]))
        return [member],{'envelopes':'unchanged'},dict(records=['unchanged']),{plan.old.digest(full):full}
    def call(self,bundle):
        m,e,h,n=bundle
        with patch.object(plan.wave10,'verify_proof_ledger',return_value=n) as verify:
            out=plan.member_proofs(m,e,h);verify.assert_called_once_with(e,m,h)
            return out
    def test_shared_join_reused_and_false_flags_retained(self):
        b=self.fixture();out=self.call(b)
        self.assertEqual(out[0]['normative_record'],next(iter(b[3].values())))
        self.assertFalse(out[0]['normative_record']['runtime_eligible'])
    def test_unmatched_source_recipe_rejected(self):
        b=self.fixture();b[0][0]['projection']['requested_roots'][0]['recipe_id']='other'
        with self.assertRaises(ValueError):self.call(b)
    def test_existing_CRT_base_in_any_role_is_not_ignored(self):
        b=self.fixture();b[0][0]['projection']['fields'][0]['original_base']='0x011c16bc'
        with self.assertRaises(ValueError):self.call(b)
    def test_existing_canonical_key_is_not_ignored(self):
        b=self.fixture();b[0][0]['projection']['fields'][0]['canonical_name']=plan.old.undefined('0x011c16bc','data')
        with self.assertRaises(ValueError):self.call(b)
    def test_addend_identity_retained(self):
        b=self.fixture();b[0][0]['projection']['fields'][0]['addend_bits']=1
        with self.assertRaises(ValueError):self.call(b)

class V10FieldTests(unittest.TestCase):
    def fixture(self):
        root=dict(recipe_id='recipe',original_address='0x00401030',object_sha256='source')
        projection=dict(requested_roots=[root],original_object_sha256='source',output_sha256='member',exports=['caller'],
            maps=dict(section_map={'11':2},symbol_map={'39':8}),undefined=[dict(serialized_symbol_index=8)])
        members=[dict(name='member.obj',projection=projection)];joined=[];fields=[]
        for i in range(629):
            raw=dict(section=11,offset=i*4,symbol_index=39,kind=20,canonical_name='ordinary-code',field_proof_sha256=str(i))
            full=dict(unknown=False,index=i)
            joined.append(dict(member='member.obj',compact=raw,normative_record=full))
            fields.append(dict(component='CODE68',member='member.obj',root='0x00401030',recipe_id='recipe',
                object_sha256='source',member_sha256='member',caller='caller',canonical='ordinary-code',kind=20,
                section=2,offset=i*4,physical_symbol_index=39,symbol_index=8,undefined=True,
                proof=dict(raw,physical_section=11,field_offset=i*4)))
        baseline=[dict(old=dict(full_annotation='unchanged'))]
        return baseline,copy.deepcopy(baseline)+fields,members,joined
    def test_all629_maps_and_old_annotations_preserved(self):
        self.assertEqual(len(plan.new_fields(*self.fixture())),629)
    def test_old_raw_annotation_change_rejected(self):
        b=self.fixture();b[1][0]['old']['full_annotation']='changed'
        with self.assertRaises(ValueError):plan.new_fields(*b)
    def test_wrong_serialized_slot_rejected(self):
        b=self.fixture();b[1][-1]['symbol_index']=9
        with self.assertRaises(ValueError):plan.new_fields(*b)
    def test_optional_hydration_must_equal_normative_source(self):
        b=self.fixture();b[1][-1]['original_field_proof']={'unknown':'changed'}
        with self.assertRaises(ValueError):plan.new_fields(*b)
    def test_unknown_fields_cannot_be_silently_dropped(self):
        b=self.fixture();b[1].pop()
        with self.assertRaises(ValueError):plan.new_fields(*b)

if __name__=='__main__':unittest.main()
