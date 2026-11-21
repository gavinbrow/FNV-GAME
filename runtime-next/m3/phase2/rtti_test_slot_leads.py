"""Source-lead registry tests avoid conflating address leads with resolved slots."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import rtti_slot_leads as s

class Leads(unittest.TestCase):
 def test_not_emitted_and_unresolved_remain_distinct(self):
  t={'slots':[{'index':0,'reference_target':10,'symbol':'x','resolved_target':None,'match':False}]}
  funcs={10:{('a','src/a.cpp',1)},20:{('b','src/b.cpp',2)}};rows=s.rows_for_table(t,[10,20,30],funcs,{})
  self.assertEqual([x['status'] for x in rows],['source_recipe_leads','not_emitted_source_recipe_leads','not_emitted_no_lead'])
  self.assertIsNone(rows[1]['emitted_symbol'])
 def test_metadata_census_disagreement_fails(self):
  t={'slots':[{'index':0,'reference_target':11,'symbol':'x','resolved_target':11,'match':True}]}
  with self.assertRaisesRegex(ValueError,'differs from census'):s.rows_for_table(t,[10],{}, {})
 def test_ambiguous_aliases_remain_multiple(self):
  t={'slots':[]};rows=s.rows_for_table(t,[10],{10:{('a','a.cpp',1),('b','b.cpp',2)}},{})
  self.assertEqual(rows[0]['unique_function_spellings'],2);self.assertFalse(rows[0]['current_match'])

if __name__=='__main__':unittest.main(verbosity=2)
