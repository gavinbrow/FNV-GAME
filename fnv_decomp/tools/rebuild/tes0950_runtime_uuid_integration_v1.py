"""TES 0950-only runtime UUID integration; in-memory, not a provider approval.

This module cannot read files, publish, launch native tools, or authorize itself.
Caller must independently authenticate all source modules, exact inputs, current
namespace, reviews, ABI assumptions and operation permission. The original
negative remains negative; runtime-only bytes are not a fresh reference MATCH.
"""
import copy
import hashlib

import coff_code_archive as coff
import runtime_code_pool as pool
import uuid_directive_occurrence_witness as witness
import uuid_directive_root_composer as composer
import uuid_directive_projection as projection

POLICY = 'tes-0950-runtime-only-uuid-integration-v1'
ADDRESS = '0x0045b020'
ROOT = dict(original_address=ADDRESS, **{k: v for k,v in witness.ROOTS[ADDRESS].items()
                                        if k != 'certificate_sha256'})
CONTRACT_SHA = '4be4a91f0fd51fb4e1c7fc41bbceef8aef1d307c444a313cf987596c7ebc0866'
NEGATIVE_SHA = 'bed5fec32a338aab551d640cbf3e11c8f25242fdcae060247baa4afcd03a73b8'
DIRECTIVE_SHA = 'c7366a9d7fda0fe26a40098fc6ae83ea281c3d5d1f666a434b407eede5ed6f0c'
EXPORT = '_fnv_code_91ffdd2aab6e0a53d4cb34aebffa32d27721e8b16c87221c23d6d3ec49216842'
TARGETS = {
 '0x00649e40': ('0732-f4064ae07833cb92','0f4cb6be17d4b498ae0d9df0587fc768c588239283eb82650c41da325abcfcc4',109),
 '0x0065c570': ('0740-5c3012fe528eb0e3','bf61826c967ea8fb065d63b397dc8e05985f64078cd5eb81996df2d2d8672bf7',213),
 '0x00662760': ('0743-fa933b780b2d1f2c','ca70d3018bd38f7221f875bfe01e1f032bfac1fde6d4f4fccebcd84a694b7437',111),
 '0x004f92e0': ('0615-a75551b90d61b1c6','7bf306f31229e95a02c7c125098ce6db1db4940efc11993111e8b85a17777adc',271),
 '0x004e0050': ('0912-457e2065f9e9256b','1104b7b2dfcaea254e6207dd8d2da3081392c864a26167283aa37d6b9c1b5e7c',103),
 '0x004de580': ('0911-75496fb3812000b5','9a6312ff2c8721ed5b80ba457aed1f56af44cb1fc380af31d51f91a94738dbb4',91),
}
OFFSETS = (4,9,14,19,24,29)
TARGET_ORDER = ('0x00649e40','0x0065c570','0x00662760','0x004f92e0','0x004e0050','0x004de580')
FALSE = ('provider_selected','runtime_eligible','ABI_verified','namespace_approved',
         'full_serialization_eligible','materialization_approved','link_ready','native_tools_run')


def require(condition, message):
    if not condition: raise ValueError(message)


def validate_saved_inputs(raw, contract, negative, witnesses, providers, existing_exports):
    """Check exact root scope and internal consistency, not review authority."""
    require(type(raw) is bytes and coff.digest(raw)==ROOT['object_sha256'], 'TES object identity differs')
    require(type(contract) is dict and witness.digest(contract)==CONTRACT_SHA, 'TES contract differs')
    require(type(negative) is dict and witness.digest(negative)==NEGATIVE_SHA, 'TES negative differs')
    require(negative.get('closure_observed') is False and negative.get('root_closure_candidate') is False,
            'negative was promoted')
    require(contract.get('verified_match') is True and contract.get('fields_complete') is True and
            contract.get('missing_fields_complete') is True and not contract.get('missing_fields') and
            not contract.get('parent_eh'), 'TES contract completeness differs')
    fields=contract.get('fields');require(type(fields) is list and len(fields)==6,'six fields required')
    observations=[]
    for row in fields:
        cr=row.get('coff_relocation',{})
        observations.append((cr.get('offset'),cr.get('kind'),cr.get('addend'),row.get('exact_original_target_va'),
                             row.get('classification'),row.get('proof_consistency')))
    require(observations==[(offset,20,0,target,'SELECTED_CODE_ENTRY','EXACT_OWN_SOURCE_RESOLUTION')
                            for offset,target in zip(OFFSETS,TARGET_ORDER)], 'TES field bindings differ')
    require(type(witnesses) is list and len(witnesses)==1 and type(witnesses[0]) is dict and
            set(witnesses[0])=={'header','binding','witness_authority','declaration','review','declaration_authority'},
            'one exact UUID witness required')
    require(type(providers) is dict and type(existing_exports) in (list,tuple,set,frozenset), 'namespace inputs required')
    require(len(existing_exports)==len(set(existing_exports)) and EXPORT not in existing_exports,
            'TES export collision or incomplete namespace')
    expected_root={k:ROOT[k] for k in ('recipe_id','object_sha256','symbol_index')}
    require(providers.get(ADDRESS)==expected_root and pool.canonical(expected_root)==EXPORT, 'TES physical owner differs')
    for address,(recipe,obj,index) in TARGETS.items():
        require(providers.get(address)==dict(recipe_id=recipe,object_sha256=obj,symbol_index=index),
                'TES target physical owner differs: '+address)
    return True


def produce(raw, contract, negative, witnesses, providers, *, existing_exports):
    """Compose, project and archive exactly TES 0950 in memory; never perform I/O.

    Fresh source/input/authority review and current selected namespace are the
    caller's responsibility. Planned target identities are unresolved obligations,
    not assertions that any six providers were emitted, selected or loaded.
    """
    validate_saved_inputs(raw,contract,negative,witnesses,providers,existing_exports)
    before=witness.digest(dict(contract=contract,negative=negative,witnesses=witnesses,
                               providers=providers,existing_exports=sorted(existing_exports)))
    w=witnesses[0]
    composed=composer.compose(raw,contract,negative,ROOT.copy(),w['header'],w['binding'],
        w['witness_authority'],w['declaration'],w['review'],w['declaration_authority'],policy_id=composer.POLICY)
    require(composed.get('original_negative_unchanged') is True and
            composed.get('base_certificate_sha256')==NEGATIVE_SHA and
            composed.get('proposal',{}).get('raw_section_sha256')==DIRECTIVE_SHA and
            len(composed.get('discharged_blocker_occurrences',[]))==3 and
            all(composed.get(k) is False for k in FALSE if k in composed), 'UUID composition differs')
    projected,proof=projection.project_member(raw,contract,negative,witnesses,composed,[ROOT.copy()],
        providers,existing_exports=existing_exports,policy_id=projection.POLICY)
    require(proof.get('exports')==[EXPORT] and len(proof.get('fields',[]))==6 and
            proof.get('original_negative_certificate_preserved') is True and
            all(proof.get(k) is False for k in FALSE if k in proof), 'TES projection differs')
    obj=coff.parse(projected);directives=[s for s in obj['sections'].values() if s['name']=='.drectve']
    require(len(directives)==1 and hashlib.sha256(directives[0]['payload']).hexdigest()==DIRECTIVE_SHA and
            directives[0]['payload'].lower().count(b'uuid.lib')==2, 'original duplicate UUID directives differ')
    require(coff.exports(projected)==[EXPORT], 'unexpected exported definitions')
    packed=coff.archive([('tes0950.obj',projected)]); parsed=coff.read_archive(packed)
    require(parsed['members']==[('tes0950.obj',projected)] and parsed['index']==[(EXPORT,'tes0950.obj')],
            'archive index differs')
    require(witness.digest(dict(contract=contract,negative=negative,witnesses=witnesses,
        providers=providers,existing_exports=sorted(existing_exports)))==before,'input evidence changed')
    return packed, dict(kind=POLICY,object_sha256=coff.digest(projected),archive_sha256=coff.digest(packed),
        root=copy.deepcopy(ROOT),expected_export=EXPORT,field_count=6,original_negative_preserved=True,
        duplicate_uuid_occurrences=2,projection=proof,target_identities=copy.deepcopy(TARGETS),
        original_byte_match_claimed=False,reference_read=False,native_tools_run=False,provider_selected=False,
        target_providers_selected=False,ABI_verified=False,runtime_eligible=False,link_ready=False,
        independent_authority_and_namespace_authentication_required=True)
