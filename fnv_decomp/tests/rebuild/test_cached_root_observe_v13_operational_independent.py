"""Whole72/44/116 authored COFF operational checks; no real saved inputs."""
import copy
import gzip
import hashlib
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch
from contextlib import ExitStack

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_root_observe_v13 as observer
import test_cached_root_observe_operational_independent as legacy
from test_coff_code_archive import section,symbol,aux,object_bytes


def whole_authored_fixture():
    """28 two-root and16 one-root recipes; each has an old unrequested root."""
    items=[];all_roots=[];source=b'// Authored V13 operational fixture; no Game source.\n'
    for i in range(44):
        wanted=2 if i<28 else 1;count=wanted+1;functions=[];sections=[];symbols=[]
        for j in range(count):
            historical=j==wanted;address='0x%08x'%((0x05000000 if historical else 0x04000000)+i*0x1000+j*0x100)
            name=('_history_%02d' if historical else '_authored_%02d')%i+('_%02d'%j)
            functions.append(dict(symbol=name,address=address,size=16));sections.append(section('.text',bytes(16),0x60501020))
            symbols.extend([symbol('.text',j+1,storage=3,auxiliary=aux(16,selection=1)),symbol(name,j+1,typ=32)])
        directives=b'   /DEFAULTLIB:"LIBCMT" /DEFAULTLIB:"OLDNAMES" '
        sections.append(section('.drectve',directives,0x100a00));symbols.extend([symbol('.drectve',count+1,storage=3,auxiliary=aux(len(directives),selection=0)),symbol('@feat.00',-1,value=1,storage=3)])
        if i<2:
            sections.append(section('.sxdata',struct.pack('<I',2+3*(wanted-1)),0x300200));symbols.append(symbol('.sxdata',count+2,storage=3,auxiliary=aux(4,selection=0)))
        raw=object_bytes(sections,symbols);object_sha=hashlib.sha256(raw).hexdigest();source_sha=hashlib.sha256(source).hexdigest()
        recipe=dict(source='src/authored_v13_%02d.cpp'%i,compiler='sp1',functions=functions);rid='authored-v13-%02d'%i
        unit=dict(recipe_id=rid,recipe_index=i,status='compiled',recipe=recipe,source=recipe['source'],compiler='sp1',object='authored_v13_%02d.obj'%i,object_sha256=object_sha,source_sha256=source_sha)
        proof=dict(recipe_id=rid,recipe_index=i,status='ok',recipe_unit_sha256=observer.digest(recipe),object_sha256=object_sha,source_sha256_recorded=source_sha,source_sha256_current=source_sha,
            verified_functions=[dict(f,section=j+1,value=0,verdict='match') for j,f in enumerate(functions)],eh_sections=[],eh_errors=[])
        roots=[dict(original_address=f['address'],recipe_id=rid,recipe_index=i,object_sha256=object_sha,source_sha256=source_sha,symbol=f['symbol'],symbol_index=2+3*j,section=j+1,value=0,size=16) for j,f in enumerate(functions)]
        items.append(dict(raw=raw,unit=unit,proof=proof,roots=roots[:wanted],historical_root=roots[-1],source_bytes=source));all_roots.extend(roots[:wanted])
    request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=all_roots);request_sha=hashlib.sha256(observer.canonical(request)+b'\n').hexdigest()
    for item in items:
        u,p,roots=item['unit'],item['proof'],item['roots'];views=[]
        provenance=dict(object_sha256=u['object_sha256'],source_sha256=u['source_sha256'],request_sha256=request_sha,recipe_unit_sha256=p['recipe_unit_sha256'],
            recipe_id=u['recipe_id'],recipe_index=u['recipe_index'],future_opaque={'typed':[True,1,False,0]})
        verification=dict(recipe_index=u['recipe_index'],raw_sha256=hashlib.sha256(b'').hexdigest(),compressed_sha256='c'*64,row_count=0,first_ordinal=None,last_ordinal=None,whole_data_hash_verified_this_read=False,unrequested_frames_verified=False)
        for event,scope in [('SINGLE_ROOT_METADATA_CONTRACT',[r]) for r in roots]+[('RECIPE_UNION_METADATA_CONTRACT',roots)]:
            contract=observer.finite.build_contract(u,p,scope,{},None,copy.deepcopy(provenance))
            views.append(dict(schema_version=1,kind='new-cached-metadata-contract',policy_id=observer.QUALIFIED_POLICY,event=event,requested_roots=copy.deepcopy(scope),contract=contract,
                contract_sha256=observer.digest(contract),new_metadata_contract_sha256=observer.digest(contract),source_frame_verification=copy.deepcopy(verification),native_observation_required=True,**{k:False for k in observer.QUALIFIED_FALSE}))
        item.update(views=views,observation_provenance=dict(qualified_request_sha256=request_sha,authored=True))
    return items,request,request_sha


def qualified_fixture_bytes(items):
    return legacy.qualified_fixture_bytes(items)


class IndependentWholeRecipeTests(unittest.TestCase):
    def test_whole72_roots44_parses116_views_preserve_scope_and_historical_functions(self):
        items,request,request_sha=whole_authored_fixture();self.assertEqual(len(request['roots']),72)
        calls=observer.coff.parse;counts=dict(single=0,union=0,positive_single=0,positive_union=0)
        with patch.object(observer.coff,'parse',wraps=calls) as parser:
            for item in items:
                old=observer.digest(item['views'])
                for row in observer.observe_recipe_contracts(item['raw'],item['unit'],item['proof'],item['roots'],iter(item['views']),item['observation_provenance']):
                    kind='single' if row['event']=='SINGLE_ROOT_OBSERVATION' else 'union';counts[kind]+=1;counts['positive_'+kind]+=row['closure_observed']
                    self.assertNotIn(item['historical_root'],row['requested_roots']);self.assertTrue(row['qualified_contract_unchanged'])
                    self.assertEqual(row['contract']['provenance']['request_sha256'],request_sha)
                self.assertEqual(observer.digest(item['views']),old)
        self.assertEqual(parser.call_count,44);self.assertEqual(counts,dict(single=72,union=44,positive_single=70,positive_union=42))


class IndependentV13BootstrapTests(unittest.TestCase):
    def test_dependency_hash_gate_does_not_trust_unverified_require(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);path=root/'tools/rebuild/authored_helper.py';path.parent.mkdir(parents=True);path.write_bytes(b'# authored helper\n')
            with patch.object(observer,'ROOT',root),patch.object(observer,'PINS',{'authored_helper.py':'0'*64}),patch.object(observer,'require',lambda *a,**kw:None):
                with self.assertRaises(ValueError):observer.bind_dependency_epoch({})

    def test_missing_profile_stops_before_dependency_or_metadata_load(self):
        from types import SimpleNamespace
        with patch.object(observer,'typed_equal',side_effect=AssertionError('unverified helper used during bootstrap')):
            observer.require_actual_authority()
        args=SimpleNamespace(operation=Path('unused'),operation_sha256='0'*64,out=Path('unused'),details=Path('unused'))
        with patch.object(observer,'ACTUAL_OPERATION_PROFILE',None),patch.object(observer,'bind_dependency_epoch',side_effect=AssertionError('dependency used before profile')),patch.object(observer,'read_bound_json',side_effect=AssertionError('metadata read before profile')):
            with self.assertRaises(ValueError):observer.run(args)


class IndependentV13WholeRunTests(unittest.TestCase):
    def setup_context(self,td):
        with patch.object(legacy,'observer',observer),patch.object(legacy,'whole_authored_fixture',whole_authored_fixture):
            context=legacy.IndependentFullRunTests().setup_context(td)
        context[2]['previous_native_recipe_overlap']=list(range(44))
        context[2]['current_successor_join']={'authored_metadata_admission_stub':True}
        return context

    def run_authored(self,context,**kwargs):
        # Only source/dependency and complete metadata admission are stubs.
        # Authored sources/objects, hashes, parsers, 4bf, reader and publisher run.
        with patch.object(legacy,'observer',observer),patch.object(observer,'bind_dependency_epoch',return_value=None):
            return legacy.IndependentFullRunTests().run_authored(context,**kwargs)

    def test_complete72_44_116_actual_authored_first_recipe_and_closed_publisher(self):
        with tempfile.TemporaryDirectory() as td:
            ctx=self.setup_context(td);parse=observer.coff.parse
            with patch.object(observer.coff,'parse',wraps=parse) as parsed:result=self.run_authored(ctx)
            self.assertEqual(parsed.call_count,44);self.assertEqual(result['native_object_observation_reads'],44)
            self.assertEqual(result['summary'],dict(roots=72,recipes=44,records=116,singleton_closure=70,singleton_blocked=2,union_closure=42,union_blocked=2))
            self.assertEqual(result['previous_native_recipe_overlap'],list(range(44)));self.assertEqual(result['historical_roots_reobserved'],0)
            self.assertEqual(result['current_successor_join'],{'authored_metadata_admission_stub':True})
            self.assertEqual(json.loads(ctx[1].out.read_bytes()),result)
            with gzip.open(ctx[1].details,'rt') as stream:rows=[json.loads(line) for line in stream]
            self.assertEqual(len(rows),116)
            for ordinal,(row,qualified) in enumerate(zip(rows,ctx[5]),1):
                self.assertEqual(row['qualified_record_ordinal'],ordinal)
                self.assertEqual(observer.canonical(row['contract']),observer.canonical(qualified['contract']))
                self.assertEqual(row['qualified_metadata_row_sha256'],observer.digest(qualified))
            self.assertTrue(all(result[k] is False for k in observer.FALSE))
            self.assertFalse((ctx[1].out.parent/'abort.json').exists())

    def test_late_gzip_identity_failure_cannot_publish_any_success(self):
        with tempfile.TemporaryDirectory() as td:
            ctx=self.setup_context(td);op=ctx[3];op['artifacts']['qualified_records']['sha256']='0'*64
            ctx[1].operation.write_bytes(observer.canonical(op)+b'\n');ctx[1].operation_sha256=hashlib.sha256(ctx[1].operation.read_bytes()).hexdigest()
            with patch.object(observer.coff,'parse',wraps=observer.coff.parse) as parsing:
                with self.assertRaises(ValueError):self.run_authored(ctx)
                self.assertEqual(parsing.call_count,44)
            self.assertFalse(ctx[1].out.exists());self.assertFalse(ctx[1].details.exists())

    def test_semantically_same_compressed_stream_with_changed_header_fails_exact_consumed_hash(self):
        with tempfile.TemporaryDirectory() as td:
            ctx=self.setup_context(td);alternate=gzip.compress(ctx[6],mtime=123)
            ctx[2]['paths']['qualified_records'].write_bytes(alternate)
            self.assertEqual(gzip.decompress(alternate),ctx[6])
            with patch.object(observer.coff,'parse',wraps=observer.coff.parse) as parsing:
                with self.assertRaises(ValueError):self.run_authored(ctx)
                self.assertEqual(parsing.call_count,44)
            self.assertFalse(ctx[1].out.exists());self.assertFalse(ctx[1].details.exists())

    def test_original_stale_source_or_object_aborts_before_first_parse(self):
        for mode in ('source','object'):
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as td:
                ctx=self.setup_context(td);item=ctx[4][0]
                path=ctx[0]/item['unit']['source'] if mode=='source' else ctx[2]['paths']['manifest'].parent/item['unit']['object']
                path.write_bytes(b'authored stale original')
                with patch.object(observer.coff,'parse',wraps=observer.coff.parse) as parsing:
                    with self.assertRaises(ValueError):self.run_authored(ctx)
                    parsing.assert_not_called()
                self.assertFalse(ctx[1].out.exists());self.assertFalse(ctx[1].details.exists())

    def test_detail_summary_and_protected_source_postwrite_drift_retracts_both(self):
        for mode in ('details','summary','source'):
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as td:
                ctx=self.setup_context(td)
                with self.assertRaises(ValueError):self.run_authored(ctx,drift=mode)
                self.assertFalse(ctx[1].out.exists());self.assertFalse(ctx[1].details.exists())

    def test_foreign_replacement_preserved_and_journal_close_failure_removes_success(self):
        with tempfile.TemporaryDirectory() as td:
            ctx=self.setup_context(td)
            with self.assertRaises(ValueError):self.run_authored(ctx,drift='foreign')
            self.assertEqual(ctx[1].out.read_bytes(),b'foreign replacement must survive')
        with tempfile.TemporaryDirectory() as td:
            ctx=self.setup_context(td)
            with self.assertRaises(OSError):self.run_authored(ctx,close_failure=True)
            self.assertFalse(ctx[1].out.exists());self.assertFalse(ctx[1].details.exists())

    def test_foreign_output_refused_before_any_named_source_or_object_read(self):
        with tempfile.TemporaryDirectory() as td:
            ctx=self.setup_context(td);ctx[1].out=ctx[0]/'foreign.json';ctx[1].details=ctx[0]/'foreign.jsonl.gz'
            opened=[];original=Path.open
            def access(path,*a,**kw):
                if path.suffix in ('.cpp','.obj'):opened.append(path)
                return original(path,*a,**kw)
            with patch.object(Path,'open',access),self.assertRaises(ValueError):self.run_authored(ctx)
            self.assertEqual(opened,[]);self.assertFalse(ctx[1].out.exists());self.assertFalse(ctx[1].details.exists())


if __name__=='__main__':unittest.main()
