"""Versioned COMDAT ANY projection adapter; frozen negative certificates remain."""
from __future__ import annotations
from collections import Counter
import argparse
import gzip
import json
import os
from pathlib import Path
import struct
import sys
import time
import re

import comdat_any_frontier_observer as observer
import comdat_any_code_projection as core
import ordinary_relocation_factory as ordinary_factory
import composed_relocation_factory as field_audit
import current_code_frontier as frontier

base=observer.base
ROOT=base.ROOT
POLICY='finite-comdat-any-frontier-projection-v1'
OWNED=('tools/rebuild/comdat_any_frontier_factory.py','tests/rebuild/test_comdat_any_frontier_factory.py',
       'docs/rebuild/COMDAT-ANY-FRONTIER-FACTORY.md')
FALSE={k:v for k,v in dict(core.FALSE,application_manifest_adopted=False,native_archive_conformance_verified=False).items()
       if k!='emission_performed'}
require=base.require
digest=base.digest
exact=observer.exact
LIMITS=dict(seconds=900,peak_memory_bytes=1024**3,output_bytes=128*1024**2)
PINS={**ordinary_factory.PINS,**observer.PINS,
    'tools/rebuild/comdat_any_frontier_observer.py':'744bf379942e960e2ec170dd325b54eb51713e873bc2e8bf5ba5799345ffc625',
    'tools/rebuild/comdat_any_code_projection.py':'be4fe7b811316630fd77649162d66912580d4516389fc42f50b5870b9ebf7fb7',
    'tools/rebuild/ordinary_relocation_factory.py':'f431d8599d7e91e2c67ed5570ccd067bdf80fbd8a92ee4c6daa3473cc26c928b',
    'tools/rebuild/composed_relocation_factory.py':'34e9ad9ccfb10943c2fc4c10ea57e28dae8312dc442621ed8045cbeb2b649477',
    'tools/rebuild/current_code_frontier.py':'34ad6b6aacf0a9c5b0cfd68cf26fdd57e18cec4f9b74e24b48296049703397bc'}
ARTIFACTS={'observer_receipt','observer_details','observer_request','observer_context','observer_input_review',
    'observer_main_review','observer_authority_review','upstream_epoch','code68_members','code68_receipt','code68_handoff',
    'code68_outcome_review','code68_authority_review','code68_handoff_review','latest_prepared_epoch',
    'manifest','retained','selection','owners','recipes','frontier','image_check','provider_map_review'}
ACCEPTANCES={
    'observer_freeze':'45ec7588f65622f6f5233b89fdb676b075f6384234f5b3584c1d8b36d764d256',
    'observer_source_review':'0ba29d84efb7357f741c6843c3904cd773ee737ffe15484078a6045c4ef2f54c',
    'observer_source_authority_review':'970be53fba8a4569ecec44f606e44a0928863dc19f2a51155a6cfca1f2d89a22',
    'core_source_review':'d6232107013645ed452e1346c1b07c9e4ccfe3549f7fed5121230c6f45ceb04d',
    'core_source_authority_review':'a4def4f92e05d817e66db4b7a4999d78e15aaaccec3a9fdc4b42b99b0d400cb9'}
SOURCE_ARTIFACT_PINS={
    'observer_receipt':'6a52f19cb3aaed9a7827190772338f3c169b98accda4d3151580784aebaef33e',
    'observer_details':'82d711379b74c21c89891ec840a84b470bfba4f9933dac5303cdf7a77629e43c',
    'observer_request':'dd723c2c1ad94ba2e7ece7ab8ac5322dc3efd73cd5119fa20269b75aa409e25a',
    'observer_main_review':'529a838d6d3377749f30e5836f5c830f39b02699a053763a7485d6ee213cc9fd',
    'observer_authority_review':'d875f577c8d411f13c89ea365aa53140c3517ad1b76074f1a7b803c881b155ec',
    'upstream_epoch':observer.METADATA_PINS['prepared_epoch'],'frontier':observer.METADATA_PINS['frontier'],
    'code68_members':'611947ef6be7a3c3f0892736aad38010b671f352236d9ce59c4d17ee6a9c03e0',
    'code68_receipt':'fc70978eacc52e261d6cd65165a42d0162959fc36627419b5c44876668610898',
    'code68_outcome_review':'99070a715d0ff7322b8ab6741208deb9229d142cfc1dacf8aada04769fdf5379',
    'code68_authority_review':'767fea0b3553885bae63611309944c3975ffa7b55f5459dde58e16212c6c0215',
    'provider_map_review':ordinary_factory.MAP_REVIEW[1],
    **{n:base.inventory.EXPECTED[n] for n in ('manifest','retained','selection','owners','recipes')}}


def validate_code68(members,receipt,handoff,refs):
    """Accepted source metadata only; no archived CODE body is re-read."""
    require(receipt.get('status')=='completed-incomplete' and receipt.get('inputs_stable') is True and
        all(type(receipt.get(k)) is int and receipt[k]==n for k,n in [('requested',70),('emitted',68),('blocked',2),('fields',629),('code_bytes',8825)]) and
        receipt['output_sha256']['members.json']==refs['code68_members']['sha256'] and
        all(receipt.get(k) is False for k in ('provider_selected','runtime_eligible','native_tools_run','compiler_performed',
            'executable_link_performed','game_execution_performed','application_manifest_adopted')),
        'accepted full CODE68 producer outcome required')
    require(type(handoff.get('schema_version')) is int and handoff['schema_version']==1 and
        handoff.get('kind')=='accepted-prepared-CODE-export-handoff' and handoff.get('cohort')=='V8-new259-bare-positive-68' and
        handoff.get('operation_status')=='completed-incomplete' and
        all(type(handoff.get(k)) is int and handoff[k]==n for k,n in [('new_distinct_exports',68),('requested_candidates',70),
            ('quarantined_candidates',2),('upstream_ordinary_prepared_count',14403),('upstream_collision_exclusion_count',14409),
            ('successor_ordinary_prepared_count',14471),('successor_collision_exclusion_count',14477),('full_field_proof_schema_version',1),
            ('full_field_proof_records',68),('full_field_proof_rows',629)]) and
        handoff.get('source_field_evidence_enriched') is False and handoff.get('requires_successor_exclusion_epoch') is True and
        all(handoff.get(k) is False for k in ('provider_selected','runtime_eligible','native_tools_run','compiler_performed',
            'executable_link_performed','game_execution_performed','application_manifest_adopted','application_cohort_adopted')),
        'accepted CODE68 handoff count/authority scope differs')
    for field,name in [('members','code68_members'),('producer_receipt','code68_receipt'),
        ('independent_outcome_review','code68_outcome_review'),('complementary_review','code68_authority_review')]:
        require(handoff[field]['sha256']==refs[name]['sha256'],'CODE68 handoff borrowed artifact: '+field)
    require(handoff['archive']['sha256']==receipt['archive_sha256'] and
        handoff['field_proofs']['sha256']==receipt['output_sha256']['field-proofs.jsonl.gz'] and
        type(members) is list and len(members)==len(handoff['records'])==68,'CODE68 complete member/proof/archive identity')
    for ordinal,(member,h) in enumerate(zip(members,handoff['records']),1):
        p=member['projection'];root=p['requested_roots'][0];name=base.pool.canonical(observer.selector.root_identity(root))
        require(h['member']==member['name'] and h['member_sha256']==p['output_sha256'] and h['canonical']==name and
            exact(h['root'],root) and exact(h['authority'],p['authority']) and
            h['original_object_sha256']==p['original_object_sha256']==root['object_sha256'] and
            h['contract_identity_sha256']==p['contract_identity_sha256'] and h['certificate_sha256']==p['certificate_sha256'] and
            type(h['fields']) is int and h['fields']==len(p['fields']) and type(h['undefined_records']) is int and h['undefined_records']==len(p['undefined']) and
            type(h['serialized_symbol_index']) is int and h['serialized_symbol_index']==p['maps']['symbol_map'][str(root['symbol_index'])] and
            type(h['serialized_section']) is int and h['serialized_section']>0 and h['serialized_section']==p['maps']['section_map'][str(root['section'])] and
            type(h['field_proof_ordinal']) is int and h['field_proof_ordinal']==ordinal and
            observer.selector.sha(h['field_proof_record_sha256']) and observer.selector.sha(h['original_fields_sha256']),
            'CODE68 handoff original physical/member/map/proof record differs')


def select_eligible(receipt,rows,request):
    """Account for every observed root; select every complete composition."""
    require(receipt.get('policy_id')==observer.POLICY and receipt.get('status')=='metadata-only' and
        receipt.get('input_stability') is True and receipt.get('optional_function_index_present') is False and
        type(receipt.get('emitted')) is int and receipt['emitted']==0 and all(receipt.get(k) is False for k in observer.FALSE),
        'accepted evidence-only original observer required')
    require(type(rows) is list and type(receipt.get('roots')) is int and
        len(rows)==receipt['roots']==len(request['roots'])==len(request['candidates'])>0,
        'whole finite observer request/outcome set required')
    wanted={c['root']['original_address']:c for c in request['candidates']}
    require(len(wanted)==len(rows) and exact(sorted(request['roots'],key=lambda r:r['original_address']),
        sorted((c['root'] for c in wanted.values()),key=lambda r:r['original_address'])),'unique exact observer request roots')
    eligible=[];ledger=[];seen=set();complete=0
    for ordinal,e in enumerate(rows,1):
        root=e['root'];identity=observer.selector.root_identity(root);a=root['original_address']
        require(a in wanted and a not in seen and exact(root,wanted[a]['root']) and
            exact(e['authority'],wanted[a]['authority']) and e['source_record_sha256']==wanted[a]['authority']['record_sha256'],
            'borrowed/duplicate observer original source/root')
        seen.add(a);negative=e['original_negative_certificate'];composed=e['composed']
        require(e.get('policy_id')==observer.POLICY and e.get('original_certificate_unchanged') is True and
            e.get('serialization_performed') is False and all(e.get(k) is False for k in observer.FALSE) and
            e.get('original_object_sha256')==root['object_sha256'] and
            negative.get('policy_id')==base.ordinary.POLICY and negative.get('closure_observed') is False and
            e['original_negative_certificate_sha256']==digest(negative)==wanted[a]['authority']['certificate_sha256']==wanted[a]['summary']['certificate_sha256'] and
            negative.get('contract_identity_sha256')==e['contract_identity_sha256'] and
            exact(negative['roots'],[{k:root[k] for k in base.NATIVE_KEYS}]),'original negative witness envelope differs')
        require(type(e['native_preflight'].get('eligible')) is bool and
            e['native_preflight'].get('policy_id')==core.composer.POLICY and
            e['native_preflight'].get('kind')=='comdat-any-native-definition-preflight' and
            e['native_preflight'].get('candidate_policy_evaluated') is False and
            e['native_preflight'].get('serialization_performed') is False and
            e['native_preflight'].get('original_certificate_unchanged') is True and
            all(e['native_preflight'].get(k) is False for k in core.composer.FALSE) and
            e['native_preflight']['original_negative_certificate_sha256']==digest(negative) and
            e['native_preflight']['contract_identity_sha256']==e['contract_identity_sha256'] and
            e['native_preflight']['object_sha256']==root['object_sha256'],'observer native preflight scope differs')
        selected=False
        if composed is not None:
            require(e['native_preflight']['eligible'] is True and type(composed.get('composed_omission_complete')) is bool and
                composed.get('policy_id')==core.composer.POLICY and composed.get('base_closure_observed') is False and
                exact(composed['base_certificate'],negative) and composed['base_certificate_sha256']==digest(negative) and
                composed['contract_identity_sha256']==e['contract_identity_sha256'] and composed['object_sha256']==root['object_sha256'] and
                all(composed.get(k) is False for k in core.composer.FALSE) and
                type(e['witnesses']) is list and len(e['witnesses'])==1 and
                exact(composed['witness_sha256'],[digest(w) for w in e['witnesses']]) and
                exact(e['unsupported_summary'],composed['unsupported_summary']),'typed COMDAT composition scope/promoted state')
            selected=composed['composed_omission_complete']
            wrapper=e['witnesses'][0];w=wrapper['observation'];census=wrapper['definition_census']
            expected_census=dict(schema_version=1,kind='planned-code-definition-census',complete=True,
                entries=[dict(root=root,planned_canonical_name=base.pool.canonical(identity))])
            require(set(wrapper)=={'kind','definition_census','observation'} and wrapper['kind']==core.composer.WITNESS_KIND and
                exact(census,expected_census) and exact(census,e['native_preflight']['definition_census']) and
                w.get('policy_id')==core.composer.policy.POLICY and w.get('kind')=='typed-comdat-any-code-policy-candidate-witness' and
                exact(w.get('requested_root'),root) and w.get('object_sha256')==root['object_sha256'] and
                w.get('source_sha256')==root['source_sha256'] and w.get('recipe_id')==root['recipe_id'] and
                w.get('original_negative_certificate_sha256')==digest(negative) and
                w.get('contract_identity_sha256')==e['contract_identity_sha256'] and
                w.get('definition_census_sha256')==digest(census) and
                composed['definition_census_sha256']==digest(census) and
                all(w.get(k) is False for k in core.composer.policy.FALSE) and
                w.get('base_closure_observed') is False and w.get('original_certificate_unchanged') is True and
                w.get('selection_rewritten') is False and type(w.get('witness_complete')) is bool and
                type(w.get('root_comdat2_policy_candidate')) is bool and
                w['witness_complete'] is w['root_comdat2_policy_candidate'] is selected,
                'borrowed/promoted/partial typed COMDAT witness scope differs')
            require(not selected or (not composed['remaining_blockers'] and len(composed['discharged_blockers'])==1),
                'complete composition still has independent blockers')
            if selected:
                discharge=composed['discharged_blockers'][0]
                require(len(negative['blockers'])==1 and negative['blockers'][0]['code']==observer.selector.ROOT_BLOCKER and
                    exact(w['discharge_blocker_ids'],[negative['blockers'][0]['blocker_id']]) and
                    w['remaining_base_blockers']==[] and w['policy_blockers']==[] and
                    set(discharge)=={'base_blocker_ordinal','blocker','witness_sha256','witness_policy_id'} and
                    type(discharge['base_blocker_ordinal']) is int and discharge['base_blocker_ordinal']==1 and
                    discharge['witness_sha256']==digest(wrapper) and discharge['witness_policy_id']==core.composer.policy.POLICY and
                    exact(discharge['blocker'],negative['blockers'][0]),
                    'complete typed witness did not discharge only original root conjunct')
            else:
                require(w['discharge_blocker_ids']==[] and composed['discharged_blockers']==[] and
                    exact(w['remaining_base_blockers'],negative['blockers']) and exact(composed['remaining_blockers'],negative['blockers']),
                    'blocked witness changed original negative occurrences')
        else:
            require(e['native_preflight']['eligible'] is False and e['witnesses']==[] and
                e['unsupported_summary']['discharged_occurrences']==0,'unsupported native form has a policy discharge')
        ids=[b['blocker_id'] for b in negative['blockers']];summary=e['unsupported_summary']
        expected_discharged=ids if selected else [];expected_remaining=[] if selected else ids
        require(exact(e['native_preflight']['original_blocker_ids'],ids) and
            exact(summary['original_blocker_ids'],ids) and exact(summary['discharged_blocker_ids'],expected_discharged) and
            exact(summary['remaining_blocker_ids'],expected_remaining) and summary.get('serialization_approved') is False and
            all(type(summary.get(k)) is int and summary[k]==n for k,n in
                [('original_occurrences',len(ids)),('discharged_occurrences',len(expected_discharged)),('remaining_occurrences',len(expected_remaining))]),
            'ordered original/discharged/remaining blocker occurrence partition differs')
        if composed is not None:
            require(type(composed['base_blocker_occurrences']) is int and composed['base_blocker_occurrences']==len(ids) and
                exact(composed['remaining_blocker_occurrences'],[] if selected else
                    [dict(base_blocker_ordinal=i,blocker=b) for i,b in enumerate(negative['blockers'],1)]),
                'composed blocker occurrence ordinal partition differs')
        complete+=selected
        item=dict(root=root,observer_ordinal=ordinal,observer_record_sha256=digest(e),
            original_record_sha256=e['source_record_sha256'],authority=e['authority'],
            original_negative_certificate_sha256=digest(negative),contract_identity_sha256=e['contract_identity_sha256'],
            witnesses_sha256=digest(e['witnesses']),composed_sha256=digest(composed) if composed is not None else None)
        ledger.append(dict(root=root,observer_ordinal=ordinal,selected=selected,unsupported_summary=e['unsupported_summary']))
        if selected:eligible.append(item)
    require(exact(sorted(seen),receipt['observed_addresses']) and type(receipt.get('composed_complete')) is int and
        receipt['composed_complete']==complete and type(receipt.get('unsupported')) is int and receipt['unsupported']==len(rows)-complete and
        type(receipt.get('blocked')) is int and receipt['blocked']==len(rows)-complete,'complete observer composition/unsupported census differs')
    eligible.sort(key=lambda r:r['root']['original_address'])
    return eligible,ledger


def rebuild_latest_exclusions(parent,code68_members,providers_expanded,units,source_member_sha):
    """Thin original-identity append; historical records are preserved verbatim."""
    require(parent.get('kind')=='prepared-CODE-collision-exclusions' and parent.get('policy_id')==observer.selector.FRONTIER_POLICY and
        type(parent.get('ordinary_prepared_count')) is int and parent['ordinary_prepared_count']==14403 and
        type(parent.get('collision_exclusion_count')) is int and parent['collision_exclusion_count']==14409 and
        len(parent['records'])==len(parent['exclusion_names'])==len(set(parent['exclusion_names']))==14409 and
        len(parent['ordinary_names'])==len(set(parent['ordinary_names']))==14403 and
        parent.get('application_selection_inferred_from_counts') is False and
        all(parent.get(k) is False for k in ('provider_selected','runtime_eligible','application_manifest_adopted')),
        'exact accepted upstream V8 collision epoch required')
    require(type(code68_members) is list and len(code68_members)==68 and observer.selector.sha(source_member_sha),
        'entire accepted 68-member source cohort required')
    records=list(parent['records']);names=set(parent['exclusion_names']);ordinary=set(parent['ordinary_names'])
    require({r['canonical'] for r in records}==names and ordinary<=names and
        all(base.pool.canonical(r['namespace_identity'])==r['canonical'] for r in records) and
        dict(Counter(r['category'] for r in records))=={'ordinary':14403,'application-candidate':6} and
        {r['canonical'] for r in records if r['category']=='ordinary'}==ordinary,'parent namespace census differs')
    members=set();addresses=set()
    for ordinal,member in enumerate(code68_members,1):
        p=member['projection'];require(type(member['name']) is str and member['name'] and member['name'] not in members and
            type(p['requested_roots']) is list and len(p['requested_roots'])==1,'unique singleton accepted CODE member')
        members.add(member['name']);root=p['requested_roots'][0];identity=observer.selector.root_identity(root);a=root['original_address']
        require(a not in addresses and a in providers_expanded and exact(root,frontier.root_record(a,providers_expanded[a],units)),
            'accepted CODE root differs from original planned/native/source identity');addresses.add(a)
        name=base.pool.canonical(identity)
        require(providers_expanded[a]['planned_canonical_name']==name and
            p.get('policy_id') in (base.POLICY,ordinary_factory.core.POLICY) and
            exact(p['exports'],[name]) and name not in names and p['original_object_sha256']==root['object_sha256'] and
            observer.selector.sha(p['output_sha256']),
            'accepted CODE member export/collision/original comparison identity differs')
        comparison_rows(p['before_comparison'],root,root['symbol']);comparison_rows(p['after_comparison'],root,name)
        sm=p['maps']['symbol_map']
        require(type(sm) is dict and all(type(k) is str and re.fullmatch('0|[1-9][0-9]*',k) and
            type(v) is int and v>=0 for k,v in sm.items()) and len(set(sm.values()))==len(sm),'typed bijective CODE symbol map required')
        sections=p['maps']['section_map']
        require(type(sections) is dict and all(type(k) is str and re.fullmatch('[1-9][0-9]*',k) and
            type(v) is int and v>0 for k,v in sections.items()) and len(set(sections.values()))==len(sections) and
            str(root['section']) in sections,'typed bijective CODE root section map required')
        index=sm.get(str(root['symbol_index']))
        require(type(index) is int and index>=0,'accepted CODE root physical output mapping required')
        names.add(name);ordinary.add(name)
        records.append(dict(canonical=name,original_address=a,cohort='V8-new-frontier-68',category='ordinary',
            identity_mode='original-selected-physical',namespace_identity=identity,origin_identity=identity,member=member['name'],
            member_sha256=p['output_sha256'],serialized_symbol_index=index,source_ledger_sha256=source_member_sha,
            source_record_ordinal=ordinal,source_record_sha256=digest(member),logical_binding_applied=True))
    require(len(records)==len(names)==14477 and len(ordinary)==14471,'complete latest disjoint collision epoch differs')
    return dict(schema_version=5,kind='prepared-CODE-collision-exclusions',policy_id=POLICY,
        parent_manifest_sha256=observer.METADATA_PINS['prepared_epoch'],ordinary_prepared_count=14471,
        broader_application_candidate_count=6,collision_exclusion_count=14477,ordinary_names=sorted(ordinary),
        exclusion_names=sorted(names),records=sorted(records,key=lambda r:r['canonical']),
        application_selected_code_count=None,application_selection_inferred_from_counts=False,emission_performed=False,**FALSE)


def comparison_rows(rows,root,name):
    require(type(rows) is list and len(rows)==1,'exact singleton plain comparison receipt required')
    row=rows[0]
    require(row.get('address')==root['original_address'] and row.get('symbol')==name and
        type(row.get('size')) is int and row['size']==root['size'] and row.get('verdict')=='match' and
        type(row.get('compiled_extent')) is int and row['compiled_extent']==root['size'] and row.get('errors')==[] and
        type(row.get('relocations')) is list and all(r.get('match') is True for r in row['relocations']) and
        not row.get('byte_differences',[]),'plain MATCH body/field receipt differs')


def verify_member(raw,row,candidate,evidence,providers,exports,original_path,stage_path,pe,recipe):
    """Fresh negative/witness/core replay and unchanged ordinary comparisons."""
    contract,negative=observer.validate_selected_row(row,candidate);root=candidate['root']
    fresh=observer.observe_member(raw,row,candidate)
    require(exact(fresh,evidence),'saved witness observation does not replay original raw/source')
    assessment=core.assess_member(raw,contract,negative,evidence['witnesses'],evidence['composed'],[root],providers,
        existing_exports=exports,policy_id=core.POLICY)
    if assessment['eligible'] is not True:
        require(assessment['blockers'],'unsupported typed consumer has no explicit blocker')
        return None,None,assessment
    contracts=[dict(selected={k:root[k] for k in base.NATIVE_KEYS})]
    before=base.bulk.compare_functions(original_path,pe,contracts,recipe)
    comparison_rows(before,root,root['symbol'])
    output,projection=core.project_member(raw,contract,negative,evidence['witnesses'],evidence['composed'],[root],providers,
        existing_exports=exports,policy_id=core.POLICY)
    require(exact(projection['fields'],assessment['fields']) and projection['exports']==[assessment['export']] and
        projection['original_negative_certificate_preserved'] is True and projection['selection2_auxiliary_preserved'] is True and
        projection['selection_rewritten'] is False,'fresh typed assessment/physical projection changed')
    base.pool.fsynced(Path(stage_path),output);base.bulk.strict_reparse(Path(stage_path),output)
    after=base.bulk.compare_functions(stage_path,pe,contracts,recipe,
        dict(bindings=projection['namespace_bindings'],comparison_base_view=projection['comparison_base_view']))
    comparison_rows(after,root,projection['exports'][0])
    projection.update(before_comparison=before,after_comparison=after,authority=candidate['authority'],
        central_record_sha256=digest(row),observer_record_sha256=digest(evidence))
    return output,projection,assessment


def field_proof_record(member,row,candidate,evidence,projection,output):
    """Versioned complete field metadata; the base remains an original negative."""
    root=candidate['root'];contract,negative=observer.validate_selected_row(row,candidate)
    require(exact(projection['requested_roots'],[root]) and projection['output_sha256']==base.coff.digest(output) and
        projection['original_object_sha256']==root['object_sha256'] and
        projection['original_negative_certificate_sha256']==digest(negative) and
        projection['composed_certificate_sha256']==digest(evidence['composed']) and
        projection['contract_identity_sha256']==digest(contract) and
        projection['central_record_sha256']==digest(row) and projection['observer_record_sha256']==digest(evidence) and
        exact(projection['authority'],candidate['authority']),'COMDAT full field proof/source binding differs')
    fields=contract['fields'];hashes=[digest(f) for f in fields]
    require(len(set(hashes))==len(hashes) and exact(hashes,[f['field_proof_sha256'] for f in projection['fields']]),
        'full original field rows differ from projected relocation identities')
    return dict(schema_version=1,kind='comdat-any-original-negative-full-field-proof',policy_id=POLICY,member=member,
        requested_root=root,authority=candidate['authority'],source_record_sha256=digest(row),
        original_negative_certificate_sha256=digest(negative),composed_certificate_sha256=digest(evidence['composed']),
        observer_record_sha256=digest(evidence),contract_identity_sha256=digest(contract),
        output_object_sha256=base.coff.digest(output),fields_sha256=digest(fields),fields=fields,
        source_evidence_enriched=False,original_base_closure_observed=False)


def write_coverage(path,providers,exports,eligible,emitted,observer_request):
    """Complete in-memory owner accounting; no historical/global stream read."""
    require(type(providers) is dict and len(providers)==68657,'complete selected identity map required')
    selected={e['root']['original_address'] for e in eligible};emitted=set(emitted)
    observed={c['root']['original_address'] for c in observer_request['candidates']}
    require(emitted<=selected<=observed and selected<=set(providers),'finite projected owner coverage scope')
    counts=Counter()
    with Path(path).open('xb') as target:
        with gzip.GzipFile(fileobj=target,mode='wb',mtime=0) as writer:
            for a,identity in sorted(providers.items()):
                name=base.pool.canonical(identity);prepared=name in exports
                require(a not in selected or not prepared,'new typed root would replace prepared owner')
                status='PROJECTED' if a in emitted else 'QUARANTINED' if a in selected else 'NOT_REQUESTED'
                counts[status]+=1
                writer.write(observer.selector.canonical(dict(schema_version=1,kind='complete-original-physical-owner-coverage',
                    original_address=a,physical_identity=identity,planned_canonical_name=name,prepared_before=prepared,
                    observer_requested=a in observed,projection_status=status,historical_status_inferred=False,
                    emission_performed=a in emitted,**FALSE))+b'\n')
        target.flush();os.fsync(target.fileno())
    require(sum(counts.values())==68657 and counts['PROJECTED']==len(emitted),'complete projection owner accounting differs')
    return dict(counts)


def validate_operation(operation):
    require(type(operation) is dict and set(operation)=={'schema_version','kind','epoch','roots','output_relative',
        'resource_limits','artifacts','acceptances','source_contexts','provider_map_sha256','reference_sha256'} and
        type(operation['schema_version']) is int and operation['schema_version']==1 and
        operation['kind']=='finite-comdat-any-frontier-projection-operation' and
        type(operation['epoch']) is str and 0<len(operation['epoch'])<=100 and operation['epoch'].isascii() and
        exact(operation['resource_limits'],LIMITS) and set(operation['artifacts'])==ARTIFACTS and
        set(operation['acceptances'])==set(ACCEPTANCES) and operation['provider_map_sha256']==ordinary_factory.MAP_PIN and
        operation['reference_sha256']==base.pool.PINS['reference'],'exact finite COMDAT projection operation required')
    require(type(operation['roots']) is list and operation['roots'] and type(operation['source_contexts']) is list and
        type(operation['output_relative']) is str,'finite complete original root/output scope')
    for root in operation['roots']:observer.selector.root_identity(root)
    for name,ref in operation['artifacts'].items():
        observer._ref(ref,private=name not in ('recipes','image_check'))
        if name in SOURCE_ARTIFACT_PINS:require(ref['sha256']==SOURCE_ARTIFACT_PINS[name],'accepted source artifact pin differs: '+name)
    for name,ref in operation['acceptances'].items():
        observer._ref(ref);require(ref['sha256']==ACCEPTANCES[name],'accepted source/witness review pin differs')


def selected_sources(operation,observer_context,eligible,request):
    """Filter exact prior source authorities to the entire eligible subset."""
    all_candidates={c['root']['original_address']:c for c in request['candidates']}
    wanted={}
    for item in eligible:
        c=all_candidates[item['root']['original_address']];auth=c['authority']
        key=tuple(auth[k] for k in ('kind','receipt_sha256','request_sha256'))
        wanted.setdefault(key,[]).append(c)
    originals={tuple(s[k]['sha256'] if k!='kind' else s[k] for k in ('kind','receipt','request')):s for s in observer_context['sources']}
    require(len(originals)==len(observer_context['sources']) and len(operation['source_contexts'])==len(wanted),'complete eligible original authority subset')
    result=[];seen=set()
    for source in operation['source_contexts']:
        require(type(source) is dict and set(source)=={'kind','receipt','request','details'},'unknown eligible original source descriptor')
        key=(source['kind'],source['receipt']['sha256'],source['request']['sha256'])
        require(key in wanted and key in originals and key not in seen,'borrowed/duplicate eligible original authority');seen.add(key)
        original=originals[key];require(exact(source['receipt'],original['receipt']) and exact(source['request'],original['request']),
            'eligible authority path/epoch differs from actual observer input')
        lanes={c['authority'].get('lane') for c in wanted[key]}
        expected=[d for d in original['details'] if d['lane'] in lanes]
        require(exact(source['details'],expected) and len(expected)==len(lanes),'only exact eligible original detail lanes allowed')
        result.append((source,wanted[key]))
    return result


def read_evidence(path,receipt,check):
    rows=[];total=0
    with gzip.open(path,'rb') as stream:
        while True:
            line=stream.readline(observer.MAX_ROW+1)
            if not line:break
            total+=len(line)
            require(len(rows)<receipt['roots'] and len(line)<=observer.MAX_ROW and line.endswith(b'\n') and total<=128*1024**2,
                'whole observer evidence record/decompression bound')
            rows.append(json.loads(line));check()
    require(len(rows)==receipt['roots'],'whole observer evidence extent differs')
    return rows


def review_gate(args,inputs):
    review=observer._load(dict(path=str(args.review),sha256=args.review_sha256),inputs)
    require(type(review) is dict and set(review)=={'schema_version','kind','reviewer','approved','root_authorized',
        'independent_source_schema_review_pass','artifact_input_review_pass','operation_sha256','source_sha256','producer_sha256',
        'allow_original_objects_read','allow_source_hashing','allow_reference_image_read','allow_code_emission',
        'allow_native_tools','allow_executable_link','allow_game_execution'} and
        type(review['schema_version']) is int and review['schema_version']==1 and
        review['kind']=='comdat-any-frontier-projection-review-v1' and type(review['reviewer']) is str and review['reviewer'] and
        all(review[k] is True for k in ('approved','root_authorized','independent_source_schema_review_pass','artifact_input_review_pass',
            'allow_original_objects_read','allow_source_hashing','allow_reference_image_read','allow_code_emission')) and
        all(review[k] is False for k in ('allow_native_tools','allow_executable_link','allow_game_execution')) and
        review['operation_sha256']==args.operation_sha256 and set(review['source_sha256'])==set(OWNED) and
        exact(review['producer_sha256'],PINS),'exact delegated COMDAT projection source/input review required')
    for name,h in {**review['source_sha256'],**PINS}.items():
        require(observer.selector.sha(h),'reviewed source digest required');base.observe(ROOT/name,h,inputs)
    for module in (observer,core,core.composer,core.field_common,ordinary_factory,field_audit,frontier,
        base,base.coff,base.pool,base.bulk,base.inventory,base.collector):
        require(Path(module.__file__).resolve()==ROOT/'tools/rebuild'/Path(module.__file__).name,'swapped factory producer module')
    return review


def input_budget(start):
    require(time.monotonic()-start<=900,'15-minute sampled input budget')
    peak=base.peak_memory_bytes();require(peak is not None and peak<=1024**3,'1-GiB sampled input memory budget')


def validate_original_basis(reports,planned,recipes):
    """Original epoch admission through frozen complete-map/native validators."""
    units={u['recipe_id']:u for u in reports['manifest']['units']};proofs={p['recipe_id']:p for p in reports['retained']['units']}
    require(len(units)==len(reports['manifest']['units'])==len(proofs)==len(reports['retained']['units'])==2988 and
        len(reports['selection']['selections'])==68657,'complete unique original selected native epoch required')
    require(base.reconcile_recipes(reports['manifest'],recipes)['verified'],'original source/compiler recipe variants differ')
    providers=ordinary_factory.validate_provider_map(planned,reports['selection']['selections'],units,proofs,reports['owners'])
    require(len(providers)==68657,'complete planned identity map required')
    return units,proofs,providers


def run(args):
    start=time.monotonic();inputs={};review=review_gate(args,inputs)
    operation=observer._load(dict(path=str(args.operation),sha256=args.operation_sha256),inputs)
    validate_operation(operation);refs=operation['artifacts'];artifacts={}
    for name,ref in refs.items():
        if name=='observer_details':continue
        artifacts[name]=observer._load(ref,inputs,private=name not in ('recipes','image_check'));input_budget(start)
    for ref in operation['acceptances'].values():base.observe(observer._ref(ref),ref['sha256'],inputs)
    receipt=artifacts['observer_receipt'];request=artifacts['observer_request'];context=artifacts['observer_context']
    require(receipt['request_sha256']==refs['observer_request']['sha256']==context['request_sha256'] and
        receipt['context_sha256']==refs['observer_context']['sha256'] and
        receipt['review_sha256']==refs['observer_input_review']['sha256'] and
        receipt['details_sha256']==refs['observer_details']['sha256'] and
        all(context['artifacts'][k]['sha256']==refs[k]['sha256'] for k in ('manifest','retained','selection','recipes')),
        'actual observer source/request/context/native epoch differs')
    observer.review_gate(argparse.Namespace(review=observer._ref(refs['observer_input_review']),
        review_sha256=refs['observer_input_review']['sha256'],request_sha256=refs['observer_request']['sha256'],
        context_sha256=refs['observer_context']['sha256']),inputs)
    detail_path=base.observe(observer._ref(refs['observer_details']),refs['observer_details']['sha256'],inputs)
    require(detail_path.stat().st_size==receipt['details_bytes']<=128*1024**2,'actual observer evidence extent differs')
    rows=read_evidence(detail_path,receipt,lambda:input_budget(start));eligible,ledger=select_eligible(receipt,rows,request)
    require(eligible and exact(operation['roots'],[e['root'] for e in eligible]),'operation must include every complete original COMDAT composition')
    evidence={e['root']['original_address']:e for e in rows if e['root']['original_address'] in {x['root']['original_address'] for x in eligible}}
    reports={k:artifacts[k] for k in ('manifest','retained','selection','owners')}
    recipes=observer._ref(refs['recipes'],private=False)
    planned=base.load_json(base.observe(args.provider_map,ordinary_factory.MAP_PIN,inputs))
    units,proofs,providers=validate_original_basis(reports,planned,recipes)
    validate_code68(artifacts['code68_members'],artifacts['code68_receipt'],artifacts['code68_handoff'],refs)
    archive_ref=artifacts['code68_handoff']['archive']
    base.observe(observer._ref(archive_ref),artifacts['code68_receipt']['archive_sha256'],inputs)
    latest=rebuild_latest_exclusions(artifacts['upstream_epoch'],artifacts['code68_members'],planned['providers'],units,refs['code68_members']['sha256'])
    require(exact(latest,artifacts['latest_prepared_epoch']) and
        observer.selector.document_hash(latest)==refs['latest_prepared_epoch']['sha256'],'latest collision epoch reconstruction differs')
    exports=set(latest['exclusion_names']);wanted={r['original_address']:r for r in operation['roots']}
    base.collector.validate_request(dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=operation['roots']),
        reports['selection']['selections'],reports['manifest'],reports['retained'],providers)
    for root in operation['roots']:require(base.pool.canonical(providers[root['original_address']]) not in exports,'selected COMDAT root already prepared')
    source_specs=[]
    for source,candidates in selected_sources(operation,context,eligible,request):
        source_receipt=observer._load(source['receipt'],inputs);source_request=observer._load(source['request'],inputs)
        for ref,count,selections in observer.validate_source(source,source_receipt,source_request,candidates):
            path=observer._ref({k:ref[k] for k in ('path','sha256')})
            require(path.stat().st_size<=128*1024**2,'bounded eligible original detail file')
            base.observe(path,ref['sha256'],inputs);source_specs.append((path,count,selections))
    manifest=reports['manifest'];native_root=observer._ref(refs['manifest']).parent/manifest.get('object_root_relative','.')
    object_paths={}
    for a,root in wanted.items():
        unit=units[root['recipe_id']];source=(ROOT/unit['source']).resolve();obj=(native_root/unit['object']).resolve()
        require(source.is_relative_to(ROOT) and obj.is_relative_to(ROOT/'build/rebuild') and obj.stat().st_size<=16*1024**2,
            'bounded original source/native input paths required')
        base.observe(source,root['source_sha256'],inputs);base.observe(obj,root['object_sha256'],inputs);object_paths[a]=obj
    for rel,h in reports['retained']['inputs']['tools_sha256'].items():
        path=(ROOT/rel).resolve();require(path.is_relative_to(ROOT/'tools'),'foreign retained proof dependency');base.observe(path,h,inputs)
    require(refs['image_check']['sha256']==reports['retained']['inputs']['image_check_sha256'],'original image probe metadata differs')
    reference=base.observe(args.reference,base.pool.PINS['reference'],inputs)
    out=Path(args.out).resolve();private=(ROOT/'build/rebuild').resolve()
    require(out==(ROOT/operation['output_relative']).resolve() and out.is_relative_to(private) and out!=private and
        not out.exists() and not any(p.is_relative_to(out) for p in inputs),'new exact exclusive private projection output required')
    for unit in manifest['units']:
        require(not (native_root/unit['object']).resolve().is_relative_to(out) and
            not (ROOT/unit['source']).resolve().is_relative_to(out),'projection output overlaps original inputs')
    # Keep only selected recipes/proofs before loading the immutable PE. The
    # complete provider and prepared censuses have already been authenticated.
    selected_recipes={r['recipe_id'] for r in operation['roots']}
    units={rid:units[rid] for rid in selected_recipes};proofs={rid:proofs[rid] for rid in selected_recipes}
    observer_roots=receipt['roots']
    del artifacts,reports,planned,latest,manifest,rows,context,receipt,source_receipt,source_request,unit
    base.stable(inputs);out.mkdir(parents=True,exist_ok=False);base.budget(start,out)
    journal=(out/'journal.jsonl').open('x',encoding='utf-8');members=[];member_receipts=[];blocked=[];assessments=[];emitted=[]
    metadata=None;proof_file=None;proof_writer=None
    def note(state,**value):
        journal.write(json.dumps(dict(state=state,elapsed_seconds=round(time.monotonic()-start,3),**value))+'\n')
        journal.flush();os.fsync(journal.fileno())
    def protect(path):
        h=base.file_hash(path);base.observe(path,h,inputs);return h
    try:
        note('started',whole_observer_roots=observer_roots,whole_composed_complete=len(eligible),latest_collision_count=len(exports))
        for name in (*OWNED,*PINS):
            source=ROOT/name;target=out/'source-snapshots'/name;target.parent.mkdir(parents=True,exist_ok=True)
            base.pool.fsynced(target,source.read_bytes());base.observe(target,inputs[source.resolve()],inputs);base.budget(start,out)
        sys.path.insert(0,str(ROOT/'tools'));import compare as oracle
        from build_and_match import image_ok
        pe=base.checked_reference(reference,oracle,image_ok);metadata=field_audit.SnapshotPe(reference,pe)
        highlow={metadata.base+rva for rva in metadata.relocations()};require(len(highlow)==351931,'fresh unchanged original HIGHLOW census differs')
        proof_file=(out/'field-proofs.jsonl.gz').open('xb');proof_writer=gzip.GzipFile(fileobj=proof_file,mode='wb',mtime=0)
        observed=set();facts={};field_count=0
        for path,count,selections in source_specs:
            for candidate,row in observer.read_selected_rows(path,count,selections,lambda:base.budget(start,out)):
                root=candidate['root'];a=root['original_address'];require(a not in observed and a in wanted,'duplicate/unrequested original context')
                observed.add(a);contract,negative=observer.validate_selected_row(row,candidate);proof=proofs[root['recipe_id']]
                require(exact(contract['unit_verified_functions'],proof['verified_functions']) and
                    contract['provenance'].get('recipe_unit_sha256')==proof['recipe_unit_sha256'],'fresh original contract/retained proof differs')
                for rel,h in contract['provenance']['dependency_tools_sha256'].items():
                    dep=(ROOT/rel).resolve();require(dep.is_relative_to(ROOT/'tools'),'foreign original observation dependency');base.observe(dep,h,inputs)
                for site,fact in field_audit.audit_original_fields(metadata,highlow,contract['fields']).items():
                    require(site not in facts or facts[site]==fact,'contradictory fresh original field facts');facts[site]=fact
                field_count+=len(contract['fields']);raw=object_paths[a].read_bytes()
                name='COMDAT-ANY-%03d-%s.obj'%(len(members),a[2:]);stage=out/name
                output,projection,assessment=verify_member(raw,row,candidate,evidence[a],providers,exports,object_paths[a],stage,pe,units[root['recipe_id']]['recipe'])
                assessments.append(dict(root=root,assessment=assessment))
                if output is None:
                    blocked.append(dict(root=root,blockers=assessment['blockers'],fresh_body_compared=False));continue
                protect(stage);proof_record=field_proof_record(name,row,candidate,evidence[a],projection,output)
                proof_writer.write(observer.selector.canonical(proof_record)+b'\n')
                members.append((name,output));member_receipts.append(dict(name=name,projection=projection,code_file_written=True));emitted.append(a)
                note('member_verified',original_address=a,fields=len(projection['fields']),object_sha256=projection['output_sha256'])
                base.budget(start,out)
        require(observed==set(wanted),'every composed-complete original context must reach a terminal outcome')
        proof_writer.close();proof_writer=None;proof_file.flush();os.fsync(proof_file.fileno());proof_file.close();proof_file=None
        metadata.close();metadata=None
        archive_sha=None
        if members:
            archive=base.coff.archive(members);archive_path=out/'COMDAT-ANY-code.lib';base.pool.fsynced(archive_path,archive)
            recovered=base.coff.read_archive(archive)
            require(recovered['members']==members and len(recovered['index'])==len(members),'typed archive member/export identity differs')
            for name,data in recovered['members']:
                path=out/('recovered-'+name);base.pool.fsynced(path,data);base.bulk.strict_reparse(path,data);protect(path)
            archive_sha=protect(archive_path)
        coverage_counts=write_coverage(out/'coverage.jsonl.gz',providers,exports,eligible,emitted,request)
        for name,value in [('members',member_receipts),('blocked',blocked),('assessments',assessments),('observer-ledger',ledger)]:
            base.save_json(out/(name+'.json'),value)
        base.save_json(out/'original-field-audit.json',dict(highlow_sites=len(highlow),retained_fields=field_count,
            unique_field_sites=len(facts),field_facts_sha256=digest(sorted(facts.items())),loaded_reference_sha256=base.coff.digest(pe.data),
            original_highlow_authority_authenticated=True))
        output_names=('members.json','blocked.json','assessments.json','observer-ledger.json','coverage.jsonl.gz','original-field-audit.json','field-proofs.jsonl.gz')
        output_hashes={name:protect(out/name) for name in output_names};base.stable(inputs);usage=base.budget(start,out)
        result=dict(schema_version=1,policy_id=POLICY,status='completed' if len(emitted)==len(eligible) else 'completed-incomplete',
            epoch=operation['epoch'],operation_sha256=args.operation_sha256,review_sha256=args.review_sha256,
            observer_receipt_sha256=refs['observer_receipt']['sha256'],whole_observer_roots=observer_roots,requested=len(eligible),
            emitted=len(emitted),blocked=len(blocked),emitted_addresses=emitted,archive_sha256=archive_sha,
            original_negative_certificates_preserved=True,selection2_auxiliaries_preserved=True,selection_rewritten=False,
            upstream_ordinary_prepared_count=14471,upstream_collision_exclusion_count=14477,
            full_field_proof_schema_version=1,full_field_proof_records=len(member_receipts),fields=sum(len(m['projection']['fields']) for m in member_receipts),
            code_bytes=sum(m['projection']['requested_roots'][0]['size'] for m in member_receipts),coverage_counts=coverage_counts,
            output_sha256=output_hashes,inputs={str(p):h for p,h in inputs.items()},input_stability=True,optional_function_index_present=False,
            emission_performed=bool(emitted),code_emission_performed=bool(emitted),original_reference_read=True,
            source_evidence_enriched=False,owner_stream_traversals=0,binding_stream_traversals=0,
            resource_observations=usage,resource_limits=LIMITS,**FALSE)
        return base.finalize_success(out,result,inputs,start,journal,note)
    except BaseException as error:
        try:
            if not journal.closed:note('failed',error_type=type(error).__name__,completed_members=len(emitted))
        except BaseException:pass
        try:base.save_json(out/'abort.json',dict(status='aborted-no-retry',error_type=type(error).__name__,
            completed_members=emitted,successful_projection=False,emission_performed=bool(emitted),**FALSE))
        except BaseException:pass
        raise
    finally:
        if proof_writer is not None:proof_writer.close()
        if proof_file is not None:proof_file.close()
        if metadata is not None:metadata.close()
        if not journal.closed:journal.close()


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('operation','review','provider-map','reference','out'):
        parser.add_argument('--'+name,required=True,type=Path,dest=name.replace('-','_'))
    for name in ('operation','review'):parser.add_argument('--'+name+'-sha256',required=True)
    args=parser.parse_args(argv)
    try:result=run(args)
    except (ValueError,OSError,KeyError,TypeError) as error:parser.exit(2,'COMDAT projection rejected: '+str(error)+'\n')
    print(json.dumps(dict(requested=result['requested'],emitted=result['emitted'],blocked=result['blocked'])))
    return 0 if result['status']=='completed' else 3


if __name__=='__main__':raise SystemExit(main())
