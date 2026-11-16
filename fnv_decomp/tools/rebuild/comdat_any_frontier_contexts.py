"""Select exact V8 negative root contexts; no native or Selection-2 inference."""
from __future__ import annotations
from collections import Counter
import copy
import hashlib
import json
import re

import frontier_root_collect_v3 as producer
import runtime_code_pool as pool

POLICY = 'V8-comdat-any-negative-context-selection-v1'
FRONTIER_POLICY = 'V8-CODE-frontier-wave-metadata-v1'
ROOT_BLOCKER = 'UNSUPPORTED_OR_PARTIAL_ROOT_SECTION'
COLLECTOR_PIN = 'b03bb96c147ba4233832ad539bcc60bc7478fc1cc0038965c8c9f587cb688bce'
FRONTIER_FALSE = {'provider_selected','runtime_eligible','ABI_verified','link_ready','application_manifest_adopted',
    'executable_link_performed','game_execution_performed','native_tools_run','code_emission_performed',
    'original_objects_read','original_image_read','source_bodies_read'}
REGISTRY_FALSE = FRONTIER_FALSE | {'materialization_approved','compiler_performed','typed_root_witnesses_consumed'}
RECEIPT_KEYS = {'schema_version','policy_id','status','epoch','original_native_epoch','inputs','context_sha256',
    'request_sha256','frontier_join_sha256','authority_kind','cache_registry_sha256','prior_authorities','cached_roots',
    'planned_map_sha256','details_sha256','details_bytes','observations','summary','baseline_binding_census',
    'owner_stream_traversals','binding_stream_traversals','cached_roots_reobserved','collector_sha256',
    'input_stability','optional_function_index_present','game_fixups_approved'} | set(producer.FALSE)
COUNTS = {'NEW_SELECTED_ROOT_REQUIRES_OBSERVATION':259,
          'CACHED_ORIGINAL_OMISSION_BLOCKED':179,
          'PRESERVED_REFERENCE_GROUP_QUARANTINE':1,
          'PREPARED_SKIP':3, 'UNSELECTED_OR_NAMESPACE_UNPROVED':25}
ROOT_KEYS = {'original_address','recipe_id','recipe_index','object_sha256',
             'source_sha256','symbol','symbol_index','section','value','size'}
FALSE = dict(provider_selected=False,runtime_eligible=False,ABI_verified=False,
    link_ready=False,emission_performed=False,namespace_approved=False,
    full_serialization_eligible=False,original_objects_read=False,
    original_image_read=False,source_bodies_read=False,native_tools_run=False)


def require(test, message):
    if not test: raise ValueError(message)


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()


def document_hash(value, *, sort_keys=True):
    """Exact Windows producers: binary sorted LF, text receipt unsorted CRLF."""
    terminal='\n' if sort_keys else '\r\n'
    return hashlib.sha256((json.dumps(value,sort_keys=sort_keys,separators=(',',':'),ensure_ascii=True)+terminal).encode()).hexdigest()


def same(a,b): return canonical(a)==canonical(b)


def sha(value):
    return type(value) is str and re.fullmatch('[0-9a-f]{64}',value) is not None


def address(value):
    return type(value) is str and re.fullmatch('0x[0-9a-f]{8}',value) is not None


def root_identity(root):
    require(type(root) is dict and set(root)==ROOT_KEYS,'exact ten-field original root required')
    require(address(root['original_address']) and all(type(root[k]) is int for k in
        ('recipe_index','symbol_index','section','value','size')),'root address/integer schema')
    require(root['recipe_index']>=0 and root['symbol_index']>=0 and root['section']>0 and
        root['value']>=0 and root['size']>0 and int(root['original_address'],16)+root['size']<=2**32,
        'root geometry bounds')
    require(all(type(root[k]) is str and root[k] and root[k].isascii() for k in ('recipe_id','symbol')) and
        sha(root['object_sha256']) and sha(root['source_sha256']),'root source identity')
    return {k:root[k] for k in ('recipe_id','object_sha256','symbol_index')}


def summary(row, *, central=False, singleton=True):
    keys={'event','recipe_id','roots','record_sha256','certificate_sha256','closure_observed',
          'graph_observation_complete','blocker_codes'} | ({'lane','lane_record_ordinal'} if central else {'ordinal'})
    require(type(row) is dict and set(row)==keys,'unknown observation summary schema')
    require(row['event'] in ('SINGLE_ROOT_OBSERVATION','RECIPE_ROOT_UNION_OBSERVATION') and
        (not singleton or row['event']=='SINGLE_ROOT_OBSERVATION'),'singleton summary required')
    require(type(row['roots']) is list and row['roots'] and all(address(a) for a in row['roots']) and
        len(set(row['roots']))==len(row['roots']) and (not singleton or len(row['roots'])==1),'summary root scope')
    require(type(row['recipe_id']) is str and row['recipe_id'] and sha(row['record_sha256']) and
        (sha(row['certificate_sha256']) or row['certificate_sha256'] is None),'summary hash schema')
    ordinal=row['lane_record_ordinal'] if central else row['ordinal']
    require(type(ordinal) is int and ordinal>0 and (not central or
        (type(row['lane']) is int and 1<=row['lane']<=8)),'summary source locator')
    require(type(row['closure_observed']) is bool and type(row['graph_observation_complete']) is bool and
        type(row['blocker_codes']) is dict and all(type(k) is str and k and type(v) is int and v>0
        for k,v in row['blocker_codes'].items()),'typed summary state/blocker counts')
    require((row['graph_observation_complete'] and not row['blocker_codes'] and sha(row['certificate_sha256']))
        if row['closure_observed'] else bool(row['blocker_codes']),'summary positive/negative contradiction')


def _registry(registry):
    require(type(registry) is dict and set(registry)=={'schema_version','kind','policy_id','roots','authorities','records',
        'contract_digest_loaded_only_from_authenticated_body'} | REGISTRY_FALSE and
        all(registry[k] is False for k in REGISTRY_FALSE),'unknown/promoted registry envelope')
    producer.validate_registry(registry)
    require(registry.get('policy_id')==FRONTIER_POLICY and
        registry.get('contract_digest_loaded_only_from_authenticated_body') is True,'registry policy/deferred identity')
    require(same(registry['authorities'],producer.AUTHORITIES),'typed cache authorities')
    locators=set();physical=set()
    for a,row in registry['records'].items():
        require(type(row) is dict and set(row)=={'root','summary','authority'},'unknown registry row')
        root,s,auth=row['root'],row['summary'],row['authority']; identity=root_identity(root)
        require(a==root['original_address'],'registry root address')
        central=auth['kind']=='cached-central';summary(s,central=central)
        require(set(auth)=={'kind','receipt_sha256','request_sha256','record_sha256','certificate_sha256',
            'contract_identity_sha256','contract_identity_is_bound_through_record_hash','ordinal'} | ({'lane'} if central else set()),
            'unknown cache locator fields')
        require(type(auth['ordinal']) is int and auth['ordinal']==s['lane_record_ordinal' if central else 'ordinal'] and
            (not central or type(auth['lane']) is int and auth['lane']==s['lane']),'cache ordinal/lane join')
        key=(auth['receipt_sha256'],auth.get('lane'),auth['ordinal'])
        require(key not in locators,'duplicate cache locator');locators.add(key)
        physical.add(canonical(identity))
    return physical


def select_candidates(frontier, registry, new_receipt, new_receipt_sha256):
    """Return finite authenticated body locators; malformed input is fatal."""
    try:
        return _select_candidates(frontier,registry,new_receipt,new_receipt_sha256)
    except (KeyError,TypeError,AttributeError) as error:
        raise ValueError('malformed context selection input: '+type(error).__name__) from error


def _select_candidates(frontier, registry, new_receipt, new_receipt_sha256):
    physical=_registry(registry)
    require(type(frontier) is dict and set(frontier)=={'schema_version','kind','policy_id','frontier','code_demands','counts',
        'records','new_roots','cached_positive_roots','eligibility_not_inferred_from_closure'} | FRONTIER_FALSE and
        type(frontier.get('schema_version')) is int and frontier['schema_version']==1 and
        frontier.get('kind')=='current-CODE-frontier-reconciliation' and frontier.get('policy_id')==FRONTIER_POLICY and
        frontier.get('frontier')=='accepted-V8' and type(frontier.get('code_demands')) is int and frontier['code_demands']==467 and
        same(frontier.get('counts'),COUNTS) and frontier.get('cached_positive_roots')==[] and
        frontier.get('eligibility_not_inferred_from_closure') is True,'exact current V8 frontier profile required')
    for k in FRONTIER_FALSE:
        require(frontier.get(k) is False,'frontier promotion: '+k)
    require(type(frontier['records']) is list and len(frontier['records'])==467 and
        type(frontier['new_roots']) is list and len(frontier['new_roots'])==259,'complete frontier demand count')
    new={}
    for root in frontier['new_roots']:
        identity=root_identity(root);a=root['original_address'];p=canonical(identity)
        require(a not in new and a not in registry['records'] and p not in physical,'duplicate new/cached root identity')
        new[a]=root;physical.add(p)
    require(list(new)==sorted(new),'new root request order')
    receipt=new_receipt
    require(type(receipt) is dict and set(receipt)==RECEIPT_KEYS,'unknown new receipt envelope')
    require(sha(new_receipt_sha256) and document_hash(receipt,sort_keys=False)==new_receipt_sha256,'new receipt document hash')
    require(type(receipt.get('schema_version')) is int and receipt['schema_version']==1 and
        receipt.get('policy_id')==producer.POLICY and receipt.get('status')=='metadata-only' and
        receipt.get('authority_kind')=='new-frontier-v3' and receipt.get('original_native_epoch')=='retained-full-v3' and
        receipt.get('input_stability') is True and receipt.get('optional_function_index_present') is False and
        type(receipt.get('cached_roots')) is int and receipt['cached_roots']==269 and
        same(receipt.get('prior_authorities'),producer.AUTHORITIES) and receipt.get('collector_sha256')==COLLECTOR_PIN and
        type(receipt.get('epoch')) is str and 0<len(receipt['epoch'])<=100 and receipt['epoch'].isascii() and
        sha(receipt.get('context_sha256')) and type(receipt.get('details_bytes')) is int and
        0<receipt['details_bytes']<=producer.MAX_OUTPUT,'accepted new receipt epoch required')
    require(all(receipt.get(k) is False for k in producer.FALSE),'new receipt promoted')
    require(all(type(receipt.get(k)) is int and receipt[k]==v for k,v in
        [('owner_stream_traversals',0),('binding_stream_traversals',1),('cached_roots_reobserved',0),('game_fixups_approved',0)]),
        'new receipt observation scope')
    request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=frontier['new_roots'])
    require(receipt.get('cache_registry_sha256')==document_hash(registry) and
        receipt.get('frontier_join_sha256')==document_hash(frontier) and
        receipt.get('request_sha256')==document_hash(request) and sha(receipt.get('details_sha256')) and
        receipt.get('planned_map_sha256')==producer.MAP_PIN,'receipt registry/frontier/request body lineage')
    singles={};events=Counter();recipes=set();unions={}
    require(type(receipt.get('observations')) is list,'new observation list')
    for ordinal,row in enumerate(receipt['observations'],1):
        summary(row,singleton=False)
        require(row['ordinal']==ordinal and all(a in new and row['recipe_id']==new[a]['recipe_id'] for a in row['roots']),
            'new observation ordinal/root/recipe join')
        events[row['event']]+=1;recipes.add(row['recipe_id'])
        if row['event']=='SINGLE_ROOT_OBSERVATION':
            require(len(row['roots'])==1 and row['roots'][0] not in singles,'duplicate new singleton')
            singles[row['roots'][0]]=row
        else:
            require(row['recipe_id'] not in unions,'duplicate new recipe union');unions[row['recipe_id']]=set(row['roots'])
    require(set(singles)==set(new) and unions=={ri:{a for a,r in new.items() if r['recipe_id']==ri} for ri in recipes},
        'complete new singleton/union coverage')
    expected=dict(roots=259,recipes=len(recipes),events=dict(events),
        singleton_closure=sum(s['closure_observed'] for s in singles.values()),
        singleton_blocked=sum(not s['closure_observed'] for s in singles.values()))
    require(same(receipt.get('summary'),expected),'new receipt summary census')
    candidates=[];audit=[];states=Counter();seen=set();seen_roots=set();new_seen=set()
    basic={'symbol','group_ordinal','group_sha256','original_bases','original_targets','state'}
    for row in frontier['records']:
        state=row['state'];require(state in COUNTS and type(row['symbol']) is str and row['symbol'] not in seen and
            type(row['group_ordinal']) is int and row['group_ordinal']>0 and sha(row['group_sha256']),'frontier demand identity')
        seen.add(row['symbol']);states[state]+=1
        require(all(type(row[k]) is list and all(address(a) for a in row[k]) for k in ('original_bases','original_targets')),
            'frontier base/target schema')
        reason=state;selected=False
        if state in ('PREPARED_SKIP','UNSELECTED_OR_NAMESPACE_UNPROVED'):
            require(set(row)==basic,'skip must not carry unproved root authority')
        else:
            root=row['root'];identity=root_identity(root);a=root['original_address']
            require(row['symbol']==pool.canonical(identity) and a in row['original_bases'] and a not in seen_roots,'frontier selected identity')
            seen_roots.add(a)
            if state=='NEW_SELECTED_ROOT_REQUIRES_OBSERVATION':
                require(set(row)==basic|{'root'} and a in new and same(root,new[a]),'new demand root join')
                new_seen.add(a);s=singles[a]
                auth=dict(kind='new-frontier-v3',receipt_sha256=new_receipt_sha256,
                    request_sha256=receipt['request_sha256'],details_sha256=receipt['details_sha256'],ordinal=s['ordinal'],
                    record_sha256=s['record_sha256'],certificate_sha256=s['certificate_sha256'],
                    contract_identity_sha256=None,contract_identity_is_bound_through_record_hash=True)
            else:
                extras={'root','cached_observation','cache_authority'} | ({'quarantine_sha256'} if state=='PRESERVED_REFERENCE_GROUP_QUARANTINE' else set())
                require(set(row)==basic|extras and a in registry['records'],'cached demand shape')
                cached=registry['records'][a]
                require(same(root,cached['root']) and same(row['cached_observation'],cached['summary']) and
                    same(row['cache_authority'],cached['authority']),'cached demand borrowed authority')
                s=cached['summary'];auth=cached['authority']
                if state=='CACHED_ORIGINAL_OMISSION_BLOCKED':require(s['closure_observed'] is False,'cached negative state contradiction')
                else:require(a=='0x0086beb0' and sha(row['quarantine_sha256']),'preserved reference quarantine identity')
            if state!='PRESERVED_REFERENCE_GROUP_QUARANTINE':
                selected=not s['closure_observed'] and ROOT_BLOCKER in s['blocker_codes'] and sha(s['certificate_sha256'])
                reason='NEGATIVE_ROOT_CONJUNCT_BODY_REQUIRED' if selected else 'NO_AUTHENTICATED_NEGATIVE_ROOT_CONJUNCT'
                if selected:
                    candidates.append(dict(root=root,authority=auth,summary=s,source_state=state,
                        symbol=row['symbol'],group_ordinal=row['group_ordinal'],group_sha256=row['group_sha256']))
        audit.append(dict(symbol=row['symbol'],group_ordinal=row['group_ordinal'],original_state=state,
            selected=selected,reason=reason))
    require(dict(states)==COUNTS and new_seen==set(new) and
        len({r['group_ordinal'] for r in frontier['records']})==467,'complete distinct frontier accounting')
    candidates.sort(key=lambda c:c['root']['original_address'])
    return copy.deepcopy(dict(schema_version=1,policy_id=POLICY,kind='finite-negative-root-context-selection',
        frontier_sha256=document_hash(frontier),registry_sha256=document_hash(registry),
        new_receipt_sha256=new_receipt_sha256,roots=[c['root'] for c in candidates],candidates=candidates,
        audit=audit,counts=dict(selected=len(candidates),preserved=467-len(candidates)),
        body_read_required=True,contract_identity_deferred=True,selection2_inferred=False,
        native_census_evaluated=False,candidate_policy_evaluated=False,**FALSE))
