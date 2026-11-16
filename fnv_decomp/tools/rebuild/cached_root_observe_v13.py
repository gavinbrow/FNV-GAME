"""V13 opt-in observer; operational source/input review precedes actual use.

Version-local root/core bodies preserve the reviewed a393 semantics. No legacy
module globals or qualified envelopes are changed to admit the new policy.
"""
from __future__ import annotations
import argparse
from collections import Counter
import gzip
import hashlib
import json
import os
from pathlib import Path
import tempfile
import time
import re
import struct
import cached_root_observe as previous

POLICY='cached-context-root-observation-v13'
QUALIFIED_POLICY='cached-CODE-frontier-inventory-v13'
# Accepted qualification census; this is not ordinary or runtime eligibility.
MAX_ROOTS=72
MAX_RECIPES=44
MAX_RECORDS=116
ACTUAL_OPERATION_PROFILE=dict(roots=72,recipes=44,records=116)
PREVIOUS_SOURCE_SHA256='a393fadfb27c086e67e5ba8fe415e73757a9597f200ee4810e61be523865b96a'
ROOT_KEYS=previous.ROOT_KEYS
NATIVE_KEYS=previous.NATIVE_KEYS
CONTRACT_KEYS=previous.CONTRACT_KEYS
QUALIFIED_FALSE=previous.QUALIFIED_FALSE
QUALIFIED_KEYS=previous.QUALIFIED_KEYS
FALSE=previous.FALSE
LIMITS=previous.LIMITS
require=previous.require
canonical=previous.canonical
digest=previous.digest
typed_equal=previous.typed_equal
verify_physical_fields=previous.verify_physical_fields
coff=previous.coff
ordinary=previous.ordinary
inventory=previous.inventory
finite=previous.finite
ROOT=previous.ROOT
PINS={**previous.PINS,'cached_root_observe.py':PREVIOUS_SOURCE_SHA256}
JOURNAL_LIMIT=previous.JOURNAL_LIMIT
read_bound_json=previous.read_bound_json
budget=previous.budget
DigestingSource=previous.DigestingSource
summary_row=previous.summary_row
publish_outputs=previous.publish_outputs
retract_outputs=previous.retract_outputs
verify_outputs=previous.verify_outputs

def validate_roots(unit,proof,requested):
    require(type(unit['recipe_index']) is int and type(proof['recipe_index']) is int and unit['recipe_index']>=0,
        'unit/proof recipe index must be exact integer')
    require(all(isinstance(unit[k],str) and re.fullmatch('[0-9a-f]{64}',unit[k]) for k in ('object_sha256','source_sha256')),
        'unit source/object digest format differs')
    inventory.check_unit(unit,proof)
    require(type(requested) is list and 0<len(requested)<=MAX_ROOTS,'finite exact requested roots required')
    require(all(all(type(f[k]) is int for k in ('section','value','size')) for f in proof['verified_functions']), 'retained physical integer types differ')
    result={}
    for r in requested:
        require(type(r) is dict and set(r)==ROOT_KEYS and all(type(r[k]) is int for k in ('recipe_index','symbol_index','section','value','size')),
            'exact typed physical root schema required')
        a=r['original_address'];require(isinstance(a,str) and re.fullmatch('0x[0-9a-f]{8}',a) and a not in result,'duplicate/invalid root address')
        require(r['recipe_index']==unit['recipe_index'] and r['recipe_id']==unit['recipe_id'] and
            r['object_sha256']==unit['object_sha256'] and r['source_sha256']==unit['source_sha256'] and
            r['section']>0 and r['value']>=0 and r['size']>0,'root source/object/recipe differs')
        matches=[f for f in proof['verified_functions'] if f['address']==a and f['symbol']==r['symbol'] and
            typed_equal([f[k] for k in ('section','value','size')],[r[k] for k in ('section','value','size')])]
        require(len(matches)==1 and r['symbol_index']>=0,'root lacks unique exact retained span')
        result[a]=r
    return result


def observe_recipe_contracts(raw,unit,proof,requested,qualified_views,observation_provenance):
    """Streaming pure seam: one parse, exact qualified contracts, no waivers.

    Qualified producer order is singletons followed by its recipe union. The
    caller must consume every result and finish the operation before publishing.
    Source-file freshness and whole-artifact authority belong to the driver.
    """
    requested_by_address=validate_roots(unit,proof,requested)
    require(type(raw) is bytes and hashlib.sha256(raw).hexdigest()==unit['object_sha256'],'raw original object hash differs')
    require(isinstance(observation_provenance,dict) and isinstance(observation_provenance.get('qualified_request_sha256'),str) and
        re.fullmatch('[0-9a-f]{64}',observation_provenance['qualified_request_sha256']),
        'qualified request lineage required')
    original_inputs=digest([unit,proof,requested,observation_provenance])
    try:obj=coff.parse(raw);parse_error=None
    except (ValueError,UnicodeError,struct.error) as error:obj=None;parse_error=inventory.public_metadata(str(error))
    if obj is not None:
        relocations={i:{canonical(list(x)) for x in s['relocs']} for i,s in obj['sections'].items()}
        for r in requested:
            s=obj['symbols'].get(r['symbol_index'])
            require(s is not None and typed_equal([s[k] for k in ('name','section','value')],
                [r[k] for k in ('symbol','section','value')]),'native selected physical owner contradiction')
    singles={};union_seen=False;common=None;frame=None;count=0
    for view in qualified_views:
        count+=1;require(count<=len(requested)+1,'extra qualified view')
        require(type(view) is dict and set(view)==QUALIFIED_KEYS and type(view.get('schema_version')) is int and view['schema_version']==1 and
            view.get('kind')=='new-cached-metadata-contract' and view.get('policy_id')==QUALIFIED_POLICY and
            all(view.get(k) is False for k in QUALIFIED_FALSE) and view.get('native_observation_required') is True,
            'qualified metadata authority/schema/promotion differs')
        before=digest(view);contract=view['contract'];roots=view['requested_roots']
        require(type(contract) is dict and set(contract)==CONTRACT_KEYS and contract['recipe_id']==unit['recipe_id'] and
            digest(contract)==view['contract_sha256']==view['new_metadata_contract_sha256'],'qualified contract identity/schema differs')
        require(type(roots) is list and roots and len({r['original_address'] for r in roots})==len(roots) and
            all(r['original_address'] in requested_by_address and typed_equal(r,requested_by_address[r['original_address']]) for r in roots), 'borrowed/duplicate qualified root')
        require(typed_equal(contract['roots'],[{k:r[k] for k in NATIVE_KEYS} for r in roots]),'qualified native root scope differs')
        require(contract['export_policy']==ordinary.EXPORT_POLICY and all(contract[k] is True for k in
            ('verified_match','fields_complete','missing_fields_complete','unit_proofs_complete')), 'incomplete qualified contract')
        require(typed_equal(contract['unit_verified_functions'],proof['verified_functions']) and
            typed_equal(contract['parent_eh'],[r for r in proof.get('eh_sections',[]) if r[3] in {v['original_address'] for v in roots}]),
            'qualified unit/EH proof changed')
        p=contract['provenance'];require(p['object_sha256']==unit['object_sha256'] and p['source_sha256']==unit['source_sha256'] and
            p['request_sha256']==observation_provenance['qualified_request_sha256'],'qualified source/request provenance differs')
        fingerprint=digest({k:v for k,v in contract.items() if k not in ('roots','fields','missing_fields','parent_eh','provenance')})
        shared_provenance=digest({k:v for k,v in p.items() if k!='binding_row_references'})
        current=(fingerprint,shared_provenance)
        require(common is None or common==current,'recipe-wide qualified proofs/provenance differ');common=current
        verification=view['source_frame_verification']
        require(type(verification['recipe_index']) is int and verification['recipe_index']==unit['recipe_index'] and
            type(verification['row_count']) is int and verification['row_count']>=0 and
            all(isinstance(verification[k],str) and re.fullmatch('[0-9a-f]{64}',verification[k]) for k in ('raw_sha256','compressed_sha256')) and
            verification.get('whole_data_hash_verified_this_read') is False and
            verification.get('unrequested_frames_verified') is False,'qualified frame identity/claims differ')
        require(frame is None or typed_equal(frame,verification),'qualified unit frame differs');frame=verification
        event=view['event']
        if event=='SINGLE_ROOT_METADATA_CONTRACT':
            require(not union_seen and len(roots)==1,'singleton after union or wrong scope');a=roots[0]['original_address']
            require(a not in singles,'duplicate qualified singleton')
            singles[a]=([digest(r) for r in contract['fields']],[digest(r) for r in contract['missing_fields']],
                        [digest(r) for r in p['binding_row_references']])
            output_event='SINGLE_ROOT_OBSERVATION'
        elif event=='RECIPE_UNION_METADATA_CONTRACT':
            require(not union_seen and set(singles)==set(requested_by_address) and len(roots)==len(requested), 'incomplete/duplicate qualified union')
            for i,values in enumerate((contract['fields'],contract['missing_fields'],p['binding_row_references'])):
                require([digest(r) for r in values]==[h for root in roots for h in singles[root['original_address']][i]], 'union field/missing/reference partition differs')
            union_seen=True;output_event='RECIPE_ROOT_UNION_OBSERVATION'
        else:raise ValueError('unknown qualified view event')
        if obj is not None:
            verify_physical_fields(obj,contract['fields'],relocations)
            if count==1:verify_physical_fields(obj,contract['omission_field_proofs'],relocations)
            certificate=ordinary.assess_object(obj,contract)
            require(certificate['contract_identity_sha256']==view['contract_sha256'] and certificate['full_serialization_eligible'] is False,
                'frozen observation identity/policy changed')
        else:certificate=None
        require(digest(view)==before and digest([unit,proof,requested,observation_provenance])==original_inputs,'observation mutated qualified evidence')
        record=dict(schema_version=1,policy_id=POLICY,kind='fresh-root-observation-from-qualified-contract',event=output_event,
            recipe_id=unit['recipe_id'],recipe_index=unit['recipe_index'],requested_roots=roots,contract=contract,
            contract_identity_sha256=view['contract_sha256'],qualified_metadata_row_sha256=before,
            qualified_metadata_identity={k:view[k] for k in ('schema_version','kind','policy_id','event','certificate_created',
                'native_observation_required','historical_certificate_contract_identity_equal_claimed','source_frame_verification')},
            observation_provenance=observation_provenance,native_object_sha256=unit['object_sha256'],native_parse_performed=obj is not None,
            qualified_contract_unchanged=True,fresh_certificate_created=certificate is not None,**FALSE)
        if certificate is None:
            record.update(closure_observed=False,graph_observation_complete=False,root_closure_candidate=False,
                blockers=[dict(code='UNSUPPORTED_ORIGINAL_COFF_FORMAT',evidence=parse_error)])
        else:
            record.update(certificate=certificate,certificate_sha256=digest(certificate),closure_observed=certificate['closure_observed'],
                graph_observation_complete=certificate['graph_observation_complete'],root_closure_candidate=certificate['root_closure_candidate'],
                blockers=certificate['blockers'])
        yield record
    require(count==len(requested)+1 and union_seen and set(singles)==set(requested_by_address),'partial qualified recipe batch')


ARTIFACT_PINS={**{k:previous.ARTIFACT_PINS[k] for k in ('selection','manifest','retained','recipes','planned_map','imports')},
    'qualified_receipt':'128933eb62f713a49c3fa26d501445ff39aacc7544ef70534071bc6ef3b5682e',
    'qualified_request':'fdfcd3773c0b3e50fa7cc9ec63982556825fb9e4eab2a9d0e77f30b429ea32c4',
    'qualified_records':'e5f18ed87c6c0a0d5220c8c2a358e6cc1484418759e942a9975c6a7ff10973b4',
    'qualified_inventory':'04cad1db5bb39f7e15682d3a842141b60ac63a7059244069897df4a636f0c603',
    'qualified_registry':'3e4af440e1587e8eb4ebd24501fdcb8ee34acce11fa6438866c36c4a816f1968',
    'prepared_epoch':'751fbe4660de0f851d6621ac89638c7b21975339be856a13284f4f0967e10c4c',
    'qualification_main_review':'1e72158b99041d926ec82d8c5aea3f7ce24a72eba6cd211b5469e7ea17e92718',
    'qualification_authority_review':'ac70782848c16e4e35911940d14967171e62f9fd516415ad6969daea6f927871',
    'current_groups':'2d7b6d0c60049539d6abfd45d04ed69f92be4322b1bd357795b4e8003e755ba6',
    'current_review':'87ddc7b3072e34589663feec02e1db797b3142ee4d208f69a8272756883b57ba',
    'old_native_receipt':'d7110b2c52f7b31053e08e2627de694d038c31f5e6ffae3dae358a9975f36768',
    'latest_prepared_epoch':'8dde3e03371386c14fe8751a2e3eda65fbd591f6e386caa0e705621d7b94ee41',
    'latest_prepared_review':'8d117f6c4eddb6aaa87dd32dc56d1d6faa2cbeb3301d458247f7faf77d32c666'}
ARTIFACT_KEYS=set(ARTIFACT_PINS)
QUALIFICATION_ARTIFACTS=dict(ARTIFACT_PINS)


def require_actual_authority():
    if ACTUAL_OPERATION_PROFILE is None or QUALIFICATION_ARTIFACTS is None:
        raise ValueError('V13 actual qualification/profile gates remain unset; source-only interface')
    # Built-in comparisons here precede verification of imported helpers.
    if (type(ACTUAL_OPERATION_PROFILE) is not dict or set(ACTUAL_OPERATION_PROFILE)!={'roots','recipes','records'} or
        any(type(ACTUAL_OPERATION_PROFILE[k]) is not int or ACTUAL_OPERATION_PROFILE[k]!=v
            for k,v in (('roots',MAX_ROOTS),('recipes',MAX_RECIPES),('records',MAX_RECORDS))) or
        QUALIFICATION_ARTIFACTS!=ARTIFACT_PINS or
        not all(isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v) for v in ARTIFACT_PINS.values())):
        raise ValueError('V13 actual qualification acceptance pins/profile are incomplete')


def bind_dependency_epoch(observations,started=None):
    """Enforce frozen helper bytes before operational metadata helpers are used."""
    for name,expected in PINS.items():
        path=ROOT/'tools/rebuild'/name;hasher=hashlib.sha256();size=0
        with path.open('rb') as source:
            while chunk:=source.read(1048576):
                size+=len(chunk)
                if size>LIMITS['output_bytes']:raise ValueError('helper source byte bound')
                hasher.update(chunk)
                if started is not None and time.monotonic()-started>LIMITS['seconds']:raise ValueError('dependency fingerprint time bound')
        if hasher.hexdigest()!=expected:raise ValueError('frozen V13 observation helper changed')
        if path in observations and observations[path]!=expected:raise ValueError('conflicting helper identity')
        observations[path]=expected
    for module,name in ((previous,'cached_root_observe.py'),(coff,'coff_code_archive.py'),(ordinary,'root_code_closure.py'),
                         (inventory,'runtime_code_inventory.py'),(finite,'scalableordinary_root_collect.py')):
        if Path(module.__file__).resolve()!=ROOT/'tools/rebuild'/name:raise ValueError('foreign imported observation dependency')
    if started is not None:budget(started)


UUID_ROOT=dict(original_address='0x00c5d4e0',recipe_id='2768-7a8853c4310f459f',recipe_index=2768,section=131,size=58,
    symbol='?FUN_00c5d4e0@@YAXXZ',symbol_index=553,value=0,
    object_sha256='a7280d36e8d796a5689c8b61adac4be327eb17d55e12d734600b0ede46cafb88',
    source_sha256='376782096fdbabae4c10fb175023317d58fcbd8930596abea1008d8628bffe02')
UUID_SUCCESSOR_PROVENANCE=dict(
    qualified_uuid_handoff_sha256='4ce4f515e43a04f622b1efaa70ac47753f16109111944f73ca0aefeb915b06a1',
    qualified_uuid_handoff_review_sha256='7b879e3baa1bf55e81c9a9884f692b27feff025c0d5fe55a30d7c3d60135ab9d',
    qualified_uuid_native_sha256='12dae2e56d941949650dbc8c0d72a0660c4d8da5d4d14f2209db4f79e2c852f1',
    qualified_uuid_native_review_sha256='f161af6ac5ce40e02088724ba156f7737484def6b5aafadc4f8bda104587b7f6')


def validate_epoch_successor(historical,latest,requested,providers):
    """Exact metadata successor join; the fixed independent peer is normative."""
    require(type(historical['schema_version']) is int and historical['schema_version']==7 and
        historical['policy_id']=='prepared-CODE56-successor-v1' and historical['kind']=='prepared-CODE-collision-exclusions' and
        historical['application_selected_code_count'] is None and historical['application_selection_inferred_from_counts'] is False and
        'application_manifest_adopted' not in historical,'historical collision-only epoch differs')
    require(type(latest['schema_version']) is int and latest['schema_version']==8 and
        latest['kind']==historical['kind'] and latest['policy_id']=='prepared-UUID2768-successor-v1' and
        latest['parent_manifest_sha256']=='250c9cf8be4cd98e805eb81ed89daae989bab6d262cab5cf0f3e8040120693af' and
        all(type(latest[k]) is int for k in ('ordinary_prepared_count','collision_exclusion_count')) and
        (latest['ordinary_prepared_count'],latest['collision_exclusion_count'])==(14529,14535), 'current UUID successor scope differs')
    require(type(latest['records']) is list and len(historical['records'])==14534 and len(latest['records'])==14535 and
        typed_equal(latest['records'][:14534],historical['records']),'historical records/order changed')
    row=latest['records'][-1];identity={k:UUID_ROOT[k] for k in ('recipe_id','object_sha256','symbol_index')}
    name='_fnv_code_'+digest(identity)
    require(UUID_ROOT['original_address'] in providers and typed_equal(providers[UUID_ROOT['original_address']],identity) and
        typed_equal(row['original_root'],UUID_ROOT) and typed_equal(row['namespace_identity'],identity) and
        typed_equal(row['origin_identity'],identity) and row['canonical']==name and row['original_address']==UUID_ROOT['original_address'] and
        row['category']=='ordinary' and row['cohort']=='UUID2768-qualified-directive-projection' and
        row['identity_mode']=='original-selected-physical-qualified-UUID-directives' and row['logical_binding_applied'] is True,
        'sole successor is not the reviewed typed UUID identity')
    require(row['original_negative_certificate_sha256']=='7c4704d0c777585656272cd2a39a06437d124e34d4cea712236b982641cf9a26' and
        row['qualified_composition_sha256']=='69076d817070c2411fbb8d3dbf9cf1ea0ca3409d6a438360c25dffc19aa7d238' and
        row['source_ledger_sha256']==UUID_SUCCESSOR_PROVENANCE['qualified_uuid_handoff_sha256'] and
        row['native_receipt_sha256']==UUID_SUCCESSOR_PROVENANCE['qualified_uuid_native_sha256'] and
        row['native_review_sha256']==UUID_SUCCESSOR_PROVENANCE['qualified_uuid_native_review_sha256'] and
        type(row['original_field_count']) is int and row['original_field_count']==9,
        'typed qualification/negative lineage replaced by ordinary closure')
    names=historical['exclusion_names'];ordinary_names=historical['ordinary_names']
    require(len(names)==len(set(names))==14534 and len(ordinary_names)==len(set(ordinary_names))==14528 and
        name not in names and UUID_ROOT['original_address'] not in {r['original_address'] for r in historical['records']},
        'UUID successor duplicates a historical definition')
    expected=dict(historical,schema_version=8,policy_id='prepared-UUID2768-successor-v1',
        parent_manifest_sha256='250c9cf8be4cd98e805eb81ed89daae989bab6d262cab5cf0f3e8040120693af',
        records=latest['records'],exclusion_names=sorted(names+[name]),ordinary_names=sorted(ordinary_names+[name]),
        ordinary_prepared_count=14529,collision_exclusion_count=14535,qualified_uuid_export_count=1,qualified_uuid_field_count=9,
        historical_records_preserved=True,fresh_original_stability_verified=False,**UUID_SUCCESSOR_PROVENANCE)
    require(typed_equal(latest,expected),'unrelated epoch fields, roles or application state changed')
    requested_names={'_fnv_code_'+digest(providers[r['original_address']]) for r in requested}
    require(not requested_names.intersection(latest['exclusion_names']) and
        UUID_ROOT['original_address'] not in {r['original_address'] for r in requested},'new roots collide with latest prepared namespace')
    return dict(historical_qualified_epoch_sha256=ARTIFACT_PINS['prepared_epoch'],
        historical_parent_manifest_sha256=latest['parent_manifest_sha256'],latest_epoch_sha256=ARTIFACT_PINS['latest_prepared_epoch'],
        latest_peer_sha256=ARTIFACT_PINS['latest_prepared_review'],preserved_records=14534,typed_uuid_appended=1,
        appended_record_sha256=digest(row),appended_canonical=name,new_requested_names_disjoint=True,
        ordinary_closure_inferred=False,UUID_selected_or_loaded=False,provider_selected=False,runtime_eligible=False)


def validate_saved_context(receipt,request,qualified_inventory,registry,current_groups,planned,manifest,proof,selection,imports,
                           prepared_epoch,old_native_receipt,latest_prepared_epoch):
    """Metadata authority only: complete new roots; old recipe overlap is explicit."""
    require(receipt['policy_id']==QUALIFIED_POLICY and receipt['status']=='metadata-only' and
        all(type(receipt[k]) is int for k in ('qualified_metadata_roots','qualified_recipes','generated_contract_records','code_demands','registry_roots')) and
        (receipt['qualified_metadata_roots'],receipt['qualified_recipes'],receipt['generated_contract_records'],receipt['code_demands'],receipt['registry_roots'])==
        (MAX_ROOTS,MAX_RECIPES,MAX_RECORDS,593,708) and receipt['certificate_created'] is False and
        receipt['native_observation_required'] is True and receipt['metadata_fingerprints_stable'] is True and
        all(receipt[k] is False for k in ('provider_selected','runtime_eligible','native_tools_run','original_objects_read','source_bodies_read','code_emission_performed')),
        'V13 qualification scope/promotion differs')
    require(set(request)=={'schema_version','kind','roots'} and type(request['schema_version']) is int and request['schema_version']==1 and
        request['kind']=='fnv-finite-ordinary-root-request' and len(request['roots'])==MAX_ROOTS,'whole exact V13 request required')
    require(typed_equal(qualified_inventory['metadata_requests'],request['roots']) and len(qualified_inventory['records'])==593,'qualified V13 census differs')
    require(type(registry['roots']) is int and registry['roots']==708 and len(registry['records'])==708 and
        not ({r['original_address'] for r in request['roots']}&set(registry['records'])),'historical root replay/registry scope differs')
    require(set(planned['providers'])==set(selection['selections']) and len(selection['selections'])==68657 and
        planned['materialized_exports']==0 and planned['provider_selected'] is False and planned['runtime_eligible'] is False,'planned identities differ')
    providers={a:{k:p[k] for k in ('recipe_id','object_sha256','symbol_index')} for a,p in planned['providers'].items()}
    groups=finite.validate_request(request,selection['selections'],manifest,proof,providers)
    require(len(groups)==MAX_RECIPES and 2768 not in groups,'V13 whole recipe scope/UUID ownership differs')
    require(receipt['requested_recipe2768'] is False and typed_equal(receipt['requested_recipe_indices'],sorted(groups)),'qualified requested recipe roster differs')
    require(current_groups['kind']=='actual-unresolved-LNK-target-groups' and current_groups['executable_execution'] is False and
        current_groups['runtime_eligible'] is False,'nonexecuted V13 frontier required')
    code_rows=[r for r in current_groups['groups'] if r['classification']=='CODE'];code={r['symbol']:r for r in code_rows}
    names=[r['symbol'] for r in qualified_inventory['records']]
    require(len(code_rows)==len(code)==len(names)==len(set(names))==593 and set(names)==set(code),'duplicate/borrowed V13 CODE demand')
    for r in request['roots']:
        item=code.get('_fnv_code_'+digest(providers[r['original_address']]))
        require(item is not None and item['observed_roles']==['code'] and item['included_provenance_is_extraction_proof'] is False and
            r['original_address'] in item['original_bases'],'requested V13 physical owner absent from demand')
    require(prepared_epoch['kind']=='prepared-CODE-collision-exclusions' and
        all(type(prepared_epoch[k]) is int for k in ('ordinary_prepared_count','collision_exclusion_count')) and
        (prepared_epoch['ordinary_prepared_count'],prepared_epoch['collision_exclusion_count'])==(14528,14534) and
        len(prepared_epoch['records'])==len(prepared_epoch['exclusion_names'])==len(set(prepared_epoch['exclusion_names']))==14534,
        'accepted collision-only epoch differs')
    epoch_join=validate_epoch_successor(prepared_epoch,latest_prepared_epoch,request['roots'],providers)
    require(all(type(row['recipe_index']) is int and type(row['requested_roots']) is int and row['requested_roots']>0 and
        type(row['verification']['recipe_index']) is int and row['verification']['recipe_index']==row['recipe_index']
        for row in receipt['recipe_frame_verifications']),'qualified frame integer identity differs')
    frames={row['recipe_index']:row for row in receipt['recipe_frame_verifications']}
    require(len(frames)==len(receipt['recipe_frame_verifications'])==MAX_RECIPES and set(frames)==set(groups) and
        all(frames[i]['requested_roots']==len(roots) for i,roots in groups.items()),'qualified frame roster differs')
    expected={r['original_address']:r for r in request['roots']};singles={}
    for item in qualified_inventory['records']:
        if item.get('inventory_action')!='REQUEST_CACHED_METADATA':continue
        root=item['root'];a=root['original_address'];entry=item['new_metadata']
        require(a not in singles and a in expected and typed_equal(root,expected[a]),'borrowed/duplicate qualified singleton')
        require(type(entry['contract_record_ordinal']) is int and 1<=entry['contract_record_ordinal']<=MAX_RECORDS and
            all(isinstance(entry[k],str) and re.fullmatch('[0-9a-f]{64}',entry[k]) for k in ('generated_record_sha256','new_metadata_contract_sha256')),
            'qualified ordinal/hash type differs')
        singles[a]=entry
    require(set(singles)==set(expected),'qualified singleton coverage differs')
    cached={a:r for a,r in registry['records'].items() if r['authority']['kind']=='cached-native'}
    require(all(type(r['root']['recipe_index']) is int for r in cached.values()),'historical recipe index type differs')
    prior_recipes={r['root']['recipe_index'] for r in cached.values()}
    require(len(cached)==180 and len(prior_recipes)==77 and old_native_receipt['policy_id']==previous.POLICY and
        old_native_receipt['source_sha256']==PREVIOUS_SOURCE_SHA256 and old_native_receipt['qualified_contracts_preserved'] is True and
        old_native_receipt['input_stability'] is True and old_native_receipt['optional_function_index_present'] is False and
        (old_native_receipt['summary']['roots'],old_native_receipt['summary']['recipes'],old_native_receipt['summary']['records'])==(180,77,257),
        'accepted previous native summary authority differs')
    prior_rows=[r for r in old_native_receipt['observations'] if r['event']=='SINGLE_ROOT_OBSERVATION']
    require(len(old_native_receipt['observations'])==257 and len(prior_rows)==180 and all(len(r['roots'])==1 for r in prior_rows),
        'historical native summary occurrence census differs')
    prior_summaries={r['roots'][0]:r for r in prior_rows}
    require(len(prior_summaries)==180 and set(prior_summaries)==set(cached) and all(typed_equal(prior_summaries[a],r['summary']) and
        r['authority']['receipt_sha256']==ARTIFACT_PINS['old_native_receipt'] for a,r in cached.items()),'cached-native summary commitments differ')
    require(imports['inputs']['manifest']==ARTIFACT_PINS['manifest'] and imports['inputs']['retained']==ARTIFACT_PINS['retained'] and
        imports['inputs']['reference']==proof['inputs']['image_sha256'],'import/reference authority differs')
    imported=[r for r in imports['imports'] if r['import_id']==175];require(len(imported)==1,'exact import175 metadata required')
    return dict(groups=groups,singleton_index=singles,frames=frames,imported=imported[0],
        units={u['recipe_index']:u for u in manifest['units']},proofs={p['recipe_index']:p for p in proof['units']},
        previous_native_recipe_overlap=sorted(prior_recipes&set(groups)),current_successor_join=epoch_join)


def prepare_operation(operation,observations,started=None):
    def check():
        if started is not None:budget(started)
    require_actual_authority();bind_dependency_epoch(observations,started);validate_operation(operation);check()
    paths={name:(ROOT/ref['path']).resolve() for name,ref in operation['artifacts'].items()};refs=operation['artifacts'];loaded={}
    for name,path in paths.items():
        if name=='qualified_records':continue
        loaded[name]=read_bound_json(path,refs[name]['sha256']);observations[path]=refs[name]['sha256'];check()
    for key,filename in (('qualified_inventory','inventory.json'),('qualified_request','metadata-request.json'),
                         ('qualified_registry','cache-registry.json'),('qualified_records','metadata-contracts.jsonl.gz'),('prepared_epoch','prepared-epoch.json')):
        require(loaded['qualified_receipt']['output_sha256'][filename]==refs[key]['sha256'],'V13 qualification/output binding differs')
    observations[paths['qualified_records']]=refs['qualified_records']['sha256']
    prepared=validate_saved_context(*[loaded[k] for k in ('qualified_receipt','qualified_request','qualified_inventory','qualified_registry',
        'current_groups','planned_map','manifest','retained','selection','imports','prepared_epoch','old_native_receipt','latest_prepared_epoch')]);check()
    require(finite.reconcile_recipes(loaded['manifest'],paths['recipes'])['verified'],'recipe epoch differs');check()
    for name,expected in PINS.items():finite.pin(ROOT/'tools/rebuild'/name,expected,observations);check()
    require(Path(previous.__file__).resolve()==ROOT/'tools/rebuild/cached_root_observe.py','foreign previous helper module')
    for module,name in ((coff,'coff_code_archive.py'),(ordinary,'root_code_closure.py'),
                         (inventory,'runtime_code_inventory.py'),(finite,'scalableordinary_root_collect.py')):
        require(Path(module.__file__).resolve()==ROOT/'tools/rebuild'/name,'foreign imported observation dependency')
    finite.pin(Path(__file__),operation['source_sha256'],observations);check()
    for name,expected in loaded['retained']['inputs']['tools_sha256'].items():
        path=(ROOT/name).resolve();require(path.is_relative_to(ROOT),'foreign proof dependency');finite.pin(path,expected,observations);check()
    prepared.update(loaded=loaded,paths=paths);return prepared


class QualifiedReader:
    def __init__(self,stream,prepared,request_sha256):
        self.stream=stream;self.prepared=prepared;self.request_sha256=request_sha256;self.ordinal=0;self.last_index=-1
        self.next=None;self.singletons=set();self.unions=set();self.sequence=hashlib.sha256();self._advance()
    def _advance(self):
        raw=self.stream.readline(LIMITS['output_bytes']+1)
        if not raw:self.next=None;return
        require(len(raw)<=LIMITS['output_bytes'],'qualified metadata row size bound')
        self.ordinal+=1;require(self.ordinal<=MAX_RECORDS,'extra qualified metadata record')
        row=json.loads(raw);roots=row['requested_roots'];require(roots and type(roots[0]['recipe_index']) is int,'qualified root recipe type')
        index=roots[0]['recipe_index'];require(index in self.prepared['groups'] and index>=self.last_index,'foreign/unsorted qualified recipe')
        self.last_index=index;expected={r['original_address']:r for r in self.prepared['groups'][index]}
        require(all(r['original_address'] in expected and typed_equal(r,expected[r['original_address']]) for r in roots),'borrowed qualified physical root')
        require(row['contract_sha256']==row['new_metadata_contract_sha256']==digest(row['contract']) and
            row['contract']['provenance']['request_sha256']==self.request_sha256,'qualified row contract/request identity differs')
        require(typed_equal(row['source_frame_verification'],self.prepared['frames'][index]['verification']),'qualified frame receipt differs')
        if row['event']=='SINGLE_ROOT_METADATA_CONTRACT':
            require(len(roots)==1,'singleton metadata scope differs');a=roots[0]['original_address'];entry=self.prepared['singleton_index'][a]
            require(a not in self.singletons and entry['contract_record_ordinal']==self.ordinal and
                entry['generated_record_sha256']==digest(row) and entry['new_metadata_contract_sha256']==row['contract_sha256'] and
                typed_equal(entry['source_frame_verification'],row['source_frame_verification']),'qualified singleton ordinal/row identity differs')
            self.singletons.add(a)
        elif row['event']=='RECIPE_UNION_METADATA_CONTRACT':
            require(index not in self.unions and len(roots)==len(expected) and {r['original_address'] for r in roots}==set(expected),'qualified union scope differs')
            self.unions.add(index)
        else:raise ValueError('unknown qualified event')
        self.sequence.update(canonical([self.ordinal,digest(row)]));self.next=(self.ordinal,row)
    def take(self,index):
        require(self.next is None or self.next[1]['requested_roots'][0]['recipe_index']>=index,'unconsumed qualified recipe')
        while self.next is not None and self.next[1]['requested_roots'][0]['recipe_index']==index:
            value=self.next;yield value;self._advance()
    def finish(self):
        require(self.next is None and self.ordinal==MAX_RECORDS and len(self.singletons)==MAX_ROOTS and
            self.unions==set(self.prepared['groups']),'partial qualified global batch')
        return dict(records=self.ordinal,singletons=len(self.singletons),unions=len(self.unions),row_sequence_sha256=self.sequence.hexdigest())


def validate_operation(operation):
    """Fixed finite operation envelope; no files are opened by this function."""
    require_actual_authority()
    require(type(operation) is dict and set(operation)=={'schema_version','kind','policy_id','epoch','roots','recipes','records',
        'limits','artifacts','source_sha256'},'unknown operation envelope')
    require(type(operation['schema_version']) is int and operation['schema_version']==1 and
        operation['kind']=='whole-qualified-contract-native-observation' and operation['policy_id']==POLICY,'unknown operation policy')
    require(type(operation['epoch']) is str and 0<len(operation['epoch'])<=100 and operation['epoch'].isascii(),'explicit epoch required')
    require(all(type(operation[k]) is int for k in ('roots','recipes','records')) and
        (operation['roots'],operation['recipes'],operation['records'])==(MAX_ROOTS,MAX_RECIPES,MAX_RECORDS) and
        typed_equal(operation['limits'],LIMITS),'whole finite census/resource limits required')
    require(isinstance(operation['source_sha256'],str) and re.fullmatch('[0-9a-f]{64}',operation['source_sha256']),'explicit observer digest required')
    require(type(operation['artifacts']) is dict and set(operation['artifacts'])==ARTIFACT_KEYS,'exact saved authority set required')
    paths=[]
    for name,ref in operation['artifacts'].items():
        require(type(ref) is dict and set(ref)=={'path','sha256'} and isinstance(ref['path'],str) and ref['path'] and
            isinstance(ref['sha256'],str) and re.fullmatch('[0-9a-f]{64}',ref['sha256']),'malformed artifact reference')
        path=(ROOT/ref['path']).resolve()
        require(not Path(ref['path']).is_absolute() and path.is_relative_to(ROOT),'foreign artifact path')
        paths.append(path)
        if name in ARTIFACT_PINS:require(ref['sha256']==ARTIFACT_PINS[name],'saved authority pin differs')
    require(len(set(paths))==len(paths),'artifact path collision')
    return operation


def stream_observations(prepared,reader,read_native,observation_provenance):
    """Read one named raw object per recipe; exhaust all views before success."""
    for index,roots in sorted(prepared['groups'].items()):
        unit,proof=prepared['units'][index],prepared['proofs'][index]
        raw=read_native(unit)
        ordinals=[]
        def views():
            for ordinal,row in reader.take(index):
                ordinals.append(ordinal);yield row
        for record in observe_recipe_contracts(raw,unit,proof,roots,views(),observation_provenance):
            record['qualified_record_ordinal']=ordinals[-1]
            yield record
        del raw
    reader.finish()


def summary_row(record,ordinal):
    return dict(ordinal=ordinal,event=record['event'],recipe_id=record['recipe_id'],recipe_index=record['recipe_index'],
        roots=[r['original_address'] for r in record['requested_roots']],record_sha256=digest(record),
        qualified_record_ordinal=record['qualified_record_ordinal'],qualified_metadata_row_sha256=record['qualified_metadata_row_sha256'],
        contract_identity_sha256=record['contract_identity_sha256'],certificate_sha256=record.get('certificate_sha256'),
        closure_observed=record['closure_observed'],graph_observation_complete=record['graph_observation_complete'],
        blocker_codes=dict(Counter(b['code'] for b in record['blockers'])))


def _run(args,published,state):
    require_actual_authority()
    started=time.monotonic();operation_path=Path(args.operation).resolve()
    state['started']=started
    observations={};bind_dependency_epoch(observations,started);budget(started)
    operation=read_bound_json(operation_path,args.operation_sha256);validate_operation(operation)
    budget(started)
    observations[operation_path]=args.operation_sha256;prepared=prepare_operation(operation,observations,started)
    state['observations']=observations
    reserved=set(observations)
    for unit in prepared['loaded']['manifest']['units']:
        obj=(prepared['paths']['manifest'].parent/prepared['loaded']['manifest'].get('object_root_relative','.')/unit['object']).resolve()
        src=(ROOT/unit['source']).resolve();reserved.update((src,obj))
    budget(started)
    out,details,progress=finite.output_paths(args.out,args.details,reserved)
    require(all(path.is_relative_to(ROOT/'build/rebuild') for path in (out,details,progress)),'private rebuild output paths required')
    index=ROOT/'build/function_index.json';require(not index.exists(),'optional index appeared')
    progress.parent.mkdir(parents=True,exist_ok=True)
    with progress.open('x',encoding='utf-8') as journal:
        def note(value):
            journal.write(json.dumps(dict(elapsed_seconds=round(time.monotonic()-started,3),**value))+'\n');journal.flush();os.fsync(journal.fileno())
            require(os.fstat(journal.fileno()).st_size<=JOURNAL_LIMIT,'progress journal byte bound')
        note(dict(state='started',pid=os.getpid(),epoch=operation['epoch'],roots=MAX_ROOTS,recipes=MAX_RECIPES))
        try:
            peak=budget(started);summaries=[];native_reads=0
            def read_native(unit):
                nonlocal native_reads,peak
                peak=max(peak,budget(started));src=(ROOT/unit['source']).resolve();require(src.is_relative_to(ROOT),'foreign selected source')
                finite.pin(src,unit['source_sha256'],observations)
                obj=(prepared['paths']['manifest'].parent/prepared['loaded']['manifest'].get('object_root_relative','.')/unit['object']).resolve()
                require(obj.is_relative_to(ROOT),'foreign selected object')
                with obj.open('rb') as source:raw=source.read(LIMITS['output_bytes']+1)
                require(len(raw)<=LIMITS['output_bytes'],'named original object byte bound')
                peak=max(peak,budget(started))
                require(hashlib.sha256(raw).hexdigest()==unit['object_sha256'],'fresh named object hash differs')
                observations[obj]=unit['object_sha256'];native_reads+=1
                note(dict(state='read_named_recipe_once',recipe_index=unit['recipe_index'],recipe_id=unit['recipe_id']))
                return raw
            provenance=dict(qualified_request_sha256=operation['artifacts']['qualified_request']['sha256'],
                observation_epoch=operation['epoch'],operation_sha256=args.operation_sha256,collector_sha256=operation['source_sha256'],
                saved_authorities={name:ref['sha256'] for name,ref in operation['artifacts'].items()},
                dependency_tools_sha256={p.relative_to(ROOT).as_posix():h for p,h in observations.items() if p.is_relative_to(ROOT/'tools')},
                optional_function_index_present=False,qualified_contract_provenance_restamped=False)
            with tempfile.TemporaryFile() as stage:
                path=prepared['paths']['qualified_records'];size=path.stat().st_size
                with path.open('rb') as source:
                    compressed=DigestingSource(source)
                    with gzip.GzipFile(fileobj=compressed,mode='rb') as incoming,gzip.GzipFile(fileobj=stage,mode='wb',mtime=0) as writer:
                        reader=QualifiedReader(incoming,prepared,operation['artifacts']['qualified_request']['sha256'])
                        for record in stream_observations(prepared,reader,read_native,provenance):
                            writer.write(canonical(record)+b'\n');summaries.append(summary_row(record,len(summaries)+1))
                            require(stage.tell()<=LIMITS['output_bytes'],'staged output bound');peak=max(peak,budget(started))
                        census=reader.finish()
                    compressed.finish(operation['artifacts']['qualified_records']['sha256'],size)
                require(len(summaries)==MAX_RECORDS and native_reads==MAX_RECIPES,'incomplete native observation batch')
                detail_size=stage.seek(0,2);require(detail_size<=LIMITS['output_bytes'],'closed staged output bound')
                stage.seek(0);hasher=hashlib.sha256()
                while block:=stage.read(1048576):hasher.update(block)
                summary=dict(roots=MAX_ROOTS,recipes=MAX_RECIPES,records=len(summaries),
                    singleton_closure=sum(r['closure_observed'] for r in summaries if r['event']=='SINGLE_ROOT_OBSERVATION'),
                    singleton_blocked=sum(not r['closure_observed'] for r in summaries if r['event']=='SINGLE_ROOT_OBSERVATION'),
                    union_closure=sum(r['closure_observed'] for r in summaries if r['event']=='RECIPE_ROOT_UNION_OBSERVATION'),
                    union_blocked=sum(not r['closure_observed'] for r in summaries if r['event']=='RECIPE_ROOT_UNION_OBSERVATION'))
                result=dict(schema_version=1,policy_id=POLICY,status='metadata-only',epoch=operation['epoch'],operation_sha256=args.operation_sha256,
                    source_sha256=operation['source_sha256'],inputs=operation['artifacts'],details_sha256=hasher.hexdigest(),details_bytes=detail_size,
                    summary=summary,observations=summaries,qualified_census=census,native_object_observation_reads=native_reads,
                    native_object_parse_attempts=MAX_RECIPES,original_binding_stream_traversals=0,owner_stream_traversals=0,cache_frame_reads=0,
                    additional_source_and_object_stability_rehash_reads=True,
                    historical_roots_reobserved=0,previous_native_recipe_overlap=prepared['previous_native_recipe_overlap'],
                    current_successor_join=prepared['current_successor_join'],qualified_contracts_preserved=True,input_stability=True,optional_function_index_present=False,
                    observed_input_bindings=[dict(path=p.relative_to(ROOT).as_posix(),sha256=h) for p,h in sorted(observations.items())],
                    peak_memory_bytes=peak,elapsed_seconds=round(time.monotonic()-started,3),**FALSE)
                require(len(canonical(result))+1+detail_size+JOURNAL_LIMIT<=LIMITS['output_bytes'],'complete output including journal reserve bound')
                publish_outputs(out,details,stage,result,observations,index,published,started)
            note(dict(state='complete',receipt_sha256=finite.file_hash(out),details_sha256=result['details_sha256'],summary=summary))
            return result
        except BaseException as error:
            retract_outputs(published)
            note(dict(state='failed',error_type=type(error).__name__));raise


def run(args):
    published=[];state={}
    try:
        result=_run(args,published,state)
        # The journal has durably closed before the final successful return.
        finite.stable(state['observations']);require(not (ROOT/'build/function_index.json').exists(),'optional index appeared at final gate')
        budget(state['started']);verify_outputs(published)
        return result
    except BaseException:
        retract_outputs(published);raise


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('operation','out','details'):parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--operation-sha256',required=True);args=parser.parse_args(argv)
    try:result=run(args)
    except (ValueError,OSError,KeyError,TypeError) as error:parser.exit(2,'cached root observation rejected: '+str(error)+'\n')
    print(json.dumps(result['summary']));return 0


if __name__=='__main__':raise SystemExit(main())
