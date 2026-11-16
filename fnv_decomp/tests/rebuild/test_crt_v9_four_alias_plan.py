import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import crt_v9_four_alias_plan as plan

class V9PlanTests(unittest.TestCase):
    def fixture(self):
        members=[];fields=[]
        for root in ('0x004f8ac0','0x005d43c0','0x0096aaf0'):
            name=root+'.obj';raws=[];symbols={};sections={};caller='caller'+root
            projection=dict(requested_roots=[dict(original_address=root,recipe_id='recipe',object_sha256='o')],
                fields=raws,maps=dict(symbol_map=symbols,section_map=sections),exports=[caller],
                output_sha256='m',original_object_sha256='o')
            members.append(dict(name=name,projection=projection))
            for (r,offset),(base,section,physical,serialized,sha) in plan.EXPECTED.items():
                if r!=root:continue
                raw=dict(original_base=base,original_target=base,role='code',section=section,symbol_index=physical,
                    offset=offset,kind=20,addend_bits=0,field_proof_sha256=sha,canonical_name='code'+base)
                raws.append(raw);symbols[str(physical)]=serialized;sections[str(section)]=2
                fields.append(dict(component='V9-three-CODE',root=root,offset=offset,member=name,recipe_id='recipe',
                    object_sha256='o',member_sha256='m',caller=caller,canonical=raw['canonical_name'],undefined=True,
                    kind=20,physical_symbol_index=physical,symbol_index=serialized,section=2,
                    proof=dict(raw,physical_section=section,field_offset=offset)))
        baseline=[dict(old='unchanged',annotation=dict(full_proof='preserved'))]
        return baseline,copy.deepcopy(baseline)+fields,members
    def test_three_maps_preserve_complete_old_records(self):
        before,after,members=self.fixture();added=plan.new_fields(before,after,members)
        self.assertEqual(len(added),3)
        self.assertIn('0x00406d30',{f['proof']['original_base'] for f in added})
    def test_old_annotation_is_not_normalized(self):
        before,after,members=self.fixture();after[0]['annotation']['full_proof']='changed'
        with self.assertRaises(ValueError):plan.new_fields(before,after,members)
    def test_duplicate_raw_record_rejected(self):
        before,after,members=self.fixture();after.append(copy.deepcopy(after[-1]))
        with self.assertRaises(ValueError):plan.new_fields(before,after,members)
    def test_neighbor_target_is_not_append_alias(self):
        before,after,members=self.fixture();after[1]['proof']['original_base']='0x00406d50'
        with self.assertRaises(ValueError):plan.new_fields(before,after,members)
    def test_serialized_symbol_mapping_is_exact(self):
        before,after,members=self.fixture();after[-1]['symbol_index']=999
        with self.assertRaises(ValueError):plan.new_fields(before,after,members)
    def test_zero_field_root_cannot_hide_an_extra_field(self):
        before,after,members=self.fixture();members[1]['projection']['fields'].append({'unexpected':True})
        with self.assertRaises(ValueError):plan.new_fields(before,after,members)

if __name__=='__main__':unittest.main()
