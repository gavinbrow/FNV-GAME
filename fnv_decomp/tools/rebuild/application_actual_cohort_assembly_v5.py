"""Pure post-V14 successor assembly with fixed accepted baseline byte pins.

No I/O, native operation, admission, or runtime approval. The operation wrapper
must independently authenticate actual producer artifacts and peer reviews.
"""
import copy
import gzip
import hashlib
import json
import application_actual_cohort_semantic_v5 as semantic
import application_link_cohort as cohort
import application_actual_archive_bind_v1 as archive_bind
import application_link_diagnostic as diagnostic
import application_wave14_diagnostic as wave14

PINS = {'report':'d4cab73220949bf23edf3eba9a250c859ee3093f8a68fedf314fa0a994ca0544',
        'observation':'b6538d8aa9aff10826da60703500a7cc8b374d5efed6cced3e41debba7332185',
        'fields':'73a57a716b97cf116e625f2a585039a494b7d8a06293be5810672d229b211075'}


def require(ok, message):
    if not ok: raise ValueError(message)


def decode_baseline(blobs):
    require(type(blobs) is dict and set(blobs) == set(PINS) and
            all(type(blobs[k]) is bytes and hashlib.sha256(blobs[k]).hexdigest() == v for k,v in PINS.items()),
            'accepted V14 byte identities differ')
    report=json.loads(blobs['report']); observation=json.loads(blobs['observation'])
    fields=json.loads(gzip.decompress(blobs['fields']))
    require(type(fields) is list and len(fields)==46292 and
            cohort.digest(cohort.canonical(sorted(fields,key=cohort.canonical))) ==
            '08106a9552e9fe8fbe43a5bd224a212409b00228c26654432b715223eb0d6da4', 'baseline field identity differs')
    require(report['response_sha256']=='7fe58875f18f1bb542c151b4c3c62dc86903c5633a6ac9ef331028ac60ce26e6' and
            report['selected_game_function_provider_count']==14555 and
            report['full_included_field_count']==len(fields) and
            all(report[k] is False for k in ('provider_adopted','provider_selected','runtime_eligible','link_ready')),
            'baseline report scope differs')
    providers,noncode=wave14._baseline_namespace(report,observation,diagnostic,cohort,14555)
    return report,observation,fields,providers,noncode


def assemble(*, baseline_bytes, semantic_inputs, archive_bytes, archive_sha256):
    report,observation,old_fields,old_providers,noncode=decode_baseline(baseline_bytes)
    archive=archive_bind.bind(archive_bytes=archive_bytes, archive_sha256=archive_sha256,
        members=semantic_inputs['members'], member_count=semantic_inputs['member_count'],
        member_bytes=semantic_inputs['member_bytes'])
    derived=semantic.derive(**semantic_inputs)
    namespace=cohort.disjoint_providers([derived['providers']], baseline_providers=old_providers,
                                        existing_noncode_definitions=noncode)
    result=copy.deepcopy(report)
    for provider in derived['providers']:
        result['provenance'].setdefault(provider['canonical'],[]).append(copy.deepcopy(provider))
    for field in derived['fields']:
        result['provenance'].setdefault(field['canonical'],[]).append(copy.deepcopy(field))
    result['selected_supplementary_providers'].extend(copy.deepcopy(derived['providers']))
    result['successor_namespace']=namespace
    result['selected_game_function_provider_count']=len(old_providers)+len(derived['providers'])
    result['full_included_field_count']=len(old_fields)+len(derived['fields'])
    result['kind']='post-v14-actual-cohort-source-assembly-v5'
    result['status']='derived-not-adopted'
    result['provider_adopted']=result['provider_selected']=result['runtime_eligible']=result['link_ready']=False
    result['native_LINK_performed']=result['executable_execution']=False
    # Existing keys including unknown annotations, quarantine and UUID evidence
    # remain untouched except the explicitly updated fields above.
    return dict(report=result, fields=old_fields+derived['fields'], providers=old_providers+derived['providers'],
                baseline_observation=observation, archive=archive, admission_approved=False, link_approved=False)
