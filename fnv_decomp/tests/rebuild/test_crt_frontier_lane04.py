import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import crt_frontier_lane04 as lane

class Lane04Tests(unittest.TestCase):
    def test_physical_evidence_and_link_scope_retained(self):
        fields=[dict(source_path='src/example.cpp',coff_relocation=dict(symbol='_strlen'),
                     ordinal=4,source_field_offset=3)]
        target=dict(original_target='0x00ec6130',field_uses=fields,actual_V4_unresolved_groups=[])
        row=lane.target_record(target,{'sp1:_strlen':{'value':0}}, {'src/example.cpp':'a'*64})
        self.assertEqual(row['field_proofs'],fields)
        self.assertEqual(row['actual_V4_unresolved_groups'],[])
        self.assertEqual(row['members'],{'sp1:_strlen':{'value':0}})
        self.assertFalse(row['provider_selected']); self.assertFalse(row['ABI_approved'])
    def test_unknown_remains_unknown(self):
        row=lane.target_record(dict(original_target='0x00481230',field_uses=[],
                                    actual_V4_unresolved_groups=[]),{}, {})
        self.assertEqual(row['hypotheses'],[])
        self.assertFalse(row['original_identity_proven'])
    def test_stream_family_and_helper_contracts_retained(self):
        self.assertIn('FILE', ' '.join(lane.coupling('0x00ecb562')))
        self.assertIn('machine ABI',' '.join(lane.coupling('0x00ec782f')))
        self.assertIn('static-destructor',' '.join(lane.coupling('0x00fdd690')))
    def test_copy_conflict_not_collapsed(self):
        self.assertEqual(lane.NAMES['0x00ec44d0'],('_memcpy','_memmove'))

if __name__=='__main__': unittest.main()
