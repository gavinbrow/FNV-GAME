"""Finite saved CODE planning inventory; cached contracts never grant admission."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import time

import cached_code_frontier as seam
import code_frontier_wave as historical
import current_code_frontier as planner
import ordinary_relocation_factory as provider_validator

base=historical.base
ROOT=base.ROOT
require=base.require
digest=seam.digest
POLICY='cached-CODE-frontier-inventory-v1'
OWNED=('tools/rebuild/cached_code_frontier_inventory.py','tests/rebuild/test_cached_code_frontier_inventory.py',
       'docs/rebuild/CACHED-CODE-FRONTIER-INVENTORY.md')
LIMITS=dict(seconds=900,peak_memory_bytes=1024**3,output_bytes=128*1024**2)
FALSE=dict(provider_selected=False,runtime_eligible=False,ABI_verified=False,link_ready=False,
    namespace_approved=False,full_serialization_eligible=False,materialization_approved=False,
    native_tools_run=False,original_objects_read=False,source_bodies_read=False,reference_image_read=False,
    global_binding_stream_read=False,owner_stream_read=False,code_emission_performed=False,
    certificate_created=False,admission_decision_created=False,closure_inferred=False,emission_performed=False)
PINS={**historical.PINS,**provider_validator.PINS,
    'tools/rebuild/code_frontier_wave.py':'5218ddc6e20eadfd2b51ff58e3d1cb35fa30abbe8a78ed7d031c4e4914fdf248',
    'tools/rebuild/current_code_frontier.py':'34ad6b6aacf0a9c5b0cfd68cf26fdd57e18cec4f9b74e24b48296049703397bc',
    'tools/rebuild/ordinary_relocation_factory.py':'f431d8599d7e91e2c67ed5570ccd067bdf80fbd8a92ee4c6daa3473cc26c928b',
    'tools/rebuild/binding_context_cache.py':'ab896ad1de9a081a8272b0b7024977c1c5199a1a8ba01df88f42fb3f5b38db9f',
    'tools/rebuild/cached_code_frontier.py':'40861c2ffc1ee74d535eb065b4d538b68127a22bcfbbcd58d481c3f901821287'}
AUTHORITY_PINS=(
 ('cached-central','290ac0e8c1ffbfd89df7dd6cdbbdb8df363edca58111b7aa19fe842aa26cc8e4','f778bdd8453d9813b978acbba7547e5733c585ebf5043b9769986bf8cf7e0665',205),
 ('cached-frontier','ea4e02c8e62264f65662ed4c9d5fdd2e4d990bf9b6c3dd70b5e0553b61f43da5','c59c18a92d790c93b73136967338e75826e6c089ebebd7c7194c680aadee03a1',10),
 ('cached-frontier','3afed5cd8a6728f0dbd7b8753fe5b3320524d1123dd68266bfb9fea22f00424a','7f30f61745419f31fcebf0fbea9124528810797473b04f03fb58bc6a1815bf26',54),
 ('cached-frontier','6eec875919603cd9cd3ce9bea7a34b82596f55dea95bc6253b6811aa08cd35ab','763a7c4641213101623cbc4226a9e6cfebee9d980bb84bd2ae2520afb8524ed9',259))
KNOWN={
 'groups':'46bc094719078cbd3fdacfd8ab9b573e898e3675253ac7af6609c12e9363aa00',
 'link_review':'de771fc26eb350a0450a55a04aa8abc24f838a689eaec520df3ffc12781377e6',
 'cache_receipt':'b84a2c21bc02783a73acf752f86b4b383f295b06244aee64b253e59cc65e2b9a',
 'cache_index':'f296613af711d42515431308e7462159eaf16f724c0d220dc8235deaae829158',
 'cache_review':'84a233f6d5a073f1a5fbe25018601a175318d3ab80c4e3bfefbad8458af283af',
 'seam_freeze':'a7be25d0dec5abc2898e2defc616cac408b8942bbf5c2b55af5585a1479edfdc',
 'seam_review':'7dd8b000e28f6023c884fae5851ac3b580fcf0d5f508d3b2a61e011cdce88012',
 'parent_epoch':'58804ef4d799868edb2230a5acbfed379f5091b914c54d2a558640cbf9723abf',
 'typed_handoff':'94ff62e56cc259b04fa2499016075ebaed4754293d581c0d35abc62d2302b24a',
 'typed_handoff_review':'f622f5cd885dfe823c20c7d9b200a7d584bc1c625338a6ef031f50945db3b05c',
 'quarantine_v5':historical.INPUTS['quarantine'][1],
 'quarantine_v8':'305d2eeb06d77077f2ccb5d1fd030d390d11281168f91d1cf39b8efcc02e2a9a',
 'planned_map':provider_validator.MAP_PIN,'provider_map_review':provider_validator.MAP_REVIEW[1],
 'binding_summary':seam.cache_module.PINS['binding'],'imports':seam.finite.IMPORT_PIN,
 **{k:base.inventory.EXPECTED[k] for k in ('manifest','retained','selection','owners','recipes')}}
DATA_SHA='b6991d8276e7b5d3529650ae30895ccd0650bbf640e85b7011d2f10d2ee87f3e'
QUARANTINE_ADDRESSES={'0x0086beb0','0x004e6620','0x0086ff70'}


def sha(value):return type(value) is str and re.fullmatch('[0-9a-f]{64}',value) is not None


def exact(left,right):return left==right and digest(left)==digest(right)


def extend_epoch(parent,handoff,providers,units,*,expected_parent=(14471,14477),expected_new=1):
    """Preserve old records; append explicit typed-negative COMDAT identities."""
    ordinary_count,collision_count=expected_parent
    require(all(type(parent[k]) is int for k in ('ordinary_prepared_count','collision_exclusion_count')) and
        parent['kind']=='prepared-CODE-collision-exclusions' and parent['ordinary_prepared_count']==ordinary_count and
        parent['collision_exclusion_count']==collision_count and len(parent['records'])==len(parent['exclusion_names'])==len(set(parent['exclusion_names']))==collision_count and
        len(parent['ordinary_names'])==len(set(parent['ordinary_names']))==ordinary_count,'exact parent collision census')
    require(parent['application_selection_inferred_from_counts'] is False and all(parent[k] is False for k in ('provider_selected','runtime_eligible','application_manifest_adopted')),'parent is collision evidence only')
    records=copy.deepcopy(parent['records']);names=set(parent['exclusion_names']);ordinary=set(parent['ordinary_names'])
    require({r['canonical'] for r in records}==names and ordinary<=names and
        all(base.pool.canonical(r['namespace_identity'])==r['canonical'] for r in records) and
        dict(Counter(r['category'] for r in records))==dict((k,v) for k,v in [('ordinary',ordinary_count),('application-candidate',collision_count-ordinary_count)] if v) and
        {r['canonical'] for r in records if r['category']=='ordinary'}==ordinary,'parent namespace/category census differs')
    require(handoff['kind']=='accepted-typed-COMDAT-CODE-export-handoff' and len(handoff['records'])==handoff['new_distinct_exports']==expected_new and
        handoff['upstream_ordinary_prepared_count']==ordinary_count and handoff['upstream_collision_exclusion_count']==collision_count and
        handoff['successor_ordinary_prepared_count']==ordinary_count+expected_new and handoff['successor_collision_exclusion_count']==collision_count+expected_new and
        handoff['original_negative_certificates_preserved'] is handoff['selection2_auxiliaries_preserved'] is handoff['requires_successor_exclusion_epoch'] is True and
        handoff['selection_rewritten'] is False and all(handoff[k] is False for k in ('provider_selected','runtime_eligible','application_manifest_adopted','native_tools_run')),
        'exact nonpromoted typed handoff required')
    seen=set()
    for ordinal,entry in enumerate(handoff['records'],1):
        root=entry['root'];a=root['original_address'];identity={k:root[k] for k in ('recipe_id','object_sha256','symbol_index')};name=base.pool.canonical(identity)
        require(set(root)==seam.ROOT_KEYS and all(type(root[k]) is int for k in ('recipe_index','symbol_index','section','value','size')) and
            a not in seen and exact(root,planner.root_record(a,providers[a],units)) and name==entry['canonical'] and name not in names and
            entry['original_object_sha256']==root['object_sha256'] and entry['original_negative_certificate_preserved'] is entry['selection2_auxiliary_preserved'] is True and
            entry['selection_rewritten'] is False,'typed source/physical namespace collision or authority differs')
        require(all(sha(entry[k]) for k in ('original_negative_certificate_sha256','composed_certificate_sha256','observer_record_sha256','definition_census_sha256','member_sha256')) and
            type(entry['serialized_symbol_index']) is int and entry['serialized_symbol_index']>=0,
            'explicit typed negative/composed/census identities required')
        seen.add(a);names.add(name);ordinary.add(name)
        records.append(dict(canonical=name,original_address=a,cohort='V8-typed-COMDAT-ANY',category='ordinary',identity_mode='original-selected-physical-typed-COMDAT',
            namespace_identity=identity,origin_identity=identity,member=entry['member'],member_sha256=entry['member_sha256'],serialized_symbol_index=entry['serialized_symbol_index'],
            source_ledger_sha256=KNOWN['typed_handoff'],source_record_ordinal=ordinal,source_record_sha256=digest(entry),logical_binding_applied=True,
            original_negative_certificate_sha256=entry['original_negative_certificate_sha256'],composed_certificate_sha256=entry['composed_certificate_sha256'],
            observer_record_sha256=entry['observer_record_sha256'],definition_census_sha256=entry['definition_census_sha256'],selection2_auxiliary_preserved=True,selection_rewritten=False))
    return dict(schema_version=6,kind='prepared-CODE-collision-exclusions',policy_id=POLICY,parent_manifest_sha256=KNOWN['parent_epoch'],
        ordinary_prepared_count=len(ordinary),broader_application_candidate_count=collision_count-ordinary_count,collision_exclusion_count=len(names),
        ordinary_names=sorted(ordinary),exclusion_names=sorted(names),records=sorted(records,key=lambda r:r['canonical']),
        application_selected_code_count=None,application_selection_inferred_from_counts=False,**FALSE)


def classify_demands(groups,providers,units,registry,exclusions,quarantines,*,expected_code_count=578,expected_quarantines=QUARANTINE_ADDRESSES):
    require(type(registry) is dict and set(registry['records'])=={r['root']['original_address'] for r in registry['records'].values()},'registry source addresses differ')
    allowed={p[:3] for p in AUTHORITY_PINS};locators=set()
    for a,record in registry['records'].items():
        root=record['root'];summary=record['summary'];authority=record['authority'];central=authority['kind']=='cached-central'
        require(exact(root,planner.root_record(a,providers[a],units)) and all(type(root[k]) is int for k in ('recipe_index','symbol_index','section','value','size')) and
            summary['event']=='SINGLE_ROOT_OBSERVATION' and summary['roots']==[a] and summary['recipe_id']==root['recipe_id'] and
            type(summary['closure_observed']) is bool and type(summary['graph_observation_complete']) is bool and
            sha(summary['record_sha256']) and authority['record_sha256']==summary['record_sha256'] and
            authority['certificate_sha256']==summary.get('certificate_sha256') and
            (sha(authority['certificate_sha256']) or (authority['certificate_sha256'] is None and summary['closure_observed'] is False)) and
            (authority['kind'],authority['receipt_sha256'],authority['request_sha256']) in allowed and
            authority['contract_identity_sha256'] is None and authority['contract_identity_is_bound_through_record_hash'] is True,
            'original registry source/summary/authority identity differs')
        require(type(authority['ordinal']) is int and authority['ordinal']>0 and
            authority['ordinal']==summary['lane_record_ordinal' if central else 'ordinal'] and
            (not central or (type(authority['lane']) is int and 1<=authority['lane']<=8 and authority['lane']==summary['lane'])),
            'original registry source ordinal/lane differs')
        key=(authority['receipt_sha256'],authority.get('lane'),authority['ordinal']);require(key not in locators,'duplicate registry source locator');locators.add(key)
    roots=[r['root'] for r in registry['records'].values()];summaries=[r['summary'] for r in registry['records'].values()]
    frontier=planner.reconcile(groups,providers,units,dict(observations=summaries),roots,exclusions,expected_code_count=expected_code_count)
    quarantine={q['root']['original_address']:q for q in quarantines}
    require(len(quarantine)==len(quarantines) and set(quarantine)==set(expected_quarantines),'exact disjoint canonical quarantines required')
    qnames={}
    for a,q in quarantine.items():
        root=q['root'];require(set(root)==seam.ROOT_KEYS and all(type(root[k]) is int for k in ('recipe_index','symbol_index','section','value','size')) and
            exact(root,planner.root_record(a,providers[a],units)) and q['fresh_body_compared'] is False and q['blockers'] and
            all(b['code']=='CANONICAL_REFERENCE_GROUP_REQUIRES_REVIEWED_V2' for b in q['blockers']),'canonical quarantine source/policy differs')
        name=base.pool.canonical({k:root[k] for k in ('recipe_id','object_sha256','symbol_index')})
        require(name not in exclusions,'quarantine cannot silently become prepared');qnames[name]=q
    requested=[]
    for record in frontier['records']:
        root=record.get('root')
        if root and root['original_address'] in registry['records']:
            old=registry['records'][root['original_address']]
            record['cached_authority']=copy.deepcopy(old['authority']);record['cached_summary_sha256']=digest(old['summary'])
        if record['symbol'] in qnames:
            require(exact(root,qnames[record['symbol']]['root']),'quarantine namespace/source contradiction')
            record['state']='PRESERVED_REFERENCE_GROUP_QUARANTINE';record['quarantine_sha256']=digest(qnames[record['symbol']])
        hydrate=record['state'] in ('NEW_SELECTED_ROOT_REQUIRES_OBSERVATION','CACHED_BARE_POSITIVE_REQUIRES_FRESH_CLASSIFICATION')
        record['inventory_action']='REQUEST_CACHED_METADATA' if hydrate else 'LEDGER_ONLY'
        if hydrate:requested.append(root)
    require(len({r['original_address'] for r in requested})==len(requested),'duplicate selected hydration root')
    return dict(schema_version=1,kind='cached-CODE-frontier-planning-ledger',policy_id=POLICY,code_demands=len(frontier['records']),
        counts=dict(Counter(r['state'] for r in frontier['records'])),records=frontier['records'],
        metadata_requests=sorted(requested,key=lambda r:r['original_address']),registry_roots=len(registry['records']),**FALSE)


def metadata_features(contract):
    """Disjoint planning cohort plus all overlapping original evidence counts."""
    fields=contract['fields'];missing=contract['missing_fields'];parents=contract['parent_eh'];omissions=contract['omission_field_proofs']
    rows=contract['provenance']['binding_row_references'];require(len(rows)==len(fields)+len(missing),'root original row census differs')
    if not rows:cohort='NO_BINDING_ROWS_NATIVE_COVERAGE_UNKNOWN'
    elif missing:cohort='MISSING_FIELDS_RECORDED'
    elif parents:cohort='PARENT_EH_RECORDED'
    elif omissions:cohort='OMISSION_FIELD_PROOFS_RECORDED'
    else:cohort='FIELD_ROWS_RECORDED'
    return dict(primary_planning_cohort=cohort,binding_row_count=len(rows),field_rows=len(fields),missing_rows=len(missing),
        parent_eh_records=len(parents),omission_field_proofs=len(omissions),
        relocation_kinds=dict(Counter(str(r['coff_relocation']['kind']) for r in fields)),
        target_classes=dict(Counter(r['classification'] for r in fields)),native_relocation_coverage_inferred=False,
        overlapping_counts_are_not_additive_unlocks=True,**FALSE)


def ref_path(ref,*,private=True):
    require(type(ref) is dict and set(ref)=={'path','sha256'} and type(ref['path']) is str and sha(ref['sha256']),'exact metadata descriptor')
    path=(ROOT/ref['path']).resolve();boundary=(ROOT/'build/rebuild').resolve() if private else ROOT.resolve()
    require(path.is_relative_to(boundary) and path!=boundary,'foreign metadata input')
    return path


def load_ref(ref,inputs,*,private=True):
    path=ref_path(ref,private=private);value=seam.read_bound_json(path,ref['sha256'])
    require(path not in inputs or inputs[path]==ref['sha256'],'conflicting metadata fingerprint');inputs[path]=ref['sha256']
    return value


def validate_operation(operation):
    require(type(operation) is dict and set(operation)=={'schema_version','kind','epoch','artifacts','authorities','cache_data','output_relative','resource_limits'} and
        type(operation['schema_version']) is int and operation['schema_version']==1 and operation['kind']=='cached-CODE-frontier-inventory-operation' and
        type(operation['epoch']) is str and 0<len(operation['epoch'])<=100 and operation['epoch'].isascii() and
        operation['resource_limits']==LIMITS and operation['output_relative']=='build/rebuild/cached-code-frontier-inventory-v11-v1' and
        set(operation['artifacts'])==set(KNOWN),'exact finite V11 metadata operation')
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


def validate_cache_receipt(receipt,index,*,data_name,index_bytes,data_bytes):
    cm=seam.cache_module
    require(type(receipt['schema_version']) is int and receipt['schema_version']==1 and receipt['policy_id']==cm.POLICY and receipt['status']=='metadata-cache-only' and
        receipt['lossless_cache_complete'] is receipt['input_stability'] is True and receipt['optional_function_index_present'] is False and
        all(type(receipt[k]) is int and receipt[k]==v for k,v in [('units',2988),('selected_functions',68657),('rows',490801)]) and
        receipt['producer_sha256']==PINS['tools/rebuild/binding_context_cache.py'] and receipt['inputs']==cm.PINS and
        receipt['data_sha256']==DATA_SHA and receipt['index_sha256']==KNOWN['cache_index'] and sha(receipt['original_raw_sha256']) and
        receipt['row_sequence_sha256']==cm.SEQUENCE and receipt['index_bytes']==index_bytes and receipt['data_bytes']==data_bytes and
        all(receipt[k] is False for k in cm.FALSE),'accepted complete lossless cache receipt')
    require(index['inputs']==receipt['inputs'] and index['data_sha256']==receipt['data_sha256'] and index['data_bytes']==data_bytes and
        index['data_file']==data_name and index['row_sequence_sha256']==receipt['row_sequence_sha256'] and
        all(index[k]==receipt[k] for k in ('units','selected_functions','rows','original_raw_sha256')),'same-byte index/receipt/data lineage')


def data_identity(path):
    stat=Path(path).stat()
    return (stat.st_dev,stat.st_ino,stat.st_size,stat.st_mtime_ns,stat.st_ctime_ns)


class SelectedRangeGuard:
    """Fresh selected compressed hashes; no claim about unrequested frames."""
    def __init__(self,path,index,recipe_indices):
        require(len(set(recipe_indices))==len(recipe_indices) and all(type(i) is int and 0<=i<len(index['frames']) for i in recipe_indices),'unique selected cache ranges')
        self.path=Path(path).resolve();self.initial=data_identity(path)
        require(self.initial[2]==index['data_bytes'],'cache file extent differs')
        self.entries=tuple(copy.deepcopy(index['frames'][i]) for i in sorted(recipe_indices))
    def verify(self):
        require(data_identity(self.path)==self.initial,'cache physical stat identity changed')
        with self.path.open('rb') as stream:
            for entry in self.entries:
                stream.seek(entry['offset']);remaining=entry['compressed_bytes'];observed=hashlib.sha256()
                while remaining:
                    part=stream.read(min(65536,remaining));require(part,'selected cache range truncated');remaining-=len(part);observed.update(part)
                require(observed.hexdigest()==entry['compressed_sha256'],'selected cache range changed after qualification')
        require(data_identity(self.path)==self.initial,'cache stat identity changed during selected-range check')
    def descriptor(self):
        return dict(path=str(self.path),physical_stat_identity=list(self.initial),receipt_expected_whole_data_sha256=DATA_SHA,
            whole_data_hash_verified_this_run=False,unrequested_frames_verified=False,
            selected_ranges=[{k:e[k] for k in ('recipe_index','offset','compressed_bytes','compressed_sha256','raw_sha256','row_sequence_sha256')} for e in self.entries])


def publish_inventory(output,result,inputs,start,journal,note,range_guard):
    """Reuse the frozen publisher, adding selected-range pre/post gates."""
    range_guard.verify()
    try:
        answer=base.finalize_success(output,result,inputs,start,journal,note)
        range_guard.verify()
        base.stable(inputs);base.budget(start,output)
        expected=(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode()
        receipt=Path(output)/'receipt.json';pending=Path(output)/'receipt.pending.json'
        require(os.path.samefile(receipt,pending) and receipt.read_bytes()==pending.read_bytes()==expected,
            'published terminal receipt differs from checked metadata result')
        return answer
    except BaseException:
        receipt=Path(output)/'receipt.json';pending=Path(output)/'receipt.pending.json'
        if receipt.exists() and pending.exists() and os.path.samefile(receipt,pending):receipt.unlink()
        raise


def review_gate(args,inputs):
    review=load_ref(dict(path=str(args.review),sha256=args.review_sha256),inputs)
    require(type(review) is dict and set(review)=={'schema_version','kind','reviewer','approved','root_authorized','independent_source_schema_review_pass',
        'artifact_input_review_pass','operation_sha256','source_sha256','producer_sha256','allow_cache_frames','allow_original_inputs','allow_reference_image',
        'allow_native_tools','allow_code_emission','allow_certificate_or_admission','allow_global_binding_or_owner_stream'} and
        type(review['schema_version']) is int and review['schema_version']==1 and review['kind']=='cached-CODE-frontier-inventory-review-v1' and
        type(review['reviewer']) is str and review['reviewer'] and review['reviewer']!='/root/code_lane_02' and
        all(review[k] is True for k in ('approved','root_authorized','independent_source_schema_review_pass','artifact_input_review_pass','allow_cache_frames')) and
        all(review[k] is False for k in ('allow_original_inputs','allow_reference_image','allow_native_tools','allow_code_emission','allow_certificate_or_admission','allow_global_binding_or_owner_stream')) and
        review['operation_sha256']==args.operation_sha256 and set(review['source_sha256'])==set(OWNED) and review['producer_sha256']==PINS,'independent metadata-only source/input gate')
    for rel,h in {**review['source_sha256'],**PINS}.items():require(sha(h),'source hash schema');base.observe(ROOT/rel,h,inputs)
    for module in (seam,seam.cache_module,seam.finite,historical,planner,provider_validator,base):
        require(Path(module.__file__).resolve()==ROOT/'tools/rebuild'/Path(module.__file__).name,'swapped metadata producer')
    return review


class BoundedSink:
    """Reject a compressed chunk before it can exceed the owned output cap."""
    def __init__(self,target,start,output):self.target=target;self.start=start;self.output=output
    def write(self,data):
        self.target.flush()
        usage=base.budget(self.start,self.output)
        require(usage['output_bytes']+len(data)<=LIMITS['output_bytes'],'compressed metadata output bound')
        return self.target.write(data)
    def __getattr__(self,name):return getattr(self.target,name)


def save_bounded_json(path,value,start,output):
    raw=(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()
    require(base.budget(start,output)['output_bytes']+len(raw)<=LIMITS['output_bytes'],'metadata JSON output bound')
    base.pool.fsynced(path,raw)


def input_budget(start):
    require(time.monotonic()-start<=LIMITS['seconds'],'metadata input time bound')
    peak=base.peak_memory_bytes();require(peak is not None and peak<=LIMITS['peak_memory_bytes'],'metadata input memory bound')


def prepare_metadata(operation,inputs,*,start=None):
    """Same-byte saved-JSON preflight; it never reads/decompresses a frame."""
    start=time.monotonic() if start is None else start
    validate_operation(operation);input_budget(start);artifacts={}
    for name,ref in operation['artifacts'].items():
        artifacts[name]=load_ref(ref,inputs,private=name!='recipes');input_budget(start)
    manifest=artifacts['manifest'];proof=artifacts['retained'];selection=artifacts['selection']
    units={u['recipe_id']:u for u in manifest['units']};proofs={u['recipe_id']:u for u in proof['units']}
    require(len(units)==len(manifest['units'])==len(proofs)==len(proof['units'])==2988 and len(selection['selections'])==68657,'complete saved native metadata universe')
    recipes=ref_path(operation['artifacts']['recipes'],private=False)
    require(base.reconcile_recipes(manifest,recipes)['verified'],'saved recipe manifest differs')
    input_budget(start)
    provider_validator.validate_provider_map(artifacts['planned_map'],selection['selections'],units,proofs,artifacts['owners'])
    input_budget(start)
    providers=artifacts['planned_map']['providers'];require(len(providers)==68657,'complete planned identity universe')
    require(artifacts['imports']['inputs']['manifest']==KNOWN['manifest'] and artifacts['imports']['inputs']['retained']==KNOWN['retained'] and
        artifacts['imports']['inputs']['reference']==proof['inputs']['image_sha256'],'frozen import metadata lineage')
    imported=[row for row in artifacts['imports']['imports'] if row['import_id']==175]
    require(len(imported)==1,'one authenticated import175 observation')
    require(artifacts['binding_summary']['details_sha256']==seam.cache_module.PINS['rows'],'original compressed binding artifact identity differs')
    sources=[]
    for source,(_,_,_,count) in zip(operation['authorities'],AUTHORITY_PINS):
        receipt=load_ref(source['receipt'],inputs);input_budget(start)
        request=load_ref(source['request'],inputs)
        input_budget(start)
        require(set(request)=={'schema_version','kind','roots'} and request['kind']=='fnv-finite-ordinary-root-request' and len(request['roots'])==count,'complete finite authority request')
        sources.append(dict(kind=source['kind'],receipt_sha256=source['receipt']['sha256'],request_sha256=source['request']['sha256'],receipt=receipt,requests=request['roots']))
    registry=historical.cache_registry(sources,providers,units,expected_total=528)
    input_budget(start)
    epoch=extend_epoch(artifacts['parent_epoch'],artifacts['typed_handoff'],providers,units)
    input_budget(start)
    quarantines=artifacts['quarantine_v5']+artifacts['quarantine_v8']
    inventory=classify_demands(artifacts['groups'],providers,units,registry,set(epoch['exclusion_names']),quarantines)
    input_budget(start)
    requests=inventory['metadata_requests']
    groups=seam.finite.validate_request(dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=requests),selection['selections'],manifest,proof,providers) if requests else {}
    index=artifacts['cache_index'];seam.cache_module.validate_index(index)
    input_budget(start)
    data_path=(ROOT/operation['cache_data']['path']).resolve()
    validate_cache_receipt(artifacts['cache_receipt'],index,data_name=data_path.name,
        index_bytes=ref_path(operation['artifacts']['cache_index']).stat().st_size,data_bytes=index['data_bytes'])
    for name,h in proof['inputs']['tools_sha256'].items():
        path=(ROOT/name).resolve();require(path.is_relative_to(ROOT/'tools'),'foreign retained validator');base.observe(path,h,inputs)
    return dict(artifacts=artifacts,units=units,proofs=proofs,providers=providers,registry=registry,epoch=epoch,inventory=inventory,
        groups=groups,imported=imported[0],data_path=data_path)


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
        note('started',code_demands=578,registry_roots=528,requested_roots=len(inventory['metadata_requests']),requested_recipes=len(groups))
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
            code_demands=578,registry_roots=528,original_authorities=4,ordinary_prepared_count=14472,collision_exclusion_count=14478,
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
