"""V8 finite CODE frontier and three-authority metadata epoch; no body reads."""
from __future__ import annotations
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import time
import code_frontier_wave as old
prior=old.prior
base=old.base
ROOT=base.ROOT
require=base.require
digest=base.digest
POLICY='V8-CODE-frontier-wave-metadata-v1'
OWNED=('tools/rebuild/code_frontier_wave_v8.py','tests/rebuild/test_code_frontier_wave_v8.py','docs/rebuild/CODE-FRONTIER-WAVE-V8.md')
PINS={**old.PINS,'tools/rebuild/code_frontier_wave.py':'5218ddc6e20eadfd2b51ff58e3d1cb35fa30abbe8a78ed7d031c4e4914fdf248',
    'tools/rebuild/frontier_wave_factory.py':'254b801f4b39c9da5b6f5473ad1f3c9b3b0ac17828654a7e2a2ebd6a1295a570'}
FALSE=old.FALSE
INPUTS={k:old.INPUTS[k] for k in ('old_receipt','old_requests','new_receipt','new_requests','new_review','quarantine')}
INPUTS.update({
 'groups':('application-link-diagnostic-v8-wave/unresolved-groups.json','daf8c6f1bb526e60cb20ba57173b9f167dd4a5ea5e5b6b8114f5786d4564d324'),
 'link_receipt':('application-link-diagnostic-v8-wave/link-receipt.json.gz','c364d56e6a24ada784073740c778cb3adc6e3170cf79f12812e9c0f7e9a7d38c'),
 'link_review':('application-link-diagnostic-v8-wave/independent-outcome-review.json','3effbc9c6ca7176b5b6a0179d6e9a0b51e29b87d1e2b19dbc7de64172bdfee15'),
 'parent_epoch':('code-frontier-wave-v7-v1/prepared-epoch.json','c87b717a93684435872b3d3f226f854e83baa5960884ffbf0457fb830eced976'),
 'parent_epoch_review':('code-lane-02/v7-wave-outcome-review-v1.json','4405e5ddbc95d7fd9d05cf6c035052837bdd9339bdb04655982ba2bbb0345280'),
 'members3':('frontier-wave-v7-production-v1/members.json','4d914daea1c5934606b568ecba475343260b3c3d14e83b04879908e280fec166'),
 'archive3':('frontier-wave-v7-production-v1/V7-code.lib','aeb5920faa0be15c6c8d174cc0003be8876ebb1ecdfbfb0ae69e177703d7f11f'),
 'receipt3':('frontier-wave-v7-production-v1/receipt.json','4eed3242de2fed5acc3c471a791d64e647db0dad6d3f13930f7cbf4b4b15bcab'),
 'review3':('code-lane-02/v7-factory-outcome-review-v1.json','23acc0cef753cb134fdaea1f86f4d3d319b42f2e43f8cc0f0fe2c6f9c8df60ec'),
 'authority_review3':('code-lane05-synthetic-projection-v1/frontier-wave-v7-context-outcome-review-v1.json','eb1909cea024bf6215aceb0b289d4974172af7ac557964e96fb344cc2cac35c1'),
 'handoff3':('frontier-wave-v7-export-handoff-v1.json','68a8110c92bf095a777f448d743ffd364eff370245d492fe26eee4395d3ec509'),
 'handoff_review3':('code-lane-02/v7-factory-handoff-review-v1.json','6ea5b58192dc6a5490104c9d33bfbd4197a9d9402cc81eecc2c3fda92052a2b4'),
 'native3':('frontier-wave7-native-conformance-v1/receipt.json','8421d0ccf4793c5a7f52d7b7f6e9af6ea21c9d87b6e76abf9eae6c0227b0dd27'),
 'native_review3':('frontier-wave7-native-conformance-v1/independent-outcome-review.json','549fbbdd249fa13045f6ac365159dc68a7aa9b59fd9d66760930813b19dd25aa'),
 'docs_transition':('frontier-wave-v7-post-outcome-docs-v1.json','79c7ec6e5417b7b30733d356d5f68e32dfb6c7752cb41d2929641be54456efaf'),
 'v2_receipt':('frontier-code-root-observation-v2/receipt.json','3afed5cd8a6728f0dbd7b8753fe5b3320524d1123dd68266bfb9fea22f00424a'),
 'v2_requests':('code-frontier-wave-v7-v1/missing-request.json','7f30f61745419f31fcebf0fbea9124528810797473b04f03fb58bc6a1815bf26'),
 'v2_review':('frontier-code-root-observation-v2/independent-outcome-review.json','79da585ca23c7ec5dddb747b0ad67b616c535de770370f0fd3e6cc30d5ef0862')})


def extend_epoch(parent,providers,units,members):
    require(parent['ordinary_prepared_count']==14400 and parent['collision_exclusion_count']==14406 and
        len(parent['records'])==len(parent['exclusion_names'])==len(set(parent['exclusion_names']))==14406,'exact accepted parent epoch')
    records=list(parent['records']);names=set(parent['exclusion_names']);ordinary=set(parent['ordinary_names'])
    require({r['canonical'] for r in records}==names and len(ordinary)==14400 and ordinary<=names,'parent records/names differ')
    for row in records:require(base.pool.canonical(row['namespace_identity'])==row['canonical'],'parent physical namespace changed')
    require(len(members)==3,'complete accepted three-member cohort required')
    for ordinal,member in enumerate(members,1):
        p=member['projection'];require(len(p['requested_roots'])==1,'singleton accepted member')
        root=p['requested_roots'][0];a=root['original_address'];identity={k:root[k] for k in ('recipe_id','object_sha256','symbol_index')}
        name=base.pool.canonical(identity)
        require(root==prior.planner.root_record(a,providers[a],units) and p['exports']==[name] and name not in names and
            p['original_object_sha256']==root['object_sha256'],'accepted three-root identity or collision differs')
        names.add(name);ordinary.add(name)
        records.append(dict(canonical=name,original_address=a,cohort='V7-new-frontier-three',category='ordinary',
            identity_mode='original-selected-physical',namespace_identity=identity,origin_identity=identity,member=member['name'],
            member_sha256=p['output_sha256'],serialized_symbol_index=p['maps']['symbol_map'][str(root['symbol_index'])],
            source_ledger_sha256=INPUTS['members3'][1],source_record_ordinal=ordinal,source_record_sha256=digest(member),logical_binding_applied=True))
    require(len(names)==len(records)==14409 and len(ordinary)==14403,'successor disjoint census')
    return dict(schema_version=4,kind='prepared-CODE-collision-exclusions',policy_id=POLICY,parent_manifest_sha256=INPUTS['parent_epoch'][1],
        ordinary_prepared_count=14403,broader_application_candidate_count=6,collision_exclusion_count=14409,
        ordinary_names=sorted(ordinary),exclusion_names=sorted(names),records=sorted(records,key=lambda r:r['canonical']),
        application_selected_code_count=None,application_selection_inferred_from_counts=False,**FALSE)


def reconcile_v8(groups,providers,units,registry,exclusions,quarantine):
    entries=list(registry['records'].values())
    frontier=prior.planner.reconcile(groups,providers,units,dict(observations=[r['summary'] for r in entries]),
        [r['root'] for r in entries],exclusions,expected_code_count=467)
    require(len(quarantine)==1 and quarantine[0]['root']['original_address']=='0x0086beb0' and
        quarantine[0]['blockers'][0]['code']=='CANONICAL_REFERENCE_GROUP_REQUIRES_REVIEWED_V2','exact prior quarantine')
    qroot=quarantine[0]['root'];qname=base.pool.canonical({k:qroot[k] for k in ('recipe_id','object_sha256','symbol_index')})
    require(qname not in exclusions,'quarantined root cannot become prepared without separately reviewed group proof')
    for item in frontier['records']:
        if item.get('root') and item['root']['original_address'] in registry['records']:
            item['cache_authority']=registry['records'][item['root']['original_address']]['authority']
        if item['symbol']==qname:
            require(item['root']==qroot,'quarantine source changed');item['state']='PRESERVED_REFERENCE_GROUP_QUARANTINE'
            item['quarantine_sha256']=INPUTS['quarantine'][1]
    frontier.update(policy_id=POLICY,frontier='accepted-V8',counts=dict(Counter(r['state'] for r in frontier['records'])))
    frontier['cached_positive_roots']=sorted([r['root'] for r in frontier['records'] if r['state']=='CACHED_BARE_POSITIVE_REQUIRES_FRESH_CLASSIFICATION'],key=lambda r:r['original_address'])
    return frontier


def protect_historical_docs(transition,inputs):
    expected={'docs/rebuild/CODE-FRONTIER-WAVE.md':('b78107f80b4b0884471c9fdf758f10071642cea8090fe15819de6e0a466a8001','code-frontier-wave-v7-v1'),
        'docs/rebuild/FRONTIER-WAVE-FACTORY.md':('7faa39d7102cb090dfa8abb7dcd36106cd887fa17afbce9a48331264c1101d4e','frontier-wave-v7-production-v1')}
    require(transition['kind']=='post-outcome-documentation-only-transition' and transition['producer_replayed'] is False and
        set(transition['documents'])==set(expected),'exact accepted historical doc transition')
    for rel,(sha,folder) in expected.items():
        pair=transition['documents'][rel];require(pair['before']==sha,'old snapshot changed')
        base.observe(ROOT/'build/rebuild'/folder/'source-snapshots'/rel,sha,inputs);base.observe(ROOT/rel,pair['after'],inputs)
    for rel,sha in transition['producer_sources_unchanged'].items():
        require(PINS.get(rel)==sha,'doc transition cannot excuse producer drift');base.observe(ROOT/rel,sha,inputs)


def run(args):
    start=time.monotonic();inputs={};review=base.load_json(base.observe(args.review,args.review_sha256,inputs))
    require(review.get('schema_version')==1 and review.get('kind')=='V8-code-frontier-wave-metadata-review-v1' and
        review.get('approved') is True and review.get('independent_source_schema_review_pass') is True and
        review.get('root_authorized') is True and review.get('reviewer') and review.get('producer_sha256')==PINS and
        review.get('input_sha256')=={k:h for k,(_,h) in INPUTS.items()} and set(review.get('source_sha256',{}))==set(OWNED) and
        review.get('allow_native_tools') is False,'exact independently reviewed V8 metadata scope required')
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
    epoch=extend_epoch(base.load_json(paths['parent_epoch']),expanded['providers'],units,base.load_json(paths['members3']))
    sources=[dict(kind=kind,receipt_sha256=INPUTS[receipt][1],request_sha256=INPUTS[request][1],
        receipt=base.load_json(paths[receipt]),requests=base.load_json(paths[request])['roots'])
        for kind,receipt,request in [('cached-central','old_receipt','old_requests'),('cached-frontier','new_receipt','new_requests'),
            ('cached-frontier','v2_receipt','v2_requests')]]
    registry=old.cache_registry(sources,expanded['providers'],units,expected_total=269)
    registry['policy_id']=POLICY
    frontier=reconcile_v8(base.load_json(paths['groups']),expanded['providers'],units,registry,set(epoch['exclusion_names']),base.load_json(paths['quarantine']))
    out=Path(args.out).resolve();private=(ROOT/'build/rebuild').resolve()
    require(out.is_relative_to(private) and out!=private and not out.exists() and not any(p.is_relative_to(out) for p in inputs),'new exclusive private wave output')
    base.stable(inputs);out.mkdir();journal=(out/'progress.jsonl').open('x',encoding='utf-8')
    def note(state,**facts):journal.write(json.dumps(dict(state=state,**facts))+'\n');journal.flush();os.fsync(journal.fileno())
    try:
        note('started',frontier='accepted-V8',code_demands=467,cached_original_roots=269)
        for rel,h in review['source_sha256'].items():
            raw=(ROOT/rel).read_bytes();require(base.coff.digest(raw)==h,'source snapshot drift');p=out/'source-snapshots'/rel;p.parent.mkdir(parents=True,exist_ok=True);base.pool.fsynced(p,raw)
        for name,value in [('prepared-epoch',epoch),('cache-registry',registry),('frontier',frontier),
            ('missing-request',dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=frontier['new_roots'])),
            ('cached-positive-request',dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=frontier['cached_positive_roots']))]:base.save_json(out/(name+'.json'),value)
        base.stable(inputs)
        result=dict(schema_version=1,kind='V8-CODE-frontier-wave-metadata-result',status='completed',code_demands=467,
            counts=frontier['counts'],cache_roots=269,ordinary_prepared_count=14403,collision_exclusion_count=14409,
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
