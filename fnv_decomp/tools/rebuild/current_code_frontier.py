"""Versioned metadata-only prepared epoch and immediate CODE frontier join."""
from __future__ import annotations
from collections import Counter
import argparse
import json
import os
from pathlib import Path
import time
import prepared_code_exclusions as old
import composed_relocation_factory as typed

base=typed.base
ROOT=base.ROOT
POLICY='current-immediate-CODE-frontier-v1'
OWNED=('tools/rebuild/current_code_frontier.py','tests/rebuild/test_current_code_frontier.py','docs/rebuild/CURRENT-CODE-FRONTIER.md')
FALSE=dict(old.FALSE,original_objects_read=False,original_image_read=False,source_bodies_read=False)
PINS={**typed.PINS,'tools/rebuild/composed_relocation_factory.py':'34e9ad9ccfb10943c2fc4c10ea57e28dae8312dc442621ed8045cbeb2b649477'}
INPUTS={**typed.ARTIFACTS,
 'typed_members':('composed-relocation-first12-v1/members.json','db65da111e1f13401dc82c2d41302881434f93fc5221588abc6e1f7c292766de'),
 'typed_receipt':('composed-relocation-first12-v1/receipt.json','6867c59b44b2ae5a4957ed7f58ac39a2abbd56123dc81e91e096535a18d94bcc'),
 'typed_review':('code-lane-02/typed-factory-outcome-review-v1.json','adf5d0d795fd3307698da031ae6e3f8938252b21ef236e1a8af582dbcd67c3f5'),
 'typed_handoff':('composed-relocation-first12-export-handoff-v1.json','a55e58f8132dab38ee17e4f59172b735c2dc93b7ba7853a4e9481311dfe4b474'),
 'typed_archive':('composed-relocation-first12-v1/typed-composed.lib','06857caa370cc3d618dd11204bc2d43fba3a09eba4e7bc7d1f42202db192fa9c'),
 'eh_metadata':('parent-eh-file-projection-v1/integration-metadata.json','b009af1c5402f37d992d0f4fa48b7667780de9fb36ee04de0618007bb3c92931'),
 'eh_receipt':('parent-eh-file-projection-v1/projection.json','27f183555a60b158a673588a4d8bc313075fe3247a2d0220225d0b378a04fff5'),
 'eh_review':('code-lane08-source-triage-v1/parent-EH-file-artifact-review-v1.json','6a22fb4730dfbad89b0cc33ae38a5709cac925eab501c55c1b1a1550028ea4c8'),
 'eh_object':('parent-eh-file-projection-v1/component.obj','db86fc462255ec7bf109486538cf16f8b94ae5bcc6135a0f8d3b4778d5e3582b'),
 'groups':('application-link-diagnostic-v5/unresolved-groups.json','a75d5295a3a01a24828928d0e412de830b5169559b0e4923b915d28446bfb510'),
 'link_receipt':('application-link-diagnostic-v5/link-receipt.json','28a6b3aa2ba0cade82d6fcdab089f15ff1dbe5f3b91af72846a5886a0be5c380'),
 'link_review':('application-link-diagnostic-v5/independent-outcome-review.json','911ff85b6c4a2450f983cfcda1bce8505abaf3191707db7e06b7b2c4fc578292'),
 'central':('central-code-root-observation-v1/receipt.json','290ac0e8c1ffbfd89df7dd6cdbbdb8df363edca58111b7aa19fe842aa26cc8e4'),
 'aggregate':('application-frontier-dispatch-v1/central-root-requests.json','61ec8851e2bd2e2208b265fba6554eabcfa81291c1e2e6738faefbafec9fe1ce')}
require=base.require
digest=base.digest


def root_record(address,entry,units):
    unit=units[entry['recipe_id']]
    require(unit['object_sha256']==entry['object_sha256'] and unit['source_sha256']==entry['source_sha256'],'planned recipe source differs')
    return dict(original_address=address,recipe_index=unit['recipe_index'],**{k:entry[k] for k in
        ('recipe_id','object_sha256','source_sha256','symbol','symbol_index','section','value','size')})


def successor_epoch(parent,providers,members,eh_metadata,eh_receipt,*,typed_members_sha256,eh_metadata_sha256):
    """Preserve old cohort records; append explicit accepted artifact identities."""
    names=typed.validate_prepared(parent,providers);reverse=old.reverse_planned(providers)
    records=list(parent['records']);added=[]
    require(len(members)==12,'exact accepted typed cohort required')
    for ordinal,member in enumerate(members,1):
        projection=member['projection'];roots=projection['requested_roots'];require(len(roots)==1,'typed singleton lineage')
        root=roots[0];identity={k:root[k] for k in ('recipe_id','object_sha256','symbol_index')};name=base.pool.canonical(identity)
        require(projection['exports']==[name] and name in reverse and reverse[name]==(root['original_address'],identity) and name not in names and
            projection['original_object_sha256']==root['object_sha256'],'typed export source identity/collision differs')
        names.add(name);record=dict(canonical=name,original_address=root['original_address'],cohort='typed-composed-first12',category='ordinary',
            identity_mode='original-selected-physical',namespace_identity=identity,origin_identity=identity,member=member['name'],
            member_sha256=projection['output_sha256'],serialized_symbol_index=projection['maps']['symbol_map'][str(root['symbol_index'])],
            source_ledger_sha256=typed_members_sha256,source_record_ordinal=ordinal,source_record_sha256=digest(member),logical_binding_applied=True)
        records.append(record);added.append(name)
    require(eh_metadata['parent']==eh_receipt['parent']=='0x005e0200' and len(eh_metadata['physical_exports'])==1,'accepted EH parent scope differs')
    name=eh_metadata['physical_exports'][0];require(name in reverse and name not in names,'EH namespace missing original owner or already prepared')
    address,identity=reverse[name]
    require(address==eh_metadata['parent'] and eh_metadata['source_object_sha256']==identity['object_sha256'] and
        eh_receipt['projection']['export']==name and eh_receipt['projection']['output_sha256']==eh_metadata['object_sha256'] and
        eh_metadata['receipt_sha256']==INPUTS['eh_receipt'][1] and eh_receipt['projection']['input_sha256']==identity['object_sha256'] and
        eh_metadata['physical_maps']==eh_receipt['projection']['maps'] and eh_metadata['all_parent_EH_fields_preserved'] is True and
        eh_receipt['source_member_layout_verified'] is False and eh_receipt['input_stability'] is True and
        all(eh_metadata[k] is False and eh_receipt[k] is False for k in ('provider_selected','runtime_eligible','ABI_verified','link_ready','namespace_approved')),
        'EH physical/source export or reviewed receipt crosslink differs')
    names.add(name)
    records.append(dict(canonical=name,original_address=address,cohort='parent-EH-File',category='application-candidate',
        identity_mode='original-selected-namespace-with-reviewed-EH-projection',namespace_identity=identity,origin_identity=identity,
        projected_object_sha256=eh_metadata['object_sha256'],serialized_symbol_index=eh_metadata['physical_maps']['symbol_map'][str(identity['symbol_index'])],
        member='component.obj',member_sha256=eh_metadata['object_sha256'],source_ledger_sha256=eh_metadata_sha256,
        source_record_ordinal=1,source_record_sha256=digest(eh_metadata),logical_binding_applied=True,
        source_member_layout_verified=False,native_COFF_conformance_collected=False,application_selection_applied=False))
    require(len(records)==len(names)==14346 and len(added)==12,'successor epoch complete/disjoint census')
    return dict(schema_version=2,kind='prepared-CODE-collision-exclusions',policy_id=POLICY,parent_manifest_sha256=INPUTS['prepared_manifest'][1],
        ordinary_prepared_count=14341,broader_application_candidate_count=5,collision_exclusion_count=14346,
        ordinary_names=sorted(set(parent['ordinary_names'])|set(added)),exclusion_names=sorted(names),records=sorted(records,key=lambda r:r['canonical']),
        source_bindings=dict(parent['source_bindings'],typed_composed_first12=typed_members_sha256,parent_EH_File=eh_metadata_sha256),
        application_selected_code_count=None,application_selection_inferred_from_counts=False,**FALSE)


def reconcile(groups,providers,units,central,known_roots,exclusions,*,expected_code_count=208):
    """Source identity join only; closure is not serialization eligibility."""
    require(groups['kind']=='actual-unresolved-LNK-target-groups' and groups['executable_execution'] is False and groups['runtime_eligible'] is False,'actual nonexecuted LINK frontier required')
    reverse=old.reverse_planned(providers);cached={}
    for summary in central['observations']:
        if summary['event']!='SINGLE_ROOT_OBSERVATION':continue
        require(len(summary['roots'])==1 and summary['roots'][0] not in cached,'duplicate cached singleton');cached[summary['roots'][0]]=summary
    known={r['original_address']:r for r in known_roots};require(len(known)==len(known_roots) and set(known)==set(cached),'complete cached original requests differ')
    records=[];missing=[];positive=[];seen=set();counts=Counter()
    for ordinal,group in enumerate(groups['groups'],1):
        require(group['symbol'] not in seen,'duplicate actual demand namespace');seen.add(group['symbol'])
        if group['classification']!='CODE':continue
        name=group['symbol'];require(group['observed_roles']==['code'] and group['included_provenance_is_extraction_proof'] is False,'conflicting CODE role/proof semantics')
        record=dict(symbol=name,group_ordinal=ordinal,group_sha256=digest(group),original_bases=group['original_bases'],original_targets=group['original_targets'])
        if name in exclusions:state='PREPARED_SKIP'
        elif name not in reverse:state='UNSELECTED_OR_NAMESPACE_UNPROVED'
        else:
            address,_=reverse[name];root=root_record(address,providers[address],units);record['root']=root
            require(address in group['original_bases'],'selected canonical demand lacks exact observed original base')
            if address not in cached:state='NEW_SELECTED_ROOT_REQUIRES_OBSERVATION';missing.append(root)
            else:
                require(root==known[address],'cached original physical identity differs');summary=cached[address]
                record['cached_observation']=summary
                if summary['closure_observed'] is True:
                    require(summary['graph_observation_complete'] is True and not summary['blocker_codes'],'positive cached root graph inconsistent')
                    state='CACHED_BARE_POSITIVE_REQUIRES_FRESH_CLASSIFICATION';positive.append(root)
                else:state='CACHED_ORIGINAL_OMISSION_BLOCKED'
        record['state']=state;records.append(record);counts[state]+=1
    require(len(records)==expected_code_count==groups['classifications']['CODE'],'complete immediate CODE frontier census differs')
    return dict(schema_version=1,kind='current-CODE-frontier-reconciliation',policy_id=POLICY,frontier='accepted-V5',
        code_demands=len(records),counts=dict(counts),records=records,new_roots=sorted(missing,key=lambda r:r['original_address']),
        cached_positive_roots=sorted(positive,key=lambda r:r['original_address']),eligibility_not_inferred_from_closure=True,**FALSE)


def run(args):
    inputs={};start=time.monotonic()
    review=base.load_json(base.observe(args.review,args.review_sha256,inputs))
    require(review.get('kind')=='current-code-frontier-metadata-review-v1' and review.get('approved') is True and
        review.get('independent_source_schema_review_pass') is True and review.get('root_authorized') is True and
        review.get('producer_sha256')==PINS and review.get('input_sha256')=={k:h for k,(_,h) in INPUTS.items()} and
        set(review.get('source_sha256',{}))==set(OWNED),'exact reviewed metadata planner and input set required')
    for rel,h in {**review['source_sha256'],**PINS}.items():base.observe(ROOT/rel,h,inputs)
    base.stable(inputs)  # Includes explicit optional-index absence before joins.
    paths={k:base.observe(ROOT/'build/rebuild'/rel,h,inputs) for k,(rel,h) in INPUTS.items()}
    planned=base.load_json(base.observe(args.provider_map,typed.prior.MAP_PIN,inputs))
    base.observe(ROOT/'build/rebuild'/typed.prior.MAP_REVIEW[0],typed.prior.MAP_REVIEW[1],inputs)
    reports={n:base.load_json(base.observe(ROOT/'build/rebuild'/p,base.inventory.EXPECTED[n],inputs)) for n,p in
        [('selection','function-selection-v2.json'),('manifest','objects-20261103T030230Z-7cfc935c.json'),('retained','retained-verify-full-v3.json'),('owners','runtime-data-owners-native-v1.json')]}
    units={u['recipe_id']:u for u in reports['manifest']['units']};proofs={u['recipe_id']:u for u in reports['retained']['units']}
    typed.prior.validate_provider_map(planned,reports['selection']['selections'],units,proofs,reports['owners'])
    epoch=successor_epoch(base.load_json(paths['prepared_manifest']),planned['providers'],base.load_json(paths['typed_members']),
        base.load_json(paths['eh_metadata']),base.load_json(paths['eh_receipt']),typed_members_sha256=INPUTS['typed_members'][1],eh_metadata_sha256=INPUTS['eh_metadata'][1])
    frontier=reconcile(base.load_json(paths['groups']),planned['providers'],units,base.load_json(paths['central']),
        base.load_json(paths['aggregate'])['roots'],set(epoch['exclusion_names']))
    out=Path(args.out).resolve();private=(ROOT/'build/rebuild').resolve()
    require(out.is_relative_to(private) and out!=private and not out.exists() and not any(p.is_relative_to(out) for p in inputs),'new private exclusive metadata output')
    base.stable(inputs);out.mkdir()
    journal=(out/'progress.jsonl').open('x',encoding='utf-8')
    def note(state,**facts):journal.write(json.dumps(dict(state=state,**facts))+'\n');journal.flush();os.fsync(journal.fileno())
    try:
        note('started',code_demands=208)
        for rel,h in review['source_sha256'].items():
            p=out/'source-snapshots'/rel;p.parent.mkdir(parents=True,exist_ok=True);raw=(ROOT/rel).read_bytes();require(base.coff.digest(raw)==h,'snapshot drift');base.pool.fsynced(p,raw)
        base.save_json(out/'prepared-epoch.json',epoch);base.save_json(out/'frontier.json',frontier)
        request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=frontier['new_roots'])
        base.save_json(out/'missing-request.json',request)
        base.save_json(out/'cached-positive-request.json',dict(request,roots=frontier['cached_positive_roots']))
        base.stable(inputs);usage=base.budget(start,out)
        result=dict(schema_version=1,kind='current-code-frontier-metadata-result',status='completed',code_demands=208,counts=frontier['counts'],
            ordinary_prepared_count=14341,collision_exclusion_count=14346,review_sha256=args.review_sha256,
            artifacts={name:base.file_hash(out/name) for name in ('prepared-epoch.json','frontier.json','missing-request.json','cached-positive-request.json')},
            inputs={str(p):h for p,h in inputs.items()},input_stability=True,optional_function_index_present=False,resource_observations=usage,**FALSE)
        result.update(emitted=0,blocked=0)
        return base.finalize_success(out,result,inputs,start,journal,note)
    except BaseException as error:
        try:
            if not journal.closed:note('failed',error_type=type(error).__name__,message=str(error))
        except OSError:pass
        base.save_json(out/'abort.json',dict(status='aborted-no-retry',error_type=type(error).__name__,message=str(error),**FALSE));raise
    finally:
        if not journal.closed:journal.close()


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('review','provider-map','out'):parser.add_argument('--'+name,required=True,type=Path,dest=name.replace('-','_'))
    parser.add_argument('--review-sha256',required=True)
    args=parser.parse_args(argv);result=run(args);print(json.dumps(dict(status=result['status'],counts=result['counts'])));return 0


if __name__=='__main__':raise SystemExit(main())
