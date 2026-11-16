"""Authored static-reference fixtures; no private metadata or binary inputs."""
import copy
import gzip
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import static_reference_graph as graph


def identity(index):return dict(recipe_id='authored-%02d'%index,object_sha256=('%064x'%index),symbol_index=index)
def va(index):return '0x%08x'%(0x10000000+index*0x1000)
def provider_map(count=6):
    providers={}
    for index in range(1,count+1):
        item=identity(index)
        providers[va(index)]=dict(**item,source_sha256='a'*64,section=index,value=0,size=128,
            symbol='authored_function_%d'%index,planned_canonical_name='_fnv_code_'+graph.digest(item))
    return dict(schema_version=1,policy_id='selected-physical-provider-map-v1',kind='typed-provider-map',
        providers=providers,census=dict(selected_owners=count),provider_identity_is_planned_namespace=True,
        materialized_exports=0,**{flag:False for flag in graph.MAP_FALSE})
def field(source,target,offset=4):
    return dict(event='SELECTED_FUNCTION_COFF_RELOCATION',recipe_id=identity(source)['recipe_id'],
        recipe_index=source,function_va=va(source),function_symbol='authored_function_%d'%source,
        source_field_offset=offset,physical_section=source,physical_offset=offset,
        original_field_va='0x%08x'%(int(va(source),16)+offset),
        coff_relocation=dict(symbol_index=target,kind=20,offset=offset,width=4,addend=0,
            symbol='authored_target_%d'%target,symbol_section=0,symbol_value=0),
        classification='SELECTED_CODE_ENTRY',proof_consistency='EXACT_OWN_SOURCE_RESOLUTION',
        selected_address=va(target),exact_original_target_va=va(target),
        derived_source_symbol_base_va=va(target),expected_original_target_va=va(target),
        code_owners=[dict(address=va(target),offset=0)],code_ownership_ambiguous=False,
        physical_field_overlap_count=1,runtime_eligible=False,provider_selected=False,
        game_fixup_approved=False,original_operand='PRIVATE_OPERAND_SENTINEL')
def missing(source,offset=24):
    row=field(source,1,offset)
    row.update(event='MISSING_ORIGINAL_HIGHLOW_SOURCE_MIGRATION_BLOCKER',coff_relocation=None,
        classification='MISSING_SOURCE_RELOCATION_NO_SYNTHESIS')
    row.pop('proof_consistency')
    return row
def summary(rows,count=6):
    from collections import Counter
    return dict(schema_version=1,kind='fnv-runtime-binding-observations',status='analysis-only',
        detail_format='gzip-jsonl-complete-selected-field-and-migration-records',
        implementation_sha256='b'*64,details_sha256='',
        summary=dict(selected_functions=count,events=dict(Counter(r['event'] for r in rows)),
            target_classes=dict(Counter(r['classification'] for r in rows)),
            proof_consistency=dict(Counter(r['proof_consistency'] for r in rows if r['event']=='SELECTED_FUNCTION_COFF_RELOCATION')),
            relocation_kinds=dict(Counter(str(r['coff_relocation']['kind']) for r in rows if r['event']=='SELECTED_FUNCTION_COFF_RELOCATION'))),
        runtime_eligible=False,provider_selected=False,runtime_closure_verified=False,link_ready=False)


class StaticReferenceCoreTests(unittest.TestCase):
    def test_cycle_and_seed_closure_are_only_known_static_lower_bounds(self):
        index=graph.ReferenceIndex(provider_map());rows=[field(1,2),field(2,1,8),field(2,3,12)]
        data=field(2,4,16);data['classification']='ORIGINAL_IMAGE_DATA_REQUIRES_CANONICAL_OWNER';rows+=[data,missing(6)]
        outputs=[index.consume(row,i) for i,row in enumerate(rows,1)]
        index.validate_census(summary(rows))
        report=index.report([identity(1)])
        self.assertEqual(report['seed_known_node_lower_bound'],3)
        self.assertEqual(report['seed_known_subgraph_groups'],dict(groups=2,multi_node_groups=1,largest_group=2,condensation_edges=1))
        self.assertEqual(report['known_unique_static_edges'],3)
        self.assertEqual(report['nodes_without_field_rows'],3)
        self.assertEqual(report['seed_frontier_unknown_fields'],{'CLASS_ORIGINAL_IMAGE_DATA_REQUIRES_CANONICAL_OWNER':1})
        self.assertFalse(report['execution_reachability_proven']);self.assertFalse(report['playable_ETA_derivable'])
        self.assertNotIn('PRIVATE_OPERAND_SENTINEL',json.dumps(outputs))
        self.assertNotIn('original_operand',json.dumps(outputs))
        self.assertNotIn('addend',json.dumps(outputs))

    def test_no_field_rows_remain_unknown_not_proven_leaves(self):
        index=graph.ReferenceIndex(provider_map())
        self.assertTrue(all(n['outgoing_reference_coverage']=='UNKNOWN_NO_FIELD_ROWS' for n in index.node_rows()))
        self.assertIn('indirect_calls',index.report([])['global_unknown_mechanisms'])

    def test_admissibility_guards_never_infer_code_edges(self):
        def cradd(row):row['coff_relocation']['addend']=1
        def iat(row):row['coff_relocation']['symbol']='_imp__authored'
        mutations=[lambda r:r.update(code_ownership_ambiguous=True),
            lambda r:r.update(code_owners=[dict(address=va(2),offset=1)]),
            lambda r:r.update(code_owners=[dict(address=va(2),offset=0),dict(address=va(3),offset=0)]),
            lambda r:r.update(proof_consistency='ORIGINAL_ORACLE_LITERAL_POOL_TOLERANCE_ADDRESS_NOT_MERGED'),
            lambda r:r.update(physical_field_overlap_count=2),cradd,iat,
            lambda r:r.update(import_pointer_source_conflict=True),
            lambda r:r.update(source_absolute_symbol_migration_blocker=True),
            lambda r:r.update(expected_original_target_va=va(3))]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                row=field(1,2);mutate(row);index=graph.ReferenceIndex(provider_map())
                self.assertEqual(index.consume(row,1)['status'],'UNKNOWN')
                self.assertFalse(index.adjacency)

    def test_source_geometry_must_match_selected_native_extent(self):
        for mutate in (lambda r:r.update(physical_offset=8),lambda r:r.update(source_field_offset=-1),
                       lambda r:r.update(source_field_offset=128),lambda r:r.update(original_field_va=va(3)),
                       lambda r:r['coff_relocation'].update(width=2)):
            row=field(1,2);mutate(row)
            self.assertEqual(graph.ReferenceIndex(provider_map()).consume(row,1)['unknown_reason'],'SOURCE_FIELD_GEOMETRY_NOT_EXACT')

    def test_selected_target_absent_from_map_is_unknown(self):
        self.assertEqual(graph.ReferenceIndex(provider_map()).consume(field(1,99),1)['unknown_reason'],'SELECTED_TARGET_ABSENT_FROM_MAP')

    def test_source_name_disagreement_is_not_an_alias(self):
        row=field(1,2);row['function_symbol']='same_address_different_name'
        self.assertIsNone(graph.ReferenceIndex(provider_map()).consume(row,1)['source_node'])

    def test_special_target_classes_stay_unknown(self):
        for classification in ('UNIQUE_CODE_INTERIOR_OR_LOCAL_LABEL_NOT_CALLABLE_APPROVAL','AMBIGUOUS_CODE_INTERIOR',
            'UNSELECTED_EXECUTABLE_TARGET_UNCLASSIFIED','COMPILER_LITERAL_FULL_READONLY_NONPOINTER_EQUALITY',
            'IAT_POINTER_CELL_NOT_FUNCTION_BODY','STATIC_TLS_INDEX_REQUIRES_CANONICAL_OWNER',
            'EXPLICIT_NORMAL_CRT_CONTRACT_CANDIDATE','COMPILER_LOCAL_EH_METADATA_OR_HELPER_CANDIDATE'):
            row=field(1,2);row['classification']=classification
            self.assertEqual(graph.ReferenceIndex(provider_map()).consume(row,1)['status'],'UNKNOWN')

    def test_missing_migration_is_not_a_field_or_execution_edge(self):
        index=graph.ReferenceIndex(provider_map());row=missing(1)
        self.assertEqual(index.consume(row,1)['unknown_reason'],'MISSING_OR_UNSUPPORTED_FIELD_EVENT')
        index.validate_census(summary([row]));self.assertFalse(index.adjacency)

    def test_promoted_or_unknown_schemas_reject(self):
        row=field(1,2);row['runtime_eligible']=True
        with self.assertRaisesRegex(ValueError,'PROMOTED'):graph.ReferenceIndex(provider_map()).consume(row,1)
        row=field(1,2);row['event']='FUTURE_DYNAMIC_RECORD'
        with self.assertRaisesRegex(ValueError,'UNKNOWN_FIELD_EVENT'):graph.ReferenceIndex(provider_map()).consume(row,1)
        row=field(1,2);row['proof_consistency']={'private':'arbitrary value'}
        with self.assertRaisesRegex(ValueError,'UNKNOWN_PROOF'):graph.ReferenceIndex(provider_map()).consume(row,1)
        row=field(1,2);row['classification']='arbitrary untyped value'
        with self.assertRaisesRegex(ValueError,'UNKNOWN_FIELD_CLASSIFICATION'):graph.ReferenceIndex(provider_map()).consume(row,1)

    def test_duplicate_exact_physical_field_rejects(self):
        index=graph.ReferenceIndex(provider_map());index.consume(field(1,2),1)
        with self.assertRaisesRegex(ValueError,'DUPLICATE_ADMISSIBLE'):index.consume(field(1,2),2)

    def test_stale_planned_name_or_duplicate_physical_identity_rejects(self):
        providers=provider_map();providers['providers'][va(1)]['planned_canonical_name']='invented'
        with self.assertRaisesRegex(ValueError,'PLANNED_NAME'):graph.ReferenceIndex(providers)
        providers=provider_map();providers['providers'][va(2)]=copy.deepcopy(providers['providers'][va(1)])
        with self.assertRaisesRegex(ValueError,'DUPLICATE_PHYSICAL'):graph.ReferenceIndex(providers)

    def test_census_and_unknown_seed_are_explicit(self):
        index=graph.ReferenceIndex(provider_map());row=field(1,2);index.consume(row,1)
        changed=summary([row]);changed['summary']['target_classes']={}
        with self.assertRaisesRegex(ValueError,'CENSUS_MISMATCH'):index.validate_census(changed)
        self.assertEqual(index.report([identity(99)])['unknown_seed_identities'],[identity(99)])

    def test_seed_values_and_duplicate_seeds_cannot_escape_whitelist(self):
        for key,value in (('recipe_id',{'arbitrary':'payload'}),('object_sha256','PRIVATE_VALUE'),
                          ('symbol_index',True),('symbol_index',2**32)):
            seed=identity(99);seed[key]=value
            with self.assertRaises(ValueError):graph.ReferenceIndex(provider_map()).report([seed])
        with self.assertRaisesRegex(ValueError,'DUPLICATE_SEED'):
            graph.ReferenceIndex(provider_map()).report([identity(1),identity(1)])

    def test_every_provider_map_promotion_flag_is_required_false(self):
        for flag in graph.MAP_FALSE:
            with self.subTest(flag=flag):
                item=provider_map();item[flag]=True
                with self.assertRaisesRegex(ValueError,'PROMOTED_PROVIDER_MAP'):graph.ReferenceIndex(item)
                item=provider_map();item.pop(flag)
                with self.assertRaisesRegex(ValueError,'PROMOTED_PROVIDER_MAP'):graph.ReferenceIndex(item)

    def test_duplicate_json_fields_cannot_hide_an_identity(self):
        with self.assertRaisesRegex(ValueError,'DUPLICATE_JSON_KEY'):
            graph.strict_json(b'{"source":{"symbol_index":1,"symbol_index":2}}')

    def test_hashing_reader_consumes_compressed_input_once(self):
        data=gzip.compress(b'{"authored":true}\n',mtime=0)
        reader=graph.HashingReader(io.BytesIO(data))
        with gzip.GzipFile(fileobj=reader) as stream:self.assertEqual(stream.readline(),b'{"authored":true}\n');self.assertEqual(stream.readline(),b'')
        while reader.read(1024):pass
        self.assertEqual(reader.bytes,len(data));self.assertEqual(reader.hasher.hexdigest(),graph.sha_bytes(data))
        with self.assertRaisesRegex(ValueError,'UNBOUNDED'):reader.read()


class StaticReferencePublicationTests(unittest.TestCase):
    def fixture(self,root,rows=None):
        rows=rows or [field(1,2),field(2,1,8),missing(6)]
        private=root/'build/rebuild';private.mkdir(parents=True)
        tool=root/'tools/rebuild/static_reference_graph.py';tool.parent.mkdir(parents=True)
        tool.write_bytes(Path(graph.__file__).read_bytes())
        p=private/'map.json';p.write_bytes(graph.canonical(provider_map()))
        d=private/'fields.jsonl.gz';d.write_bytes(gzip.compress(b''.join(graph.canonical(r)+b'\n' for r in rows),mtime=0))
        s=private/'summary.json';report=summary(rows);report['details_sha256']=graph.file_hash(d);s.write_bytes(graph.canonical(report))
        manifest=dict(schema_version=1,policy_id=graph.POLICY,inputs={
            'provider_map':dict(path=str(p),sha256=graph.file_hash(p),max_bytes=1024*1024),
            'binding_summary':dict(path=str(s),sha256=graph.file_hash(s),max_bytes=1024*1024),
            'binding_fields':dict(path=str(d),sha256=graph.file_hash(d),max_bytes=1024*1024,format='gzip-jsonl')},
            tools_sha256={'tools/rebuild/static_reference_graph.py':graph.file_hash(tool)},
            out_dir=str(private/'output'),seeds=[identity(1)],seed_scope='STATIC_DIAGNOSTIC_IDENTITY_ONLY_NOT_GAME_REACHABILITY',
            bounds=dict(seconds=900,peak_bytes=1024**3,output_bytes=128*1024**2,max_nodes=100000,max_rows=2000000,max_known_fields=2000000,max_line_bytes=262144,max_uncompressed_bytes=2*1024**3))
        m=private/'request.json';m.write_bytes(graph.canonical(manifest));return m,manifest

    def test_finite_single_pass_publishes_whitelisted_metadata(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(graph,'ROOT',Path(tmp)):
            root=Path(tmp);m,manifest=self.fixture(root);result=graph.run(m,graph.file_hash(m))
            self.assertEqual(result['stream_read_passes'],1);self.assertTrue(result['stream_sha256_verified_at_EOF'])
            self.assertEqual(result['known_unique_static_edges'],2)
            output=Path(manifest['out_dir']);self.assertTrue((output/'manifest.json').exists())
            rows=gzip.decompress((output/'references.jsonl.gz').read_bytes())
            self.assertNotIn(b'PRIVATE_OPERAND_SENTINEL',rows);self.assertNotIn(b'original_operand',rows)

    def test_bad_stream_hash_removes_success_outputs(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(graph,'ROOT',Path(tmp)):
            m,manifest=self.fixture(Path(tmp));manifest['inputs']['binding_fields']['sha256']='f'*64
            summarypath=Path(manifest['inputs']['binding_summary']['path']);s=json.loads(summarypath.read_bytes());s['details_sha256']='f'*64;summarypath.write_bytes(graph.canonical(s))
            manifest['inputs']['binding_summary']['sha256']=graph.file_hash(summarypath);m.write_bytes(graph.canonical(manifest))
            with self.assertRaisesRegex(ValueError,'STREAM_HASH'):graph.run(m,graph.file_hash(m))
            out=Path(manifest['out_dir']);self.assertFalse((out/'manifest.json').exists());self.assertFalse((out/'references.jsonl.gz').exists())
            self.assertIn('failed',(out/'progress.jsonl').read_text())

    def test_row_bound_violation_retains_no_success(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(graph,'ROOT',Path(tmp)):
            row=field(1,2);row['unconsumed_private_payload']='x'*262145
            m,manifest=self.fixture(Path(tmp),[row])
            with self.assertRaisesRegex(ValueError,'STREAM_ROW'):graph.run(m,graph.file_hash(m))
            self.assertFalse((Path(manifest['out_dir'])/'manifest.json').exists())

    def test_late_input_stat_drift_cleans_success_outputs(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(graph,'ROOT',Path(tmp)):
            m,manifest=self.fixture(Path(tmp));original=graph.ReferenceIndex.consume
            def mutate(index,row,ordinal):
                result=original(index,row,ordinal)
                if ordinal==2:
                    p=Path(manifest['inputs']['provider_map']['path']);p.write_bytes(p.read_bytes()+b' ')
                return result
            with patch.object(graph.ReferenceIndex,'consume',mutate):
                with self.assertRaisesRegex(ValueError,'LATE_INPUT_STAT'):graph.run(m,graph.file_hash(m))
            self.assertFalse((Path(manifest['out_dir'])/'nodes.jsonl.gz').exists())

    def test_census_mismatch_cleans_outputs(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(graph,'ROOT',Path(tmp)):
            m,manifest=self.fixture(Path(tmp));s=Path(manifest['inputs']['binding_summary']['path']);v=json.loads(s.read_bytes());v['summary']['events']={};s.write_bytes(graph.canonical(v))
            manifest['inputs']['binding_summary']['sha256']=graph.file_hash(s);m.write_bytes(graph.canonical(manifest))
            with self.assertRaisesRegex(ValueError,'CENSUS_MISMATCH'):graph.run(m,graph.file_hash(m))
            self.assertFalse((Path(manifest['out_dir'])/'manifest.json').exists())

    def test_existing_output_is_not_mutated(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(graph,'ROOT',Path(tmp)):
            m,manifest=self.fixture(Path(tmp));out=Path(manifest['out_dir']);out.mkdir();sentinel=out/'sentinel';sentinel.write_text('owned elsewhere')
            with self.assertRaisesRegex(ValueError,'OUTPUT_MUST_BE_NEW'):graph.run(m,graph.file_hash(m))
            self.assertEqual(sentinel.read_text(),'owned elsewhere')


if __name__=='__main__':unittest.main()
