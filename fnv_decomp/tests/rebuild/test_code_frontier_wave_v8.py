"""Metadata phase and historical source-document authority boundaries."""
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/rebuild'))
import code_frontier_wave_v8 as f


def transition():
    return dict(kind='post-outcome-documentation-only-transition',producer_replayed=False,
        documents={'docs/rebuild/CODE-FRONTIER-WAVE.md':dict(before='b78107f80b4b0884471c9fdf758f10071642cea8090fe15819de6e0a466a8001',after='a'*64),
        'docs/rebuild/FRONTIER-WAVE-FACTORY.md':dict(before='7faa39d7102cb090dfa8abb7dcd36106cd887fa17afbce9a48331264c1101d4e',after='b'*64)},
        producer_sources_unchanged={'tools/rebuild/code_frontier_wave.py':f.PINS['tools/rebuild/code_frontier_wave.py']})


class WaveGateTests(unittest.TestCase):
    def test_missing_independent_phase_stops_before_other_inputs(self):
        args=SimpleNamespace(review=Path('authored.json'),review_sha256='a'*64)
        with patch.object(f.base,'observe',return_value=args.review) as observed,patch.object(f.base,'load_json',return_value={}):
            with self.assertRaises(ValueError):f.run(args)
        self.assertEqual(observed.call_count,1)

    def test_transition_binds_old_snapshot_current_doc_and_unchanged_producer(self):
        with patch.object(f.base,'observe',return_value=Path('authored')) as observed:
            f.protect_historical_docs(transition(),{})
        self.assertEqual(observed.call_count,5)
        self.assertTrue(any('source-snapshots' in str(call.args[0]) for call in observed.call_args_list))

    def test_transition_cannot_erase_or_invent_historical_document_source(self):
        for kind in ('drop','before','extra'):
            value=transition()
            if kind=='drop':value['documents'].pop('docs/rebuild/CODE-FRONTIER-WAVE.md')
            elif kind=='before':value['documents']['docs/rebuild/CODE-FRONTIER-WAVE.md']['before']='c'*64
            else:value['documents']['docs/rebuild/unknown.md']=dict(before='c'*64,after='d'*64)
            with patch.object(f.base,'observe'),self.assertRaises(ValueError):f.protect_historical_docs(value,{})

    def test_documentation_transition_cannot_excuse_tool_drift(self):
        value=transition();value['producer_sources_unchanged']['tools/rebuild/frontier_code_factory.py']='e'*64
        with patch.object(f.base,'observe'),self.assertRaises(ValueError):f.protect_historical_docs(value,{})


if __name__=='__main__':unittest.main()
