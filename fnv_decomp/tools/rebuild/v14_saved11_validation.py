"""V14 saved-11 validation core; no production entry or object-file writes.

These helpers do not grant access to any saved object, source or reference. A
separately reviewed operation, held watchdog and fresh lease must authenticate
all inputs before a future execution calls them. Earlier V3 remains quarantined.
"""
from __future__ import annotations
import hashlib
import re
from pathlib import Path

EXPECTED_COUNT=11
FORBIDDEN={'0x0048e140','0x00484da0','0x00484d60','0x0076b610'}


def _equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(_equal(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(_equal(x,y) for x,y in zip(a,b))
    return a==b


def validate_scope(operation,evidence,positive):
    """Join exactly the 11 hash-only saved identities to original root metadata."""
    if (type(operation) is not dict or operation.get('kind')!='v14-saved11-fresh-validation-proposal' or
            operation.get('status')!='owner-authorized-finite-work-awaiting-reviewed-gates-and-fresh-lease' or
            operation.get('in_memory_reconstruction_authorized') is not True or
            any(operation.get(k) is not False for k in ('new_object_emission','prior_batch_replay','prior_match_inferred','provider_selected','runtime_eligible'))):
        raise ValueError('exact finite non-emitting scope required')
    members=operation['members']; recorded=evidence['verified_members']; roots=positive['roots']
    if type(members) is not list or type(recorded) is not list or type(roots) is not list or len(members)!=EXPECTED_COUNT or len(recorded)!=EXPECTED_COUNT or len(roots)!=15:
        raise ValueError('complete original and saved census required')
    known={r['original_address']:r for r in roots}
    if len(known)!=15:raise ValueError('duplicate original roots')
    seen=set()
    for row,prior in zip(members,recorded):
        if type(row) is not dict or set(row)!={'root','saved_member'}:raise ValueError('exact member schema')
        root=row['root'];address=root['original_address']; saved=row['saved_member']
        if (address in seen or address in FORBIDDEN or address not in known or not _equal(root,known[address]) or
                type(saved) is not dict or set(saved)!={'name','sha256','bytes'} or
                not _equal(saved,{k:prior[k] for k in ('name','sha256','bytes')}) or prior['address']!=address or
                type(saved['name']) is not str or not re.fullmatch(r'CACHED-CODE-[0-9]{3}-[0-9a-f]{8}\.obj',saved['name']) or
                saved['name'][-12:-4]!=address[2:] or
                type(saved['bytes']) is not int or not 0<saved['bytes']<=16*1024*1024 or
                type(saved['sha256']) is not str or len(saved['sha256'])!=64 or
                any(c not in '0123456789abcdef' for c in saved['sha256'])):
            raise ValueError('saved root/member identity differs')
        seen.add(address)
    excluded=operation['exclusions']
    if (not _equal(excluded,{'quarantined':['0x0048e140'],'inflight_unknown':['0x00484da0'],
                             'unstarted':['0x00484d60','0x0076b610']}) or
            set(known)-seen!=FORBIDDEN):
        raise ValueError('excluded V3 roots must remain outside validation')
    return True


def verify_saved_member(row, record, selection, raw, saved, providers, exports,
                        original_path, saved_path, pe, unit, retained_proof, snapshot, highlow):
    """Fresh no-write reconstruction, byte equality, field audit and two MATCHes.

    Caller must already have authenticated all path/source/original/reference
    inputs, exact selection and stable files under the reviewed guardian. This
    function never writes or replaces a member; integrity or policy failures
    raise and must quarantine the entire new validation operation.
    """
    import cached_frontier_code_factory_v14 as selection_core
    import cached_frontier_code_factory_v13 as v13
    import cached_frontier_code_factory_v14_driver as driver
    import cached_root_observe_v14 as native
    driver._require_absent_index(v13.ROOT/'build/function_index.json')
    selection_core.validate_selected(record,selection)
    root=row['root']; member=row['saved_member']; contract=record['contract']; certificate=record['certificate']
    native.validate_roots(unit,retained_proof,[root])
    if (not _equal(contract['unit_verified_functions'],retained_proof['verified_functions']) or
            contract['provenance']['recipe_unit_sha256']!=retained_proof['recipe_unit_sha256']):
        raise ValueError('full retained source proof differs')
    if (not _equal(root,selection['root']) or root['original_address'] in FORBIDDEN or
            Path(saved_path).name!=member['name'] or type(raw) is not bytes or type(saved) is not bytes or
            not 0<len(raw)<=16*1024*1024 or len(saved)!=member['bytes'] or
            hashlib.sha256(raw).hexdigest()!=root['object_sha256'] or
            hashlib.sha256(saved).hexdigest()!=member['sha256'] or len(highlow)!=351931):
        raise ValueError('fresh physical identities or HIGHLOW census differ')
    facts=v13.audit.audit_original_fields(snapshot,highlow,contract['fields'])
    if contract['fields']:
        assessment=v13.frozen.fields.core.assess_member(raw,contract,certificate,[root],providers,existing_exports=exports)
        if assessment['eligible'] is not True:
            raise ValueError('saved member no longer satisfies supported field policy')
        reconstructed,projection=v13.frozen.fields.core.project_member(raw,contract,certificate,[root],providers,existing_exports=exports)
        if not _equal(projection['fields'],assessment['fields']) or not _equal(projection['exports'],assessment['exports']):
            raise ValueError('independent field classification differs')
    else:
        identity={k:root[k] for k in ('recipe_id','object_sha256','symbol_index')}
        if v13.base.pool.canonical(identity) in exports or not _equal(providers[root['original_address']],identity):
            raise ValueError('zero-field physical namespace differs')
        reconstructed,projection=v13.base.project_member(raw,contract,certificate,[root])
        projection.update(fields=[],comparison_base_view={})
    if reconstructed!=saved or projection['output_sha256']!=member['sha256']:
        raise ValueError('saved member differs from fresh in-memory reconstruction')
    v13.base.bulk.strict_reparse(Path(saved_path),saved)
    contracts=[dict(selected={k:root[k] for k in v13.base.NATIVE_KEYS})]
    before=v13.base.bulk.compare_functions(original_path,pe,contracts,unit['recipe'])
    plan=dict(bindings=projection['namespace_bindings'],comparison_base_view=projection['comparison_base_view'])
    after=v13.base.bulk.compare_functions(saved_path,pe,contracts,unit['recipe'],plan)
    for reports,name in ((before,root['symbol']),(after,projection['exports'][0])):
        if type(reports) is not list or len(reports)!=1:raise ValueError('one full comparison required')
        report=reports[0]
        if not (report['verdict']=='match' and report['address']==root['original_address'] and report['symbol']==name and
                type(report['size']) is int and type(report['compiled_extent']) is int and
                report['size']==report['compiled_extent']==root['size'] and not report['errors'] and
                not report.get('byte_differences',[]) and len(report['relocations'])==len(contract['fields']) and
                all(r['match'] is True and r['expected']==r['observed'] for r in report['relocations'])):
            raise ValueError('fresh full original/staged comparison required')
    if len(projection['fields'])!=len(contract['fields']):raise ValueError('complete field proof required')
    projection.update(before_comparison=before,after_comparison=after,authority=selection['authority'],
        central_record_sha256=v13.digest(record),native_observation_record_sha256=v13.digest(record),
        qualified_metadata_row_sha256=record['qualified_metadata_row_sha256'])
    full=driver.field_proof_record(member['name'],record,selection,projection,saved)
    driver._require_absent_index(v13.ROOT/'build/function_index.json')
    return dict(root=root,saved_member=member,before_comparison=before,after_comparison=after,
        full_field_proof=full,field_facts=facts,in_memory_equality=True,
        function_index_present=False,canonical_index_checked=False,
        prior_match_inferred=False,new_object_emission=False,provider_selected=False,runtime_eligible=False)


def run(*_args,**_kwargs):
    raise ValueError('saved-11 production authority, guardian and reviewed driver remain unbound')
