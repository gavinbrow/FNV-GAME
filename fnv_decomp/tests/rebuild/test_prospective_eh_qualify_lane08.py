"""Independent authored/resealed qualifier attacks; no real evidence inputs."""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).absolute().parents[2]
spec=importlib.util.spec_from_file_location('lane08_qualification_fixtures',ROOT/'tests/rebuild/test_prospective_eh_qualify.py')
fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture)
q=fixture.q

class TypedConsistencyAttacks(unittest.TestCase):
    def setUp(self):
        self.b,self.a=fixture.valid_case();self.row=self.b['roots'][0];self.root=self.row['root_address']

    def evidence(self,kind):return next(e for e in self.row['evidence']if e['obligation_id']==kind)
    def run_claim(self):
        fixture.seal(self.b,self.a)
        return q.qualify_prospective_parent_eh(self.b,self.root,anchors=self.a)
    def both_fields(self,name,**changes):
        for key in ('field_inventory','physical_fields'):
            next(f for f in self.row[key]if f['field_id']==name).update(changes)
    def target(self,index):return next(t for t in self.row['targets']if t['index']==index)
    def rejects(self):
        with self.assertRaises(q.QualificationError):self.run_claim()

    def test_absent_decoded_state_and_funcinfo_not_complete(self):
        self.row.pop('funcinfo',None);self.row.pop('state_graph',None)
        self.rejects()

    def test_false_decoded_state_cannot_be_hidden_by_frame_claim(self):
        self.row['funcinfo']=dict(offset=8,magic=0x19930522,max_state=0,flags=1)
        self.row['state_graph']=[]
        self.rejects()

    def test_defined_cleanup_CODE_cannot_live_in_DATA_or_have_DATA_type(self):
        t=self.target(10);t['section']=self.row['owned_sections'][1]['section'];t['type']=0
        self.rejects()

    def test_defined_target_value_must_be_inside_native_extent(self):
        self.target(10)['value']=38
        self.rejects()

    def test_bool_target_reference_does_not_alias_integer_one(self):
        self.target(20)['index']=1
        for key in ('field_inventory','physical_fields'):
            for f in self.row[key]:
                if f['target_index']==20:f['target_index']=True
        e=self.evidence(q.CENSUS);e['facts']['target_indices']=sorted(t['index']for t in self.row['targets'])
        self.rejects()

    def test_bool_section_reference_does_not_alias_parent_one(self):
        old=self.row['parent']['section'];self.row['parent']['section']=1
        for s in self.row['owned_sections']:s['parent_section']=1
        for key in ('field_inventory','physical_fields'):
            for f in self.row[key]:
                if f['section']==old:f['section']=True
        self.evidence(q.GRAPH)['facts']['retained_sections']=sorted([1]+[s['section']for s in self.row['owned_sections']])
        self.rejects()

    def test_frame_handler_tail_cannot_be_parent_field(self):
        self.both_fields('handler',section=self.row['parent']['section'],offset=34)
        self.rejects()

    def test_cookie_checker_cannot_be_cleanup_piece_field(self):
        self.both_fields('checker',offset=2)
        self.rejects()

    def test_HIGHLOW_occurrence_count_bool_is_not_one(self):
        next(e for e in self.row['evidence']if e['obligation_id']==q.HIGHLOW)['facts']['highlow_occurrences']=True
        self.rejects()

    def test_FRAME_state_zero_bool_is_not_integer_zero(self):
        self.evidence(q.FRAME)['facts']['state_transitions']=[[False,-1]]
        self.rejects()

    def test_object_source_context_anchors_are_digest_strings(self):
        index=str(self.row['recipe_index'])
        self.a['objects'][index]=True;self.a['sources'][index]=True
        self.row['object_sha256']=True;self.row['source_context_sha256']=True
        self.evidence(q.SOURCE)['facts'].update(object_sha256=True,source_sha256=True)
        self.rejects()

    def test_original_target_base_is_uint32_nonzero(self):
        self.target(23)['original_base']=0x100000000
        self.rejects()

    def test_missing_cleanup_call_not_complete_family(self):
        for key in ('field_inventory','physical_fields'):
            self.row[key]=[f for f in self.row[key]if f['field_id']!='cleanup-call']
        self.evidence(q.CENSUS)['facts']['field_ids']=sorted(f['field_id']for f in self.row['physical_fields'])
        self.rejects()

    def test_consistent_authored_claims_still_no_discharge_or_promotion(self):
        out=self.run_claim();self.assertEqual(out['discharged'],[])
        self.assertTrue(out['claims_are_not_verified_closure'])
        self.assertEqual(len(out['obligations']),7)
        self.assertTrue(all(r['discharged']is False for r in out['obligations']))
        for key in q.FALSE_FLAGS:self.assertIs(out[key],False)

    def test_duplicate_inherited_IDs_keep_original_ordinals(self):
        self.row['inherited_blockers']=[dict(id='SAME_UUID_NEGATIVE',ordinal=n,evidence_sha256=fixture.h(['authored',n]))for n in (9,2)]
        out=self.run_claim();self.assertEqual([r['occurrence']for r in out['obligations'][-2:]],[9,2])
        self.assertEqual(out['unresolved_obligation_ids'][-2:],['SAME_UUID_NEGATIVE']*2)
        self.assertEqual(out['discharged'],[])

if __name__=='__main__':unittest.main()
