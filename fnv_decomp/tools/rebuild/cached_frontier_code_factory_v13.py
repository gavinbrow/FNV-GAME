"""Version-local V13 singleton factory; immutable consumers and gates unchanged."""
from __future__ import annotations
from collections import Counter, defaultdict
import argparse,copy,gzip,hashlib,json,os,re,struct,time
from pathlib import Path
import cached_frontier_code_factory as previous
import cached_root_observe_v13 as native
import cached_code_frontier_inventory_v13 as metadata
frozen=previous.frozen
prior=previous.prior
audit=previous.audit
base=previous.base
ROOT=previous.ROOT
require=previous.require
digest=previous.digest
exact=native.typed_equal
sha=previous.sha
LIMITS=previous.LIMITS
FALSE=previous.FALSE
POLICY='cached-native-positive-singleton-CODE-factory-v13'
OWNED=('tools/rebuild/cached_frontier_code_factory_v13.py','tests/rebuild/test_cached_frontier_code_factory_v13.py','docs/rebuild/CACHED-FRONTIER-CODE-FACTORY-V13.md')
PINS={**previous.PINS,'tools/rebuild/cached_frontier_code_factory.py':'3585144819a57b61bf8ffb71c3ddfc0ce85297ae59e3808bb60d79782007673b',
 'tools/rebuild/cached_root_observe_v13.py':'05489b372585fac5f615548b53232bf30b7e28e5494ed914cc4e9972eb69deb4',
 'tools/rebuild/cached_code_frontier_inventory_v13.py':'cc9c228fd93fcd9147c1e61a66e7917c05d21cdee33e67dfed6cf22fb4de41d0',
 'tools/rebuild/prepared_code56_successor.py':'fb8863d67e64cd3dce24b61b3c1f42d88248e72eb81110be6ec54abef1f07559'}
NATIVE_RECEIPT='846087b14800e313181064f5a897c110f8d07cc261c89e8b2730a75ad04efc08'
NATIVE_DETAILS='8083f44b2554509883d4c78089099756e552f8d53a2ae378bab7f5b51252e75c'
QUARANTINES=metadata.QUARANTINE_ADDRESSES
KNOWN={**previous.KNOWN,'native_receipt':NATIVE_RECEIPT,'native_details':NATIVE_DETAILS,
 'native_main_review':'d1d8dda9053c4bf30e6d054c55abff5c53ec9d9d95936e4e9ea075850898d920',
 'native_authority_review':'d2bcc2c6e57cc69dd54023ea63ad44d548bdde1fd692d98efa7b808cb416425b',
 'positive_request':'04d9006356d01d32cf52d377293dfe8f6b501bffb8e5146a0eddc8880910585c',
 **{name:native.ARTIFACT_PINS[key] for name,key in [('qualification_request','qualified_request'),('qualification_receipt','qualified_receipt'),
 ('qualification_main_review','qualification_main_review'),('qualification_authority_review','qualification_authority_review'),
 ('current_groups','current_groups'),('current_review','current_review')]},
 'qualified_prepared_epoch':native.ARTIFACT_PINS['prepared_epoch'],
 'prepared_epoch':native.ARTIFACT_PINS['latest_prepared_epoch'],'prepared_review':native.ARTIFACT_PINS['latest_prepared_review']}
OUTPUT='build/rebuild/cached-frontier-code-v13-v1'
IMAGE_CHECK_PATH=previous.IMAGE_CHECK_PATH


def prepared_nonadmission(prepared):
    require(prepared['application_selection_inferred_from_counts'] is False and
        all(prepared[k] is False for k in ('provider_selected','runtime_eligible')),'collision evidence promoted')
    if 'application_manifest_adopted' in prepared:
        require(prepared['application_manifest_adopted'] is False,'explicit application adoption promoted')
    else:
        require(type(prepared.get('schema_version')) is int and prepared['schema_version']==8 and
            prepared.get('policy_id')=='prepared-UUID2768-successor-v1' and prepared.get('application_selected_code_count','ABSENT') is None and
            all(prepared.get(k) is False for k in metadata.FALSE),'only accepted UUID successor may preserve missing app flag')


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
        expected_census=(72,44,116),expected_current_codes=593,expected_prepared=(14529,14535),receipt_sha256=NATIVE_RECEIPT,on_selected=None):
    """Stream all observations; select every positive SINGLE event only."""
    expected_roots,expected_recipes,expected_records=expected_census
    require(sha(receipt_sha256) and receipt['policy_id']==native.POLICY and receipt['status']=='metadata-only' and
        receipt['input_stability'] is True and receipt['optional_function_index_present'] is False and
        receipt['qualified_contracts_preserved'] is True and type(receipt['historical_roots_reobserved']) is int and receipt['historical_roots_reobserved']==0 and
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
            sha(root['object_sha256']) and sha(root['source_sha256']),'typed exact native physical root')
        by_recipe[root['recipe_index']].append(root)
    require(len(by_recipe)==expected_recipes,'whole qualified recipe request')
    require(prepared['kind']=='prepared-CODE-collision-exclusions' and all(type(prepared[k]) is int for k in ('ordinary_prepared_count','collision_exclusion_count')) and
        (prepared['ordinary_prepared_count'],prepared['collision_exclusion_count'])==expected_prepared and
        len(prepared['exclusion_names'])==len(set(prepared['exclusion_names']))==expected_prepared[1] and
        prepared['application_selection_inferred_from_counts'] is False,'exact prepared collision epoch')
    prepared_nonadmission(prepared)
    exports=set(prepared['exclusion_names'])
    require(current_groups['kind']=='actual-unresolved-LNK-target-groups' and current_groups['executable_execution'] is False and current_groups['runtime_eligible'] is False,
        'actual nonexecuted current LINK groups')
    current_rows=[g for g in current_groups['groups'] if g['classification']=='CODE'];current={g['symbol']:g for g in current_rows}
    require(len(current)==len(current_rows)==current_groups['classifications']['CODE']==expected_current_codes,'whole unique current CODE namespace')
    singles={};unions=set();ledger=[];selected=[];seen_records=0;counts=Counter();last_recipe=-1
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
                if on_selected is not None:on_selected(record,selection)
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
        'whole72/44/116 outcome partition differs')
    selected.sort(key=lambda s:s['root']['original_address'])
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


def write_context(stream,record,selection):
    """Same frozen frame format, preserving the new native row unmodified."""
    validate_selected(record,selection)
    raw=json.dumps(dict(row=record,selection=selection),sort_keys=True,separators=(',',':')).encode()
    require(len(raw)<=frozen.MAX_CONTEXT,'selected native context raw bound')
    packed=gzip.compress(raw,mtime=0);require(len(packed)<=frozen.MAX_CONTEXT,'selected native context compressed bound')
    offset=stream.tell();stream.write(struct.pack('<Q',len(packed)));stream.write(packed)
    return dict(original_address=selection['root']['original_address'],offset=offset,bytes=len(packed),frame_sha256=base.coff.digest(packed),
        context_sha256=base.coff.digest(raw),record_sha256=digest(record),authority=selection['authority'])


def verify_member(raw,record,selection,providers,exports,original_path,stage_path,pe,recipe):
    """Fresh frozen graph/core replay, with unchanged original/staged MATCH."""
    validate_selected(record,selection);root=selection['root'];contract=record['contract'];certificate=record['certificate']
    if contract['fields']:
        assessment=frozen.fields.core.assess_member(raw,contract,certificate,[root],providers,existing_exports=exports)
        if assessment['eligible'] is not True:
            require(assessment['blockers'],'unsupported field policy has no blocker')
            return None,None,assessment
    else:assessment=None
    # Frozen helper independently replays its appropriate zero or field core.
    output,projection=frozen.verify_candidate(raw,record,root,providers,exports,original_path,stage_path,pe,recipe)
    for key,name in [('before_comparison',root['symbol']),('after_comparison',projection['exports'][0])]:
        reports=projection[key]
        require(type(reports) is list and len(reports)==1,'one whole original/staged comparison')
        report=reports[0]
        require(report['verdict']=='match' and report['address']==root['original_address'] and report['symbol']==name and
            type(report['size']) is type(report['compiled_extent']) is int and report['size']==report['compiled_extent']==root['size'] and
            not report['errors'] and not report.get('byte_differences',[]) and len(report['relocations'])==len(contract['fields']) and
            all(r['match'] is True and r['expected']==r['observed'] for r in report['relocations']),
            'full original/staged body and relocation MATCH required')
    require(len(projection['fields'])==len(contract['fields']),'projected original field census differs')
    if assessment is not None:require(exact(projection['fields'],assessment['fields']) and projection['exports']==assessment['exports'],
        'fresh assessment and independent projection differ')
    if assessment is None:
        assessment=dict(eligible=True,blockers=[],strict_zero_consumer_replayed=True,serialization_performed=False,
            requested_roots=[root],contract_identity_sha256=digest(contract),certificate_sha256=digest(certificate))
    projection.update(authority=selection['authority'],central_record_sha256=digest(record),
        native_observation_record_sha256=digest(record),qualified_metadata_row_sha256=record['qualified_metadata_row_sha256'])
    return output,projection,assessment


def field_proof_record(member,record,selection,projection,output):
    """Reuse full original-field copying; unit IAT context never adds rows."""
    validate_selected(record,selection)
    return prior.field_proof_record(member,record,selection,projection,output)




def ref_path(ref,*,private=True):
    require(type(ref) is dict and set(ref)=={'path','sha256'} and type(ref['path']) is str and sha(ref['sha256']),'exact artifact descriptor')
    path=(ROOT/ref['path']).resolve();boundary=(ROOT/'build/rebuild').resolve() if private else ROOT.resolve()
    require(path.is_relative_to(boundary) and path!=boundary,'foreign artifact path');return path


def load_ref(ref,inputs,*,private=True):
    path=ref_path(ref,private=private);value=native.read_bound_json(path,ref['sha256'])
    require(path not in inputs or inputs[path]==ref['sha256'],'conflicting same-byte metadata pin');inputs[path]=ref['sha256'];return value


def validate_operation(operation):
    require(all(sha(h) for h in KNOWN.values()),'accepted native outcome and wholepositive request pins remain pending')
    require(type(operation) is dict and set(operation)=={'schema_version','kind','epoch','roots','artifacts','output_relative','resource_limits'} and
        type(operation['schema_version']) is int and operation['schema_version']==1 and operation['kind']=='cached-native-positive-CODE-production-operation' and
        type(operation['epoch']) is str and 0<len(operation['epoch'])<=100 and operation['epoch'].isascii() and
        exact(operation['resource_limits'],LIMITS) and operation['output_relative']==OUTPUT and set(operation['artifacts'])==set(KNOWN) and
        type(operation['roots']) is list and operation['roots'],'closed whole-positive CODE operation')
    for name,ref in operation['artifacts'].items():
        ref_path(ref,private=name not in ('recipes','image_check'))
        if KNOWN[name] is not None:require(ref['sha256']==KNOWN[name],'unaccepted source artifact: '+name)
        if name=='image_check':require((ROOT/ref['path']).resolve()==(ROOT/IMAGE_CHECK_PATH).resolve(),'retained image-check role requires its exact original metadata path')
    require(len({r['original_address'] for r in operation['roots']})==len(operation['roots']) and
        all(set(r)==native.ROOT_KEYS and all(type(r[k]) is int for k in ('recipe_index','symbol_index','section','value','size')) for r in operation['roots']),
        'exact unique physical whole-positive request')


def output_path(operation,path):
    target=Path(path).resolve();require(target==(ROOT/operation['output_relative']).resolve() and target.is_relative_to(ROOT/'build/rebuild') and
        target!=ROOT/'build/rebuild' and not target.exists(),'new exact private CODE output before original input access')
    return target


def prepare_operation(operation,inputs,*,start=None):
    """Saved metadata admission only; no original/source/reference byte reads."""
    start=time.monotonic() if start is None else start;validate_operation(operation);loaded={}
    for name,ref in operation['artifacts'].items():
        if name=='native_details':continue
        loaded[name]=load_ref(ref,inputs,private=name not in ('recipes','image_check'));metadata.input_budget(start)
    r=loaded['native_receipt'];q=loaded['qualification_request'];m=loaded['qualification_receipt']
    require(r['source_sha256']==PINS['tools/rebuild/cached_root_observe_v13.py'] and r['details_sha256']==NATIVE_DETAILS and
        r['inputs']['qualified_request']['sha256']==operation['artifacts']['qualification_request']['sha256'] and
        r['inputs']['qualified_receipt']['sha256']==operation['artifacts']['qualification_receipt']['sha256'] and
        all(r['inputs'][native_name]['sha256']==operation['artifacts'][name]['sha256'] for name,native_name in
            [('manifest','manifest'),('retained','retained'),('selection','selection'),('recipes','recipes'),('planned_map','planned_map'),('imports','imports'),('current_groups','current_groups'),('current_review','current_review')]) and
        m['output_sha256']['metadata-request.json']==operation['artifacts']['qualification_request']['sha256'] and
        m['output_sha256']['prepared-epoch.json']==operation['artifacts']['qualified_prepared_epoch']['sha256'] and
        r['inputs']['latest_prepared_epoch']['sha256']==operation['artifacts']['prepared_epoch']['sha256'],'accepted native/qualification/current source lineage')
    manifest=loaded['manifest'];retained=loaded['retained'];units={u['recipe_id']:u for u in manifest['units']};proofs={p['recipe_id']:p for p in retained['units']}
    require(len(units)==len(manifest['units'])==len(proofs)==len(retained['units'])==2988 and len(loaded['selection']['selections'])==68657,'complete selected metadata universe')
    require(base.reconcile_recipes(manifest,ref_path(operation['artifacts']['recipes'],private=False))['verified'],'original recipe metadata differs')
    providers=frozen.fields.validate_provider_map(loaded['planned_map'],loaded['selection']['selections'],units,proofs,loaded['owners']);metadata.input_budget(start)
    require(len(providers)==68657 and operation['artifacts']['image_check']['sha256']==retained['inputs']['image_check_sha256'],'complete namespace/image-check metadata')
    epoch=loaded['prepared_epoch'];require(epoch['ordinary_prepared_count']==14529 and epoch['collision_exclusion_count']==14535 and
        len(epoch['records'])==len(epoch['exclusion_names'])==len(set(epoch['exclusion_names']))==14535 and
        {e['canonical'] for e in epoch['records']}==set(epoch['exclusion_names']) and
        all(base.pool.canonical(e['namespace_identity'])==e['canonical'] for e in epoch['records']),'latest collision epoch physical identity')
    prepared_nonadmission(epoch)
    namespace={a:{k:p[k] for k in ('recipe_id','object_sha256','symbol_index')} for a,p in loaded['planned_map']['providers'].items()}
    epoch_join=native.validate_epoch_successor(loaded['qualified_prepared_epoch'],epoch,q['roots'],namespace)
    exports=set(epoch['exclusion_names'])
    require(all(base.pool.canonical(providers[a]) not in exports for a in QUARANTINES),'prior quarantines cannot become prepared')
    expected=loaded['positive_request']['roots'];require(exact(operation['roots'],expected),'whole accepted positive request required')
    base.collector.validate_request(dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=expected),loaded['selection']['selections'],manifest,retained,providers)
    for rel,h in retained['inputs']['tools_sha256'].items():
        path=(ROOT/rel).resolve();require(path.is_relative_to(ROOT/'tools'),'foreign retained validator');base.observe(path,h,inputs)
    for root in expected:require(base.pool.canonical(providers[root['original_address']]) not in exports,'requested source namespace already prepared')
    metadata.input_budget(start)
    return dict(operation=operation,artifacts=loaded,receipt=r,qualification_request=q,current_groups=loaded['current_groups'],prepared=epoch,
        expected_request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=expected),units=units,proofs=proofs,providers=providers,exports=exports,
        current_successor_join=epoch_join,native_details=ref_path(operation['artifacts']['native_details']))


def native_records(path,receipt,start):
    with Path(path).open('rb') as source:
        compressed=native.DigestingSource(source)
        with gzip.GzipFile(fileobj=compressed,mode='rb') as stream:
            count=0
            while True:
                raw=stream.readline(LIMITS['output_bytes']+1)
                if not raw:break
                count+=1;require(count<=116 and len(raw)<=LIMITS['output_bytes'] and raw.endswith(b'\n'),'bounded complete native record')
                record=json.loads(raw);del raw;metadata.input_budget(start)
                yield record;del record;metadata.input_budget(start)
            require(count==116,'whole native record count')
        compressed.finish(receipt['details_sha256'],receipt['details_bytes'])


def spool_contexts(out,prepared,inputs,start):
    path=Path(out)/'contexts.bin';indices={}
    with path.open('xb') as stream:
        def selected(record,selection):
            a=selection['root']['original_address'];require(a not in indices,'duplicate selected context');indices[a]=write_context(stream,record,selection);base.budget(start,out)
        request,selections,ledger=select_candidates(prepared['receipt'],native_records(prepared['native_details'],prepared['receipt'],start),
            prepared['qualification_request'],prepared['current_groups'],prepared['prepared'],on_selected=selected)
        require(exact(request,prepared['expected_request']) and set(indices)=={r['original_address'] for r in request['roots']},'complete selected original context stream')
        stream.flush();os.fsync(stream.fileno())
    inputs[prepared['native_details'].resolve()]=prepared['receipt']['details_sha256']
    base.save_json(Path(out)/'contexts-index.json',indices)
    hashes=frozen.protect_context_artifacts(path,Path(out)/'contexts-index.json',indices,inputs)
    return path,indices,selections,ledger,hashes


def review_gate(args,inputs):
    review=load_ref(dict(path=str(args.review),sha256=args.review_sha256),inputs)
    require(type(review) is dict and set(review)=={'schema_version','kind','reviewer','approved','root_authorized','independent_source_schema_review_pass',
        'artifact_input_review_pass','operation_sha256','source_sha256','producer_sha256','allow_original_objects_read','allow_source_hashing',
        'allow_reference_image_read','allow_code_emission','allow_native_tools','allow_executable_link','allow_game_execution'} and
        type(review['schema_version']) is int and review['schema_version']==1 and review['kind']=='cached-frontier-CODE-factory-v13-review-v1' and
        type(review['reviewer']) is str and review['reviewer'] and review['reviewer']!='/root/code_lane_02' and
        all(review[k] is True for k in ('approved','root_authorized','independent_source_schema_review_pass','artifact_input_review_pass',
            'allow_original_objects_read','allow_source_hashing','allow_reference_image_read','allow_code_emission')) and
        all(review[k] is False for k in ('allow_native_tools','allow_executable_link','allow_game_execution')) and
        review['operation_sha256']==args.operation_sha256 and set(review['source_sha256'])==set(OWNED) and review['producer_sha256']==PINS,
        'independent exact whole-positive production review')
    for rel,h in {**review['source_sha256'],**PINS}.items():require(sha(h),'source hash schema');base.observe(ROOT/rel,h,inputs)
    for module in (native,frozen,prior,metadata,audit,base,frozen.fields,frozen.fields.core,
            base.bulk,base.coff,base.pool,base.inventory,base.collector,previous,native.previous):
        require(Path(module.__file__).resolve()==ROOT/'tools/rebuild'/Path(module.__file__).name,'foreign producer module')
    return review


def current_ledger(groups,qualification_request,native_ledger,providers,exports):
    singles={entry['roots'][0]['original_address']:entry for entry in native_ledger if entry['event']=='SINGLE_ROOT_OBSERVATION'}
    known={base.pool.canonical({k:r[k] for k in ('recipe_id','object_sha256','symbol_index')}):r for r in qualification_request['roots']}
    quarantined={base.pool.canonical(providers[a]) for a in QUARANTINES};result=[]
    for ordinal,group in enumerate(groups['groups'],1):
        if group['classification']!='CODE':continue
        name=group['symbol'];entry=dict(symbol=name,group_ordinal=ordinal,group_sha256=digest(group),original_bases=group['original_bases'])
        if name in exports:state='PREPARED_SKIP'
        elif name in quarantined:state='PRESERVED_REFERENCE_GROUP_QUARANTINE'
        elif name in known:
            root=known[name];source=singles[root['original_address']];entry.update(root=root,native_record_sha256=source['record_sha256'],original_blocker_codes=source['blocker_codes'])
            state='REQUESTED_FRESH_PROJECTION' if source['closure_observed'] else 'NATIVE_ORIGINAL_NEGATIVE_PRESERVED'
        else:state='OUTSIDE_NEW_NATIVE_OBSERVATION_UNIVERSE'
        entry['production_status']=state;result.append(entry)
    require(len(result)==593 and len({r['symbol'] for r in result})==593,'whole current CODE ledger')
    return result



write_coverage=previous.write_coverage
publish_result=previous.publish_result
checked_reference=previous.checked_reference


def run(args):
    start=time.monotonic();inputs={};review=review_gate(args,inputs)
    operation=load_ref(dict(path=str(args.operation),sha256=args.operation_sha256),inputs);validate_operation(operation)
    out=output_path(operation,args.out)  # Must precede any original/source/reference input access.
    prepared=prepare_operation(operation,inputs,start=start)
    native_root=ref_path(operation['artifacts']['manifest']).parent/prepared['artifacts']['manifest'].get('object_root_relative','.')
    for unit in prepared['artifacts']['manifest']['units']:
        require(not (native_root/unit['object']).resolve().is_relative_to(out) and not (ROOT/unit['source']).resolve().is_relative_to(out),'output collides with named original input')
    require(not any(p.is_relative_to(out) for p in inputs),'output contains protected metadata input')
    base.stable(inputs);out.mkdir(parents=True,exist_ok=False);base.budget(start,out)
    journal=(out/'progress.jsonl').open('x',encoding='utf-8');members=[];receipts=[];blocked=[];assessments=[];emitted=[];snapshot=None;proof_file=None;proof_writer=None
    def note(state,**facts):
        journal.write(json.dumps(dict(state=state,elapsed_seconds=round(time.monotonic()-start,3),**facts))+'\n');journal.flush();os.fsync(journal.fileno())
    def protect(path):
        h=base.file_hash(path);base.observe(path,h,inputs);return h
    try:
        note('started',whole_native_roots=72,whole_native_records=116,whole_current_CODE=593)
        for rel in (*OWNED,*PINS):
            target=out/'source-snapshots'/rel;target.parent.mkdir(parents=True,exist_ok=True);base.pool.fsynced(target,(ROOT/rel).read_bytes());base.observe(target,inputs[(ROOT/rel).resolve()],inputs)
        spool,index,selections,native_ledger,context_hashes=spool_contexts(out,prepared,inputs,start)
        require(exact([s['root'] for s in selections],operation['roots']),'every original positive singleton is requested')
        providers=prepared['providers'];exports=prepared['exports'];qualification_request=prepared['qualification_request'];epoch_join=prepared['current_successor_join']
        code_ledger=current_ledger(prepared['current_groups'],qualification_request,native_ledger,providers,exports)
        current_names={r['symbol'] for r in code_ledger};wanted={s['root']['original_address']:s for s in selections};originals={}
        selected_units={};selected_proofs={}
        for selection in selections:
            root=selection['root'];rid=root['recipe_id'];unit=prepared['units'][rid]
            if rid in originals:continue
            source=(ROOT/unit['source']).resolve();obj=(native_root/unit['object']).resolve()
            require(source.is_relative_to(ROOT) and obj.is_relative_to(ROOT/'build/rebuild') and not source.is_relative_to(out) and not obj.is_relative_to(out) and
                obj.stat().st_size<=16*1024**2,'bounded exact original source/object path')
            base.observe(source,root['source_sha256'],inputs);base.observe(obj,root['object_sha256'],inputs)
            originals[rid]=obj;selected_units[rid]=unit;selected_proofs[rid]=prepared['proofs'][rid]
        reference=base.observe(args.reference,base.pool.PINS['reference'],inputs)
        del prepared
        base.stable(inputs);base.budget(start,out)
        pe=checked_reference(reference);snapshot=audit.SnapshotPe(reference,pe)
        highlow={snapshot.base+rva for rva in snapshot.relocations()};require(len(highlow)==351931,'fresh original HIGHLOW identity differs')
        proof_file=(out/'field-proofs.jsonl.gz').open('xb');proof_writer=gzip.GzipFile(fileobj=metadata.BoundedSink(proof_file,start,out),mode='wb',mtime=0)
        facts={};all_fields=0;last_recipe=None;raw=None
        with spool.open('rb') as contexts:
            for selection in sorted(selections,key=lambda s:(s['root']['recipe_index'],s['authority']['ordinal'])):
                root=selection['root'];address=root['original_address'];rid=root['recipe_id'];record=frozen.read_context(contexts,index[address],selection)
                validate_selected(record,selection);contract=record['contract'];proof=selected_proofs[rid]
                require(exact(contract['unit_verified_functions'],proof['verified_functions']) and
                    contract['provenance']['recipe_unit_sha256']==proof['recipe_unit_sha256'],'original full retained source proof differs')
                for site,fact in audit.audit_original_fields(snapshot,highlow,contract['fields']).items():
                    require(site not in facts or facts[site]==fact,'contradictory original operand field facts');facts[site]=fact
                all_fields+=len(contract['fields'])
                if last_recipe!=rid:
                    raw=None
                    with originals[rid].open('rb') as source:raw=source.read(16*1024**2+1)
                    require(len(raw)<=16*1024**2 and base.coff.digest(raw)==root['object_sha256'],'fresh original object bytes/hash differ');last_recipe=rid
                name='CACHED-CODE-%03d-%s.obj'%(len(members),address[2:]);stage=out/name
                output,projection,assessment=verify_member(raw,record,selection,providers,exports,originals[rid],stage,pe,selected_units[rid]['recipe'])
                assessments.append(dict(root=root,assessment=assessment))
                if output is None:
                    blocked.append(dict(root=root,blockers=assessment['blockers'],fresh_body_compared=False))
                    del record,contract,assessment
                    continue
                protect(stage);full=field_proof_record(name,record,selection,projection,output);proof_writer.write(native.canonical(full)+b'\n')
                members.append((name,output));receipts.append(dict(name=name,projection=projection));emitted.append(address)
                note('member_verified',original_address=address,fields=len(projection['fields']),object_sha256=projection['output_sha256']);base.budget(start,out)
                del record,contract,output,projection,assessment,full
        proof_writer.close();proof_writer=None;proof_file.flush();os.fsync(proof_file.fileno());proof_file.close();proof_file=None
        snapshot.close();snapshot=None;raw=None;archive_hash=None
        if members:
            blob=base.coff.archive(members);require(base.budget(start,out)['output_bytes']+len(blob)<=LIMITS['output_bytes'],'complete archive output cap')
            archive=out/'CACHED-code.lib';base.pool.fsynced(archive,blob);recovered=base.coff.read_archive(blob)
            require(recovered['members']==members and len(recovered['index'])==len(members),'archive member/index integrity')
            for name,body in recovered['members']:
                path=out/('recovered-'+name);base.pool.fsynced(path,body);base.bulk.strict_reparse(path,body);protect(path)
            archive_hash=protect(archive)
        require(set(emitted).isdisjoint(b['root']['original_address'] for b in blocked) and set(emitted)|{b['root']['original_address'] for b in blocked}==set(wanted),
            'every requested singleton needs an exact terminal outcome')
        quarantine={b['root']['original_address']:b['blockers'] for b in blocked}
        for entry in native_ledger:
            if entry['state']=='ALL_POSITIVE_SINGLETON_REQUESTED':
                address=entry['roots'][0]['original_address'];entry['production_status']='EMITTED' if address in emitted else 'QUARANTINED_UNSUPPORTED_POLICY'
                if address in quarantine:entry['production_blockers']=quarantine[address]
        for entry in code_ledger:
            if entry['production_status']=='REQUESTED_FRESH_PROJECTION':
                address=entry['root']['original_address'];entry['production_status']='EMITTED' if address in emitted else 'QUARANTINED_UNSUPPORTED_POLICY'
        coverage=write_coverage(out/'coverage.jsonl.gz',providers,exports,qualification_request,wanted,emitted,current_names)
        for name,value in [('members',receipts),('blocked',blocked),('assessments',assessments),('native-ledger',native_ledger),('current-frontier-ledger',code_ledger),
            ('original-field-audit',dict(highlow_sites=len(highlow),retained_fields=all_fields,unique_field_sites=len(facts),field_facts_sha256=digest(sorted(facts.items())),
                loaded_reference_sha256=base.coff.digest(pe.data),original_highlow_authority_authenticated=True))]:metadata.save_bounded_json(out/(name+'.json'),value,start,out)
        names=('members.json','blocked.json','assessments.json','native-ledger.json','current-frontier-ledger.json','original-field-audit.json','coverage.jsonl.gz','field-proofs.jsonl.gz')
        generated={name:protect(out/name) for name in names};base.stable(inputs);usage=base.budget(start,out)
        result=dict(schema_version=1,policy_id=POLICY,status='completed' if not blocked else 'completed-incomplete',epoch=operation['epoch'],operation_sha256=args.operation_sha256,
            review_sha256=args.review_sha256,native_receipt_sha256=NATIVE_RECEIPT,whole_native_roots=72,whole_native_records=116,whole_current_CODE=593,
            requested=len(wanted),emitted=len(emitted),blocked=len(blocked),emitted_addresses=emitted,archive_sha256=archive_hash,
            context_spool_sha256=context_hashes[0],context_index_sha256=context_hashes[1],derived_context_inputs_protected=2,
            fields=sum(len(m['projection']['fields']) for m in receipts),code_bytes=sum(m['projection']['requested_roots'][0]['size'] for m in receipts),
            full_field_proof_schema_version=1,full_field_proof_records=len(receipts),full_field_proof_rows=sum(len(m['projection']['fields']) for m in receipts),source_evidence_enriched=False,
            original_bare_certificates_unmodified=True,whole_positive_singletons_requested=True,union_providers_created=False,
            upstream_ordinary_prepared_count=14529,upstream_collision_exclusion_count=14535,preserved_prior_quarantine_addresses=sorted(QUARANTINES),
            historical_qualification_epoch_sha256=KNOWN['qualified_prepared_epoch'],upstream_current_epoch_sha256=KNOWN['prepared_epoch'],current_successor_join=epoch_join,
            coverage_counts=coverage,current_frontier_counts=dict(Counter(e['production_status'] for e in code_ledger)),inputs={str(p):h for p,h in inputs.items()},
            input_stability=True,optional_function_index_present=False,output_sha256=generated,resource_limits=LIMITS,resource_observations=usage,**FALSE)
        return publish_result(out,result,inputs,start,journal,note)
    except BaseException as error:
        if not journal.closed:note('failed',error_type=type(error).__name__,completed_members=len(emitted))
        base.save_json(out/'abort.json',dict(status='aborted-no-retry',error_type=type(error).__name__,completed_members=emitted,successful_projection=False,**FALSE));raise
    finally:
        if proof_writer is not None:proof_writer.close()
        if proof_file is not None:proof_file.close()
        if snapshot is not None:snapshot.close()
        if not journal.closed:journal.close()


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('operation','review','reference','out'):parser.add_argument('--'+name,type=Path,required=True)
    for name in ('operation','review'):parser.add_argument('--'+name+'-sha256',required=True)
    args=parser.parse_args(argv)
    try:result=run(args)
    except (ValueError,OSError,KeyError,TypeError) as error:parser.exit(2,'cached CODE factory rejected: '+str(error)+'\n')
    print(json.dumps(dict(requested=result['requested'],emitted=result['emitted'],blocked=result['blocked'])))
    return 0 if result['status']=='completed' else 3


if __name__=='__main__':raise SystemExit(main())
