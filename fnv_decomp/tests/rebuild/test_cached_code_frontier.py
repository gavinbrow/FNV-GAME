"""Authored metadata only; no production inputs."""
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_code_frontier as subject
import binding_context_cache as cache_module
from test_binding_context_cache import fixture


class AuthoredReader:
    def __init__(self,path,index):self.path=path;self.index=index;self.calls=[]
    def read_recipe(self,i,selections,unit,proof):
        self.calls.append(i)
        return cache_module._read_recipe(self.path,self.index,i,selections,unit,proof)


class CachedContextTests(unittest.TestCase):
    def test_unknown_missing_and_empty_recipe_contracts_preserve_exact_rows(self):
        _,_,units,proofs,selections,_,_,data,index=fixture()
        raw,rows,units,proofs,selections,summary,rosters,_,_=fixture()
        for row in rows:
            if row['coff_relocation']:
                row['coff_relocation'].update(symbol_storage=2,symbol='_authored_target')
        lines=[subject.canonical(row)+b'\n' for row in rows]
        seq=hashlib.sha256()
        for ordinal,row in enumerate(rows,1):seq.update(subject.canonical([ordinal,subject.digest(row)]))
        stage=io.BytesIO()
        result=cache_module.build_frames(lines,stage,rosters,selections,summary,
                    required_missing=1,required_functions=1,expected_sequence=seq.hexdigest())
        data=stage.getvalue();index=dict(policy_id=cache_module.POLICY,inputs=cache_module.PINS,**result)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'frames';path.write_bytes(data);reader=AuthoredReader(path,index)
            for i in range(3):
                u=units[i];r=index['frames'][i]['roster'][0]
                root=dict(original_address=r[0],symbol=r[1],section=r[2],value=r[3],size=r[4],symbol_index=r[5],
                          recipe_index=i,recipe_id=u['recipe_id'],object_sha256=u['object_sha256'],source_sha256=u['source_sha256'])
                result=subject.build_recipe_contexts(reader,i,selections,u,proofs[i],[root],None,{'authored':True})
                self.assertEqual([x['event'] for x in result['records']],['SINGLE_ROOT_METADATA_CONTRACT','RECIPE_UNION_METADATA_CONTRACT'])
                a,b=result['records'];self.assertEqual(subject.canonical(a['contract']),subject.canonical(b['contract']))
                self.assertFalse(result['certificate_created']);self.assertTrue(result['native_observation_required'])
                self.assertEqual(a['contract_sha256'],subject.digest(a['contract']))
                if i==0:self.assertEqual(a['contract']['fields'][0]['opaque_future_field'],{'unknown':[True,None,'preserve me']})
                if i==1:self.assertEqual(a['contract']['fields'],[])
                if i==2:self.assertEqual(len(a['contract']['missing_fields']),1)
            self.assertEqual(reader.calls,[0,1,2])

    def test_same_bytes_hash_parse_refuses_wrong_hash_and_bound(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'json';raw=b'{"a":true}';p.write_bytes(raw);sha=hashlib.sha256(raw).hexdigest()
            self.assertEqual(subject.read_bound_json(p,sha),{'a':True})
            with self.assertRaises(ValueError):subject.read_bound_json(p,'0'*64)
            with self.assertRaises(ValueError):subject.read_bound_json(p,sha,limit=2)


if __name__=='__main__':unittest.main()
