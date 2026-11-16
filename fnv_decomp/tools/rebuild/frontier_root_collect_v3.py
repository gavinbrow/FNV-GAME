"""Observe V8's finite new roots using a distinct-authority cached registry.

Cached roots are rejected, not replayed. The accepted compact physical map
replaces an owner-stream scan; one binding pass hydrates new recipe contracts.
"""
from __future__ import annotations
import argparse
from collections import Counter
import gzip
import json
import os
from pathlib import Path
import re
import tempfile
import time

import centralordinary_root_collect as central
import scalableordinary_root_collect as finite
from scalableordinary_root_collect import (ROOT, EXPECTED, IMPORT_PIN, ORDINARY_PIN, PARSER_PIN,
    INVENTORY_PIN, FALSE, ordinary, canonical, digest, file_hash, read_bound, pin, stable,
    validate_headers, reconcile_recipes, BindingReader)

POLICY = 'new-frontier-ordinary-root-observation-v3'
CENTRAL_PIN = '97c827795e46c6d1e6558f6e785266b4e908ddb4c5cf253ec61a71ef19d51409'
FINITE_PIN = 'e7e5b45df15af0a2bd5cb4a65b36d85ca21eb753656714c0a9a5d8dd919e58ad'
MAP_PIN = '6cd5bf884bb28d460cfc92f63b765c15413904f58355844243ddd6b59b97001c'
REGISTRY_PIN = '7c11ea72a7375cadf79771c8a1aa9f02f554e062e811ec9e852042df9aca67df'
AUTHORITIES = [dict(kind='cached-central',receipt_sha256='290ac0e8c1ffbfd89df7dd6cdbbdb8df363edca58111b7aa19fe842aa26cc8e4',
    request_sha256='f778bdd8453d9813b978acbba7547e5733c585ebf5043b9769986bf8cf7e0665',roots=205),
    dict(kind='cached-frontier',receipt_sha256='ea4e02c8e62264f65662ed4c9d5fdd2e4d990bf9b6c3dd70b5e0553b61f43da5',
    request_sha256='c59c18a92d790c93b73136967338e75826e6c089ebebd7c7194c680aadee03a1',roots=10),
    dict(kind='cached-frontier',receipt_sha256='3afed5cd8a6728f0dbd7b8753fe5b3320524d1123dd68266bfb9fea22f00424a',
    request_sha256='7f30f61745419f31fcebf0fbea9124528810797473b04f03fb58bc6a1815bf26',roots=54)]
MAX_ROOTS = 259
MAX_OUTPUT = 128*1024**2
CONTEXT_KEYS = {'schema_version','kind','epoch','request_sha256','frontier_join_sha256',
    'planned_map_sha256','cache_registry_sha256','new_original_addresses',
    'provider_selected','runtime_eligible','emission_performed'}


def validate_registry(registry, selections=None, planned=None):
    ordinary.require(type(registry['schema_version']) is int and registry['schema_version']==1 and registry['kind']=='distinct-authority-original-root-registry' and
        registry['authorities']==AUTHORITIES and type(registry['roots']) is int and registry['roots']==269 and len(registry['records'])==269,
        'cached registry authority/count differs')
    ordinary.require(all(registry[k] is False for k in ('provider_selected','runtime_eligible','ABI_verified','link_ready',
        'materialization_approved','native_tools_run','code_emission_performed','compiler_performed','executable_link_performed',
        'game_execution_performed','original_image_read','original_objects_read','source_bodies_read')), 'cached registry promoted')
    counts=Counter(); physical=set()
    for address,row in registry['records'].items():
        root,authority,summary=row['root'],row['authority'],row['summary']
        ordinary.require(set(root)==finite.ROOT_KEYS and root['original_address']==address and
            all(type(root[k]) is int for k in ('recipe_index','section','value','size','symbol_index')) and
            root['section']>0 and root['value']>=0 and root['size']>0 and root['symbol_index']>=0,
            'cached physical root schema differs')
        matches=[a for a in AUTHORITIES if all(authority.get(k)==a[k] for k in ('kind','receipt_sha256','request_sha256'))]
        ordinary.require(len(matches)==1, 'cached root authority differs');counts[tuple(matches[0][k] for k in ('kind','receipt_sha256','request_sha256'))]+=1
        ordinary.require(summary['event']=='SINGLE_ROOT_OBSERVATION' and summary['roots']==[address] and
            summary['recipe_id']==root['recipe_id'] and type(summary['closure_observed']) is bool and
            type(summary['graph_observation_complete']) is bool and
            authority['record_sha256']==summary['record_sha256'] and authority['certificate_sha256']==summary['certificate_sha256'],
            'cached summary/authority identity differs')
        ordinary.require(not summary['closure_observed'] or summary['graph_observation_complete'], 'cached positive has incomplete graph')
        ordinary.require(all(isinstance(authority[k],str) and re.fullmatch('[0-9a-f]{64}',authority[k]) for k in ('record_sha256','certificate_sha256')) and
            authority['contract_identity_sha256'] is None and authority['contract_identity_is_bound_through_record_hash'] is True,
            'cached contract identity must remain deferred through exact record hash')
        key=(root['recipe_id'],root['object_sha256'],root['symbol_index'])
        ordinary.require(key not in physical, 'duplicate cached physical identity');physical.add(key)
        if selections is not None:
            choice=selections[address];p=planned['providers'][address]
            expected=dict(original_address=address,recipe_id=p['recipe_id'],recipe_index=choice['recipe_index'],object_sha256=p['object_sha256'],
                source_sha256=p['source_sha256'],symbol=choice['symbol'],symbol_index=p['symbol_index'],section=choice['section'],value=choice['value'],size=choice['size'])
            ordinary.require(root==expected, 'cached physical identity differs from selected planned namespace')
    ordinary.require(dict(counts)=={tuple(a[k] for k in ('kind','receipt_sha256','request_sha256')):a['roots'] for a in AUTHORITIES}, 'cached authority coverage differs')
    return set(registry['records'])


def validate_context(context, request, registry, request_hash, frontier_hash):
    ordinary.require(type(context) is dict and set(context) == CONTEXT_KEYS and
        type(context['schema_version']) is int and context['schema_version'] == 3 and
        context['kind'] == 'new-original-frontier-root-context-v3', 'unknown frontier context')
    ordinary.require(type(context['epoch']) is str and 0 < len(context['epoch']) <= 100 and
        context['epoch'].isascii(), 'explicit frontier epoch required')
    ordinary.require(context['request_sha256'] == request_hash and context['frontier_join_sha256'] == frontier_hash and
        context['planned_map_sha256'] == MAP_PIN and context['cache_registry_sha256'] == REGISTRY_PIN and
        all(context[k] is False for k in ('provider_selected','runtime_eligible','emission_performed')), 'frontier lineage/promotion differs')
    ordinary.require(set(request) == {'schema_version','kind','roots'} and type(request['schema_version']) is int and request['schema_version'] == 1 and
        request['kind'] == 'fnv-finite-ordinary-root-request' and 0 < len(request['roots']) <= MAX_ROOTS,
        'bounded finite new-root request required')
    addresses = [r['original_address'] for r in request['roots']]
    ordinary.require(context['new_original_addresses'] == addresses and len(set(addresses)) == len(addresses),
        'new-root scope differs')
    previous = validate_registry(registry)
    ordinary.require(not previous.intersection(addresses), 'cached roots must not be recollected')
    return context['epoch']


def map_identities(planned, selections):
    ordinary.require(planned['policy_id'] == 'selected-physical-provider-map-v1' and
        planned['kind'] == 'typed-provider-map' and planned['census']['selected_owners'] == 68657 and
        planned['materialized_exports'] == 0 and planned['provider_identity_is_planned_namespace'] is True and
        planned['input_stability'] is True and planned['optional_function_index_present'] is False and
        all(planned[k] is False for k in (*FALSE,'materialization_approved','native_tools_run')) and
        set(planned['providers']) == set(selections), 'planned map scope/promotion differs')
    return {a:{k:r[k] for k in ('recipe_id','object_sha256','symbol_index')} for a,r in planned['providers'].items()}


def summary_row(record, ordinal):
    return dict(ordinal=ordinal,event=record['event'],recipe_id=record['recipe_id'],
        roots=[r['original_address'] for r in record['requested_roots']],record_sha256=digest(record),
        certificate_sha256=record.get('certificate_sha256'),closure_observed=record['closure_observed'],
        graph_observation_complete=record['graph_observation_complete'],
        blocker_codes=dict(Counter(b['code'] for b in record['blockers'])))


def run(args):
    started = time.monotonic(); pins = dict(EXPECTED, imports=IMPORT_PIN)
    paths = {n:Path(getattr(args,n)).resolve() for n in pins}
    data = {n:read_bound(paths[n],h) for n,h in pins.items()}; validate_headers(data)
    manifest, proof, selection, binding, imports = [data[n] for n in ('manifest','retained','selection','binding','imports')]
    ordinary.require(reconcile_recipes(manifest,paths['recipes'])['verified'], 'recipe epoch differs')
    extra = {n:Path(getattr(args,n)).resolve() for n in ('request','context','frontier_join','planned_map','registry')}
    hashes = dict(request=args.request_sha256,context=args.context_sha256,frontier_join=args.frontier_join_sha256,
                  planned_map=MAP_PIN,registry=REGISTRY_PIN)
    loaded = {n:read_bound(p,hashes[n]) for n,p in extra.items()}
    epoch = validate_context(loaded['context'],loaded['request'],loaded['registry'],hashes['request'],hashes['frontier_join'])
    providers = map_identities(loaded['planned_map'],selection['selections'])
    validate_registry(loaded['registry'],selection['selections'],loaded['planned_map'])
    groups = finite.validate_request(loaded['request'],selection['selections'],manifest,proof,providers)
    observations = {paths[n]:h for n,h in pins.items()}
    for n,p in extra.items(): pin(p,hashes[n],observations)
    detail_in = Path(args.binding_details).resolve(); pin(detail_in,binding['details_sha256'],observations)
    fixed = {'root_code_closure.py':ORDINARY_PIN,'coff_code_archive.py':PARSER_PIN,
             'runtime_code_inventory.py':INVENTORY_PIN,'centralordinary_root_collect.py':CENTRAL_PIN,
             'scalableordinary_root_collect.py':FINITE_PIN}
    for name,h in fixed.items(): pin(ROOT/'tools/rebuild'/name,h,observations)
    ordinary.require(Path(central.__file__).resolve()==ROOT/'tools/rebuild/centralordinary_root_collect.py' and
        Path(finite.__file__).resolve()==ROOT/'tools/rebuild/scalableordinary_root_collect.py' and
        Path(ordinary.__file__).resolve()==ROOT/'tools/rebuild/root_code_closure.py', 'swapped collector modules')
    for name in ('frontier_root_collect_v3.py','runtime_gaps.py','data_plan.py','import_plan.py','coff_inventory.py'):
        p=ROOT/'tools/rebuild'/name;pin(p,file_hash(p),observations)
    for name,h in proof['inputs']['tools_sha256'].items():
        p=(ROOT/name).resolve();ordinary.require(p.is_relative_to(ROOT),'foreign proof dependency');pin(p,h,observations)
    proofs={u['recipe_index']:u for u in proof['units']}; reserved=set(observations)
    for unit in manifest['units']:
        obj=(paths['manifest'].parent/manifest.get('object_root_relative','.')/unit['object']).resolve()
        src=(ROOT/unit['source']).resolve();reserved.update((obj,src))
        if unit['recipe_index'] in groups:
            ordinary.require(src.is_relative_to(ROOT),'foreign source');pin(src,unit['source_sha256'],observations)
            observations[obj]=unit['object_sha256']
    out,details,progress=finite.output_paths(args.out,args.details,reserved|set(observations))
    index=ROOT/'build/function_index.json';ordinary.require(not index.exists(),'optional index appeared')
    progress.parent.mkdir(parents=True,exist_ok=True);published=[]
    with progress.open('x',encoding='utf-8') as journal:
        def note(v):
            journal.write(json.dumps(dict(elapsed_seconds=round(time.monotonic()-started,3),**v))+'\n')
            journal.flush();os.fsync(journal.fileno())
        note(dict(state='started',epoch=epoch,roots=len(loaded['request']['roots']),recipes=len(groups),pid=os.getpid()))
        try:
            summaries=[];events=Counter();seen=set();parsed=0
            imported=next((r for r in imports['imports'] if r['import_id']==175),None)
            ordinary.require(imported is not None and imports['inputs']['manifest']==pins['manifest'] and
                imports['inputs']['retained']==pins['retained'] and imports['inputs']['reference']==proof['inputs']['image_sha256'], 'imports epoch differs')
            with tempfile.TemporaryFile() as stage:
                with gzip.GzipFile(fileobj=stage,mode='wb',mtime=0) as writer:
                    with gzip.open(detail_in,'rt',encoding='utf-8') as stream:
                        reader=BindingReader(stream,binding['summary'],selection['selections'])
                        for unit in manifest['units']:
                            bucket=reader.take(unit['recipe_index']); ri=unit['recipe_index']
                            if ri not in groups: continue
                            central.check_budget(started); pv=proofs[ri]
                            provenance=dict(object_sha256=unit['object_sha256'],source_sha256=unit['source_sha256'],recipe_id=unit['recipe_id'],recipe_index=ri,
                                recipe_unit_sha256=pv['recipe_unit_sha256'],recipe_manifest_sha256=pins['recipes'],producer_manifest_sha256=pins['manifest'],
                                retained_proof_sha256=pins['retained'],selection_sha256=pins['selection'],binding_sha256=pins['binding'],
                                binding_details_sha256=binding['details_sha256'],imports_sha256=IMPORT_PIN,reference_identity_sha256=proof['inputs']['image_sha256'],
                                request_sha256=hashes['request'],context_sha256=hashes['context'],frontier_join_sha256=hashes['frontier_join'],
                                authority_kind='new-frontier-v3',cache_registry_sha256=REGISTRY_PIN,prior_authorities=AUTHORITIES,planned_map_sha256=MAP_PIN,observation_epoch=epoch,original_native_epoch='retained-full-v3',
                                source_relative=unit['source'],producer_compiler_variant=unit['compiler'],optional_function_index_present=False,
                                collector_sha256=file_hash(__file__),observer_sha256=ORDINARY_PIN,parser_sha256=PARSER_PIN,
                                dependency_tools_sha256={p.relative_to(ROOT).as_posix():h for p,h in observations.items() if p.is_relative_to(ROOT/'tools')})
                            native=(paths['manifest'].parent/manifest.get('object_root_relative','.')/unit['object']).resolve()
                            for record in central.observe_recipe(native.read_bytes(),unit,pv,groups[ri],bucket,imported,provenance,started):
                                writer.write(canonical(record)+b'\n');events[record['event']]+=1
                                summaries.append(summary_row(record,len(summaries)+1))
                                if record['event']=='SINGLE_ROOT_OBSERVATION':
                                    a=record['requested_roots'][0]['original_address'];ordinary.require(a not in seen,'duplicate new root');seen.add(a)
                            parsed+=1;note(dict(state='observed_new_recipe_once',recipe_id=unit['recipe_id'],roots=len(groups[ri])))
                        census=reader.finish()
                size=stage.seek(0,2);ordinary.require(size<=MAX_OUTPUT,'new frontier detail bound')
                ordinary.require(seen==set(loaded['context']['new_original_addresses']) and parsed==len(groups),'incomplete new-root accounting')
                stable(observations);ordinary.require(not index.exists(),'optional index appeared');stage.seek(0)
                details.parent.mkdir(parents=True,exist_ok=True)
                with details.open('xb') as target:
                    published.append(details)
                    while block:=stage.read(1048576):target.write(block)
                    target.flush();os.fsync(target.fileno())
            summary=dict(roots=len(seen),recipes=parsed,events=dict(events),
                singleton_closure=sum(r['closure_observed'] for r in summaries if r['event']=='SINGLE_ROOT_OBSERVATION'),
                singleton_blocked=sum(not r['closure_observed'] for r in summaries if r['event']=='SINGLE_ROOT_OBSERVATION'))
            result=dict(schema_version=1,policy_id=POLICY,status='metadata-only',epoch=epoch,original_native_epoch='retained-full-v3',
                inputs=pins,context_sha256=hashes['context'],request_sha256=hashes['request'],frontier_join_sha256=hashes['frontier_join'],
                authority_kind='new-frontier-v3',cache_registry_sha256=REGISTRY_PIN,prior_authorities=AUTHORITIES,cached_roots=269,planned_map_sha256=MAP_PIN,details_sha256=file_hash(details),details_bytes=size,
                observations=summaries,summary=summary,baseline_binding_census=census,owner_stream_traversals=0,
                binding_stream_traversals=1,cached_roots_reobserved=0,collector_sha256=file_hash(__file__),
                input_stability=True,optional_function_index_present=False,game_fixups_approved=0,**FALSE)
            ordinary.require(len(canonical(result))+size<=MAX_OUTPUT,'final output bound')
            finite.publish_summary(out,result,observations,index,published)
            central.check_budget(started)
            note(dict(state='complete',summary_sha256=file_hash(out),details_sha256=result['details_sha256'],summary=summary))
            return result
        except BaseException as error:
            for p in published:p.unlink(missing_ok=True)
            note(dict(state='failed',error_type=type(error).__name__));raise


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    for name in tuple(EXPECTED)+('imports','request','context','frontier_join','planned_map','registry','binding_details','out','details'):
        p.add_argument('--'+name.replace('_','-'),dest=name,type=Path,required=True)
    for name in ('request','context','frontier_join'):p.add_argument('--'+name.replace('_','-')+'-sha256',dest=name+'_sha256',required=True)
    args=p.parse_args(argv)
    try:r=run(args)
    except (ValueError,OSError,KeyError,TypeError) as error:p.exit(2,'frontier collection rejected: '+str(error)+'\n')
    print(json.dumps(r['summary']));return 0


if __name__=='__main__':raise SystemExit(main())
