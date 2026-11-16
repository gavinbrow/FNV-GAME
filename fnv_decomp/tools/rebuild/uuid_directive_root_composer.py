"""Finite UUID root composition; no I/O, publication, or authority inference."""
import copy
import hashlib
import ntpath
import re
import struct

import coff_code_archive as coff
import root_code_closure as ordinary
import uuid_directive_occurrence_witness as witness

POLICY = 'finite-uuid-root-composition-v1'
FALSE = dict(provider_selected=False, runtime_eligible=False, ABI_verified=False,
             namespace_approved=False, full_serialization_eligible=False,
             emission_performed=False, materialization_approved=False,
             link_ready=False, native_tools_run=False)
require = coff.require
digest = witness.digest


def validate_declaration(declaration, review, authority, binding):
    """Check internal pins; caller must independently authenticate authority."""
    require(type(declaration) is dict and set(declaration) == {
        'kind', 'library_name', 'absolute_path', 'sha256', 'required_response_token'}, 'declaration schema')
    require(declaration['kind'] == 'explicit-normal-sdk-library-dependency-v1' and
            declaration['library_name'] == 'uuid.lib', 'not the finite UUID dependency')
    path = declaration['absolute_path']
    require(type(path) is str and ntpath.isabs(path) and bool(ntpath.splitdrive(path)[0]) and ntpath.splitdrive(path)[1].startswith('\\') and
            ntpath.normpath(path) == path and not path.startswith(('\\\\?\\','\\\\.\\')) and witness.safe_path(path) and
            ntpath.basename(path).lower() == 'uuid.lib' and path == declaration['required_response_token'],
            'exact absolute full-path response token required')
    require(witness.sha(declaration['sha256']) and type(binding) is dict and
            binding.get('path') == path and binding.get('sha256') == declaration['sha256'],
            'candidate and declared physical dependency differ')
    require(type(review) is dict and set(review) == {'kind', 'status', 'declaration_sha256', 'reviewer'} and
            review['kind'] == 'independent-normal-dependency-declaration-review-v1' and
            review['status'] == 'accepted' and review['declaration_sha256'] == digest(declaration) and
            type(review['reviewer']) is str and bool(review['reviewer'].strip()), 'declaration review differs')
    require(type(authority) is dict and set(authority) == {'declaration_sha256', 'review_sha256'} and
            authority['declaration_sha256'] == digest(declaration) and authority['review_sha256'] == digest(review),
            'caller authority pins differ')
    return dict(declaration_sha256=digest(declaration), review_sha256=digest(review),
                required_response_token=path, caller_authority_authentication_required=True,
                dependency_selected=False, dependency_loaded=False, duplicate_semantics_proved=False)


def _header(raw, header):
    require(type(raw) is bytes and len(raw) >= 60 and type(header) is dict, 'raw/header required')
    machine,count,_,_,_,optional,_ = struct.unpack_from('<HHIIIHH', raw, 0)
    idx = header.get('index')
    require(machine == 0x14c and type(idx) is int and 1 <= idx <= count and len(raw) >= 20 + 40*count,
            'header bounds')
    raw_header = raw[20+40*(idx-1):20+40*idx]
    name, vs, va, size, ptr, rp, lp, nr, nl, flags = struct.unpack('<8sIIIIIIHHI',raw_header)
    expected = dict(index=idx,name=name.rstrip(b'\0').decode('ascii'),size=size,flags=flags,
                    virtual_size=vs,virtual_address=va,object_size=len(raw),raw_data_offset=ptr,
                    section_count=count,optional_header_size=optional,relocation_count=nr,
                    relocation_pointer=rp,line_number_count=nl,line_number_pointer=lp)
    require(header == expected and ptr + size <= len(raw), 'actual original header differs')
    return raw_header, raw[ptr:ptr+size]


def _compose_core(raw, contract, base, root, header, binding, witness_authority, declaration, review, declaration_authority, *, policy_id, proposal_fn):
    require(policy_id == POLICY and type(raw) is bytes and 0 < len(raw) <= 16*1024**2, 'policy or object bound')
    before = digest(dict(contract=contract,base=base,root=root,header=header,binding=binding,
                         witness_authority=witness_authority,declaration=declaration,review=review,
                         declaration_authority=declaration_authority))
    require(coff.digest(raw) == contract['provenance']['object_sha256'], 'object provenance differs')
    obj = coff.parse(raw)
    require(ordinary.assess_object(obj,contract) == base and base['contract_identity_sha256'] == digest(contract),
            'fresh original ordinary assessment differs')
    raw_header, payload = _header(raw,header)
    proposal = proposal_fn(root,contract,base,payload,header,binding,witness_authority)
    dependency = validate_declaration(declaration,review,declaration_authority,binding)
    occurrences = proposal['proposed_blocker_occurrences']
    require([x['ordinal'] for x in occurrences] == [1,2,3] and
            [x['blocker_id'] for x in occurrences] == [witness.UUID_ID,witness.UUID_ID,witness.DIFF_ID],
            'exact original blocker occurrences required')
    require(digest(dict(contract=contract,base=base,root=root,header=header,binding=binding,
                        witness_authority=witness_authority,declaration=declaration,review=review,
                        declaration_authority=declaration_authority)) == before, 'proof input changed')
    return dict(schema_version=1,kind='finite-uuid-structural-composition',policy_id=POLICY,
        base_certificate=copy.deepcopy(base),base_certificate_sha256=digest(base),
        contract_identity_sha256=digest(contract),original_negative_unchanged=True,
        original_closure_observed=False, original_header_hex=raw_header.hex(),
        original_header_sha256=hashlib.sha256(raw_header).hexdigest(),proposal=proposal,
        declaration=copy.deepcopy(declaration),review=copy.deepcopy(review),dependency_obligation=dependency,
        discharged_blocker_occurrences=copy.deepcopy(occurrences),remaining_blocker_occurrences=[],
        structural_composition_complete=True,caller_authority_authentication_required=True,**FALSE)


def compose(raw, contract, base, root, header, binding, witness_authority, declaration, review, declaration_authority, *, policy_id):
    """Fixed production trust path: the caller cannot substitute witness authority."""
    return _compose_core(raw,contract,base,root,header,binding,witness_authority,declaration,review,
                         declaration_authority,policy_id=policy_id,proposal_fn=witness.assess)
