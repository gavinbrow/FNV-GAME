"""Derive a private V14 saved-11 partial handoff from reviewed metadata only.

This does not open saved objects, reports, original inputs or archives; it does
not select a provider or authorize assembly, linking, runtime or admission.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
INPUTS={
 'operation':('build/rebuild/v14-v3-saved11-validation-operation-v1.json','b9fcbbdee3f3ce18231665a2ad0ebb2941cd232d07b3a7913607cbd87f660488'),
 'saved_hash_evidence':('build/rebuild/v14-v3-salvage-feasibility-v1/saved-hash-check.json','3d4aca1dd3a6fce9de13006aa7d0e159c31cae35037980dff58c946263038f3f'),
 'failure_review':('build/rebuild/v14-v3-failed-outcome-independent-v1/review.json','a27d9a801a2027b8a47542381f71ae94e6008c364e2593c26ba7f2264ad00fc7'),
 'main_review':('build/rebuild/v14-saved11-outcome-independent-v1/review.json','131791b0821ab32a7dd1876a61544cccbb5e153a4ca6a086ca44a92af538284e'),
 'complement_review':('build/rebuild/v14-saved11-complement-outcome-v1/independent-outcome-review-v1.json','161b76cdeb6c09ba62ee15f777fd4939c6da4aeed10805043cba64df691460ff'),
 'validation_receipt':('build/rebuild/v14-v3-saved11-validation-v1/receipt.json','62a94ee04a04ce0edf8a90824dce14d8280182ce83ec1937d00ae72c37c5986d'),
 'host_terminal':('build/rebuild/v14-saved11-host-v1/control-v1/terminal.json','3a54607d7d6a62e0bece1f6ef9756065607a58f03c7702b455eb49adfc741725'),
 'observation_review':('build/rebuild/terra-v14-complement-review-v1/review.json','bd38122d730e6972d9695454768d7b714426060e52287b1e311e75d249172f5a'),
}
OUT=ROOT/'build/rebuild/v14-saved11-partial-handoff-v1.json'
EXCLUDED={'quarantined':['0x0048e140'],'inflight_unknown':['0x00484da0'],'unstarted':['0x00484d60','0x0076b610']}


def derive(operation,evidence,failure,main,peer,receipt,terminal,observation):
    if (operation['kind']!='v14-saved11-fresh-validation-proposal' or operation['new_object_emission'] is not False or
            operation['prior_batch_replay'] is not False or operation['prior_match_inferred'] is not False or
            operation['exclusions']!=EXCLUDED or failure['status']!='failed-quarantined-no-replay' or
            failure['replay_authorized'] is not False):
        raise ValueError('exact failed-V3 and 11-only scope required')
    if (main['status']!='accepted-fresh-saved-validation-only-not-provider-or-runtime-admission' or
            main['operation_sha256']!=INPUTS['operation'][1] or main['receipt_sha256']!=INPUTS['validation_receipt'][1] or
            main['complement_review_sha256']!=INPUTS['complement_review'][1] or
            main['host_terminal_sha256']!=INPUTS['host_terminal'][1] or
            peer['approved'] is not True or peer['operation_sha256']!=INPUTS['operation'][1] or
            peer['receipt_sha256']!=INPUTS['validation_receipt'][1] or peer['host_terminal_sha256']!=INPUTS['host_terminal'][1] or
            peer['provider_selected'] is not False or peer['runtime_eligible'] is not False):
        raise ValueError('both independently reviewed saved outcomes required')
    counts=main['counts']
    if (any(type(counts[k]) is not int for k in ('roots','before_match_reports','after_match_reports','field_rows','unique_field_facts','relocation_match_observations','excluded_roots')) or
            [counts[k] for k in ('roots','before_match_reports','after_match_reports','field_rows','unique_field_facts','relocation_match_observations','excluded_roots')] != [11,11,11,22,22,44,4]):
        raise ValueError('reviewed saved-outcome census differs')
    if (receipt['kind']!='v14-saved11-validation-receipt' or receipt['status']!='validated-unreviewed' or
            receipt['operation_sha256']!=INPUTS['operation'][1] or receipt['validated']!=11 or
            receipt['full_field_proof_records']!=11 or receipt['input_stability'] is not True or
            any(receipt[k] is not False for k in ('canonical_index_checked','function_index_present','excluded_member_payloads_accessed',
                'new_object_emission','prior_batch_replay','prior_match_inferred','provider_selected','runtime_eligible','standalone_receipt_admission')) or
            terminal['status']!='completed-unreviewed' or terminal['runner_receipt_sha256']!=INPUTS['validation_receipt'][1] or
            terminal['provider_selected'] is not False or terminal['runtime_eligible'] is not False):
        raise ValueError('saved validation or host terminal differs')
    if peer['reports_sha256']!=receipt['output_sha256']['reports.jsonl.gz']:
        raise ValueError('reviewed report binding differs')
    members=operation['members'];saved=evidence['verified_members'];by_address={r['root']['original_address']:r for r in observation['positive_singletons']}
    if len(members)!=11 or len(saved)!=11 or len(by_address)!=15:
        raise ValueError('complete reviewed 11/15 roster required')
    result=[];seen=set()
    for row,prior in zip(members,saved):
        root=row['root'];address=root['original_address'];member=row['saved_member']
        if (address in seen or address not in by_address or prior['address']!=address or
                {k:prior[k] for k in ('name','sha256','bytes')}!=member or by_address[address]['root']!=root or
                not re.fullmatch(r'CACHED-CODE-[0-9]{3}-[0-9a-f]{8}\.obj',member['name']) or member['name'][-12:-4]!=address[2:]):
            raise ValueError('root/member/native ancestry differs')
        source=by_address[address];seen.add(address)
        result.append({'root':root,'saved_object':dict(path='build/rebuild/cached-frontier-code-v14-v3/'+member['name'],
            sha256=member['sha256'],bytes=member['bytes']),'observation_ordinal':source['ordinal'],
            'observation_record_sha256':source['record_sha256'],'certificate_sha256':source['certificate_sha256'],
            'contract_identity_sha256':source['contract_identity_sha256'],'validation_status':'fresh-original-and-saved-match-reviewed'})
    if receipt['validated_addresses']!=[row['root']['original_address'] for row in result] or seen & set(sum(EXCLUDED.values(),[])):
        raise ValueError('validation roster or excluded-root scope differs')
    return {'schema_version':1,'kind':'v14-saved11-partial-evidence-handoff','status':'pending-independent-handoff-review-not-admission',
        'members':result,'exclusions':EXCLUDED,'operation_sha256':INPUTS['operation'][1],
        'validation_receipt_sha256':INPUTS['validation_receipt'][1],'host_terminal_sha256':INPUTS['host_terminal'][1],
        'main_outcome_review_sha256':INPUTS['main_review'][1],'complement_outcome_review_sha256':INPUTS['complement_review'][1],
        'reports_sha256':receipt['output_sha256']['reports.jsonl.gz'],'progress_sha256':receipt['output_sha256']['progress.jsonl'],
        'counts':counts,'function_index_present':False,'canonical_index_checked':False,'previous_v3_failure_preserved':True,
        'prior_inflight_unknown_resolved':False,'new_object_emission':False,'archive_created':False,'provider_selected':False,
        'ABI_verified':False,'runtime_eligible':False,'admission_decision_created':False,
        'handoff_review_required':True,
        'not_retained':['reconstructed projection section/symbol/auxiliary maps','complete exports/directives/EH and SafeSEH metadata',
                        'complete original certificate/contract bodies in handoff','archive and independent native archive conformance'],
        'prerequisites':['independent review of this exact handoff and reviewed saved outcomes',
            'fresh exact source/member identity rechecks before any downstream use',
            'separately reviewed recovery of missing projection/namespace evidence without uncertain-root replay',
            'if an archive is built, exact member/index integrity and independent native conformance',
            'separate namespace/provider/ABI/runtime and link-specific gates'],
        'limitations':['Saved claims were independently reviewed, not re-run in this handoff.',
            'No saved object, report body, original/reference payload or archive was opened during derivation.',
            'Canonical function-index spans were not checked; exact retained spans and before/after compiled extents were checked in the new validation.',
            'The failed V3 attempt and its inflight unknown remain quarantined; this handoff does not resolve or replay them.']}


def run():
    if OUT.exists() or OUT.is_symlink():raise FileExistsError('exclusive handoff already exists')
    values={}
    for name,(relative,expected) in INPUTS.items():
        with (ROOT/relative).open('rb') as stream:raw=stream.read(16*1024*1024+1)
        if len(raw)>16*1024*1024 or hashlib.sha256(raw).hexdigest()!=expected:
            raise ValueError('metadata hash differs: '+name)
        values[name]=json.loads(raw)
    result=derive(values['operation'],values['saved_hash_evidence'],values['failure_review'],values['main_review'],
        values['complement_review'],values['validation_receipt'],values['host_terminal'],values['observation_review'])
    data=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode()
    with OUT.open('xb') as stream:stream.write(data);stream.flush();os.fsync(stream.fileno())
    return result


if __name__=='__main__':run()
