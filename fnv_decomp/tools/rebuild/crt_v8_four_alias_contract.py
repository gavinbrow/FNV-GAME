"""Pure V8 existing-four gate; no file, native, object, image or process API."""
from __future__ import annotations
import hashlib

import crt_frontier_adoption_contract as previous
import crt_v8_four_alias_plan as v8

PLAN='aeedc2d33a0aadc040582ee734e2a25208cc30f7d3ec969f2e63e56879b82c0c'
REVIEW='fef8b2cf07f3e138e8f09f6911440c114882acbc1a9a5b0fcf8c26672b86915d'
RESPONSE='aaec970cae1dcf32699bda75317afbbcd4551c67252fca0d508d47eec997024a'
COMPLETE_FIELDS=45315
POTENTIAL_FIELDS=202

def validate(plan_bytes,review_bytes,response_bytes,fields,strong_definitions):
    """Return a reviewed subset and explicit inherited-token removal policy.

    The caller still owns complete actual native-input observation, live
    source/input rehashing, controlled normal LIBCMT selection and the separate
    diagnostic operation gate. Runtime approval is never returned here.
    """
    require=v8.require;old=v8.old
    plan=previous.previous.bound_json(plan_bytes,PLAN,'V8 contract')
    review=previous.previous.bound_json(review_bytes,REVIEW,'V8 contract review')
    require(isinstance(response_bytes,bytes) and hashlib.sha256(response_bytes).hexdigest()==RESPONSE,
        'V8 response identity differs')
    require(plan['kind']=='V8-existing-four-CRT-diagnostic-contract' and
        review['kind']=='V8-existing-four-CRT-contract-artifact-review' and
        review['status']=='approved-for-V8-diagnostic-successor-preparation' and review['reviewer'] and
        review['plan_sha256']==PLAN and review['response_sha256']==RESPONSE,'review does not cover exact V8 contract')
    require(plan['scope']=='V7-plus-CODE59-ModelLoader' and plan['complete_input_fields']==COMPLETE_FIELDS and
        plan['selected_field_sha256']==v8.FULL_DIGEST and plan['alias_field_count']==POTENTIAL_FIELDS and
        plan['own_sources']==v8.OWN_SOURCES and plan['old_raw_source_records_preserved'] is True and
        plan['old_annotation_delta']==[] and plan['generated_and_ordinary_proofs_remain_distinct'] is True and
        plan['unreviewed_new_CRT_aliases']==[], 'V8 source/cohort/proof/alias scope differs')
    require(all(plan[k] is False for k in ('native_operation_authorized','provider_adopted','runtime_ABI_approved','runtime_eligible')),
        'V8 contract has incompatible native/runtime claim')
    previous.previous.complete_fields(fields,COMPLETE_FIELDS,v8.FULL_DIGEST)
    uses=previous.validate_bindings(plan['bindings'],fields,strong_definitions)
    require(sum(b['field_count'] for b in uses)==POTENTIAL_FIELDS,'V8 complete potential use census differs')
    original=old.response([dict(canonical_undefined=old.undefined(b,r),normal_export=e)
        for b,r,e,k in old.BINDINGS]).replace('\n','\r\n').encode('ascii')
    expected=v8.prior.response_bytes(plan['bindings'],original)
    enabled_fields=sum(b['field_count'] for b in uses if b['enabled'])
    enabled_count=sum(b['enabled'] for b in uses)
    require(response_bytes==expected and plan['response_text'].encode('ascii')==expected and
        plan['response_sha256']==RESPONSE and plan['enabled_alias_count']==enabled_count and
        plan['enabled_alias_field_count']==enabled_fields,'V8 enabled subset/response differs')
    return dict(scope=plan['scope'],plan_sha256=PLAN,review_sha256=REVIEW,response_sha256=RESPONSE,
        tokens=expected.decode('ascii').splitlines(),inherited_tokens_to_remove=original.decode('ascii').splitlines(),
        response_application='remove all four exact inherited CRT tokens before applying enabled subset',
        validated_bindings=uses,complete_input_fields=COMPLETE_FIELDS,selected_field_sha256=v8.FULL_DIGEST,
        alias_field_count=POTENTIAL_FIELDS,potential_alias_field_count=POTENTIAL_FIELDS,
        enabled_alias_count=enabled_count,enabled_alias_field_count=enabled_fields,
        ordinary_and_generated_EH_proofs_remain_distinct=True,native_operation_authorized=False,
        provider_adopted=False,runtime_ABI_approved=False,runtime_eligible=False,
        remaining='actual V8 prepared input/source review and diagnostic operation delegation')
