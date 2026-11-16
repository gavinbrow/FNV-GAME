"""Authored metadata and gzip bytes only; no saved production stream pass."""
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import binding_context_cache as c
from test_runtime_code_inventory import field,choice


def fixture():
    units=[];proofs=[];selections={};providers={};rows=[]
    for i in range(3):
        address='0x%08x'%(0x500000+i*256);symbol='_original1';recipe=dict(source='authored%d.cpp'%i,compiler='authored',functions=[dict(symbol=symbol,address=address,size=16)])
        unit=dict(recipe_index=i,recipe_id='fixture'+str(i),status='compiled',recipe=recipe,source_sha256='a'*64,object_sha256=('%064x'%(i+1)))
        proof=dict(recipe_index=i,recipe_id=unit['recipe_id'],status='ok',object_sha256=unit['object_sha256'],source_sha256_recorded='a'*64,
            source_sha256_current='a'*64,recipe_unit_sha256=c.digest(recipe),verified_functions=[dict(symbol=symbol,address=address,size=16,section=1,value=0,verdict='match')])
        selected=dict(choice(address),recipe_index=i,recipe_id=unit['recipe_id'])
        selections[address]=selected;providers[address]=dict(recipe_id=unit['recipe_id'],object_sha256=unit['object_sha256'],source_sha256='a'*64,
            symbol_index=8,symbol=symbol,section=1,value=0,size=16)
        units.append(unit);proofs.append(proof)
        if i!=1:
            row=field(address);row.update(recipe_index=i,recipe_id=unit['recipe_id'])
            if i==2:row.update(coff_relocation=None,event='MISSING_ORIGINAL_HIGHLOW_SOURCE_MIGRATION_BLOCKER',classification='MISSING_SOURCE_RELOCATION_NO_SYNTHESIS')
            else:
                row['classification']='AUTHORED_UNKNOWN_CLASS';row['coff_relocation']['kind']=11;row['opaque_future_field']={'unknown':[True,None,'preserve me']}
            rows.append(row)
    raw=[(json.dumps(rows[0],indent=None,separators=(', ', ': '))+'\r\n').encode(),json.dumps(rows[1],sort_keys=True).encode()]
    summary=dict(events=dict(c.Counter(r['event'] for r in rows)),target_classes=dict(c.Counter(r['classification'] for r in rows)),
        relocation_kinds=dict(c.Counter(str(r['coff_relocation']['kind']) for r in rows if r['coff_relocation'])),
        proof_consistency=dict(c.Counter(r['proof_consistency'] for r in rows if r['coff_relocation'])))
    seq=hashlib.sha256()
    for i,row in enumerate(rows,1):seq.update(c.canonical([i,c.digest(row)]))
    rosters=c.make_rosters(dict(units=units),dict(units=proofs),selections,
        dict(providers=providers,materialized_exports=0,provider_selected=False,runtime_eligible=False),expected_units=3,expected_selected=3)
    target=io.BytesIO();result=c.build_frames(raw,target,rosters,selections,summary,required_missing=1,required_functions=1,expected_sequence=seq.hexdigest())
    index=dict(schema_version=1,policy_id=c.POLICY,inputs=c.PINS,units=3,selected_functions=3,**result,**c.FALSE)
    return raw,rows,units,proofs,selections,summary,rosters,target.getvalue(),index


class BindingCacheTests(unittest.TestCase):
    def test_exact_raw_lines_unknown_fields_missing_and_zero_row_frame(self):
        raw,rows,units,proofs,sels,summary,rosters,data,index=fixture()
        self.assertEqual(index['rows'],2);self.assertEqual(len(index['frames']),3)
        self.assertEqual(index['frames'][1]['row_count'],0);self.assertIsNone(index['frames'][1]['first_ordinal'])
        self.assertEqual(index['frames'][1]['roster'][0][6:],[0,0])
        self.assertEqual(rosters[0]['roster'][0][6:],[0,0])
        recovered=[]
        for e in index['frames']:recovered+=list(c.frame_lines(io.BytesIO(data),e,c.time.monotonic()))
        self.assertEqual(recovered,raw)
        self.assertEqual(index['original_raw_sha256'],hashlib.sha256(b''.join(raw)).hexdigest())

    def test_original_global_ordinals_and_frozen_buckets_equal(self):
        raw,rows,units,proofs,sels,summary,_,data,index=fixture()
        direct=c.frozen.BindingReader(raw,summary,sels);expected=[direct.take(i) for i in range(3)];direct.finish(1,1)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'data';p.write_bytes(data)
            for i in range(3):
                bucket,verification=c._read_recipe(p,index,i,sels,units[i],proofs[i])
                self.assertEqual(bucket,expected[i]);self.assertFalse(verification['runtime_eligible'])
            self.assertEqual(expected[2]['0x00500200']['row_identities'][0]['ordinal'],2)

    def test_same_frozen_contract_and_observer_result_from_cached_authored_fields(self):
        from test_scalableordinary_root_collect import fixture as native_fixture
        import scalableordinary_root_collect as finite
        import coff_code_archive as coff
        import root_code_closure as ordinary
        raw,unit,proof,requests,sels,providers,buckets=native_fixture(field=True)
        row=copy.deepcopy(buckets['0x00500000']['fields'][0])
        row.update(event='SELECTED_FUNCTION_COFF_RELOCATION',recipe_index=0,runtime_eligible=False,provider_selected=False)
        row['coff_relocation']['conservative_extent']=4
        lines=[(json.dumps(row,separators=(', ', ': '))+'\r\n').encode()]
        summary=dict(events={row['event']:1},target_classes={row['classification']:1},relocation_kinds={'20':1},proof_consistency={row['proof_consistency']:1})
        planned={r['original_address']:{k:r[k] for k in ('recipe_id','object_sha256','source_sha256','symbol_index','symbol','section','value','size')} for r in requests}
        rosters=c.make_rosters(dict(units=[unit]),dict(units=[proof]),sels,
            dict(providers=planned,materialized_exports=0,provider_selected=False,runtime_eligible=False),expected_units=1,expected_selected=2)
        expected_seq=hashlib.sha256(c.canonical([1,c.digest(row)])).hexdigest();target=io.BytesIO()
        result=c.build_frames(lines,target,rosters,sels,summary,required_missing=0,required_functions=0,expected_sequence=expected_seq)
        index=dict(policy_id=c.POLICY,inputs=c.PINS,**result)
        reader=c.frozen.BindingReader(lines,summary,sels);direct=reader.take(0);reader.finish(0,0)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'frames';path.write_bytes(target.getvalue())
            cached,_=c._read_recipe(path,index,0,sels,unit,proof)
        provenance=dict(object_sha256=unit['object_sha256'],source_sha256=unit['source_sha256'])
        a=finite.build_contract(unit,proof,requests[:1],direct,{},provenance)
        b=finite.build_contract(unit,proof,requests[:1],cached,{},provenance)
        self.assertEqual(a,b)
        self.assertEqual(ordinary.assess_object(coff.parse(raw),a),ordinary.assess_object(coff.parse(raw),b))

    def test_crc_trailing_truncation_and_hash_mismatch_rejected(self):
        *_,data,index=fixture();entry=index['frames'][0]
        bads=[data[:entry['compressed_bytes']-1],bytes([data[0]^1])+data[1:],data[:entry['compressed_bytes']]+b'extra']
        for bad in bads:
            e=copy.deepcopy(entry)
            if bad.endswith(b'extra'):e['compressed_bytes']+=5
            with self.assertRaises((ValueError,c.zlib.error)):list(c.frame_lines(io.BytesIO(bad),e,c.time.monotonic()))
        bad=copy.deepcopy(entry);bad['raw_sha256']='0'*64
        with self.assertRaises(ValueError):list(c.frame_lines(io.BytesIO(data),bad,c.time.monotonic()))

    def test_concatenated_member_cannot_be_one_recipe_frame(self):
        *_,data,index=fixture();e=copy.deepcopy(index['frames'][0]);e['compressed_bytes']+=index['frames'][1]['compressed_bytes']
        with self.assertRaises(ValueError):list(c.frame_lines(io.BytesIO(data),e,c.time.monotonic()))

    def test_streaming_decoder_crosses_output_chunk_without_losing_bytes(self):
        raw=(b'a'*100000+b'\n')*25+b'last unterminated line';encoder=c.zlib.compressobj(wbits=31)
        data=encoder.compress(raw)+encoder.flush()
        e=dict(offset=0,compressed_bytes=len(data),compressed_sha256=hashlib.sha256(data).hexdigest(),
               raw_bytes=len(raw),raw_sha256=hashlib.sha256(raw).hexdigest())
        lines=list(c.frame_lines(io.BytesIO(data),e,c.time.monotonic()))
        self.assertEqual(b''.join(lines),raw);self.assertEqual(len(lines),26)

    def test_foreign_unsorted_duplicate_and_long_original_rows_fail(self):
        raw,rows,units,proofs,sels,summary,rosters,_,_=fixture()
        cases=[list(reversed(raw)),[raw[0],raw[0],raw[1]],[b'x'*(c.MAX_LINE+1)]]
        row=copy.deepcopy(rows[0]);row['recipe_index']=99;cases.append([json.dumps(row).encode()])
        for lines in cases:
            with self.assertRaises((ValueError,KeyError)):
                c.build_frames(lines,io.BytesIO(),rosters,sels,summary,required_missing=1,required_functions=1,expected_sequence='0'*64)

    def test_wrong_global_sequence_and_roster_location_fail(self):
        raw,rows,units,proofs,sels,summary,rosters,_,_=fixture()
        with self.assertRaises(ValueError):c.build_frames(raw,io.BytesIO(),rosters,sels,summary,required_missing=1,required_functions=1,expected_sequence='0'*64)
        proofs[0]['verified_functions'][0]['section']=2
        with self.assertRaises(ValueError):c.make_rosters(dict(units=units),dict(units=proofs),sels,
            dict(providers={},materialized_exports=0,provider_selected=False,runtime_eligible=False),expected_units=3,expected_selected=3)

    def test_requested_frame_read_does_not_claim_whole_file_verification(self):
        _,_,units,proofs,sels,_,_,data,index=fixture()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'data';p.write_bytes(data)
            bucket,v=c._read_recipe(p,index,0,sels,units[0],proofs[0]);self.assertIn('0x00500000',bucket)
            self.assertFalse(v['whole_data_hash_verified_this_read']);self.assertFalse(v['unrequested_frames_verified'])
            bad=copy.deepcopy(units[0]);bad['object_sha256']='f'*64
            with self.assertRaises(ValueError):c._read_recipe(p,index,0,sels,bad,proofs[0])

    def test_reader_checks_frame_census_ordinal_roster_and_file_size(self):
        _,_,units,proofs,sels,_,_,data,index=fixture()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'data';p.write_bytes(data)
            for key,val in [('preceding_ordinal',99),('row_count',2),('row_sequence_sha256','f'*64)]:
                bad=copy.deepcopy(index);bad['frames'][0][key]=val
                with self.subTest(key=key),self.assertRaises(ValueError):c._read_recipe(p,bad,0,sels,units[0],proofs[0])
            p.write_bytes(data+b'changed')
            with self.assertRaises(ValueError):c._read_recipe(p,index,0,sels,units[0],proofs[0])

    def test_public_index_rejects_wrong_hash_and_nonproduction_scope(self):
        *_,index=fixture()
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'index';path.write_bytes(c.canonical(index))
            with self.assertRaises(ValueError):c.load_index(path,'0'*64)
            with self.assertRaises(ValueError):c.load_index(path,c.file_hash(path))

    def test_loader_hashes_the_exact_single_read_not_a_separate_snapshot(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'index';original={'data_bytes':1,'identity':'original'};other={'data_bytes':1,'identity':'replacement'}
            raw=c.canonical(original);path.write_bytes(raw);expected=hashlib.sha256(raw).hexdigest()
            with patch.object(c,'file_hash',return_value=expected) as separate_hash,\
                 patch.object(Path,'read_bytes',return_value=c.canonical(other)) as separate_read,\
                 patch.object(c,'validate_index'):
                self.assertEqual(c.load_index(path,expected),original)
                separate_hash.assert_not_called();separate_read.assert_not_called()
            path.write_bytes(c.canonical(other))
            with patch.object(c,'validate_index'),self.assertRaisesRegex(ValueError,'hash differs'):c.load_index(path,expected)

    def test_index_overlap_is_rejected_before_final_coverage_check(self):
        *_,index=fixture();index.update(units=2988,selected_functions=68657,rows=490801,row_sequence_sha256=c.SEQUENCE)
        index['frames'][1]['offset']=0
        with self.assertRaisesRegex(ValueError,'gap/overlap'):c.validate_index(index)

    def test_raw_decompression_and_line_bounds_reject_inflation(self):
        *_,index=fixture();e=copy.deepcopy(index['frames'][0]);encoder=c.zlib.compressobj(wbits=31)
        data=encoder.compress(b'x'*(c.MAX_LINE+1))+encoder.flush();e['compressed_bytes']=len(data);e['raw_bytes']=c.MAX_LINE+1
        with self.assertRaisesRegex(ValueError,'line bound'):list(c.frame_lines(io.BytesIO(data),e,c.time.monotonic()))

    def test_fixed_resource_caps_and_no_contract_creation(self):
        self.assertEqual(c.MAX_OUTPUT,128*1024**2);self.assertEqual(c.MAX_MEMORY,1024**3);self.assertEqual(c.MAX_SECONDS,900)
        self.assertFalse(c.FALSE['contract_created']);self.assertFalse(c.FALSE['admission_decision_created'])

    def test_generated_artifact_drift_fails_exact_expected_hashes(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'frames';p.write_bytes(b'authored frame bytes');expected={p:c.file_hash(p)}
            c.verify_hashes(expected,'changed')
            p.write_bytes(b'changed bytes')
            with self.assertRaisesRegex(ValueError,'changed'):c.verify_hashes(expected,'changed')
