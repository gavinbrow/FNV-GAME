"""Independent authored COFF factory ordering and physical-output boundaries."""
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import frontier_code_factory as f
from test_ordinary_relocation_projection_independent import authored


def context(*,fields=False):
    raw,contract,certificate,roots,providers=authored() if fields else authored(classes=())
    return raw,dict(contract=contract,certificate=certificate,requested_roots=roots),roots[0],providers


class IndependentFrontierFactoryTests(unittest.TestCase):
    def test_zero_core_original_and_recovered_plain_MATCH(self):
        raw,row,root,providers=context()
        pe=SimpleNamespace(read=lambda a,n:bytes(root['size']) if (a,n)==(int(root['original_address'],16),root['size']) else b'')
        with tempfile.TemporaryDirectory() as td:
            original,stage=Path(td)/'original.obj',Path(td)/'stage.obj'
            original.write_bytes(raw)
            output,receipt=f.verify_candidate(raw,row,root,providers,set(),original,stage,pe,{})
            self.assertEqual(output,stage.read_bytes())
            self.assertTrue(receipt['strict_zero_consumer_replayed'])
            self.assertEqual([r['verdict'] for r in receipt['before_comparison']+receipt['after_comparison']],['match','match'])
            self.assertEqual(receipt['fields'],[])
            archive=f.base.coff.archive([('authored.obj',output)])
            recovered=f.base.coff.read_archive(archive)
            self.assertEqual(recovered['members'],[('authored.obj',output)])
            recovered_path=Path(td)/'recovered.obj';recovered_path.write_bytes(output)
            f.base.bulk.strict_reparse(recovered_path,output)

    def test_zero_pipeline_replays_in_original_core_reader_after_order(self):
        raw,row,root,providers=context();events=[]
        project=f.base.project_member;strict=f.base.bulk.strict_reparse
        def compare(*args,**kwargs):events.append('original' if not events else 'after');return [dict(verdict='match')]
        def replay(*args,**kwargs):events.append('core');return project(*args,**kwargs)
        def reader(*args,**kwargs):events.append('reader');return strict(*args,**kwargs)
        with tempfile.TemporaryDirectory() as td:
            original,stage=Path(td)/'original.obj',Path(td)/'stage.obj';original.write_bytes(raw)
            with patch.object(f.base.bulk,'compare_functions',side_effect=compare),patch.object(f.base,'project_member',side_effect=replay),patch.object(f.base.bulk,'strict_reparse',side_effect=reader):
                f.verify_candidate(raw,row,root,providers,set(),original,stage,object(),{})
            self.assertEqual(events,['original','core','reader','after'])

    def test_zero_failures_abort_without_success_and_preserve_failed_stage_only_when_written(self):
        raw,row,root,providers=context()
        for phase in ('original','core','reader','after'):
            with self.subTest(phase=phase),tempfile.TemporaryDirectory() as td:
                original,stage=Path(td)/'original.obj',Path(td)/'stage.obj';original.write_bytes(raw)
                calls=[];project=f.base.project_member;strict=f.base.bulk.strict_reparse
                def compare(*args,**kwargs):
                    label='original' if not calls else 'after';calls.append(label)
                    if phase==label:raise ValueError('authored '+phase+' failure')
                    return [dict(verdict='match')]
                def replay(*args,**kwargs):
                    if phase=='core':raise ValueError('authored core failure')
                    return project(*args,**kwargs)
                def reader(*args,**kwargs):
                    if phase=='reader':raise ValueError('authored reader failure')
                    return strict(*args,**kwargs)
                with patch.object(f.base.bulk,'compare_functions',side_effect=compare),patch.object(f.base,'project_member',side_effect=replay),patch.object(f.base.bulk,'strict_reparse',side_effect=reader):
                    with self.assertRaisesRegex(ValueError,'authored '+phase+' failure'):
                        f.verify_candidate(raw,row,root,providers,set(),original,stage,object(),{})
                self.assertEqual(stage.exists(),phase in ('reader','after'))
                self.assertFalse((Path(td)/'receipt.json').exists())

    def test_zero_prepared_namespace_is_fatal_before_original_compare(self):
        raw,row,root,providers=context()
        name=f.base.pool.canonical(providers[root['original_address']])
        with patch.object(f.base.bulk,'compare_functions') as compare:
            with self.assertRaises(ValueError):
                f.verify_candidate(raw,row,root,providers,{name},Path('authored-original'),Path('authored-stage'),object(),{})
            compare.assert_not_called()

    def test_field_branch_uses_frozen_verifier_and_integrity_failure_propagates(self):
        raw,row,root,providers=context(fields=True)
        with patch.object(f.fields,'verify_member',side_effect=ValueError('authored field integrity refusal')) as verify,patch.object(f.base,'project_member') as zero:
            with self.assertRaisesRegex(ValueError,'authored field integrity refusal'):
                f.verify_candidate(raw,row,root,providers,set(),Path('authored-original'),Path('authored-stage'),object(),{})
            verify.assert_called_once();zero.assert_not_called()


if __name__=='__main__':unittest.main()
