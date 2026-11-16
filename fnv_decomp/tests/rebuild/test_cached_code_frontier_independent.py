"""Independent full-unit metadata equivalence; authored rows/frames only."""
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
import cached_code_frontier as consumer
import binding_context_cache as cache_module
from test_binding_context_cache import fixture as initial_fixture


def fixture():
    _,original,units,proofs,_,_,_,_,_=initial_fixture()
    unit=copy.deepcopy(units[0]);proof=copy.deepcopy(proofs[0]);addresses=['0x00500000','0x00500080']
    functions=[dict(symbol='_original1',address=addresses[0],size=16),dict(symbol='_unrequested',address=addresses[1],size=16)]
    unit['recipe']['functions']=functions;proof['recipe_unit_sha256']=cache_module.digest(unit['recipe'])
    proof['verified_functions']=[dict(f,section=i+1,value=0,verdict='match') for i,f in enumerate(functions)]
    proof['eh_sections']=[[2,12,False,addresses[1],['authored-parent']]]
    selections={};providers={};requested=[]
    for i,f in enumerate(functions):
        selections[f['address']]=dict(recipe_id=unit['recipe_id'],recipe_index=0,symbol=f['symbol'],section=i+1,value=0,size=16,
            selection_status='CODE_OWNERSHIP_SELECTED',runtime_eligible=False,link_ready=False)
        root=dict(original_address=f['address'],recipe_id=unit['recipe_id'],recipe_index=0,object_sha256=unit['object_sha256'],
            source_sha256=unit['source_sha256'],symbol=f['symbol'],symbol_index=8+i*3,section=i+1,value=0,size=16)
        requested.append(root);providers[f['address']]={k:v for k,v in root.items() if k not in ('original_address','recipe_index')}
    first=copy.deepcopy(original[0]);first['coff_relocation'].update(symbol_storage=2,symbol='_unknown')
    first['opaque_future_field']={'all':[True,1,False,0,None,{'unknown':'preserved'}]}
    other=copy.deepcopy(first);other.update(function_va=addresses[1],function_symbol='_unrequested',physical_section=2,
        original_field_va='0x00500084',classification='AUTHORED_LOCAL_LABEL_UNKNOWN')
    other['coff_relocation'].update(symbol_storage=6,symbol='$LN_authored',symbol_type=0)
    missing=copy.deepcopy(other);missing.update(event='MISSING_ORIGINAL_HIGHLOW_SOURCE_MIGRATION_BLOCKER',
        source_field_offset=8,physical_offset=8,original_field_va='0x00500088',coff_relocation=None,
        classification='MISSING_SOURCE_RELOCATION_NO_SYNTHESIS')
    rows=[first,other,missing]
    lines=[(json.dumps(rows[0],separators=(', ',': '))+'\r\n').encode(),
           (json.dumps(rows[1],sort_keys=True)+'\n').encode(),json.dumps(rows[2]).encode()]
    summary=dict(events=dict(cache_module.Counter(r['event'] for r in rows)),
        target_classes=dict(cache_module.Counter(r['classification'] for r in rows)),
        relocation_kinds=dict(cache_module.Counter(str(r['coff_relocation']['kind']) for r in rows if r['coff_relocation'])),
        proof_consistency=dict(cache_module.Counter(r['proof_consistency'] for r in rows if r['coff_relocation'])))
    rosters=cache_module.make_rosters(dict(units=[unit]),dict(units=[proof]),selections,
        dict(providers=providers,materialized_exports=0,provider_selected=False,runtime_eligible=False),expected_units=1,expected_selected=2)
    sequence=hashlib.sha256(b''.join(cache_module.canonical([i,cache_module.digest(r)]) for i,r in enumerate(rows,1))).hexdigest()
    data=io.BytesIO();result=cache_module.build_frames(lines,data,rosters,selections,summary,
        required_missing=1,required_functions=1,expected_sequence=sequence)
    index=dict(schema_version=1,policy_id=cache_module.POLICY,inputs=cache_module.PINS,**result)
    return unit,proof,selections,requested,lines,summary,index,data.getvalue()


class AuthoredCache:
    """Real framed reader with synthetic index; not a receipt admission fixture."""
    def __init__(self,path,index):self.path=path;self.index=index;self.calls=[]
    def read_recipe(self,index,selections,unit,proof):
        self.calls.append(index)
        return cache_module._read_recipe(self.path,self.index,index,selections,unit,proof)


class IndependentCacheConsumerTests(unittest.TestCase):
    def context(self,td):
        unit,proof,selections,roots,lines,summary,index,data=fixture()
        path=Path(td)/'authored.frames';path.write_bytes(data)
        return AuthoredCache(path,index),unit,proof,selections,roots,lines,summary

    def build(self,context,roots=None):
        cache,unit,proof,selections,requested,_,_=context
        return consumer.build_recipe_contexts(cache,0,selections,unit,proof,requested if roots is None else roots,
            {'observation_only':{'unknown':True}},dict(original='kept',typed=[True,1]))

    def test_singletons_and_union_are_typed_full_contract_equivalent_to_direct_reader(self):
        with tempfile.TemporaryDirectory() as td:
            ctx=self.context(td);cache,unit,proof,selections,roots,lines,summary=ctx
            before=consumer.canonical([unit,proof,selections,roots]);result=self.build(ctx)
            direct=cache_module.frozen.BindingReader(lines,summary,selections);bucket=direct.take(0);direct.finish(1,1)
            scopes=[[roots[0]],[roots[1]],roots]
            self.assertEqual(cache.calls,[0]);self.assertEqual(len(result['records']),3)
            for record,scope in zip(result['records'],scopes):
                expected=consumer.finite.build_contract(unit,proof,scope,bucket,{'observation_only':{'unknown':True}},dict(original='kept',typed=[True,1]))
                self.assertEqual(consumer.canonical(record['contract']),consumer.canonical(expected))
                self.assertEqual(record['contract_sha256'],consumer.digest(expected))
                self.assertTrue(all(record[k] is False for k in consumer.FALSE))
                self.assertFalse(record['source_frame_verification']['whole_data_hash_verified_this_read'])
            self.assertEqual(before,consumer.canonical([unit,proof,selections,roots]));self.assertFalse(result['certificate_created'])
            self.assertTrue(result['native_observation_required'])
            self.assertEqual(result['records'][0]['contract']['parent_eh'],[])
            self.assertEqual(result['records'][-1]['contract']['parent_eh'],proof['eh_sections'])

    def test_unrequested_label_uses_missing_rows_and_unknown_payload_remain_present(self):
        with tempfile.TemporaryDirectory() as td:
            ctx=self.context(td);root=ctx[4][0];result=self.build(ctx,[root]);contract=result['records'][0]['contract']
            self.assertEqual(contract['fields'][0]['opaque_future_field']['all'][:4],[True,1,False,0])
            self.assertEqual(len(contract['omission_field_proofs']),1)
            self.assertEqual(contract['omission_field_proofs'][0]['function_va'],'0x00500080')
            self.assertEqual(len(contract['provenance']['omission_binding_row_references']),3)
            both=self.build(ctx);self.assertEqual(len(both['records'][1]['contract']['missing_fields']),1)
            self.assertEqual(both['records'][1]['contract']['missing_fields'][0]['classification'],'MISSING_SOURCE_RELOCATION_NO_SYNTHESIS')

    def test_wrong_native_slot_duplicate_foreign_or_boolean_request_is_rejected(self):
        for mode in ('slot','duplicate','source','object','value_bool','extra'):
            with tempfile.TemporaryDirectory() as td:
                ctx=self.context(td);roots=copy.deepcopy(ctx[4])
                if mode=='slot':roots[0]['symbol_index']+=1
                elif mode=='duplicate':roots[1]=copy.deepcopy(roots[0])
                elif mode in ('source','object'):roots[0][mode+'_sha256']='f'*64
                elif mode=='value_bool':roots[0]['value']=False
                else:roots[0]['admitted']=True
                with self.subTest(mode=mode),self.assertRaises(ValueError):self.build(ctx,roots)

    def test_typed_native_proof_and_selection_flags_cannot_alias_frozen_values(self):
        for mode in ('unit_index','proof_index','proof_value','proof_section','proof_size','runtime_flag','link_flag'):
            with tempfile.TemporaryDirectory() as td:
                ctx=self.context(td);_,unit,proof,selections,roots,_,_=ctx
                if mode=='unit_index':unit['recipe_index']=False
                elif mode=='proof_index':proof['recipe_index']=False
                elif mode.startswith('proof_'):proof['verified_functions'][0][mode[6:]]=False
                else:selections[roots[0]['original_address']]['runtime_eligible' if mode=='runtime_flag' else 'link_ready']=0
                with self.subTest(mode=mode),self.assertRaises(ValueError):self.build(ctx)

    def test_bad_raw_or_compressed_frame_identity_cannot_yield_contracts(self):
        for mode in ('raw','compressed','ordinal','count','data'):
            with tempfile.TemporaryDirectory() as td:
                ctx=self.context(td);cache=ctx[0];entry=cache.index['frames'][0]
                if mode in ('raw','compressed'):entry[mode+'_sha256']='f'*64
                elif mode=='ordinal':entry['preceding_ordinal']=2
                elif mode=='count':entry['row_count']+=1
                else:cache.path.write_bytes(cache.path.read_bytes()+b'trailing')
                with self.subTest(mode=mode),self.assertRaises(ValueError):self.build(ctx)

    def test_bound_JSON_parses_only_the_exact_hashed_buffer(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'authored.json';original=b'{"nested":[true,1],"value":"accepted"}'
            path.write_bytes(original);expected=hashlib.sha256(original).hexdigest()
            self.assertEqual(consumer.read_bound_json(path,expected),json.loads(original))
            path.write_bytes(b'{"value":"changed"}')
            with self.assertRaises(ValueError):consumer.read_bound_json(path,expected)
            path.write_bytes(original)
            with self.assertRaises(ValueError):consumer.read_bound_json(path,expected,limit=4)
            opened=io.BytesIO(b'{"value":"loaded-other-bytes"}')
            with patch('builtins.open',return_value=opened),self.assertRaises(ValueError):consumer.read_bound_json(path,expected)


if __name__=='__main__':unittest.main()
