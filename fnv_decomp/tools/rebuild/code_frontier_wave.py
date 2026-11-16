"""V7 prepared epoch and distinct-authority cached-root registry, metadata only."""
from __future__ import annotations
import argparse
from collections import Counter
import json
import os
import re
from pathlib import Path
import time
import frontier_code_factory as prior

base=prior.base
ROOT=base.ROOT
POLICY='V7-CODE-frontier-wave-metadata-v1'
OWNED=('tools/rebuild/code_frontier_wave.py','tests/rebuild/test_code_frontier_wave.py','docs/rebuild/CODE-FRONTIER-WAVE.md')
PINS={**prior.PINS,'tools/rebuild/frontier_code_factory.py':'1ded932d2a398724b9595d9ea948cfefbc0faf6adcb77b78767e6f7858bb2f8f'}
FALSE=dict(prior.FALSE,original_objects_read=False,original_image_read=False,source_bodies_read=False,code_emission_performed=False)
INPUTS={
 'groups':('application-link-diagnostic-v7-frontier/unresolved-groups.json','87ca6e030671ca15ff0c640630c66f2dbb6745b4d6bba86d04fa7608cb312f85'),
 'link_receipt':('application-link-diagnostic-v7-frontier/link-receipt.json','05fab245e57474faaecdba76c94b2ed7da3228f5229d2509800360252c6a218f'),
 'link_review':('application-link-diagnostic-v7-frontier/independent-outcome-review.json','578dded065c35f922c55a62299594847ade4f91e371a2a56f1f965ad1e79cf64'),
 'parent_epoch':('current-code-frontier-v5-v1/prepared-epoch.json','e1bb236a98cdecf8480dd0aacedd66866ffe939d61a3d63e34bfe266461260f7'),
 'parent_epoch_review':('code-lane-02/current-frontier-outcome-review-v1.json','618808fb03b51e445071e41f72976e044700f46788a14c6b7584342d42a85370'),
 'members59':('frontier-code-production-v5-v1/members.json','9d7ae7c145a7da035ed5437784d2d0334d4aae9385ce854a5e788e9dc5251429'),
 'archive59':('frontier-code-production-v5-v1/frontier-code.lib','48c1bd32c18ac802aac6cd6781912b73205a43b9c4115d1df538ca0b5af77ebd'),
 'receipt59':('frontier-code-production-v5-v1/receipt.json','bbd4e450b2317c1adda3923dcfc656b55ed6f4bab2276614e3e2b53458da3d05'),
 'review59':('code-lane-02/frontier-factory-outcome-review-v1.json','5b7abc7509e1f24c0057d15d0a19454d10698d401b6b99b20a7ae1526b4229f3'),
 'authority_review59':('code-lane05-synthetic-projection-v1/frontier-v5-context-authority-outcome-review-v1.json','00b05fdfaca7e879da1272600e6337a9916e8ecf994e50046db300ddc9262f5f'),
 'handoff59':('frontier-code-production-v5-export-handoff-v1.json','a3eec7d2ef1e8f7c75dd20d2950cc91597f1915861294614c6b56bdb21a03d5b'),
 'handoff_review59':('code-lane-02/frontier-factory-handoff-review-v1.json','2dfa68f7d1e0affff157ac3654d85f392341aee6b65a921aa89c37a1b9c738ba'),
 'docs_transition':('frontier-code-production-v5-post-outcome-docs-v1.json','bf729ef48746f78ca6829b55d3cd957fd0f54895b1f0b7b3667486d32e9e2aa5'),
 'native59':('frontier-code59-native-conformance-v1/receipt.json','8c70779205139a05732092274e67b1643eacfbd6713dcf51387800557d8c2c6f'),
 'native_review59':('frontier-code59-native-conformance-v1/independent-outcome-review.json','bdaddb0f27949b60a7820c2d402ff0081a5c8ea2bdf48d1808835c07dcea76f0'),
 'ML_metadata':('parent-eh-model-loader-projection-v1/integration-metadata.json','e45a0a84e3af7c3b34e80ec107c72894ff96ef3826b2dbc33f944bd554aaa368'),
 'ML_object':('parent-eh-model-loader-projection-v1/component.obj','c7ee32f03ebc9acb559b6516f526ca515733564035259e15271f6f3b1029afc9'),
 'ML_receipt':('parent-eh-model-loader-projection-v1/projection.json','f90c7d1de48b7ef914eed5036e2c915ba7130c966f76db42e76671808d57a4b8'),
 'ML_review':('code-lane08-source-triage-v1/ModelLoader-EH-groups-artifact-review-v1.json','7fe86281277b92e9b04ceaa6152976321d8b4df380ae0e654502763ef5953f0b'),
 'ML_review_correction':('code-lane08-source-triage-v1/ModelLoader-EH-groups-artifact-review-correction-v1.json','96f92f1c2f187a85dae704a8726a6c60d486d83b91e4619327d30db3990d5061'),
 'ML_ledger_review':('code-lane08-source-triage-v1/ModelLoader-EH-groups-integration-ledger-review-v1.json','c8a2610ca79214323db1562fd3c4f2925e8047e843591655fce894cef677ca9f'),
 'ML_native':('model-loader-native-conformance-v1/receipt.json','d84b5d5b2dd8b22713b28a2d12341b181f84bfc0bdd3892b10ea45779b32dfa5'),
 'ML_native_review':('model-loader-native-conformance-v1/independent-outcome-review.json','ad81b07634c82dce89e77cc02158efe5aa3bac74ecd4bd484809ce7ad76f1710'),
 'old_receipt':('central-code-root-observation-v1/receipt.json','290ac0e8c1ffbfd89df7dd6cdbbdb8df363edca58111b7aa19fe842aa26cc8e4'),
 'old_requests':('central-code-root-observation-v1/request.json','f778bdd8453d9813b978acbba7547e5733c585ebf5043b9769986bf8cf7e0665'),
 'new_receipt':('frontier-code-root-observation-v1/receipt.json','ea4e02c8e62264f65662ed4c9d5fdd2e4d990bf9b6c3dd70b5e0553b61f43da5'),
 'new_requests':('current-code-frontier-v5-v1/missing-request.json','c59c18a92d790c93b73136967338e75826e6c089ebebd7c7194c680aadee03a1'),
 'new_review':('frontier-code-root-observation-v1/independent-outcome-review.json','689a77c1da079d5f2c168319a7e8810cec2657a315f82b5281d776e46c997026'),
 'quarantine':('frontier-code-production-v5-v1/blocked.json','8a3de38e30a0633eed55185d3863d33104f037d54cfc029a4b34082d0d275b3f')}
require=base.require
digest=base.digest


def extend_epoch(parent,providers,units,members,ml,receipt):
    require(parent['ordinary_prepared_count']==14341 and parent['collision_exclusion_count']==14346 and
        len(parent['records'])==len(parent['exclusion_names'])==len(set(parent['exclusion_names']))==14346,'exact accepted parent epoch')
    records=list(parent['records']);names=set(parent['exclusion_names']);ordinary=set(parent['ordinary_names'])
    require({r['canonical'] for r in records}==names and len(ordinary)==14341,'parent record/name mismatch')
    for r in records:require(base.pool.canonical(r['namespace_identity'])==r['canonical'],'parent physical namespace changed')
    require(len(members)==59,'complete accepted59 cohort')
    for ordinal,member in enumerate(members,1):
        p=member['projection'];require(len(p['requested_roots'])==1,'singleton accepted member')
        root=p['requested_roots'][0];a=root['original_address'];expected=prior.planner.root_record(a,providers[a],units)
        identity={k:root[k] for k in ('recipe_id','object_sha256','symbol_index')};name=base.pool.canonical(identity)
        require(root==expected and p['exports']==[name] and name not in names and p['original_object_sha256']==root['object_sha256'],
            'accepted59 logical/source identity or collision differs')
        names.add(name);ordinary.add(name)
        records.append(dict(canonical=name,original_address=a,cohort='current-V5-frontier-59',category='ordinary',
            identity_mode='original-selected-physical',namespace_identity=identity,origin_identity=identity,
            member=member['name'],member_sha256=p['output_sha256'],serialized_symbol_index=p['maps']['symbol_map'][str(root['symbol_index'])],
            source_ledger_sha256=INPUTS['members59'][1],source_record_ordinal=ordinal,source_record_sha256=digest(member),logical_binding_applied=True))
    root=ml['original_root'];a=root['original_address'];identity={k:root[k] for k in ('recipe_id','object_sha256','symbol_index')};name=base.pool.canonical(identity)
    require(a==ml['parent']==receipt['parent']=='0x00448420' and root==prior.planner.root_record(a,providers[a],units) and
        ml['physical_exports']==[name] and name not in names and ml['source_object_sha256']==identity['object_sha256'] and
        ml['receipt_sha256']==INPUTS['ML_receipt'][1] and receipt['projection']['input_sha256']==identity['object_sha256'] and
        receipt['projection']['output_sha256']==ml['object_sha256'] and receipt['projection']['export']==name and
        receipt['projection']['maps']==ml['physical_maps'] and ml['all_parent_EH_fields_preserved'] is True and ml['no_symbol_coalescing'] is True and
        receipt['input_stability'] is True and receipt['observation_sha256']==ml['observation_sha256'] and
        receipt['input_request_sha256']==ml['input_request_sha256'] and receipt['source_member_layout_verified'] is False and
        ml['native_COFF_conformance_collected'] is False and
        all(ml[k] is False and receipt[k] is False for k in ('provider_selected','runtime_eligible','ABI_verified','link_ready','namespace_approved')),
        'ModelLoader exact accepted namespace/source/physical map differs')
    names.add(name);records.append(dict(canonical=name,original_address=a,cohort='ModelLoader-EH',category='application-candidate',
        identity_mode='original-selected-namespace-with-reviewed-EH-projection',namespace_identity=identity,origin_identity=identity,
        projected_object_sha256=ml['object_sha256'],member='component.obj',member_sha256=ml['object_sha256'],
        serialized_symbol_index=ml['physical_maps']['symbol_map'][str(root['symbol_index'])],
        source_ledger_sha256=INPUTS['ML_metadata'][1],source_record_ordinal=1,source_record_sha256=digest(ml),logical_binding_applied=True,
        historical_native_flag=ml['native_COFF_conformance_collected'],subsequent_native_review_sha256=INPUTS['ML_native_review'][1],
        source_member_layout_verified=receipt['source_member_layout_verified'],application_selection_applied=False))
    require(len(names)==len(records)==14406 and len(ordinary)==14400,'successor disjoint full census differs')
    return dict(schema_version=3,kind='prepared-CODE-collision-exclusions',policy_id=POLICY,parent_manifest_sha256=INPUTS['parent_epoch'][1],
        ordinary_prepared_count=14400,broader_application_candidate_count=6,collision_exclusion_count=14406,
        ordinary_names=sorted(ordinary),exclusion_names=sorted(names),records=sorted(records,key=lambda r:r['canonical']),
        application_selected_code_count=None,application_selection_inferred_from_counts=False,**FALSE)


def cache_registry(authorities,providers,units,*,expected_total=215):
    records={};receipts=set();locators=set()
    valid_hash=lambda value:isinstance(value,str) and re.fullmatch('[0-9a-f]{64}',value) is not None
    for source in authorities:
        receipt=source['receipt'];requests=source['requests'];sha=source['receipt_sha256']
        require(valid_hash(sha) and valid_hash(source['request_sha256']) and sha not in receipts and receipt['status']=='metadata-only' and receipt['input_stability'] is True and
            receipt['optional_function_index_present'] is False and source['request_sha256']==receipt['request_sha256'],
            'duplicate/unaccepted cache epoch or borrowed request authority')
        receipts.add(sha);roots={r['original_address']:r for r in requests}
        require(len(roots)==len(requests),'duplicate cache request root')
        seen=set()
        for summary in receipt['observations']:
            if summary['event']!='SINGLE_ROOT_OBSERVATION':continue
            require(len(summary['roots'])==1,'cache singleton scope');a=summary['roots'][0];root=roots[a]
            require(a not in seen and a not in records and root==prior.planner.root_record(a,providers[a],units) and
                summary['recipe_id']==root['recipe_id'] and type(summary['closure_observed']) is bool and
                type(summary['graph_observation_complete']) is bool,'cache duplicate/conflicting physical root or state')
            if summary['closure_observed']:require(summary['graph_observation_complete'] and not summary['blocker_codes'],'positive cache has incomplete proof')
            else:require(summary['blocker_codes'],'negative cache lacks blockers')
            require(valid_hash(summary['record_sha256']) and (valid_hash(summary.get('certificate_sha256')) or
                (not summary['closure_observed'] and summary.get('certificate_sha256') is None)), 'cache record/certificate digest schema')
            locator=dict(kind=source['kind'],receipt_sha256=sha,request_sha256=source['request_sha256'],record_sha256=summary['record_sha256'],
                certificate_sha256=summary.get('certificate_sha256'),contract_identity_sha256=None,
                contract_identity_is_bound_through_record_hash=True)
            if source['kind']=='cached-central':
                require(type(summary['lane']) is int and 1<=summary['lane']<=8,'exact old cache lane')
                locator.update(lane=summary['lane'],ordinal=summary['lane_record_ordinal'])
            else:require(source['kind']=='cached-frontier','unknown cache authority');locator.update(ordinal=summary['ordinal'])
            require(type(locator['ordinal']) is int and locator['ordinal']>0,'positive integer cache source ordinal')
            key=(sha,source['kind'],locator.get('lane'),locator['ordinal'])
            require(key not in locators,'one source locator cannot identify two original roots');locators.add(key)
            records[a]=dict(root=root,summary=summary,authority=locator);seen.add(a)
        require(seen==set(roots),'cache requests/observations incomplete')
    require(len(records)==expected_total,'complete cached root universe differs')
    return dict(schema_version=1,kind='distinct-authority-original-root-registry',policy_id=POLICY,roots=len(records),
        authorities=[dict(kind=s['kind'],receipt_sha256=s['receipt_sha256'],request_sha256=s['request_sha256'],roots=len(s['requests'])) for s in authorities],
        records=records,contract_digest_loaded_only_from_authenticated_body=True,**FALSE)


def reconcile_v7(groups,providers,units,registry,exclusions,quarantine):
    entries=list(registry['records'].values())
    frontier=prior.planner.reconcile(groups,providers,units,dict(observations=[r['summary'] for r in entries]),
        [r['root'] for r in entries],exclusions,expected_code_count=249)
    require(len(quarantine)==1 and quarantine[0]['root']['original_address']=='0x0086beb0' and
        quarantine[0]['blockers'][0]['code']=='CANONICAL_REFERENCE_GROUP_REQUIRES_REVIEWED_V2','exact prior group quarantine required')
    qroot=quarantine[0]['root'];qname=base.pool.canonical({k:qroot[k] for k in ('recipe_id','object_sha256','symbol_index')})
    require(qname not in exclusions,'quarantined root cannot become prepared without a separately reviewed group proof')
    for item in frontier['records']:
        if item.get('root') and item['root']['original_address'] in registry['records']:
            item['cache_authority']=registry['records'][item['root']['original_address']]['authority']
        if item['symbol']==qname and item['state']!='PREPARED_SKIP':
            require(item['root']==qroot,'prior quarantine source identity changed')
            item['state']='PRESERVED_REFERENCE_GROUP_QUARANTINE';item['quarantine_sha256']=INPUTS['quarantine'][1]
    frontier.update(policy_id=POLICY,frontier='accepted-V7',counts=dict(Counter(r['state'] for r in frontier['records'])))
    frontier['cached_positive_roots']=sorted([r['root'] for r in frontier['records'] if r['state']=='CACHED_BARE_POSITIVE_REQUIRES_FRESH_CLASSIFICATION'],key=lambda r:r['original_address'])
    return frontier


def protect_historical_docs(transition,inputs):
    expected={'docs/rebuild/CURRENT-CODE-FRONTIER.md':('bebb5240ba0a96a262aad6b7d2c5dcd520e60d5a1ac77832e0cf7d619b486dcc','current-code-frontier-v5-v1'),
        'docs/rebuild/FRONTIER-CODE-FACTORY.md':('83d13d48c8ff3e19aa7f55e3a9ba915018c840e479addc283ad7ce1898fe2f36','frontier-code-production-v5-v1')}
    require(transition['kind']=='post-outcome-documentation-only-transition' and transition['producer_replayed'] is False and
        set(transition['documents'])==set(expected),'exact accepted post-outcome documentation transition')
    for rel,(old_sha,folder) in expected.items():
        pair=transition['documents'][rel];require(pair['before']==old_sha,'historical document source changed')
        base.observe(ROOT/'build/rebuild'/folder/'source-snapshots'/rel,old_sha,inputs)
        base.observe(ROOT/rel,pair['after'],inputs)
    for rel,h in transition['producer_sources_unchanged'].items():
        require(PINS.get(rel)==h,'post-doc transition cannot excuse producer drift');base.observe(ROOT/rel,h,inputs)


def run(args):
    start=time.monotonic();inputs={};review=base.load_json(base.observe(args.review,args.review_sha256,inputs))
    require(review.get('schema_version')==1 and review.get('kind')=='V7-code-frontier-wave-metadata-review-v1' and
        review.get('approved') is True and review.get('independent_source_schema_review_pass') is True and
        review.get('root_authorized') is True and review.get('reviewer') and review.get('producer_sha256')==PINS and
        review.get('input_sha256')=={k:h for k,(_,h) in INPUTS.items()} and set(review.get('source_sha256',{}))==set(OWNED) and
        review.get('allow_native_tools') is False,'exact independently reviewed V7 metadata scope required')
    for rel,h in {**PINS,**review['source_sha256']}.items():base.observe(ROOT/rel,h,inputs)
    base.stable(inputs)
    paths={k:base.observe(ROOT/'build/rebuild'/rel,h,inputs) for k,(rel,h) in INPUTS.items()}
    protect_historical_docs(base.load_json(paths['docs_transition']),inputs)
    reports={n:base.load_json(base.observe(ROOT/'build/rebuild'/p,base.inventory.EXPECTED[n],inputs)) for n,p in
        [('selection','function-selection-v2.json'),('manifest','objects-20261103T030230Z-7cfc935c.json'),('retained','retained-verify-full-v3.json'),('owners','runtime-data-owners-native-v1.json')]}
    units={u['recipe_id']:u for u in reports['manifest']['units']};proofs={u['recipe_id']:u for u in reports['retained']['units']}
    expanded=base.load_json(base.observe(args.provider_map,prior.fields.MAP_PIN,inputs))
    base.observe(ROOT/'build/rebuild'/prior.fields.MAP_REVIEW[0],prior.fields.MAP_REVIEW[1],inputs)
    prior.fields.validate_provider_map(expanded,reports['selection']['selections'],units,proofs,reports['owners'])
    require(len(expanded['providers'])==68657 and len(units)==len(proofs)==2988,'complete planned native universe differs')
    epoch=extend_epoch(base.load_json(paths['parent_epoch']),expanded['providers'],units,base.load_json(paths['members59']),
        base.load_json(paths['ML_metadata']),base.load_json(paths['ML_receipt']))
    sources=[dict(kind=kind,receipt_sha256=INPUTS[receipt][1],request_sha256=INPUTS[request][1],
        receipt=base.load_json(paths[receipt]),requests=base.load_json(paths[request])['roots'])
        for kind,receipt,request in [('cached-central','old_receipt','old_requests'),('cached-frontier','new_receipt','new_requests')]]
    registry=cache_registry(sources,expanded['providers'],units)
    frontier=reconcile_v7(base.load_json(paths['groups']),expanded['providers'],units,registry,set(epoch['exclusion_names']),base.load_json(paths['quarantine']))
    out=Path(args.out).resolve();private=(ROOT/'build/rebuild').resolve()
    require(out.is_relative_to(private) and out!=private and not out.exists() and not any(p.is_relative_to(out) for p in inputs),'new exclusive private wave output')
    base.stable(inputs);out.mkdir();journal=(out/'progress.jsonl').open('x',encoding='utf-8')
    def note(state,**facts):journal.write(json.dumps(dict(state=state,**facts))+'\n');journal.flush();os.fsync(journal.fileno())
    try:
        note('started',frontier='accepted-V7',code_demands=249,cached_original_roots=215)
        for rel,h in review['source_sha256'].items():
            raw=(ROOT/rel).read_bytes();require(base.coff.digest(raw)==h,'source snapshot drift');p=out/'source-snapshots'/rel;p.parent.mkdir(parents=True,exist_ok=True);base.pool.fsynced(p,raw)
        for name,value in [('prepared-epoch',epoch),('cache-registry',registry),('frontier',frontier),
            ('missing-request',dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=frontier['new_roots'])),
            ('cached-positive-request',dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=frontier['cached_positive_roots']))]:base.save_json(out/(name+'.json'),value)
        base.stable(inputs)
        result=dict(schema_version=1,kind='V7-CODE-frontier-wave-metadata-result',status='completed',code_demands=249,
            counts=frontier['counts'],cache_roots=215,ordinary_prepared_count=14400,collision_exclusion_count=14406,
            artifacts={n:base.file_hash(out/n) for n in ('prepared-epoch.json','cache-registry.json','frontier.json','missing-request.json','cached-positive-request.json')},
            review_sha256=args.review_sha256,inputs={str(p):h for p,h in inputs.items()},input_stability=True,optional_function_index_present=False,
            resource_observations=base.budget(start,out),emitted=0,blocked=0,**FALSE)
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
    parser.add_argument('--review-sha256',required=True);args=parser.parse_args(argv)
    result=run(args);print(json.dumps(dict(status=result['status'],counts=result['counts'])));return 0


if __name__=='__main__':raise SystemExit(main())
