"""New pure COMDAT ANY consumer; frozen policies and writers stay unchanged."""
from __future__ import annotations
import struct

import coff_code_archive as coff
import runtime_code_pool as pool
import bulk_code_pool as bulk
import ordinary_relocation_projection as field_common
import comdat_any_root_composer as composer

POLICY = 'comdat-any-singleton-code-projection-v1'
require = coff.require
digest = composer.digest
exact = composer.exact
FALSE = dict(composer.FALSE,native_tools_run=False,compiler_performed=False,
             executable_link_performed=False,game_execution_performed=False)


def _plan(raw,contract,base,witnesses,composed,requested_roots,providers,existing_exports,policy_id):
    require(policy_id==POLICY,'explicit COMDAT consumer opt-in required')
    require(type(requested_roots)is list and len(requested_roots)==1 and isinstance(providers,dict),
            'exact singleton/provider input required')
    require(type(existing_exports)in(list,tuple,set,frozenset) and all(isinstance(n,str)and n for n in existing_exports) and
            len(existing_exports)==len(set(existing_exports)),'complete noncompeting prepared export census required')
    before=digest(dict(contract=contract,base=base,witnesses=witnesses,composed=composed,roots=requested_roots,providers=providers))
    fresh=composer.compose(raw,contract,base,witnesses,policy_id=composer.POLICY)
    require(exact(fresh,composed),'versioned COMDAT composition does not exactly replay')
    require(all(composed.get(k)is False for k in composer.FALSE),'composed observation was promoted')
    root=requested_roots[0];observed_root=witnesses[0]['observation']['requested_root']
    require(exact(root,observed_root),'requested original physical root differs')
    native={k:root[k]for k in composer.policy.NATIVE_KEYS}
    identity={k:root[k]for k in ('recipe_id','object_sha256','symbol_index')};name=pool.canonical(identity)
    require(exact(providers.get(root['original_address']),identity),'selected original root provider differs')
    require(name not in existing_exports,'prepared canonical root cannot be emitted again')
    binding=dict(original_object_sha256=coff.digest(raw),contract_identity_sha256=digest(contract),
        original_negative_certificate_sha256=digest(base),composed_certificate_sha256=digest(composed),
        requested_roots=requested_roots,definition_census_sha256=composed['definition_census_sha256'])
    if not composed['composed_omission_complete']:
        return dict(eligible=False,blockers=composed['remaining_blockers'],binding=binding,
                    unsupported_summary=composed['unsupported_summary'])
    require(len(composed['discharged_blockers'])==1 and len(base['blockers'])==1 and base['closure_observed']is False,
            'only the exact COMDAT root conjunct may be discharged')
    obj=coff.parse(raw);secs,syms=obj['sections'],obj['symbols'];keep=base['retained_section_indices']
    refs={(r['section'],r['offset'],r['symbol_index'],r['kind']):r for r in base['references']}
    require(len(refs)==len(base['references'])==len(contract['fields']),'full unique field proof required')
    provider_identities={};checked=[];names={root['symbol_index']:name};bases={name:root['original_address']}
    for row in contract['fields']:
        cr=row['coff_relocation'];si=cr['symbol_index'];target=syms[si]
        require(all(type(cr.get(k))is int for k in ('symbol_index','offset','kind','width','addend',
            'symbol_section','symbol_value','symbol_type','symbol_storage')) and
            all(type(row.get(k))is int for k in ('recipe_index','physical_section','physical_offset','source_field_offset',
                                               'physical_field_overlap_count','original_operand')),'typed native field metadata required')
        key=(row['physical_section'],cr['offset'],si,cr['kind']);ref=refs.get(key)
        require(ref is not None and ref['binding_row_sha256']==digest(row) and cr['kind']in(6,20)and cr['width']==4,
                'exact original DIR32/REL32 field identity required')
        require(row.get('proof_consistency')=='EXACT_OWN_SOURCE_RESOLUTION' and row.get('recipe_index')==root['recipe_index'] and
                row.get('function_symbol')==root['symbol'] and row.get('source_resolution_basis')=='OWN_RECIPE_BINDING',
                'field source/parent binding differs')
        base_va,final,role=ref['original_base'],ref['original_target'],ref['role']
        field_common.address(base_va);field_common.address(final)
        require(row.get('expected_original_target_va')==final and
                row['original_field_va']=='0x%08x'%(field_common.address(root['original_address'])+row['source_field_offset']) and
                0<=row['original_operand']<=0xffffffff,'original field/operand geometry differs')
        observed=(row['original_operand']+(field_common.address(row['original_field_va'])+4 if cr['kind']==20 else 0))&0xffffffff
        require(observed==field_common.address(final),'original field operand target differs')
        require(role in('code','crt-contract')and target['type']==32 and target['storage']in(2,3)and
                target['section']>=0 and not target['aux_count'],'DATA/special field is outside CODE policy')
        require(row.get('code_ownership_ambiguous')is False and type(row.get('code_owners'))is list,'code owner ambiguity/schema')
        self_reference=target['section']==root['section']
        if self_reference:
            require(si==root['symbol_index'] and target['value']==0 and base_va==root['original_address'] and role=='code',
                    'retained alias or unowned interior target')
            offset=field_common.address(final)-field_common.address(root['original_address']);owners=row['code_owners']
            require(0<=offset<root['size'] and len(owners)==1 and type(owners[0])is dict and
                    set(owners[0])=={'address','offset'} and type(owners[0]['offset'])is int and
                    exact(owners,[dict(address=root['original_address'],offset=offset)]),'self reference escapes checked root/owner')
            require(row['classification']in('SELECTED_CODE_ENTRY','UNIQUE_CODE_INTERIOR_OR_LOCAL_LABEL_NOT_CALLABLE_APPROVAL'),
                    'unknown self reference role')
        elif role=='code' and row['classification']=='SELECTED_CODE_ENTRY':
            owners=row['code_owners'];require(len(owners)==1 and type(owners[0])is dict and set(owners[0])=={'address','offset'} and
                type(owners[0]['offset'])is int and exact(owners,[dict(address=base_va,offset=0)]) and final==base_va,
                'external CODE target is not an exact selected entry')
            require(base_va in providers,'selected external provider missing');pool.canonical(providers[base_va])
            provider_identities[base_va]=providers[base_va]
        else:
            require(not row['code_owners'] and base_va not in providers and final not in providers,
                    'unresolved role contradicts selected owner map')
            require((role=='code' and row['classification']=='UNSELECTED_EXECUTABLE_TARGET_UNCLASSIFIED')or
                    (role=='crt-contract' and row['classification']=='EXPLICIT_NORMAL_CRT_CONTRACT_CANDIDATE'),
                    'unknown CODE/CRT field contract')
        checked.append((row,cr,ref,self_reference))
    legacy=dict(recipe_id=root['recipe_id'],source_sha256=root['source_sha256'],object_sha256=coff.digest(raw),selected=native,
        verified_match=True,fields_complete=True,missing_fields_complete=True,fields=contract['fields'],missing_fields=[],
        provider_identities=provider_identities)
    assessment=pool.assess_parsed(obj,legacy);allowed=[]
    section_definition=[(i,s)for i,s in syms.items()if s['section']==root['section']and s['name']=='.text'and
                        s['storage']==3 and s['type']==0 and s['value']==0 and s['aux_count']==1]
    require(len(section_definition)==1,'root auxiliary ownership differs')
    expected_evidence=[(section_definition[0][0],list(struct.unpack('<IHHIhBBH',section_definition[0][1]['aux'])))]
    for blocker in assessment['blockers']:
        require(blocker['code']=='UNSUPPORTED_ROOT_COMDAT' and exact(blocker['evidence'],expected_evidence),
                'independent legacy field/namespace policy cannot be discharged')
        allowed.append(blocker)
    require(len(allowed)==1,'exact legacy Selection2 conjunct observation required')
    plan=assessment['extraction_plan'];conversions=sorted(r['symbol_index']for r in base['omitted_definition_conversions'])
    require(exact(plan['sections'],base['retained_section_indices']) and exact(plan['symbols'],base['retained_primary_indices']) and
            exact(plan['undefined'],conversions),'negative/composed/field extraction scope differs')
    plan_names=dict(plan['bindings']);require(plan_names.get(root['symbol_index'])==name,'original root canonical identity changed')
    evidence=[]
    for row,cr,ref,self_reference in checked:
        si=cr['symbol_index'];base_va,role=ref['original_base'],ref['role']
        expected=name if self_reference else pool.canonical(provider_identities[base_va])if base_va in provider_identities else pool.unresolved(base_va,role)
        require(plan_names.get(si)==expected,'canonical field identity differs from frozen classifier')
        require(expected not in bases or bases[expected]==base_va,'one canonical field name has conflicting base')
        bases[expected]=base_va
        evidence.append(dict(section=row['physical_section'],offset=cr['offset'],symbol_index=si,kind=cr['kind'],
            addend_bits=ref['addend_bits'],original_base=base_va,original_target=ref['original_target'],role=role,
            canonical_name=expected,field_proof_sha256=digest(row),retained_self_reference=self_reference))
    require(len(plan_names)==len(plan['bindings'])and len(set(plan_names.values()))==len(plan_names),'uncertified duplicate namespace')
    require(digest(dict(contract=contract,base=base,witnesses=witnesses,composed=composed,roots=requested_roots,providers=providers))==before,
            'consumer changed source proof inputs')
    return dict(eligible=True,blockers=[],obj=obj,plan=plan,binding=binding,fields=evidence,bases=bases,export=name,
                legacy_conjunct=allowed[0],root=root,unsupported_summary=composed['unsupported_summary'])


def assess_member(raw,contract,base,witnesses,composed,requested_roots,providers,*,existing_exports,policy_id):
    result=_plan(raw,contract,base,witnesses,composed,requested_roots,providers,existing_exports,policy_id)
    public={k:v for k,v in result.items()if k not in('obj','root')}
    return dict(schema_version=1,policy_id=POLICY,serialization_performed=False,artifact_disk_write_performed=False,**public,**FALSE)


def project_member(raw,contract,base,witnesses,composed,requested_roots,providers,*,existing_exports,policy_id):
    result=_plan(raw,contract,base,witnesses,composed,requested_roots,providers,existing_exports,policy_id)
    require(result['eligible'],'incomplete COMDAT policy cannot authorize serialization')
    plan,obj,root=result['plan'],result['obj'],result['root']
    named=coff.namespace(raw,plan['bindings']);output,maps=coff.serialize(named,plan['sections'],plan['symbols'],plan['undefined'])
    coff.verify_selection(named,output,maps);sm,ym,am=bulk.slot_maps(obj,plan['sections'],plan['symbols'])
    require(exact(maps['section_map'],sm)and exact(maps['symbol_map'],ym)and exact(maps['auxiliary_map'],am),'physical slot bijection differs')
    after=coff.parse(output);require(coff.exports(output)==[result['export']],'only selected original root may be defined')
    for old,new in sm.items():
        a,b=obj['sections'][old],after['sections'][new]
        require(all(a[k]==b[k]for k in('name','size','flags','payload'))and
                b['relocs']==[(off,ym[index],kind)for off,index,kind in a['relocs']],'payload/addend/original physical target changed')
    root_aux=[s['aux']for s in obj['symbols'].values()if s['section']==root['section']and s['name']=='.text'and s['aux_count']==1]
    output_aux=[s['aux']for s in after['symbols'].values()if s['section']==sm[root['section']]and s['name']=='.text'and s['aux_count']==1]
    require(root_aux==output_aux and len(root_aux)==1 and struct.unpack('<IHHIhBBH',output_aux[0])[5]==2,'Selection2 auxiliary changed')
    names=dict(plan['bindings']);undefined=[dict(original_symbol_index=i,serialized_symbol_index=ym[i],name=names[i],
        original_base=next(e['original_base']for e in result['fields']if e['symbol_index']==i))
        for i in plan['symbols']if after['symbols'][ym[i]]['section']==0]
    return output,dict(schema_version=1,policy_id=POLICY,output_sha256=coff.digest(output),maps=maps,
        exports=[result['export']],namespace_bindings=plan['bindings'],comparison_base_view=result['bases'],fields=result['fields'],
        undefined=undefined,legacy_conjunct_observation=result['legacy_conjunct'],original_negative_certificate_preserved=True,
        selection2_auxiliary_preserved=True,selection_rewritten=False,serialization_performed=True,artifact_disk_write_performed=False,
        **result['binding'],**FALSE)
