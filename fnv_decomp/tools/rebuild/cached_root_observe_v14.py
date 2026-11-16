"""V14 finite graph observer; actual execution requires independent external gates.

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

POLICY='cached-context-root-observation-v14'
QUALIFIED_POLICY='cached-CODE-frontier-inventory-v14'
# Fixed finite census; source/input review and lease are external execution gates.
MAX_ROOTS=55
MAX_RECIPES=34
MAX_RECORDS=89
ACTUAL_OPERATION_PROFILE=None
ARTIFACT_PINS={'manifest': {'path': 'build/rebuild/objects-20261103T030230Z-7cfc935c.json', 'sha256': 'bc62a5fb2553431b1e0547d11f366e52efb73096ea8ceb206c556ae5740a53eb'}, 'retained': {'path': 'build/rebuild/retained-verify-full-v3.json', 'sha256': '04d44b73e81982f846bfe8d81806db72ea669586b579ff22007dfd6f7d831297'}, 'recipes': {'path': 'build/units.json', 'sha256': '62f2c8da5f0daa912abdf4576328706711c6561eef7f01c93a89cb71ad46fb6c'}, 'imports': {'path': 'build/rebuild/import-plan-native-v3.json', 'sha256': 'e39b8db63ef73aea57b5dd4963ff29310524644ca36e137cd8b5461a3c90a23f'}, 'prepared_epoch': {'path': 'build/rebuild/prepared-cached-v13-successor-v1/prepared-epoch.json', 'sha256': '2e8a762f851eae7cf133cc5228efdd145ab4b32e70a2872ab527a3f32e6e318c'}, 'prepared_review': {'path': 'build/rebuild/prepared-cached-v13-successor-v1/independent-outcome-review.json', 'sha256': '095a5552bd594d5337f7f112d22f4e3b282dbf571dc9882244781d9a0fbc57dc'}, 'current_groups': {'path': 'build/rebuild/application-link-diagnostic-v14-combined/unresolved-groups-v1.json', 'sha256': '1a88328d4dbde77be1fb571fd4d87439857d14b43472e0ece8eec4e8e3d9c94d'}, 'current_review': {'path': 'build/rebuild/application-link-diagnostic-v14-combined/independent-outcome-review.json', 'sha256': '9e107134eb10c39ee7a768975f627ae64cf28d3d07f3e47dbf260d888eaf573d'}, 'qualified_receipt': {'path': 'build/rebuild/cached-code-frontier-inventory-v14-v1/receipt.json', 'sha256': '2a49890d27943fb87a2b6a036d0c56f27ec472faf8c3fa0d54a1cf13b300584f'}, 'qualified_inventory': {'path': 'build/rebuild/cached-code-frontier-inventory-v14-v1/inventory.json', 'sha256': '2ffdcb6060d79fea95bcb8a4a98d627fa6458a3cbceaf7860ba197e4c4630cfd'}, 'qualified_request': {'path': 'build/rebuild/cached-code-frontier-inventory-v14-v1/metadata-request.json', 'sha256': 'c15ea262418bfd23cea06a4e5cf2c24dbe9bb3a019af7c2f454af0d209bd771c'}, 'qualified_registry': {'path': 'build/rebuild/cached-code-frontier-inventory-v14-v1/cache-registry.json', 'sha256': 'd6ac047f59dbbbac65a6406c494bdba0df56dd281269505f7c079f308e54d7af'}, 'qualified_records': {'path': 'build/rebuild/cached-code-frontier-inventory-v14-v1/metadata-contracts.jsonl.gz', 'sha256': 'bc8e059b012441a6c5ac941afacecc0dcde36a197099e58dcef07deab934ce43'}, 'qualification_main_review': {'path': 'build/rebuild/code-lane01-analysis-v1/cached-code-frontier-inventory-v14-main-outcome-review-v1.json', 'sha256': '258ac698a0b512851064dd5601c125ae56581ff40af54eafdbc08d77f2ee231a'}, 'qualification_authority_review': {'path': 'build/rebuild/code-lane05-synthetic-projection-v1/cached-code-frontier-inventory-v14-outcome-authority-review-v1.json', 'sha256': '90c0a3bd7dd0f3b662747876e1f5693b6943252ea71481757aeb133363bea14e'}, 'qualification_operation': {'path': 'build/rebuild/cached-code-frontier-v14-operation-v1.json', 'sha256': '2c281b4948ea35ca00bfd704d95aa9955f672c32d6108f7cdecdc6253a63e524'}, 'read_reuse_plan': {'path': 'build/rebuild/broad55-prospective-seven-read-reuse-plan-v1.json', 'sha256': 'a29ab5a97db56179fc4db91cb40cc3dd7fe43d97c2ae68cec46ba13483035d74'}}
LATEST_EPOCH_AUTHORITY=None
PREVIOUS_SOURCE_SHA256='a393fadfb27c086e67e5ba8fe415e73757a9597f200ee4810e61be523865b96a'
ROOT_KEYS=previous.ROOT_KEYS
NATIVE_KEYS=previous.NATIVE_KEYS
CONTRACT_KEYS=previous.CONTRACT_KEYS
QUALIFIED_FALSE=previous.QUALIFIED_FALSE
QUALIFIED_KEYS=previous.QUALIFIED_KEYS
FALSE=previous.FALSE
LIMITS={**previous.LIMITS,'seconds':720}
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
DigestingSource=previous.DigestingSource
summary_row=previous.summary_row
publish_outputs=previous.publish_outputs
retract_outputs=previous.retract_outputs
verify_outputs=previous.verify_outputs


def budget(start):
    from coff_inventory import peak_memory_bytes
    require(time.monotonic()-start<=LIMITS['seconds'],'observation time bound')
    peak=peak_memory_bytes()
    require(type(peak) is int and 0<peak<=LIMITS['peak_memory_bytes'],'observation memory bound/counter unavailable')
    return peak

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


# Both metadata qualification outcomes are pinned; the observer itself still
# requires independent source/input review and an external once-only lease.
QUALIFICATION_ARTIFACTS=None
ARTIFACT_KEYS=None
READ_REUSE_PLAN_SHA256='a29ab5a97db56179fc4db91cb40cc3dd7fe43d97c2ae68cec46ba13483035d74'
PREVIOUSLY_READ_PROSPECTIVE_RECIPES=(1445,2769,2770,2779)
PROSPECTIVE_ROOTS=('0x00c43500','0x00c546c0','0x00c55200','0x00c5f240',
                   '0x00c616c0','0x00c618f0','0x00c65530')
PROSPECTIVE_OVERLAP={1445:('0x00c546c0',),2769:('0x00c55200',),
                     2770:('0x00c43500','0x00c5f240'),
                     2779:('0x00c616c0','0x00c618f0','0x00c65530')}


def validate_structural_overlap(groups, plan):
    """Check the explicit seven-root reuse policy; never open a native input.

    This check does not grant operation authority. The caller must separately
    bind the plan's exact file hash and the accepted qualification authorities.
    """
    require(type(groups) is dict and type(plan) is dict,'typed overlap inputs required')
    require(plan.get('kind')=='V14-broad55-prospective-seven-read-reuse-plan' and
        type(plan.get('schema_version')) is int and plan['schema_version']==1 and
        plan.get('status')=='source-plan-not-original-operation-approval', 'overlap plan identity differs')
    broad=plan['broad_request'];prior=plan['prior_actual'];policy=plan['reuse_policy']
    require(broad['sha256']=='c15ea262418bfd23cea06a4e5cf2c24dbe9bb3a019af7c2f454af0d209bd771c' and
        type(broad['requested_roots']) is int and broad['requested_roots']==55 and
        type(broad['requested_recipes']) is int and broad['requested_recipes']==34, 'overlap broad request differs')
    require(prior['raw_byte_cache_reusable'] is False and prior['source_derived_integrity_passes']==3 and
        type(prior['source_derived_integrity_passes']) is int and prior['reported_integrity_passes']==2 and
        type(prior['reported_integrity_passes']) is int and prior['exact_two_pass_conformance'] is False and
        prior['CPP_content_read'] is False and prior['CPP_SHA_authority']=='declared-retained-context-only',
        'prior read limitations differ')
    require(policy['reuse_prior_facts_as_fresh_broad_graph_validation'] is False and
        policy['silent_frozen_observer_widening_allowed'] is False and
        policy['parallel_optional_four_unit_capture_allowed'] is False and
        policy['reuse_prior_selected_structural_facts_as_supplement'] is True and
        policy['future_overlap_payload_observation']=='one necessary broad55 observation under its own exact accepted operation/input/CPU gate',
        'overlap reuse policy differs')
    require(set(groups).issuperset(PROSPECTIVE_OVERLAP) and all(type(k) is int for k in groups), 'overlap recipe roster differs')
    expected=[]
    for index,addresses in PROSPECTIVE_OVERLAP.items():
        rows=groups[index]
        require(type(rows) is list and all(type(r) is dict and type(r.get('recipe_index')) is int and
            r['recipe_index']==index for r in rows), 'overlap root recipe differs')
        actual=[r['original_address'] for r in rows]
        require(len(actual)==len(set(actual)) and set(actual)==set(addresses), 'overlap root scope differs')
        ids={r['recipe_id'] for r in rows};require(len(ids)==1,'overlap recipe identities differ')
        expected.append((next(iter(ids)),set(addresses)))
    entries=plan['overlap_units'];require(type(entries) is list and len(entries)==4,'overlap plan roster differs')
    observed=[]
    for row in entries:
        require(type(row) is dict and set(row)=={'recipe_id','roots'} and type(row['roots']) is list and
            len(row['roots'])==len(set(row['roots'])), 'overlap plan row differs')
        observed.append((row['recipe_id'],set(row['roots'])))
    require(all(item in observed for item in expected) and len({item[0] for item in observed})==4,
        'overlap plan physical recipe differs')
    return dict(roots=list(PROSPECTIVE_ROOTS),recipes=list(PREVIOUSLY_READ_PROSPECTIVE_RECIPES),
        prior_raw_reusable=False,prior_source_derived_integrity_passes=3,prior_reported_integrity_passes=2,
        prior_cpp_hash_authority='declared-retained-context-only')


def validate_qualification_scope(receipt, request, qualified_inventory, registry, groups):
    """Pure metadata join, separate from all file reads and operation authority."""
    require(receipt['policy_id']==QUALIFIED_POLICY and receipt['status']=='metadata-only' and
        all(type(receipt[k]) is int for k in ('qualified_metadata_roots','qualified_recipes','generated_contract_records','code_demands','registry_roots')) and
        (receipt['qualified_metadata_roots'],receipt['qualified_recipes'],receipt['generated_contract_records'],receipt['code_demands'],receipt['registry_roots'])==(55,34,89,626,780) and
        receipt['certificate_created'] is False and receipt['native_observation_required'] is True and
        receipt['metadata_fingerprints_stable'] is True and all(receipt[k] is False for k in
            ('provider_selected','runtime_eligible','native_tools_run','original_objects_read','source_bodies_read','code_emission_performed')),
        'V14 qualification scope/promotion differs')
    require(type(request) is dict and set(request)=={'schema_version','kind','roots'} and
        type(request['schema_version']) is int and request['schema_version']==1 and
        request['kind']=='fnv-finite-ordinary-root-request' and type(request['roots']) is list and len(request['roots'])==55,
        'exact V14 root request required')
    require(typed_equal(qualified_inventory['metadata_requests'],request['roots']) and
        len(qualified_inventory['records'])==626, 'qualified V14 inventory differs')
    expected={r['original_address']:r for r in request['roots']}
    require(len(expected)==55 and type(registry['roots']) is int and registry['roots']==780 and
        len(registry['records'])==780 and not (set(expected)&set(registry['records'])), 'historical root replay/registry differs')
    require(type(groups) is dict and len(groups)==34 and all(type(i) is int for i in groups) and
        typed_equal(receipt['requested_recipe_indices'],sorted(groups)) and receipt['requested_recipe2768'] is False and
        2768 not in groups, 'qualified recipe scope differs')
    flattened=[r for rows in groups.values() for r in rows]
    require(len(flattened)==55 and len({r['original_address'] for r in flattened})==55 and
        all(r['original_address'] in expected and typed_equal(r,expected[r['original_address']]) and
            type(r['recipe_index']) is int and r['recipe_index']==i
            for i,rows in groups.items() for r in rows), 'qualified grouped physical roots differ')
    frames={}
    for row in receipt['recipe_frame_verifications']:
        i=row['recipe_index'];require(type(i) is int and i not in frames and i in groups and
            type(row['requested_roots']) is int and row['requested_roots']==len(groups[i]) and
            type(row['verification']['recipe_index']) is int and row['verification']['recipe_index']==i,
            'qualified frame identity differs')
        frames[i]=row
    require(set(frames)==set(groups),'qualified frame roster differs')
    singles={}
    for item in qualified_inventory['records']:
        if item.get('inventory_action')!='REQUEST_CACHED_METADATA':continue
        root=item['root'];a=root['original_address'];entry=item['new_metadata']
        require(a in expected and a not in singles and typed_equal(root,expected[a]) and
            type(entry['contract_record_ordinal']) is int and 1<=entry['contract_record_ordinal']<=89 and
            all(isinstance(entry[k],str) and re.fullmatch('[0-9a-f]{64}',entry[k]) for k in
                ('generated_record_sha256','new_metadata_contract_sha256')), 'qualified singleton index differs')
        singles[a]=entry
    require(set(singles)==set(expected) and len({e['contract_record_ordinal'] for e in singles.values()})==55,
        'qualified singleton coverage/ordinals differ')
    return dict(frames=frames,singleton_index=singles)


def validate_frontier_context(request, qualified_inventory, current_groups, epoch):
    """Join each requested physical owner to the reviewed V14 frontier and epoch."""
    providers={r['original_address']:{k:r[k] for k in ('recipe_id','object_sha256','symbol_index')} for r in request['roots']}
    require(len(providers)==55, 'requested physical namespace differs')
    require(current_groups['kind']=='actual-unresolved-LNK-target-groups' and current_groups['executable_execution'] is False and
        current_groups['runtime_eligible'] is False, 'current diagnostic authority differs')
    code_rows=[r for r in current_groups['groups'] if r['classification']=='CODE']
    code={r['symbol']:r for r in code_rows};names=[r['symbol'] for r in qualified_inventory['records']]
    require(len(code_rows)==len(code)==len(names)==len(set(names))==626 and set(names)==set(code),
        'V14 CODE demand census differs')
    require(type(epoch['schema_version']) is int and epoch['schema_version']==9 and
        epoch['kind']=='prepared-CODE-collision-exclusions' and epoch['policy_id']=='prepared-cached-V13-successor-v1' and
        type(epoch['ordinary_prepared_count']) is int and epoch['ordinary_prepared_count']==14550 and
        type(epoch['collision_exclusion_count']) is int and epoch['collision_exclusion_count']==14556 and
        len(epoch['records'])==len(epoch['exclusion_names'])==len(set(epoch['exclusion_names']))==14556 and
        len(epoch['ordinary_names'])==len(set(epoch['ordinary_names']))==14550 and
        epoch['application_selected_code_count'] is None and epoch['application_selection_inferred_from_counts'] is False and
        'application_manifest_adopted' not in epoch and epoch['provider_selected'] is False and epoch['runtime_eligible'] is False,
        'accepted collision-only epoch differs')
    requested_names=[]
    for root in request['roots']:
        a=root['original_address'];require(a in providers,'requested root absent from selection')
        name='_fnv_code_'+digest(providers[a]);item=code.get(name)
        require(item is not None and item['observed_roles']==['code'] and item['included_provenance_is_extraction_proof'] is False and
            a in item['original_bases'], 'requested physical owner absent from current demand')
        requested_names.append(name)
    require(len(set(requested_names))==55 and not set(requested_names).intersection(epoch['exclusion_names']),
        'requested owners duplicate or collide with prepared epoch')
    return providers


def validate_current_reviews(prepared_review, current_review, epoch_sha256, groups_sha256):
    require(prepared_review['kind']=='independent-prepared-cached-v13-successor-outcome-review' and
        prepared_review['status']=='accepted-derived-metadata-only' and prepared_review['epoch_sha256']==epoch_sha256,
        'prepared epoch independent review differs')
    require(current_review['kind']=='independent-wave14-combined-diagnostic-link-outcome-review' and
        current_review['status']=='accepted-failed-link-diagnostic-only' and current_review['groups_sha256']==groups_sha256 and
        type(current_review['link_exit_code']) is int and current_review['link_exit_code']==1120 and
        current_review['executable_execution'] is False and current_review['provider_adopted'] is False and
        current_review['runtime_eligible'] is False and current_review['loaded_member_enumeration_claimed'] is False,
        'current diagnostic independent review differs')


def validate_import_authority(imports,proof,manifest_sha256,retained_sha256):
    require(imports['inputs']['manifest']==manifest_sha256 and imports['inputs']['retained']==retained_sha256 and
        imports['inputs']['reference']==proof['inputs']['image_sha256'], 'import/reference authority differs')
    imported=[r for r in imports['imports'] if type(r['import_id']) is int and r['import_id']==175]
    require(len(imported)==1,'exact import175 required')
    return imported[0]


def require_actual_authority():
    # The reviewed operation and external lease/watchdog gates remain mandatory.
    require(type(ARTIFACT_PINS) is dict and len(ARTIFACT_PINS)==17 and
        READ_REUSE_PLAN_SHA256==ARTIFACT_PINS['read_reuse_plan']['sha256'], 'V14 fixed authority pins differ')


def validate_operation_envelope(operation, allowed_artifacts):
    """Pure exact path-and-hash whitelist check; this does not authorize a run."""
    require(type(operation) is dict and set(operation)=={'schema_version','kind','policy_id','epoch','roots','recipes','records',
        'limits','artifacts','source_sha256'}, 'unknown V14 operation envelope')
    require(type(operation['schema_version']) is int and operation['schema_version']==1 and
        operation['kind']=='whole-qualified-contract-native-observation' and operation['policy_id']==POLICY and
        type(operation['epoch']) is str and 0<len(operation['epoch'])<=100 and operation['epoch'].isascii(), 'operation identity differs')
    require(all(type(operation[k]) is int for k in ('roots','recipes','records')) and
        (operation['roots'],operation['recipes'],operation['records'])==(55,34,89) and typed_equal(operation['limits'],LIMITS),
        'operation census/limits differ')
    require(type(operation['source_sha256']) is str and re.fullmatch('[0-9a-f]{64}',operation['source_sha256']), 'observer SHA differs')
    require(type(allowed_artifacts) is dict and allowed_artifacts and type(operation['artifacts']) is dict and
        typed_equal(operation['artifacts'],allowed_artifacts), 'exact V14 role/path/hash whitelist required')
    paths=[]
    for ref in allowed_artifacts.values():
        require(type(ref) is dict and set(ref)=={'path','sha256'} and type(ref['path']) is str and ref['path'] and
            type(ref['sha256']) is str and re.fullmatch('[0-9a-f]{64}',ref['sha256']), 'artifact reference differs')
        raw=Path(ref['path']);path=(ROOT/raw).resolve()
        require(not raw.is_absolute() and path.is_relative_to(ROOT) and '..' not in raw.parts,
            'foreign or noncanonical artifact path')
        paths.append(path)
    require(len(set(paths))==len(paths),'artifact path collision')
    return operation


def validate_operation(operation):
    require_actual_authority()
    return validate_operation_envelope(operation,ARTIFACT_PINS)


def prepare_operation(operation,observations,started=None):
    require_actual_authority()
    validate_operation(operation)
    paths={name:(ROOT/ref['path']).resolve() for name,ref in operation['artifacts'].items()}
    refs=operation['artifacts'];loaded={}
    for name,path in paths.items():
        if name=='qualified_records':continue
        loaded[name]=read_bound_json(path,refs[name]['sha256']);observations[path]=refs[name]['sha256']
        if started is not None:budget(started)
    receipt=loaded['qualified_receipt']
    for role,filename in (('qualified_inventory','inventory.json'),('qualified_request','metadata-request.json'),
            ('qualified_registry','cache-registry.json'),('qualified_records','metadata-contracts.jsonl.gz'),
            ('prepared_epoch','prepared-epoch.json')):
        require(receipt['output_sha256'][filename]==refs[role]['sha256'],'qualified receipt output identity differs')
    observations[paths['qualified_records']]=refs['qualified_records']['sha256']
    validate_current_reviews(loaded['prepared_review'],loaded['current_review'],refs['prepared_epoch']['sha256'],refs['current_groups']['sha256'])
    main=loaded['qualification_main_review'];peer=loaded['qualification_authority_review']
    require(main['approved'] is True and main['status']=='accepted-metadata-only' and
        main['independent_saved_output_review_pass'] is True and peer['approved'] is True and
        peer['all_requested_roots_and_union_records_present'] is True and
        main['receipt_sha256']==peer['receipt_sha256']==refs['qualified_receipt']['sha256'] and
        main['operation_sha256']==peer['operation_sha256']==refs['qualification_operation']['sha256'] and
        main['complementary_outcome_review_sha256']==refs['qualification_authority_review']['sha256'] and
        main['saved_epoch_sha256']==refs['prepared_epoch']['sha256'] and
        main['request_artifact_sha256']==refs['qualified_request']['sha256'] and
        main['metadata_contracts_sha256']==refs['qualified_records']['sha256'] and
        main['native_observation_required'] is True and main['zero_binding_roots_remain_native_UNKNOWN'] is True and
        all(review['certificate_created'] is False and review['provider_selected'] is False and
            review['runtime_eligible'] is False for review in (main,peer)), 'qualification review authority differs')
    validate_frontier_context(loaded['qualified_request'],loaded['qualified_inventory'],loaded['current_groups'],loaded['prepared_epoch'])
    groups={}
    for root in loaded['qualified_request']['roots']:
        index=root['recipe_index'];require(type(index) is int and index>=0,'typed recipe index required')
        groups.setdefault(index,[]).append(root)
    units={u['recipe_index']:u for u in loaded['manifest']['units']}
    proofs={p['recipe_index']:p for p in loaded['retained']['units']}
    require(len(units)==len(loaded['manifest']['units']) and len(proofs)==len(loaded['retained']['units']), 'duplicate unit/proof recipe')
    for index,roots in groups.items():
        require(index in units and index in proofs,'selected unit/proof missing')
        validate_roots(units[index],proofs[index],roots)
    prepared=validate_qualification_scope(receipt,loaded['qualified_request'],loaded['qualified_inventory'],loaded['qualified_registry'],groups)
    overlap=validate_structural_overlap(groups,loaded['read_reuse_plan'])
    imports=loaded['imports'];proof=loaded['retained']
    imported=validate_import_authority(imports,proof,refs['manifest']['sha256'],refs['retained']['sha256'])
    require(finite.reconcile_recipes(loaded['manifest'],paths['recipes'])['verified'],'recipe epoch differs')
    finite.pin(Path(__file__),operation['source_sha256'],observations)
    for name,expected in proof['inputs']['tools_sha256'].items():
        path=(ROOT/name).resolve();require(path.is_relative_to(ROOT),'foreign retained proof dependency');finite.pin(path,expected,observations)
    prepared.update(groups=groups,units=units,proofs=proofs,imported=imported,loaded=loaded,paths=paths,
        prior_seven_root_structural_overlap=overlap,current_successor_join=dict(epoch_sha256=refs['prepared_epoch']['sha256'],
            current_demand_sha256=refs['current_groups']['sha256'],requested_names_disjoint=True))
    return prepared


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
        if hasher.hexdigest()!=expected:raise ValueError('frozen V14 observation helper changed')
        if path in observations and observations[path]!=expected:raise ValueError('conflicting helper identity')
        observations[path]=expected
    for module,name in ((previous,'cached_root_observe.py'),(coff,'coff_code_archive.py'),(ordinary,'root_code_closure.py'),
                         (inventory,'runtime_code_inventory.py'),(finite,'scalableordinary_root_collect.py')):
        if Path(module.__file__).resolve()!=ROOT/'tools/rebuild'/name:raise ValueError('foreign imported observation dependency')
    if started is not None:budget(started)


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
                    historical_registry_roots_reobserved=0,prior_seven_root_structural_overlap=prepared['prior_seven_root_structural_overlap'],
                    graph_observation_scope='physical primary symbols, section metadata, ordinary edges and SafeSEH including omitted relocations',
                    graph_observation_excludes=['whole EH closure','HIGHLOW closure','raw-byte proof'],
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
