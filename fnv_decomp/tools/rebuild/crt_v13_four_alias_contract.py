"""Pure V13 existing-four gate; no file, native, object, image or process API."""
from __future__ import annotations
import hashlib

import crt_frontier_adoption_contract as previous
import crt_v13_four_alias_plan as v13

PLAN='d47b3b0efe542808e1fc22481da41888f6daa11d3d6c928279e397344dec5721'
REVIEW='d020b039377efe24821028b8d4c667f9953ce2116db0bb52871966e652e87b27'
RESPONSE='aaec970cae1dcf32699bda75317afbbcd4551c67252fca0d508d47eec997024a'
COMPLETE_FIELDS=46237
POTENTIAL_FIELDS=202

def validate(plan_bytes,review_bytes,response_bytes,fields,strong_definitions):
    """Return only the reviewed existing subset and inherited-token removal."""
    require=v13.require;old=v13.old
    plan=previous.previous.bound_json(plan_bytes,PLAN,'V13 contract')
    review=previous.previous.bound_json(review_bytes,REVIEW,'V13 contract review')
    require(isinstance(response_bytes,bytes) and hashlib.sha256(response_bytes).hexdigest()==RESPONSE,
        'V13 response identity differs')
    require(plan['kind']=='V13-existing-four-CRT-diagnostic-contract' and
        review['kind']=='V13-existing-four-CRT-contract-artifact-review' and
        review['status']=='approved-for-V13-diagnostic-successor-preparation' and review['reviewer'] and
        review['plan_sha256']==PLAN and review['response_sha256']==RESPONSE,'review does not cover exact V13 contract')
    require(plan['scope']=='V12-plus-CODE56' and plan['complete_input_fields']==COMPLETE_FIELDS and
        plan['selected_field_sha256']==v13.FULL_DIGEST and plan['alias_field_count']==POTENTIAL_FIELDS and
        plan['own_sources']==v13.OWN_SOURCES and plan['old_raw_source_records_preserved'] is True and
        plan['old_annotation_delta']==[] and plan['generated_and_ordinary_proofs_remain_distinct'] is True and
        plan['unreviewed_new_CRT_aliases']==[] and plan['extra_fields']==290 and plan['normative_source_evidence_enriched'] is False and
        plan['new_fields_use_existing_CRT_aliases'] is False and plan['new_current_CRT_uses']==0 and
        plan['inherited_binding_evidence_scope']=='V7-plus-CODE59-ModelLoader','V13 source/cohort/proof/alias scope differs')
    require(all(plan[k] is False for k in ('native_operation_authorized','provider_adopted','runtime_ABI_approved','runtime_eligible')),
        'V13 contract has incompatible native/runtime claim')
    previous.previous.complete_fields(fields,COMPLETE_FIELDS,v13.FULL_DIGEST)
    uses=previous.validate_bindings(plan['bindings'],fields,strong_definitions)
    require(sum(b['field_count'] for b in uses)==POTENTIAL_FIELDS,'V13 complete potential use census differs')
    original=old.response([dict(canonical_undefined=old.undefined(b,r),normal_export=e)
        for b,r,e,k in old.BINDINGS]).replace('\n','\r\n').encode('ascii')
    expected=v13.base.v9.v8.prior.response_bytes(plan['bindings'],original)
    enabled_fields=sum(b['field_count'] for b in uses if b['enabled'])
    enabled_count=sum(b['enabled'] for b in uses)
    require(response_bytes==expected and plan['response_text'].encode('ascii')==expected and
        plan['response_sha256']==RESPONSE and plan['enabled_alias_count']==enabled_count and
        plan['enabled_alias_field_count']==enabled_fields,'V13 enabled subset/response differs')
    return dict(scope=plan['scope'],plan_sha256=PLAN,review_sha256=REVIEW,response_sha256=RESPONSE,
        tokens=expected.decode('ascii').splitlines(),inherited_tokens_to_remove=original.decode('ascii').splitlines(),
        response_application='remove all four exact inherited CRT tokens before applying enabled subset',
        validated_bindings=uses,complete_input_fields=COMPLETE_FIELDS,selected_field_sha256=v13.FULL_DIGEST,
        alias_field_count=POTENTIAL_FIELDS,potential_alias_field_count=POTENTIAL_FIELDS,
        enabled_alias_count=enabled_count,enabled_alias_field_count=enabled_fields,
        ordinary_and_generated_EH_proofs_remain_distinct=True,native_operation_authorized=False,
        provider_adopted=False,runtime_ABI_approved=False,runtime_eligible=False,
        remaining='actual V13 prepared input/source review and diagnostic operation delegation')
