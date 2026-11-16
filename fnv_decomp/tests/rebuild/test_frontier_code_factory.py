"""Finite operation authorization and resource boundaries, authored inputs only."""
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/rebuild'))
import frontier_code_factory as f


class OperationGateTests(unittest.TestCase):
    def test_unreviewed_operation_fails_before_opening_operation_or_outputs(self):
        args=SimpleNamespace(review=Path('authored-review.json'),review_sha256='a'*64)
        with patch.object(f.base,'observe',return_value=args.review) as observed,patch.object(f.base,'load_json',return_value={}):
            with self.assertRaises(ValueError):f.review_gate(args,{})
        self.assertEqual(observed.call_count,1)

    def test_root_authorization_does_not_allow_partial_positive_batches(self):
        args=SimpleNamespace(review=Path('authored-review.json'),review_sha256='a'*64,operation_sha256='b'*64)
        review=dict(schema_version=1,kind='finite-frontier-CODE-factory-review-v1',approved=True,
            independent_source_schema_review_pass=True,root_authorized=True,reviewer='authored-peer',operation_sha256='b'*64,
            all_positive_current_frontier_roots_required=False,new_observation_independently_accepted=True,
            producer_sha256=f.PINS,fixed_source_sha256=f.SOURCE_PINS,source_sha256={p:'c'*64 for p in f.OWNED},
            allow_native_tools=False,allow_game_execution=False)
        with patch.object(f.base,'observe',return_value=args.review),patch.object(f.base,'load_json',return_value=review):
            with self.assertRaises(ValueError):f.review_gate(args,{})

    def test_operation_cannot_expand_resource_caps(self):
        args=SimpleNamespace(operation=Path('authored-op.json'),operation_sha256='a'*64)
        operation=dict(schema_version=1,kind='ALL-positive-V5-CODE-production',sources={k:{} for k in f.SOURCE_KEYS},
            root_request={},output_relative='build/rebuild/authored',resource_limits=dict(seconds=901,peak_memory_bytes=2*1024**3,output_bytes=129*1024**2))
        with patch.object(f,'review_gate',return_value={}),patch.object(f.base,'observe',return_value=args.operation),patch.object(f.base,'load_json',return_value=operation):
            with self.assertRaises(ValueError):f.run(args)

    def test_operation_rejects_extra_authority_source_before_any_body_read(self):
        args=SimpleNamespace(operation=Path('authored-op.json'),operation_sha256='a'*64)
        operation=dict(schema_version=1,kind='ALL-positive-V5-CODE-production',sources={**{k:{} for k in f.SOURCE_KEYS},'borrowed':{}},
            root_request={},output_relative='build/rebuild/authored',resource_limits=dict(seconds=900,peak_memory_bytes=1024**3,output_bytes=128*1024**2))
        with patch.object(f,'review_gate',return_value={}),patch.object(f.base,'observe',return_value=args.operation),patch.object(f.base,'load_json',return_value=operation):
            with self.assertRaises(ValueError):f.run(args)


if __name__=='__main__':unittest.main()
