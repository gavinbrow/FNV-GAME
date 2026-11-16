"""Original authored context-spool corruption tests; no original inputs."""
import copy
import gzip
import io
import json
from pathlib import Path
import struct
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'tools/rebuild'), str(ROOT/'tests/rebuild')]
import frontier_code_factory as factory
import scalableordinary_root_collect as collector
import root_code_closure as ordinary
import coff_code_archive as coff
from test_scalableordinary_root_collect import fixture


def context(which=0, kind='cached-central'):
    raw, unit, proof, roots, _, _, bindings = fixture()
    root = roots[which]
    contract = collector.build_contract(unit,proof,[root],bindings,{},
        dict(recipe_id=unit['recipe_id'],recipe_index=unit['recipe_index'],
             object_sha256=unit['object_sha256'],source_sha256=unit['source_sha256']))
    certificate = ordinary.assess_object(coff.parse(raw),contract)
    row = dict(event='SINGLE_ROOT_OBSERVATION',recipe_id=unit['recipe_id'],requested_roots=[root],
               closure_observed=True,graph_observation_complete=True,contract=contract,certificate=certificate,
               certificate_sha256=factory.digest(certificate),contract_identity_sha256=factory.digest(contract),
               provenance=contract['provenance'])
    authority = dict(kind=kind,receipt_sha256=('a' if kind=='cached-central' else 'b')*64,
                     record_sha256=factory.digest(row),certificate_sha256=factory.digest(certificate),ordinal=1)
    if kind=='cached-central': authority['lane']=1
    return row, dict(root=root,authority=authority)


def metadata_sources(base):
    old, old_selection = context()
    new, new_selection = context(1,'new-frontier')
    rows = [old]
    for _ in range(302):
        row = copy.deepcopy(old)
        row['event'] = 'RECIPE_ROOT_UNION_OBSERVATION'
        rows.append(row)
    lanes = base/'source'/'lanes'
    lanes.mkdir(parents=True)
    path = lanes/'code-lane-01.jsonl.gz'
    with gzip.open(path,'wt') as target:
        for row in rows: target.write(json.dumps(row)+'\n')
    summaries = [dict(lane=1,lane_record_ordinal=i,event=row['event'],recipe_id=row['recipe_id'],
                      record_sha256=factory.digest(row),roots=[r['original_address'] for r in row['requested_roots']])
                 for i,row in enumerate(rows,1)]
    central = dict(observations=summaries,lane_artifacts={'1':dict(path=path.name,
        sha256=factory.base.file_hash(path),bytes=path.stat().st_size,records=303)})
    new_path = base/'source'/'new.jsonl.gz'
    with gzip.open(new_path,'wt') as target: target.write(json.dumps(new)+'\n')
    new_receipt = dict(observations=[dict(ordinal=1,event=new['event'],recipe_id=new['recipe_id'],
        record_sha256=factory.digest(new),roots=[new_selection['root']['original_address']],graph_observation_complete=True)])
    out=base/'output';out.mkdir()
    return out,central,lanes,new_receipt,new_path,[old_selection,new_selection]


class IndependentSpoolTests(unittest.TestCase):
    def test_each_frame_is_independently_seekable_and_retains_source_epoch(self):
        stream=io.BytesIO();first,one=context();second,two=context(1,'new-frontier')
        one_index=factory.write_context(stream,first,one)
        two_index=factory.write_context(stream,second,two)
        self.assertGreater(two_index['offset'],one_index['offset'])
        self.assertEqual(factory.read_context(stream,two_index,two),second)
        self.assertEqual(factory.read_context(stream,one_index,one),first)

    def test_borrowed_root_or_epoch_index_cannot_read_another_frame(self):
        row,selection=context();stream=io.BytesIO();index=factory.write_context(stream,row,selection)
        for mutation in ('root','epoch','record','certificate'):
            other=copy.deepcopy(selection)
            if mutation=='root':other['root']['source_sha256']='f'*64
            elif mutation=='epoch':other['authority']['receipt_sha256']='f'*64
            elif mutation=='record':other['authority']['record_sha256']='f'*64
            else:other['authority']['certificate_sha256']='f'*64
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):
                factory.read_context(stream,index,other)

    def test_corrupt_truncated_or_misdirected_frames_are_fatal(self):
        row,selection=context();stream=io.BytesIO();index=factory.write_context(stream,row,selection);data=stream.getvalue()
        for mutation in ('header','payload','truncated','offset','raw_digest'):
            bad=copy.deepcopy(index);blob=bytearray(data)
            if mutation=='header':struct.pack_into('<Q',blob,0,index['bytes']+1)
            elif mutation=='payload':blob[-1]^=1
            elif mutation=='truncated':blob=blob[:-1]
            elif mutation=='offset':bad['offset']=1
            else:bad['context_sha256']='f'*64
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):
                factory.read_context(io.BytesIO(blob),bad,selection)

    def test_rehashed_private_payload_still_cannot_replace_authoritative_record(self):
        row,selection=context();stream=io.BytesIO();index=factory.write_context(stream,row,selection)
        envelope=json.loads(gzip.decompress(stream.getvalue()[8:]));envelope['row']['contract_identity_sha256']='f'*64
        raw=json.dumps(envelope,sort_keys=True,separators=(',',':')).encode();packed=gzip.compress(raw,mtime=0)
        bad=dict(index,bytes=len(packed),frame_sha256=coff.digest(packed),context_sha256=coff.digest(raw))
        with self.assertRaises(ValueError):
            factory.read_context(io.BytesIO(struct.pack('<Q',len(packed))+packed),bad,selection)

    def test_partial_or_borrowed_source_context_is_refused_before_writing(self):
        for mutation in ('root','certificate','contract','negative'):
            row,selection=context();before=copy.deepcopy(row)
            if mutation=='root':row['requested_roots'][0]['source_sha256']='f'*64
            elif mutation=='certificate':row['certificate_sha256']='f'*64
            elif mutation=='contract':row['contract_identity_sha256']='f'*64
            else:row['certificate']['blockers']=[dict(code='UNPROVED',evidence=1)]
            stream=io.BytesIO()
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):
                factory.write_context(stream,row,selection)
            self.assertEqual(stream.getvalue(),b'')

    def test_decompression_and_index_geometry_are_bounded(self):
        row,selection=context();stream=io.BytesIO();index=factory.write_context(stream,row,selection)
        for field,value in [('offset',True),('bytes',True),('offset',-1),('bytes',factory.MAX_CONTEXT+1)]:
            bad=dict(index);bad[field]=value
            with self.subTest(field=field,value=value),self.assertRaises(ValueError):
                factory.read_context(stream,bad,selection)
        with patch.object(factory,'MAX_CONTEXT',16):
            with self.assertRaises(ValueError):factory.write_context(io.BytesIO(),row,selection)
        inflated=b'x'*4096
        packed=gzip.compress(inflated,mtime=0)
        bomb=dict(index,bytes=len(packed),frame_sha256=coff.digest(packed),context_sha256=coff.digest(inflated))
        with patch.object(factory,'MAX_CONTEXT',512):
            with self.assertRaises(ValueError):
                factory.read_context(io.BytesIO(struct.pack('<Q',len(packed))+packed),bomb,selection)

    def test_full_selected_cached_and_new_scope_spools_once(self):
        with tempfile.TemporaryDirectory() as td:
            args=metadata_sources(Path(td))
            with patch.object(factory.base,'budget',return_value={}):
                path,indices=factory.spool_selected(*args,{},time.monotonic())
            self.assertEqual(len(indices),2)
            with path.open('rb') as stream:
                for selection in args[5]:
                    row=factory.read_context(stream,indices[selection['root']['original_address']],selection)
                    self.assertEqual(row['requested_roots'],[selection['root']])

    def test_duplicate_selection_or_missing_selected_view_cannot_publish_complete_index(self):
        for mutation in ('duplicate','missing'):
            with tempfile.TemporaryDirectory() as td:
                args=list(metadata_sources(Path(td)))
                if mutation=='duplicate':args[5].append(copy.deepcopy(args[5][0]))
                else:
                    args[3]['observations']=[]
                    with gzip.open(args[4],'wt'):pass
                with self.subTest(mutation=mutation),patch.object(factory.base,'budget',return_value={}):
                    with self.assertRaises(ValueError):factory.spool_selected(*args,{},time.monotonic())
                self.assertFalse((args[0]/'contexts-index.json').exists())

    def test_saved_index_must_match_authenticated_in_memory_index_before_binding(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);spool=root/'contexts.bin';index_path=root/'contexts-index.json'
            row,selection=context();stream=io.BytesIO();index=factory.write_context(stream,row,selection)
            spool.write_bytes(stream.getvalue())
            indices={selection['root']['original_address']:index}
            corrupt=copy.deepcopy(indices);corrupt[selection['root']['original_address']]['offset']=1
            factory.base.save_json(index_path,corrupt)
            protected={}
            with self.assertRaises(ValueError):factory.protect_context_artifacts(spool,index_path,indices,protected)
            self.assertEqual(protected,{})

    def test_both_bound_context_artifacts_are_rechecked_by_terminal_stability(self):
        for changed in ('spool','index'):
            with tempfile.TemporaryDirectory() as td:
                root=Path(td);spool=root/'contexts.bin';index_path=root/'contexts-index.json'
                row,selection=context();stream=io.BytesIO();index=factory.write_context(stream,row,selection)
                spool.write_bytes(stream.getvalue());indices={selection['root']['original_address']:index}
                factory.base.save_json(index_path,indices);protected={}
                hashes=factory.protect_context_artifacts(spool,index_path,indices,protected)
                self.assertEqual(set(protected),{spool.resolve(),index_path.resolve()})
                self.assertEqual(hashes,(factory.base.file_hash(spool),factory.base.file_hash(index_path)))
                with patch.object(factory.base,'ROOT',root):
                    factory.base.stable(protected)
                    if changed=='spool':spool.write_bytes(spool.read_bytes()+b'changed')
                    else:index_path.write_text('{}')
                    with self.subTest(changed=changed),self.assertRaises(ValueError):factory.base.stable(protected)


if __name__=='__main__':unittest.main()
