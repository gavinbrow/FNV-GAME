"""Finite UUID projection. Pure in-memory transforms; caller owns authority gates."""
from collections import defaultdict
import json
import re
import struct
import coff_code_archive as coff
import runtime_code_pool as pool
import root_code_closure as ordinary
import uuid_directive_root_composer as composer
import uuid_directive_occurrence_witness as uuid_witness
import local_label_projection as labels
import ordinary_relocation_projection as fields
import ordinary_code_projection as schema
import bulk_code_pool as bulk
POLICY = 'finite-uuid-singleton-projection-v1'
require=coff.require
digest=fields.digest
UnsupportedRoot=fields.UnsupportedRoot
support=fields.support
FALSE=dict(fields.FALSE, namespace_approved=False, full_serialization_eligible=False)

def _identity_core(raw, contract, base, witnesses, composed, requested, providers, existing_exports, policy_id, *, roots, compose_fn):
    require(policy_id == POLICY, 'explicit UUID projection policy required')
    require(type(raw) is bytes and 0 < len(raw) <= 16*1024**2, 'object bound')
    require(type(contract) is dict and set(contract) == schema.CONTRACT_KEYS, 'complete exact ordinary contract required')
    require(type(base) is dict and type(composed) is dict and type(providers) is dict, 'proof schema')
    require(type(requested) is list and len(requested)==1 and type(requested[0]) is dict and
            set(requested[0])==schema.ROOT_KEYS, 'exact singleton root required')
    root=requested[0]; provenance=contract['provenance']; original_hash=coff.digest(raw)
    require(root.get('original_address') in roots, 'unsupported finite root')
    require(all(type(root[k]) is int for k in ('recipe_index','symbol_index','section','value','size')),
            'integer root identity required')
    fields.address(root['original_address'])
    require(root['value']==0 and root['size']>0 and type(root['source_sha256']) is str and
            re.fullmatch('[0-9a-f]{64}',root['source_sha256']), 'whole checked source root required')
    require(root['object_sha256']==provenance.get('object_sha256')==original_hash and
            root['source_sha256']==provenance.get('source_sha256') and
            root['recipe_id']==contract['recipe_id']==provenance.get('recipe_id') and
            root['recipe_index']==provenance.get('recipe_index'), 'root provenance differs')
    native={k:root[k] for k in schema.NATIVE_KEYS}
    require(contract['roots']==base.get('roots')==[native] and base.get('policy_id')==ordinary.POLICY and
            base.get('closure_observed') is False and base.get('blockers'), 'original negative root required')
    require(not contract['missing_fields'] and not contract['parent_eh'], 'missing fields/EH unsupported')
    require(type(witnesses) is list and len(witnesses)==1 and type(witnesses[0]) is dict and
            set(witnesses[0])=={'header','binding','witness_authority','declaration','review','declaration_authority'},
            'exact single UUID proof input required')
    before=digest(dict(contract=contract,base=base,witnesses=witnesses,composed=composed))
    w=witnesses[0]
    replay=compose_fn(raw,contract,base,root,w['header'],w['binding'],w['witness_authority'],
                            w['declaration'],w['review'],w['declaration_authority'],policy_id=composer.POLICY)
    require(replay==composed and composed['base_certificate']==base and
            composed['base_certificate_sha256']==digest(base) and composed['original_closure_observed'] is False and
            composed['original_negative_unchanged'] is True and composed['structural_composition_complete'] is True and
            not composed['remaining_blocker_occurrences'] and len(composed['discharged_blocker_occurrences'])==3 and
            all(composed.get(k) is False for k in composer.FALSE), 'UUID composition replay differs')
    require(isinstance(existing_exports,(list,tuple,set,frozenset)) and
            all(isinstance(n,str) and n for n in existing_exports) and len(existing_exports)==len(set(existing_exports)),
            'complete export census required')
    identity={k:root[k] for k in ('recipe_id','object_sha256','symbol_index')};export=pool.canonical(identity)
    require(export not in existing_exports and providers.get(root['original_address'])==identity, 'root provider/export differs')
    obj=coff.parse(raw);retained=set(base['retained_primary_indices'])
    require(all(s['storage']!=6 for i,s in obj['symbols'].items() if i in retained), 'local labels unsupported')
    require(digest(dict(contract=contract,base=base,witnesses=witnesses,composed=composed))==before, 'proof input changed')
    return obj,root,native,identity,export,None,set(),before

def _identity(raw, contract, base, witnesses, composed, requested, providers, existing_exports, policy_id):
    return _identity_core(raw,contract,base,witnesses,composed,requested,providers,existing_exports,policy_id,
                          roots=uuid_witness.ROOTS,compose_fn=composer.compose)


def _plan_core(raw, contract, base, witnesses, composed, requested, providers, existing_exports, policy_id, *, identity_fn):
    obj,root,native,identity,export,label_cert,label_indices,before = identity_fn(
        raw,contract,base,witnesses,composed,requested,providers,existing_exports,policy_id)
    keep = base['retained_section_indices']; primary = base['retained_primary_indices']
    refs = {(r['section'],r['offset'],r['symbol_index'],r['kind']):r for r in base['references']}
    require(len(refs) == len(base['references']) == len(contract['fields']), 'complete physical reference coverage required')
    checked = []; provider_identities = {}; evidence = []; names = {root['symbol_index']:export}; bases = {}
    for row in contract['fields']:
        cr = row['coff_relocation']; si = cr['symbol_index']; target = obj['symbols'].get(si)
        require(all(type(cr.get(k)) is int for k in ('symbol_index','offset','kind','width','addend',
                    'symbol_section','symbol_value','symbol_type','symbol_storage')) and
                all(type(row.get(k)) is int for k in ('recipe_index','physical_section','physical_offset',
                    'source_field_offset','physical_field_overlap_count')), 'integer physical field metadata required')
        require(target is not None and cr['kind'] in (6,20) and cr['width'] == 4,
                'only exact DIR32/REL32 fields supported')
        key = (row['physical_section'],cr['offset'],si,cr['kind']); ref = refs.get(key)
        require(ref is not None and ref['binding_row_sha256'] == digest(row), 'field hash/physical scope differs')
        local = si in label_indices
        required_basis = 'EXACT_LOCAL_FUNCTION_CONTAINMENT' if local else 'OWN_RECIPE_BINDING'
        require(row.get('source_resolution_basis') == required_basis and
                row.get('proof_consistency') == 'EXACT_OWN_SOURCE_RESOLUTION' and
                row.get('recipe_index') == root['recipe_index'] and row.get('function_symbol') == root['symbol'],
                'field lacks exact checked source parent')
        base_va, final, role = ref['original_base'],ref['original_target'],ref['role']
        fields.address(base_va); fields.address(final)
        require(row.get('expected_original_target_va') == final and
                row['original_field_va'] == '0x%08x'%(fields.address(root['original_address'])+row['source_field_offset']) and
                type(row.get('original_operand')) is int and 0 <= row['original_operand'] <= 0xffffffff,
                'original operand/field geometry differs')
        observed = (row['original_operand'] + (fields.address(row['original_field_va'])+4 if cr['kind']==20 else 0)) & 0xffffffff
        require(observed == fields.address(final), 'original operand does not resolve to proved target')
        if local:
            owners = row.get('code_owners')
            require(label_cert is not None and si in primary and target['section'] == root['section'] and
                    target['storage'] in (3,6) and target['type'] == 0 and not target['aux_count'] and
                    fields.address(base_va) == fields.address(root['original_address'])+target['value'] and
                    fields.address(root['original_address']) <= fields.address(final) < fields.address(root['original_address'])+root['size'],
                    'typed retained label target escapes exact checked root')
            require(row.get('code_ownership_ambiguous') is False and isinstance(owners,list) and len(owners)==1 and
                    isinstance(owners[0],dict) and set(owners[0])=={'address','offset'} and type(owners[0]['offset'])is int and
                    owners==[dict(address=root['original_address'],offset=fields.address(final)-fields.address(root['original_address']))],
                    'typed local containment owner/offset differs')
        else:
            require(target['storage'] in (2,3) and not target['aux_count'] and target['section'] >= 0,
                    'ordinary field record outside compatible frozen classifier')
            require(isinstance(row.get('code_owners'),list), 'complete code owner observation required')
            if role != 'code':
                require(row.get('code_ownership_ambiguous') is False and not row['code_owners'] and
                        base_va not in providers and final not in providers,
                        'non-CODE role contradicts selected provider evidence')
            elif row['classification'] == 'SELECTED_CODE_ENTRY':
                require(providers.get(base_va) is not None, 'selected target provider missing')
                pool.canonical(providers[base_va]); owners = row['code_owners']
                require(len(owners)==1 and isinstance(owners[0],dict) and set(owners[0])=={'address','offset'} and
                        type(owners[0]['offset']) is int, 'selected target owner schema differs')
            elif row['classification'] == 'UNSELECTED_EXECUTABLE_TARGET_UNCLASSIFIED':
                require(base_va not in providers and final not in providers, 'unselected role contradicts provider map')
        checked.append((row,cr,si,target,ref,base_va,final,role,key,local))

    for row,cr,si,target,ref,base_va,final,role,key,local in checked:
        if local:
            name = target['name']
        else:
            cls = row['classification']
            if role == 'code':
                support(target['type']==32 and row.get('code_ownership_ambiguous') is False,
                        'UNSUPPORTED_CODE_TYPE_OR_OWNER',dict(symbol_index=si,classification=cls))
                if cls == 'SELECTED_CODE_ENTRY':
                    support(final==base_va and row['code_owners']==[dict(address=base_va,offset=0)],
                            'CODE_INTERIOR_UNSUPPORTED',dict(symbol_index=si))
                    provider_identities[base_va]=providers[base_va];name=pool.canonical(providers[base_va])
                else:
                    support(cls=='UNSELECTED_EXECUTABLE_TARGET_UNCLASSIFIED' and not row['code_owners'],
                            'UNSUPPORTED_CODE_CLASS_OR_INTERIOR',dict(symbol_index=si,classification=cls))
                    name=pool.unresolved(base_va,role)
            else:
                require(role in ('data','iat-cell','crt-contract'),'unknown field role')
                if role=='iat-cell':
                    support(cls=='IAT_POINTER_CELL_NOT_FUNCTION_BODY' and type(row.get('import_id')) is int and
                            row['import_id']>=0 and target['type']==0 and row.get('import_pointer_source_conflict') is not True,
                            'UNSUPPORTED_IAT_TYPE_OR_CONTRACT',dict(symbol_index=si))
                elif role=='crt-contract':
                    support(cls=='EXPLICIT_NORMAL_CRT_CONTRACT_CANDIDATE' and target['type']==32,
                            'UNSUPPORTED_CRT_TYPE_OR_CONTRACT',dict(symbol_index=si))
                else:
                    support(target['type']==0 and cls in ('ORIGINAL_IMAGE_DATA_REQUIRES_CANONICAL_OWNER',
                            'COMPILER_LITERAL_FULL_READONLY_NONPOINTER_EQUALITY'),
                            'UNSUPPORTED_DATA_TYPE_OR_CLASS',dict(symbol_index=si))
                name=pool.unresolved(base_va,role)
            if target['section'] not in base['retained_runtime_section_indices']:
                require(si not in names or names[si]==name,'conflicting physical canonical identity');names[si]=name
            elif si==root['symbol_index']:
                require(name==export,'retained root target provider differs')
        if not local:
            require(name not in bases or bases[name]==base_va,'canonical name has conflicting base');bases[name]=base_va
        evidence.append(dict(section=key[0],offset=key[1],symbol_index=si,kind=key[3],field_proof_sha256=digest(row),
            original_base=base_va,original_target=final,addend_bits=ref['addend_bits'],role=role,
            canonical_name=name,typed_local_label=local))

    legacy=dict(recipe_id=root['recipe_id'],source_sha256=root['source_sha256'],object_sha256=coff.digest(raw),selected=native,
        verified_match=True,fields_complete=True,missing_fields_complete=True,fields=contract['fields'],missing_fields=[],
        provider_identities=provider_identities)
    assessment=pool.assess_parsed(obj,legacy);remaining=[];typed_legacy=[]
    uuid_legacy = []
    for blocker in assessment['blockers']:
        code,e=blocker['code'],blocker['evidence']
        if code == 'UNKNOWN_DIRECTIVE_CONTRACT' and e == uuid_witness.TOKENS:
            uuid_legacy.append(blocker); continue
        label_index=e.get('symbol_index') if isinstance(e,dict) else e
        label_ok=(type(label_index)is int and label_index in label_indices and label_index in primary and
                  ((code=='UNPROVED_EXTRA_ENTRY_OR_ALIAS' and obj['symbols'][label_index]['storage']==6) or
                   (code=='UNSUPPORTED_REFERENCE_RECORD' and obj['symbols'][label_index]['storage']==6)))
        if code in fields.OMISSION_ONLY or label_ok:typed_legacy.append(blocker)
        else:remaining.append(blocker)
    require(len(uuid_legacy)==1, 'exact single UUID legacy directive observation required')
    typed_legacy.extend(uuid_legacy)
    namespace=[b for b in remaining if b['code']=='CANONICAL_NAMESPACE_COLLISION']
    support(not namespace,'CANONICAL_REFERENCE_GROUP_REQUIRES_REVIEWED_V2',namespace)
    require(not remaining,'frozen field classifier blocked: '+','.join(b['code'] for b in remaining))
    plan=assessment['extraction_plan'];conversions=sorted(c['symbol_index'] for c in base['omitted_definition_conversions'])
    require(plan['sections']==keep and plan['symbols']==primary and plan['undefined']==conversions,
            'composed and frozen field disposition scopes differ')
    for si,name in plan['bindings']:
        if si in label_indices:continue
        require(names.get(si)==name,'frozen classifier canonical namespace differs')
    require(all(obj['symbols'][si]['storage']!=2 or si in names for si in primary),'unnamespaced external record')
    canonical_groups=defaultdict(list)
    for si,name in names.items():canonical_groups[name].append(si)
    support(all(len(indices)==1 for indices in canonical_groups.values()),
            'CANONICAL_REFERENCE_GROUP_REQUIRES_REVIEWED_V2',dict(canonical_groups))
    original_names={s['name'] for s in obj['symbols'].values()}
    require(not(set(names.values()) & original_names),'preexisting canonical name collision')
    require(digest(dict(contract=contract,base=base,witnesses=witnesses,composed=composed))==before,'proof input mutation')
    return obj,root,label_cert,dict(sections=keep,symbols=primary,undefined=conversions,bindings=sorted(names.items())),evidence,bases,export,typed_legacy

def _plan(raw, contract, base, witnesses, composed, requested, providers, existing_exports, policy_id):
    return _plan_core(raw,contract,base,witnesses,composed,requested,providers,existing_exports,policy_id,
                      identity_fn=_identity)


def _assess_core(raw,contract,base,witnesses,composed,requested_roots,providers,*,existing_exports,policy_id,plan_fn):
    binding=dict(original_object_sha256=coff.digest(raw),contract_identity_sha256=digest(contract),
        original_negative_certificate_sha256=digest(base),composed_certificate_sha256=digest(composed),requested_roots=requested_roots)
    try:_,_,_,plan,evidence,bases,export,legacy=plan_fn(raw,contract,base,witnesses,composed,requested_roots,providers,existing_exports,policy_id)
    except UnsupportedRoot as unsupported:
        return dict(schema_version=1,policy_id=POLICY,eligible=False,blockers=[dict(code=unsupported.code,evidence=unsupported.evidence)],
                    serialization_performed=False,**binding,**FALSE)
    return dict(schema_version=1,policy_id=POLICY,eligible=True,blockers=[],plan=plan,fields=evidence,
        comparison_base_view=bases,exports=[export],original_negative_certificate_preserved=True,
        discharged_legacy_screening_observations=legacy,serialization_performed=False,**binding,**FALSE)

def assess_member(raw,contract,base,witnesses,composed,requested_roots,providers,*,existing_exports,policy_id):
    return _assess_core(raw,contract,base,witnesses,composed,requested_roots,providers,
                        existing_exports=existing_exports,policy_id=policy_id,plan_fn=_plan)


def _verify_directive_mapping(output, section_map, header, raw_section_hex):
    """Check mapped COFF layout; original header bytes remain evidence only."""
    oldidx=header['index']; require(oldidx in section_map, 'directive section omitted')
    require(len(set(section_map.values()))==len(section_map), 'nonbijective section map')
    newidx=section_map[oldidx]; require(type(newidx) is int and newidx>=1, 'invalid mapped index')
    off=20+40*(newidx-1); require(off+40<=len(output), 'mapped directive header bounds')
    machine,count,_,_,_,optional,_=struct.unpack_from('<HHIIIHH',output,0)
    require(machine==0x14c and optional==0 and count==len(section_map) and newidx<=count,
            'mapped COFF header differs')
    name,vs,va,size,ptr,rp,lp,nr,nl,flags=struct.unpack_from('<8sIIIIIIHHI',output,off)
    require((name.rstrip(b'\0'),vs,va,size,flags,nr,nl,rp,lp)==
            (b'.drectve',0,0,93,0x100a00,0,0,0,0), 'mapped directive semantic header differs')
    require(ptr>=20+40*count and ptr+size<=len(output) and
            output[ptr:ptr+size]==bytes.fromhex(raw_section_hex), 'directive payload or mapped bounds differs')


def _project_core(raw,contract,base,witnesses,composed,requested_roots,providers,*,existing_exports,policy_id,plan_fn):
    obj,root,label_cert,plan,evidence,bases,export,legacy=plan_fn(
        raw,contract,base,witnesses,composed,requested_roots,providers,existing_exports,policy_id)
    before=digest(dict(contract=contract,base=base,witnesses=witnesses,composed=composed))
    if label_cert is None:
        selected,maps=coff.serialize(raw,plan['sections'],plan['symbols'],plan['undefined']);writer=coff.__name__
    else:
        selected,maps,label_receipt=labels.serialize_labels(raw,plan['sections'],plan['symbols'],plan['undefined'],label_cert)
        labels.verify_label_selection(raw,selected,maps,label_cert);writer=labels.POLICY
    projected_bindings=[(maps['symbol_map'][i],name) for i,name in plan['bindings']]
    output=coff.namespace(selected,projected_bindings)
    after=coff.parse(output);sm,ym,am=bulk.slot_maps(obj,plan['sections'],plan['symbols'])
    require(maps['section_map']==sm and maps['symbol_map']==ym and maps['auxiliary_map']==am,'physical map bijection differs')
    expected_slots=sorted(k for i in plan['symbols'] for k in range(i,i+1+obj['symbols'][i]['aux_count']))
    require(expected_slots==base['retained_physical_slots'],'exact retained slot universe differs')
    require(coff.exports(output)==[export],'only selected root export allowed')
    for old,new in sm.items():
        a,b=obj['sections'][old],after['sections'][new]
        require(all(a[k]==b[k] for k in ('name','flags','payload','size')) and
                b['relocs']==[(off,ym[si],kind) for off,si,kind in a['relocs']],'payload/addend/relocation target changed')
    for old,new in ym.items():
        a,b=obj['symbols'][old],after['symbols'][new]
        typed_local = label_cert is not None and old in json.loads(label_cert.decision_json)['labels']
        if typed_local:
            require(b['storage']==a['storage'] and b['name']==a['name'] and b['value']==a['value'] and b['type']==a['type'] and
                    b['section']==sm[a['section']] and old not in plan['undefined'],'LABEL class/value/name changed')
    _verify_directive_mapping(output, sm, witnesses[0]['header'], composed['proposal']['raw_section_hex'])
    require(digest(dict(contract=contract,base=base,witnesses=witnesses,composed=composed))==before,'negative proof input mutated')
    names=dict(plan['bindings']);undefined=[dict(original_symbol_index=i,serialized_symbol_index=ym[i],name=names[i],
        original_base=next(e['original_base'] for e in evidence if e['symbol_index']==i))
        for i in plan['symbols'] if after['symbols'][ym[i]]['section']==0]
    return output,dict(schema_version=1,policy_id=POLICY,original_object_sha256=coff.digest(raw),output_sha256=coff.digest(output),
        contract_identity_sha256=digest(contract),original_negative_certificate_sha256=digest(base),
        composed_certificate_sha256=digest(composed),original_negative_certificate_preserved=True,base_closure_observed=False,
        discharged_blocker_occurrences=composed['discharged_blocker_occurrences'],requested_roots=requested_roots,maps=maps,exports=[export],
        namespace_bindings=plan['bindings'],comparison_base_view=bases,fields=evidence,undefined=undefined,
        original_physical_namespace_plan=plan['bindings'],projected_namespace_bindings=projected_bindings,
        namespace_after_selection=True,local_labels_resolve_by='checked-function-section-plus-value-and-addend',
        local_label_names_added_to_base_view=False,writer_policy=writer,class6_disguised=False,
        discharged_legacy_screening_observations=legacy,**FALSE)


def project_member(raw,contract,base,witnesses,composed,requested_roots,providers,*,existing_exports,policy_id):
    return _project_core(raw,contract,base,witnesses,composed,requested_roots,providers,
                         existing_exports=existing_exports,policy_id=policy_id,plan_fn=_plan)
