"""Independent authored V8 new-frame to frozen-oracle and coverage integration."""
import copy
import gzip
import json
from pathlib import Path
import struct
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild'),str(ROOT/'tools')]
import frontier_wave_factory_v8 as f
from test_ordinary_relocation_projection_independent import authored


def authored_new_source(*,fields=False):
    raw,contract,certificate,roots,providers=authored() if fields else authored(classes=())
    root=roots[0]
    row=dict(event='SINGLE_ROOT_OBSERVATION',recipe_id=root['recipe_id'],requested_roots=roots,
        closure_observed=True,graph_observation_complete=True,contract=contract,certificate=certificate,
        certificate_sha256=f.digest(certificate),contract_identity_sha256=f.digest(contract),provenance=contract['provenance'])
    rows=[row]
    for index in range(258):
        negative=dict(root,original_address='0x%08x'%(0x00700000+index*16))
        rows.append(dict(event='SINGLE_ROOT_OBSERVATION',recipe_id=root['recipe_id'],requested_roots=[negative],
            closure_observed=False,graph_observation_complete=False))
    summaries=[dict(ordinal=i,event=r['event'],recipe_id=r['recipe_id'],roots=[r['requested_roots'][0]['original_address']],
        record_sha256=f.digest(r),certificate_sha256=r.get('certificate_sha256'),closure_observed=r['closure_observed'],graph_observation_complete=r['graph_observation_complete'])
        for i,r in enumerate(rows,1)]
    authority=dict(kind='new-frontier-v3',receipt_sha256='e'*64,ordinal=1,record_sha256=f.digest(row),certificate_sha256=f.digest(certificate))
    selected=[dict(root=root,authority=authority)]
    payload=bytearray(f.base.coff.parse(raw)['sections'][root['section']]['payload'])
    for field in contract['fields']:struct.pack_into('<I',payload,field['source_field_offset'],field['original_operand'])
    pe=SimpleNamespace(read=lambda address,size:bytes(payload) if (address,size)==(int(root['original_address'],16),root['size']) else b'')
    recipe=dict(symbols={r['coff_relocation']['symbol']:r['derived_source_symbol_base_va'] for r in contract['fields']})
    return raw,root,providers,rows,dict(observations=summaries,summary=dict(roots=259),status='metadata-only',input_stability=True,
        optional_function_index_present=False,policy_id='new-frontier-ordinary-root-observation-v3'),selected,pe,recipe


def spool(directory,values):
    raw,root,providers,rows,receipt,selected,pe,recipe=values
    details=directory/'authored-source.jsonl.gz'
    with gzip.open(details,'wt') as stream:
        for row in rows:stream.write(json.dumps(row)+'\n')
    path,index=f.spool_new_contexts(directory,receipt,details,selected,{},time.monotonic(),expected_receipt_sha256='e'*64)
    with path.open('rb') as stream:row=f.frozen.read_context(stream,index[root['original_address']],selected[0])
    return row


class IndependentWaveFactoryTests(unittest.TestCase):
    def test_new_only_zero_and_field_frames_replay_actual_frozen_oracle(self):
        for fields in (False,True):
            with self.subTest(fields=fields),tempfile.TemporaryDirectory() as td:
                directory=Path(td);values=authored_new_source(fields=fields);raw,root,providers,_,_,_,pe,recipe=values
                row=spool(directory,values);before=copy.deepcopy(row)
                original,stage=directory/'original.obj',directory/'stage.obj';original.write_bytes(raw)
                output,projection=f.frozen.verify_candidate(raw,row,root,providers,set(),original,stage,pe,recipe)
                self.assertEqual(row,before)
                self.assertEqual([r['verdict'] for r in projection['before_comparison']+projection['after_comparison']],['match','match'])
                self.assertEqual(stage.read_bytes(),output)
                self.assertEqual(len(projection['fields']),int(fields))
                selection=values[5][0]
                projection.update(authority=selection['authority'],central_record_sha256=f.digest(row))
                proof=f.field_proof_record('authored.obj',row,selection,projection,output)
                restored=json.loads(gzip.decompress(gzip.compress(json.dumps(proof).encode(),mtime=0)))
                self.assertEqual(restored['fields'],row['contract']['fields'])
                self.assertEqual(restored['fields_sha256'],f.digest(row['contract']['fields']))
                self.assertEqual(restored['output_object_sha256'],f.base.coff.digest(output))
                self.assertFalse(restored['source_evidence_enriched'])
                archive=f.base.coff.read_archive(f.base.coff.archive([('authored.obj',output)]))
                self.assertEqual(archive['members'],[('authored.obj',output)])
                recovered=directory/'recovered.obj';recovered.write_bytes(archive['members'][0][1]);f.base.bulk.strict_reparse(recovered,output)

    def test_authenticated_positive_frame_does_not_replace_fresh_core_gate(self):
        with tempfile.TemporaryDirectory() as td:
            directory=Path(td);values=authored_new_source();raw,root,providers,*_=values;row=spool(directory,values)
            original,stage=directory/'original.obj',directory/'stage.obj';original.write_bytes(raw)
            with patch.object(f.base,'project_member',side_effect=ValueError('authored fresh replay refusal')),patch.object(f.base.bulk,'compare_functions',return_value=[dict(verdict='match')]):
                with self.assertRaisesRegex(ValueError,'authored fresh replay refusal'):
                    f.frozen.verify_candidate(raw,row,root,providers,set(),original,stage,object(),{})
            self.assertFalse(stage.exists());self.assertFalse((directory/'receipt.json').exists())

    def test_reused_terminal_publisher_revokes_success_on_derived_input_drift(self):
        with tempfile.TemporaryDirectory() as td:
            directory=Path(td);calls=[]
            def stable(_):
                calls.append(1)
                if len(calls)==3:raise ValueError('authored late derived-input drift')
            with patch.object(f.base,'stable',side_effect=stable),patch.object(f.base,'budget',return_value={}):
                with self.assertRaisesRegex(ValueError,'authored late derived-input drift'):
                    f.base.publish_receipt(directory,dict(status='completed'),{},time.monotonic())
            self.assertFalse((directory/'receipt.json').exists());self.assertTrue((directory/'receipt.pending.json').exists())

    def test_reused_full_coverage_keeps_original_hashes_and_new_only_status(self):
        values=authored_new_source();root=values[1];identity=values[2][root['original_address']]
        with tempfile.TemporaryDirectory() as td:
            directory=Path(td);source=directory/'authored-coverage.jsonl.gz';target=directory/'projected-coverage.jsonl.gz';providers={}
            with gzip.open(source,'wt') as stream:
                for index in range(68657):
                    a=root['original_address'] if index==0 else '0x%08x'%(0x01000000+index*16)
                    physical=identity if index==0 else dict(recipe_id='authored-coverage',object_sha256='f'*64,symbol_index=index)
                    providers[a]=physical;stream.write(json.dumps(dict(original_address=a,physical_identity=physical,status='AUTHORED_HISTORICAL_BLOCKED'))+'\n')
            frontier=dict(records=[dict(root=root,state='NEW_SELECTED_ROOT_REQUIRES_OBSERVATION')])
            counts=f.frozen.write_coverage(target,source,providers,set(),frontier,{root['original_address']},{root['original_address']})
            self.assertEqual(counts,dict(NEW_FRONTIER_PROJECTED=1,NOT_REQUESTED=68656))
            with gzip.open(target,'rt') as current,gzip.open(source,'rt') as original:
                new=json.loads(next(current));old=json.loads(next(original))
                self.assertEqual(new['original_coverage_row'],dict(ordinal=1,sha256=f.digest(old)))
                self.assertEqual(new['physical_identity'],old['physical_identity'])
                self.assertEqual(new['current_frontier_state'],'NEW_SELECTED_ROOT_REQUIRES_OBSERVATION')


if __name__=='__main__':unittest.main()
