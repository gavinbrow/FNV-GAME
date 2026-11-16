"""V14 source-only candidate selection seam. No production authority is bound.

Actual operation, source pins, outcomes, and resource authority remain pending.
This module performs no file access and cannot launch a production operation.
"""
from collections import Counter, defaultdict
import copy
import re
import cached_frontier_code_factory_v13 as previous
import cached_root_observe_v14 as native

base=previous.base
require=previous.require
digest=previous.digest
sha=previous.sha
exact=native.typed_equal
QUARANTINES=previous.QUARANTINES

def prepared_nonadmission(prepared):
    require(type(prepared.get('schema_version')) is int and prepared['schema_version']==9 and
        prepared.get('policy_id')=='prepared-cached-V13-successor-v1' and
        prepared.get('application_selected_code_count','ABSENT') is None and
        prepared.get('historical_records_preserved') is True and
        ('application_manifest_adopted' not in prepared or prepared['application_manifest_adopted'] is False) and
        all(prepared.get(k) is False for k in ('application_selection_inferred_from_counts','provider_selected',
            'runtime_eligible','ABI_verified','admission_decision_created','certificate_created','closure_inferred',
            'code_emission_performed','emission_performed','full_serialization_eligible','link_ready',
            'materialization_approved','namespace_approved')),
        'accepted V14 collision epoch cannot imply admission')

def qualified_view(record):
    """Reconstruct the exact original metadata row, without restamping it."""
    identity=record['qualified_metadata_identity']
    row=dict(identity,requested_roots=record['requested_roots'],contract=record['contract'],
        contract_sha256=record['contract_identity_sha256'],new_metadata_contract_sha256=record['contract_identity_sha256'])
    for key in native.QUALIFIED_FALSE:row.setdefault(key,False)
    require(set(row)==native.QUALIFIED_KEYS and type(row['schema_version']) is int and row['schema_version']==1 and
        row['kind']=='new-cached-metadata-contract' and row['policy_id']==native.QUALIFIED_POLICY and
        all(row[k] is False for k in native.QUALIFIED_FALSE) and
        row['native_observation_required'] is True and digest(row)==record['qualified_metadata_row_sha256'],
        'native observation changed its original qualified metadata row')
    return row

def select_candidates(receipt,records,qualification_request,current_groups,prepared,*,
        expected_census,expected_current_codes,expected_prepared,receipt_sha256,on_selected=None):
    """Stream all observations; select every positive SINGLE event only."""
    require(type(expected_census) is tuple and len(expected_census)==3 and
        all(type(n) is int and 0<n<=89 for n in expected_census) and
        expected_census[0]<=55 and expected_census[1]<=34 and
        type(expected_current_codes) is int and 0<expected_current_codes<=626 and
        type(expected_prepared) is tuple and len(expected_prepared)==2 and
        all(type(n) is int and 0<=n<=100000 for n in expected_prepared) and sha(receipt_sha256),
        'explicit bounded exact integer census and receipt hash required')
    expected_roots,expected_recipes,expected_records=expected_census
    require(sha(receipt_sha256) and type(receipt.get('schema_version')) is int and receipt['schema_version']==1 and
        receipt['policy_id']==native.POLICY and receipt['status']=='metadata-only' and
        receipt.get('graph_observation_scope')=='physical primary symbols, section metadata, ordinary edges and SafeSEH including omitted relocations' and
        receipt.get('graph_observation_excludes')==['whole EH closure','HIGHLOW closure','raw-byte proof'] and
        receipt.get('additional_source_and_object_stability_rehash_reads') is True and
        receipt['input_stability'] is True and receipt['optional_function_index_present'] is False and
        receipt['qualified_contracts_preserved'] is True and type(receipt['historical_registry_roots_reobserved']) is int and receipt['historical_registry_roots_reobserved']==0 and
        all(type(receipt[k]) is int and receipt[k]==0 for k in ('original_binding_stream_traversals','owner_stream_traversals','cache_frame_reads')) and
        all(receipt[k] is False for k in native.FALSE),'accepted fresh ordinary observation envelope required')
    require(all(type(receipt['summary'][k]) is int and receipt['summary'][k]==v for k,v in
        [('roots',expected_roots),('recipes',expected_recipes),('records',expected_records)]) and
        len(receipt['observations'])==expected_records and type(receipt['native_object_observation_reads']) is type(receipt['native_object_parse_attempts']) is int and
        receipt['native_object_observation_reads']==receipt['native_object_parse_attempts']==expected_recipes,
        'whole finite native observation census differs')
    require(qualification_request['kind']=='fnv-finite-ordinary-root-request' and type(qualification_request['schema_version']) is int and
        qualification_request['schema_version']==1 and len(qualification_request['roots'])==expected_roots,'whole qualified request required')
    wanted={r['original_address']:r for r in qualification_request['roots']};by_recipe=defaultdict(list)
    require(len(wanted)==expected_roots,'duplicate qualified root')
    for root in wanted.values():
        require(set(root)==native.ROOT_KEYS and all(type(root[k]) is int for k in ('recipe_index','symbol_index','section','value','size')) and
            0<=root['recipe_index']<10000 and root['symbol_index']>=0 and root['section']>0 and root['value']>=0 and root['size']>0 and
            type(root['original_address']) is str and re.fullmatch(r'0x[0-9a-f]{8}',root['original_address']) is not None and
            type(root['recipe_id']) is str and bool(root['recipe_id']) and
            sha(root['object_sha256']) and sha(root['source_sha256']),'typed exact native physical root')
        by_recipe[root['recipe_index']].append(root)
    require(len(by_recipe)==expected_recipes and
        all(len({r['recipe_id'] for r in rows})==1 for rows in by_recipe.values()) and
        len({rows[0]['recipe_id'] for rows in by_recipe.values()})==expected_recipes,
        'whole qualified recipe request with coherent recipe identity')
    require(prepared['kind']=='prepared-CODE-collision-exclusions' and all(type(prepared[k]) is int for k in ('ordinary_prepared_count','collision_exclusion_count')) and
        (prepared['ordinary_prepared_count'],prepared['collision_exclusion_count'])==expected_prepared and
        len(prepared['exclusion_names'])==len(set(prepared['exclusion_names']))==expected_prepared[1] and
        prepared['application_selection_inferred_from_counts'] is False,'exact prepared collision epoch')
    prepared_nonadmission(prepared)
    exports=set(prepared['exclusion_names'])
    require(current_groups['kind']=='actual-unresolved-LNK-target-groups' and current_groups['executable_execution'] is False and current_groups['runtime_eligible'] is False,
        'actual nonexecuted current LINK groups')
    current_rows=[g for g in current_groups['groups'] if g['classification']=='CODE'];current={g['symbol']:g for g in current_rows}
    require(type(current_groups['classifications']['CODE']) is int and len(current)==len(current_rows)==current_groups['classifications']['CODE']==expected_current_codes and
        all(type(g['original_bases']) is list and g['original_bases'] and len(g['original_bases'])==len(set(g['original_bases'])) and
            all(type(a) is str and re.fullmatch(r'0x[0-9a-f]{8}',a) is not None for a in g['original_bases']) for g in current_rows),
        'whole unique current CODE namespace and canonical base lists')
    singles={};unions=set();ledger=[];selected=[];pending_callbacks=[];callback_bytes=0;seen_records=0;counts=Counter();last_recipe=-1
    for ordinal,record in enumerate(records,1):
        seen_records+=1;require(ordinal<=expected_records,'extra observation record')
        summary=receipt['observations'][ordinal-1]
        require(exact(native.summary_row(record,ordinal),summary),'entire native record differs from accepted receipt summary')
        roots=record['requested_roots'];require(roots and all(r['original_address'] in wanted and exact(r,wanted[r['original_address']]) for r in roots) and
            len({r['original_address'] for r in roots})==len(roots),'borrowed or duplicate observed roots')
        index=roots[0]['recipe_index'];require(index>=last_recipe and all(r['recipe_index']==index for r in roots),'mixed/unsorted observed recipe');last_recipe=index
        event=record['event'];contract=record['contract'];certificate=record.get('certificate')
        require(record['schema_version']==1 and type(record['schema_version']) is int and record['kind']=='fresh-root-observation-from-qualified-contract' and
            record['policy_id']==native.POLICY and all(record[k] is False for k in native.FALSE) and record['qualified_contract_unchanged'] is True and
            set(contract)==native.CONTRACT_KEYS and contract['recipe_id']==record['recipe_id']==roots[0]['recipe_id'] and
            type(record['recipe_index']) is int and record['recipe_index']==index and digest(contract)==record['contract_identity_sha256'] and
            contract['export_policy']==base.ordinary.EXPORT_POLICY and
            exact(contract['roots'],[{k:r[k] for k in native.NATIVE_KEYS} for r in roots]) and
            all(contract[k] is True for k in ('verified_match','fields_complete','missing_fields_complete','unit_proofs_complete')) and
            record['native_object_sha256']==roots[0]['object_sha256'] and
            contract['provenance']['object_sha256']==roots[0]['object_sha256'] and contract['provenance']['source_sha256']==roots[0]['source_sha256'] and
            all(r['object_sha256']==roots[0]['object_sha256'] and r['source_sha256']==roots[0]['source_sha256'] for r in roots),
            'unchanged exact observed contract/native provenance')
        q=qualified_view(record);require(type(record['qualified_record_ordinal']) is int and record['qualified_record_ordinal']==ordinal,
            'exact original qualified ordinal')
        p=record['observation_provenance']
        require(p['qualified_request_sha256']==receipt['inputs']['qualified_request']['sha256']==contract['provenance']['request_sha256'] and
            p['operation_sha256']==receipt['operation_sha256'] and p['collector_sha256']==receipt['source_sha256'] and
            p['saved_authorities']=={k:v['sha256'] for k,v in receipt['inputs'].items()} and
            p['optional_function_index_present'] is p['qualified_contract_provenance_restamped'] is False and
            record['qualified_metadata_identity']['event']==('SINGLE_ROOT_METADATA_CONTRACT' if event=='SINGLE_ROOT_OBSERVATION' else 'RECIPE_UNION_METADATA_CONTRACT'),
            'original qualification/collector/source authorities restamped or borrowed')
        require(type(record['closure_observed']) is bool and type(record['graph_observation_complete']) is bool and
            type(record['root_closure_candidate']) is bool and type(record['native_parse_performed']) is bool,'typed original outcome flags')
        if certificate is not None:
            require(record['native_parse_performed'] is record['fresh_certificate_created'] is True and
                certificate['policy_id']==base.ordinary.POLICY and digest(certificate)==record['certificate_sha256'] and
                certificate['contract_identity_sha256']==record['contract_identity_sha256'] and exact(certificate['roots'],contract['roots']) and
                exact(certificate['provenance'],contract['provenance']) and certificate['export_policy']==contract['export_policy'] and certificate['recipe_id']==contract['recipe_id'] and
                all(certificate[k] is record[k] for k in ('closure_observed','graph_observation_complete','root_closure_candidate')) and
                exact(certificate['blockers'],record['blockers']) and all(certificate[k] is False for k in (*base.ordinary.FALSE,'full_serialization_eligible')),
                'fresh unedited ordinary certificate required')
        else:require(record['native_parse_performed'] is record['fresh_certificate_created'] is False and record['closure_observed'] is False and
            record['graph_observation_complete'] is False and record['blockers'],'missing original certificate cannot become positive')
        positive=record['closure_observed']
        require(not positive or (record['graph_observation_complete'] is record['root_closure_candidate'] is True and certificate is not None and not record['blockers']),'contradictory positive graph')
        if event=='SINGLE_ROOT_OBSERVATION':
            require(len(roots)==1 and index not in unions,'singleton scope/order differs');root=roots[0];a=root['original_address'];require(a not in singles,'duplicate singleton')
            singles[a]=True;counts['singleton_closure' if positive else 'singleton_blocked']+=1
            name=base.pool.canonical({k:root[k] for k in ('recipe_id','object_sha256','symbol_index')});group=current.get(name)
            require(group is not None and group['observed_roles']==['code'] and group['included_provenance_is_extraction_proof'] is False and a in group['original_bases'],
                'qualified singleton absent from current exact CODE demand')
            if positive:
                require(name not in exports and a not in QUARANTINES,'positive singleton competes with prepared/quarantined namespace')
                authority=dict(kind='cached-qualified-native-singleton',receipt_sha256=receipt_sha256,ordinal=ordinal,record_sha256=digest(record),
                    certificate_sha256=record['certificate_sha256'],contract_identity_sha256=record['contract_identity_sha256'],
                    qualified_record_ordinal=record['qualified_record_ordinal'],qualified_metadata_row_sha256=record['qualified_metadata_row_sha256'])
                selection=dict(root=root,authority=authority,current_group_sha256=digest(group));selected.append(selection)
                if on_selected is not None:
                    callback_bytes+=len(native.canonical(record))
                    require(callback_bytes<=128*1024*1024,'bounded deferred callback evidence')
                    pending_callbacks.append((copy.deepcopy(record),copy.deepcopy(selection)))
            state='ALL_POSITIVE_SINGLETON_REQUESTED' if positive else 'ORIGINAL_NEGATIVE_PRESERVED'
        elif event=='RECIPE_ROOT_UNION_OBSERVATION':
            require(index not in unions and {r['original_address'] for r in roots}=={r['original_address'] for r in by_recipe[index]} and
                all(r['original_address'] in singles for r in roots),'complete recipe union required after all singletons')
            unions.add(index);counts['union_closure' if positive else 'union_blocked']+=1;state='RECIPE_UNION_EVIDENCE_ONLY'
        else:raise ValueError('unknown observed event')
        ledger.append(dict(event=event,roots=roots,ordinal=ordinal,record_sha256=digest(record),certificate_sha256=record.get('certificate_sha256'),
            contract_identity_sha256=record['contract_identity_sha256'],qualified_metadata_row_sha256=record['qualified_metadata_row_sha256'],state=state,
            closure_observed=record['closure_observed'],graph_observation_complete=record['graph_observation_complete'],blocker_codes=summary['blocker_codes']))
        del q,contract,certificate,p,record
    require(seen_records==expected_records and set(singles)==set(wanted) and unions==set(by_recipe) and
        all(type(receipt['summary'][k]) is int and receipt['summary'][k]==counts[k] for k in ('singleton_closure','singleton_blocked','union_closure','union_blocked')),
        'complete observed outcome partition differs')
    selected.sort(key=lambda s:s['root']['original_address'])
    for callback_record,callback_selection in pending_callbacks:
        on_selected(callback_record,callback_selection)
    return dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=[s['root'] for s in selected]),selected,ledger

def validate_selected(record,selection):
    root=selection['root'];a=selection['authority'];contract=record['contract'];cert=record['certificate']
    require(set(a)=={'kind','receipt_sha256','ordinal','record_sha256','certificate_sha256','contract_identity_sha256','qualified_record_ordinal','qualified_metadata_row_sha256'} and
        a['kind']=='cached-qualified-native-singleton' and sha(a['receipt_sha256']) and type(a['ordinal']) is int and a['ordinal']>0 and
        a['ordinal']==a['qualified_record_ordinal'] and
        type(a['qualified_record_ordinal']) is int and a['qualified_record_ordinal']==record['qualified_record_ordinal'] and
        a['qualified_metadata_row_sha256']==record['qualified_metadata_row_sha256'] and all(record[k] is False for k in native.FALSE) and
        record['native_parse_performed'] is record['fresh_certificate_created'] is True and
        record['event']=='SINGLE_ROOT_OBSERVATION' and exact(record['requested_roots'],[root]) and
        record['closure_observed'] is record['graph_observation_complete'] is record['root_closure_candidate'] is True and
        digest(record)==a['record_sha256'] and digest(contract)==record['contract_identity_sha256']==a['contract_identity_sha256']==cert['contract_identity_sha256'] and
        digest(cert)==record['certificate_sha256']==a['certificate_sha256'] and exact(cert['provenance'],contract['provenance']) and
        cert['closure_observed'] is cert['graph_observation_complete'] is True and not cert['blockers'] and
        all(cert[k] is False for k in (*base.ordinary.FALSE,'full_serialization_eligible')),
        'exact unchanged selected native singleton/certificate/contract')
    qualified_view(record)

def validate_operation(_operation):
    """Fail before any artifact access until a reviewed V14 profile exists."""
    raise ValueError('V14 production authority and independent actual outcomes remain pending')
