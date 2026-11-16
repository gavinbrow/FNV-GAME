"""Finite, candidate-only qualification for the existing UUID directive profile.

The frozen witness authenticates two exact root/certificate identities; this
adapter additionally requires the independently reviewed full-path dependency
before returning a proposal. It does not parse objects, create a composition,
serialize, certify closure, authorize a provider or select/load a library.
Caller must separately authenticate all supplied authority records.
"""
import copy
import hashlib

import uuid_directive_occurrence_witness as witness
import uuid_directive_root_composer as composer

POLICY='cached-directive-known-uuid-candidate-v1'
FALSE_FLAGS=('provider_selected','runtime_eligible','ABI_verified','admission_approved',
             'namespace_approved','full_serialization_eligible','materialization_approved',
             'link_ready','native_tools_run','emission_performed','object_write_performed',
             'library_selection_proved','library_loaded_proved','duplicate_linker_semantics_proved',
             'library_request_proved','library_dependencies_proved','certificate_rewritten','ordinary_graph_closure')


def _require(condition,message):
    if not condition:raise ValueError(message)


def _qualify_core(root,contract,negative,raw_section,header,binding,witness_authority,
                  declaration,review,declaration_authority,*,proposal_fn,declaration_fn):
    """Private pure fixture seam; production binds both frozen public delegates."""
    _require(type(root) is dict and root.get('original_address') in witness.ROOTS,'unsupported finite root')
    spec=witness.ROOTS[root['original_address']]
    expected=dict(original_address=root['original_address'],**{k:v for k,v in spec.items() if k!='certificate_sha256'})
    _require(root==expected and witness.digest(root)==witness.digest(expected),'exact known root identity required')
    _require(type(contract) is dict and type(negative) is dict and type(raw_section) is bytes and
             len(raw_section)==93 and type(header) is dict and type(binding) is dict,'exact evidence types required')
    before=witness.digest(dict(root=root,contract=contract,negative=negative,raw_section=raw_section.hex(),
        header=header,binding=binding,witness_authority=witness_authority,declaration=declaration,
        review=review,declaration_authority=declaration_authority))
    proposal=proposal_fn(root,contract,negative,raw_section,header,binding,witness_authority)
    dependency=declaration_fn(declaration,review,declaration_authority,binding)
    proposal_keys={'schema_version','kind','policy_id','root','original_negative','original_negative_sha256',
       'original_negative_unchanged','contract_sha256','raw_section_sha256','raw_section_hex','header','binding',
       'authority','directive_occurrences','proposed_blocker_occurrences','caller_authority_authentication_required'} | set(FALSE_FLAGS)
    _require(type(proposal) is dict and set(proposal)==proposal_keys and
        type(proposal.get('schema_version')) is int and proposal['schema_version']==1 and
        proposal.get('policy_id')==witness.POLICY and proposal.get('caller_authority_authentication_required') is True and
        proposal.get('kind')=='typed-uuid-directive-occurrence-discharge-proposal' and
        proposal.get('root')==root and proposal.get('contract_sha256')==witness.digest(contract) and
        proposal.get('original_negative')==negative and proposal.get('original_negative_sha256')==witness.digest(negative) and
        proposal.get('original_negative_unchanged') is True and proposal.get('raw_section_hex')==raw_section.hex() and
        proposal.get('raw_section_sha256')==hashlib.sha256(raw_section).hexdigest() and
        proposal.get('header')==header and proposal.get('binding')==binding and proposal.get('authority')==witness_authority and
        all(proposal.get(k) is False for k in FALSE_FLAGS),'occurrence proposal evidence or flags differ')
    _require(all(negative.get(k) is False for k in ('closure_observed','graph_observation_complete','root_closure_candidate')),
             'original negative promoted')
    expected_blockers=[dict(code='UNSUPPORTED_IMPLICIT_LINKER_DIRECTIVE',evidence=witness.UUID,blocker_id=witness.UUID_ID),
                       dict(code='UNSUPPORTED_IMPLICIT_LINKER_DIRECTIVE',evidence=witness.UUID,blocker_id=witness.UUID_ID),
                       dict(code='DIRECTIVE_CONTRACT_DIFFERS',evidence=witness.TOKENS,blocker_id=witness.DIFF_ID)]
    _require(negative.get('blockers')==expected_blockers,'exact ordered negative occurrences required')
    occurrences=proposal.get('proposed_blocker_occurrences');spans=proposal.get('directive_occurrences')
    _require(type(occurrences) is list and len(occurrences)==3 and type(spans) is list and len(spans)==4,
             'occurrence cardinality differs')
    for ordinal,(item,blocker,indices) in enumerate(zip(occurrences,expected_blockers,([1],[2],[1,2,3,4])),1):
        _require(type(item) is dict and set(item)=={'ordinal','blocker_id','blocker_sha256','blocker','directive_ordinals'} and
            type(item.get('ordinal')) is int and item['ordinal']==ordinal and
            type(item.get('directive_ordinals')) is list and
            all(type(value) is int for value in item['directive_ordinals']) and
            item.get('blocker')==blocker and item.get('blocker_id')==blocker['blocker_id'] and
            item.get('blocker_sha256')==witness.digest(blocker) and item.get('directive_ordinals')==indices,
            'ordered blocker occurrence differs')
    position=0
    for ordinal,(span,token) in enumerate(zip(spans,witness.TOKENS),1):
        _require(type(span) is dict and set(span)=={'ordinal','start','end','token'} and
            type(span['ordinal']) is int and span['ordinal']==ordinal and type(span['start']) is int and
            type(span['end']) is int and position<=span['start']<span['end']<=len(raw_section) and
            all(ch in b' \t\r\n' for ch in raw_section[position:span['start']]) and
            span['token']==token and raw_section[span['start']:span['end']]==token.encode('ascii'),
            'raw directive occurrence differs')
        position=span['end']
    _require(all(ch in b' \t\r\n' for ch in raw_section[position:]),'unparsed raw directive bytes')
    _require(type(dependency) is dict and dependency.get('required_response_token')==declaration.get('absolute_path')==binding.get('path') and
        dependency.get('caller_authority_authentication_required') is True and
        all(dependency.get(k) is False for k in ('dependency_selected','dependency_loaded','duplicate_semantics_proved')),
        'reviewed full-path dependency obligation differs')
    _require(before==witness.digest(dict(root=root,contract=contract,negative=negative,raw_section=raw_section.hex(),
        header=header,binding=binding,witness_authority=witness_authority,declaration=declaration,
        review=review,declaration_authority=declaration_authority)),'input evidence changed')
    return dict(schema_version=1,kind='known-uuid-directive-candidate',policy_id=POLICY,
        root=copy.deepcopy(root),original_negative=copy.deepcopy(negative),original_negative_sha256=witness.digest(negative),
        contract_sha256=witness.digest(contract),original_negative_unchanged=True,proposal=copy.deepcopy(proposal),
        dependency_obligation=copy.deepcopy(dependency),required_future_response_token=dependency['required_response_token'],
        caller_authority_authentication_required=True,response_token_observed=False,SDK_identity_freshly_observed=False,
        composition_proved=False,projection_performed=False,**{k:False for k in FALSE_FLAGS})


def qualify(root,contract,negative,raw_section,header,binding,witness_authority,
            declaration,review,declaration_authority):
    """Fixed two-root proposal; not a new-root policy or operational authority."""
    return _qualify_core(root,contract,negative,raw_section,header,binding,witness_authority,
        declaration,review,declaration_authority,proposal_fn=witness.assess,
        declaration_fn=composer.validate_declaration)
