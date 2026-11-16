"""Replay and qualify an existing narrow readonly-section omission witness.

No certificate is modified, created, or made positive. The caller must separately
authenticate the collector envelope and original input/authority identities.
The existing witness is replayed over its exact input, never trusted by assertion.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import ordinary_initialized_data_omission as omission

POLICY = 'readonly-section-semantics-qualification-v1'
WITNESS_PIN = '1a0e8aa2271218f59c11497c1363b41f099bb259791e19adac7d80718e7a5d7b'
FORMS = {('.rdata', 0x40300040), ('.rdata', 0x40101040)}
FALSE = dict(provider_selected=False, runtime_eligible=False, ABI_verified=False,
             namespace_approved=False, link_ready=False, emission_performed=False,
             full_serialization_eligible=False, adapted_root_certificate_created=False)

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',', ':'),ensure_ascii=True).encode()).hexdigest()

def require(condition, message):
    if not condition: raise ValueError(message)

def qualify(raw, contract, negative, requested_sections, supplied_witness, *, authority):
    """Recompute the frozen producer and report exact blocker occurrences only.

    `authority` is an externally authenticated locator, not authentication by
    this function. Raw is supplied by the separately controlled caller: this
    function itself performs no filesystem access to objects or game inputs.
    """
    require(hashlib.sha256(Path(omission.__file__).read_bytes()).hexdigest()==WITNESS_PIN,'witness producer drift')
    require(type(raw) is bytes and type(contract) is dict and type(negative) is dict and type(supplied_witness) is dict,'input types')
    require(type(requested_sections) is list and requested_sections and all(type(n) is int and n>0 for n in requested_sections) and requested_sections==sorted(set(requested_sections)),'section selection')
    require(type(authority) is dict and set(authority)=={'record_sha256','certificate_sha256','contract_sha256','receipt_sha256','lane','ordinal'},'authority schema')
    require(all(type(authority[k]) is str and re.fullmatch('[0-9a-f]{64}',authority[k]) for k in ('record_sha256','certificate_sha256','contract_sha256','receipt_sha256')) and all(type(authority[k]) is int and authority[k]>0 for k in ('lane','ordinal')),'authority identity')
    require(authority['certificate_sha256']==digest(negative) and authority['contract_sha256']==digest(contract),'authority scope drift')
    require(negative.get('closure_observed') is False and type(negative.get('blockers')) is list and negative['blockers'],'negative certificate required')
    before=digest(dict(contract=contract,negative=negative,witness=supplied_witness,authority=authority,sections=requested_sections))
    fresh=omission.observe_omitted_initialized_data(raw,contract,negative,requested_sections)
    require(digest(fresh)==digest(supplied_witness),'witness replay mismatch')
    require(fresh.get('policy_id')==omission.POLICY and fresh.get('original_certificate_unchanged') is True and fresh.get('adapted_root_certificate_created') is False,'witness provenance')
    require(fresh.get('contract_identity_sha256')==digest(contract) and fresh.get('original_certificate_sha256')==digest(negative),'witness scope')
    original=negative['blockers']; occurrences=[]
    for n,b in enumerate(original,1):
        require(type(b) is dict and set(b)=={'code','evidence','blocker_id'} and b['blocker_id']==digest({'code':b['code'],'evidence':b['evidence']}),'blocker identity')
        occurrences.append(dict(ordinal=n,blocker=b))
    selected=[]
    require(type(fresh.get('rows')) is list and len(fresh['rows'])==len(requested_sections),'witness rows')
    for section,row in zip(requested_sections,fresh['rows']):
        require(type(row.get('section')) is int and row['section']==section and type(row.get('flags')) is int and type(row.get('name')) is str,'witness section')
        if not row.get('approved'): continue
        require(row['approved'] is True and (row['name'],row['flags']) in FORMS and row.get('blockers')==[],'unsupported section form')
        evidence={'section':section,'name':row['name'],'flags':row['flags']}
        matches=[o for o in occurrences if o['blocker']['code']=='UNSUPPORTED_SECTION_SEMANTICS' and digest(o['blocker']['evidence'])==digest(evidence)]
        require(len(matches)==1,'ambiguous section blocker occurrence')
        require(row['discharge_blocker_ids']==[matches[0]['blocker']['blocker_id']],'witness occurrence differs')
        selected.append(dict(ordinal=matches[0]['ordinal'],blocker=matches[0]['blocker'],section=section,witness_row_sha256=digest(row)))
    require(len({o['ordinal'] for o in selected})==len(selected),'duplicate selected occurrence')
    ids=[o['blocker']['blocker_id'] for o in selected]
    require(fresh['discharge_blocker_ids']==ids,'witness ordered discharge differs')
    require(fresh['witness_complete'] is (len(selected)==len(requested_sections)),'witness completeness differs')
    require(digest(dict(contract=contract,negative=negative,witness=supplied_witness,authority=authority,sections=requested_sections))==before,'input mutation')
    require(hashlib.sha256(Path(omission.__file__).read_bytes()).hexdigest()==WITNESS_PIN,'witness producer drift after replay')
    return dict(schema_version=1,policy_id=POLICY,kind='readonly-section-qualification',
                original_certificate_sha256=digest(negative),original_contract_sha256=digest(contract),
                original_blocker_occurrences=occurrences,qualified_occurrences=selected,
                unqualified_occurrences=[o for o in occurrences if o['ordinal'] not in {s['ordinal'] for s in selected}],
                original_certificate_preserved=True,authority=authority,authority_authentication_required=True,
                witness_sha256=digest(fresh),witness_producer_sha256=WITNESS_PIN,
                qualification_is_not_closure_or_provider_approval=True,**FALSE)
