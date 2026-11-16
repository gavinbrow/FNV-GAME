"""Pure gate for the separately reviewed 44,540-field four-alias successor.

No file access, native tools, object parsing or execution. The exact immutable
contract, artifact review and response are separate from the caller's actual
prepared-input review and root's native operation delegation.
"""
from __future__ import annotations
import hashlib

import crt_adoption_consumer_contract as previous
import crt_frontier_adoption_plan as frontier

PLAN='1baadbcd376c2e03dba219558eac940ed50e970cf8e5b12391a4969f336f6e21'
REVIEW='8cb0711700c68e799700324de725566991ef7366881190224a77ef3c2aa27357'
RESPONSE='aaec970cae1dcf32699bda75317afbbcd4551c67252fca0d508d47eec997024a'
COMPLETE_FIELDS=44540
POTENTIAL_ALIAS_FIELDS=198

def validate_bindings(bindings,fields,strong_definitions):
    require=frontier.require;old=frontier.old
    expected={(b,r):(e,k) for b,r,e,k in old.BINDINGS}
    require(len(bindings)==4 and {(b['original_base'],b['role']) for b in bindings}==set(expected),
        'not the existing four role-keyed bindings')
    require(isinstance(strong_definitions,(dict,set,list,tuple)), 'explicit strong definition names required')
    strong=set(strong_definitions);result=[]
    for b in bindings:
        base,role=b['original_base'],b['role'];export,kind=expected[(base,role)];name=old.undefined(base,role)
        require(b['canonical_undefined']==name and b['normal_export']==export and type(b['enabled']) is bool,
            'canonical export or enabled policy differs')
        uses=old.census(fields,base,role,kind)
        require(uses==b['fields'] and len(uses)==b['field_count'] and old.digest(uses)==b['field_census_sha256'],
            'complete canonical use/source identities differ')
        if b['enabled']:require(name not in strong,'strong definition supersedes enabled alternate name')
        result.append(dict(canonical_undefined=name,normal_export=export,enabled=b['enabled'],
            field_count=len(uses),field_census_sha256=old.digest(uses)))
    # The source-reviewed policy forbids a half-enabled cookie/state owner.
    states={b['canonical_undefined']:b['enabled'] for b in bindings}
    require(len({states[n] for n in frontier.COOKIE_NAMES})==1,'partial cookie owner pair')
    return result

def validate(plan_bytes,review_bytes,response_bytes,fields,strong_definitions):
    require=frontier.require
    plan=previous.bound_json(plan_bytes,PLAN,'expanded contract')
    review=previous.bound_json(review_bytes,REVIEW,'expanded contract review')
    require(isinstance(response_bytes,bytes) and hashlib.sha256(response_bytes).hexdigest()==RESPONSE,
        'expanded response identity differs')
    require(plan['kind']=='expanded-four-CRT-diagnostic-contract' and
        review['kind']=='expanded-four-CRT-contract-artifact-review' and
        review['status']=='approved-for-expanded-diagnostic-successor-preparation' and review['reviewer'] and
        review['plan_sha256']==PLAN and review['response_sha256']==RESPONSE,
        'review does not bind this separate successor')
    require(plan['scope']=='V6-plus-first3-CODE12-EHFile' and plan['complete_input_fields']==COMPLETE_FIELDS and
        plan['selected_field_sha256']==frontier.FULL_DIGEST and plan['alias_field_count']==POTENTIAL_ALIAS_FIELDS and
        plan['generated_EH_proof_remains_distinct'] is True and plan['unreviewed_new_CRT_aliases']==[],
        'expanded component, proof or alias scope differs')
    require(all(plan[k] is False for k in ('native_operation_authorized','provider_adopted','runtime_ABI_approved','runtime_eligible')),
        'incompatible native or runtime claim')
    previous.complete_fields(fields,COMPLETE_FIELDS,frontier.FULL_DIGEST)
    uses=validate_bindings(plan['bindings'],fields,strong_definitions)
    require(sum(b['field_count'] for b in uses)==POTENTIAL_ALIAS_FIELDS,'complete potential alias field count differs')
    original=frontier.old.response([dict(canonical_undefined=frontier.old.undefined(b,r),normal_export=e)
        for b,r,e,k in frontier.old.BINDINGS]).replace('\n','\r\n').encode('ascii')
    expected=frontier.response_bytes(plan['bindings'],original)
    require(response_bytes==expected and plan['response_text'].encode('ascii')==expected and
        plan['response_sha256']==RESPONSE and plan['enabled_alias_count']==sum(b['enabled'] for b in uses),
        'enabled existing response tokens differ')
    return dict(scope=plan['scope'],plan_sha256=PLAN,review_sha256=REVIEW,response_sha256=RESPONSE,
        tokens=expected.decode('ascii').splitlines(),validated_bindings=uses,
        inherited_tokens_to_remove=original.decode('ascii').splitlines(),
        response_application='remove all four exact inherited CRT tokens before appending enabled tokens',
        complete_input_fields=COMPLETE_FIELDS,selected_field_sha256=frontier.FULL_DIGEST,
        alias_field_count=POTENTIAL_ALIAS_FIELDS,potential_alias_field_count=POTENTIAL_ALIAS_FIELDS,
        enabled_alias_count=sum(b['enabled'] for b in uses),
        enabled_alias_field_count=sum(b['field_count'] for b in uses if b['enabled']),
        generated_EH_proof_remains_distinct=True,native_operation_authorized=False,
        provider_adopted=False,runtime_ABI_approved=False,runtime_eligible=False,
        remaining='actual prepared input/source review and root diagnostic-only delegation')
