"""V14 factory bounded observation and terminal-outcome primitives.

This module does not authorize or launch a factory operation. An operation must
bind the accepted V14 authorities and pass source/input/resource review first.
"""
from __future__ import annotations
import gzip
import hashlib
import json
from pathlib import Path

MAX_RECORDS = 89
MAX_DETAIL_BYTES = 128 * 1024 * 1024
MAX_RECORD_BYTES = 16 * 1024 * 1024


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError('non-finite JSON value: ' + value)


def read_observations(path, *, expected_sha256, expected_bytes, expected_records=MAX_RECORDS):
    """Return a fully authenticated bounded stream before any caller acts on it.

    The compressed body is read once into a bounded private buffer. Parsing and
    census must finish before records escape. This bounds compressed and expanded
    input separately and rejects malformed, partial, duplicate-key and extra rows.
    """
    if (not isinstance(expected_sha256, str) or len(expected_sha256) != 64 or
            any(c not in '0123456789abcdef' for c in expected_sha256)):
        raise ValueError('lowercase SHA-256 required')
    if type(expected_bytes) is not int or not 0 < expected_bytes <= MAX_DETAIL_BYTES:
        raise ValueError('bounded compressed size required')
    if type(expected_records) is not int or not 0 < expected_records <= MAX_RECORDS:
        raise ValueError('bounded exact record count required')
    with Path(path).open('rb') as stream:
        body = stream.read(expected_bytes + 1)
    if len(body) != expected_bytes or hashlib.sha256(body).hexdigest() != expected_sha256:
        raise ValueError('observation compressed identity differs')
    import io
    records = []
    expanded = 0
    with gzip.GzipFile(fileobj=io.BytesIO(body), mode='rb') as stream:
        while True:
            line = stream.readline(MAX_RECORD_BYTES + 1)
            if not line:
                break
            expanded += len(line)
            if (len(line) > MAX_RECORD_BYTES or expanded > MAX_DETAIL_BYTES or
                    not line.endswith(b'\n') or len(records) >= expected_records):
                raise ValueError('observation stream bounds or framing differ')
            value = json.loads(line, object_pairs_hook=_pairs, parse_constant=_invalid_constant)
            if type(value) is not dict:
                raise ValueError('observation row must be an object')
            records.append(value)
    if len(records) != expected_records:
        raise ValueError('incomplete observation stream')
    return records


def _typed_equal(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(_typed_equal(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(_typed_equal(a, b) for a, b in zip(left, right))
    return left == right


def reconcile_outcomes(selections, outcomes):
    """Require one explicit emitted or unsupported-policy result per selection."""
    if type(selections) is not list or type(outcomes) is not list or not selections:
        raise ValueError('nonempty finite selection and outcome lists required')
    wanted = {}
    for selection in selections:
        root = selection['root']
        address = root['original_address']
        if not isinstance(address, str) or address in wanted:
            raise ValueError('duplicate or invalid selected address')
        wanted[address] = root
    seen = {}
    for outcome in outcomes:
        if type(outcome) is not dict or set(outcome) != {'root', 'status', 'evidence'}:
            raise ValueError('exact terminal outcome required')
        root = outcome['root']
        address = root['original_address']
        if address not in wanted or address in seen or not _typed_equal(root, wanted[address]):
            raise ValueError('foreign, duplicate or altered root outcome')
        evidence = outcome['evidence']
        if type(evidence) is not dict:
            raise ValueError('terminal evidence required')
        if outcome['status'] == 'emitted':
            if (evidence.get('original_plain_match') is not True or
                    evidence.get('staged_plain_match') is not True or
                    evidence.get('strict_reparse') is not True or
                    evidence.get('complete_field_proof') is not True):
                raise ValueError('complete emitted proof required')
        elif outcome['status'] == 'quarantined-unsupported-policy':
            if (type(evidence.get('blockers')) is not list or not evidence['blockers'] or
                    evidence.get('integrity_failure') is not False):
                raise ValueError('explicit unsupported-policy blocker required')
        else:
            raise ValueError('unknown or incomplete outcome')
        seen[address] = outcome
    if set(seen) != set(wanted):
        raise ValueError('missing selected terminal outcome')
    return {'requested': len(wanted), 'emitted': sum(x['status'] == 'emitted' for x in outcomes),
            'quarantined': sum(x['status'] == 'quarantined-unsupported-policy' for x in outcomes),
            'status': 'completed-incomplete' if any(x['status'] != 'emitted' for x in outcomes) else 'completed'}

# The hashes identify the one accepted V14 observation, not a production grant.
ACCEPTED = {
    'receipt': ('build/rebuild/cached-root-observe-v14-output-v1/receipt.json', 'f1b4cd678c0b0f648085574933308cc5533545773af800ec79c03c1d4580dd01'),
    'details': ('build/rebuild/cached-root-observe-v14-output-v1/details.jsonl.gz', '534bff7f58d37c3feb06b4b05ba78b81fbf37aad4825598e86b0eec2aea62ee6'),
    'main_review': ('build/rebuild/cached-root-observe-v14-outcome-review-v1.json', '1647fea5c4b75d1f12740752dfdd4f7f5921de443f1d548d4e43b0b718ee428d'),
    'complement_review': ('build/rebuild/terra-v14-complement-review-v1/review.json', 'bd38122d730e6972d9695454768d7b714426060e52287b1e311e75d249172f5a'),
    'positive_request': ('build/rebuild/terra-v14-complement-review-v1/positive15-request-metadata.json', '41102183e7d118d7bf431e1b841008bbfdca669611a0f6ae64761a66551f5636'),
}


def validate_saved_reviews(receipt, main, complement, request):
    """Check the exact accepted observation links, without granting production."""
    receipt_hash = ACCEPTED['receipt'][1]
    details_hash = ACCEPTED['details'][1]
    if (receipt['policy_id'] != 'cached-context-root-observation-v14' or
            receipt['status'] != 'metadata-only' or receipt['details_sha256'] != details_hash or
            receipt['input_stability'] is not True or receipt['qualified_contracts_preserved'] is not True or
            not _typed_equal(receipt['summary'], dict(roots=55, recipes=34, records=89, singleton_closure=15,
                singleton_blocked=40, union_closure=8, union_blocked=26))):
        raise ValueError('accepted V14 observation census differs')
    if (main['approved'] is not True or main['status'] != 'accepted-observation-only' or
            main['receipt_sha256'] != receipt_hash or main['details_sha256'] != details_hash or
            main['saved_output_hashes_and_progress_reconciled'] is not True or
            main['native_replay_or_original_payload_read_in_review'] is not False or
            main['provider_selected'] is not False or main['runtime_eligible'] is not False):
        raise ValueError('accepted V14 main review differs')
    if (complement['status'] != 'accepted-derived-observation-only' or
            not _typed_equal(complement['counts'], dict(positive=15, union_positive=8, blocked=40, union_blocked=26)) or
            complement['factory_or_runtime_approved'] is not False):
        raise ValueError('accepted complementary review differs')
    if (request['kind'] != 'v14-positive-singletons-observation-request-metadata-only' or
            request['status'] != 'proposed-not-admission' or request['observer_receipt_sha256'] != receipt_hash or
            request['main_outcome_review_sha256'] != ACCEPTED['main_review'][1] or
            request['complement_review_sha256'] != ACCEPTED['complement_review'][1] or
            type(request['roots']) is not list or len(request['roots']) != 15 or
            len({r['original_address'] for r in request['roots']}) != 15):
        raise ValueError('accepted positive request differs')
    # Request roots are compared to the independently reviewed rows without
    # converting or restamping their native V14 authority envelopes.
    reviewed = [row['root'] for row in complement['positive_singletons']]
    if not _typed_equal(sorted(request['roots'], key=lambda r: r['original_address']), sorted(reviewed, key=lambda r: r['original_address'])):
        raise ValueError('positive request and complementary review differ')
    return True


def load_accepted_metadata(root):
    """Read only bounded, pinned saved metadata; never open the details body."""
    root = Path(root).resolve(strict=True)
    loaded = {}
    for name in ('receipt', 'main_review', 'complement_review', 'positive_request'):
        relative, expected = ACCEPTED[name]
        path = (root / relative).resolve(strict=True)
        if not path.is_relative_to(root / 'build' / 'rebuild'):
            raise ValueError('metadata path escapes private output')
        with path.open('rb') as stream:
            body = stream.read(MAX_RECORD_BYTES + 1)
        if len(body) > MAX_RECORD_BYTES or hashlib.sha256(body).hexdigest() != expected:
            raise ValueError('accepted metadata hash differs: ' + name)
        loaded[name] = json.loads(body, object_pairs_hook=_pairs, parse_constant=_invalid_constant)
    validate_saved_reviews(loaded['receipt'], loaded['main_review'], loaded['complement_review'], loaded['positive_request'])
    return loaded


def select_accepted_candidates(details_path, saved, qualification_request, current_groups, prepared):
    """Authenticate and reconcile the complete V14 stream before returning work.

    This performs no original object, source, reference or executable access.
    The caller must already have authenticated the other supplied metadata.
    """
    import cached_frontier_code_factory_v14 as selection
    selector_path = Path(__file__).resolve().parent / 'cached_frontier_code_factory_v14.py'
    if (Path(selection.__file__).resolve() != selector_path or
            hashlib.sha256(selector_path.read_bytes()).hexdigest() != '565cf51b6d709e0638ae2fb347be3fef6d684f4c13dbdca359c5ea784a31e8c7'):
        raise ValueError('reviewed V14 selector source differs')
    receipt = saved['receipt']
    validate_saved_reviews(receipt, saved['main_review'], saved['complement_review'], saved['positive_request'])
    rows = read_observations(details_path, expected_sha256=ACCEPTED['details'][1],
        expected_bytes=receipt['details_bytes'])
    request, chosen, ledger = selection.select_candidates(receipt, iter(rows), qualification_request,
        current_groups, prepared, expected_census=(55,34,89), expected_current_codes=626,
        expected_prepared=(14550,14556), receipt_sha256=ACCEPTED['receipt'][1])
    expected = sorted(saved['positive_request']['roots'], key=lambda r: r['original_address'])
    if not _typed_equal(request['roots'], expected) or len(chosen) != 15:
        raise ValueError('derived selection differs from whole accepted positive request')
    reviewed = {row['ordinal']: row for row in saved['complement_review']['positive_singletons']}
    if len(reviewed) != 15:
        raise ValueError('duplicate reviewed observation ordinal')
    for selected in chosen:
        authority = selected['authority']; ordinal = authority['ordinal']
        if ordinal not in reviewed:
            raise ValueError('selected observation missing independent review')
        review = reviewed[ordinal]
        if (not _typed_equal(selected['root'], review['root']) or
                any(authority[k] != review[k] for k in ('record_sha256','certificate_sha256','contract_identity_sha256'))):
            raise ValueError('selected observation differs from independent review')
    contexts = {item['root']['original_address']: rows[item['authority']['ordinal'] - 1] for item in chosen}
    return request, chosen, ledger, contexts


def verify_member(raw, record, selected, providers, exports, original_path, stage_path, pe, recipe):
    """Run the unchanged frozen projection and both original/staged comparisons."""
    import cached_frontier_code_factory_v14 as v14
    import cached_frontier_code_factory_v13 as v13
    v14.validate_selected(record, selected)
    root = selected['root']; contract = record['contract']; certificate = record['certificate']
    frozen = v13.frozen
    if contract['fields']:
        assessment = frozen.fields.core.assess_member(raw, contract, certificate, [root], providers, existing_exports=exports)
        if assessment['eligible'] is not True:
            if not assessment['blockers']:
                raise ValueError('unsupported field assessment lacks blockers')
            return None, None, assessment
    else:
        assessment = None
    output, projection = frozen.verify_candidate(raw, record, root, providers, exports,
        original_path, stage_path, pe, recipe)
    for key, name in (('before_comparison',root['symbol']),('after_comparison',projection['exports'][0])):
        reports = projection[key]
        if type(reports) is not list or len(reports) != 1:
            raise ValueError('one full comparison required')
        report = reports[0]
        if not (report['verdict'] == 'match' and report['address'] == root['original_address'] and
                report['symbol'] == name and type(report['size']) is int and
                type(report['compiled_extent']) is int and report['size'] == report['compiled_extent'] == root['size'] and
                not report['errors'] and not report.get('byte_differences',[]) and
                len(report['relocations']) == len(contract['fields']) and
                all(r['match'] is True and r['expected'] == r['observed'] for r in report['relocations'])):
            raise ValueError('full original and staged plain MATCH required')
    if len(projection['fields']) != len(contract['fields']):
        raise ValueError('projected original field census differs')
    if assessment is not None and (not _typed_equal(projection['fields'],assessment['fields']) or
                                   not _typed_equal(projection['exports'],assessment['exports'])):
        raise ValueError('field assessment and projection disagree')
    if assessment is None:
        assessment = dict(eligible=True,blockers=[],strict_zero_consumer_replayed=True,serialization_performed=False,
            requested_roots=[root],contract_identity_sha256=v13.digest(contract),certificate_sha256=v13.digest(certificate))
    projection.update(authority=selected['authority'],central_record_sha256=v13.digest(record),
        native_observation_record_sha256=v13.digest(record),qualified_metadata_row_sha256=record['qualified_metadata_row_sha256'])
    return output, projection, assessment


def field_proof_record(member, record, selected, projection, output):
    import cached_frontier_code_factory_v14 as v14
    import frontier_wave_factory_v8 as proof
    v14.validate_selected(record, selected)
    return proof.field_proof_record(member, record, selected, projection, output)


def load_qualification_metadata(root, saved):
    """Authenticate the selected V14 saved context without reading original bodies."""
    import cached_root_observe_v14 as native
    root = Path(root).resolve(strict=True)
    roles = ('qualified_receipt','qualified_inventory','qualified_request','qualified_registry',
             'prepared_epoch','prepared_review','current_groups','current_review')
    native_source = root / 'tools/rebuild/cached_root_observe_v14.py'
    if hashlib.sha256(native_source.read_bytes()).hexdigest() != '2b7a01ae18a9ea862da8a1c92ebb4d9608c199c7d45b6b23d83bb4ace85dedd4':
        raise ValueError('accepted V14 observer source differs')
    if Path(native.__file__).resolve() != native_source.resolve():
        raise ValueError('foreign V14 observer module')
    loaded = {}
    for role in roles:
        ref = native.ARTIFACT_PINS[role]
        if not _typed_equal(saved['receipt']['inputs'][role], ref):
            raise ValueError('observation input binding differs: ' + role)
        path = (root / ref['path']).resolve(strict=True)
        if not path.is_relative_to(root / 'build' / 'rebuild'):
            raise ValueError('qualification metadata escaped private root')
        with path.open('rb') as stream:
            body = stream.read(MAX_DETAIL_BYTES + 1)
        if len(body) > MAX_DETAIL_BYTES or hashlib.sha256(body).hexdigest() != ref['sha256']:
            raise ValueError('qualification metadata hash differs: ' + role)
        loaded[role] = json.loads(body, object_pairs_hook=_pairs, parse_constant=_invalid_constant)
    groups = {}
    for item in loaded['qualified_request']['roots']:
        groups.setdefault(item['recipe_index'], []).append(item)
    native.validate_qualification_scope(loaded['qualified_receipt'],loaded['qualified_request'],
        loaded['qualified_inventory'],loaded['qualified_registry'],groups)
    native.validate_frontier_context(loaded['qualified_request'],loaded['qualified_inventory'],
        loaded['current_groups'],loaded['prepared_epoch'])
    native.validate_current_reviews(loaded['prepared_review'],loaded['current_review'],
        native.ARTIFACT_PINS['prepared_epoch']['sha256'],native.ARTIFACT_PINS['current_groups']['sha256'])
    return loaded


def produce_selected(record, selected, unit, retained_proof, original_path, stage_path,
                     providers, exports, pe, snapshot, highlow, field_facts):
    """Audit retained fields and project exactly one selected original body.

    Only a reviewed, leased operation may call this function. Its caller owns
    stable-input rechecks, output protection and the all-or-nothing journal.
    """
    import cached_frontier_code_factory_v14 as v14
    import cached_frontier_code_factory_v13 as v13
    v14.validate_selected(record, selected)
    root = selected['root']; contract = record['contract']
    if (not _typed_equal(contract['unit_verified_functions'],retained_proof['verified_functions']) or
            contract['provenance']['recipe_unit_sha256'] != retained_proof['recipe_unit_sha256']):
        raise ValueError('full retained source proof differs')
    facts = v13.audit.audit_original_fields(snapshot,highlow,contract['fields'])
    for site, fact in facts.items():
        if site in field_facts and not _typed_equal(field_facts[site],fact):
            raise ValueError('contradictory original operand field facts')
        field_facts[site] = fact
    with Path(original_path).open('rb') as stream:
        raw = stream.read(MAX_RECORD_BYTES + 1)
    if len(raw) > MAX_RECORD_BYTES or hashlib.sha256(raw).hexdigest() != root['object_sha256']:
        raise ValueError('bounded original object identity differs')
    output, projection, assessment = verify_member(raw,record,selected,providers,exports,
        original_path,stage_path,pe,unit['recipe'])
    if output is None:
        return dict(root=root,status='quarantined-unsupported-policy',assessment=assessment)
    proof = field_proof_record(Path(stage_path).name,record,selected,projection,output)
    return dict(root=root,status='emitted',assessment=assessment,projection=projection,field_proof=proof,output=output)

PROVIDER_INPUTS = {
    'selection': ('build/rebuild/function-selection-v2.json','48ae62cdc5b1754b9c4af674ef4716d53afb554882e174a93acf860eaf1c6cb1'),
    'planned_map': ('build/rebuild/root-certificate-composer-v1/physical-provider-map.json','6cd5bf884bb28d460cfc92f63b765c15413904f58355844243ddd6b59b97001c'),
    'owners': ('build/rebuild/runtime-data-owners-native-v1.json','fac1496a2675e9a6b697d604c8d5b35a2e4b8bb6194e2ec823e5a37d1092f2e8'),
    'image_check': ('build/image_check.json','c03da09d39b8fd22283792c3dc1fbb6ac1e526d8afadd832fabc4071f1720cb1'),
}


def load_provider_inputs(root, saved, qualification):
    """Authenticate provider metadata and retained recipe evidence only.

    No source body, object, reference image or compiler is opened here. The
    caller must separately protect these inputs for its entire operation.
    """
    import cached_root_observe_v14 as native
    import cached_frontier_code_factory_v13 as v13
    root = Path(root).resolve(strict=True)
    refs = dict(PROVIDER_INPUTS)
    for name in ('manifest','retained','recipes'):
        ref = native.ARTIFACT_PINS[name]
        if not _typed_equal(saved['receipt']['inputs'][name],ref):
            raise ValueError('observed input binding differs: '+name)
        refs[name] = (ref['path'],ref['sha256'])
    values = {}
    for name,(relative,expected) in refs.items():
        path=(root/relative).resolve(strict=True)
        if not path.is_relative_to(root) or (name not in ('image_check','recipes') and
                not path.is_relative_to(root/'build'/'rebuild')):
            raise ValueError('provider metadata path escapes scope')
        with path.open('rb') as stream:
            body=stream.read(MAX_DETAIL_BYTES+1)
        if len(body)>MAX_DETAIL_BYTES or hashlib.sha256(body).hexdigest()!=expected:
            raise ValueError('provider metadata hash differs: '+name)
        if name in ('selection','planned_map','owners'):
            # Bind provider descriptors to the accepted qualification receipt.
            recorded=qualification['qualified_receipt']['inputs'].get(str(path))
            if recorded != expected:
                raise ValueError('qualification does not bind provider input: '+name)
        values[name]=json.loads(body,object_pairs_hook=_pairs,parse_constant=_invalid_constant)
    retained=values['retained']; manifest=values['manifest']
    if retained['inputs']['image_check_sha256'] != PROVIDER_INPUTS['image_check'][1]:
        raise ValueError('retained image-check identity differs')
    units={u['recipe_id']:u for u in manifest['units']}
    proofs={p['recipe_id']:p for p in retained['units']}
    if not (len(units)==len(manifest['units'])==len(proofs)==len(retained['units'])==2988 and
            len(values['selection']['selections'])==68657):
        raise ValueError('provider metadata universe differs')
    if not v13.base.reconcile_recipes(manifest,root/refs['recipes'][0])['verified']:
        raise ValueError('recipe metadata differs')
    providers=v13.frozen.fields.validate_provider_map(values['planned_map'],values['selection']['selections'],
        units,proofs,values['owners'])
    if len(providers)!=68657:
        raise ValueError('whole physical provider map required')
    request=qualification['qualified_request']
    v13.base.collector.validate_request(request,values['selection']['selections'],manifest,retained,providers)
    by_recipe={}
    for item in request['roots']:
        by_recipe.setdefault(item['recipe_id'],[]).append(item)
    for recipe_id, roots in by_recipe.items():
        if recipe_id not in units or recipe_id not in proofs:
            raise ValueError('qualified recipe missing retained evidence')
        native.validate_roots(units[recipe_id],proofs[recipe_id],roots)
    return dict(values=values,units=units,proofs=proofs,providers=providers,
        input_sha256={str((root/path).resolve()):h for path,h in refs.values()})


def project_batch(out, selections, contexts, provider_state, prepared_epoch, native_root,
                  snapshot, pe, highlow, inputs, note, guard):
    """Stage selected members and complete original-field evidence.

    Requires the caller's reviewed operation, input/output protection and
    process-tree watchdog. This helper creates no receipt and grants no admission.
    """
    import cached_frontier_code_factory_v13 as v13
    import os
    out=Path(out).resolve(strict=True); native_root=Path(native_root).resolve(strict=True)
    if len(highlow)!=351931 or len(selections)!=15 or len(contexts)!=15:
        raise ValueError('whole V14 request and fresh HIGHLOW census required')
    providers=provider_state['providers'];units=provider_state['units'];proofs=provider_state['proofs']
    exports=set(prepared_epoch['exclusion_names'])
    field_facts={}; outcomes=[]; members=[]; field_proofs=[]
    for selected in sorted(selections,key=lambda s:(s['root']['recipe_index'],s['authority']['ordinal'])):
        root=selected['root']; address=root['original_address']; record=contexts[address]
        unit=units[root['recipe_id']]; proof=proofs[root['recipe_id']]
        source=(v13.ROOT/unit['source']).resolve(); original=(native_root/unit['object']).resolve()
        if (not source.is_relative_to(v13.ROOT) or not original.is_relative_to(v13.ROOT/'build/rebuild') or
                source.is_relative_to(out) or original.is_relative_to(out)):
            raise ValueError('original path escapes authorized scope or overlaps output')
        guard.check('before-source')
        v13.base.observe(source,root['source_sha256'],inputs)
        guard.check('after-source')
        guard.check('before-object')
        v13.base.observe(original,root['object_sha256'],inputs)
        name='CACHED-CODE-%03d-%s.obj'%(len(members),address[2:]);stage=out/name
        outcome=produce_selected(record,selected,unit,proof,original,stage,providers,exports,
            pe,snapshot,highlow,field_facts)
        guard.check('after-object')
        if outcome['status']=='emitted':
            output=outcome.pop('output'); projection=outcome['projection']
            if not stage.is_file() or v13.base.file_hash(stage)!=projection['output_sha256']:
                raise ValueError('staged member identity differs')
            v13.base.observe(stage,projection['output_sha256'],inputs)
            members.append((name,output));field_proofs.append(outcome.pop('field_proof'))
            note('member_verified',original_address=address,object_sha256=projection['output_sha256'])
        else:
            if stage.exists():
                raise ValueError('quarantined member left staged output')
            note('member_quarantined',original_address=address)
        outcomes.append(outcome)
    wanted={s['root']['original_address'] for s in selections}
    if (len(wanted)!=15 or len(outcomes)!=15 or
            {o['root']['original_address'] for o in outcomes}!=wanted or
            any(o['status'] not in ('emitted','quarantined-unsupported-policy') for o in outcomes)):
        raise ValueError('whole selection terminal partition differs')
    return dict(outcomes=outcomes,members=members,field_proofs=field_proofs,field_facts=field_facts)


def stage_archive(out, batch, inputs, *, remaining_bytes):
    """Stage and independently reparse every recovered archive member."""
    import cached_frontier_code_factory_v13 as v13
    out=Path(out).resolve(strict=True);members=batch['members']
    if type(remaining_bytes) is not int or remaining_bytes<0 or remaining_bytes>MAX_DETAIL_BYTES:
        raise ValueError('bounded remaining output allowance required')
    if not members:
        return None
    import re
    if (len({name for name,_ in members})!=len(members) or
            any(not isinstance(name,str) or not re.fullmatch(r'CACHED-CODE-[0-9]{3}-[0-9a-f]{8}\.obj',name) or
                type(body) is not bytes for name,body in members)):
        raise ValueError('duplicate or invalid archive member name/body')
    blob=v13.base.coff.archive(members)
    # The recovered copies are output too; reserve them before writing anything.
    if len(blob)+sum(len(body) for _,body in members)>remaining_bytes:
        raise ValueError('archive and recovered copies exceed output allowance')
    recovered=v13.base.coff.read_archive(blob)
    if recovered['members']!=members or len(recovered['index'])!=len(members):
        raise ValueError('archive member or index identity differs')
    archive=out/'CACHED-code.lib';v13.base.pool.fsynced(archive,blob)
    archive_hash=v13.base.coff.digest(blob);v13.base.observe(archive,archive_hash,inputs)
    for name,body in recovered['members']:
        path=out/('recovered-'+name)
        v13.base.pool.fsynced(path,body)
        v13.base.bulk.strict_reparse(path,body)
        v13.base.observe(path,v13.base.coff.digest(body),inputs)
    return archive_hash


def write_evidence(out, batch, selections, contexts, native_ledger, current_ledger, *, start):
    """Write complete selected contexts, projections, blockers and field proofs."""
    import cached_frontier_code_factory_v13 as v13
    import cached_root_observe_v14 as native
    import os
    out=Path(out).resolve(strict=True)
    selected_by_address={s['root']['original_address']:s for s in selections}
    if (len(selected_by_address)!=15 or set(selected_by_address)!=set(contexts) or
            {o['root']['original_address'] for o in batch['outcomes']}!=set(contexts)):
        raise ValueError('complete selected evidence required')
    records=[dict(selection=selected_by_address[a],observation=contexts[a]) for a in sorted(contexts)]
    proof_rows=batch['field_proofs']
    if len(proof_rows)!=len(batch['members']):
        raise ValueError('one complete proof per emitted member required')
    for filename,rows in (('selected-contexts.jsonl.gz',records),('field-proofs.jsonl.gz',proof_rows)):
        with (out/filename).open('xb') as raw:
            with gzip.GzipFile(fileobj=v13.metadata.BoundedSink(raw,start,out),mode='wb',mtime=0) as stream:
                for row in rows:
                    stream.write(native.canonical(row)+b'\n')
                    v13.base.budget(start,out)
            raw.flush();os.fsync(raw.fileno())
    emitted=[o for o in batch['outcomes'] if o['status']=='emitted']
    blocked=[o for o in batch['outcomes'] if o['status']=='quarantined-unsupported-policy']
    evidence=[('members',emitted),('blocked',blocked),('native-ledger',native_ledger),
        ('current-frontier-ledger',current_ledger),('original-field-audit',
        dict(highlow_sites=351931,unique_field_sites=len(batch['field_facts']),
             field_facts_sha256=v13.digest(sorted(batch['field_facts'].items())),
             function_index_present=False,canonical_index_checked=False,
             span_authority='retained-physical-span-and-original-staged-compiled-extents'))]
    for name,value in evidence:
        v13.metadata.save_bounded_json(out/(name+'.json'),value,start,out)
    return dict(requested=len(selections),emitted=len(emitted),blocked=len(blocked),
        status='completed-incomplete' if blocked else 'completed')


def current_code_ledger(groups, qualification_request, native_ledger, providers, exports, outcomes):
    """Record every current CODE demand without inferring historic outcomes."""
    import cached_frontier_code_factory_v13 as v13
    singles={e['roots'][0]['original_address']:e for e in native_ledger if e['event']=='SINGLE_ROOT_OBSERVATION'}
    known={v13.base.pool.canonical({k:r[k] for k in ('recipe_id','object_sha256','symbol_index')}):r
           for r in qualification_request['roots']}
    quarantine={v13.base.pool.canonical(providers[a]) for a in v13.QUARANTINES}
    terminal={o['root']['original_address']:o for o in outcomes}
    if (len(singles)!=55 or len(known)!=55 or len(terminal)!=15 or
            any(o['status'] not in ('emitted','quarantined-unsupported-policy') for o in outcomes)):
        raise ValueError('whole V14 native and terminal ledgers required')
    result=[]
    for ordinal,group in enumerate(groups['groups'],1):
        if group['classification']!='CODE':
            continue
        name=group['symbol']; entry=dict(symbol=name,group_ordinal=ordinal,group_sha256=v13.digest(group),
            original_bases=group['original_bases'])
        if name in exports:
            state='PREPARED_SKIP'
        elif name in quarantine:
            state='PRESERVED_REFERENCE_GROUP_QUARANTINE'
        elif name in known:
            root=known[name]; source=singles[root['original_address']]
            entry.update(root=root,native_record_sha256=source['record_sha256'],original_blocker_codes=source['blocker_codes'])
            if source['closure_observed']:
                outcome=terminal[root['original_address']]
                state='EMITTED' if outcome['status']=='emitted' else 'QUARANTINED_UNSUPPORTED_POLICY'
            else:
                state='NATIVE_ORIGINAL_NEGATIVE_PRESERVED'
        else:
            state='OUTSIDE_NEW_NATIVE_OBSERVATION_UNIVERSE'
        entry['production_status']=state;result.append(entry)
    if len(result)!=626 or len({r['symbol'] for r in result})!=626:
        raise ValueError('whole current V14 CODE ledger required')
    return result


def annotate_native_ledger(ledger, outcomes):
    """Bind each positive singleton to exactly its own terminal outcome."""
    import copy
    result=copy.deepcopy(ledger)
    terminal={o['root']['original_address']:o for o in outcomes}
    if len(terminal)!=15 or any(o['status'] not in ('emitted','quarantined-unsupported-policy') for o in outcomes):
        raise ValueError('unique terminal outcomes required')
    seen=set()
    for row in result:
        if row['state']!='ALL_POSITIVE_SINGLETON_REQUESTED':
            continue
        if row['event']!='SINGLE_ROOT_OBSERVATION' or len(row['roots'])!=1:
            raise ValueError('positive union cannot become a provider')
        root=row['roots'][0];address=root['original_address'];outcome=terminal[address]
        if address in seen or not _typed_equal(root,outcome['root']):
            raise ValueError('terminal result borrowed or duplicate')
        seen.add(address)
        if outcome['status']=='emitted':
            row['production_status']='EMITTED'
        else:
            blockers=outcome['assessment']['blockers']
            if type(blockers) is not list or not blockers:
                raise ValueError('quarantine lacks explicit blockers')
            row['production_status']='QUARANTINED_UNSUPPORTED_POLICY';row['production_blockers']=blockers
    if seen!=set(terminal):
        raise ValueError('positive native ledger is incomplete')
    return result


def pin_producer_dependencies(root, inputs):
    """Pin the reviewed V13 core and V14 observer/selector dependency tree."""
    import cached_frontier_code_factory_v13 as v13
    import cached_root_observe_v14 as native
    import cached_frontier_code_factory_v14 as selector
    root=Path(root).resolve(strict=True)
    pinned={**v13.PINS,
        'tools/rebuild/cached_frontier_code_factory_v13.py':'b502ff4c79e608e6cf444b9db2621704135ec435dab35aef602c11c316102c1e',
        'tools/rebuild/cached_root_observe_v14.py':'2b7a01ae18a9ea862da8a1c92ebb4d9608c199c7d45b6b23d83bb4ace85dedd4',
        'tools/rebuild/cached_frontier_code_factory_v14.py':'565cf51b6d709e0638ae2fb347be3fef6d684f4c13dbdca359c5ea784a31e8c7',
        'tools/rebuild/v14_factory_output_publication.py':'86ebab28decd164fb0d2bbd9f0be0f8e20508deef620f31ecdbe874f5c4baebc'}
    for name,expected in pinned.items():
        path=(root/name).resolve(strict=True)
        frozen_composer=root/'build/rebuild/root-certificate-composer-v1/source-freeze-v1/root_certificate_composer.py'
        if not path.is_relative_to(root/'tools') and path!=frozen_composer:
            raise ValueError('foreign producer dependency')
        v13.base.observe(path,expected,inputs)
    for module in (v13,native,selector,v13.frozen,v13.prior,v13.metadata,v13.audit,v13.base,
                   v13.frozen.fields,v13.frozen.fields.core,v13.base.bulk,v13.base.coff,
                   v13.base.pool,v13.base.inventory,v13.base.collector,v13.previous,native.previous):
        if Path(module.__file__).resolve()!=root/'tools/rebuild'/Path(module.__file__).name:
            raise ValueError('foreign loaded producer module')
    return pinned


def summarize_batch(batch, selections, contexts):
    """Cross-check emitted members and proofs before any output receipt."""
    import cached_frontier_code_factory_v14 as v14
    import cached_frontier_code_factory_v13 as v13
    selected={s['root']['original_address']:s for s in selections}
    outcomes={o['root']['original_address']:o for o in batch['outcomes']}
    if len(selected)!=15 or len(outcomes)!=15 or set(selected)!=set(outcomes) or set(contexts)!=set(selected):
        raise ValueError('entire unique V14 batch required')
    emitted=[o for o in batch['outcomes'] if o['status']=='emitted']
    blocked=[o for o in batch['outcomes'] if o['status']=='quarantined-unsupported-policy']
    if len(emitted)+len(blocked)!=15 or len(batch['members'])!=len(emitted) or len(batch['field_proofs'])!=len(emitted):
        raise ValueError('member/proof/terminal partition differs')
    for index,outcome in enumerate(emitted):
        address=outcome['root']['original_address']; choice=selected[address];record=contexts[address]
        v14.validate_selected(record,choice)
        if not _typed_equal(outcome['root'],choice['root']):
            raise ValueError('emitted outcome borrowed root')
        name,body=batch['members'][index]; projection=outcome['projection'];proof=batch['field_proofs'][index]
        if (hashlib.sha256(body).hexdigest()!=projection['output_sha256'] or
                not _typed_equal(proof,field_proof_record(name,record,choice,projection,body))):
            raise ValueError('emitted member/full proof differs')
        for key in ('before_comparison','after_comparison'):
            reports=projection[key]
            if (type(reports) is not list or len(reports)!=1 or reports[0]['verdict']!='match' or
                    reports[0]['errors'] or reports[0].get('byte_differences',[]) or
                    not all(r['match'] is True and r['expected']==r['observed'] for r in reports[0]['relocations'])):
                raise ValueError('full comparison proof no longer matches')
    for outcome in blocked:
        address=outcome['root']['original_address']
        if (not _typed_equal(outcome['root'],selected[address]['root']) or
                outcome['assessment']['eligible'] is not False or
                type(outcome['assessment']['blockers']) is not list or not outcome['assessment']['blockers']):
            raise ValueError('unsupported quarantine evidence differs')
    return dict(requested=15,emitted=len(emitted),blocked=len(blocked))


def publish_batch(out, operation_sha256, journal, batch, selections, contexts, inputs, *, start, source_snapshots, guard, small_metadata):
    """Publish the explicitly enumerated full staged artifact census."""
    import cached_frontier_code_factory_v13 as v13
    import v14_factory_output_publication as publication
    out=Path(out).resolve(strict=True)
    publisher=Path(__file__).resolve().parent/'v14_factory_output_publication.py'
    if (Path(publication.__file__).resolve()!=publisher or hashlib.sha256(publisher.read_bytes()).hexdigest()!=
            '86ebab28decd164fb0d2bbd9f0be0f8e20508deef620f31ecdbe874f5c4baebc'):
        raise ValueError('independently reviewed publisher differs')
    summary=summarize_batch(batch,selections,contexts)
    names={'selected-contexts.jsonl.gz','field-proofs.jsonl.gz','members.json','blocked.json',
        'native-ledger.json','current-frontier-ledger.json','original-field-audit.json','coverage.jsonl.gz',
        Path(journal.name).resolve(strict=True).relative_to(out).as_posix()}
    for name,_ in batch['members']:
        names.update((name,'recovered-'+name))
    if batch['members']:
        names.add('CACHED-code.lib')
    if type(source_snapshots) is not dict or not source_snapshots:
        raise ValueError('exact reviewed source snapshots required')
    for relative,expected in source_snapshots.items():
        if not isinstance(relative,str) or not relative.startswith('source-snapshots/') or relative in names:
            raise ValueError('invalid source snapshot name')
        path=(out/relative).resolve(strict=True)
        if not path.is_relative_to(out/'source-snapshots') or v13.base.file_hash(path)!=expected:
            raise ValueError('source snapshot identity differs')
        names.add(relative)
    hashes={}
    for name in names:
        path=(out/name).resolve(strict=True)
        if not path.is_relative_to(out):
            raise ValueError('output escaped staging directory')
        hashes[name]=v13.base.file_hash(path)
    stable_calls=0
    def stable():
        nonlocal stable_calls
        stable_calls+=1
        if stable_calls>3:
            raise ValueError('unexpected publisher stability callback count')
        guard.refresh()
        stable_with_small_metadata(inputs,small_metadata)
        v13.base.budget(start,out)
        if stable_calls==3:
            guard.check('after-publication')
        else:
            guard.refresh()
    guard.check('before-publication')
    result=publication.publish_complete(out,hashes,operation_sha256,journal,stable,summary=summary)
    if stable_calls!=3:
        raise ValueError('incomplete publisher stability callbacks')
    return result


def write_complete_coverage(out, provider_state, prepared_epoch, qualification_request, selections, batch, current_ledger):
    """Retain the frozen all-owner coverage semantics for V14's current demand."""
    import cached_frontier_code_factory_v13 as v13
    names={row['symbol'] for row in current_ledger}
    wanted={s['root']['original_address'] for s in selections}
    emitted={o['root']['original_address'] for o in batch['outcomes'] if o['status']=='emitted'}
    if len(names)!=626 or len(wanted)!=15 or not emitted<=wanted:
        raise ValueError('whole V14 coverage inputs required')
    return v13.write_coverage(Path(out)/'coverage.jsonl.gz',provider_state['providers'],
        set(prepared_epoch['exclusion_names']),qualification_request,wanted,emitted,names)

# A source/input review must bind an exact operation profile before run can read
# metadata or create staging. This remains unset until independent acceptance.
ACTUAL_OPERATION_PROFILE = None


def run(args):
    """Run the reviewed single V14 operation; reject until authority is bound."""
    if ACTUAL_OPERATION_PROFILE is None:
        raise ValueError('V14 operation/source review and resource authority are not bound')
    raise ValueError('standalone factory entry is disabled; held launcher required')


def validate_operation_review(review, operation_sha256):
    """Bind the source/input review while requiring a later fresh lease."""
    required=('approved','root_authorized','source_review_pass','input_review_pass','resource_lease_required',
              'allow_original_objects_read','allow_source_hashing','allow_reference_image_read','allow_code_emission')
    forbidden=('allow_native_tools','allow_executable_link','allow_game_execution')
    keys={'schema_version','kind','reviewer','operation_sha256','source_sha256','peer_review_path','peer_review_sha256',*required,*forbidden}
    if (type(review) is not dict or set(review)!=keys or type(review['schema_version']) is not int or
            review['schema_version']!=1 or review['kind']!='v14-factory-source-input-review-v1' or
            review['operation_sha256']!=operation_sha256 or
            any(review[k] is not True for k in required) or any(review[k] is not False for k in forbidden) or
            type(review['source_sha256']) is not dict or set(review['source_sha256'])!={
                'tools/rebuild/cached_frontier_code_factory_v14_driver.py',
                'tests/rebuild/test_cached_frontier_code_factory_v14_driver.py'} or
            type(review['reviewer']) is not str or not review['reviewer'] or
            review['reviewer'] in ('/root/terra_factory_driver_v14','/root/terra_code_pipeline_v14') or
            any(type(h) is not str or len(h)!=64 or any(c not in '0123456789abcdef' for c in h)
                for h in (*review['source_sha256'].values(),review['peer_review_sha256'])) or
            type(review['peer_review_path']) is not str):
        raise ValueError('exact independent reviewed operation policy required')
    return True


def validate_complementary_review(peer, primary, operation_sha256):
    """Require distinct independently approved, explicitly non-admission evidence."""
    keys={'schema_version','kind','reviewer','approved','operation_sha256','source_sha256',
          'profile_packet_path','profile_packet_sha256','provider_selected','runtime_eligible'}
    if (type(peer) is not dict or set(peer)!=keys or type(peer['schema_version']) is not int or
            peer['schema_version']!=1 or peer['kind']!='v14-factory-input-complement-review-v1' or
            peer['approved'] is not True or peer['operation_sha256']!=operation_sha256 or
            not _typed_equal(peer['source_sha256'],primary['source_sha256']) or
            type(peer['reviewer']) is not str or not peer['reviewer'] or
            peer['reviewer'] in (primary['reviewer'],'/root/terra_factory_driver_v14','/root/terra_code_pipeline_v14') or
            peer['provider_selected'] is not False or peer['runtime_eligible'] is not False or
            type(peer['profile_packet_path']) is not str or type(peer['profile_packet_sha256']) is not str or
            len(peer['profile_packet_sha256'])!=64 or any(c not in '0123456789abcdef' for c in peer['profile_packet_sha256'])):
        raise ValueError('independent complementary input review required')
    return True


def read_small_bound_json(path,expected):
    """Hash-bind one small metadata object with the bound enforced at read."""
    with Path(path).open('rb') as stream:
        body=stream.read(1024*1024+1)
    if not body or len(body)>1024*1024 or hashlib.sha256(body).hexdigest()!=expected:
        raise ValueError('small metadata hash or size differs')
    value=json.loads(body,object_pairs_hook=_pairs,parse_constant=_invalid_constant)
    if type(value) is not dict:
        raise ValueError('small metadata object required')
    return value


def stable_with_small_metadata(inputs,small_paths):
    """Retain the original stability gate and enforce each small read bound."""
    import cached_frontier_code_factory_v13 as v13
    small={Path(p) for p in small_paths}
    if len(small)!=len(small_paths) or not small.issubset(inputs):
        raise ValueError('exact protected small metadata set required')
    v13.base.stable({p:h for p,h in inputs.items() if p not in small})
    for path in small:
        read_small_bound_json(path,inputs[path])


def validate_profile_binding(packet,actual,primary_sha256):
    """Only the reviewed draft's fresh review/slot/lease placeholders may vary."""
    import copy
    if (type(packet) is not dict or packet.get('kind')!='v14-factory-exact-profile-packet' or
            packet.get('status')!='pending-review-and-fresh-lease-NOT-LAUNCHABLE' or
            type(packet.get('profile_draft')) is not dict or type(actual) is not dict):
        raise ValueError('exact reviewed profile packet required')
    expected=copy.deepcopy(packet['profile_draft'])
    if (expected['operation']['review_sha256'] is not None or expected['slot'] is not None or
            expected['lease_sha256'] is not None or
            expected['metadata_inputs'].get(expected['operation']['review_path'],'missing') is not None or
            type(actual.get('slot')) is not int or actual['slot'] not in (1,2) or
            type(actual.get('lease_sha256')) is not str or len(actual['lease_sha256'])!=64 or
            any(c not in '0123456789abcdef' for c in actual['lease_sha256'])):
        raise ValueError('reviewed draft placeholders or fresh lease identity differ')
    expected['operation']['review_sha256']=primary_sha256
    expected['metadata_inputs'][expected['operation']['review_path']]=primary_sha256
    expected['slot']=actual['slot'];expected['lease_sha256']=actual['lease_sha256']
    if not _typed_equal(expected,actual):
        raise ValueError('held profile differs from reviewed draft')
    return True


def _run_authorized(args, profile, guard):
    guard=_AbsentIndexGuard(_authenticate_held(profile,guard),Path(__file__).resolve().parents[2]/'build/function_index.json')
    import os
    import time
    import cached_frontier_code_factory_v13 as v13
    import cached_root_observe_v14 as native
    if guard is None or getattr(guard,'profile',None) is not profile:
        raise ValueError('held reviewed guard required')
    guard.check('before-metadata')
    start=time.monotonic();root=v13.ROOT.resolve();inputs={};out=None;journal=None;snapshot=None
    # The profile comes from the frozen reviewed source, never from a CLI caller.
    held_profile=profile
    operation_profile=profile['operation']
    _validate_held_metadata(profile,operation_profile,native)
    profile=operation_profile
    operation_path=Path(args.operation).resolve(strict=True);review_path=Path(args.review).resolve(strict=True)
    if not operation_path.is_relative_to(root/'build/rebuild') or not review_path.is_relative_to(root/'build/rebuild'):
        raise ValueError('private reviewed operation/review paths required')
    operation=native.read_bound_json(operation_path,profile['operation_sha256'])
    review=native.read_bound_json(review_path,profile['review_sha256'])
    inputs[operation_path]=profile['operation_sha256'];inputs[review_path]=profile['review_sha256']
    if (type(operation) is not dict or set(operation)!={'schema_version','kind','epoch','roots','output_relative','limits'} or
            type(operation['schema_version']) is not int or operation['schema_version']!=1 or
            operation['kind']!='cached-native-positive-CODE-v14-operation' or
            operation['output_relative']!=profile['output_relative'] or not _typed_equal(operation['limits'],profile['limits']) or
            not _typed_equal(profile['limits'],v13.LIMITS) or
            type(operation['epoch']) is not str or not operation['epoch'] or len(operation['epoch'])>100):
        raise ValueError('closed reviewed V14 operation differs')
    validate_operation_review(review,profile['operation_sha256'])
    from pathlib import PurePosixPath
    relative=review['peer_review_path']; part=PurePosixPath(relative)
    if ('\\' in relative or part.is_absolute() or part.as_posix()!=relative or
            any(piece in ('','.','..') for piece in part.parts)):
        raise ValueError('canonical complementary review path required')
    peer_path=(root/relative).resolve(strict=True)
    if (not peer_path.is_relative_to(root/'build/rebuild') or peer_path in inputs or
            not peer_path.is_file() or not 0<peer_path.stat().st_size<=1024*1024):
        raise ValueError('complementary review escaped scope, duplicated input, or exceeded bound')
    peer=read_small_bound_json(peer_path,review['peer_review_sha256'])
    validate_complementary_review(peer,review,profile['operation_sha256'])
    inputs[peer_path]=review['peer_review_sha256']
    packet_relative=peer['profile_packet_path'];packet_part=PurePosixPath(packet_relative)
    if ('\\' in packet_relative or packet_part.is_absolute() or packet_part.as_posix()!=packet_relative or
            any(piece in ('','.','..') for piece in packet_part.parts)):
        raise ValueError('canonical profile packet path required')
    packet_path=(root/packet_relative).resolve(strict=True)
    if (not packet_path.is_relative_to(root/'build/rebuild') or packet_path in inputs or
            not packet_path.is_file() or not 0<packet_path.stat().st_size<=1024*1024):
        raise ValueError('profile packet escaped scope, duplicated input, or exceeded bound')
    packet=read_small_bound_json(packet_path,peer['profile_packet_sha256'])
    validate_profile_binding(packet,held_profile,profile['review_sha256'])
    inputs[packet_path]=peer['profile_packet_sha256']
    out=(root/profile['output_relative']).resolve()
    if (not out.is_relative_to(root/'build/rebuild') or out==root/'build/rebuild' or
            out.exists() or out.is_symlink() or Path(args.out).resolve()!=out):
        raise ValueError('exclusive private versioned output required')
    producer_pins=pin_producer_dependencies(root,inputs)
    for relative,h in review['source_sha256'].items():
        path=(root/relative).resolve(strict=True)
        if not path.is_relative_to(root) or path.is_relative_to(out):
            raise ValueError('reviewed source path out of scope')
        v13.base.observe(path,h,inputs)
    saved=load_accepted_metadata(root);qualification=load_qualification_metadata(root,saved)
    for name in ('receipt','main_review','complement_review','positive_request','details'):
        relative,h=ACCEPTED[name];v13.base.observe(root/relative,h,inputs)
    for role in ('qualified_receipt','qualified_inventory','qualified_request','qualified_registry',
                 'prepared_epoch','prepared_review','current_groups','current_review'):
        ref=native.ARTIFACT_PINS[role];v13.base.observe(root/ref['path'],ref['sha256'],inputs)
    providers=load_provider_inputs(root,saved,qualification);inputs.update({Path(p):h for p,h in providers['input_sha256'].items()})
    request,selected,ledger,contexts=select_accepted_candidates(root/ACCEPTED['details'][0],saved,
        qualification['qualified_request'],qualification['current_groups'],qualification['prepared_epoch'])
    if not _typed_equal(request['roots'],operation['roots']):
        raise ValueError('operation differs from complete reviewed positive request')
    manifest=providers['values']['manifest'];native_root=(root/native.ARTIFACT_PINS['manifest']['path']).parent/manifest.get('object_root_relative','.')
    native_root=native_root.resolve(strict=True)
    if any(path.is_relative_to(out) for path in inputs):
        raise ValueError('protected input overlaps output')
    small_metadata=(peer_path,packet_path)
    stable_with_small_metadata(inputs,small_metadata);guard.check('after-metadata');out.mkdir(parents=True,exist_ok=False)
    try:
        journal=(out/'progress.jsonl').open('x',encoding='utf-8')
        def note(state,**facts):
            journal.write(json.dumps(dict(state=state,**facts),sort_keys=True)+'\n');journal.flush();os.fsync(journal.fileno())
            v13.base.budget(start,out)
        note('started',requested=15)
        snapshots={}
        guard.check('before-source-snapshots')
        for relative,h in {**producer_pins,**review['source_sha256']}.items():
            target=out/'source-snapshots'/relative;target.parent.mkdir(parents=True,exist_ok=True)
            v13.base.pool.fsynced(target,(root/relative).read_bytes());v13.base.observe(target,h,inputs)
            snapshots[target.relative_to(out).as_posix()]=h
        guard.check('after-source-snapshots')
        guard.check('before-reference')
        if Path(args.reference).resolve().is_relative_to(out):
            raise ValueError('reference path overlaps staging')
        reference=v13.base.observe(Path(args.reference),v13.base.pool.PINS['reference'],inputs)
        pe=v13.checked_reference(reference);snapshot=v13.audit.SnapshotPe(reference,pe)
        highlow={snapshot.base+rva for rva in snapshot.relocations()}
        if len(highlow)!=351931:
            raise ValueError('fresh original HIGHLOW census differs')
        guard.check('after-reference')
        batch=project_batch(out,selected,contexts,providers,qualification['prepared_epoch'],native_root,
            snapshot,pe,highlow,inputs,note,guard)
        snapshot.close();snapshot=None
        usage=v13.base.budget(start,out)
        stage_archive(out,batch,inputs,remaining_bytes=profile['limits']['output_bytes']-usage['output_bytes'])
        native_ledger=annotate_native_ledger(ledger,batch['outcomes'])
        current=current_code_ledger(qualification['current_groups'],qualification['qualified_request'],native_ledger,
            providers['providers'],set(qualification['prepared_epoch']['exclusion_names']),batch['outcomes'])
        write_complete_coverage(out,providers,qualification['prepared_epoch'],qualification['qualified_request'],selected,batch,current)
        summary=write_evidence(out,batch,selected,contexts,native_ledger,current,start=start)
        if not _typed_equal(summary,{**summarize_batch(batch,selected,contexts),'status':summary['status']}):
            raise ValueError('evidence and terminal summaries differ')
        guard.check('before-final-stability')
        stable_with_small_metadata(inputs,small_metadata)
        guard.check('after-final-stability')
        note('terminal',**summary);journal.close()
        return publish_batch(out,profile['operation_sha256'],journal,batch,selected,contexts,inputs,start=start,source_snapshots=snapshots,guard=guard,small_metadata=small_metadata)
    except BaseException as error:
        if journal is not None and not journal.closed:
            journal.write(json.dumps(dict(state='failed',error_type=type(error).__name__))+'\n');journal.flush();os.fsync(journal.fileno());journal.close()
        if out is not None and out.exists():
            with (out/'abort.json').open('x',encoding='utf-8') as stream:
                json.dump(dict(status='aborted-no-retry',error_type=type(error).__name__,provider_selected=False,runtime_eligible=False),stream)
                stream.flush();os.fsync(stream.fileno())
        raise
    finally:
        if snapshot is not None:snapshot.close()
        if journal is not None and not journal.closed:journal.close()


# This pin is the independently reviewed held launcher/verifier source.
HELD_PARENT_SHA256='000a937920e69b1fe2c897714fe7f766600c37fba9715f36efe04517ab7d74c4'


def _require_absent_index(path):
    """Reject any index entry, including a dangling link, at every phase."""
    try:
        Path(path).lstat()
    except FileNotFoundError:
        return
    raise ValueError('function index appeared; absent-index operation stopped')


class _AbsentIndexGuard:
    def __init__(self,guard,index_path):
        self._guard=guard
        self._index_path=index_path
        self.profile=guard.profile

    def check(self,phase):
        _require_absent_index(self._index_path)
        result=self._guard.check(phase)
        _require_absent_index(self._index_path)
        return result

    def refresh(self):
        _require_absent_index(self._index_path)
        result=self._guard.refresh()
        _require_absent_index(self._index_path)
        return result


def _authenticate_held(profile,guard):
    """Authenticate the one issued session before project/native input access."""
    import sys
    import types
    runtime=sys.modules.get('_fnv_verified_held_bootstrap_v3')
    if type(runtime) is not types.ModuleType or type(profile) is not dict:
        raise ValueError('held launcher capability is not authenticated')
    path=Path(__file__).resolve().parent/'factory_held_launcher_v4.py'
    with path.open('rb') as stream:
        body=stream.read(1024*1024+1)
    if len(body)>1024*1024 or hashlib.sha256(body).hexdigest()!=HELD_PARENT_SHA256:
        raise ValueError('held launcher verifier source differs')
    verifier=types.ModuleType('_v14_independent_held_verifier')
    verifier.__file__=str(path)
    exec(compile(body,str(path),'exec',dont_inherit=True),verifier.__dict__)
    authenticated=verifier.authenticate_runtime(runtime,profile,guard,parent_sha256=HELD_PARENT_SHA256)
    if authenticated is not guard:
        raise ValueError('held launcher returned a different guard')
    return authenticated


def _validate_held_metadata(profile,op,native):
    if type(op) is not dict or set(op)!={'operation_path','operation_sha256','review_path','review_sha256',
            'reference_path','output_path','output_relative','limits'}:
        raise ValueError('closed held operation required')
    root=native.ROOT.resolve()
    expected={str((root/path).resolve()):h for path,h in ACCEPTED.values()}
    expected.update({str((root/path).resolve()):h for path,h in PROVIDER_INPUTS.values()})
    for role in ('qualified_receipt','qualified_inventory','qualified_request','qualified_registry',
                 'prepared_epoch','prepared_review','current_groups','current_review','manifest','retained','recipes'):
        ref=native.ARTIFACT_PINS[role];expected[str((root/ref['path']).resolve())]=ref['sha256']
    if (op['operation_path']==op['review_path'] or op['operation_path'] in expected or
            op['review_path'] in expected):
        raise ValueError('operation/review roles collide with accepted metadata')
    expected.update({op['operation_path']:op['operation_sha256'],op['review_path']:op['review_sha256']})
    metadata=profile['metadata_inputs']
    if (not _typed_equal(metadata,expected) or op['reference_path'] in metadata or
            op['output_path']!=profile['output'] or
            any(not Path(op[k]).is_absolute() for k in ('operation_path','review_path','reference_path','output_path'))):
        raise ValueError('held operation metadata/path binding differs')


def held_entry(profile, guard):
    """Accept only the one verified held launcher session."""
    from types import SimpleNamespace
    if type(profile) is not dict or type(profile.get('operation')) is not dict:
        raise ValueError('closed held operation required')
    op=profile['operation']
    required={'operation_path','operation_sha256','review_path','review_sha256',
            'reference_path','output_path','output_relative','limits'}
    if set(op)!=required:
        raise ValueError('closed held operation required')
    args=SimpleNamespace(operation=op['operation_path'],review=op['review_path'],
        reference=op['reference_path'],out=op['output_path'])
    return _run_authorized(args,profile,guard)


def main(argv=None):
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('operation','review','reference','out'):
        parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args(argv)
    try:
        result=run(args)
    except (ValueError,OSError,KeyError,TypeError) as error:
        parser.exit(2,'V14 factory rejected: '+str(error)+'\n')
    print(json.dumps(dict(status=result['status'],summary=result['summary']),sort_keys=True))
    return 3 if result['status']=='completed-incomplete' else 0


if __name__=='__main__':
    raise SystemExit(main())
