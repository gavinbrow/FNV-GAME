"""Versioned COMDAT ANY composition; original negative observer is preserved."""
from __future__ import annotations
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import struct

import comdat_any_code_omission as policy
import coff_code_archive as coff
import root_code_closure as ordinary

POLICY = 'comdat-any-root-certificate-composition-v1'
WITNESS_KIND = 'typed-comdat-any-code-witness'
WITNESS_PIN = 'd9e283ee6b63c5d3913bd61ffaa92bb80e1618989da9899bb6a15f69953dea10'
FALSE = dict(provider_selected=False,runtime_eligible=False,ABI_verified=False,namespace_approved=False,
    full_serialization_eligible=False,emission_performed=False,materialization_approved=False,link_ready=False,
    global_link_uniqueness_proved=False,planned_definition_census_authenticated=False)
require = coff.require


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()


def exact(left,right):
    return left==right and digest(left)==digest(right)


def reconstruct_definition_census(raw,contract,requested_root):
    """Original-native singleton census; no prepared/linker uniqueness claim."""
    identity=policy._root_schema(requested_root)
    require(isinstance(raw,bytes) and coff.digest(raw)==requested_root['object_sha256'], 'census original object differs')
    require(contract['provenance']['object_sha256']==requested_root['object_sha256'] and
            contract['provenance']['source_sha256']==requested_root['source_sha256'] and
            contract['recipe_id']==requested_root['recipe_id'], 'census checked source differs')
    obj=coff.parse(raw);section=obj['sections'].get(requested_root['section']);symbol=obj['symbols'].get(requested_root['symbol_index'])
    require(section is not None and symbol is not None and requested_root['value']==0 and requested_root['size']==section['size'] and
            (symbol['name'],symbol['section'],symbol['value'],symbol['type'],symbol['storage'],symbol['aux_count'])==
            (requested_root['symbol'],requested_root['section'],0,32,2,0), 'census exact whole original definition differs')
    native_definitions=[i for i,s in obj['symbols'].items()if s['section']==requested_root['section']and
                        (s['storage']==2 or s['type']==32)]
    require(native_definitions==[requested_root['symbol_index']], 'census has aliases/multiple original definitions')
    return dict(schema_version=1,kind='planned-code-definition-census',complete=True,
        entries=[dict(root=dict(requested_root),planned_canonical_name=policy.pool.canonical(identity))])


def assess_native_definition(raw,contract,negative_base,requested_root,*,policy_id):
    """Structured native-census preflight, not a broad integrity-error catch."""
    require(policy_id==POLICY,'explicit native COMDAT census opt-in required')
    require(hashlib.sha256(Path(policy.__file__).read_bytes()).hexdigest()==WITNESS_PIN,'accepted witness source changed')
    policy._producers();policy._root_schema(requested_root)
    require(isinstance(raw,bytes) and 0<len(raw)<=16*1024**2 and coff.digest(raw)==requested_root['object_sha256'],
            'native census raw object/hash differs')
    require(type(contract)is dict and set(contract)==policy.CONTRACT_KEYS and type(negative_base)is dict,
            'native census contract/base schema differs')
    provenance=contract['provenance'];native={k:requested_root[k]for k in policy.NATIVE_KEYS}
    require(provenance.get('object_sha256')==requested_root['object_sha256'] and
            provenance.get('source_sha256')==requested_root['source_sha256'] and
            provenance.get('recipe_id')==contract['recipe_id']==requested_root['recipe_id'] and
            type(provenance.get('recipe_index'))is int and provenance['recipe_index']==requested_root['recipe_index'],
            'native census source/recipe differs')
    require(exact(contract['roots'],[native])and exact(negative_base.get('roots'),[native]) and
            negative_base.get('policy_id')==ordinary.POLICY and negative_base.get('closure_observed')is False,
            'native census original negative singleton scope differs')
    before=digest(dict(contract=contract,base=negative_base,root=requested_root))
    obj=coff.parse(raw)
    require(exact(ordinary.assess_object(obj,contract),negative_base),'native census negative graph replay differs')
    s=obj['symbols'].get(requested_root['symbol_index']);sec=obj['sections'].get(requested_root['section'])
    require(s is not None and sec is not None and
            (s['name'],s['section'],s['value'])==(requested_root['symbol'],requested_root['section'],requested_root['value']),
            'declared native symbol identity contradicts original object')
    blockers=[]
    def block(code,evidence):blockers.append(dict(code=code,evidence=evidence))
    if (s['type'],s['storage'],s['aux_count'])!=(32,2,0):block('UNSUPPORTED_NATIVE_OWNERSHIP_FORM',requested_root['symbol_index'])
    if requested_root['value']!=0 or requested_root['size']!=sec['size'] or sec['size']!=len(sec['payload']):
        block('ROOT_NOT_EXACT_WHOLE_NATIVE_SECTION',dict(value=requested_root['value'],size=requested_root['size'],extent=sec['size']))
    if (sec['name'],sec['flags'])!=('.text',0x60501020):block('UNSUPPORTED_NATIVE_CODE_SECTION',dict(name=sec['name'],flags=sec['flags']))
    definitions=[i for i,t in obj['symbols'].items()if t['section']==requested_root['section']and(t['storage']==2 or t['type']==32)]
    if definitions!=[requested_root['symbol_index']]:block('NATIVE_ALIAS_OR_MULTIPLE_DEFINITIONS',definitions)
    aliases=[i for i,t in obj['symbols'].items()if t['name']==requested_root['symbol']]
    if aliases!=[requested_root['symbol_index']]:block('NATIVE_NAME_LOOKUP_ALIAS',aliases)
    section_symbols=[(i,t)for i,t in obj['symbols'].items()if t['section']==requested_root['section']and
                     t['name']==sec['name']and(t['storage'],t['type'],t['value'],t['aux_count'])==(3,0,0,1)]
    if len(section_symbols)!=1:block('NATIVE_SECTION_DEFINITION_NOT_UNIQUE',[i for i,_ in section_symbols])
    else:
        a=struct.unpack('<IHHIhBBH',section_symbols[0][1]['aux'])
        if a[0]!=sec['size']or a[1]!=len(sec['relocs'])or a[2]or a[4]or a[6]or a[7]:block('UNSUPPORTED_NATIVE_AUXILIARY',list(a))
        if a[5]!=2:block('NATIVE_SELECTION_IS_NOT_ANY',a[5])
    owners=[f for f in contract['unit_verified_functions']if f.get('address')==requested_root['original_address']and
            f.get('symbol')==requested_root['symbol']and all(type(f.get(k))is int for k in ('section','value','size'))and
            (f['section'],f['value'],f['size'],f.get('verdict'))==(requested_root['section'],requested_root['value'],requested_root['size'],'match')]
    if len(owners)!=1:block('NATIVE_CHECKED_OWNER_NOT_UNIQUE',len(owners))
    census=None if blockers else reconstruct_definition_census(raw,contract,requested_root)
    require(digest(dict(contract=contract,base=negative_base,root=requested_root))==before,'native census changed original negative inputs')
    return dict(schema_version=1,policy_id=POLICY,kind='comdat-any-native-definition-preflight',eligible=not blockers,
        state='qualified-native-census'if not blockers else'no-policy-for-unsupported-native-form',
        blockers=blockers,definition_census=census,object_sha256=coff.digest(raw),contract_identity_sha256=digest(contract),
        original_negative_certificate_sha256=digest(negative_base),original_blocker_ids=[b['blocker_id']for b in negative_base['blockers']],
        original_certificate_unchanged=True,candidate_policy_evaluated=False,serialization_performed=False,**FALSE)


def _summary(base,observation,discharged,remaining):
    auxiliary=observation.get('root_section_auxiliary')
    selection2=type(auxiliary)is list and len(auxiliary)==8 and type(auxiliary[5])is int and auxiliary[5]==2
    return dict(base_closure_observed=False,selection2_observed=selection2,
        root_conjunct_discharge_proved=bool(discharged),
        state='eligible-for-consumer-review' if not remaining else
              'witnessed-but-still-blocked' if selection2 else 'unsupported-native-or-policy',
        original_blocker_ids=[b['blocker_id']for b in base['blockers']],
        discharged_blocker_ids=[discharged[i]['blocker']['blocker_id']for i in sorted(discharged)],
        remaining_blocker_ids=[r['blocker']['blocker_id']for r in remaining],
        original_occurrences=len(base['blockers']),discharged_occurrences=len(discharged),remaining_occurrences=len(remaining),
        candidate_policy_blockers=observation['policy_blockers'],serialization_approved=False)


def compose(raw,contract,negative_base,witnesses,*,policy_id):
    require(policy_id==POLICY,'explicit versioned COMDAT composer opt-in required')
    require(hashlib.sha256(Path(policy.__file__).read_bytes()).hexdigest()==WITNESS_PIN,'accepted COMDAT witness source changed')
    require(isinstance(raw,bytes) and 0<len(raw)<=16*1024**2,'bounded original object bytes required')
    require(type(witnesses)is list and len(witnesses)==1,'one complete COMDAT witness wrapper required')
    wrapper=witnesses[0]
    require(type(wrapper)is dict and set(wrapper)=={'kind','definition_census','observation'} and
            wrapper['kind']==WITNESS_KIND and isinstance(wrapper['observation'],dict),'unknown COMDAT witness wrapper')
    before=digest(dict(contract=contract,base=negative_base,witnesses=witnesses))
    observation=wrapper['observation']
    fresh=policy.observe_comdat_any_code_policy(raw,contract,negative_base,observation['requested_root'],
        wrapper['definition_census'],policy_id=policy.POLICY)
    require(exact(fresh,observation),'COMDAT witness does not exactly replay source/census/negative scope')
    if observation['witness_complete']is True:
        require(exact(wrapper['definition_census'],reconstruct_definition_census(raw,contract,observation['requested_root'])),
                'complete witness census is not the exact reconstructed original definition')
    require(negative_base['policy_id']==ordinary.POLICY and negative_base['closure_observed']is False,
            'original negative ordinary certificate required')
    require(all(observation.get(flag)is False for flag in policy.FALSE),'COMDAT observation was promoted')
    ids=observation['discharge_blocker_ids']
    require(type(ids)is list and len(ids)==len(set(ids)) and len(ids)<=1,'only one exact root-conjunct discharge is supported')
    original=defaultdict(list)
    for ordinal,blocker in enumerate(negative_base['blockers'],1):original[blocker['blocker_id']].append((ordinal,blocker))
    discharged={}
    for bid in ids:
        require(observation['witness_complete']is True and observation['root_comdat2_policy_candidate']is True,
                'blocked witness cannot discharge a root policy')
        occurrences=original.get(bid,[]);require(len(occurrences)==1,'ambiguous original blocker occurrence')
        ordinal,blocker=occurrences[0]
        native={key:observation['requested_root'][key]for key in policy.NATIVE_KEYS}
        require(blocker['code']=='UNSUPPORTED_OR_PARTIAL_ROOT_SECTION' and exact(blocker['evidence'],native),
                'COMDAT witness escaped exact selected root conjunct')
        discharged[ordinal]=dict(base_blocker_ordinal=ordinal,blocker=blocker,witness_sha256=digest(wrapper),
                                witness_policy_id=policy.POLICY)
    remaining=[dict(base_blocker_ordinal=i,blocker=b)for i,b in enumerate(negative_base['blockers'],1)if i not in discharged]
    require(digest(dict(contract=contract,base=negative_base,witnesses=witnesses))==before,'composer changed proof inputs')
    require(hashlib.sha256(Path(policy.__file__).read_bytes()).hexdigest()==WITNESS_PIN,'COMDAT witness source drift')
    return dict(schema_version=1,kind='comdat-any-composed-root-observation',policy_id=POLICY,
        object_sha256=coff.digest(raw),contract_identity_sha256=digest(contract),base_certificate_sha256=digest(negative_base),
        base_policy_id=ordinary.POLICY,base_closure_observed=False,base_certificate=negative_base,
        original_certificate_unchanged=True,roots=negative_base['roots'],
        retained_section_indices=negative_base['retained_section_indices'],
        retained_primary_indices=negative_base['retained_primary_indices'],retained_physical_slots=negative_base['retained_physical_slots'],
        base_blocker_occurrences=len(negative_base['blockers']),discharged_blockers=[discharged[i]for i in sorted(discharged)],
        remaining_blocker_occurrences=remaining,remaining_blockers=[r['blocker']for r in remaining],
        composed_omission_complete=not remaining,witness_sha256=[digest(w)for w in witnesses],
        definition_census_sha256=digest(wrapper['definition_census']),witness_producer_sha256=WITNESS_PIN,
        unsupported_summary=_summary(negative_base,observation,discharged,remaining),
        selection_rewritten=False,explicit_composed_policy_required=True,collector_envelope_authentication_required=True,**FALSE)


def summarize_unsupported(raw,contract,negative_base,witnesses,composed,*,policy_id):
    """Fresh replay, ordered original IDs and no promotion of a cached result."""
    fresh=compose(raw,contract,negative_base,witnesses,policy_id=policy_id)
    require(exact(fresh,composed),'unsupported summary composition differs')
    return fresh['unsupported_summary']
