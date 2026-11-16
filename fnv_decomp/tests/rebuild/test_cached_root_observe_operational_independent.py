"""Operational integration fixtures: authored COFF/metadata, no real inputs."""
import copy
import gzip
import hashlib
import io
from pathlib import Path
from contextlib import ExitStack
import json
import struct
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_root_observe as observer
from test_coff_code_archive import section,symbol,aux,object_bytes
from test_cached_root_observe import fixture as small_fixture


def whole_authored_fixture():
    """Exactly180 roots/77 recipes/257 views; one busy28-root unit."""
    recipes=[];all_roots=[];source=b'// Authored operational fixture only; no Game source.\n'
    for i in range(77):
        count=28 if i==0 else 2;functions=[];sections=[];symbols=[]
        for j in range(count):
            name='_authored_%02d_%02d'%(i,j);a='0x%08x'%(0x01000000+i*0x10000+j*0x100)
            functions.append(dict(symbol=name,address=a,size=16))
            sections.append(section('.text',bytes(16),0x60501020))
            symbols.extend([symbol('.text',j+1,storage=3,auxiliary=aux(16,selection=1)),symbol(name,j+1,typ=32)])
        directives=b'   /DEFAULTLIB:"LIBCMT" /DEFAULTLIB:"OLDNAMES" '
        sections.append(section('.drectve',directives,0x100a00))
        symbols.extend([symbol('.drectve',count+1,storage=3,auxiliary=aux(len(directives),selection=0)),symbol('@feat.00',-1,value=1,storage=3)])
        if i<2:
            payload=struct.pack('<I',2+3*(count-1));sections.append(section('.sxdata',payload,0x300200))
            symbols.append(symbol('.sxdata',count+2,storage=3,auxiliary=aux(4,selection=0)))
        raw=object_bytes(sections,symbols);object_sha=hashlib.sha256(raw).hexdigest();source_sha=hashlib.sha256(source).hexdigest()
        recipe=dict(source='src/authored_%02d.cpp'%i,compiler='sp1',functions=functions);rid='authored-operational-%02d'%i
        unit=dict(recipe_id=rid,recipe_index=i,status='compiled',recipe=recipe,source=recipe['source'],compiler='sp1',
            object='authored_%02d.obj'%i,object_sha256=object_sha,source_sha256=source_sha)
        proof=dict(recipe_id=rid,recipe_index=i,status='ok',recipe_unit_sha256=observer.digest(recipe),object_sha256=object_sha,
            source_sha256_recorded=source_sha,source_sha256_current=source_sha,
            verified_functions=[dict(f,section=j+1,value=0,verdict='match') for j,f in enumerate(functions)],eh_sections=[],eh_errors=[])
        roots=[dict(original_address=f['address'],recipe_id=rid,recipe_index=i,object_sha256=object_sha,source_sha256=source_sha,
            symbol=f['symbol'],symbol_index=2+3*j,section=j+1,value=0,size=16) for j,f in enumerate(functions)]
        recipes.append(dict(raw=raw,unit=unit,proof=proof,roots=roots,source_bytes=source));all_roots.extend(roots)
    request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=all_roots)
    request_sha=hashlib.sha256(observer.canonical(request)+b'\n').hexdigest()
    for item in recipes:
        unit=item['unit'];proof=item['proof'];roots=item['roots'];views=[]
        provenance=dict(object_sha256=unit['object_sha256'],source_sha256=unit['source_sha256'],request_sha256=request_sha,
            original_future_provenance={'typed':[True,1,False,0]})
        verification=dict(recipe_index=unit['recipe_index'],raw_sha256=hashlib.sha256(b'').hexdigest(),
            compressed_sha256='c'*64,row_count=0,first_ordinal=None,last_ordinal=None,
            whole_data_hash_verified_this_read=False,unrequested_frames_verified=False)
        for event,scope in [('SINGLE_ROOT_METADATA_CONTRACT',[root]) for root in roots]+[('RECIPE_UNION_METADATA_CONTRACT',roots)]:
            contract=observer.finite.build_contract(unit,proof,scope,{},None,copy.deepcopy(provenance))
            views.append(dict(schema_version=1,kind='new-cached-metadata-contract',policy_id=observer.QUALIFIED_POLICY,
                event=event,requested_roots=copy.deepcopy(scope),contract=contract,contract_sha256=observer.digest(contract),
                new_metadata_contract_sha256=observer.digest(contract),source_frame_verification=copy.deepcopy(verification),
                native_observation_required=True,**{k:False for k in observer.QUALIFIED_FALSE}))
        item.update(views=views,observation_provenance=dict(qualified_request_sha256=request_sha,authored=True))
    return recipes,request,request_sha


def qualified_fixture_bytes(items):
    prepared=dict(groups={x['unit']['recipe_index']:x['roots'] for x in items},
        frames={x['unit']['recipe_index']:dict(verification=x['views'][0]['source_frame_verification']) for x in items},singleton_index={})
    rows=[]
    for item in items:
        for view in item['views']:
            rows.append(view)
            if view['event']=='SINGLE_ROOT_METADATA_CONTRACT':
                prepared['singleton_index'][view['requested_roots'][0]['original_address']]=dict(contract_record_ordinal=len(rows),
                    generated_record_sha256=observer.digest(view),new_metadata_contract_sha256=view['contract_sha256'],
                    source_frame_verification=view['source_frame_verification'])
    raw=b''.join(observer.canonical(row)+b'\n' for row in rows)
    return prepared,rows,raw,gzip.compress(raw,mtime=0)


class IndependentRecipeIntegrationTests(unittest.TestCase):
    def test_real_authored_field_observation_preserves_qualified_contract_and_parses_once(self):
        args=small_fixture(field=True);before=observer.digest(args[4]);parse=observer.coff.parse
        with patch.object(observer.coff,'parse',wraps=parse) as parser:
            records=list(observer.observe_recipe_contracts(*args))
        self.assertEqual(parser.call_count,1);self.assertEqual(len(records),len(args[3])+1)
        self.assertEqual(observer.digest(args[4]),before)
        for record,view in zip(records,args[4]):
            self.assertTrue(record['native_parse_performed']);self.assertTrue(record['fresh_certificate_created'])
            self.assertTrue(record['qualified_contract_unchanged']);self.assertEqual(record['contract_identity_sha256'],view['contract_sha256'])
            self.assertEqual(observer.canonical(record['contract']),observer.canonical(view['contract']))
            self.assertEqual(record['certificate_sha256'],observer.digest(record['certificate']))
            self.assertTrue(all(record[k] is False for k in observer.FALSE))

    def test_whole180_77_257_stream_uses_one_parse_per_recipe_and_distinct_union_outcomes(self):
        items,request,request_sha=whole_authored_fixture();parse=observer.coff.parse;events=[];single_positive=0;union_positive=0
        self.assertEqual(len(request['roots']),180);self.assertEqual(len(items),77)
        with patch.object(observer.coff,'parse',wraps=parse) as parser:
            for item in items:
                original=observer.digest(item['views'])
                records=observer.observe_recipe_contracts(item['raw'],item['unit'],item['proof'],item['roots'],iter(item['views']),item['observation_provenance'])
                count=0
                for record in records:
                    count+=1;events.append(record['event'])
                    self.assertEqual(record['observation_provenance']['qualified_request_sha256'],request_sha)
                    self.assertTrue(record['fresh_certificate_created']);self.assertTrue(all(record[k] is False for k in observer.FALSE))
                    if record['event']=='SINGLE_ROOT_OBSERVATION':single_positive+=record['closure_observed']
                    else:union_positive+=record['closure_observed']
                self.assertEqual(count,len(item['roots'])+1);self.assertEqual(observer.digest(item['views']),original)
        self.assertEqual(parser.call_count,77);self.assertEqual(len(events),257)
        self.assertEqual(events.count('SINGLE_ROOT_OBSERVATION'),180);self.assertEqual(events.count('RECIPE_ROOT_UNION_OBSERVATION'),77)
        self.assertEqual((single_positive,union_positive),(178,75))


class IndependentQualifiedStreamTests(unittest.TestCase):
    def consume(self,compressed,prepared,request_sha,*,expected=None,size=None):
        source=observer.DigestingSource(io.BytesIO(compressed));identities=[]
        with gzip.GzipFile(fileobj=source,mode='rb') as stream:
            reader=observer.QualifiedReader(stream,prepared,request_sha)
            for i in sorted(prepared['groups']):
                for ordinal,row in reader.take(i):identities.append([ordinal,observer.digest(row)])
            result=reader.finish()
        source.finish(expected or hashlib.sha256(compressed).hexdigest(),len(compressed) if size is None else size)
        return result,identities,source

    def test_all257_qualified_records_have_exact_ordinal_semantics_and_compressed_identity(self):
        items,_,request_sha=whole_authored_fixture();prepared,rows,_,compressed=qualified_fixture_bytes(items)
        result,identities,source=self.consume(compressed,prepared,request_sha)
        self.assertEqual((result['records'],result['singletons'],result['unions']),(257,180,77))
        self.assertEqual(identities,[[i,observer.digest(row)] for i,row in enumerate(rows,1)])
        expected=hashlib.sha256(b''.join(observer.canonical(x) for x in identities)).hexdigest()
        self.assertEqual(result['row_sequence_sha256'],expected)
        self.assertEqual(source.bytes,len(compressed));self.assertEqual(source.hash.hexdigest(),hashlib.sha256(compressed).hexdigest())

    def test_semantically_identical_but_different_consumed_compressed_bytes_fail_hash(self):
        items,_,request_sha=whole_authored_fixture();prepared,_,raw,compressed=qualified_fixture_bytes(items)
        other=gzip.compress(raw,mtime=1);self.assertNotEqual(other,compressed)
        with self.assertRaises(ValueError):self.consume(other,prepared,request_sha,expected=hashlib.sha256(compressed).hexdigest())
        with self.assertRaises(ValueError):self.consume(compressed,prepared,request_sha,size=len(compressed)+1)

    def test_partial_extra_and_out_of_order_recipe_streams_are_fatal(self):
        items,_,request_sha=whole_authored_fixture();prepared,rows,_,_=qualified_fixture_bytes(items)
        for mode in ('missing_union','extra_record','wrong_recipe_order'):
            changed=copy.deepcopy(rows)
            if mode=='missing_union':changed.pop()
            elif mode=='extra_record':changed.append(copy.deepcopy(changed[-1]))
            else:changed[0],changed[-1]=changed[-1],changed[0]
            compressed=gzip.compress(b''.join(observer.canonical(row)+b'\n' for row in changed),mtime=0)
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.consume(compressed,prepared,request_sha)

    def test_digest_source_rejects_unbounded_read_and_trailing_unconsumed_bytes(self):
        source=observer.DigestingSource(io.BytesIO(b'authored bytes'))
        with self.assertRaises(ValueError):source.read()
        source.read(2)
        with self.assertRaises(ValueError):source.finish(hashlib.sha256(b'au').hexdigest(),2)


class IndependentFullRunTests(unittest.TestCase):
    def setup_context(self,directory):
        root=Path(directory);area=root/'build/rebuild/authored';area.mkdir(parents=True)
        items,request,request_sha=whole_authored_fixture();prepared,rows,raw,compressed=qualified_fixture_bytes(items)
        def save(name,value):
            path=area/name;path.write_bytes(observer.canonical(value)+b'\n')
            return dict(path=path.relative_to(root).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        for item in items:
            unit=item['unit'];source=root/unit['source'];source.parent.mkdir(parents=True,exist_ok=True);source.write_bytes(item['source_bytes'])
            (area/unit['object']).write_bytes(item['raw'])
        manifest=dict(units=[item['unit'] for item in items]);manifest_ref=save('manifest.json',manifest)
        request_ref=save('qualified-request.json',request);self.assertEqual(request_ref['sha256'],request_sha)
        qualified=area/'qualified.jsonl.gz';qualified.write_bytes(compressed)
        qualified_ref=dict(path=qualified.relative_to(root).as_posix(),sha256=hashlib.sha256(compressed).hexdigest())
        operation=dict(epoch='AUTHORED-ONLY-whole180',source_sha256=hashlib.sha256(Path(observer.__file__).read_bytes()).hexdigest(),
            artifacts=dict(qualified_request=request_ref,qualified_records=qualified_ref,manifest=manifest_ref))
        op=save('operation.json',operation)
        prepared.update(units={x['unit']['recipe_index']:x['unit'] for x in items},proofs={x['unit']['recipe_index']:x['proof'] for x in items},
            loaded=dict(manifest=manifest),paths=dict(manifest=area/'manifest.json',qualified_records=qualified))
        args=SimpleNamespace(operation=root/op['path'],operation_sha256=op['sha256'],out=root/'build/rebuild/output.json',details=root/'build/rebuild/output.jsonl.gz')
        return root,args,prepared,operation,items,rows,raw

    def run_authored(self,context,*,drift=None,close_failure=False):
        root,args,prepared,operation,items,rows,raw=context;original_open=Path.open
        def admit(operation,observations,started=None):
            # Explicitly stub only production operation/receipt/currentV12/global
            # metadata admission. All source/object/hash/parser/reader/4bf/EOF/
            # journal/publisher logic below executes against authored files.
            for name,ref in operation['artifacts'].items():
                path=(root/ref['path']).resolve()
                if name=='qualified_records':observations[path]=ref['sha256']
                else:observer.finite.pin(path,ref['sha256'],observations)
            return prepared
        class Journal:
            def __init__(self,wrapped):self.wrapped=wrapped
            def __getattr__(self,name):return getattr(self.wrapped,name)
            def __enter__(self):return self
            def close(self):
                if not self.wrapped.closed:
                    self.wrapped.close()
                    raise OSError('authored durable journal close failure')
            def __exit__(self,*args):self.close()
        def opened(path,*a,**kw):
            value=original_open(path,*a,**kw)
            if close_failure and path==Path(str(args.out)+'.progress.jsonl'):return Journal(value)
            return value
        stable=observer.finite.stable;changed=[]
        def stability(observations):
            if drift and not changed and args.out.exists() and args.details.exists():
                changed.append(True)
                if drift=='details':args.details.write_bytes(b'changed detail after first checksum')
                elif drift=='summary':args.out.write_bytes(b'{"runtime_eligible":true}\n')
                elif drift=='source':(root/items[0]['unit']['source']).write_bytes(b'changed protected authored source')
                elif drift=='foreign':
                    args.out.rename(args.out.with_name('displaced-owned-output.json'))
                    args.out.write_bytes(b'foreign replacement must survive')
            return stable(observations)
        with ExitStack() as stack:
            stack.enter_context(patch.object(observer,'ROOT',root))
            stack.enter_context(patch.object(observer,'validate_operation',return_value=operation))
            stack.enter_context(patch.object(observer,'prepare_operation',side_effect=admit))
            stack.enter_context(patch.object(Path,'open',opened))
            stack.enter_context(patch.object(observer.finite,'stable',side_effect=stability))
            return observer.run(args)

    def test_whole180_real_first_recipe_through_closed_journal_and_both_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            ctx=self.setup_context(td);parse=observer.coff.parse
            with patch.object(observer.coff,'parse',wraps=parse) as parser:result=self.run_authored(ctx)
            self.assertEqual(parser.call_count,77);self.assertEqual(result['native_object_observation_reads'],77)
            self.assertEqual(result['summary'],dict(roots=180,recipes=77,records=257,singleton_closure=178,singleton_blocked=2,union_closure=75,union_blocked=2))
            self.assertEqual(json.loads(ctx[1].out.read_bytes()),result)
            self.assertEqual(hashlib.sha256(ctx[1].details.read_bytes()).hexdigest(),result['details_sha256'])
            with gzip.open(ctx[1].details,'rt') as stream:records=[json.loads(line) for line in stream]
            self.assertEqual(len(records),257)
            for ordinal,(record,qualified) in enumerate(zip(records,ctx[5]),1):
                self.assertEqual(record['qualified_record_ordinal'],ordinal)
                self.assertEqual(observer.canonical(record['contract']),observer.canonical(qualified['contract']))
                self.assertEqual(record['qualified_metadata_row_sha256'],observer.digest(qualified))
            events=[json.loads(line) for line in Path(str(ctx[1].out)+'.progress.jsonl').read_text().splitlines()]
            self.assertEqual(events[0]['state'],'started');self.assertEqual(events[-1]['state'],'complete')
            self.assertEqual(sum(e['state']=='read_named_recipe_once' for e in events),77)
            self.assertTrue(result['additional_source_and_object_stability_rehash_reads'])
            checked={entry['path']:entry['sha256'] for entry in result['observed_input_bindings']}
            self.assertEqual(len(checked),len(result['observed_input_bindings']))
            for item in ctx[4]:
                unit=item['unit']
                self.assertEqual(checked[unit['source']],unit['source_sha256'])
                obj=ctx[2]['paths']['manifest'].parent/unit['object']
                self.assertEqual(checked[obj.relative_to(ctx[0]).as_posix()],unit['object_sha256'])
            self.assertEqual(sum(path.endswith('.obj') for path in checked),77)
            self.assertEqual(sum(path.endswith('.cpp') for path in checked),77)
            self.assertEqual((result['cache_frame_reads'],result['historical_roots_reobserved']),(0,0))
            self.assertTrue(all(result[k] is False for k in observer.FALSE))

    def test_stale_named_source_or_object_aborts_before_first_native_parse(self):
        for mode in ('source','object'):
            with tempfile.TemporaryDirectory() as td:
                ctx=self.setup_context(td);unit=ctx[4][0]['unit']
                path=ctx[0]/unit['source'] if mode=='source' else ctx[2]['paths']['manifest'].parent/unit['object']
                path.write_bytes(b'authored stale bytes')
                with patch.object(observer.coff,'parse',wraps=observer.coff.parse) as parser:
                    with self.subTest(mode=mode),self.assertRaises(ValueError):self.run_authored(ctx)
                    self.assertEqual(parser.call_count,0)
                self.assertFalse(ctx[1].out.exists());self.assertFalse(ctx[1].details.exists())

    def test_consumed_compressed_hash_failure_after_full_stream_cannot_publish(self):
        with tempfile.TemporaryDirectory() as td:
            ctx=self.setup_context(td);ctx[2]['paths']['qualified_records'].write_bytes(gzip.compress(ctx[6],mtime=1))
            with self.assertRaises(ValueError):self.run_authored(ctx)
            self.assertFalse(ctx[1].out.exists());self.assertFalse(ctx[1].details.exists())
            states=[json.loads(line)['state'] for line in Path(str(ctx[1].out)+'.progress.jsonl').read_text().splitlines()]
            self.assertEqual(states[-1],'failed');self.assertEqual(states.count('read_named_recipe_once'),77)

    def test_late_missing_union_cannot_publish_earlier_successful_records(self):
        with tempfile.TemporaryDirectory() as td:
            ctx=self.setup_context(td);raw=b''.join(observer.canonical(x)+b'\n' for x in ctx[5][:-1])
            ctx[2]['paths']['qualified_records'].write_bytes(gzip.compress(raw,mtime=0))
            with self.assertRaises(ValueError):self.run_authored(ctx)
            self.assertFalse(ctx[1].out.exists());self.assertFalse(ctx[1].details.exists())

    def test_postwrite_detail_summary_and_protected_source_drift_retract_both_outputs(self):
        for kind in ('details','summary','source'):
            with tempfile.TemporaryDirectory() as td:
                ctx=self.setup_context(td)
                with self.subTest(kind=kind),self.assertRaises(ValueError):self.run_authored(ctx,drift=kind)
                self.assertFalse(ctx[1].out.exists());self.assertFalse(ctx[1].details.exists())

    def test_failure_retraction_preserves_foreign_replacement(self):
        with tempfile.TemporaryDirectory() as td:
            ctx=self.setup_context(td)
            with self.assertRaises(ValueError):self.run_authored(ctx,drift='foreign')
            self.assertEqual(ctx[1].out.read_bytes(),b'foreign replacement must survive');self.assertFalse(ctx[1].details.exists())

    def test_durable_journal_close_failure_leaves_no_success_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            ctx=self.setup_context(td)
            with self.assertRaisesRegex(OSError,'journal close'):self.run_authored(ctx,close_failure=True)
            self.assertFalse(ctx[1].out.exists());self.assertFalse(ctx[1].details.exists())

    def test_public_output_paths_refused_before_native_read_or_publication(self):
        with tempfile.TemporaryDirectory() as td:
            ctx=self.setup_context(td);ctx[1].out=ctx[0]/'public.json';ctx[1].details=ctx[0]/'public.jsonl.gz'
            with patch.object(observer.coff,'parse',wraps=observer.coff.parse) as parser:
                with self.assertRaises(ValueError):self.run_authored(ctx)
                self.assertEqual(parser.call_count,0)
            self.assertFalse(ctx[1].out.exists());self.assertFalse(ctx[1].details.exists())


if __name__=='__main__':unittest.main()
