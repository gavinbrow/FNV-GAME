"""Synthetic assembly contracts, no real baseline or native operations."""
import copy,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import application_actual_cohort_assembly_v2 as v
from test_application_actual_cohort_semantic_v2 import fixture

class Tests(unittest.TestCase):
    def test_wrong_actual_baseline_bytes_rejected(self):
        with self.assertRaises(ValueError):v.decode_baseline(dict(report=b'{}',observation=b'{}',fields=b''))

    def test_assembly_retains_unknowns_and_exact_baseline_prefix(self):
        report=dict(provenance={},selected_supplementary_providers=[],unknown={'future': True},
                    producer_prior_quarantines=['preserve'],uuid_source_evidence={'negative':'preserve'})
        old_fields=[{'old':'field','unknown':1}]; observation={'preserve':True}
        baseline=(report,observation,old_fields,[],[])
        with patch.object(v,'decode_baseline',return_value=copy.deepcopy(baseline)):
            result=v.assemble(baseline_bytes={},semantic_inputs=fixture())
        self.assertEqual(result['fields'][0],old_fields[0]);self.assertEqual(result['report']['unknown'],report['unknown'])
        self.assertEqual(result['report']['producer_prior_quarantines'],['preserve'])
        self.assertEqual(result['report']['uuid_source_evidence'],{'negative':'preserve'})
        self.assertFalse(result['link_approved']);self.assertEqual(result['report']['full_included_field_count'],2)

    def test_provider_conflict_rejected_after_physical_derivation(self):
        args=fixture(); data=v.semantic.derive(**args); p=copy.deepcopy(data['providers'][0]);p['component']='baseline'
        report=dict(provenance={},selected_supplementary_providers=[])
        with patch.object(v,'decode_baseline',return_value=(report,{},[],[p],[])):
            with self.assertRaises(ValueError):v.assemble(baseline_bytes={},semantic_inputs=args)

if __name__=='__main__':unittest.main()
