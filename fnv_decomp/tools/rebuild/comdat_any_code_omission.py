"""Synthetic-first typed COMDAT ANY CODE policy witness; never a writer.

The original negative ordinary certificate is replayed and preserved. Only its
exact selected-root conjunct blocker can be proposed for discharge. Declared
planned-definition uniqueness is not authenticated linker uniqueness.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import struct

import coff_code_archive as coff
import root_code_closure as ordinary
import runtime_code_pool as pool

POLICY = 'comdat-selection-2-owned-code-policy-v1'
CATEGORY = 'COMDAT_SELECTION_2_CODE_POLICY'
ROOT_KEYS = {'original_address','recipe_id','recipe_index','object_sha256','source_sha256',
             'symbol','symbol_index','section','value','size'}
NATIVE_KEYS = ('original_address','symbol','symbol_index','section','value','size')
CONTRACT_KEYS = {'recipe_id','roots','export_policy','verified_match','fields_complete',
    'missing_fields_complete','unit_proofs_complete','fields','missing_fields','parent_eh',
    'omission_field_proofs','unit_verified_functions','iat_import_observation','provenance'}
PINS = {'coff_code_archive.py':'76244d2d4dca4c1f8aa72224be1ef5c92f68976b5cda7d31b5cfe23d3cc29e64',
        'root_code_closure.py':'4bfdb5001380a3d7e5db7517033285d49ab211be68e2fcba15964f0ad5b03c53',
        'runtime_code_pool.py':'729f189e2893c7f3a3e3cd97df7d7381ac115169e1d75cf664e6bbc1c587b277'}
FALSE = dict(provider_selected=False,runtime_eligible=False,ABI_verified=False,link_ready=False,
    namespace_approved=False,serialization_approved=False,full_serialization_eligible=False,
    emission_performed=False,materialization_approved=False,global_link_uniqueness_proved=False,
    planned_definition_census_authenticated=False)
require = coff.require


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()


def _producers():
    for module in (coff,ordinary,pool):
        path=Path(module.__file__)
        require(hashlib.sha256(path.read_bytes()).hexdigest()==PINS[path.name], 'frozen dependency changed')
    return {'tools/rebuild/'+name:value for name,value in PINS.items()}


def _root_schema(root):
    require(isinstance(root,dict) and set(root)==ROOT_KEYS,'exact physical root schema required')
    require(all(type(root[k])is int for k in ('recipe_index','symbol_index','section','value','size')) and
            min(root['recipe_index'],root['symbol_index'],root['value'])>=0 and root['section']>0 and root['size']>0,
            'integer physical root bounds required')
    require(isinstance(root['original_address'],str) and re.fullmatch(r'0x[0-9a-f]{8}',root['original_address']) and
            isinstance(root['symbol'],str) and root['symbol'] and isinstance(root['recipe_id'],str) and root['recipe_id'],
            'invalid root address/spelling/recipe')
    require(all(isinstance(root[k],str) and re.fullmatch('[0-9a-f]{64}',root[k]) for k in ('object_sha256','source_sha256')),
            'invalid source/object digest')
    require(int(root['original_address'],16)+root['size']<=0x100000000,
            'original checked CODE extent wraps 32-bit address space')
    return {k:root[k] for k in ('recipe_id','object_sha256','symbol_index')}


def _census(census):
    require(isinstance(census,dict) and set(census)=={'schema_version','kind','complete','entries'} and
            type(census['schema_version'])is int and census['schema_version']==1 and
            census['kind']=='planned-code-definition-census' and census['complete']is True and
            type(census['entries'])is list and len(census['entries'])<=100000,
            'complete explicit planned-definition census required')
    entries=[]
    for entry in census['entries']:
        require(isinstance(entry,dict) and set(entry)=={'root','planned_canonical_name'},'definition entry schema differs')
        identity=_root_schema(entry['root'])
        require(entry['planned_canonical_name']==pool.canonical(identity),'planned name is not original physical identity')
        entries.append((entry,identity))
    return entries


def observe_comdat_any_code_policy(raw,contract,negative_base,requested_root,definition_census,*,policy_id):
    """Return a candidate witness or explicit blocked candidate, without edits.

    Malformed/stale identities and incomplete evidence raise ValueError. Valid
    but unsupported physical forms or nonunique/stale plans produce a blocked
    witness with no discharge. Runtime and collector authentication stay false.
    """
    require(policy_id==POLICY,'explicit COMDAT ANY CODE policy opt-in required')
    dependencies=_producers()
    require(isinstance(raw,bytes) and 0<len(raw)<=16*1024**2,'bounded original object bytes required')
    require(isinstance(contract,dict) and set(contract)==CONTRACT_KEYS and isinstance(negative_base,dict),
            'complete contract/original certificate schema required')
    identity=_root_schema(requested_root);entries=_census(definition_census)
    object_hash=coff.digest(raw);provenance=contract['provenance']
    require(provenance.get('object_sha256')==requested_root['object_sha256']==object_hash and
            provenance.get('source_sha256')==requested_root['source_sha256'] and
            provenance.get('recipe_id')==contract['recipe_id']==requested_root['recipe_id'] and
            type(provenance.get('recipe_index'))is int and provenance['recipe_index']==requested_root['recipe_index'],
            'source/object/recipe identity differs')
    native={k:requested_root[k] for k in NATIVE_KEYS}
    require(contract['roots']==negative_base.get('roots')==[native] and
            digest(contract['roots'])==digest([native]) and digest(negative_base['roots'])==digest([native]),
            'exact typed selected singleton scope required')
    require(negative_base.get('policy_id')==ordinary.POLICY and negative_base.get('closure_observed')is False,
            'original negative frozen ordinary certificate required')
    before=digest(dict(contract=contract,base=negative_base,root=requested_root,census=definition_census))
    obj=coff.parse(raw)
    replay=ordinary.assess_object(obj,contract)
    require(replay==negative_base and digest(replay)==digest(negative_base) and
            negative_base['contract_identity_sha256']==digest(contract),'original negative certificate does not replay')
    blockers=[]
    def block(code,evidence):blockers.append(dict(code=code,evidence=evidence))
    canonical_name=pool.canonical(identity)
    relevant=[entry for entry,ident in entries if entry['root']['original_address']==requested_root['original_address'] or
              ident==identity or entry['planned_canonical_name']==canonical_name]
    if len(relevant)!=1:block('MISSING_OR_MULTIPLE_PLANNED_DEFINITIONS',len(relevant))
    elif relevant[0]['root']!=requested_root:block('STALE_PLANNED_DEFINITION',digest(relevant[0]))

    symbols,sections=obj['symbols'],obj['sections'];sn=requested_root['section'];si=requested_root['symbol_index']
    sec=sections.get(sn);root=symbols.get(si);auxiliary=None;section_symbol_index=None
    if root is None or sec is None:
        block('MISSING_NATIVE_ROOT',dict(section=sn,symbol_index=si))
    else:
        if (root['name'],root['section'],root['value'],root['type'],root['storage'],root['aux_count'])!=(
                requested_root['symbol'],sn,requested_root['value'],32,2,0):block('ROOT_OWNED_DEFINITION_DIFFERS',si)
        if requested_root['value']!=0 or requested_root['size']!=sec['size'] or sec['size']!=len(sec['payload']):
            block('ROOT_NOT_EXACT_WHOLE_SECTION',dict(value=requested_root['value'],size=requested_root['size'],extent=sec['size']))
        if (sec['name'],sec['flags'])!=('.text',0x60501020):
            block('ROOT_CODE_NAME_OR_FLAGS_DIFFER',dict(name=sec['name'],flags=sec['flags']))
        definitions=[i for i,s in symbols.items() if s['section']==sn and not(s['storage']==3 and s['type']==0 and
            s['value']==0 and s['name']==sec['name'] and s['aux_count']==1) and (s['storage']==2 or s['type']==32)]
        if definitions!=[si]:block('ALIASED_OR_MULTIPLE_ROOT_DEFINITIONS',definitions)
        same_name=[i for i,s in symbols.items() if s['name']==requested_root['symbol']]
        if same_name!=[si]:block('ROOT_SPELLING_ALIAS_OR_LOOKUP',same_name)
        section_symbols=[(i,s) for i,s in symbols.items() if s['section']==sn and s['name']==sec['name'] and
                         s['storage']==3 and s['type']==0 and s['value']==0 and s['aux_count']==1]
        if len(section_symbols)!=1:block('ROOT_SECTION_DEFINITION_NOT_UNIQUE',[i for i,_ in section_symbols])
        else:
            section_symbol_index,s=section_symbols[0];a=struct.unpack('<IHHIhBBH',s['aux']);auxiliary=list(a)
            if a[0]!=sec['size'] or a[1]!=len(sec['relocs']) or a[2] or a[4] or a[6] or a[7]:
                block('ROOT_SECTION_AUXILIARY_DIFFERS',auxiliary)
            if a[5]!=2:block('ROOT_IS_NOT_COMDAT_SELECTION_2',a[5])
        owned=[f for f in contract['unit_verified_functions'] if f.get('address')==requested_root['original_address'] and
               f.get('symbol')==requested_root['symbol'] and f.get('section')==sn and
               all(type(f.get(k))is int for k in ('section','value','size')) and
               f.get('value')==requested_root['value'] and f.get('size')==requested_root['size'] and f.get('verdict')=='match']
        if len(owned)!=1:block('EXACT_CHECKED_NATIVE_OWNER_NOT_UNIQUE',len(owned))

    # This initial profile does not infer permission for storage or special
    # domains elsewhere in the recipe. Such evidence needs a separate policy.
    debug_drops={r['index'] for r in negative_base['sections'] if r['disposition']=='OMIT_PROVED_DEBUG_ASSOCIATION'}
    for number,s in sections.items():
        if s['name'] in ('.data','.bss','.rdata','.rdata$r'):
            block('UNOWNED_OR_SHARED_DATA_SECTION',dict(section=number,name=s['name']))
        elif s['name'] not in ('.text','.drectve','.debug$S','.debug$F'):
            block('SPECIAL_OR_UNKNOWN_SECTION_REQUIRES_SEPARATE_PROOF',dict(section=number,name=s['name']))
        if s['name']=='.text' and s['flags']!=0x60501020:block('UNKNOWN_OTHER_CODE_SECTION_FLAGS',number)
    for index,s in symbols.items():
        if s['storage']==105 or(s['section']==0 and s['value']):block('WEAK_OR_COMMON_RECORD_UNSUPPORTED',index)
        if s['storage']==6:block('LOCAL_LABEL_REQUIRES_SEPARATE_PROOF',index)
        if re.match(r'(?i)^(?:_+(?:eh|unwind|catch|tls|CxxFrame|SEH|xi_|xc_|xp_|xt_)|\?\?_[R78])',s['name']):
            block('SPECIAL_COMPILER_IDENTITY_REQUIRES_SEPARATE_PROOF',index)
        if s['aux_count'] and not(s['storage']==103 and s['section']==-2):
            is_section=(s['storage']==3 and s['type']==0 and s['value']==0 and s['section']>0 and
                        s['name']==sections[s['section']]['name'] and s['aux_count']==1)
            if not is_section:block('UNKNOWN_AUXILIARY_OR_HIDDEN_INDEX',index);continue
            a=struct.unpack('<IHHIhBBH',s['aux']);other=sections[s['section']]
            if a[0]!=other['size'] or a[1]!=len(other['relocs']) or a[2] or a[6] or a[7]:
                block('UNKNOWN_SECTION_AUXILIARY',index)
            if a[5]==5:
                if s['section'] not in debug_drops:block('UNKNOWN_ASSOCIATION_REQUIRES_SEPARATE_PROOF',index)
            elif a[4] or a[5] not in(0,1,2):block('UNKNOWN_SELECTION_OR_HIDDEN_ASSOCIATION',index)
    if contract['missing_fields']:block('MISSING_ORIGINAL_FIELD_PROOF',digest(contract['missing_fields']))
    if contract['parent_eh']:block('PARENT_EH_REQUIRES_SEPARATE_PROOF',digest(contract['parent_eh']))
    refs={(r['section'],r['offset'],r['symbol_index'],r['kind']):r for r in negative_base['references']}
    if len(refs)!=len(negative_base['references']) or len(refs)!=len(contract['fields']):
        block('FIELD_PROOF_COVERAGE_NOT_UNIQUE',dict(references=len(refs),fields=len(contract['fields'])))
    for field in contract['fields']:
        rel=field['coff_relocation']
        typed=(all(type(rel.get(k))is int for k in ('symbol_index','kind','offset','addend','width',
                                                  'symbol_section','symbol_value','symbol_type','symbol_storage')) and
               all(type(field.get(k))is int for k in ('physical_section','physical_offset','source_field_offset','physical_field_overlap_count')))
        key=(field['physical_section'],rel['offset'],rel['symbol_index'],rel['kind']);ref=refs.get(key)
        if not typed or rel.get('width')!=4 or ref is None or ref['binding_row_sha256']!=digest(field):
            block('EXACT_TYPED_FIELD_LEDGER_REQUIRED',list(key));continue
        if ref['role'] in ('data','iat-cell'):
            block('UNOWNED_OR_SHARED_DATA_REFERENCE',dict(symbol_index=rel['symbol_index'],role=ref['role']))
        if ref['role'] not in ('code','crt-contract') or rel.get('symbol_type')!=32:
            block('FIELD_TYPE_OR_ROLE_REQUIRES_SEPARATE_PROOF',list(key))
    # Preserve all independent observations. Only an exact instance of the
    # conflated root-conjunct blocker can be proposed for discharge.
    candidates=[b for b in negative_base['blockers'] if b['code']=='UNSUPPORTED_OR_PARTIAL_ROOT_SECTION' and b['evidence']==native]
    if len(candidates)!=1:block('EXACT_ROOT_CONJUNCT_BLOCKER_NOT_UNIQUE',len(candidates))
    for b in negative_base['blockers']:
        if b not in candidates:
            block('INDEPENDENT_BASE_POLICY_REMAINS',dict(blocker_id=b['blocker_id'],code=b['code']))
    complete=not blockers
    discharge=[candidates[0]['blocker_id']] if complete else []
    remaining=[b for b in negative_base['blockers'] if b['blocker_id']not in discharge]
    require(digest(dict(contract=contract,base=negative_base,root=requested_root,census=definition_census))==before,
            'policy observation changed original inputs')
    require(_producers()==dependencies,'frozen source drift during observation')
    return dict(schema_version=1,kind='typed-comdat-any-code-policy-candidate-witness',policy_id=POLICY,
        semantic_category=CATEGORY,object_sha256=object_hash,source_sha256=requested_root['source_sha256'],
        recipe_id=requested_root['recipe_id'],requested_root=requested_root,contract_identity_sha256=digest(contract),
        original_negative_certificate_sha256=digest(negative_base),definition_census_sha256=digest(definition_census),
        planned_canonical_name=canonical_name,planned_definition_observations=len(relevant),
        root_section_definition_symbol_index=section_symbol_index,root_section_auxiliary=auxiliary,
        root_section_name=sec['name'] if sec else None,root_section_flags=sec['flags'] if sec else None,
        root_section_extent=sec['size'] if sec else None,
        root_payload_sha256=coff.digest(sec['payload']) if sec else None,
        root_relocation_metadata_sha256=digest(sec['relocs']) if sec else None,
        root_relocations=[dict(offset=off,symbol_index=index,kind=kind,
                              addend_bits=int.from_bytes(sec['payload'][off:off+4],'little') if kind in(6,20) else None)
                          for off,index,kind in sec['relocs']] if sec else [],
        complete_root_field_proof_sha256=digest(contract['fields']),
        original_numeric_primary_indices=sorted(symbols),original_physical_slots=obj['symbol_count'],
        retained_physical_slots=negative_base['retained_physical_slots'],
        witness_complete=complete,root_comdat2_policy_candidate=complete,policy_blockers=blockers,
        discharge_blocker_ids=discharge,remaining_base_blockers=remaining,base_closure_observed=False,
        original_certificate_unchanged=True,original_object_changed=False,selection_rewritten=False,
        candidate_only=True,collector_envelope_authentication_required=True,dependency_tools_sha256=dependencies,**FALSE)
