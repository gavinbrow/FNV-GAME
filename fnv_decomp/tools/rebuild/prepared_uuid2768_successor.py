"""Pure UUID-qualified CODE exclusion successor; not application admission.

This transform does not open files or read objects, images, archives, or SDKs.
Callers authenticate exact source and input review before publishing its result.
"""
import copy
import hashlib
import json
import re

PARENT='250c9cf8be4cd98e805eb81ed89daae989bab6d262cab5cf0f3e8040120693af'
HANDOFF='4ce4f515e43a04f622b1efaa70ac47753f16109111944f73ca0aefeb915b06a1'
HANDOFF_REVIEW='7b879e3baa1bf55e81c9a9884f692b27feff025c0d5fe55a30d7c3d60135ab9d'
NATIVE='12dae2e56d941949650dbc8c0d72a0660c4d8da5d4d14f2209db4f79e2c852f1'
NATIVE_REVIEW='f161af6ac5ce40e02088724ba156f7737484def6b5aafadc4f8bda104587b7f6'
NEGATIVE='7c4704d0c777585656272cd2a39a06437d124e34d4cea712236b982641cf9a26'
COMPOSED='69076d817070c2411fbb8d3dbf9cf1ea0ca3409d6a438360c25dffc19aa7d238'
OBJECT='6fcd604987e08477566cbf9b6901f3200304eb557fdc8f7c356fedaf27d633b3'
ARCHIVE='b921ee8a8d6baf9a751f1a488aa10a763627ede51b2b475668c97455a4e9eb53'
PROOFS='4b7cb6ce64a9a84d461ef0ef536cd17c5952fe03b697e45e652e18c2f5e7cc31'
UUID='500b64d35a879017b6e729c7264954dafd1722389e78fe47ff618916fb537d35'
DIFF='771cd50e84e5996d8fda1470742f71fe7d99f887e03ad7338a4dd10d753ef094'
TOKENS=['/DEFAULTLIB:"uuid.lib"','/DEFAULTLIB:"uuid.lib"','/DEFAULTLIB:"LIBCMT"','/DEFAULTLIB:"OLDNAMES"']
ROOT=dict(original_address='0x00c5d4e0',recipe_id='2768-7a8853c4310f459f',recipe_index=2768,section=131,size=58,
          symbol='?FUN_00c5d4e0@@YAXXZ',symbol_index=553,value=0,
          object_sha256='a7280d36e8d796a5689c8b61adac4be327eb17d55e12d734600b0ede46cafb88',
          source_sha256='376782096fdbabae4c10fb175023317d58fcbd8930596abea1008d8628bffe02')


def need(ok,message):
    if not ok:raise ValueError(message)


def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')
def digest(value):return hashlib.sha256(canonical(value)).hexdigest()


def physical(value):
    need(type(value) is dict and set(value)=={'recipe_id','object_sha256','symbol_index'} and
         type(value['recipe_id']) is str and bool(value['recipe_id']) and
         type(value['object_sha256']) is str and re.fullmatch('[0-9a-f]{64}',value['object_sha256']) and
         type(value['symbol_index']) is int and value['symbol_index']>=0,'invalid physical identity')
    return '_fnv_code_'+digest(value)


def census(records):
    names=set();addresses=set();ordinary=set()
    for record in records:
        name=record['canonical'];address=record['original_address']
        need(name==physical(record['namespace_identity']) and name not in names,'duplicate/invalid canonical identity')
        physical(record['origin_identity'])
        need(type(address) is str and re.fullmatch('0x[0-9a-f]{8}',address) and address not in addresses and
             record['category'] in ('ordinary','application-candidate'),'duplicate/invalid address/category')
        names.add(name);addresses.add(address)
        if record['category']=='ordinary':ordinary.add(name)
    return sorted(names),sorted(ordinary)


def build(parent,handoff,handoff_peer,native,native_peer):
    """Append one qualified UUID root; caller supplies independently pinned inputs."""
    need(type(parent) is dict and type(parent.get('schema_version')) is int and parent['schema_version']==7 and
         parent.get('kind')=='prepared-CODE-collision-exclusions' and parent.get('policy_id')=='prepared-CODE56-successor-v1' and
         type(parent.get('ordinary_prepared_count')) is int and parent['ordinary_prepared_count']==14528 and
         type(parent.get('collision_exclusion_count')) is int and parent['collision_exclusion_count']==14534 and
         parent.get('application_selected_code_count') is None and parent.get('application_selection_inferred_from_counts') is False and
         'application_manifest_adopted' not in parent and parent.get('historical_records_preserved') is True,
         'accepted parent epoch scope differs')
    records=parent['records'];names,ordinary=census(records)
    need(len(records)==14534 and len(ordinary)==14528 and names==parent['exclusion_names'] and
         ordinary==parent['ordinary_names'],'complete parent census differs')
    need(type(handoff) is dict and handoff.get('schema_version')==1 and handoff.get('kind')=='accepted-qualified-UUID-CODE-export-handoff' and
         handoff.get('sealed') is True and type(handoff.get('records')) is list and len(handoff['records'])==1 and
         handoff.get('object',{}).get('sha256')==OBJECT and handoff.get('archive',{}).get('sha256')==ARCHIVE and
         handoff.get('field_proofs',{}).get('sha256')==PROOFS and handoff['field_proofs'].get('fields')==9 and
         all(handoff.get(k) is False for k in ('native_archive_conformance_verified','provider_selected','runtime_eligible',
             'ABI_verified','namespace_approved','library_selected','library_loaded','executable_link_performed')),
         'qualified handoff scope/promotion differs')
    need(type(handoff_peer) is dict and handoff_peer.get('status')=='accepted-qualified-metadata-handoff' and
         handoff_peer.get('handoff_sha256')==HANDOFF and handoff_peer.get('whole_payload_matches_independently_reviewed_draft') is True and
         type(handoff_peer.get('complete_fields')) is int and handoff_peer['complete_fields']==9 and
         handoff_peer.get('native_conformance_claim_created') is False and handoff_peer.get('namespace_adoption_authorized') is False and
         handoff_peer.get('provider_selected') is False and handoff_peer.get('runtime_eligible') is False,
         'independent handoff review differs')
    need(type(native) is dict and native.get('kind')=='uuid2768-native-conformance-v1' and native.get('status')=='pass' and
         native.get('input_stability_verified') is True and native.get('typed_producer_evidence',{}).get('base_closure_observed') is False and
         native['typed_producer_evidence'].get('original_negative_preserved') is True and
         all(native.get(k) is False for k in ('UUID_selected_or_loaded','duplicate_semantics_proved','ordinary_two_library_policy_applied',
             'provider_selected','runtime_eligible','ABI_verified','executable_linked','Game_execution')), 'native evidence scope differs')
    need(type(native_peer) is dict and native_peer.get('kind')=='uuid2768-native-independent-review-v1' and
         native_peer.get('status')=='accepted' and native_peer.get('receipt_sha256')==NATIVE and
         native_peer.get('archive_sha256')==ARCHIVE and native_peer.get('object_sha256')==OBJECT and
         all(native_peer.get(k) is False for k in ('UUID_selected_or_loaded','duplicate_semantics_proved','ordinary_two_library_policy_applied',
             'provider_selected','runtime_eligible','ABI_verified','link_performed','game_execution')), 'native peer scope differs')
    row=handoff['records'][0];root=row['root'];identity={k:ROOT[k] for k in ('recipe_id','object_sha256','symbol_index')}
    nested=native['typed_producer_evidence']['nested_sha256'];components=native.get('components')
    need(type(components) is list and len(components)==1 and components[0].get('input_sha256')==ARCHIVE and
         components[0].get('native_metadata_matches') is True and
         components[0].get('receipt_sha256')==handoff['producer_receipt']['sha256'] and
         nested.get('assessment')==row['qualified_assessment_sha256'] and nested.get('projection')==row['projection_sha256'] and
         nested.get('field_ledger')==row['field_ledger_sha256'], 'native evidence/typed nested identity differs')
    facts=components[0]['facts'];directives=facts['qualified_directive_evidence']
    need(type(facts.get('members')) is int and facts['members']==1 and type(facts.get('exports')) is int and facts['exports']==1 and
         facts.get('LIB_membership_exact') is True and facts.get('complete_native_linker_index') is True and
         directives.get('payload_bytes')==93 and directives.get('tokens')==TOKENS and
         directives.get('exact_directive_token_sequence_matches') is True and directives.get('original_negative_occurrences')==3 and
         directives.get('original_negative_preserved') is True and directives.get('qualified_witness_is_separate') is True and
         all(directives.get(k) is False for k in ('UUID_selected_or_loaded','duplicate_semantics_proved','ordinary_two_library_fallback_used')),
         'native member/directive scope differs')
    name=physical(identity)
    need(root==ROOT and digest(root)==digest(ROOT) and row['canonical_export']==name and name not in names and
         ROOT['original_address'] not in {r['original_address'] for r in records} and
         type(row.get('code_bytes')) is int and row['code_bytes']==58 and type(row.get('fields')) is int and row['fields']==9 and
         row.get('serialized_section')==2 and type(row.get('serialized_section')) is int and
         row.get('serialized_symbol_index')==6 and type(row.get('serialized_symbol_index')) is int and
         row.get('original_negative_certificate_sha256')==NEGATIVE and row.get('qualified_composition_sha256')==COMPOSED,
         'root/namespace/negative/composition differs')
    need(type(row.get('original_fields')) is list and len(row['original_fields'])==9 and
         type(row.get('normalized_fields')) is list and len(row['normalized_fields'])==9 and
         row['namespace_maps']['section_map']['131']==2 and row['namespace_maps']['symbol_map']['553']==6 and
         digest(row['namespace_maps'])==row['namespace_maps_sha256'], 'complete fields or physical root maps differ')
    seen=set()
    for i,(original,mapped) in enumerate(zip(row['original_fields'],row['normalized_fields']),1):
        cr=original['coff_relocation'];section=original['physical_section'];symbol=cr['symbol_index']
        need(type(mapped.get('ordinal')) is int and mapped['ordinal']==i and mapped.get('original_field_sha256')==digest(original) and
             all(type(x) is int for x in (section,symbol,cr['offset'],cr['kind'],mapped.get('serialized_section'),
                                           mapped.get('serialized_symbol_index'))) and
             mapped['serialized_section']>0 and mapped['serialized_symbol_index']>=0 and
             mapped.get('original_section')==section and mapped.get('original_symbol_index')==symbol and
             mapped.get('original_offset')==cr['offset'] and mapped.get('kind')==cr['kind'] and
             mapped['serialized_section']==row['namespace_maps']['section_map'][str(section)] and
             mapped['serialized_symbol_index']==row['namespace_maps']['symbol_map'][str(symbol)] and
             type(mapped.get('canonical_name')) is str and bool(mapped['canonical_name']) and type(mapped.get('role')) is str,
             'physical/normalized field join differs')
        key=(section,cr['offset'],symbol,cr['kind']);need(key not in seen,'duplicate physical field');seen.add(key)
    occurrences=row['original_negative_occurrences']
    need(type(occurrences) is list and len(occurrences)==3 and all(type(x.get('ordinal')) is int for x in occurrences) and
         [x['ordinal'] for x in occurrences]==[1,2,3] and [x['blocker_id'] for x in occurrences]==[UUID,UUID,DIFF] and
         [x['directive_ordinals'] for x in occurrences]==[[1],[2],[1,2,3,4]], 'original occurrence multiplicity differs')
    directive=handoff['directive'];raw=bytes.fromhex(directive['payload_hex'])
    need(type(directive.get('extent')) is int and directive['extent']==93 and len(raw)==93 and
         hashlib.sha256(raw).hexdigest()==directive['payload_sha256']=='c7366a9d7fda0fe26a40098fc6ae83ea281c3d5d1f666a434b407eede5ed6f0c' and
         directive.get('ordered_tokens')==TOKENS and type(handoff.get('future_uuid_response_token')) is str and
         handoff['future_uuid_response_token']==r'C:\Projects\Decompilation\FNV\tools\vc2008\VC\PlatformSDK\Lib\Uuid.Lib' and
         handoff['declaration'].get('canonical_sha256')==
         '26e13ca4ee534ef4dd7df52b5b31b388dfd49ba79a4099561ffe2bf9fa8c73d9','directive/dependency obligation differs')
    new=copy.deepcopy(records)
    new.append(dict(canonical=name,original_address=ROOT['original_address'],category='ordinary',
        cohort='UUID2768-qualified-directive-projection',identity_mode='original-selected-physical-qualified-UUID-directives',
        namespace_identity=identity,origin_identity=copy.deepcopy(identity),logical_binding_applied=True,
        member='uuid2768.obj',member_sha256=OBJECT,original_root=copy.deepcopy(ROOT),
        serialization_maps=copy.deepcopy(row['namespace_maps']),serialized_section=2,serialized_symbol_index=6,
        source_ledger_sha256=HANDOFF,source_record_ordinal=1,source_record_sha256=digest(row),
        full_field_proof_ledger_sha256=PROOFS,original_field_count=9,
        original_negative_certificate_sha256=NEGATIVE,qualified_composition_sha256=COMPOSED,
        qualified_assessment_sha256=row['qualified_assessment_sha256'],field_ledger_sha256=row['field_ledger_sha256'],
        normalized_fields=copy.deepcopy(row['normalized_fields']),original_fields=copy.deepcopy(row['original_fields']),
        original_negative_occurrences=copy.deepcopy(occurrences),directive=copy.deepcopy(directive),
        future_uuid_response_token=handoff['future_uuid_response_token'],native_receipt_sha256=NATIVE,native_review_sha256=NATIVE_REVIEW))
    names,ordinary=census(new)
    need(len(names)==14535 and len(ordinary)==14529,'successor census differs')
    result=copy.deepcopy(parent)
    result.update(schema_version=8,policy_id='prepared-UUID2768-successor-v1',parent_manifest_sha256=PARENT,
        records=new,exclusion_names=names,ordinary_names=ordinary,ordinary_prepared_count=14529,
        collision_exclusion_count=14535,qualified_uuid_handoff_sha256=HANDOFF,qualified_uuid_handoff_review_sha256=HANDOFF_REVIEW,
        qualified_uuid_native_sha256=NATIVE,qualified_uuid_native_review_sha256=NATIVE_REVIEW,
        qualified_uuid_export_count=1,qualified_uuid_field_count=9,historical_records_preserved=True,
        fresh_original_stability_verified=False)
    need(result['records'][:14534]==parent['records'] and 'application_manifest_adopted' not in result and
         result['application_selected_code_count'] is None,'historical or application state changed')
    return result


def from_bytes(parent_bytes,handoff_bytes,handoff_review_bytes,native_bytes,native_review_bytes):
    for data,expected in ((parent_bytes,PARENT),(handoff_bytes,HANDOFF),(handoff_review_bytes,HANDOFF_REVIEW),
                          (native_bytes,NATIVE),(native_review_bytes,NATIVE_REVIEW)):
        need(type(data) is bytes and hashlib.sha256(data).hexdigest()==expected,'fixed input hash differs')
    return build(*(json.loads(data) for data in (parent_bytes,handoff_bytes,handoff_review_bytes,native_bytes,native_review_bytes)))
