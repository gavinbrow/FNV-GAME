"""New-only operation and declared finite/resource gate regressions."""
from pathlib import Path
import sys
import subprocess
from types import SimpleNamespace
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/rebuild'))
import frontier_wave_factory_v8 as f


class WaveOperationTests(unittest.TestCase):
    def test_fresh_cli_help_loads_the_real_entry_point(self):
        result=subprocess.run([sys.executable,str(ROOT/'tools/rebuild/frontier_wave_factory_v8.py'),'--help'],
            capture_output=True,text=True,check=False)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('--operation',result.stdout)
        self.assertIn('--reference',result.stdout)
        self.assertEqual(result.stderr,'')

    def test_missing_independent_acceptance_stops_before_any_other_input(self):
        args=SimpleNamespace(review=Path('authored.json'),review_sha256='a'*64)
        with patch.object(f.base,'observe',return_value=args.review) as observed,patch.object(f.base,'load_json',return_value={}):
            with self.assertRaises(ValueError):f.review_gate(args,{})
        self.assertEqual(observed.call_count,1)

    def test_phase_cannot_authorize_arbitrary_positive_subset(self):
        args=SimpleNamespace(review=Path('authored.json'),review_sha256='a'*64,operation_sha256='b'*64)
        review=dict(kind='V8-new-only-CODE-factory-review-v1',schema_version=1,approved=True,
            independent_source_schema_review_pass=True,root_authorized=True,reviewer='authored',
            all_positive_new_roots_required=False,operation_sha256='b'*64,producer_sha256=f.PINS,
            source_artifacts={k:h for k,(_,h) in f.SOURCES.items()},source_sha256={p:'c'*64 for p in f.OWNED},
            allow_native_tools=False,allow_game_execution=False)
        with patch.object(f.base,'observe',return_value=args.review),patch.object(f.base,'load_json',return_value=review):
            with self.assertRaises(ValueError):f.review_gate(args,{})

    def test_callers_cannot_raise_memory_time_or_output_caps(self):
        args=SimpleNamespace(operation=Path('authored-op.json'),operation_sha256='a'*64)
        op=dict(schema_version=1,kind='ALL-positive-new259-V8-CODE-production',roots=[],output_relative='build/rebuild/authored',
            resource_limits=dict(seconds=901,peak_memory_bytes=2*1024**3,output_bytes=129*1024**2))
        with patch.object(f,'review_gate',return_value={}),patch.object(f.base,'observe',return_value=args.operation),patch.object(f.base,'load_json',return_value=op):
            with self.assertRaises(ValueError):f.run(args)

    def test_old_metadata_authority_cannot_substitute_a_v8_operation(self):
        args=SimpleNamespace(operation=Path('authored-op.json'),operation_sha256='a'*64)
        op=dict(schema_version=1,kind='ALL-positive-V5-CODE-production',roots=[],output_relative='build/rebuild/authored',
            resource_limits=dict(seconds=900,peak_memory_bytes=1024**3,output_bytes=128*1024**2))
        with patch.object(f,'review_gate',return_value={}),patch.object(f.base,'observe',return_value=args.operation),patch.object(f.base,'load_json',return_value=op):
            with self.assertRaises(ValueError):f.run(args)


if __name__=='__main__':unittest.main()
