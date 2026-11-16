"""Conservative saved-metadata reference index; no binary, source or service API.

Selected CODE references describe static field identities, never execution,
callability, materialized providers or complete reachability. Missing adjacency
is unknown. The only production reader is an exact manifest-bound single pass.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict, deque
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import time

POLICY='saved-static-reference-index-v1'
ROOT=Path(__file__).resolve().parents[2]
FALSE=dict(provider_selected=False,alias_selected=False,MATCH_established=False,
           runtime_eligible=False,execution_reachability_proven=False)
BLIND_SPOTS=['indirect_calls','vtable_dispatch','dynamic_loading','callbacks',
             'initializer_execution','DATA_ownership_and_pointer_graphs',
             'unselected_or_ambiguous_CODE','missing_or_unrepresented_fields']
MAP_FALSE=('provider_selected','runtime_eligible','ABI_verified','namespace_approved',
           'full_serialization_eligible','emission_performed','materialization_approved',
           'link_ready','native_tools_run')
CLASSIFICATIONS={
    'UNSUPPORTED_OR_UNMAPPED','IAT_POINTER_CELL_NOT_FUNCTION_BODY','SELECTED_CODE_ENTRY',
    'UNIQUE_CODE_INTERIOR_OR_LOCAL_LABEL_NOT_CALLABLE_APPROVAL','AMBIGUOUS_CODE_INTERIOR',
    'STATIC_TLS_INDEX_REQUIRES_CANONICAL_OWNER','STATIC_TLS_TEMPLATE_REQUIRES_CANONICAL_OWNER',
    'COMPILER_LITERAL_FULL_READONLY_NONPOINTER_EQUALITY','EXPLICIT_NORMAL_CRT_CONTRACT_CANDIDATE',
    'COMPILER_LOCAL_EH_METADATA_OR_HELPER_CANDIDATE','ORIGINAL_IMAGE_DATA_REQUIRES_CANONICAL_OWNER',
    'UNSELECTED_EXECUTABLE_TARGET_UNCLASSIFIED','UNSUPPORTED_PADDING_OR_STRADDLING_FIELD',
    'IMAGE_RELATIVE_RVA_REQUIRES_OWNER','STATIC_TLS_SECREL_REQUIRES_OWNER',
    'SECTION_INDEX_REQUIRES_OWNER','COMPILER_TLS_ARRAY_OFFSET_CANDIDATE_NOT_PROCESS_VA',
    'AMBIGUOUS_PHYSICAL_RELOCATION_FIELD','MISSING_SOURCE_RELOCATION_NO_SYNTHESIS'}
PROOF_CLASSES={'NO_CONTAINED_FIELD','SPECIAL_OR_UNSUPPORTED_SEMANTICS','EXACT_OWN_SOURCE_RESOLUTION',
    'ORIGINAL_ORACLE_LITERAL_POOL_TOLERANCE_ADDRESS_NOT_MERGED','IMAGE_RELATIVE_PROJECTION_ONLY',
    'STATIC_TLS_OFFSET_PROJECTION_ONLY'}

def require(condition, message):
    if not condition: raise ValueError(message)

def canonical(value): return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def digest(value): return hashlib.sha256(canonical(value)).hexdigest()
def sha_bytes(value): return hashlib.sha256(value).hexdigest()
def address(value):
    require(isinstance(value,str) and len(value)==10 and value.startswith('0x'),'INVALID_ADDRESS_IDENTITY')
    number=int(value[2:],16); require(0<=number<=0xffffffff,'INVALID_ADDRESS_IDENTITY')
    return '0x%08x'%number
def integer(value): require(type(value) is int and 0<=value<=0xffffffff,'INVALID_PHYSICAL_INTEGER'); return value
def text(value, limit=4096):
    require(isinstance(value,str) and 0<len(value)<=limit and '\x00' not in value,'INVALID_METADATA_NAME')
    return value
def hash_text(value):
    require(isinstance(value,str) and len(value)==64 and all(c in '0123456789abcdef' for c in value),'INVALID_HASH')
    return value

def strict_json(data):
    def pairs(items):
        result={}
        for key,value in items:
            require(key not in result,'DUPLICATE_JSON_KEY')
            result[key]=value
        return result
    return json.loads(data,object_pairs_hook=pairs)

class ReferenceIndex:
    """Pure incremental index of one selected provider map and saved field rows."""
    def __init__(self, provider_map, *, max_nodes=100000, max_known_fields=2000000):
        require(provider_map.get('schema_version')==1 and provider_map.get('policy_id')=='selected-physical-provider-map-v1' and provider_map.get('kind')=='typed-provider-map','UNKNOWN_PROVIDER_MAP')
        require(provider_map.get('provider_identity_is_planned_namespace') is True and provider_map.get('materialized_exports')==0,'PROVIDER_MAP_IS_NOT_PLANNED_ONLY')
        for flag in MAP_FALSE:
            require(provider_map.get(flag) is False,'PROMOTED_PROVIDER_MAP')
        self.nodes={}; self.by_source=defaultdict(list); self.by_address={}
        self.adjacency=defaultdict(set); self.events=Counter();self.classes=Counter()
        self.proofs=Counter();self.kinds=Counter();self.unknown=Counter()
        self.source_unknown=Counter();self.known_fields=set();self.max_known_fields=max_known_fields
        self.rows=0
        providers=provider_map['providers']
        require(isinstance(providers,dict) and len(providers)<=max_nodes,'NODE_BOUND')
        for va,record in providers.items():
            va=address(va)
            identity=dict(recipe_id=text(record['recipe_id']),object_sha256=hash_text(record['object_sha256']),symbol_index=integer(record['symbol_index']))
            node_id=digest(identity)
            require(node_id not in self.nodes and va not in self.by_address,'DUPLICATE_PHYSICAL_OR_ADDRESS_NODE')
            require(record['planned_canonical_name']=='_fnv_code_'+node_id,'PLANNED_NAME_IDENTITY_MISMATCH')
            section=integer(record['section']);require(section>0,'INVALID_SOURCE_SECTION')
            node=dict(node_id=node_id,identity=identity,address=va,symbol=text(record['symbol']),section=section,
                      native_start=integer(record['value']),size=integer(record['size']),
                      planned_name=record['planned_canonical_name'],observed_rows=0,known_reference_fields=0,unknown_fields=Counter())
            self.nodes[node_id]=node;self.by_address[va]=node_id
            self.by_source[(identity['recipe_id'],va,node['symbol'],section)].append(node_id)
        require(provider_map['census']['selected_owners']==len(self.nodes),'MAP_CENSUS_MISMATCH')

    def consume(self,row,ordinal):
        """Return a whitelist-only output row; operands/addends never escape."""
        require(isinstance(row,dict),'FIELD_ROW_NOT_OBJECT')
        for flag in ('runtime_eligible','provider_selected','game_fixup_approved'):
            require(row.get(flag) is False,'PROMOTED_FIELD_RECORD')
        event=text(row['event'],200); classification=text(row['classification'],200)
        require(classification in CLASSIFICATIONS,'UNKNOWN_FIELD_CLASSIFICATION_SCHEMA')
        require(event in ('SELECTED_FUNCTION_COFF_RELOCATION','MISSING_ORIGINAL_HIGHLOW_SOURCE_MIGRATION_BLOCKER'),'UNKNOWN_FIELD_EVENT_SCHEMA')
        self.rows+=1;self.events[event]+=1;self.classes[classification]+=1
        proof=row.get('proof_consistency')
        cr=row.get('coff_relocation')
        if event=='SELECTED_FUNCTION_COFF_RELOCATION':
            require(isinstance(proof,str) and proof in PROOF_CLASSES,'UNKNOWN_PROOF_CONSISTENCY_SCHEMA')
            self.proofs[proof]+=1
            require(isinstance(cr,dict),'SELECTED_FIELD_MISSING_RELOCATION_SCHEMA')
            self.kinds[str(integer(cr['kind']))]+=1
        va=address(row['function_va']);rid=text(row['recipe_id']);symbol=text(row['function_symbol'])
        section=integer(row['physical_section']);offset=integer(row['physical_offset'])
        sources=self.by_source.get((rid,va,symbol,section),[])
        source=sources[0] if len(sources)==1 else None
        if source:self.nodes[source]['observed_rows']+=1
        output=dict(ordinal=ordinal,event=event,classification=classification,source_node=source,
                    source_field=dict(recipe_id=rid,function_address=va,function_symbol=symbol,
                                      section=section,offset=offset),status='UNKNOWN')
        if cr is not None:
            output['native_reference_symbol']=dict(symbol_index=integer(cr['symbol_index']),
                name=text(cr['symbol']),kind=integer(cr['kind']))
        reason=None;target=None
        if source is None:reason='SOURCE_IDENTITY_NOT_UNIQUELY_IN_SELECTED_MAP'
        elif event!='SELECTED_FUNCTION_COFF_RELOCATION':reason='MISSING_OR_UNSUPPORTED_FIELD_EVENT'
        elif cr is None:reason='MISSING_NATIVE_RELOCATION'
        elif (cr.get('offset')!=offset or cr.get('width')!=4 or
              type(row.get('source_field_offset')) is not int or
              not 0<=row['source_field_offset']<=self.nodes[source]['size']-4 or
              offset!=self.nodes[source]['native_start']+row['source_field_offset'] or
              row.get('original_field_va')!='0x%08x'%(int(va,16)+row['source_field_offset'])):
            reason='SOURCE_FIELD_GEOMETRY_NOT_EXACT'
        elif classification!='SELECTED_CODE_ENTRY':reason='CLASS_'+classification
        elif proof!='EXACT_OWN_SOURCE_RESOLUTION':reason='SOURCE_RESOLUTION_NOT_EXACT'
        elif row.get('physical_field_overlap_count')!=1:reason='AMBIGUOUS_PHYSICAL_FIELD'
        elif cr['kind'] not in (6,20) or cr.get('addend')!=0:reason='NONZERO_OR_SPECIAL_RELOCATION'
        elif row.get('code_ownership_ambiguous') is not False:reason='AMBIGUOUS_CODE_OWNER'
        else:
            selected=address(row['selected_address'])
            owners=row.get('code_owners')
            if owners!=[dict(address=selected,offset=0)]:reason='CODE_ENTRY_OWNER_NOT_UNIQUE_OFFSET_ZERO'
            elif not all(row.get(k)==selected for k in ('exact_original_target_va','derived_source_symbol_base_va','expected_original_target_va')):reason='CODE_ENTRY_IDENTITIES_DIFFER'
            elif row.get('import_pointer_source_conflict') or row.get('source_absolute_symbol_migration_blocker'):reason='SPECIAL_SOURCE_MIGRATION_CONFLICT'
            elif cr['symbol'].startswith(('__imp_','_imp__')):reason='IAT_NAME_IS_NOT_CODE_BODY'
            else:
                target=self.by_address.get(selected)
                if target is None:reason='SELECTED_TARGET_ABSENT_FROM_MAP'
        if reason is None:
            key=(source,section,offset,cr['kind'],cr['symbol_index'])
            require(key not in self.known_fields,'DUPLICATE_ADMISSIBLE_PHYSICAL_FIELD')
            require(len(self.known_fields)<self.max_known_fields,'KNOWN_FIELD_MEMORY_BOUND')
            self.known_fields.add(key);self.adjacency[source].add(target)
            self.nodes[source]['known_reference_fields']+=1
            output.update(status='KNOWN_STATIC_SELECTED_CODE_REFERENCE',target_node=target,
                          target_address=self.nodes[target]['address'],provider_selected=False,
                          execution_edge=False)
        else:
            output['unknown_reason']=reason;self.unknown[reason]+=1
            if source:self.nodes[source]['unknown_fields'][reason]+=1
            else:self.source_unknown[reason]+=1
        return output

    def validate_census(self,summary):
        require(summary.get('schema_version')==1 and summary.get('kind')=='fnv-runtime-binding-observations' and summary.get('status')=='analysis-only','UNKNOWN_BINDING_SUMMARY')
        require(summary.get('detail_format')=='gzip-jsonl-complete-selected-field-and-migration-records','UNKNOWN_DETAIL_FORMAT')
        for flag in ('runtime_eligible','provider_selected','runtime_closure_verified','link_ready'):
            require(summary.get(flag) is False,'PROMOTED_BINDING_SUMMARY')
        s=summary['summary']
        require(s['selected_functions']==len(self.nodes),'SELECTED_UNIVERSE_COUNT_MISMATCH')
        require(s['events']==dict(self.events) and s['target_classes']==dict(self.classes),'FIELD_CENSUS_MISMATCH')
        require(s['proof_consistency']==dict(self.proofs) and s['relocation_kinds']==dict(self.kinds),'FIELD_PROOF_OR_KIND_CENSUS_MISMATCH')

    def node_rows(self):
        for key,node in sorted(self.nodes.items()):
            yield dict(node_id=key,identity=node['identity'],address=node['address'],symbol=node['symbol'],
                section=node['section'],planned_name=node['planned_name'],observed_field_rows=node['observed_rows'],
                known_reference_fields=node['known_reference_fields'],unknown_field_categories=dict(node['unknown_fields']),
                outgoing_reference_coverage='PARTIAL_OBSERVED_STATIC_FIELDS' if node['observed_rows'] else 'UNKNOWN_NO_FIELD_ROWS',
                provider_selected=False,complete_execution_dependencies=False)

    def groups(self,subset):
        """Iterative SCCs of known static edges only; no recursion/closure claim."""
        visited=set();order=[]
        for root in sorted(subset):
            if root in visited:continue
            visited.add(root);stack=[(root,iter(self.adjacency.get(root,())))]
            while stack:
                node,children=stack[-1]
                child=next(children,None)
                if child is None:order.append(node);stack.pop()
                elif child in subset and child not in visited:
                    visited.add(child);stack.append((child,iter(self.adjacency.get(child,()))))
        reverse=defaultdict(list)
        for source in subset:
            for target in self.adjacency.get(source,()):
                if target in subset:reverse[target].append(source)
        assigned={};sizes=[]
        for root in reversed(order):
            if root in assigned:continue
            gid=len(sizes);assigned[root]=gid;stack=[root];size=0
            while stack:
                node=stack.pop();size+=1
                for child in reverse.get(node,()):
                    if child not in assigned:assigned[child]=gid;stack.append(child)
            sizes.append(size)
        edges={(assigned[s],assigned[t]) for s in subset for t in self.adjacency.get(s,()) if t in subset and assigned[s]!=assigned[t]}
        return dict(groups=len(sizes),multi_node_groups=sum(n>1 for n in sizes),largest_group=max(sizes,default=0),condensation_edges=len(edges))

    def report(self,seeds):
        seed_ids=[];unknown_seeds=[];seen=set()
        for seed in seeds:
            require(set(seed)=={'recipe_id','object_sha256','symbol_index'},'SEED_MUST_BE_EXACT_PHYSICAL_IDENTITY')
            seed=dict(recipe_id=text(seed['recipe_id']),object_sha256=hash_text(seed['object_sha256']),symbol_index=integer(seed['symbol_index']))
            sid=digest(seed);require(sid not in seen,'DUPLICATE_SEED_IDENTITY');seen.add(sid)
            if sid in self.nodes:seed_ids.append(sid)
            else:unknown_seeds.append(seed)
        closure=set(seed_ids);queue=deque(seed_ids)
        while queue:
            for child in self.adjacency.get(queue.popleft(),()):
                if child not in closure:closure.add(child);queue.append(child)
        frontier=Counter()
        for node in closure:frontier.update(self.nodes[node]['unknown_fields'])
        return dict(policy_id=POLICY,selected_physical_nodes=len(self.nodes),input_field_rows=self.rows,
            events=dict(self.events),classifications=dict(self.classes),unknown_field_categories=dict(self.unknown),
            known_reference_fields=len(self.known_fields),known_unique_static_edges=sum(map(len,self.adjacency.values())),
            nodes_with_observed_fields=sum(n['observed_rows']>0 for n in self.nodes.values()),
            nodes_without_field_rows=sum(n['observed_rows']==0 for n in self.nodes.values()),
            whole_known_subgraph_groups=self.groups(set(self.nodes)),seed_count=len(seeds),known_seed_count=len(seed_ids),
            unknown_seed_identities=unknown_seeds,seed_known_node_lower_bound=len(closure),
            seed_known_subgraph_groups=self.groups(closure),seed_frontier_unknown_fields=dict(frontier),
            source_unattributed_field_categories=dict(self.source_unknown),global_unknown_mechanisms=BLIND_SPOTS,
            graph_coverage='PARTIAL_SAVED_SELECTED_STATIC_RELOCATION_FIELDS',
            complete_dependency_work_remaining_known=False,playable_ETA_derivable=False,**FALSE)

class HashingReader:
    """Hash compressed bytes in their single parsing pass, never a replay."""
    def __init__(self,raw):self.raw=raw;self.hasher=hashlib.sha256();self.bytes=0
    def read(self,size=-1):
        require(size>=0,'UNBOUNDED_COMPRESSED_READ')
        data=self.raw.read(min(size,1024*1024));self.hasher.update(data);self.bytes+=len(data);return data

def peak_bytes():
    if os.name=='nt':
        import ctypes
        class Counters(ctypes.Structure):
            _fields_=[('cb',ctypes.c_ulong),('faults',ctypes.c_ulong)]+[(n,ctypes.c_size_t) for n in ('peak','working','peak_paged','paged','peak_nonpaged','nonpaged','pagefile','peak_pagefile')]
        c=Counters();c.cb=ctypes.sizeof(c)
        require(ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.c_void_p(-1),ctypes.byref(c),c.cb),'MEMORY_OBSERVATION_FAILED')
        return c.peak
    import resource
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024

def file_stamp(path):
    s=path.stat();return (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)

def file_hash(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        while block:=stream.read(1024*1024):h.update(block)
    return h.hexdigest()

def bounded_json(spec):
    path=Path(spec['path']).resolve();hash_text(spec['sha256'])
    require(0<spec['max_bytes']<=96*1024**2 and 0<path.stat().st_size<=spec['max_bytes'],'JSON_INPUT_BOUND')
    stamp=file_stamp(path);data=path.read_bytes()
    require(sha_bytes(data)==spec['sha256'] and file_stamp(path)==stamp,'JSON_INPUT_IDENTITY_OR_STABILITY')
    return strict_json(data),stamp

def run(manifest_path,expected_hash):
    start=time.monotonic();manifest_path=Path(manifest_path).resolve()
    require(0<manifest_path.stat().st_size<=1024*1024,'MANIFEST_BOUND')
    raw=manifest_path.read_bytes();require(sha_bytes(raw)==expected_hash,'MANIFEST_HASH')
    manifest=strict_json(raw)
    require(set(manifest)=={'schema_version','policy_id','inputs','tools_sha256','out_dir','seeds','seed_scope','bounds'},'UNKNOWN_MANIFEST_FIELDS')
    require(manifest['schema_version']==1 and manifest['policy_id']==POLICY,'UNKNOWN_MANIFEST')
    require(manifest['seed_scope']=='STATIC_DIAGNOSTIC_IDENTITY_ONLY_NOT_GAME_REACHABILITY','UNKNOWN_SEED_SCOPE')
    bounds=manifest['bounds'];require(bounds==dict(seconds=900,peak_bytes=1024**3,output_bytes=128*1024**2,max_nodes=100000,max_rows=2000000,max_known_fields=2000000,max_line_bytes=262144,max_uncompressed_bytes=2*1024**3),'UNKNOWN_RESOURCE_BOUNDS')
    require(set(manifest['inputs'])=={'provider_map','binding_summary','binding_fields'},'UNKNOWN_INPUT_SET')
    require(set(manifest['tools_sha256'])=={'tools/rebuild/static_reference_graph.py'},'UNKNOWN_TOOL_SET')
    source=ROOT/'tools/rebuild/static_reference_graph.py';require(sha_bytes(source.read_bytes())==manifest['tools_sha256'][source.relative_to(ROOT).as_posix()],'TOOL_HASH')
    directory=Path(manifest['out_dir']).resolve()
    require(directory.is_relative_to(ROOT/'build/rebuild') and not directory.exists(),'OUTPUT_MUST_BE_NEW_PRIVATE_REBUILD_DIRECTORY')
    specs=manifest['inputs'];paths={Path(s['path']).resolve() for s in specs.values()}
    require(len(paths)==3 and manifest_path not in paths and not any(p.is_relative_to(directory) for p in paths),'INPUT_OUTPUT_COLLISION')
    require(all(p.is_relative_to(ROOT/'build/rebuild') for p in paths),'ONLY_SAVED_REBUILD_METADATA_INPUTS')
    def budget():
        require(time.monotonic()-start<=bounds['seconds'],'TIME_BOUND')
        require(peak_bytes()<=bounds['peak_bytes'],'MEMORY_BOUND')
    provider,ps=bounded_json(specs['provider_map']);budget()
    summary,ss=bounded_json(specs['binding_summary']);budget()
    field_spec=specs['binding_fields'];fieldpath=Path(field_spec['path']).resolve()
    require(set(field_spec)=={'path','sha256','max_bytes','format'} and field_spec['format']=='gzip-jsonl','UNKNOWN_FIELD_STREAM')
    require(0<fieldpath.stat().st_size<=field_spec['max_bytes']<=1024**3,'COMPRESSED_INPUT_BOUND')
    require(summary['details_sha256']==field_spec['sha256'],'SUMMARY_DETAILS_IDENTITY')
    hash_text(summary['implementation_sha256']) # Historical producer pin, not current producer source assertion.
    index=ReferenceIndex(provider,max_nodes=bounds['max_nodes'],max_known_fields=bounds['max_known_fields'])
    del provider
    directory.mkdir();owned=[]
    def own(path):
        stream=path.open('xb');s=os.fstat(stream.fileno());owned.append((path,s.st_dev,s.st_ino));return stream
    def output_bound():require(sum(p.stat().st_size for p,_,_ in owned if p.exists())+(directory/'progress.jsonl').stat().st_size<=bounds['output_bytes'],'TOTAL_OUTPUT_BOUND')
    journal=(directory/'progress.jsonl').open('x',encoding='utf8')
    def note(event):journal.write(json.dumps(event,sort_keys=True)+'\n');journal.flush();os.fsync(journal.fileno())
    try:
        note(dict(state='started',policy_id=POLICY,manifest_sha256=expected_hash))
        edgepath=directory/'references.jsonl.gz';count=0;uncompressed=0
        stamp=file_stamp(fieldpath)
        with fieldpath.open('rb') as original,own(edgepath) as output:
            reader=HashingReader(original)
            with gzip.GzipFile(fileobj=reader,mode='rb') as stream,gzip.GzipFile(fileobj=output,mode='wb',filename='',mtime=0) as sink:
                while True:
                    line=stream.readline(bounds['max_line_bytes']+1)
                    if not line:break
                    count+=1;uncompressed+=len(line)
                    require(count<=bounds['max_rows'] and len(line)<=bounds['max_line_bytes'] and line.endswith(b'\n') and uncompressed<=bounds['max_uncompressed_bytes'],'STREAM_ROW_OR_EXPANSION_BOUND')
                    row=index.consume(strict_json(line),count);sink.write(canonical(row)+b'\n')
                    if count%1024==0:budget();sink.flush();output_bound()
            while reader.read(1024*1024):pass
            require(reader.hasher.hexdigest()==field_spec['sha256'],'STREAM_HASH_MISMATCH')
            require(file_stamp(fieldpath)==stamp,'STREAM_CHANGED_DURING_PASS')
            output.flush();os.fsync(output.fileno())
        index.validate_census(summary);budget();output_bound()
        nodepath=directory/'nodes.jsonl.gz'
        with own(nodepath) as output,gzip.GzipFile(fileobj=output,mode='wb',filename='',mtime=0) as sink:
            for ordinal,row in enumerate(index.node_rows(),1):
                sink.write(canonical(row)+b'\n')
                if ordinal%1024==0:budget();sink.flush();output_bound()
        report=index.report(manifest['seeds']);budget();output_bound()
        report.update(schema_version=1,kind='conservative-saved-static-reference-index',manifest_sha256=expected_hash,
            input_sha256={k:s['sha256'] for k,s in specs.items()},historical_binding_producer_sha256=summary['implementation_sha256'],
            stream_read_passes=1,stream_sha256_verified_at_EOF=True,input_field_uncompressed_bytes=uncompressed,
            input_stat_stability=True,elapsed_seconds=round(time.monotonic()-start,3),peak_memory_bytes=peak_bytes(),
            files={p.name:dict(sha256=file_hash(p),bytes=p.stat().st_size) for p in (edgepath,nodepath)})
        # Only own derived outputs are rehashed; never repeat input streams.
        def stable_inputs():
            require(file_stamp(Path(specs['provider_map']['path']).resolve())==ps and file_stamp(Path(specs['binding_summary']['path']).resolve())==ss and file_stamp(fieldpath)==stamp,'LATE_INPUT_STAT_DRIFT')
            require(sha_bytes(source.read_bytes())==manifest['tools_sha256'][source.relative_to(ROOT).as_posix()] and sha_bytes(manifest_path.read_bytes())==expected_hash,'LATE_TOOL_OR_MANIFEST_DRIFT')
        stable_inputs()
        with own(directory/'manifest.json') as output:output.write(canonical(report)+b'\n');output.flush();os.fsync(output.fileno())
        stable_inputs();budget();output_bound();note(dict(state='complete',nodes=len(index.nodes),rows=count))
        budget();output_bound();return report
    except BaseException as error:
        for path,device,inode in owned:
            if path.exists() and file_stamp(path)[:2]==(device,inode):path.unlink()
        note(dict(state='failed',error_type=type(error).__name__,reason=str(error)[:200]));raise
    finally:journal.close()

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--manifest',type=Path,required=True);parser.add_argument('--manifest-sha256',required=True)
    args=parser.parse_args(argv);report=run(args.manifest,args.manifest_sha256)
    print(json.dumps({k:report[k] for k in ('selected_physical_nodes','input_field_rows','known_unique_static_edges','graph_coverage')}))
    return 0

if __name__=='__main__':raise SystemExit(main())
