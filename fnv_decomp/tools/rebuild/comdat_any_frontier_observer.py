"""Finite evidence-only COMDAT ANY observer; no reference/native/code writer."""
from __future__ import annotations
from collections import Counter
import argparse
import gzip
import json
import os
from pathlib import Path
import time

import coff_inventory as native_inventory
import ordinary_code_projection as base
import comdat_any_frontier_contexts as selector
import comdat_any_root_composer as composer

ROOT=base.ROOT
POLICY='finite-comdat-any-frontier-witness-observer-v1'
OWNED=('tools/rebuild/comdat_any_frontier_observer.py','tests/rebuild/test_comdat_any_frontier_observer.py',
       'docs/rebuild/COMDAT-ANY-FRONTIER-OBSERVER.md')
PINS={**base.PINS,
    'tools/rebuild/ordinary_code_projection.py':'e01437aed27549d8892035d3ea7f1500a5e15150bb14a8d56db95ff17c1dac8d',
    'tools/rebuild/comdat_any_frontier_contexts.py':'0b306c51c32626714b48058c42160c0efc9371b95c49bb80d8f908932b9bbda1',
    'tools/rebuild/frontier_root_collect_v3.py':selector.COLLECTOR_PIN,
    'tools/rebuild/comdat_any_code_omission.py':composer.WITNESS_PIN,
    'tools/rebuild/comdat_any_root_composer.py':'243559315e7d3a3799d3e5d8e582973406dcc0a481a80c9af74d7ac7ef8b3e5d'}
ARTIFACTS={'frontier','registry','new_receipt','manifest','retained','selection','recipes','prepared_epoch','epoch_review'}
ACCEPTANCES={'selector_freeze','selector_review','comdat_source_review','comdat_authority_review',
             'metadata_review','new_receipt_review'}
KNOWN_ACCEPTANCES={
    'selector_freeze':'82b7d1f54140a47c0cd78db75d69753b37e82bde61b194f2c0e2df5cad04707f',
    'selector_review':'684f2f29fae0125111d61c0c2e81e8a6dedc980eaca9e6f22bacc92f68aa9988',
    'comdat_source_review':'d6232107013645ed452e1346c1b07c9e4ccfe3549f7fed5121230c6f45ceb04d',
    'comdat_authority_review':'a4def4f92e05d817e66db4b7a4999d78e15aaaccec3a9fdc4b42b99b0d400cb9',
    'metadata_review':'b4b4369eaa2535c77032cec29913e0d78aa6dedbe208eb1ed23cb4e2eee3920b',
    'new_receipt_review':'49b35751bc9135e606695d83fc79cabe68d9ca9578750f829234ea10aa19ebbc'}
METADATA_PINS=dict(frontier='b7ef2d261f8a25571495e541a2cd77ecdae40ed1d0879257171c794777a2182f',
    registry='7c11ea72a7375cadf79771c8a1aa9f02f554e062e811ec9e852042df9aca67df',
    new_receipt='6eec875919603cd9cd3ce9bea7a34b82596f55dea95bc6253b6811aa08cd35ab',
    prepared_epoch='714d970200b9333293a7e643c6f2b7a78b2829cbe7cb0b021bd0ee9515d5749b',
    epoch_review='b4b4369eaa2535c77032cec29913e0d78aa6dedbe208eb1ed23cb4e2eee3920b')
FALSE=dict(provider_selected=False,runtime_eligible=False,ABI_verified=False,link_ready=False,
    namespace_approved=False,full_serialization_eligible=False,materialization_approved=False,
    emission_performed=False,code_emission_performed=False,native_tools_run=False,
    executable_link_performed=False,game_execution_performed=False,reference_image_read=False,
    global_link_uniqueness_proved=False,application_manifest_adopted=False)
MAX_ROW=64*1024**2
MAX_DETAILS=4*1024**3
require=base.require
digest=base.digest
exact=composer.exact


def _ref(ref, *, private=True):
    require(type(ref) is dict and set(ref)=={'path','sha256'} and type(ref['path']) is str and
        selector.sha(ref['sha256']),'exact file reference required')
    path=(ROOT/ref['path']).resolve()
    boundary=(ROOT/'build/rebuild').resolve() if private else ROOT.resolve()
    require(path.is_relative_to(boundary) and path!=boundary,'foreign input reference')
    return path


def validate_request_context(request,context,loaded_artifacts):
    """Pure complete-selector replay; paths are validated without opening them."""
    require(type(context) is dict and set(context)=={'schema_version','kind','epoch','request_sha256',
        'artifacts','acceptances','sources','provider_selected','runtime_eligible','emission_performed','reference_image_read'} and
        type(context['schema_version']) is int and context['schema_version']==1 and
        context['kind']=='finite-comdat-any-frontier-observer-context' and
        type(context['epoch']) is str and 0<len(context['epoch'])<=100 and context['epoch'].isascii() and
        all(context[k] is False for k in ('provider_selected','runtime_eligible','emission_performed','reference_image_read')),
        'exact nonpromoted observer context required')
    require(context['request_sha256']==selector.document_hash(request) and set(context['artifacts'])==ARTIFACTS and
        set(context['acceptances'])==ACCEPTANCES and set(loaded_artifacts)==ARTIFACTS,'observer context/request artifact set')
    for name,ref in context['artifacts'].items():
        _ref(ref,private=name!='recipes')
        if name in METADATA_PINS:require(ref['sha256']==METADATA_PINS[name],'fixed accepted V8 metadata pin differs')
        # Original manifest/proof/selection/recipe formatting belongs to their
        # immutable producers. run() authenticates those raw files before JSON
        # parsing; this pure join never invents a reserialization fingerprint.
        if name in ('frontier','registry','new_receipt','prepared_epoch'):
            require(ref['sha256']==selector.document_hash(loaded_artifacts[name],sort_keys=name!='new_receipt'),
                'loaded artifact document differs: '+name)
    for name,ref in context['acceptances'].items():
        _ref(ref)
        if name in KNOWN_ACCEPTANCES:require(ref['sha256']==KNOWN_ACCEPTANCES[name],'unaccepted source/selector acceptance')
    a=loaded_artifacts
    fresh=selector.select_candidates(a['frontier'],a['registry'],a['new_receipt'],context['artifacts']['new_receipt']['sha256'])
    require(exact(fresh,request),'whole accepted selector request replay differs')
    require(len(request['roots'])==len(request['candidates'])>0,'nonempty whole finite candidate request required')
    require(request['frontier_sha256']==context['artifacts']['frontier']['sha256'] and
        request['registry_sha256']==context['artifacts']['registry']['sha256'],'selector context body lineage')
    for key in ('manifest','retained','selection','recipes'):
        require(context['artifacts'][key]['sha256']==base.inventory.EXPECTED[key],'original retained native epoch differs')
    prepared=a['prepared_epoch']
    require(prepared.get('kind')=='prepared-CODE-collision-exclusions' and
        prepared.get('application_selection_inferred_from_counts') is False and
        all(prepared.get(k) is False for k in ('provider_selected','runtime_eligible','application_manifest_adopted')),
        'prepared epoch is collision evidence only')
    require(type(prepared.get('exclusion_names')) is list and len(set(prepared['exclusion_names']))==len(prepared['exclusion_names']) and
        all(c['symbol'] not in set(prepared['exclusion_names']) for c in request['candidates']),
        'witness request competes with already prepared code')
    wanted={}
    for candidate in request['candidates']:
        auth=candidate['authority'];key=(auth['kind'],auth['receipt_sha256'],auth['request_sha256'])
        wanted.setdefault(key,set()).add(auth.get('lane'))
    require(type(context['sources']) is list and len(context['sources'])==len(wanted),'complete exact selected source authority count')
    sources={}
    for source in context['sources']:
        require(type(source) is dict and set(source)=={'kind','receipt','request','details'},'unknown source reference schema')
        _ref(source['receipt']);_ref(source['request'])
        key=(source['kind'],source['receipt']['sha256'],source['request']['sha256'])
        require(key in wanted and key not in sources and type(source['details']) is list,'borrowed/duplicate source authority')
        lanes=set()
        for detail in source['details']:
            require(type(detail) is dict and set(detail)=={'lane','path','sha256'},'unknown exact detail reference')
            lane=detail['lane'];require(lane is None if source['kind']!='cached-central' else type(lane) is int and 1<=lane<=8,
                'source kind/lane schema')
            require(lane not in lanes,'duplicate detail lane');lanes.add(lane)
            _ref({k:detail[k] for k in ('path','sha256')})
        require(lanes==wanted[key],'only exact selected source lanes allowed');sources[key]=source
    return sources


def validate_selected_row(row,candidate):
    root=candidate['root'];auth=candidate['authority'];s=candidate['summary']
    selector.root_identity(root)
    selector.summary(s,central=auth['kind']=='cached-central')
    kind=auth['kind'];central=kind=='cached-central'
    require(kind in ('cached-central','cached-frontier','new-frontier-v3') and set(auth)==
        {'kind','receipt_sha256','request_sha256','ordinal','record_sha256','certificate_sha256',
         'contract_identity_sha256','contract_identity_is_bound_through_record_hash'} |
        ({'lane'} if central else {'details_sha256'} if kind=='new-frontier-v3' else set()) and
        type(auth['ordinal']) is int and auth['ordinal']==s['lane_record_ordinal' if central else 'ordinal'] and
        (not central or type(auth['lane']) is int and auth['lane']==s['lane']) and
        selector.sha(auth['receipt_sha256']) and selector.sha(auth['request_sha256']) and
        (kind!='new-frontier-v3' or selector.sha(auth['details_sha256'])) and
        auth['contract_identity_sha256'] is None and auth['contract_identity_is_bound_through_record_hash'] is True,
        'exact selected body source locator/deferred identity differs')
    require(exact(s['roots'],[root['original_address']]) and s['recipe_id']==root['recipe_id'] and
        s['closure_observed'] is False,'selected original negative summary scope differs')
    require(type(row) is dict and set(row)=={'schema_version','policy_id','event','recipe_id','requested_roots',
        'provenance','contract','contract_identity_sha256','certificate_sha256','certificate','closure_observed',
        'graph_observation_complete','root_closure_candidate','blockers','unit_EH_evidence'} | set(base.collector.FALSE) and
        digest(row)==auth['record_sha256']==s['record_sha256'] and
        type(row.get('schema_version')) is int and row['schema_version']==1 and
        row.get('event')=='SINGLE_ROOT_OBSERVATION' and row.get('policy_id')=='central-ordinary-root-views-v1' and
        exact(row.get('requested_roots'),[root]) and row.get('recipe_id')==root['recipe_id'],
        'full original singleton record/physical identity differs')
    contract=row['contract'];cert=row['certificate'];p=row['provenance']
    require(type(contract) is dict and set(contract)==base.CONTRACT_KEYS and exact(p,contract['provenance']) and
        digest(contract)==row['contract_identity_sha256']==cert['contract_identity_sha256'] and
        digest(cert)==row['certificate_sha256']==auth['certificate_sha256']==s['certificate_sha256'],
        'full original contract/negative certificate digest differs')
    require(row.get('closure_observed') is False and cert.get('closure_observed') is False and
        cert.get('policy_id')==base.ordinary.POLICY and
        type(row.get('graph_observation_complete')) is bool and
        row['graph_observation_complete'] is cert.get('graph_observation_complete') is s['graph_observation_complete'] and
        type(row.get('root_closure_candidate')) is bool and row['root_closure_candidate'] is cert.get('root_closure_candidate') and
        exact(row['blockers'],cert['blockers']) and
        exact(dict(Counter(b['code'] for b in cert['blockers'])),s['blocker_codes']) and
        selector.ROOT_BLOCKER in s['blocker_codes'],'original negative blocker scope differs')
    require(all(row.get(k) is False for k in base.collector.FALSE) and
        all(cert.get(k) is False for k in ('provider_selected','runtime_eligible','full_serialization_eligible')),
        'original source record/certificate promoted')
    require(p.get('scope_mode')=='singleton' and p.get('recipe_id')==root['recipe_id'] and
        type(p.get('recipe_index')) is int and p['recipe_index']==root['recipe_index'] and
        p.get('object_sha256')==root['object_sha256'] and p.get('source_sha256')==root['source_sha256'] and
        p.get('request_sha256')==auth['request_sha256'] and
        exact(contract['roots'],[{k:root[k] for k in base.NATIVE_KEYS}]),'original provenance/request/native scope join')
    return contract,cert


def observe_member(raw,row,candidate):
    """Fresh native policy only; this function cannot emit code or read a PE."""
    contract,cert=validate_selected_row(row,candidate);root=candidate['root']
    before=digest(dict(row=row,candidate=candidate))
    preflight=composer.assess_native_definition(raw,contract,cert,root,policy_id=composer.POLICY)
    witnesses=[];composed=None
    if preflight['eligible']:
        census=preflight['definition_census']
        observation=composer.policy.observe_comdat_any_code_policy(raw,contract,cert,root,census,policy_id=composer.policy.POLICY)
        witnesses=[dict(kind=composer.WITNESS_KIND,definition_census=census,observation=observation)]
        composed=composer.compose(raw,contract,cert,witnesses,policy_id=composer.POLICY)
        summary=composer.summarize_unsupported(raw,contract,cert,witnesses,composed,policy_id=composer.POLICY)
    else:
        ids=[b['blocker_id'] for b in cert['blockers']]
        summary=dict(state='no-policy-for-unsupported-native-form',original_blocker_ids=ids,
            discharged_blocker_ids=[],remaining_blocker_ids=ids,original_occurrences=len(ids),
            discharged_occurrences=0,remaining_occurrences=len(ids),serialization_approved=False)
    require(digest(dict(row=row,candidate=candidate))==before,'observer changed original negative inputs')
    return dict(schema_version=1,policy_id=POLICY,root=root,authority=candidate['authority'],
        source_record_sha256=digest(row),contract_identity_sha256=digest(contract),
        original_negative_certificate=cert,original_negative_certificate_sha256=digest(cert),
        original_certificate_unchanged=True,native_preflight=preflight,witnesses=witnesses,composed=composed,
        unsupported_summary=summary,serialization_performed=False,original_object_sha256=base.coff.digest(raw),**FALSE)


def validate_source(source,receipt,requests,candidates):
    """Authenticate exact selected summaries against one finite source receipt."""
    require(receipt.get('status')=='metadata-only' and receipt.get('input_stability') is True and
        receipt.get('optional_function_index_present') is False and
        receipt.get('request_sha256')==source['request']['sha256'] and
        all(receipt.get(k) is False for k in base.collector.FALSE),'unaccepted original source receipt')
    require(type(requests) is dict and set(requests)=={'schema_version','kind','roots'} and
        type(requests['schema_version']) is int and requests['schema_version']==1 and
        requests['kind']=='fnv-finite-ordinary-root-request' and type(requests.get('roots')) is list,
        'original source finite request roots required')
    roots={r['original_address']:r for r in requests['roots']}
    require(len(roots)==len(requests['roots']),'duplicate original source request roots')
    summaries={}
    for s in receipt['observations']:
        if s['event']!='SINGLE_ROOT_OBSERVATION':continue
        require(len(s['roots'])==1 and s['roots'][0] not in summaries,'duplicate original source singleton')
        summaries[s['roots'][0]]=s
    require(set(summaries)==set(roots),'complete original source summary/request coverage')
    central=source['kind']=='cached-central'
    require(source['kind'] in ('cached-central','cached-frontier','new-frontier-v3') and
        receipt.get('policy_id')==('central-ordinary-root-views-v1' if central else
        'new-frontier-ordinary-root-observation-v3' if source['kind']=='new-frontier-v3' else
        'new-frontier-ordinary-root-observation-v2' if source['receipt']['sha256']==selector.producer.AUTHORITIES[2]['receipt_sha256'] else
        'new-frontier-ordinary-root-observation-v1'),'source kind/producer policy differs')
    wanted={};locators=set()
    for candidate in candidates:
        auth=candidate['authority'];root=candidate['root'];a=root['original_address']
        require((auth['kind'],auth['receipt_sha256'],auth['request_sha256'])==
            (source['kind'],source['receipt']['sha256'],source['request']['sha256']) and a in roots and
            exact(root,roots[a]) and exact(candidate['summary'],summaries[a]),'selected original request/receipt/summary borrowed')
        s=summaries[a];selector.summary(s,central=central)
        ordinal=s['lane_record_ordinal'] if central else s['ordinal'];lane=s['lane'] if central else None
        require(type(auth['ordinal']) is int and auth['ordinal']==ordinal and
            (not central or type(auth['lane']) is int and auth['lane']==lane),'selected exact source ordinal/lane differs')
        key=(lane,ordinal);require(key not in locators,'duplicate selected source locator');locators.add(key)
        if source['kind']=='new-frontier-v3':
            require(auth.get('details_sha256')==receipt['details_sha256'],'new authority details identity differs')
        wanted[key]=candidate
    specifications=[]
    for ref in source['details']:
        lane=ref['lane']
        if central:
            artifact=receipt['lane_artifacts'][str(lane)]
            require(Path(ref['path']).name==artifact['path'] and ref['sha256']==artifact['sha256'] and
                type(artifact['records']) is int and artifact['records']>0,'selected lane artifact differs')
            count=artifact['records']
        else:
            require(ref['sha256']==receipt['details_sha256'],'selected frontier details artifact differs')
            count=len(receipt['observations'])
        subset={ordinal:c for (ln,ordinal),c in wanted.items() if ln==lane}
        require(subset and all(0<n<=count for n in subset),'empty or out-of-bounds selected detail source')
        specifications.append((ref,count,subset))
    require(sum(len(s[2]) for s in specifications)==len(candidates),'selected source lane coverage')
    return specifications


def read_selected_rows(path,expected_records,wanted,check):
    """Skip bounded unselected lines; parse only exact requested ordinals."""
    require(type(expected_records) is int and expected_records>0 and type(wanted) is dict and wanted and
        all(type(n) is int and 0<n<=expected_records for n in wanted),'finite selected detail geometry')
    count=0;characters=0
    with gzip.open(path,'rb') as stream:
        while True:
            line=stream.readline(MAX_ROW+1)
            if not line:break
            count+=1;characters+=len(line)
            require(count<=expected_records and len(line)<=MAX_ROW and line.endswith(b'\n') and characters<=MAX_DETAILS,
                'selected source decompression/line/count bound')
            check()
            if count in wanted:
                require(type(wanted[count]['authority']['ordinal']) is int and wanted[count]['authority']['ordinal']==count,
                    'selected reader ordinal contradicts source locator')
                row=json.loads(line);validate_selected_row(row,wanted[count]);yield wanted[count],row
    require(count==expected_records,'selected source record extent differs')


def _load(ref,inputs,*,private=True):
    path=_ref(ref,private=private)
    require(path.stat().st_size<=128*1024**2,'bounded JSON metadata input')
    base.observe(path,ref['sha256'],inputs)
    return base.load_json(path)


def review_gate(args,inputs):
    review=_load(dict(path=str(args.review),sha256=args.review_sha256),inputs)
    require(type(review) is dict and set(review)=={'schema_version','kind','reviewer','root_authorized',
        'independent_source_schema_review_pass','artifact_input_review_pass','request_sha256','context_sha256',
        'source_sha256','producer_sha256','allow_original_objects_read','allow_source_hashing',
        'allow_reference_image_read','allow_native_tools','allow_code_emission'} and
        type(review['schema_version']) is int and review['schema_version']==1 and
        review['kind']=='comdat-any-frontier-observer-review-v1' and type(review['reviewer']) is str and review['reviewer'] and
        all(review[k] is True for k in ('root_authorized','independent_source_schema_review_pass','artifact_input_review_pass',
            'allow_original_objects_read','allow_source_hashing')) and
        all(review[k] is False for k in ('allow_reference_image_read','allow_native_tools','allow_code_emission')) and
        review['request_sha256']==args.request_sha256 and review['context_sha256']==args.context_sha256 and
        set(review['source_sha256'])==set(OWNED) and exact(review['producer_sha256'],PINS),
        'exact delegated source/input observation review required')
    for name,h in {**review['source_sha256'],**PINS}.items():
        require(selector.sha(h),'reviewed source digest required');base.observe(ROOT/name,h,inputs)
    for module in (base,selector,selector.producer,composer,composer.policy,base.ordinary,base.coff,
                   base.collector,base.inventory,base.pool,native_inventory):
        require(Path(module.__file__).resolve()==ROOT/'tools/rebuild'/Path(module.__file__).name,'swapped observer producer')
    return review


def run(args):
    start=time.monotonic();inputs={};review=review_gate(args,inputs)
    request=_load(dict(path=str(args.request),sha256=args.request_sha256),inputs)
    context=_load(dict(path=str(args.context),sha256=args.context_sha256),inputs)
    require(context.get('request_sha256')==args.request_sha256,'operation request/context hash differs')
    artifacts={n:_load(ref,inputs,private=n!='recipes') for n,ref in context['artifacts'].items()}
    sources=validate_request_context(request,context,artifacts)
    for ref in context['acceptances'].values():base.observe(_ref(ref),ref['sha256'],inputs)
    manifest,retained,selection=[artifacts[n] for n in ('manifest','retained','selection')]
    recipes=_ref(context['artifacts']['recipes'],private=False)
    require(base.reconcile_recipes(manifest,recipes)['verified'],'original recipe manifest differs')
    providers={r['original_address']:selector.root_identity(r) for r in request['roots']}
    base.collector.validate_request(dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=request['roots']),
        selection['selections'],manifest,retained,providers)
    units={u['recipe_id']:u for u in manifest['units']};proofs={p['recipe_id']:p for p in retained['units']}
    require(len(units)==len(manifest['units']) and len(proofs)==len(retained['units']),'unique original proof units required')
    for name,h in retained['inputs']['tools_sha256'].items():
        path=(ROOT/name).resolve();require(path.is_relative_to(ROOT/'tools'),'foreign retained proof dependency');base.observe(path,h,inputs)
    source_specs=[]
    for key,source in sources.items():
        receipt=_load(source['receipt'],inputs);requests=_load(source['request'],inputs)
        candidates=[c for c in request['candidates'] if tuple(c['authority'][k] for k in
            ('kind','receipt_sha256','request_sha256'))==key]
        for ref,count,wanted in validate_source(source,receipt,requests,candidates):
            path=_ref({k:ref[k] for k in ('path','sha256')})
            require(path.stat().st_size<=128*1024**2,'bounded compressed detail input')
            base.observe(path,ref['sha256'],inputs)
            source_specs.append((path,count,wanted))
    out=Path(args.out).resolve();private=(ROOT/'build/rebuild').resolve()
    require(out.is_relative_to(private) and out!=private and not out.exists() and
        not any(p.is_relative_to(out) for p in inputs),'new exclusive private observer output required')
    # Resolve every native/source path before publication, including unselected
    # units, so an output directory can never swallow an original input tree.
    native_root=_ref(context['artifacts']['manifest']).parent/manifest.get('object_root_relative','.')
    for u in manifest['units']:
        obj=(native_root/u['object']).resolve();src=(ROOT/u['source']).resolve()
        require(obj.is_relative_to(private) and src.is_relative_to(ROOT) and
            not obj.is_relative_to(out) and not src.is_relative_to(out),'native/source/output path collision')
    base.stable(inputs);out.mkdir(parents=True,exist_ok=False);base.budget(start,out)
    journal=(out/'journal.jsonl').open('x',encoding='utf-8');observed=[];complete=0;unsupported=0
    def note(state,**value):
        journal.write(json.dumps(dict(state=state,elapsed_seconds=round(time.monotonic()-start,3),**value))+'\n')
        journal.flush();os.fsync(journal.fileno())
    try:
        note('started',roots=len(request['roots']),source_files=len(source_specs))
        for name in (*OWNED,*PINS):
            p=ROOT/name;target=out/'source-snapshots'/name;target.parent.mkdir(parents=True,exist_ok=True)
            base.pool.fsynced(target,p.read_bytes())
            base.observe(target,inputs[p.resolve()],inputs)
            base.budget(start,out)
        details=out/'observations.jsonl.gz'
        with details.open('xb') as target:
            with gzip.GzipFile(fileobj=target,mode='wb',mtime=0) as writer:
                for path,count,wanted in source_specs:
                    for candidate,row in read_selected_rows(path,count,wanted,lambda:base.budget(start,out)):
                        r=candidate['root'];a=r['original_address'];u=units[r['recipe_id']];proof=proofs[r['recipe_id']]
                        require(a not in observed,'duplicate observed root');contract,cert=validate_selected_row(row,candidate)
                        require(exact(contract['unit_verified_functions'],proof['verified_functions']) and
                            contract['provenance'].get('recipe_unit_sha256')==proof['recipe_unit_sha256'],
                            'original contract/retained proof unit differs')
                        for name,h in contract['provenance']['dependency_tools_sha256'].items():
                            dep=(ROOT/name).resolve();require(dep.is_relative_to(ROOT/'tools'),'foreign original observer dependency');base.observe(dep,h,inputs)
                        src=(ROOT/u['source']).resolve();obj=(native_root/u['object']).resolve()
                        require(obj.stat().st_size<=16*1024**2,'original native object input bound')
                        base.observe(src,r['source_sha256'],inputs);base.observe(obj,r['object_sha256'],inputs)
                        evidence=observe_member(obj.read_bytes(),row,candidate)
                        raw=selector.canonical(evidence);require(len(raw)<=MAX_ROW,'witness evidence row bound')
                        writer.write(raw+b'\n');observed.append(a)
                        eligible=evidence['composed'] is not None and evidence['composed']['composed_omission_complete'] is True
                        complete+=eligible;unsupported+=not eligible
                        note('observed_original_negative',original_address=a,native_state=evidence['unsupported_summary']['state'])
                        base.budget(start,out)
            target.flush();os.fsync(target.fileno())
        require(set(observed)=={r['original_address'] for r in request['roots']} and len(observed)==len(request['roots']),
            'complete finite original negative observation required')
        details_hash=base.file_hash(details);base.observe(details,details_hash,inputs)
        base.stable(inputs);usage=base.budget(start,out)
        result=dict(schema_version=1,policy_id=POLICY,status='metadata-only',epoch=context['epoch'],
            request_sha256=args.request_sha256,context_sha256=args.context_sha256,review_sha256=args.review_sha256,
            roots=len(observed),observed_addresses=sorted(observed),composed_complete=complete,unsupported=unsupported,
            emitted=0,blocked=unsupported,details_sha256=details_hash,details_bytes=details.stat().st_size,
            inputs={str(p):h for p,h in inputs.items()},source_snapshots_sha256={name:base.file_hash(out/'source-snapshots'/name) for name in (*OWNED,*PINS)},
            input_stability=True,optional_function_index_present=False,original_objects_read=True,source_contents_hashed=True,
            source_bodies_parsed=False,owner_stream_traversals=0,binding_stream_traversals=0,
            prepared_epoch_role='historical-V8-planning-collision-only',latest_prepared_epoch_claimed=False,
            future_projection_requires_fresh_operand_highlow_and_plain_match=True,resource_observations=usage,**FALSE)
        base.finalize_success(out,result,inputs,start,journal,note)
        return result
    except BaseException as error:
        try:
            if not journal.closed:note('failed',error_type=type(error).__name__)
        except BaseException:pass
        # The frozen publisher removes only its own successful-name link on a
        # failed postgate. Partial evidence has no terminal success receipt.
        try:base.save_json(out/'abort.json',dict(status='aborted-no-retry',error_type=type(error).__name__,
            observed_addresses=observed,successful_observation=False,**FALSE))
        except BaseException:pass
        raise
    finally:
        if not journal.closed:journal.close()


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('request','context','review','out'):parser.add_argument('--'+name,type=Path,required=True)
    for name in ('request','context','review'):parser.add_argument('--'+name+'-sha256',required=True)
    args=parser.parse_args(argv)
    try:result=run(args)
    except (ValueError,OSError,KeyError,TypeError) as error:parser.exit(2,'COMDAT witness observation rejected: '+str(error)+'\n')
    print(json.dumps(dict(roots=result['roots'],composed_complete=result['composed_complete'],unsupported=result['unsupported'])))
    return 0


if __name__=='__main__':raise SystemExit(main())
