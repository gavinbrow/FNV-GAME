"""V8 new-only context selection and sealed spool; versioned operational factory."""
from __future__ import annotations
from collections import Counter
import argparse
import gzip
import json
import os
import re
import time
import sys
from pathlib import Path
import frontier_code_factory as frozen
import code_frontier_wave_v8 as wave
base=frozen.base
ROOT=base.ROOT
require=base.require
digest=base.digest
POLICY='V8-new-only-CODE-wave-factory-v1'
FALSE=dict(frozen.FALSE,cached_context_bodies_reloaded=False)


def select_new_contexts(frontier,registry,new_receipt,new_receipt_sha256):
    """Every new selected root has an outcome; every positive enters the batch."""
    require(frontier['frontier']=='accepted-V8' and frontier['code_demands']==len(frontier['records'])==467 and
        dict(Counter(r['state'] for r in frontier['records']))==frontier['counts'] and frontier['cached_positive_roots']==[],
        'complete V8 frontier with no cached positive candidates required')
    missing_count=len(frontier['new_roots'])
    require(missing_count>0,'nonempty exact new-root request required')
    requested={r['original_address']:r for r in frontier['new_roots']}
    require(len(requested)==len(frontier['new_roots'])==missing_count and len(registry['records'])==registry['roots']==269 and
        not(set(requested)&set(registry['records'])),'exact missing-only roots distinct from cached269')
    require(new_receipt.get('status')=='metadata-only' and new_receipt.get('input_stability') is True and
        new_receipt.get('optional_function_index_present') is False and new_receipt.get('policy_id')=='new-frontier-ordinary-root-observation-v3' and
        new_receipt['summary']['roots']==missing_count,'complete accepted new-only metadata envelope required')
    demands=[r for r in frontier['records'] if r['state']=='NEW_SELECTED_ROOT_REQUIRES_OBSERVATION']
    demand_roots={r['root']['original_address']:r['root'] for r in demands}
    require(len({r['symbol'] for r in frontier['records']})==467 and len(demands)==len(demand_roots)==missing_count and demand_roots==requested,
        'whole unique current demand/root census differs')
    require(isinstance(new_receipt_sha256,str) and re.fullmatch('[0-9a-f]{64}',new_receipt_sha256),'exact new receipt hash')
    singles={};locators=set()
    for summary in new_receipt['observations']:
        if summary['event']!='SINGLE_ROOT_OBSERVATION':continue
        require(len(summary['roots'])==1 and summary['roots'][0] not in singles,'duplicate/non-singleton new-root summary')
        require(type(summary['ordinal']) is int and summary['ordinal']>0 and summary['ordinal'] not in locators and
            isinstance(summary['record_sha256'],str) and re.fullmatch('[0-9a-f]{64}',summary['record_sha256']), 'new source locator/hash schema')
        locators.add(summary['ordinal'])
        singles[summary['roots'][0]]=summary
    require(set(singles)==set(requested),'all new new observations must be accounted')
    selected=[];ledger=[]
    for item in frontier['records']:
        state=item['state'];row=dict(item,production_status=state)
        if state=='NEW_SELECTED_ROOT_REQUIRES_OBSERVATION':
            root=item['root'];a=root['original_address'];summary=singles[a]
            require(root==requested[a] and root['recipe_id']==summary['recipe_id'] and type(summary['closure_observed']) is bool and
                type(summary['graph_observation_complete']) is bool and item['symbol']==base.pool.canonical({k:root[k] for k in
                    ('recipe_id','object_sha256','symbol_index')}),'new frontier/root/source summary or namespace differs')
            if summary['closure_observed']:
                require(summary['graph_observation_complete'] and not summary['blocker_codes'],'positive new graph remains incomplete')
                require(isinstance(summary['certificate_sha256'],str) and re.fullmatch('[0-9a-f]{64}',summary['certificate_sha256']), 'positive certificate hash')
                authority=dict(kind='new-frontier-v3',receipt_sha256=new_receipt_sha256,ordinal=summary['ordinal'],
                    record_sha256=summary['record_sha256'],certificate_sha256=summary['certificate_sha256'])
                selected.append(dict(root=root,authority=authority));row.update(production_status='REQUESTED_FRESH_CLASSIFICATION',authority=authority)
            else:
                require(summary['blocker_codes'],'negative new root has no explicit blocker')
                row.update(production_status='NEW_ORIGINAL_OMISSION_BLOCKED',new_observation=summary)
        elif state=='PRESERVED_REFERENCE_GROUP_QUARANTINE':
            require(item['root']['original_address']=='0x0086beb0','unknown preserved quarantine')
        else:require(state in ('CACHED_ORIGINAL_OMISSION_BLOCKED','PREPARED_SKIP','UNSELECTED_OR_NAMESPACE_UNPROVED'),
            'new wave cannot silently route unsupported cached-positive/unknown states')
        ledger.append(row)
    selected.sort(key=lambda r:r['root']['original_address'])
    require(len(selected)==len({s['root']['original_address'] for s in selected})==sum(s['closure_observed'] is True for s in singles.values()),
        'complete unique positive subset differs')
    return dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=[r['root'] for r in selected]),selected,ledger


def spool_new_contexts(out,receipt,details,selected,inputs,start,*,expected_receipt_sha256):
    missing_count=receipt['summary']['roots']
    require(type(missing_count) is int and missing_count>0,'exact finite missing-root census')
    wanted={r['root']['original_address']:r for r in selected};require(len(wanted)==len(selected),'duplicate full selection')
    indices={};path=out/'contexts.bin';seen=set();summaries=receipt['observations'];count=0
    expected={r['roots'][0] for r in summaries if r['event']=='SINGLE_ROOT_OBSERVATION' and len(r['roots'])==1}
    require(len(expected)==receipt['summary']['roots']==missing_count and set(wanted)<=expected,'whole missing-only receipt scope')
    positive={r['roots'][0] for r in summaries if r['event']=='SINGLE_ROOT_OBSERVATION' and len(r['roots'])==1 and r['closure_observed'] is True}
    require(set(wanted)==positive,'new-only spool must contain the entire positive subset')
    require(isinstance(expected_receipt_sha256,str) and re.fullmatch('[0-9a-f]{64}',expected_receipt_sha256),'operation-bound receipt hash required')
    for selection in selected:
        authority=selection['authority'];ordinal=authority['ordinal']
        require(authority['kind']=='new-frontier-v3' and authority['receipt_sha256']==expected_receipt_sha256 and
            type(ordinal) is int and 0<ordinal<=len(summaries),'borrowed new-only selected authority')
        summary=summaries[ordinal-1]
        require(summary['ordinal']==ordinal and summary['event']=='SINGLE_ROOT_OBSERVATION' and summary['roots']==[selection['root']['original_address']] and
            summary['record_sha256']==authority['record_sha256'] and summary['certificate_sha256']==authority['certificate_sha256'],
            'selected new-only source locator differs')
    with path.open('xb') as stream,gzip.open(details,'rt') as source:
        for line in source:
            count+=1;require(count<=len(summaries) and len(line)<=64*1024**2,'new-only source row bound')
            row=json.loads(line);summary=summaries[count-1]
            require(summary['ordinal']==count and digest(row)==summary['record_sha256'] and row['event']==summary['event'] and
                row['recipe_id']==summary['recipe_id'] and [r['original_address'] for r in row['requested_roots']]==summary['roots'] and
                row['closure_observed']==summary['closure_observed'] and row['graph_observation_complete']==summary['graph_observation_complete'],
                'new-only source row/authority differs')
            if row['event']=='SINGLE_ROOT_OBSERVATION':
                a=row['requested_roots'][0]['original_address'];require(a not in seen,'duplicate new source singleton');seen.add(a)
                if a in wanted:
                    require(wanted[a]['authority']['ordinal']==count,'selected new locator differs')
                    indices[a]=frozen.write_context(stream,row,wanted[a])
            base.budget(start,out)
        require(count==len(summaries) and seen==expected and set(indices)==set(wanted),
            'whole new-source scope or selected spool incomplete')
        stream.flush();os.fsync(stream.fileno())
    base.save_json(out/'contexts-index.json',indices)
    return path,indices



def field_proof_record(member,row,selection,projection,output):
    """Full source evidence, copied without enrichment and bound to output fields."""
    root=selection['root'];fields=row['contract']['fields']
    require(row['requested_roots']==projection['requested_roots']==[root] and
        isinstance(output,bytes) and base.coff.digest(output)==projection['output_sha256'] and
        digest(projection['authority'])==digest(selection['authority']) and
        digest(row)==selection['authority']['record_sha256']==projection['central_record_sha256'] and
        digest(row['contract'])==row['contract_identity_sha256']==projection['contract_identity_sha256']==row['certificate']['contract_identity_sha256'] and
        digest(row['certificate'])==row['certificate_sha256']==selection['authority']['certificate_sha256']==projection['certificate_sha256'] and
        root['object_sha256']==projection['original_object_sha256']==row['contract']['provenance']['object_sha256'] and
        root['source_sha256']==row['contract']['provenance']['source_sha256'] and root['recipe_id']==row['contract']['recipe_id'],
        'full proof ledger source/root/authority differs')
    source_hashes=[digest(field) for field in fields]
    require(len(set(source_hashes))==len(source_hashes) and
        source_hashes==[field['field_proof_sha256'] for field in projection['fields']],
        'full proof ledger and projected physical fields differ')
    return dict(schema_version=1,member=member,requested_root=root,authority=selection['authority'],
        central_record_sha256=digest(row),contract_identity_sha256=row['contract_identity_sha256'],
        certificate_sha256=row['certificate_sha256'],output_object_sha256=projection['output_sha256'],
        fields_sha256=digest(fields),fields=fields,source_evidence_enriched=False)


OWNED=('tools/rebuild/frontier_wave_factory_v8.py','tests/rebuild/test_frontier_wave_factory_v8.py','docs/rebuild/FRONTIER-WAVE-FACTORY-V8.md')
PINS={**wave.PINS,'tools/rebuild/code_frontier_wave_v8.py':'95757fdb00820ef1bcb03bf9b5dc561cd8700f50ddf7bc196c14561a6d23cc51',
    'tools/rebuild/frontier_root_collect_v3.py':'b03bb96c147ba4233832ad539bcc60bc7478fc1cc0038965c8c9f587cb688bce'}
SOURCES={
 'wave_receipt':('code-frontier-wave-v8-v1/receipt.json','4371d49abf83a5478110fff73e0a609ec3641113a5068e75e61df5ea44a73d1e'),
 'epoch':('code-frontier-wave-v8-v1/prepared-epoch.json','714d970200b9333293a7e643c6f2b7a78b2829cbe7cb0b021bd0ee9515d5749b'),
 'registry':('code-frontier-wave-v8-v1/cache-registry.json','7c11ea72a7375cadf79771c8a1aa9f02f554e062e811ec9e852042df9aca67df'),
 'frontier':('code-frontier-wave-v8-v1/frontier.json','b7ef2d261f8a25571495e541a2cd77ecdae40ed1d0879257171c794777a2182f'),
 'wave_review':('code-lane-02/v8-wave-outcome-review-v1.json','b4b4369eaa2535c77032cec29913e0d78aa6dedbe208eb1ed23cb4e2eee3920b'),
 'wave_authority_review':('code-lane05-synthetic-projection-v1/code-frontier-wave-v8-saved-authority-outcome-review-v1.json','0bb5a1cc36f2134bc98619aff9a73ecc36e79025c2c162fb33b6c745dbf7c777'),
 'new_receipt':('frontier-code-root-observation-v3/receipt.json','6eec875919603cd9cd3ce9bea7a34b82596f55dea95bc6253b6811aa08cd35ab'),
 'new_details':('frontier-code-root-observation-v3/observations.jsonl.gz','b7d007e4dfd7218bd7f8b0e6117b2cb5618f646da52415e954bb5d294911d2ca'),
 'new_review':('frontier-code-root-observation-v3/independent-outcome-review.json','49b35751bc9135e606695d83fc79cabe68d9ca9578750f829234ea10aa19ebbc')}


def review_gate(args,inputs):
    review=base.load_json(base.observe(args.review,args.review_sha256,inputs))
    require(review.get('kind')=='V8-new-only-CODE-factory-review-v1' and review.get('schema_version')==1 and
        review.get('approved') is True and review.get('independent_source_schema_review_pass') is True and
        review.get('root_authorized') is True and review.get('reviewer') and review.get('all_positive_new_roots_required') is True and
        review.get('operation_sha256')==args.operation_sha256 and review.get('producer_sha256')==PINS and
        review.get('source_artifacts')=={k:h for k,(_,h) in SOURCES.items()} and set(review.get('source_sha256',{}))==set(OWNED) and
        review.get('allow_native_tools') is False and review.get('allow_game_execution') is False,'exact independent V8 source/input and finite authorization required')
    for rel,h in {**PINS,**review['source_sha256']}.items():base.observe(ROOT/rel,h,inputs)
    base.stable(inputs);return review


def run(args):
    start=time.monotonic();inputs={};review=review_gate(args,inputs)
    operation=base.load_json(base.observe(args.operation,args.operation_sha256,inputs))
    require(set(operation)=={'schema_version','kind','roots','output_relative','resource_limits'} and type(operation['schema_version']) is int and
        operation['schema_version']==1 and operation['kind']=='ALL-positive-new259-V8-CODE-production' and
        operation['resource_limits']==dict(seconds=900,peak_memory_bytes=1024**3,output_bytes=128*1024**2),'exact bounded V8 operation schema')
    paths={k:base.observe(ROOT/'build/rebuild'/rel,h,inputs) for k,(rel,h) in SOURCES.items()}
    wave_receipt=base.load_json(paths['wave_receipt']);epoch=base.load_json(paths['epoch']);registry=base.load_json(paths['registry']);frontier=base.load_json(paths['frontier'])
    require(wave_receipt['status']=='completed' and wave_receipt['input_stability'] is True and
        wave_receipt['artifacts']['prepared-epoch.json']==SOURCES['epoch'][1] and wave_receipt['artifacts']['cache-registry.json']==SOURCES['registry'][1] and
        wave_receipt['artifacts']['frontier.json']==SOURCES['frontier'][1],'accepted complete wave metadata differs')
    for p,h in wave_receipt['inputs'].items():base.observe(Path(p),h,inputs)
    new=base.load_json(paths['new_receipt'])
    require(new['cache_registry_sha256']==SOURCES['registry'][1] and new['frontier_join_sha256']==SOURCES['frontier'][1] and
        new['request_sha256']==wave_receipt['artifacts']['missing-request.json'] and new['planned_map_sha256']==frozen.fields.MAP_PIN and
        new['details_sha256']==SOURCES['new_details'][1] and new['collector_sha256']==PINS['tools/rebuild/frontier_root_collect_v3.py'] and
        new['cached_roots']==269 and new['cached_roots_reobserved']==0 and new['owner_stream_traversals']==0 and new['binding_stream_traversals']==1,
        'accepted new-only registry/native observation lineage differs')
    request,selected,ledger=select_new_contexts(frontier,registry,new,SOURCES['new_receipt'][1])
    require(operation['roots']==request['roots'] and len(selected)>0,'operation omits/substitutes supported complete positive subset')
    reports={n:base.load_json(base.observe(ROOT/'build/rebuild'/p,base.inventory.EXPECTED[n],inputs)) for n,p in
        [('selection','function-selection-v2.json'),('manifest','objects-20261103T030230Z-7cfc935c.json'),('retained','retained-verify-full-v3.json'),('owners','runtime-data-owners-native-v1.json')]}
    units={u['recipe_id']:u for u in reports['manifest']['units']};proofs={u['recipe_id']:u for u in reports['retained']['units']}
    require(len(units)==len(proofs)==2988 and len(reports['selection']['selections'])==68657,'full original source universe differs')
    recipes=base.observe(ROOT/'build/units.json',base.inventory.EXPECTED['recipes'],inputs)
    require(base.reconcile_recipes(reports['manifest'],recipes)['verified'],'original compiler/source variants differ')
    planned=base.load_json(base.observe(args.provider_map,frozen.fields.MAP_PIN,inputs))
    base.observe(ROOT/'build/rebuild'/frozen.fields.MAP_REVIEW[0],frozen.fields.MAP_REVIEW[1],inputs)
    providers=frozen.fields.validate_provider_map(planned,reports['selection']['selections'],units,proofs,reports['owners'])
    # Reconstruct current definitions with exact accepted member ledgers, never address aliases.
    rebuilt=wave.extend_epoch(base.load_json(ROOT/'build/rebuild'/wave.INPUTS['parent_epoch'][0]),planned['providers'],units,
        base.load_json(ROOT/'build/rebuild'/wave.INPUTS['members3'][0]))
    require(rebuilt==epoch,'complete prepared epoch reconstruction differs');exports=set(epoch['exclusion_names'])
    require(len(exports)==14409 and epoch['ordinary_prepared_count']==14403,'prepared epoch count differs')
    base.collector.validate_request(request,reports['selection']['selections'],reports['manifest'],reports['retained'],providers)
    wanted={r['original_address']:r for r in request['roots']};object_paths={};object_root=reports['manifest'].get('object_root_relative','.')
    for a,root in wanted.items():
        require(base.pool.canonical(providers[a]) not in exports,'prepared physical namespace cannot be replaced')
        u=units[root['recipe_id']];source=(ROOT/u['source']).resolve();obj=(ROOT/'build/rebuild'/object_root/u['object']).resolve()
        require(source.is_relative_to(ROOT) and obj.stat().st_size<=16*1024**2,'bounded original object/source input')
        base.observe(source,root['source_sha256'],inputs);base.observe(obj,root['object_sha256'],inputs);object_paths[a]=obj
    for rel,h in reports['retained']['inputs']['tools_sha256'].items():base.observe(ROOT/rel,h,inputs)
    base.observe(ROOT/'build/image_check.json',reports['retained']['inputs']['image_check_sha256'],inputs)
    reference=base.observe(args.reference,base.pool.PINS['reference'],inputs)
    coverage_source=base.observe(ROOT/'build/rebuild'/frozen.fields.ARTIFACTS['baseline_coverage'][0],frozen.fields.ARTIFACTS['baseline_coverage'][1],inputs)
    out=Path(args.out).resolve();private=(ROOT/'build/rebuild').resolve()
    require(out==(ROOT/operation['output_relative']).resolve() and out.is_relative_to(private) and out!=private and not out.exists() and
        not any(p.is_relative_to(out) for p in inputs),'exact new exclusive private V8 output required')
    del planned,reports,proofs,rebuilt,registry,wave_receipt
    base.stable(inputs);out.mkdir();journal=(out/'progress.jsonl').open('x',encoding='utf-8')
    def note(state,**facts):journal.write(json.dumps(dict(state=state,elapsed_seconds=round(time.monotonic()-start,3),**facts))+'\n');journal.flush();os.fsync(journal.fileno())
    members=[];receipts=[];blocked=[];emitted=[];assessments=[];metadata=None;proof_raw=None;proof_stream=None
    try:
        note('started',all_positive_new_roots=len(selected),new_observed_roots=259,cached_contexts_reloaded=0)
        for rel,h in review['source_sha256'].items():
            raw=(ROOT/rel).read_bytes();require(base.coff.digest(raw)==h,'source snapshot drift');p=out/'source-snapshots'/rel;p.parent.mkdir(parents=True,exist_ok=True);base.pool.fsynced(p,raw)
        spool,index=spool_new_contexts(out,new,paths['new_details'],selected,inputs,start,expected_receipt_sha256=SOURCES['new_receipt'][1])
        spool_hash,index_hash=frozen.protect_context_artifacts(spool,out/'contexts-index.json',index,inputs)
        note('new_only_contexts_spooled',contexts=len(index),spool_sha256=spool_hash,index_sha256=index_hash)
        del new
        sys.path.insert(0,str(ROOT/'tools'));import compare as oracle
        from build_and_match import image_ok
        pe=base.checked_reference(reference,oracle,image_ok);metadata=wave.prior.planner.typed.SnapshotPe(reference,pe)
        highlow={metadata.base+rva for rva in metadata.relocations()};require(len(highlow)==351931,'fresh original HIGHLOW count differs')
        proof_raw=(out/'field-proofs.jsonl.gz').open('xb')
        proof_stream=gzip.GzipFile(fileobj=proof_raw,mode='wb',mtime=0)
        facts={};audited=0
        with spool.open('rb') as stream:
            for selection in selected:
                base.budget(start,out);root=selection['root'];a=root['original_address'];row=frozen.read_context(stream,index[a],selection)
                contract=row['contract'];certificate=row['certificate']
                for rel,h in contract['provenance']['dependency_tools_sha256'].items():
                    path=(ROOT/rel).resolve();require(path.is_relative_to(ROOT/'tools'),'foreign observer dependency');base.observe(path,h,inputs)
                raw=object_paths[a].read_bytes();require(base.coff.digest(raw)==root['object_sha256'],'fresh original object drift')
                for site,fact in wave.prior.planner.typed.audit_original_fields(metadata,highlow,contract['fields']).items():
                    require(site not in facts or facts[site]==fact,'contradictory original field facts');facts[site]=fact
                audited+=len(contract['fields'])
                assessment=None
                if contract['fields']:
                    assessment=frozen.fields.core.assess_member(raw,contract,certificate,[root],providers,existing_exports=exports)
                    assessments.append(dict(original_address=a,assessment=assessment))
                    if assessment['eligible'] is not True:
                        require(assessment['blockers'],'unsupported field policy has no blocker');blocked.append(dict(root=root,blockers=assessment['blockers'],fresh_body_compared=False));continue
                name='V8-%03d-%s.obj'%(len(members),a[2:]);path=out/name
                output,projection=frozen.verify_candidate(raw,row,root,providers,exports,object_paths[a],path,pe,units[root['recipe_id']]['recipe'])
                if assessment is not None:require(projection['fields']==assessment['fields'] and projection['exports']==assessment['exports'],'fresh field assessment changed')
                else:assessments.append(dict(original_address=a,strict_zero_consumer_replayed=True,serialization_performed=True))
                projection.update(authority=selection['authority'],central_record_sha256=digest(row))
                proof=field_proof_record(name,row,selection,projection,output)
                proof_stream.write((json.dumps(proof,sort_keys=True,separators=(',',':'))+'\n').encode())
                members.append((name,output));receipts.append(dict(name=name,projection=projection));emitted.append(a)
                note('member_verified',original_address=a,fields=len(projection['fields']),member_sha256=base.coff.digest(output))
        proof_stream.close();proof_stream=None;proof_raw.flush();os.fsync(proof_raw.fileno());proof_raw.close();proof_raw=None
        metadata.close();metadata=None
        require(base.file_hash(spool)==spool_hash and base.file_hash(out/'contexts-index.json')==index_hash,'sealed context drift')
        archive_hash=None
        if members:
            archive=base.coff.archive(members);base.pool.fsynced(out/'V8-code.lib',archive);recovered=base.coff.read_archive(archive)
            require(recovered['members']==members and len(recovered['index'])==len(emitted),'archive defined exports/member identities differ')
            for name,data in recovered['members']:
                p=out/('recovered-'+name);base.pool.fsynced(p,data);base.bulk.strict_reparse(p,data)
            archive_hash=base.coff.digest(archive)
        quarantine={b['root']['original_address']:b['blockers'] for b in blocked}
        for item in ledger:
            if item['production_status']=='REQUESTED_FRESH_CLASSIFICATION':
                a=item['root']['original_address'];require(a in emitted or a in quarantine,'requested root lacks terminal status')
                item['production_status']='EMITTED' if a in emitted else 'QUARANTINED_UNSUPPORTED_POLICY'
                if a in quarantine:item['production_blockers']=quarantine[a]
        coverage=frozen.write_coverage(out/'coverage.jsonl.gz',coverage_source,providers,exports,frontier,set(wanted),set(emitted))
        for name,value in [('members',receipts),('blocked',blocked),('assessments',assessments),('frontier-ledger',ledger)]:base.save_json(out/(name+'.json'),value)
        base.save_json(out/'original-field-audit.json',dict(highlow_sites=len(highlow),retained_fields=audited,unique_field_sites=len(facts),
            field_facts_sha256=digest(sorted(facts.items())),loaded_reference_sha256=base.coff.digest(pe.data),original_highlow_authority_authenticated=True))
        base.stable(inputs)
        result=dict(schema_version=1,policy_id=POLICY,status='completed' if len(emitted)==len(selected) else 'completed-incomplete',
            operation_sha256=args.operation_sha256,review_sha256=args.review_sha256,requested=len(selected),emitted=len(emitted),blocked=len(blocked),
            emitted_addresses=emitted,archive_sha256=archive_hash,prepared_exclusion_count=14409,ordinary_prepared_upstream_count=14403,
            new_original_observations=259,cache_roots=269,cached_context_body_reads=0,whole_frontier_demands=467,
            final_frontier_counts=dict(Counter(r['production_status'] for r in ledger)),
            full_field_proof_schema_version=1,full_field_proof_records=len(receipts),full_field_proof_rows=sum(len(r['projection']['fields']) for r in receipts),
            source_field_evidence_enriched=False,fields=sum(len(r['projection']['fields']) for r in receipts),code_bytes=sum(r['projection']['requested_roots'][0]['size'] for r in receipts),
            context_spool_sha256=spool_hash,context_index_sha256=index_hash,derived_context_inputs_protected=2,
            output_sha256={n:base.file_hash(out/n) for n in ('members.json','blocked.json','assessments.json','frontier-ledger.json','coverage.jsonl.gz','original-field-audit.json','field-proofs.jsonl.gz')},
            historical_owners=68657,coverage_counts=coverage,inputs={str(p):h for p,h in inputs.items()},inputs_stable=True,
            optional_function_index_present=False,native_archive_conformance_verified=False,resource_observations=base.budget(start,out),resource_limits=operation['resource_limits'],**FALSE)
        return base.finalize_success(out,result,inputs,start,journal,note)
    except BaseException as error:
        try:
            if not journal.closed:note('failed',error_type=type(error).__name__,message=str(error),completed_members=len(emitted))
        except OSError:pass
        base.save_json(out/'abort.json',dict(status='aborted-no-retry',error_type=type(error).__name__,message=str(error),completed_members=emitted,successful_projection=False,**FALSE));raise
    finally:
        if proof_stream is not None:proof_stream.close()
        if proof_raw is not None:proof_raw.close()
        if metadata is not None:metadata.close()
        if not journal.closed:journal.close()


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('operation','review','provider-map','reference','out'):parser.add_argument('--'+name,required=True,type=Path,dest=name.replace('-','_'))
    for name in ('operation','review'):parser.add_argument('--'+name+'-sha256',required=True,dest=name+'_sha256')
    args=parser.parse_args(argv)
    try:result=run(args)
    except (ValueError,OSError,KeyError,TypeError) as error:parser.exit(2,'V8 wave rejected: '+str(error)+'\n')
    print(json.dumps({k:result[k] for k in ('status','requested','emitted','blocked','fields','archive_sha256')}));return 0 if result['status']=='completed' else 3


if __name__=='__main__':raise SystemExit(main())
