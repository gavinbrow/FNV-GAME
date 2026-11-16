"""Main V13 source/operational review; authored metadata and cache frames only."""
import copy
import gzip
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_code_frontier_inventory_v13 as inventory
import test_cached_code_frontier_inventory_v13 as owner
import test_cached_code_frontier_inventory_independent as legacy_tests
from test_cached_code_frontier_independent import fixture as frame_fixture


class IndependentNativeSummaryTests(unittest.TestCase):
    def test_unknown_summary_payload_preserved_without_loading_body_or_issuing_certificate(self):
        args=owner.fixture();summary=args[1]['observations'][0]
        summary['opaque_future_payload']={'typed':[True,1,False,0,None,{'not_admission':'unknown'}]}
        before=copy.deepcopy(args)
        with patch.object(inventory.native.coff,'parse',side_effect=AssertionError('no original object')), \
             patch.object(inventory.base.ordinary,'assess_object',side_effect=AssertionError('no certificate replay')):
            result=owner.registry(args)
        row=result['records'][args[2]['roots'][0]['original_address']]
        self.assertEqual(row['summary'],summary);self.assertEqual(args,before)
        self.assertNotIn('contract',row);self.assertNotIn('certificate',row)
        self.assertFalse(result['native_certificate_bodies_reloaded']);self.assertFalse(result['certificate_created'])
        self.assertEqual(result['native_authority_scope'],'accepted-receipt-summary-hashes-only')
        row['summary']['opaque_future_payload']['typed'].append('changed returned copy')
        self.assertEqual(args,before)

    def test_positive_union_never_upgrades_negative_singleton(self):
        args=owner.fixture(field=False,safeseh=True);union=args[1]['observations'][-1]
        union.update(closure_observed=True,graph_observation_complete=True,blocker_codes={})
        args[1]['summary'].update(union_closure=1,union_blocked=0)
        registry=owner.registry(args)
        result=inventory.classify_demands(args[5],args[3],args[4],registry,set(),[],expected_code_count=2,expected_quarantines=set())
        self.assertEqual(len(result['metadata_requests']),1)
        beta=args[2]['roots'][1]['original_address']
        entry=next(r for r in result['records'] if r.get('root',{}).get('original_address')==beta)
        self.assertEqual(entry['inventory_action'],'LEDGER_ONLY')
        self.assertFalse(registry['records'][beta]['summary']['closure_observed'])
        self.assertFalse(result['admission_decision_created'])

    def test_unsupported_original_format_retains_absent_certificate_as_unknown_negative(self):
        args=owner.fixture(field=False);s=args[1]['observations'][0]
        s.update(certificate_sha256=None,closure_observed=False,graph_observation_complete=False,
            blocker_codes={'UNSUPPORTED_ORIGINAL_COFF_FORMAT':1})
        args[1]['summary'].update(singleton_closure=1,singleton_blocked=1)
        registry=owner.registry(args);a=s['roots'][0]
        self.assertIsNone(registry['records'][a]['authority']['certificate_sha256'])
        self.assertFalse(registry['records'][a]['summary']['graph_observation_complete'])
        ledger=inventory.classify_demands(args[5],args[3],args[4],registry,set(),[],expected_code_count=2,expected_quarantines=set())
        self.assertNotIn(a,{r['original_address'] for r in ledger['metadata_requests']})


class IndependentV13OperationalTests(unittest.TestCase):
    def setup_context(self,td):
        with patch.object(legacy_tests,'inventory',inventory):
            return legacy_tests.IndependentAuthoredInventoryTests().setup_context(td)

    def run_context(self,context,drift=False):
        with patch.object(legacy_tests,'inventory',inventory),patch.object(inventory.previous,'ROOT',context[0]):
            return legacy_tests.IndependentAuthoredInventoryTests().run_authored(context,drift=drift)

    def test_real_v13_frames_match_direct_frozen_contracts_with_unknown_missing_and_full_unit_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            context=self.setup_context(td);result=self.run_context(context);out=context[1].out
            self.assertEqual((result['qualified_metadata_roots'],result['qualified_recipes'],result['generated_contract_records']),(2,1,3))
            self.assertEqual(context[3].calls,[0]);self.assertTrue(all(result[k] is False for k in inventory.FALSE))
            _,_,selections,roots,lines,summary,_,_=frame_fixture()
            direct=inventory.seam.cache_module.frozen.BindingReader(lines,summary,selections);bucket=direct.take(0);direct.finish(1,1)
            request_sha=hashlib.sha256((out/'metadata-request.json').read_bytes()).hexdigest()
            with gzip.open(out/'metadata-contracts.jsonl.gz','rt') as source:records=[json.loads(line) for line in source]
            unit=next(iter(context[2]['units'].values()));proof=context[2]['proofs'][unit['recipe_id']]
            for record,scope in zip(records,([roots[0]],[roots[1]],roots)):
                expected=inventory.seam.finite.build_contract(unit,proof,scope,bucket,context[2]['imported'],copy.deepcopy(record['contract']['provenance']))
                self.assertEqual(inventory.seam.canonical(record['contract']),inventory.seam.canonical(expected))
                self.assertEqual(record['contract']['provenance']['request_sha256'],request_sha)
                self.assertEqual(record['contract']['provenance']['collector_policy_id'],inventory.POLICY)
                self.assertFalse(record['historical_certificate_contract_identity_equal_claimed']);self.assertFalse(record['certificate_created'])
            self.assertEqual(records[0]['contract']['fields'][0]['opaque_future_field']['all'][:4],[True,1,False,0])
            self.assertEqual(records[1]['contract']['missing_fields'][0]['classification'],'MISSING_SOURCE_RELOCATION_NO_SYNTHESIS')
            self.assertEqual(len(records[-1]['contract']['parent_eh']),1)
            self.assertEqual(len(records[0]['contract']['omission_field_proofs']),1)
            self.assertEqual(json.loads((out/'receipt.json').read_bytes()),result)

    def test_late_protected_contract_output_drift_retracts_success(self):
        with tempfile.TemporaryDirectory() as td:
            context=self.setup_context(td)
            with self.assertRaises(ValueError):self.run_context(context,drift=True)
            self.assertFalse((context[1].out/'receipt.json').exists());self.assertTrue((context[1].out/'abort.json').exists())

    def test_exact_published_request_file_sha_is_used_by_both_singletons_and_union(self):
        with tempfile.TemporaryDirectory() as td:
            context=self.setup_context(td);self.run_context(context);out=context[1].out
            raw=(out/'metadata-request.json').read_bytes();self.assertTrue(raw.endswith(b'\n'))
            exact_sha=hashlib.sha256(raw).hexdigest();semantic_sha=inventory.digest(json.loads(raw));self.assertNotEqual(exact_sha,semantic_sha)
            with gzip.open(out/'metadata-contracts.jsonl.gz','rt') as source:
                records=[json.loads(line) for line in source]
            self.assertEqual({r['contract']['provenance']['request_sha256'] for r in records},{exact_sha})
            self.assertEqual([r['event'] for r in records],['SINGLE_ROOT_METADATA_CONTRACT','SINGLE_ROOT_METADATA_CONTRACT','RECIPE_UNION_METADATA_CONTRACT'])


if __name__=='__main__':unittest.main()
