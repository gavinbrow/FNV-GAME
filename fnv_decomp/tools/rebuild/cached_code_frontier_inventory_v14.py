"""V14 saved CODE metadata inventory; no certificate or admission is created."""
from __future__ import annotations
import argparse
from collections import Counter
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import time

import cached_code_frontier_inventory_v13 as previous
import cached_root_observe_v13 as native
import types

base=previous.base
seam=previous.seam
historical=previous.historical
planner=previous.planner
provider_validator=previous.provider_validator
ROOT=previous.ROOT
require=previous.require
digest=previous.digest
exact=previous.exact
sha=previous.sha
FALSE=previous.FALSE
LIMITS=previous.LIMITS
POLICY='cached-CODE-frontier-inventory-v14'
OWNED=('tools/rebuild/cached_code_frontier_inventory_v14.py','tests/rebuild/test_cached_code_frontier_inventory_v14.py',
       'docs/rebuild/CACHED-CODE-FRONTIER-INVENTORY-V14.md')
PINS={**previous.PINS,
 'tools/rebuild/cached_code_frontier_inventory_v13.py':'cc9c228fd93fcd9147c1e61a66e7917c05d21cdee33e67dfed6cf22fb4de41d0',
 'tools/rebuild/cached_root_observe_v13.py':'05489b372585fac5f615548b53232bf30b7e28e5494ed914cc4e9972eb69deb4',
 'tools/rebuild/prepared_cached_v13_successor.py':'ccf6dfdf474d0e07cb161ab5c8e3206a512412e720daacfdf869ee5f05c290b0'}
AUTHORITY_PINS=previous.AUTHORITY_PINS
NATIVE_RECEIPT='846087b14800e313181064f5a897c110f8d07cc261c89e8b2730a75ad04efc08'
QUALIFIED_REQUEST='fdfcd3773c0b3e50fa7cc9ec63982556825fb9e4eab2a9d0e77f30b429ea32c4'


def bind_successor():
    """Verify the exact public pure constructor bytes before compiling them."""
    path=ROOT/'tools/rebuild/prepared_cached_v13_successor.py'
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!='ccf6dfdf474d0e07cb161ab5c8e3206a512412e720daacfdf869ee5f05c290b0':
        raise ValueError('fixed pure successor source changed')
    module=types.ModuleType('prepared_cached_v13_successor_frozen_ccf6')
    module.__file__=str(path)
    exec(compile(raw,str(path),'exec'),module.__dict__)
    return module


successor=bind_successor()
KNOWN={**previous.KNOWN}
KNOWN.update(groups='1a88328d4dbde77be1fb571fd4d87439857d14b43472e0ece8eec4e8e3d9c94d',
 link_review='9e107134eb10c39ee7a768975f627ae64cf28d3d07f3e47dbf260d888eaf573d',
 link_delta='a1dd8daed71150484ba677f4f19b539e42dfbd94ce0a749a6eebc8fb7bc7cff2',
 crt_primary_review='c2c5bf48ecbb74efb404fc1e1cf7305fda996433e52f844312179657a1b63eaa',
 crt_main_join_review='8b5c41573238edefaf4e51947b8c094725a90d6b69949158f8fdb6d662a0752e',
 prepared_epoch='2e8a762f851eae7cf133cc5228efdd145ab4b32e70a2872ab527a3f32e6e318c',
 prepared_review='095a5552bd594d5337f7f112d22f4e3b282dbf571dc9882244781d9a0fbc57dc',
 old_registry='3e4af440e1587e8eb4ebd24501fdcb8ee34acce11fa6438866c36c4a816f1968',
 native_receipt=NATIVE_RECEIPT,qualified_request=QUALIFIED_REQUEST,
 native_main_review='d1d8dda9053c4bf30e6d054c55abff5c53ec9d9d95936e4e9ea075850898d920',
 native_authority_review='d2bcc2c6e57cc69dd54023ea63ad44d548bdde1fd692d98efa7b808cb416425b',
 native_operation='5a15eaab95e65352716b0cb13cdce357af5417588455a6aa115e6bdf5a335dee',
 qualified_receipt='128933eb62f713a49c3fa26d501445ff39aacc7544ef70534071bc6ef3b5682e',
 successor_parent=successor.PARENT,successor_handoff=successor.HANDOFF,successor_handoff_review=successor.PEER,
 successor_members=successor.MEMBERS,successor_field_proofs=successor.PROOFS,
 successor_source_review='c7894b969b9ea452592b2d00097985d589f76e74caedf2682989f3f4d4b8d53a',
 old_registry_main_review='1e72158b99041d926ec82d8c5aea3f7ce24a72eba6cd211b5469e7ea17e92718',
 old_registry_authority_review='ac70782848c16e4e35911940d14967171e62f9fd516415ad6969daea6f927871')
DATA_SHA=previous.DATA_SHA
QUARANTINE_ADDRESSES=previous.QUARANTINE_ADDRESSES
metadata_features=previous.metadata_features
SelectedRangeGuard=previous.SelectedRangeGuard
BoundedSink=previous.BoundedSink
publish_inventory=previous.publish_inventory
save_bounded_json=previous.save_bounded_json
input_budget=previous.input_budget
load_ref=previous.load_ref
ref_path=previous.ref_path
validate_cache_receipt=previous.validate_cache_receipt


def validate_epoch(epoch,providers,units,*,expected=(14550,14556)):
    """Validate the accepted collision epoch without inventing application state."""
    ordinary,collision=expected
    require(epoch['kind']=='prepared-CODE-collision-exclusions' and
        all(type(epoch[k]) is int for k in ('ordinary_prepared_count','collision_exclusion_count')) and
        (epoch['ordinary_prepared_count'],epoch['collision_exclusion_count'])==expected and
        len(epoch['records'])==len(epoch['exclusion_names'])==len(set(epoch['exclusion_names']))==collision and
        len(epoch['ordinary_names'])==len(set(epoch['ordinary_names']))==ordinary,'accepted collision epoch census')
    require(epoch['application_selection_inferred_from_counts'] is False and epoch['application_selected_code_count'] is None and
        all(epoch[k] is False for k in FALSE) and
        ('application_manifest_adopted' not in epoch or epoch['application_manifest_adopted'] is False),'collision-only nonadmission epoch')
    names=set(epoch['exclusion_names']);onames=set(epoch['ordinary_names'])
    require({r['canonical'] for r in epoch['records']}==names and onames<=names and
        {r['canonical'] for r in epoch['records'] if r['category']=='ordinary'}==onames and
        Counter(r['category'] for r in epoch['records'])==Counter({'ordinary':ordinary,'application-candidate':collision-ordinary}),
        'epoch category and namespace census')
    for row in epoch['records']:
        require(base.pool.canonical(row['namespace_identity'])==row['canonical'],'epoch canonical identity')
    return copy.deepcopy(epoch)


def extend_registry(old,receipt,request,providers,units,*,expected_old=708,expected_new=72,expected_recipes=44):
    """Add fresh native summaries; qualification itself never had a certificate."""
    require(len(old['records'])==expected_old and request['kind']=='fnv-finite-ordinary-root-request' and
        type(request['schema_version']) is int and request['schema_version']==1 and len(request['roots'])==expected_new,'complete native qualified request')
    requested={r['original_address']:r for r in request['roots']}
    require(len(requested)==expected_new and len({r['recipe_id'] for r in requested.values()})==expected_recipes,'native request unique roots/recipes')
    for a,r in requested.items():
        require(set(r)==seam.ROOT_KEYS and all(type(r[k]) is int for k in ('recipe_index','symbol_index','section','value','size')) and
            exact(r,planner.root_record(a,providers[a],units)) and a not in old['records'],'native root source identity or old authority collision')
    require(type(receipt['schema_version']) is int and receipt['schema_version']==1 and receipt['policy_id']==native.POLICY and
        receipt['status']=='metadata-only' and receipt['operation_sha256']==KNOWN['native_operation'] and receipt['source_sha256']==PINS['tools/rebuild/cached_root_observe_v13.py'] and
        receipt['inputs']['qualified_request']['sha256']==QUALIFIED_REQUEST and receipt['qualified_contracts_preserved'] is True and
        receipt['input_stability'] is True and receipt['optional_function_index_present'] is False and
        all(receipt[k] is False for k in native.FALSE),'accepted fresh native authority envelope')
    require(all(type(receipt[k]) is int and receipt[k]==expected_recipes for k in ('native_object_observation_reads','native_object_parse_attempts')) and
        all(type(receipt[k]) is int and receipt[k]==0 for k in ('historical_roots_reobserved','original_binding_stream_traversals','owner_stream_traversals','cache_frame_reads')),
        'native once-only scope counters')
    summaries=receipt['observations'];require(len(summaries)==expected_new+expected_recipes,'all singleton and union summaries')
    records=copy.deepcopy(old['records']);singletons=set();unions=set();census=Counter({k:0 for k in ('singleton_closure','singleton_blocked','union_closure','union_blocked')})
    for ordinal,s in enumerate(summaries,1):
        require(type(s['ordinal']) is int and s['ordinal']==ordinal and type(s['qualified_record_ordinal']) is int and
            s['qualified_record_ordinal']==ordinal and type(s['recipe_index']) is int and
            s['recipe_id'] in units and s['recipe_index']==units[s['recipe_id']]['recipe_index'] and
            all(sha(s[k]) for k in ('record_sha256','qualified_metadata_row_sha256','contract_identity_sha256')) and
            (sha(s['certificate_sha256']) or (s['certificate_sha256'] is None and s['closure_observed'] is False)) and
            type(s['closure_observed']) is bool and type(s['graph_observation_complete']) is bool and
            type(s['blocker_codes']) is dict and all(type(v) is int and v>0 for v in s['blocker_codes'].values()) and
            ((s['closure_observed'] and s['graph_observation_complete'] and not s['blocker_codes']) or
             (not s['closure_observed'] and bool(s['blocker_codes']))),'native summary original hashes/ordinal/outcome')
        expected_roots={a for a,r in requested.items() if r['recipe_id']==s['recipe_id']}
        if s['event']=='SINGLE_ROOT_OBSERVATION':
            require(len(s['roots'])==1 and s['roots'][0] in expected_roots and s['roots'][0] not in singletons,'native singleton root census')
            a=s['roots'][0];singletons.add(a)
            authority=dict(kind='cached-native-v13',receipt_sha256=NATIVE_RECEIPT,request_sha256=QUALIFIED_REQUEST,ordinal=ordinal,
                record_sha256=s['record_sha256'],certificate_sha256=s['certificate_sha256'],contract_identity_sha256=s['contract_identity_sha256'],
                qualified_record_ordinal=s['qualified_record_ordinal'],qualified_metadata_row_sha256=s['qualified_metadata_row_sha256'],
                qualification_certificate_created=False,contract_identity_is_bound_through_record_hash=True)
            records[a]=dict(root=copy.deepcopy(requested[a]),summary=copy.deepcopy(s),authority=authority)
            census['singleton_closure' if s['closure_observed'] else 'singleton_blocked']+=1
        else:
            require(s['event']=='RECIPE_ROOT_UNION_OBSERVATION' and s['recipe_id'] not in unions and
                len(s['roots'])==len(set(s['roots'])) and set(s['roots'])==expected_roots,'native union full recipe scope')
            unions.add(s['recipe_id']);census['union_closure' if s['closure_observed'] else 'union_blocked']+=1
    expected_summary=dict(roots=expected_new,recipes=expected_recipes,records=len(summaries),**dict(census))
    require(singletons==set(requested) and len(unions)==expected_recipes and
        set(receipt['summary'])==set(expected_summary) and all(type(receipt['summary'][k]) is int and receipt['summary'][k]==v for k,v in expected_summary.items()),
        'native full finite summary reconciliation')
    return dict(schema_version=2,kind='cached-CODE-observation-authority-registry',records=records,roots=len(records),
        original_authorities=6,preserved_registry_roots=expected_old,new_native_singleton_authorities=expected_new,native_union_summaries_evidence_only=expected_recipes,
        historical_contract_digests_not_restamped=True,qualification_certificate_created=False,native_certificate_bodies_reloaded=False,
        native_authority_scope='accepted-receipt-summary-hashes-only',**FALSE)


def classify_demands(groups,providers,units,registry,exclusions,quarantines,*,expected_code_count=626,expected_quarantines=QUARANTINE_ADDRESSES):
    """Retain every original authority; hydrate only unprepared supported candidates."""
    old_records={a:r for a,r in registry['records'].items() if r['authority']['kind']!='cached-native-v13'}
    # Frozen validation authenticates the four historical authority schemas independently.
    empty=dict(kind='actual-unresolved-LNK-target-groups',executable_execution=False,runtime_eligible=False,groups=[],classifications={'CODE':0})
    previous.classify_demands(empty,providers,units,dict(records=old_records),set(),[],expected_code_count=0,expected_quarantines=set())
    for a,r in registry['records'].items():
        if r['authority']['kind']!='cached-native-v13':continue
        s=r['summary'];auth=r['authority'];root=r['root']
        require(exact(root,planner.root_record(a,providers[a],units)) and all(type(root[k]) is int for k in ('recipe_index','symbol_index','section','value','size')) and
            s['event']=='SINGLE_ROOT_OBSERVATION' and s['roots']==[a] and s['recipe_id']==root['recipe_id'] and
            type(s['recipe_index']) is int and s['recipe_index']==root['recipe_index'] and
            type(s['closure_observed']) is bool and type(s['graph_observation_complete']) is bool and
            type(s['blocker_codes']) is dict and all(type(v) is int and v>0 for v in s['blocker_codes'].values()) and
            ((s['closure_observed'] and s['graph_observation_complete'] and not s['blocker_codes']) or
             (not s['closure_observed'] and bool(s['blocker_codes']))) and
            auth['receipt_sha256']==NATIVE_RECEIPT and auth['request_sha256']==QUALIFIED_REQUEST and
            all(type(v) is int and v>0 for v in (auth['ordinal'],s['ordinal'],auth['qualified_record_ordinal'],s['qualified_record_ordinal'])) and
            auth['ordinal']==s['ordinal']==auth['qualified_record_ordinal']==s['qualified_record_ordinal'] and
            all(sha(auth[k]) and auth[k]==s[k] for k in ('record_sha256','contract_identity_sha256','qualified_metadata_row_sha256')) and
            auth['certificate_sha256']==s['certificate_sha256'] and (sha(auth['certificate_sha256']) or (auth['certificate_sha256'] is None and s['closure_observed'] is False)) and
            auth['qualification_certificate_created'] is False and auth['contract_identity_is_bound_through_record_hash'] is True,
            'cached native singleton authority differs')
    frontier=planner.reconcile(groups,providers,units,dict(observations=[r['summary'] for r in registry['records'].values()]),
        [r['root'] for r in registry['records'].values()],exclusions,expected_code_count=expected_code_count)
    q={r['root']['original_address']:r for r in quarantines}
    require(len(q)==len(quarantines) and set(q)==set(expected_quarantines),'exact six quarantines')
    qnames={}
    for a,row in q.items():
        root=row['root'];require(exact(root,planner.root_record(a,providers[a],units)) and
            all(type(root[k]) is int for k in ('recipe_index','symbol_index','section','value','size')) and row['fresh_body_compared'] is False and
            row['blockers'] and all(b['code']=='CANONICAL_REFERENCE_GROUP_REQUIRES_REVIEWED_V2' for b in row['blockers']),'quarantine source/policy')
        name=base.pool.canonical({k:root[k] for k in ('recipe_id','object_sha256','symbol_index')});require(name not in exclusions,'quarantine cannot become prepared');qnames[name]=row
    requested=[]
    for row in frontier['records']:
        root=row.get('root');a=root['original_address'] if root else None
        if a in registry['records']:
            cached=registry['records'][a];row['cached_authority']=copy.deepcopy(cached['authority']);row['cached_summary_sha256']=digest(cached['summary'])
        if row['symbol'] in qnames:
            require(exact(root,qnames[row['symbol']]['root']),'quarantine namespace mismatch')
            row['state']='PRESERVED_REFERENCE_GROUP_QUARANTINE';row['quarantine_sha256']=digest(qnames[row['symbol']])
        hydrate=row['state'] in ('NEW_SELECTED_ROOT_REQUIRES_OBSERVATION','CACHED_BARE_POSITIVE_REQUIRES_FRESH_CLASSIFICATION')
        row['inventory_action']='REQUEST_CACHED_METADATA' if hydrate else 'LEDGER_ONLY'
        if hydrate:requested.append(root)
    require(len({r['original_address'] for r in requested})==len(requested),'unique hydration roots')
    return dict(schema_version=1,kind='cached-CODE-frontier-planning-ledger',policy_id=POLICY,code_demands=len(frontier['records']),
        counts=dict(Counter(r['state'] for r in frontier['records'])),records=frontier['records'],metadata_requests=sorted(requested,key=lambda r:r['original_address']),
        registry_roots=len(registry['records']),**FALSE)


def validate_operation(operation):
    require(type(operation) is dict and set(operation)=={'schema_version','kind','epoch','artifacts','authorities','cache_data','output_relative','resource_limits'} and
        type(operation['schema_version']) is int and operation['schema_version']==1 and operation['kind']=='cached-CODE-frontier-inventory-operation' and
        type(operation['epoch']) is str and 0<len(operation['epoch'])<=100 and operation['epoch'].isascii() and
        operation['resource_limits']==LIMITS and operation['output_relative']=='build/rebuild/cached-code-frontier-inventory-v14-v1' and
        set(operation['artifacts'])==set(KNOWN),'exact finite V14 metadata operation')
    for name,ref in operation['artifacts'].items():
        ref_path(ref,private=name!='recipes');require(ref['sha256']==KNOWN[name],'unaccepted metadata pin: '+name)
    require(type(operation['authorities']) is list and len(operation['authorities'])==4,'exact four original authorities')
    actual=[]
    for source in operation['authorities']:
        require(type(source) is dict and set(source)=={'kind','receipt','request'},'authority descriptor schema')
        ref_path(source['receipt']);ref_path(source['request'])
        actual.append((source['kind'],source['receipt']['sha256'],source['request']['sha256']))
    require(actual==[p[:3] for p in AUTHORITY_PINS],'distinct ordered original authority epochs')
    data=operation['cache_data'];require(type(data) is dict and set(data)=={'path','receipt_expected_whole_data_sha256'} and
        type(data['path']) is str and data['receipt_expected_whole_data_sha256']==DATA_SHA,'receipt-bound cache data descriptor')
    path=(ROOT/data['path']).resolve();require(path.is_relative_to(ROOT/'build/rebuild'),'private cache data path')



def review_gate(args,inputs):
    review=load_ref(dict(path=str(args.review),sha256=args.review_sha256),inputs)
    require(type(review) is dict and set(review)=={'schema_version','kind','reviewer','approved','root_authorized','independent_source_schema_review_pass',
        'artifact_input_review_pass','operation_sha256','source_sha256','producer_sha256','allow_cache_frames','allow_original_inputs','allow_reference_image',
        'allow_native_tools','allow_code_emission','allow_certificate_or_admission','allow_global_binding_or_owner_stream'} and
        type(review['schema_version']) is int and review['schema_version']==1 and review['kind']=='cached-CODE-frontier-inventory-v14-review-v1' and
        type(review['reviewer']) is str and review['reviewer'] and review['reviewer']!='/root/code_lane_02' and
        all(review[k] is True for k in ('approved','root_authorized','independent_source_schema_review_pass','artifact_input_review_pass','allow_cache_frames')) and
        all(review[k] is False for k in ('allow_original_inputs','allow_reference_image','allow_native_tools','allow_code_emission','allow_certificate_or_admission','allow_global_binding_or_owner_stream')) and
        review['operation_sha256']==args.operation_sha256 and set(review['source_sha256'])==set(OWNED) and review['producer_sha256']==PINS,'independent metadata-only source/input gate')
    for rel,h in {**review['source_sha256'],**PINS}.items():require(sha(h),'source hash schema');base.observe(ROOT/rel,h,inputs)
    for module in (seam,seam.cache_module,seam.finite,historical,planner,provider_validator,base,previous,native,successor):
        require(Path(module.__file__).resolve()==ROOT/'tools/rebuild'/Path(module.__file__).name,'swapped metadata producer')
    return review


def prepare_metadata(operation,inputs,*,start=None):
    """Bounded saved JSON only. No prior detail stream or cache frame is read."""
    start=time.monotonic() if start is None else start
    validate_operation(operation);input_budget(start);artifacts={};epoch_bytes={}
    for name,ref in operation['artifacts'].items():
        if name in ('successor_parent','successor_handoff','successor_handoff_review','successor_members','successor_field_proofs'):
            path=ref_path(ref)
            with path.open('rb') as stream:raw=stream.read(LIMITS['output_bytes']+1)
            require(len(raw)<=LIMITS['output_bytes'] and hashlib.sha256(raw).hexdigest()==ref['sha256'],'same-byte successor input')
            epoch_bytes[name]=raw;inputs[path]=ref['sha256']
            if name!='successor_field_proofs':artifacts[name]=json.loads(raw)
        else:artifacts[name]=load_ref(ref,inputs,private=name!='recipes')
        input_budget(start)
    manifest=artifacts['manifest'];proof=artifacts['retained'];selection=artifacts['selection']
    units={u['recipe_id']:u for u in manifest['units']};proofs={u['recipe_id']:u for u in proof['units']}
    require(len(units)==len(manifest['units'])==len(proofs)==len(proof['units'])==2988 and len(selection['selections'])==68657,'complete saved native metadata universe')
    require(base.reconcile_recipes(manifest,ref_path(operation['artifacts']['recipes'],private=False))['verified'],'saved recipe manifest differs');input_budget(start)
    provider_validator.validate_provider_map(artifacts['planned_map'],selection['selections'],units,proofs,artifacts['owners']);input_budget(start)
    providers=artifacts['planned_map']['providers'];require(len(providers)==68657,'complete planned identity universe')
    require(artifacts['imports']['inputs']['manifest']==KNOWN['manifest'] and artifacts['imports']['inputs']['retained']==KNOWN['retained'] and
        artifacts['imports']['inputs']['reference']==proof['inputs']['image_sha256'],'frozen import metadata lineage')
    imported=[row for row in artifacts['imports']['imports'] if row['import_id']==175];require(len(imported)==1,'one authenticated import175 observation')
    require(artifacts['binding_summary']['details_sha256']==seam.cache_module.PINS['rows'],'compressed binding identity')
    require(artifacts['qualified_receipt']['output_sha256']['cache-registry.json']==KNOWN['old_registry'] and
        artifacts['old_registry_main_review']['approved'] is True and artifacts['old_registry_main_review']['receipt_sha256']==KNOWN['qualified_receipt'] and
        artifacts['old_registry_main_review']['producer_receipt_sha256']==KNOWN['qualified_receipt'] and
        artifacts['old_registry_authority_review']['approved'] is True and artifacts['old_registry_authority_review']['receipt_sha256']==KNOWN['qualified_receipt'],
        'accepted old708 registry/qualification outcome authority')
    rebuilt=artifacts['old_registry']
    empty=dict(kind='actual-unresolved-LNK-target-groups',executable_execution=False,runtime_eligible=False,groups=[],classifications={'CODE':0})
    previous.classify_demands(empty,providers,units,rebuilt,set(),[],expected_code_count=0,expected_quarantines=set())
    input_budget(start)
    registry=extend_registry(rebuilt,artifacts['native_receipt'],artifacts['qualified_request'],providers,units);input_budget(start)
    epoch=successor.from_bytes(epoch_bytes['successor_parent'],epoch_bytes['successor_handoff'],epoch_bytes['successor_handoff_review'],epoch_bytes['successor_members'],epoch_bytes['successor_field_proofs'])
    require(exact(epoch,artifacts['prepared_epoch']),'whole normative prepared successor differs')
    validate_epoch(epoch,providers,units);del epoch_bytes,raw;input_budget(start)
    quarantines=artifacts['quarantine_v5']+artifacts['quarantine_v8']+artifacts['quarantine_v12']
    inventory=classify_demands(artifacts['groups'],providers,units,registry,set(epoch['exclusion_names']),quarantines);input_budget(start)
    requests=inventory['metadata_requests']
    groups=seam.finite.validate_request(dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=requests),selection['selections'],manifest,proof,providers) if requests else {}
    index=artifacts['cache_index'];seam.cache_module.validate_index(index);input_budget(start)
    data_path=(ROOT/operation['cache_data']['path']).resolve()
    validate_cache_receipt(artifacts['cache_receipt'],index,data_name=data_path.name,index_bytes=ref_path(operation['artifacts']['cache_index']).stat().st_size,data_bytes=index['data_bytes'])
    for name,h in proof['inputs']['tools_sha256'].items():
        path=(ROOT/name).resolve();require(path.is_relative_to(ROOT/'tools'),'foreign retained validator');base.observe(path,h,inputs)
    return dict(artifacts=artifacts,units=units,proofs=proofs,providers=providers,registry=registry,epoch=epoch,inventory=inventory,groups=groups,imported=imported[0],data_path=data_path)




def provenance_for(unit,proof,prepared,request_sha256,operation_sha256):
    """New metadata provenance, never a historical certificate identity."""
    a=prepared['artifacts'];cm=seam.cache_module
    return dict(object_sha256=unit['object_sha256'],source_sha256=unit['source_sha256'],recipe_id=unit['recipe_id'],recipe_index=unit['recipe_index'],
        recipe_unit_sha256=proof['recipe_unit_sha256'],recipe_manifest_sha256=KNOWN['recipes'],producer_manifest_sha256=KNOWN['manifest'],
        retained_proof_sha256=KNOWN['retained'],selection_sha256=KNOWN['selection'],binding_sha256=cm.PINS['binding'],binding_details_sha256=cm.PINS['rows'],
        owner_ledger_sha256=KNOWN['owners'],owner_details_sha256=a['owners']['details_sha256'],imports_sha256=KNOWN['imports'],
        reference_identity_sha256=a['retained']['inputs']['image_sha256'],request_sha256=request_sha256,source_relative=unit['source'],
        producer_compiler_variant=unit['compiler'],optional_function_index_present=False,collector_policy_id=POLICY,
        metadata_operation_sha256=operation_sha256,metadata_contract_identity_is_new=True,native_observation_required=True,
        dependency_tools_sha256=PINS)


def run(args):
    start=time.monotonic();inputs={};review=review_gate(args,inputs)
    operation=load_ref(dict(path=str(args.operation),sha256=args.operation_sha256),inputs)
    prepared=prepare_metadata(operation,inputs,start=start);artifacts=prepared['artifacts'];inventory=prepared['inventory'];groups=prepared['groups']
    index_path=ref_path(operation['artifacts']['cache_index']);cache=seam.cache_module.BindingContextCache(prepared['data_path'],index_path,KNOWN['cache_index'])
    require(exact(cache.index,artifacts['cache_index']),'cache constructor and parsed same-byte index differ')
    range_guard=SelectedRangeGuard(prepared['data_path'],cache.index,list(groups))
    out=(ROOT/operation['output_relative']).resolve()
    require(Path(args.out).resolve()==out and out.is_relative_to(ROOT/'build/rebuild') and not out.exists() and
        not any(p.is_relative_to(out) for p in inputs) and not prepared['data_path'].is_relative_to(out),'new exclusive private inventory output')
    native_root=ref_path(operation['artifacts']['manifest']).parent/artifacts['manifest'].get('object_root_relative','.')
    for unit in artifacts['manifest']['units']:
        require(not (native_root/unit['object']).resolve().is_relative_to(out) and not (ROOT/unit['source']).resolve().is_relative_to(out),'output may not contain a named original input')
    base.stable(inputs);out.mkdir(parents=True,exist_ok=False);base.budget(start,out)
    journal=(out/'progress.jsonl').open('x',encoding='utf-8');record_count=0;singletons={};cohorts=Counter();recipe_verifications=[]
    def note(state,**facts):
        journal.write(json.dumps(dict(state=state,elapsed_seconds=round(time.monotonic()-start,3),**facts))+'\n');journal.flush();os.fsync(journal.fileno())
    try:
        note('started',code_demands=626,registry_roots=780,requested_roots=len(inventory['metadata_requests']),requested_recipes=len(groups))
        for rel in (*OWNED,*PINS):
            path=ROOT/rel;target=out/'source-snapshots'/rel;target.parent.mkdir(parents=True,exist_ok=True)
            base.pool.fsynced(target,path.read_bytes());base.observe(target,inputs[path.resolve()],inputs)
        request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=inventory['metadata_requests'])
        save_bounded_json(out/'metadata-request.json',request,start,out)
        request_hash=base.file_hash(out/'metadata-request.json');base.observe(out/'metadata-request.json',request_hash,inputs)
        with (out/'metadata-contracts.jsonl.gz').open('xb') as target:
            with gzip.GzipFile(fileobj=BoundedSink(target,start,out),mode='wb',mtime=0) as writer:
                for index,requested in groups.items():
                    unit=next(u for u in prepared['units'].values() if u['recipe_index']==index);proof=prepared['proofs'][unit['recipe_id']]
                    provenance=provenance_for(unit,proof,prepared,request_hash,args.operation_sha256)
                    result=seam.build_recipe_contexts(cache,index,artifacts['selection']['selections'],unit,proof,requested,prepared['imported'],provenance)
                    require(result['certificate_created'] is False and result['native_observation_required'] is True and
                        len(result['records'])==len(requested)+1,'whole requested recipe singleton/union metadata scope')
                    for record in result['records']:
                        record_count+=1;value=dict(schema_version=1,kind='new-cached-metadata-contract',policy_id=POLICY,**record,
                            new_metadata_contract_sha256=record['contract_sha256'],historical_certificate_contract_identity_equal_claimed=False,
                            certificate_created=False,native_observation_required=True)
                        raw=seam.canonical(value);require(len(raw)<=LIMITS['output_bytes'],'one metadata contract exceeds bounded record size')
                        writer.write(raw+b'\n')
                        if record['event']=='SINGLE_ROOT_METADATA_CONTRACT':
                            root=record['requested_roots'][0];a=root['original_address'];require(a not in singletons,'duplicate generated singleton')
                            features=metadata_features(record['contract']);cohorts[features['primary_planning_cohort']]+=1
                            singletons[a]=dict(contract_record_ordinal=record_count,new_metadata_contract_sha256=record['contract_sha256'],
                                generated_record_sha256=digest(value),features=features,source_frame_verification=record['source_frame_verification'])
                        base.budget(start,out)
                    recipe_verifications.append(dict(recipe_index=index,requested_roots=len(requested),verification=result['records'][0]['source_frame_verification']))
                    note('recipe_metadata_qualified',recipe_index=index,requested_roots=len(requested),contract_records=len(result['records']))
                    del result,record,value,raw,provenance
            target.flush();os.fsync(target.fileno())
        require(set(singletons)=={r['original_address'] for r in inventory['metadata_requests']} and
            record_count==len(singletons)+len(groups),'exact generated finite metadata record coverage')
        for record in inventory['records']:
            if record['inventory_action']=='REQUEST_CACHED_METADATA':record['new_metadata']=singletons[record['root']['original_address']]
        for name,value in [('inventory',inventory),('cache-registry',prepared['registry']),('prepared-epoch',prepared['epoch']),
            ('cohorts',dict(roots=len(singletons),primary_planning_counts=dict(cohorts),overlapping_evidence_not_additive=True,**FALSE))]:save_bounded_json(out/(name+'.json'),value,start,out)
        names=('inventory.json','cache-registry.json','prepared-epoch.json','metadata-request.json','cohorts.json','metadata-contracts.jsonl.gz')
        generated={name:base.file_hash(out/name) for name in names}
        require(generated['metadata-request.json']==request_hash,'exact generated request byte identity changed')
        for name,h in generated.items():base.observe(out/name,h,inputs)
        range_guard.verify();base.stable(inputs);usage=base.budget(start,out)
        result=dict(schema_version=1,policy_id=POLICY,status='metadata-only',epoch=operation['epoch'],operation_sha256=args.operation_sha256,review_sha256=args.review_sha256,
            code_demands=626,registry_roots=780,original_authorities=6,ordinary_prepared_count=14550,collision_exclusion_count=14556,
            requested_recipe_indices=sorted(groups),requested_recipe2768=2768 in groups,
            inherited_original_authority_descriptors=operation['authorities'],inherited_receipt_request_bodies_opened=False,
            inherited_descriptors_match_fixed_source_pins=True,preserved_registry_input_sha256=KNOWN['old_registry'],
            preserved_registry_main_review_sha256=KNOWN['old_registry_main_review'],preserved_registry_authority_review_sha256=KNOWN['old_registry_authority_review'],
            frontier_counts=inventory['counts'],qualified_metadata_roots=len(singletons),qualified_recipes=len(groups),generated_contract_records=record_count,
            new_metadata_contract_identity_is_not_historical_certificate_identity=True,primary_planning_cohorts=dict(cohorts),
            preserved_canonical_quarantine_addresses=sorted(QUARANTINE_ADDRESSES),native_observation_required=True,
            metadata_fingerprints_stable=True,selected_ranges_verified_prepublication=True,cache_data_stat_identity_stable=True,
            whole_cache_data_hash_verified_this_run=False,unrequested_cache_frames_verified=False,cache_data_range_protection=range_guard.descriptor(),
            recipe_frame_verifications=recipe_verifications,output_sha256=generated,inputs={str(p):h for p,h in inputs.items()},
            resource_limits=LIMITS,resource_observations=usage,emitted=0,blocked=0,**FALSE)
        return publish_inventory(out,result,inputs,start,journal,note,range_guard)
    except BaseException as error:
        if not journal.closed:note('failed',error_type=type(error).__name__)
        base.save_json(out/'abort.json',dict(status='aborted-no-retry',error_type=type(error).__name__,successful_inventory=False,**FALSE))
        raise
    finally:
        if not journal.closed:journal.close()


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('operation','review','out'):parser.add_argument('--'+name,type=Path,required=True)
    for name in ('operation','review'):parser.add_argument('--'+name+'-sha256',required=True)
    args=parser.parse_args(argv)
    try:result=run(args)
    except (ValueError,OSError,KeyError,TypeError) as error:parser.exit(2,'cached inventory rejected: '+str(error)+'\n')
    print(json.dumps(dict(code_demands=result['code_demands'],metadata_roots=result['qualified_metadata_roots'],contracts=result['generated_contract_records'])))
    return 0


if __name__=='__main__':raise SystemExit(main())
