"""Finite current-frontier CODE production; prior pools and policies stay frozen."""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import argparse
import gzip
import io
import json
import os
import re
import struct
import sys
import time
import ordinary_relocation_factory as fields
import current_code_frontier as planner

base=fields.base
ROOT=base.ROOT
POLICY='finite-current-frontier-CODE-factory-v1'
OWNED=('tools/rebuild/frontier_code_factory.py','tests/rebuild/test_frontier_code_factory.py','docs/rebuild/FRONTIER-CODE-FACTORY.md')
require=base.require
digest=base.digest
FALSE=dict(fields.FALSE,application_manifest_adopted=False)
PINS={**planner.PINS,'tools/rebuild/current_code_frontier.py':'34ad6b6aacf0a9c5b0cfd68cf26fdd57e18cec4f9b74e24b48296049703397bc'}
PINS['tools/rebuild/frontier_root_collect.py']='751cf4fb09d94a41abcb37778fcdd194484cb498a465aaa9eb9c22e7438705f8'
SOURCE_KEYS={'epoch_receipt','epoch_manifest','frontier','epoch_review','new_receipt','new_details','new_review'}
SOURCE_PINS=dict(epoch_receipt='9e8849e43686622544d15d3639234868d4d6d7617c206ea3ebfa980a0b3b1266',
    epoch_manifest='e1bb236a98cdecf8480dd0aacedd66866ffe939d61a3d63e34bfe266461260f7',
    frontier='78e4bf8ad266efb726836458444feb1d368d06b0ac74d1cdfb1d7d1d742c5f51',
    epoch_review='618808fb03b51e445071e41f72976e044700f46788a14c6b7584342d42a85370',
    new_receipt='ea4e02c8e62264f65662ed4c9d5fdd2e4d990bf9b6c3dd70b5e0553b61f43da5',
    new_details='100d8805aa9ab2b04781b84d6b7454773a01783cdf60cf5f9a31619b7c38769f')
MAX_CONTEXT=16*1024**2


def candidate_request(frontier,new_summary,old_receipt_sha256,new_receipt_sha256,exclusions):
    """Select every unprepared positive, never an arbitrary root-size sample.

    The current accepted composed positives belong to the prepared typed12
    cohort. No negative bare certificate is relabeled from a composition flag.
    """
    require(frontier['kind']=='current-CODE-frontier-reconciliation' and frontier['code_demands']==len(frontier['records']) and
        dict(Counter(r['state'] for r in frontier['records']))==frontier['counts'],'complete current frontier ledger required')
    require(all(isinstance(h,str) and re.fullmatch('[0-9a-f]{64}',h) for h in (old_receipt_sha256,new_receipt_sha256)),
        'exact source authority receipt hashes required')
    singles={}
    for row in new_summary['observations']:
        if row['event']!='SINGLE_ROOT_OBSERVATION':continue
        require(len(row['roots'])==1 and row['roots'][0] not in singles,'duplicate/multi-root new observation')
        singles[row['roots'][0]]=row
    missing={r['original_address']:r for r in frontier['new_roots']}
    require(len(missing)==len(frontier['new_roots']) and set(singles)==set(missing),'every unique newly requested original root must be accounted')
    roots=[];selected=[];ledger=[];seen=set()
    for item in frontier['records']:
        name=item['symbol'];require(name not in seen,'duplicate immediate namespace');seen.add(name)
        state=item['state'];entry=dict(symbol=name,upstream_state=state,group_sha256=item['group_sha256'])
        if state=='PREPARED_SKIP':
            require(name in exclusions,'prepared skip lacks current accepted export');entry['status']='PREPARED_SKIP'
        elif state in ('UNSELECTED_OR_NAMESPACE_UNPROVED','CACHED_ORIGINAL_OMISSION_BLOCKED'):
            require(name not in exclusions,'prepared owner misclassified as blocker');entry['status']=state
            if 'root' in item:entry.update(root=item['root'],original_observation=item['cached_observation'])
        else:
            require(state in ('CACHED_BARE_POSITIVE_REQUIRES_FRESH_CLASSIFICATION','NEW_SELECTED_ROOT_REQUIRES_OBSERVATION'),
                'unknown frontier state')
            root=item['root'];a=root['original_address'];identity={k:root[k] for k in ('recipe_id','object_sha256','symbol_index')}
            require(name==base.pool.canonical(identity) and name not in exclusions,'selected root namespace/collision differs')
            if state=='NEW_SELECTED_ROOT_REQUIRES_OBSERVATION':require(root==missing.get(a),'new root request/source identity differs')
            summary=item['cached_observation'] if state.startswith('CACHED_') else singles[a]
            require(summary['event']=='SINGLE_ROOT_OBSERVATION' and summary['roots']==[a] and
                summary.get('recipe_id')==root['recipe_id'] and type(summary['closure_observed']) is bool,
                'borrowed/union original root observation')
            if state.startswith('CACHED_'):require(summary['closure_observed'] is True,'positive cached frontier state contradicts its observation')
            if summary['closure_observed'] is not True:
                require(summary['blocker_codes'],'negative new root lacks explicit blocker')
                entry.update(status='NEW_ORIGINAL_OMISSION_BLOCKED',root=root,original_observation=summary)
            else:
                require(summary.get('graph_observation_complete') is True and not summary['blocker_codes'],'positive root graph incomplete or retains blockers')
                authority='cached-central' if state.startswith('CACHED_') else 'new-frontier'
                locator=dict(kind=authority,receipt_sha256=old_receipt_sha256 if authority=='cached-central' else new_receipt_sha256,
                    record_sha256=summary['record_sha256'],certificate_sha256=summary['certificate_sha256'])
                if authority=='cached-central':locator.update(lane=summary['lane'],ordinal=summary['lane_record_ordinal'])
                else:locator.update(ordinal=summary['ordinal'])
                entry.update(status='REQUESTED_FRESH_CLASSIFICATION',root=root,authority=locator)
                selected.append(dict(root=root,authority=locator));roots.append(root)
        ledger.append(entry)
    require(len(roots)==len({r['original_address'] for r in roots}),'duplicate selected root')
    roots.sort(key=lambda r:r['original_address']);selected.sort(key=lambda r:r['root']['original_address'])
    return dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=roots),selected,ledger


def verify_candidate(raw,row,root,providers,exports,original_path,stage_path,pe,recipe):
    """Use the appropriate frozen core, with no positive-certificate synthesis."""
    contract=row['contract'];certificate=row['certificate']
    require(row['requested_roots']==[root] and certificate['closure_observed'] is True and not certificate['blockers'],
        'exact positive bare observation required')
    if contract['fields']:
        return fields.verify_member(raw,contract,certificate,[root],providers,exports,original_path,stage_path,pe,recipe)
    # Frozen zero consumer owns its complete strict graph/record/export policy.
    require(base.pool.canonical({k:root[k] for k in ('recipe_id','object_sha256','symbol_index')}) not in exports and
        providers[root['original_address']]=={k:root[k] for k in ('recipe_id','object_sha256','symbol_index')},'zero root planned namespace collision')
    contracts=[dict(selected={k:root[k] for k in base.NATIVE_KEYS})]
    before=base.bulk.compare_functions(original_path,pe,contracts,recipe)
    output,projection=base.project_member(raw,contract,certificate,[root])
    base.pool.fsynced(Path(stage_path),output);base.bulk.strict_reparse(Path(stage_path),output)
    after=base.bulk.compare_functions(stage_path,pe,contracts,recipe,dict(bindings=projection['namespace_bindings'],comparison_base_view={}))
    projection.update(before_comparison=before,after_comparison=after,fields=[],comparison_base_view={},
        strict_zero_consumer_replayed=True)
    return output,projection


def write_context(stream,row,selection):
    """One independently compressed frame permits bounded random access."""
    authority=selection['authority'];root=selection['root']
    require(digest(row)==authority['record_sha256'] and row['event']=='SINGLE_ROOT_OBSERVATION' and
        row['requested_roots']==[root] and row['closure_observed'] is True and row['graph_observation_complete'] is True and
        row['certificate_sha256']==digest(row['certificate'])==authority['certificate_sha256'] and
        row['contract_identity_sha256']==digest(row['contract'])==row['certificate']['contract_identity_sha256'] and
        row['certificate']['closure_observed'] is True and row['certificate']['graph_observation_complete'] is True and
        row['provenance']==row['contract']['provenance'] and not row['certificate']['blockers'],
        'selected source context/authority differs')
    raw=json.dumps(dict(row=row,selection=selection),sort_keys=True,separators=(',',':')).encode()
    require(len(raw)<=MAX_CONTEXT,'selected context raw bound')
    packed=gzip.compress(raw,mtime=0);require(len(packed)<=MAX_CONTEXT,'selected context compressed bound')
    offset=stream.tell();stream.write(struct.pack('<Q',len(packed)));stream.write(packed)
    return dict(original_address=root['original_address'],offset=offset,bytes=len(packed),frame_sha256=base.coff.digest(packed),
        context_sha256=base.coff.digest(raw),record_sha256=digest(row),authority=authority)


def read_context(stream,index,selection):
    require(index['original_address']==selection['root']['original_address'] and index['authority']==selection['authority'],
        'private context index borrowed source authority')
    require(type(index['offset']) is int and type(index['bytes']) is int and index['offset']>=0 and 0<index['bytes']<=MAX_CONTEXT,'context frame geometry')
    stream.seek(index['offset']);header=stream.read(8)
    require(len(header)==8 and struct.unpack('<Q',header)[0]==index['bytes'],'private frame header differs')
    packed=stream.read(index['bytes']);require(len(packed)==index['bytes'] and base.coff.digest(packed)==index['frame_sha256'],'private frame bytes changed')
    with gzip.GzipFile(fileobj=io.BytesIO(packed),mode='rb') as decoded:
        raw=decoded.read(MAX_CONTEXT+1);require(len(raw)<=MAX_CONTEXT and decoded.read(1)==b'','private frame decompression bound')
    require(base.coff.digest(raw)==index['context_sha256'],'private context identity changed')
    value=json.loads(raw);require(set(value)=={'row','selection'} and value['selection']==selection and
        digest(value['row'])==index['record_sha256']==selection['authority']['record_sha256'],'private context/source row differs')
    return value['row']


def spool_selected(out,central,lanes_dir,new_receipt,new_details,selected,inputs,start):
    wanted={r['root']['original_address']:r for r in selected};indices={};seen=set()
    require(len(wanted)==len(selected),'duplicate complete selected context request')
    old_index={(r['lane'],r['lane_record_ordinal']):r for r in central['observations']}
    require(len(old_index)==len(central['observations']),'duplicate original source locator')
    path=out/'contexts.bin'
    with path.open('xb') as spool:
        old_total=0;old_characters=0
        for lane,artifact in sorted(central['lane_artifacts'].items(),key=lambda p:int(p[0])):
            require(re.fullmatch(r'code-lane-\d\d.jsonl.gz',artifact['path']),'foreign cached lane path')
            source=base.observe(Path(lanes_dir)/artifact['path'],artifact['sha256'],inputs)
            require(source.stat().st_size==artifact['bytes'],'cached lane extent differs')
            count=0
            with gzip.open(source,'rt') as stream:
                for line in stream:
                    count+=1;old_total+=1;old_characters+=len(line)
                    require(len(line)<=64*1024**2 and old_characters<=4*1024**3 and count<=1000,'original cached row bound')
                    row=json.loads(line);summary=old_index.get((int(lane),count))
                    require(summary and digest(row)==summary['record_sha256'] and row['event']==summary['event'] and
                        row['recipe_id']==summary['recipe_id'] and [r['original_address'] for r in row['requested_roots']]==summary['roots'],
                        'cached source row/locator differs')
                    base.budget(start,out)
                    if row['event']!='SINGLE_ROOT_OBSERVATION':continue
                    a=row['requested_roots'][0]['original_address'];selection=wanted.get(a)
                    if selection and selection['authority']['kind']=='cached-central':
                        require(a not in seen and selection['authority']['lane']==int(lane) and selection['authority']['ordinal']==count,'cached selected locator differs')
                        indices[a]=write_context(spool,row,selection);seen.add(a)
            require(count==artifact['records'],'original cached lane record count differs');base.budget(start,out)
        require(old_total==len(old_index)==303,'original complete cached universe differs')
        summaries=new_receipt['observations'];count=0
        with gzip.open(new_details,'rt') as stream:
            for line in stream:
                count+=1;require(count<=len(summaries) and len(line)<=MAX_CONTEXT,'new context source bound')
                row=json.loads(line);summary=summaries[count-1]
                require(summary['ordinal']==count and digest(row)==summary['record_sha256'] and row['event']==summary['event'] and
                    row['recipe_id']==summary['recipe_id'] and [r['original_address'] for r in row['requested_roots']]==summary['roots'] and
                    row['graph_observation_complete']==summary['graph_observation_complete'],'new source row/locator differs')
                if row['event']!='SINGLE_ROOT_OBSERVATION':continue
                a=row['requested_roots'][0]['original_address'];selection=wanted.get(a)
                if selection and selection['authority']['kind']=='new-frontier':
                    require(a not in seen and selection['authority']['ordinal']==count,'new selected locator differs')
                    indices[a]=write_context(spool,row,selection);seen.add(a)
        require(count==len(summaries) and seen==set(wanted),'selected context universe incomplete')
        spool.flush();os.fsync(spool.fileno())
    base.save_json(out/'contexts-index.json',indices)
    return path,indices


def protect_context_artifacts(spool,index_path,indices,inputs):
    """Saved index and bytes become protected inputs to actual projection."""
    spool_hash=base.file_hash(spool);index_hash=base.file_hash(index_path)
    require(base.load_json(index_path)==indices,'saved context index differs from authenticated in-memory index')
    base.observe(spool,spool_hash,inputs);base.observe(index_path,index_hash,inputs)
    return spool_hash,index_hash


def write_coverage(path,source,providers,exclusions,frontier,requested,emitted):
    demanded={r.get('root',{}).get('original_address'):r for r in frontier['records'] if r.get('root')}
    counts=Counter();seen=set()
    with gzip.open(source,'rt') as original,Path(path).open('xb') as file:
        with gzip.GzipFile(fileobj=file,mode='wb',mtime=0) as target:
            for ordinal,line in enumerate(original,1):
                require(ordinal<=68657 and len(line)<=4*1024**2,'historical coverage bound')
                row=json.loads(line);a=row['original_address'];require(a not in seen and row['physical_identity']==providers[a],'historical owner identity differs');seen.add(a)
                prepared=base.pool.canonical(providers[a]) in exclusions
                require(a not in requested or not prepared,'new projection would replace prepared owner')
                status='NEW_FRONTIER_PROJECTED' if a in emitted else 'REQUEST_QUARANTINED' if a in requested else 'NOT_REQUESTED'
                counts[status]+=1
                value=dict(original_address=a,physical_identity=row['physical_identity'],original_status=row['status'],
                    original_coverage_row=dict(ordinal=ordinal,sha256=digest(row)),prepared_namespace_present=prepared,
                    current_frontier_state=demanded[a]['state'] if a in demanded else None,frontier_projection_status=status,**FALSE)
                target.write((json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode())
        file.flush();os.fsync(file.fileno())
    require(len(seen)==68657 and set(requested)<=seen,'complete historical owner accounting differs')
    return dict(counts)


def review_gate(args,inputs):
    review=base.load_json(base.observe(args.review,args.review_sha256,inputs))
    require(review.get('schema_version')==1 and review.get('kind')=='finite-frontier-CODE-factory-review-v1' and
        review.get('approved') is True and review.get('independent_source_schema_review_pass') is True and
        review.get('root_authorized') is True and review.get('reviewer') and review.get('operation_sha256')==args.operation_sha256 and
        review.get('all_positive_current_frontier_roots_required') is True and review.get('new_observation_independently_accepted') is True and
        review.get('producer_sha256')==PINS and review.get('fixed_source_sha256')==SOURCE_PINS and
        set(review.get('source_sha256',{}))==set(OWNED) and review.get('allow_native_tools') is False and review.get('allow_game_execution') is False,
        'exact independent source/input acceptance and finite delegated authorization required')
    for rel,h in {**review['source_sha256'],**PINS}.items():base.observe(ROOT/rel,h,inputs)
    base.stable(inputs);return review


def run(args):
    start=time.monotonic();inputs={};review=review_gate(args,inputs)
    operation=base.load_json(base.observe(args.operation,args.operation_sha256,inputs))
    require(set(operation)=={'schema_version','kind','sources','root_request','output_relative','resource_limits'} and
        type(operation['schema_version']) is int and operation['schema_version']==1 and operation['kind']=='ALL-positive-V5-CODE-production' and
        set(operation['sources'])==SOURCE_KEYS and operation['resource_limits']==dict(seconds=900,peak_memory_bytes=1024**3,output_bytes=128*1024**2),
        'complete finite operation schema required')
    paths={}
    for key,value in operation['sources'].items():
        require(set(value)=={'path','sha256'} and isinstance(value['path'],str) and not Path(value['path']).is_absolute(),'strict private source locator')
        path=(ROOT/value['path']).resolve();require(path.is_relative_to(ROOT/'build/rebuild'),'foreign finite source input')
        if key in SOURCE_PINS:require(value['sha256']==SOURCE_PINS[key],'fixed accepted frontier source differs')
        paths[key]=base.observe(path,value['sha256'],inputs)
    require(review.get('operation_sources')==operation['sources'],'independent phase/source authority differs')
    epoch_receipt=base.load_json(paths['epoch_receipt']);epoch=base.load_json(paths['epoch_manifest']);frontier=base.load_json(paths['frontier'])
    require(epoch_receipt['status']=='completed' and epoch_receipt['input_stability'] is True and
        epoch_receipt['artifacts']['prepared-epoch.json']==SOURCE_PINS['epoch_manifest'] and epoch_receipt['artifacts']['frontier.json']==SOURCE_PINS['frontier'],
        'successful accepted successor epoch differs')
    # These bound metadata/artifact fingerprints do not reopen old owner/binding streams.
    for p,h in epoch_receipt['inputs'].items():base.observe(Path(p),h,inputs)
    central=base.load_json(base.observe(ROOT/'build/rebuild'/planner.INPUTS['central'][0],planner.INPUTS['central'][1],inputs))
    new=base.load_json(paths['new_receipt'])
    require(new['policy_id']=='new-frontier-ordinary-root-observation-v1' and new['status']=='metadata-only' and
        new['input_stability'] is True and new['optional_function_index_present'] is False and
        new['prior_receipt_sha256']==planner.INPUTS['central'][1] and new['planned_map_sha256']==fields.MAP_PIN and
        new['frontier_join_sha256']==SOURCE_PINS['frontier'] and new['request_sha256']==epoch_receipt['artifacts']['missing-request.json'] and
        new['details_sha256']==SOURCE_PINS['new_details'] and new['collector_sha256']==PINS['tools/rebuild/frontier_root_collect.py'] and
        new['summary']['roots']==10 and new['cached_roots_reobserved']==0 and new['owner_stream_traversals']==0 and new['binding_stream_traversals']==1,
        'new-only independently accepted observation epoch differs')
    reports={n:base.load_json(base.observe(ROOT/'build/rebuild'/p,base.inventory.EXPECTED[n],inputs)) for n,p in
        [('selection','function-selection-v2.json'),('manifest','objects-20261103T030230Z-7cfc935c.json'),('retained','retained-verify-full-v3.json'),('owners','runtime-data-owners-native-v1.json')]}
    units={u['recipe_id']:u for u in reports['manifest']['units']};proofs={u['recipe_id']:u for u in reports['retained']['units']}
    require(len(units)==len(proofs)==2988 and len(reports['selection']['selections'])==68657,'complete original source context differs')
    recipes=base.observe(ROOT/'build/units.json',base.inventory.EXPECTED['recipes'],inputs)
    require(base.reconcile_recipes(reports['manifest'],recipes)['verified'],'original source variants differ')
    expanded=base.load_json(base.observe(args.provider_map,fields.MAP_PIN,inputs))
    base.observe(ROOT/'build/rebuild'/fields.MAP_REVIEW[0],fields.MAP_REVIEW[1],inputs)
    providers=fields.validate_provider_map(expanded,reports['selection']['selections'],units,proofs,reports['owners'])
    # Rebuild the full successor, rather than trusting a cached namespace list.
    parent=base.load_json(ROOT/'build/rebuild'/planner.INPUTS['prepared_manifest'][0])
    rebuilt=planner.successor_epoch(parent,expanded['providers'],base.load_json(ROOT/'build/rebuild'/planner.INPUTS['typed_members'][0]),
        base.load_json(ROOT/'build/rebuild'/planner.INPUTS['eh_metadata'][0]),base.load_json(ROOT/'build/rebuild'/planner.INPUTS['eh_receipt'][0]),
        typed_members_sha256=planner.INPUTS['typed_members'][1],eh_metadata_sha256=planner.INPUTS['eh_metadata'][1])
    require(rebuilt==epoch,'fresh complete successor namespace reconstruction differs');exports=set(epoch['exclusion_names'])
    require(len(exports)==14346 and epoch['ordinary_prepared_count']==14341,'accepted prepared epoch census differs')
    request,selected,ledger=candidate_request(frontier,new,planner.INPUTS['central'][1],SOURCE_PINS['new_receipt'],exports)
    require(operation['root_request']==request and 0<len(request['roots'])<=208,'operation truncates/substitutes current positive roots')
    require(len(request['roots'])==60,'exact accepted current positive root census differs')
    base.collector.validate_request(request,reports['selection']['selections'],reports['manifest'],reports['retained'],providers)
    wanted={r['original_address']:r for r in request['roots']}
    retained_tools=dict(reports['retained']['inputs']['tools_sha256']);image_check_hash=reports['retained']['inputs']['image_check_sha256']
    object_paths={};object_root=reports['manifest'].get('object_root_relative','.')
    for a,r in wanted.items():
        u=units[r['recipe_id']];source=(ROOT/u['source']).resolve();obj=(ROOT/'build/rebuild'/object_root/u['object']).resolve()
        require(source.is_relative_to(ROOT) and obj.stat().st_size<=16*1024**2,'bounded original source/native object required')
        base.observe(source,r['source_sha256'],inputs);base.observe(obj,r['object_sha256'],inputs);object_paths[a]=obj
    for rel,h in retained_tools.items():base.observe(ROOT/rel,h,inputs)
    base.observe(ROOT/'build/image_check.json',image_check_hash,inputs)
    reference=base.observe(args.reference,base.pool.PINS['reference'],inputs)
    coverage_source=base.observe(ROOT/'build/rebuild'/fields.ARTIFACTS['baseline_coverage'][0],fields.ARTIFACTS['baseline_coverage'][1],inputs)
    out=Path(args.out).resolve();private=(ROOT/'build/rebuild').resolve()
    require(out==(ROOT/operation['output_relative']).resolve() and out.is_relative_to(private) and out!=private and not out.exists() and
        not any(p.is_relative_to(out) for p in inputs),'exact new exclusive finite output required')
    # Large whole-universe metadata is no longer needed during per-root replay.
    del expanded,proofs,reports,rebuilt,parent
    base.stable(inputs);out.mkdir();journal=(out/'progress.jsonl').open('x',encoding='utf-8')
    def note(state,**facts):journal.write(json.dumps(dict(state=state,elapsed_seconds=round(time.monotonic()-start,3),**facts))+'\n');journal.flush();os.fsync(journal.fileno())
    members=[];receipts=[];assessments=[];blocked=[];emitted=[];metadata=None
    try:
        note('started',requested=len(wanted),frontier_demands=208,prepared_exclusions=len(exports),all_positive_roots_included=True)
        for rel,h in review['source_sha256'].items():
            raw=(ROOT/rel).read_bytes();require(base.coff.digest(raw)==h,'frozen source drift');snapshot=out/'source-snapshots'/rel
            snapshot.parent.mkdir(parents=True,exist_ok=True);base.pool.fsynced(snapshot,raw)
        spool,index=spool_selected(out,central,args.lanes_dir,new,paths['new_details'],selected,inputs,start)
        spool_hash,index_hash=protect_context_artifacts(spool,out/'contexts-index.json',index,inputs)
        note('all_selected_contexts_spooled',contexts=len(index),spool_sha256=spool_hash,index_sha256=index_hash)
        del central,new,epoch_receipt
        sys.path.insert(0,str(ROOT/'tools'));import compare as oracle
        from build_and_match import image_ok
        pe=base.checked_reference(reference,oracle,image_ok);metadata=planner.typed.SnapshotPe(reference,pe)
        highlow={metadata.base+rva for rva in metadata.relocations()};require(len(highlow)==351931,'fresh original HIGHLOW census differs')
        facts={};audited_fields=0
        with spool.open('rb') as context_stream:
            for selection in selected:
                base.budget(start,out);root=selection['root'];a=root['original_address'];row=read_context(context_stream,index[a],selection)
                contract=row['contract'];certificate=row['certificate']
                for rel,h in contract['provenance']['dependency_tools_sha256'].items():
                    p=(ROOT/rel).resolve();require(p.is_relative_to(ROOT/'tools'),'foreign observer dependency');base.observe(p,h,inputs)
                raw=object_paths[a].read_bytes();require(base.coff.digest(raw)==root['object_sha256'],'fresh source object changed')
                for site,fact in planner.typed.audit_original_fields(metadata,highlow,contract['fields']).items():
                    require(site not in facts or facts[site]==fact,'original selected field contradiction');facts[site]=fact
                audited_fields+=len(contract['fields'])
                if contract['fields']:
                    assessment=fields.core.assess_member(raw,contract,certificate,[root],providers,existing_exports=exports)
                    assessments.append(dict(original_address=a,assessment=assessment))
                    if assessment['eligible'] is not True:
                        require(assessment['blockers'],'unsupported root has no explicit reason');blocked.append(dict(root=root,blockers=assessment['blockers'],fresh_body_compared=False))
                        note('root_quarantined',original_address=a,blockers=assessment['blockers']);continue
                else:
                    assessment=None  # Strict frozen zero-consumer replay occurs below; no cached eligibility claim.
                name='frontier-%03d-%s.obj'%(len(members),a[2:]);path=out/name
                output,projection=verify_candidate(raw,row,root,providers,exports,object_paths[a],path,pe,units[root['recipe_id']]['recipe'])
                if assessment is not None:require(projection['exports']==assessment['exports'] and projection['fields']==assessment['fields'],'fresh field plan changed')
                else:assessments.append(dict(original_address=a,strict_zero_consumer_replayed=True,serialization_performed=True,output_sha256=projection['output_sha256']))
                projection.update(authority=selection['authority'],central_record_sha256=digest(row))
                members.append((name,output));receipts.append(dict(name=name,projection=projection));emitted.append(a)
                note('member_verified',original_address=a,fields=len(projection['fields']),member_sha256=base.coff.digest(output))
        metadata.close();metadata=None
        require(base.file_hash(spool)==spool_hash and base.file_hash(out/'contexts-index.json')==index_hash,
            'private context spool or saved index changed during use')
        archive_hash=None
        if members:
            archive=base.coff.archive(members);base.pool.fsynced(out/'frontier-code.lib',archive);recovered=base.coff.read_archive(archive)
            require(recovered['members']==members and len(recovered['index'])==len(emitted),'archive members/defined-export indices differ')
            for name,data in recovered['members']:
                p=out/('recovered-'+name);base.pool.fsynced(p,data);base.bulk.strict_reparse(p,data)
            archive_hash=base.coff.digest(archive)
        coverage=write_coverage(out/'coverage.jsonl.gz',coverage_source,providers,exports,frontier,set(wanted),set(emitted))
        quarantine={r['root']['original_address']:r['blockers'] for r in blocked}
        for item in ledger:
            if item['status']=='REQUESTED_FRESH_CLASSIFICATION':
                a=item['root']['original_address']
                item['production_status']='EMITTED' if a in emitted else 'QUARANTINED_UNSUPPORTED_POLICY'
                if a in quarantine:item['production_blockers']=quarantine[a]
                require(a in emitted or a in quarantine,'requested frontier root lacks terminal outcome')
            else:item['production_status']=item['status']
        for name,value in [('members',receipts),('blocked',blocked),('assessments',assessments),('frontier-ledger',ledger)]:base.save_json(out/(name+'.json'),value)
        audit=dict(highlow_sites=len(highlow),retained_fields=audited_fields,unique_field_sites=len(facts),
            field_facts_sha256=digest(sorted(facts.items())),loaded_reference_sha256=base.coff.digest(pe.data),original_highlow_authority_authenticated=True)
        base.save_json(out/'original-field-audit.json',audit);base.stable(inputs)
        result=dict(schema_version=1,policy_id=POLICY,status='completed' if len(emitted)==len(wanted) else 'completed-incomplete',
            operation_sha256=args.operation_sha256,review_sha256=args.review_sha256,requested=len(wanted),emitted=len(emitted),blocked=len(blocked),
            emitted_addresses=emitted,archive_sha256=archive_hash,prepared_exclusion_count=14346,ordinary_prepared_upstream_count=14341,
            all_positive_frontier_roots_requested=True,whole_frontier_demands=208,whole_frontier_counts=frontier['counts'],
            final_frontier_counts=dict(Counter(r['production_status'] for r in ledger)),
            fields=sum(len(r['projection']['fields']) for r in receipts),code_bytes=sum(r['projection']['requested_roots'][0]['size'] for r in receipts),
            context_spool_sha256=spool_hash,context_index_sha256=index_hash,derived_context_inputs_protected=2,
            output_sha256={n:base.file_hash(out/n) for n in ('members.json','blocked.json','assessments.json','frontier-ledger.json','coverage.jsonl.gz','original-field-audit.json')},
            historical_owners=68657,coverage_counts=coverage,inputs={str(p):h for p,h in inputs.items()},inputs_stable=True,
            optional_function_index_present=False,native_archive_conformance_verified=False,resource_observations=base.budget(start,out),
            resource_limits=operation['resource_limits'],**FALSE)
        return base.finalize_success(out,result,inputs,start,journal,note)
    except BaseException as error:
        try:
            if not journal.closed:note('failed',error_type=type(error).__name__,message=str(error),completed_members=len(emitted))
        except OSError:pass
        base.save_json(out/'abort.json',dict(status='aborted-no-retry',error_type=type(error).__name__,message=str(error),completed_members=emitted,successful_projection=False,**FALSE));raise
    finally:
        if metadata is not None:metadata.close()
        if not journal.closed:journal.close()


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('operation','review','provider-map','lanes-dir','reference','out'):parser.add_argument('--'+name,required=True,type=Path,dest=name.replace('-','_'))
    for name in ('operation','review'):parser.add_argument('--'+name+'-sha256',required=True,dest=name+'_sha256')
    args=parser.parse_args(argv)
    try:result=run(args)
    except (ValueError,OSError,KeyError,TypeError) as error:parser.exit(2,'current frontier factory rejected: '+str(error)+'\n')
    print(json.dumps({k:result[k] for k in ('status','requested','emitted','blocked','fields','archive_sha256')}));return 0 if result['status']=='completed' else 3


if __name__=='__main__':raise SystemExit(main())
