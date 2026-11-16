"""Independent authored saved-selection and owned-output checks."""
import copy,importlib.util,unittest,tempfile,os,io
from pathlib import Path
from unittest.mock import patch
P=Path(__file__).resolve().parents[2]/'build/rebuild/uuid-seven-selected-metadata-v2/test_collect.py';s=importlib.util.spec_from_file_location('uuid_seven_fixture_lane08',P);h=importlib.util.module_from_spec(s);s.loader.exec_module(h);m=h.m
class UUIDSevenIndependentTests(unittest.TestCase):
 def test_no_input_mutation_and_global_piece_ordinals_preserved(self):
  x=h.fixture();x[2]['units'][0]['eh_sections'].insert(0,[1,8,True,'0x00ffffff',[]]);before=copy.deepcopy(x);out=m.select(*x);self.assertEqual(x,before);root=next(iter(out.values()))['roots'][0];self.assertEqual([p['ordinal'] for p in root['own_eh_pieces']],[1,2]);self.assertEqual(root['own_eh_false_count'],1)
 def test_diagnostics_preserved_and_no_eligibility(self):
  x=h.fixture();x[2]['units'][0]['eh_errors']=['authored-other-parent-diagnostic'];out=m.select(*x);packet=next(iter(out.values()));self.assertEqual(packet['unit_diagnostics_preserved'],['authored-other-parent-diagnostic']);self.assertEqual(packet['unit_diagnostic_count'],1)
  for packet in out.values():
   for k in m.FALSE:self.assertIs(packet[k],False)
 def test_oversize_input_rejected_before_open(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'input';p.write_bytes(b'12345')
   with patch.object(Path,'open',side_effect=AssertionError('must not open')):
    with self.assertRaisesRegex(ValueError,'file cap'):m.bounded(p,4,lambda:None)
 def test_absent_EH_key_is_unknown_not_an_empty_or_successful_proof(self):
  x=h.fixture();x[2]['units'][0].pop('eh_sections');out=m.select(*x);root=next(iter(out.values()))['roots'][0]
  self.assertEqual(root['own_eh_pieces'],[]);self.assertIn('unknown',root['own_eh_evidence_status'].lower());self.assertFalse(root['no_catch_family_established']);self.assertTrue(root['fresh_graph_required'])
 def test_foreign_replacement_not_removed_by_cleanup(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'output';foreign=Path(d)/'foreign';foreign.write_bytes(b'foreign');calls=[0]
   def stable():
    calls[0]+=1
    if calls[0]==2:os.replace(foreign,p)
   with self.assertRaisesRegex(ValueError,'output replaced'):m.publish({p:b'original'},stable,lambda:None)
   self.assertEqual(p.read_bytes(),b'foreign')
if __name__=='__main__':unittest.main()
