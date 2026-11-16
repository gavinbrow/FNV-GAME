"""Pure source-only V14 consumer draft; all actual artifact pins are unbound."""
from __future__ import annotations
import hashlib
import crt_v13_four_alias_contract as predecessor
import crt_v14_four_alias_plan as v14

PLAN='e832d09148559e859cb4358530407edb0be39fa678d5ad4e0c524dc587e2a7be'
REVIEW='e18ef6adc4c878240c4daad02e1d2fbaaed925a59740916ad298569d548f9e25'
RESPONSE='aaec970cae1dcf32699bda75317afbbcd4551c67252fca0d508d47eec997024a'

def validate(plan_bytes,review_bytes,response_bytes,fields,strong_definitions):
    """Keep the five-argument API and fail closed until actual V14 binding."""
    require=v14.require;old=v14.old;shared=predecessor.previous
    require(all(isinstance(h,str) and len(h)==64 and all(c in '0123456789abcdef' for c in h)
        for h in (PLAN,REVIEW,RESPONSE,v14.FULL_DIGEST)) and
        type(v14.COMPLETE_FIELDS) is int and type(v14.ALIAS_USE_COUNT) is int and
        isinstance(v14.ACTUAL_COHORT,dict) and v14.ACTUAL_COHORT['complete_field_count']==v14.COMPLETE_FIELDS,
        'V14 actual contract, complete cohort and review identities are unbound')
    plan=shared.previous.bound_json(plan_bytes,PLAN,'V14 contract')
    review=shared.previous.bound_json(review_bytes,REVIEW,'V14 contract review')
    require(isinstance(response_bytes,bytes) and hashlib.sha256(response_bytes).hexdigest()==RESPONSE,'V14 response differs')
    require(plan['kind']=='V14-existing-four-CRT-diagnostic-contract' and plan['scope']==v14.SCOPE and
        review['kind']=='V14-existing-four-CRT-contract-artifact-review' and
        review['status']=='approved-for-V14-diagnostic-successor-preparation' and review['reviewer'] and
        review['plan_sha256']==PLAN and review['response_sha256']==RESPONSE,'V14 exact scope/review differs')
    require(plan['complete_input_fields']==v14.COMPLETE_FIELDS and plan['selected_field_sha256']==v14.FULL_DIGEST and
        plan['alias_field_count']==v14.ALIAS_USE_COUNT and old.canonical(plan['actual_cohort'])==old.canonical(v14.ACTUAL_COHORT) and
        plan['own_sources']==v14.OWN_SOURCES and plan['old_raw_source_records_preserved'] is True and
        plan['unknown_flags_preserved'] is True and plan['requested_batch_assumed'] is False and plan['old_annotation_delta']==[] and
        plan['extra_fields']==55 and plan['new_current_CRT_uses']==2 and
        plan['unreviewed_new_CRT_aliases']==[], 'V14 complete fields or actual source scope differs')
    require(all(plan['qualified_UUID_evidence'][k] is False for k in ('base_closure_observed','full_serialization_eligible',
        'provider_selected','runtime_eligible','ABI_verified','UUID_selected_or_loaded','fresh_sdk_identity_verified')),
        'V14 qualified UUID negative metadata was promoted')
    require(all(plan[k] is False for k in ('native_operation_authorized','provider_adopted','runtime_ABI_approved','runtime_eligible')),
        'V14 has incompatible native/runtime claims')
    shared.previous.complete_fields(fields,v14.COMPLETE_FIELDS,v14.FULL_DIGEST)
    uses=shared.validate_bindings(plan['bindings'],fields,strong_definitions)
    require(sum(b['field_count'] for b in uses)==v14.ALIAS_USE_COUNT,'V14 all-canonical census differs')
    original=old.response([dict(canonical_undefined=old.undefined(b,r),normal_export=e)
        for b,r,e,k in old.BINDINGS]).replace('\n','\r\n').encode('ascii')
    expected=v14.response_bytes(plan['bindings'],original)
    enabled_count=sum(b['enabled'] for b in uses);enabled_fields=sum(b['field_count'] for b in uses if b['enabled'])
    require(response_bytes==expected and plan['response_text'].encode('ascii')==expected and
        plan['response_sha256']==RESPONSE and plan['enabled_alias_count']==enabled_count and
        plan['enabled_alias_field_count']==enabled_fields,'V14 enabled subset differs')
    return dict(scope=plan['scope'],plan_sha256=PLAN,review_sha256=REVIEW,response_sha256=RESPONSE,
        tokens=expected.decode('ascii').splitlines(),inherited_tokens_to_remove=original.decode('ascii').splitlines(),
        validated_bindings=uses,complete_input_fields=v14.COMPLETE_FIELDS,selected_field_sha256=v14.FULL_DIGEST,
        alias_field_count=v14.ALIAS_USE_COUNT,potential_alias_field_count=v14.ALIAS_USE_COUNT,
        enabled_alias_count=enabled_count,enabled_alias_field_count=enabled_fields,
        native_operation_authorized=False,provider_adopted=False,runtime_ABI_approved=False,runtime_eligible=False)
