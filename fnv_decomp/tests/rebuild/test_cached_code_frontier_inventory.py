"""Owner operational regressions using authored metadata, never saved Game inputs."""
import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
import zlib

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_code_frontier_inventory as inventory
import test_cached_code_frontier_inventory_independent as authored


class OwnerInventoryTests(unittest.TestCase):
    def test_fresh_process_cli_help_does_not_enter_run(self):
        result=subprocess.run([sys.executable,str(ROOT/'tools/rebuild/cached_code_frontier_inventory.py'),'--help'],
            cwd=ROOT,capture_output=True,text=True,timeout=30)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('--operation-sha256',result.stdout)
        self.assertIn('--review-sha256',result.stdout)

    def test_corrupt_first_frame_aborts_without_receipt_or_retry(self):
        harness=authored.IndependentAuthoredInventoryTests()
        with tempfile.TemporaryDirectory() as directory:
            context=harness.setup_context(directory);path=context[2]['data_path'];raw=bytearray(path.read_bytes());raw[0]^=255;path.write_bytes(raw)
            with self.assertRaises((ValueError,zlib.error)):harness.run_authored(context)
            out=context[1].out
            self.assertFalse((out/'receipt.json').exists());self.assertTrue((out/'abort.json').exists())
            self.assertEqual(context[3].calls,[0])
            self.assertEqual(json.loads((out/'abort.json').read_bytes())['status'],'aborted-no-retry')
            events=[json.loads(line)['state'] for line in (out/'progress.jsonl').read_text().splitlines()]
            self.assertEqual(events,['started','failed'])

    def test_empty_hydration_writes_complete_empty_contract_stream_without_frame_read(self):
        harness=authored.IndependentAuthoredInventoryTests()
        with tempfile.TemporaryDirectory() as directory:
            context=harness.setup_context(directory);prepared=context[2]
            prepared['groups']={};prepared['inventory']['metadata_requests']=[]
            for row in prepared['inventory']['records']:
                row['state']='CACHED_ORIGINAL_OMISSION_BLOCKED';row['inventory_action']='LEDGER_ONLY'
            result=harness.run_authored(context);out=context[1].out
            self.assertEqual((result['qualified_metadata_roots'],result['qualified_recipes'],result['generated_contract_records']),(0,0,0))
            self.assertEqual(context[3].calls,[])
            with gzip.open(out/'metadata-contracts.jsonl.gz','rb') as stream:self.assertEqual(stream.read(),b'')
            self.assertEqual(result['cache_data_range_protection']['selected_ranges'],[])
            self.assertFalse(result['whole_cache_data_hash_verified_this_run'])
            self.assertEqual(len(json.loads((out/'inventory.json').read_bytes())['records']),2)
            self.assertTrue((out/'receipt.json').exists())

    def test_compressed_output_chunk_is_refused_before_crossing_cap(self):
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory);path=out/'authored.gz'
            with patch.dict(inventory.LIMITS,output_bytes=20),path.open('xb') as target:
                sink=inventory.BoundedSink(target,time.monotonic(),out)
                self.assertEqual(sink.write(b'A'*10),10)
                with self.assertRaises(ValueError):sink.write(b'B'*11)
            self.assertEqual(path.read_bytes(),b'A'*10)


if __name__=='__main__':unittest.main()
