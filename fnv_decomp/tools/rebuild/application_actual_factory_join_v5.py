"""Saved V14 factory outcome reconciliation for an actual emitted subset.

No original reads, comparisons or native calls: this validates saved evidence
and reuses the factory's own selection and original field-wrapper constructors.
Origin, exact producer identities and independent outcome review are external.
"""
import cached_frontier_code_factory_v14 as factory
import cached_frontier_code_factory_v14_driver as driver
import application_link_cohort as cohort


def require(ok,message):
    if not ok: raise ValueError(message)


def exact(a,b):
    return cohort.canonical(a)==cohort.canonical(b)


def validate(*, selections, outcomes, emitted, members, wrappers, member_bytes):
    summary=driver.reconcile_outcomes(selections,outcomes)
    require(type(emitted) is list and len(emitted)==summary['emitted'] and
            type(members) is list and type(wrappers) is list and
            len(members)==len(wrappers)==len(emitted) and type(member_bytes) is dict,
            'actual emitted evidence census differs')
    selected={s['root']['original_address']:s for s in selections}
    emitted_roots=[o['root']['original_address'] for o in outcomes if o['status']=='emitted']
    require(len(set(emitted_roots))==len(emitted_roots) and
            set(emitted_roots)=={x['root']['original_address'] for x in emitted}, 'terminal emitted subset differs')
    seen=set()
    for entry,member,wrapper in zip(emitted,members,wrappers):
        root=entry['root']; address=root['original_address'];selection=selected[address]
        require(address not in seen and exact(root,selection['root']), 'duplicate or changed emitted root');seen.add(address)
        record=entry['record']; projection=member['projection']; assessment=entry['assessment'];name=member['name']
        factory.validate_selected(record,selection)
        require(exact(entry['projection'],projection) and name in member_bytes and
                type(member_bytes[name]) is bytes and cohort.digest(member_bytes[name])==projection['output_sha256'],
                'saved projection/member byte identity differs')
        expected=driver.field_proof_record(name,record,selection,projection,member_bytes[name])
        require(exact(expected,wrapper), 'factory original field wrapper differs')
        contract=record['contract']; require(len(projection['fields'])==len(contract['fields']), 'complete field census differs')
        if contract['fields']:
            require(assessment.get('eligible') is True and assessment.get('blockers') == [] and
                    assessment.get('serialization_performed') is False and
                    all(assessment.get(k) is False for k in ('provider_selected','runtime_eligible','ABI_verified',
                        'link_ready','native_tools_run','compiler_performed','executable_link_performed','game_execution_performed')) and
                    exact(assessment['fields'],projection['fields']) and
                    exact(assessment['exports'],projection['exports']), 'saved assessment differs from projection')
        else:
            require(type(assessment) is dict and set(assessment)=={'eligible','blockers','strict_zero_consumer_replayed',
                    'serialization_performed','requested_roots','contract_identity_sha256','certificate_sha256'} and
                    assessment.get('eligible') is True and assessment.get('blockers') == [] and
                    assessment.get('serialization_performed') is False and
                    assessment.get('strict_zero_consumer_replayed') is True and
                    exact(assessment.get('requested_roots'),[root]) and
                    assessment.get('contract_identity_sha256') == selection['authority']['contract_identity_sha256'] and
                    assessment.get('certificate_sha256') == selection['authority']['certificate_sha256'],
                    'zero-field strict consumer evidence missing')
        for key,name_expected in (('before_comparison',root['symbol']),('after_comparison',projection['exports'][0])):
            reports=projection[key]
            require(type(reports) is list and len(reports)==1, 'one full saved comparison required')
            r=reports[0]
            require(r['verdict']=='match' and r['address']==address and r['symbol']==name_expected and
                    type(r['size']) is int and type(r['compiled_extent']) is int and
                    r['size']==r['compiled_extent']==root['size'] and not r['errors'] and
                    not r.get('byte_differences',[]) and len(r['relocations'])==len(contract['fields']) and
                    all(x['match'] is True and x['expected']==x['observed'] for x in r['relocations']),
                    'saved full plain comparison differs')
            expected_fields=[]
            for field in contract['fields']:
                cr=field['coff_relocation']; off=field['source_field_offset']; kind=cr['kind']; target=field['expected_original_target_va']
                require(type(off) is int and type(kind) is int and kind in (6,20) and type(target) is str,
                        'typed original field geometry required')
                expected_fields.append((off,kind,target))
            actual_fields=[]
            for relocation in r['relocations']:
                require(type(relocation['offset']) is int and type(relocation['kind']) is int and
                        type(relocation['expected']) is str and type(relocation['observed']) is str,
                        'typed comparison relocation required')
                actual_fields.append((relocation['offset'],relocation['kind'],relocation['expected']))
            require(len(set(expected_fields))==len(expected_fields) and sorted(actual_fields)==sorted(expected_fields),
                    'saved comparison field geometry/target differs from contract')
    require(set(member_bytes)=={m['name'] for m in members}, 'foreign member bytes')
    return dict(summary=summary, emitted_roots=emitted_roots, saved_evidence_only=True,
                admission_approved=False, link_approved=False)
