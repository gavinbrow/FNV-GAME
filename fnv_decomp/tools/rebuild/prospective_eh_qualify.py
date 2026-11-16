"""Pure fixed-seven EH claim accounting; no observation, proof replay or admission.

Externally supplied anchors are comparison expectations, not independently
verified authority. Even consistent authored claims leave every obligation open.
"""
from __future__ import annotations
import copy
import hashlib
import json

ROOTS = {'0x00c546c0':1445, '0x00c55200':2769, '0x00c5f240':2770,
         '0x00c43500':2770, '0x00c65530':2779, '0x00c618f0':2779,
         '0x00c616c0':2779}
CENSUS = 'COMPLETE_PHYSICAL_FIELD_AND_TARGET_RECORD_CENSUS'
HIGHLOW = 'PE_HIGHLOW_METADATA_OWNERSHIP'
FAMILY = 'HANDLER_COOKIE_AND_CLEANUP_SEMANTIC_FAMILY'
FRAME = 'PARENT_FRAME_PRESERVATION_AND_NO_CATCH_CLASS'
SOURCE = 'CURRENT_SOURCE_BINDING'
GRAPH = 'EXPANDED_OMISSION_NAMESPACE_AND_SAFETY_CLOSURE'
SINGLE = (CENSUS, FAMILY, FRAME, SOURCE, GRAPH)
FALSE_FLAGS = dict(runtime_eligible=False, provider_selected=False,
                   ABI_verified=False, frame_execution_verified=False,
                   projection_authorized=False, full_closure_verified=False)
FAMILIES = {CENSUS:'PHYSICAL_FIELD_CENSUS_V1', HIGHLOW:'PE_HIGHLOW_SITE_V1',
            FAMILY:'OWN_HANDLER_COOKIE_CLEANUP_V1', FRAME:'OWN_FRAME_NO_CATCH_V1',
            SOURCE:'SOURCE_COMPILER_OBJECT_LINEAGE_V1', GRAPH:'EXPANDED_GRAPH_V1'}

class QualificationError(ValueError):
    """Malformed or inconsistent claim input; no qualification is produced."""

def need(condition, reason):
    if not condition:
        raise QualificationError(reason)

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                         separators=(',', ':')).encode()).hexdigest()

def hex_digest(value):
    return isinstance(value, str) and len(value)==64 and all(c in '0123456789abcdef' for c in value)

def integer(value, minimum=0):
    return type(value) is int and value >= minimum

def uint32(value, nonzero=False):
    return type(value) is int and (1 if nonzero else 0)<=value<=0xffffffff

def coff_section(value, allow_undefined=False):
    return type(value) is int and (0 if allow_undefined else 1)<=value<=0x7fff

def typed_equal(left, right):
    if type(left) is not type(right): return False
    if isinstance(left, dict):
        return set(left)==set(right) and all(typed_equal(left[k],right[k]) for k in left)
    if isinstance(left, list):
        return len(left)==len(right) and all(typed_equal(a,b) for a,b in zip(left,right))
    return left==right

def validate_anchors(anchors):
    unitkeys={str(i) for i in ROOTS.values()}
    for key in ('objects','sources'):
        need(set(anchors[key])==unitkeys and all(hex_digest(x) for x in anchors[key].values()), 'object/source anchor digest inventory')
    need(hex_digest(anchors['highlow_directory_sha256']), 'HIGHLOW directory anchor digest')
    need(set(anchors['safe_seh_counts'])==set(ROOTS) and all(integer(x,1) and x<=1024 for x in anchors['safe_seh_counts'].values()), 'SafeSEH count anchor inventory')
    for key,allowed in [('cleanup_receipts',set(ROOTS)),('frame_receipts',set(ROOTS)),('expanded_scopes',set(ROOTS)),('root_inputs',set(ROOTS)),('source_lineage',unitkeys)]:
        need(set(anchors[key])<=allowed and all(hex_digest(x) for x in anchors[key].values()), 'typed anchor digest: '+key)
    need(set(anchors['root_inputs'])==set(ROOTS), 'root input anchor inventory')
    for value in anchors['witnesses'].values():
        need(hex_digest(value['sha256']) and hex_digest(value['facts_sha256']), 'witness anchor digest')

def no_floats(value):
    if isinstance(value, float): return False
    if isinstance(value, dict): return all(no_floats(v) for v in value.values())
    if isinstance(value, list): return all(no_floats(v) for v in value)
    return True

def claim_key(root, obligation, subject):
    return root+'|'+obligation+'|'+subject

def validate_target(target, root):
    need(uint32(target['index']) and isinstance(target['name'],str) and target['name'], 'target identity')
    need(coff_section(target['section'],True) and uint32(target['value']) and integer(target['storage'])
         and integer(target['type']) and type(target['aux_count']) is int and target['aux_count']==0, 'target physical record')
    need(uint32(target['original_base'],True) and hex_digest(target['canonical_identity_sha256']), 'target original identity')
    role, domain, subtype = target['canonical_role'], target['semantic_domain'], target['contract_kind']
    allowed={'code':('code',{'ordinary-function','parent-owned-cleanup','parent-owned-handler'}),
             'data':('data',{'original-data','parent-owned-state','security-cookie'}),
             'iat-cell':('data',{'iat-cell'}),
             'crt-contract':('code',{'cxx-frame-handler','security-cookie-check'})}
    need(not target['name'].startswith(('__imp_','_imp__')) or role=='iat-cell', 'IAT spelling cannot be CODE/data witness')
    need(role in allowed and domain==allowed[role][0] and subtype in allowed[role][1], 'canonical role/domain/subtype conflict')
    if target['section']==0:
        need(target['storage']==2 and target['value']==0, 'undefined target storage/value')
        need(target['type']==(32 if domain=='code' else 0), 'undefined target code/data type')
    else:
        need(target.get('owner_root')==root, 'cross-parent target borrowing')
        need(target['storage']==3 and target['type']==(32 if domain=='code' else 0), 'owned target storage/type')

def mapped_target(row, target, addend):
    effective=target['value']+addend
    if target['section']==0:
        value=target['original_base']+addend
    elif target['section']==row['parent']['section']:
        need(0<=effective<157, 'parent target addend outside extent')
        value=int(row['root_address'],16)+effective
    elif target['semantic_domain']=='data':
        need(0<=effective<44, 'metadata target addend outside extent')
        value=row['metadata_original_base']+effective
    else:
        cuts=[x for x in row['pieces'] if x['section']==target['section'] and x['start']<=effective<x['end']]
        need(len(cuts)==1, 'target effective value outside owned cut')
        value=cuts[0]['original_start']+effective-cuts[0]['start']
    need(uint32(value,True), 'target addend uint32 overflow')
    return value

def mapped_field_site(row, field):
    if field['section']==row['parent']['section']:return int(row['root_address'],16)+field['offset']
    if field['section']==next(s['section'] for s in row['owned_sections'] if s['domain']=='data'):
        return row['metadata_original_base']+field['offset']
    cuts=[p for p in row['pieces'] if p['section']==field['section'] and p['start']<=field['offset'] and field['offset']+4<=p['end']]
    need(len(cuts)==1,'field crosses owned code cut')
    return cuts[0]['original_start']+field['offset']-cuts[0]['start']

def validate_safe_seh(row, anchors, targetmap):
    sx=row['safe_seh_inventory'];root=row['root_address']
    need(coff_section(sx['section']) and sx['section'] not in [row['parent']['section']]+[s['section'] for s in row['owned_sections']], 'SafeSEH section identity')
    count=anchors['safe_seh_counts'][root]
    need(integer(count,1) and count<=1024 and type(sx['count']) is int and sx['count']==count and sx['size']==4*count and type(sx['size']) is int, 'whole SafeSEH count/extent')
    need(sx['whole_table_captured'] is True and hex_digest(sx['table_payload_sha256']) and sx['relocation_count']==0 and type(sx['relocation_count']) is int, 'whole SafeSEH capture')
    aux=sx['section_aux'];need(typed_equal(aux,dict(kind='section-definition',length=4*count,relocations=0,selection=0,association=0)), 'SafeSEH section aux form')
    records=sx['records'];need(len(records)==count and [x['ordinal'] for x in records]==list(range(count)) and all(type(x['ordinal']) is int for x in records), 'SafeSEH ordinal inventory')
    need(len({x['target']['index'] for x in records})==count,'duplicate SafeSEH target index')
    owned=[t for t in targetmap.values() if t['contract_kind']=='parent-owned-handler'];need(len(owned)==1,'one owned native handler')
    handler=owned[0];own_count=0;unresolved=[]
    retained={row['parent']['section']}|{s['section'] for s in row['owned_sections']}
    for record in records:
        target=record['target'];need(uint32(target['index']) and isinstance(target['name'],str) and target['name'] and coff_section(target['section']) and uint32(target['value']) and type(target['storage']) is int and type(target['type']) is int and type(target['aux_count']) is int,'SafeSEH physical target types')
        need(target['storage']==3 and target['type']==32 and target['aux_count']==0,'SafeSEH target form')
        ts=record['target_section'];need(coff_section(ts['index']) and ts['index']==target['section'] and uint32(ts['extent'],True) and target['value']<ts['extent'] and uint32(ts['flags']) and ts['flags'] & 0x20000000 and ts['backed'] is True, 'SafeSEH target section domain/extent')
        if target['index']==handler['index']:
            need(record['disposition']=='retained-own' and all(typed_equal(target[k],handler[k]) for k in ('index','name','section','value','storage','type','aux_count')), 'SafeSEH owned handler index/record')
            own_count+=1
        else:
            need(target['index'] not in targetmap and target['section'] not in retained and target['section']!=sx['section'],'foreign SafeSEH retained identity')
            need(record['disposition'] in ('omission-claim','unresolved-other'),'unsupported SafeSEH disposition')
            if record['disposition']=='omission-claim':need(record['expanded_scope_sha256']==anchors['expanded_scopes'][root],'foreign SafeSEH omission scope')
            else:unresolved.append(record['ordinal'])
    need(own_count==1,'missing or duplicate owned SafeSEH handler')
    return unresolved

def validate_root(row, anchors):
    root=row['root_address']; index=ROOTS[root]
    need(type(row['recipe_index']) is int, 'recipe index type')
    need(row['recipe_index']==index, 'wrong recipe index')
    need(row['object_sha256']==anchors['objects'][str(index)] and
         row['source_context_sha256']==anchors['sources'][str(index)], 'stale object/source context')
    parent=row['parent']; need(coff_section(parent['section']) and parent['value']==0 and uint32(parent['size']) and parent['size']==157, 'parent span')
    owned=row['owned_sections']; need(len(owned)==2 and len({s['section'] for s in owned})==2, 'owned section inventory')
    sections={s['section']:s for s in owned}
    need(parent['section'] not in sections and type(parent['value']) is int, 'parent/child overlap')
    for section in owned:
        need(coff_section(section['section']) and coff_section(section['parent_section']) and section['parent_section']==parent['section'], 'stale parent association')
        need(uint32(section['size']) and uint32(section['flags']) and section['backed'] is True and bool(section['flags'] & 0x20000000)==(section['domain']=='code'), 'native section domain/backing')
    code=[s for s in owned if s['domain']=='code']; data=[s for s in owned if s['domain']=='data']
    need(len(code)==len(data)==1 and code[0]['size']==38 and data[0]['size']==44, 'owned domain/extent')
    pieces=row['pieces']; need(len(pieces)==2 and [(x['start'],x['end']) for x in pieces]==[(0,11),(11,38)], '11/27 family cuts')
    need(all(uint32(p['start']) and uint32(p['end']) and coff_section(p['section']) and p['section']==code[0]['section'] and p['owner_root']==root for p in pieces), 'foreign piece')
    need(all(type(p['MATCH']) is bool for p in pieces) and type(parent['MATCH']) is bool, 'comparison boolean')
    need(uint32(row['metadata_original_base'],True) and row['metadata_original_base']+44<=0x100000000, 'metadata original uint32 extent')
    for piece in pieces:
        need(uint32(piece['original_start'],True) and type(piece['original_end']) is int and
             piece['original_end']==piece['original_start']+piece['end']-piece['start'] and
             piece['original_end']<=0x100000000, 'original code piece uint32 extent')
    need(not (pieces[0]['original_start']<pieces[1]['original_end'] and pieces[1]['original_start']<pieces[0]['original_end']), 'overlapping original pieces')
    need(type(row['metadata_nonrelocation_MATCH']) is bool and type(row['metadata_full_MATCH']) is bool, 'metadata comparison booleans')
    inventory=row['field_inventory']; fields=row['physical_fields']
    need(len(inventory)==len(fields) and len({x['field_id'] for x in inventory})==len(inventory), 'field inventory duplicates/count')
    need(len({x['field_id'] for x in fields})==len(fields), 'duplicate physical field')
    need(typed_equal(sorted(inventory,key=lambda x:x['field_id']),sorted(fields,key=lambda x:x['field_id'])), 'incomplete physical field census')
    targets=row['targets']; need(len({t['index'] for t in targets})==len(targets), 'duplicate target index')
    targetmap={t['index']:t for t in targets}; names={}
    for target in targets:
        validate_target(target,root)
        if target['section']:
            sn=target['section'];need(sn in sections or sn==parent['section'], 'defined target outside retained owner')
            extent=157 if sn==parent['section'] else sections[sn]['size']
            domain='code' if sn==parent['section'] else sections[sn]['domain']
            need(target['value']<extent and target['semantic_domain']==domain, 'defined target extent/domain')
            if target['contract_kind'] in ('parent-owned-cleanup','parent-owned-handler'):
                part=pieces[0 if target['contract_kind']=='parent-owned-cleanup' else 1]
                need(sn==part['section'] and target['value']==part['start'] and target['original_base']==part['original_start'], 'defined code role/cut mapping')
            elif target['contract_kind']=='parent-owned-state':
                need(sn==data[0]['section'] and target['value'] in (0,8) and target['original_base']==row['metadata_original_base']+target['value'], 'defined state role/value mapping')
            else:
                need(sn==parent['section'] and target['contract_kind']=='ordinary-function' and target['original_base']==int(root,16)+target['value'], 'unsupported defined target role')
        # Identical names never make two physical records interchangeable.
        names.setdefault(target['name'],[]).append(target['index'])
    seen=[]
    for field in fields:
        need(coff_section(field['section']) and uint32(field['target_index']), 'field physical reference types')
        need(isinstance(field['field_id'],str) and field['field_id'], 'field ID')
        sn=field['section']; extent=157 if sn==parent['section'] else sections.get(sn,{}).get('size',0)
        need(field['owner_root']==root and uint32(field['offset']) and field['offset']+4<=extent, 'foreign/outside field')
        need(field['kind'] in ('DIR32','REL32') and type(field['addend']) is int and -0x80000000<=field['addend']<=0x7fffffff, 'field relocation kind/addend')
        need(field['target_index'] in targetmap, 'missing required target')
        target=targetmap[field['target_index']]
        need(field['target_name']==target['name'], 'same-name/index mismatch')
        need(uint32(field['original_site'],True) and field['original_site']==mapped_field_site(row,field),'field original site mapping')
        expected=mapped_target(row,target,field['addend'])
        need(uint32(field['original_target'],True) and type(field['comparison_MATCH']) is bool and (field['original_target']==expected)==field['comparison_MATCH'], 'field original target/verdict mapping')
        need(not any(sn==other[0] and abs(field['offset']-other[1])<4 for other in seen), 'overlapping fields')
        seen.append((sn,field['offset']))
    metadata=row['metadata_sites']; need(len(metadata)==2 and len({x['subject'] for x in metadata})==2, 'two distinct metadata sites')
    fieldmap={x['field_id']:x for x in fields}
    need(len({x['original_site'] for x in metadata})==2, 'duplicate original metadata site')
    need(sorted(x['offset'] for x in metadata)==[4,16], 'metadata state/FuncInfo field positions')
    for site in metadata:
        need(coff_section(site['section']) and uint32(site['offset']) and uint32(site['target_index']) and type(site['addend']) is int, 'metadata physical types')
        need(site['owner_root']==root and site['section']==data[0]['section'], 'foreign metadata owner')
        need(site['field_id'] in fieldmap, 'missing metadata physical field')
        field=fieldmap[site['field_id']]
        need(field['section']==site['section'] and field['offset']==site['offset'] and field['kind']=='DIR32'
             and field['target_index']==site['target_index'] and field['addend']==site['addend'], 'metadata/field join')
        need(site['original_site']==row['metadata_original_base']+site['offset'] and integer(site['original_site']), 'metadata original site')
        need(uint32(site['original_target'],True) and site['original_target']==mapped_target(row,targetmap[site['target_index']],site['addend']) and site['original_target']==field['original_target'] and site['MATCH']==field['comparison_MATCH'], 'metadata target/addend join')
        need(type(site['MATCH']) is bool, 'metadata verdict type')
    need({f['field_id'] for f in fields if f['section']==data[0]['section']}=={s['field_id'] for s in metadata}, 'extra hidden metadata field')
    info=row['funcinfo'];expected_info=dict(offset=8,magic=0x19930522,max_state=1,unwind_field_id='unwind',try_count=0,try_map=0,ip_count=0,ip_map=0,type_list=0,flags=1)
    need(typed_equal(info,expected_info), 'unsupported or absent captured FuncInfo')
    states=row['state_graph'];need(typed_equal(states,[dict(state=0,to_state=-1,action_field_id='action')]), 'missing or unsupported state transitions')
    action=fieldmap[states[0]['action_field_id']];unwind=fieldmap[info['unwind_field_id']]
    at=targetmap[action['target_index']];ut=targetmap[unwind['target_index']]
    need(action['section']==data[0]['section'] and action['offset']==4 and action['kind']=='DIR32' and
         at['section']==code[0]['section'] and at['contract_kind']=='parent-owned-cleanup' and at['value']+action['addend']==0, 'state/action/cleanup mapping')
    need(unwind['section']==data[0]['section'] and unwind['offset']==16 and unwind['kind']=='DIR32' and
         ut['section']==data[0]['section'] and ut['value']+unwind['addend']==0, 'FuncInfo/unwind map ownership')
    need(set(targetmap)=={f['target_index'] for f in fields}, 'unconsumed target record')
    validate_safe_seh(row,anchors,targetmap)
    return fieldmap, targetmap

def check_supported(obligation, subject, facts, row, fieldmap, targetmap, anchors):
    root=row['root_address']
    if obligation==CENSUS:
        need(typed_equal(facts,{'field_ids':sorted(fieldmap),'target_indices':sorted(targetmap),'complete_physical_scope':True}), 'census witness incomplete')
    elif obligation==HIGHLOW:
        site=next(s for s in row['metadata_sites'] if s['subject']==subject)
        need(typed_equal(facts,dict(image_sha256=anchors['image_sha256'],field_id=site['field_id'],section=site['section'],offset=site['offset'],
                        original_site=site['original_site'],original_target=site['original_target'],kind=3,addend=site['addend'],
                        highlow_occurrences=1,directory_evidence_sha256=anchors['highlow_directory_sha256'])), 'HIGHLOW site/type/addend/target mismatch')
    elif obligation==FAMILY:
        need(type(facts['cleanup_extent']) is int and type(facts['handler_extent']) is int and facts['cleanup_extent']==11 and facts['handler_extent']==27, 'foreign cleanup/handler family')
        for key,name,role,subtype,kind in [('handler','___CxxFrameHandler3','crt-contract','cxx-frame-handler','REL32'),
             ('cookie','___security_cookie','data','security-cookie','DIR32'),
             ('checker','@__security_check_cookie@4','crt-contract','security-cookie-check','REL32')]:
            field=fieldmap[facts[key+'_field_id']];target=targetmap[field['target_index']]
            need(target['name']==name and target['canonical_role']==role and target['contract_kind']==subtype and field['kind']==kind, 'wrong handler/cookie/checker semantic role')
            need(uint32(facts[key+'_original_target'],True) and facts[key+'_original_target']==mapped_target(row,target,field['addend']) and facts[key+'_original_target']==field['original_target'], 'handler/cookie/checker destination')
            if key=='cookie':need(field['section']==row['parent']['section'] and field['offset']==21, 'cookie not own parent field')
            else:need(field['section']==row['pieces'][1]['section'] and 11<=field['offset']<=34, 'handler/checker outside own handler cut')
        need(facts['owner_root']==root and facts['basis']=='OWN_MATCHED_FIELDS_AND_EXPLICIT_RESOLVERS', 'name-only or foreign family evidence')
        cleanup=fieldmap[facts['cleanup_call_field_id']];ct=targetmap[cleanup['target_index']]
        need(cleanup['section']==row['pieces'][0]['section'] and 0<=cleanup['offset']<=7 and cleanup['kind']=='REL32' and
             ct['semantic_domain']=='code' and ct['contract_kind']=='ordinary-function', 'missing/wrong cleanup call field')
        need(facts['cleanup_semantics_receipt_sha256']==anchors['cleanup_receipts'][root], 'cleanup semantics anchor')
        infofield=fieldmap[facts['info_field_id']];it=targetmap[infofield['target_index']]
        need(infofield['section']==row['pieces'][1]['section'] and 11<=infofield['offset']<=34 and infofield['kind']=='DIR32' and
             it['section']==next(s['section'] for s in row['owned_sections'] if s['domain']=='data') and it['value']+infofield['addend']==8, 'handler FuncInfo field ownership')
    elif obligation==FRAME:
        need(facts['owner_root']==root and type(facts['cleanup_extent']) is int and type(facts['handler_extent']) is int and facts['cleanup_extent']==11 and facts['handler_extent']==27 and
             typed_equal(facts['state_transitions'],[[0,-1]]) and type(facts['catch_count']) is int and facts['catch_count']==0 and facts['normal_and_unwind_coordinates_distinct'] is True
             and facts['frame_preservation_receipt_sha256']==anchors['frame_receipts'][root] and facts['funcinfo_sha256']==digest(row['funcinfo']) and facts['state_graph_sha256']==digest(row['state_graph']), 'unsupported frame/no-catch family')
    elif obligation==SOURCE:
        need(facts['authority']=='HISTORICAL_COMPILER_OBJECT_SOURCE_LINEAGE' and facts['object_sha256']==row['object_sha256'] and
             facts['source_sha256']==row['source_context_sha256'] and facts['lineage_receipt_sha256']==anchors['source_lineage'][str(row['recipe_index'])], 'declared/hash-only source is not compiler lineage')
    elif obligation==GRAPH:
        need(facts['owner_root']==root and facts['expanded_scope_sha256']==anchors['expanded_scopes'][root] and
             typed_equal(facts['retained_sections'],sorted([row['parent']['section']]+[s['section'] for s in row['owned_sections']])) and
             facts['whole_SafeSEH_accounted'] is True and facts['SafeSEH_inventory_sha256']==digest(row['safe_seh_inventory']) and facts['no_unknown_omission_waiver'] is True, 'expanded graph scope/omission mismatch')

def qualify_prospective_parent_eh(bundle, root_address, *, anchors):
    """Account claims only. No supplied hash or supported status discharges proof."""
    try:
        return _qualify(bundle,root_address,anchors)
    except (KeyError,TypeError,StopIteration,AttributeError,IndexError,OverflowError) as error:
        raise QualificationError('missing/malformed qualification input: '+str(error)) from error

def _qualify(bundle, root_address, anchors):
    need(no_floats(bundle),'floating numeric evidence is unsupported')
    validate_anchors(anchors)
    need(bundle.get('kind')=='prospective-UUID-seven-qualification-input-v1','input family')
    need(root_address in ROOTS,'foreign or historical root')
    for key in ('observation_sha256','review_sha256','request_sha256','image_sha256','producer_sha256'):
        need(hex_digest(anchors[key]) and bundle['provenance'][key]==anchors[key], 'stale independently supplied anchor: '+key)
    rows=bundle['roots'];need(len(rows)==7 and {r['root_address'] for r in rows}==set(ROOTS),'exact seven root inventory')
    validated={};identities={};all_sites=[];owned_sections=set();original_intervals=[];sx_by_object={};native_by_object={}
    for row in rows:
        need(hex_digest(anchors['root_inputs'][row['root_address']]) and digest(row)==anchors['root_inputs'][row['root_address']], 'stale anchored root input')
        validated[row['root_address']]=validate_root(row,anchors)
        for sn in [row['parent']['section']]+[x['section'] for x in row['owned_sections']]:
            key=(row['object_sha256'],sn);need(key not in owned_sections,'cross-parent shared section');owned_sections.add(key)
        all_sites.extend(x['original_site'] for x in row['metadata_sites'])
        intervals=[(int(row['root_address'],16),int(row['root_address'],16)+157), (row['metadata_original_base'],row['metadata_original_base']+44)]+[(x['original_start'],x['original_end']) for x in row['pieces']]
        for start,end in intervals:
            need(not any(start<b and a<end for a,b in original_intervals), 'shared/overlapping original interval needs separate ICF proof')
            original_intervals.append((start,end))
        sx=row['safe_seh_inventory'];native_sx={k:v for k,v in sx.items() if k!='records'}
        native_sx['records']=[{k:v for k,v in record.items() if k not in ('disposition','expanded_scope_sha256')} for record in sx['records']]
        old_sx=sx_by_object.setdefault(row['object_sha256'],digest(native_sx));need(old_sx==digest(native_sx),'same object has conflicting whole SafeSEH inventory')
        for physical_target in row['targets']+[record['target'] for record in sx['records']]:
            physical={k:physical_target[k] for k in ('index','name','section','value','storage','type','aux_count')}
            physical_key=(row['object_sha256'],physical_target['index']);old_physical=native_by_object.setdefault(physical_key,physical)
            need(typed_equal(old_physical,physical),'same object physical symbol index conflicts across roots')
        for target in row['targets']:
            physical={k:target[k] for k in ('index','name','section','value','storage','type','aux_count')}
            physical_key=(row['object_sha256'],target['index']);old_physical=native_by_object.setdefault(physical_key,physical)
            need(typed_equal(old_physical,physical),'same object physical symbol index conflicts across roots')
            identity=(target['canonical_role'],target['semantic_domain'],target['contract_kind'],target['canonical_identity_sha256'])
            previous=identities.setdefault(target['original_base'],identity)
            need(previous==identity,'same-base canonical identity/domain/subtype conflict')
    need(len(all_sites)==14 and len(set(all_sites))==14,'fourteen distinct own metadata sites')
    row=next(r for r in rows if r['root_address']==root_address);fieldmap,targetmap=validated[root_address]
    required=[(name,'parent') for name in SINGLE]+[(HIGHLOW,s['subject']) for s in row['metadata_sites']]
    evidence=row['evidence'];keys=[(e['obligation_id'],e['subject']) for e in evidence]
    need(len(set(keys))==len(keys) and set(keys)<=set(required),'duplicate/foreign obligation evidence')
    records=[];consistent=bool(row['parent']['MATCH'] and all(p['MATCH'] for p in row['pieces']) and all(s['MATCH'] for s in row['metadata_sites']) and row['metadata_nonrelocation_MATCH'] and row['metadata_full_MATCH'])
    consistent=consistent and all(f['comparison_MATCH'] for f in row['physical_fields'])
    observation_false=not consistent
    need(isinstance(row['parent']['errors'],list) and isinstance(row['EH_errors'],list) and isinstance(row['unknown_diagnostics'],list),'comparison diagnostics shape')
    if row['parent']['errors'] or row['EH_errors'] or row['unknown_diagnostics']:consistent=False;observation_false=True
    for obligation,subject in required:
        match=[e for e in evidence if(e['obligation_id'],e['subject'])==(obligation,subject)]
        e=match[0] if match else None;status=e['status'] if e else 'missing'
        need(status in ('supported','unknown','false','missing'),'unknown evidence status')
        reason={'unknown':'UNKNOWN','false':'EXPLICIT_FALSE','missing':'MISSING','supported':'SOURCE_PHASE_NOT_INDEPENDENTLY_REPLAYED'}[status]
        if status=='supported':
            need(e['family']==FAMILIES[obligation],'wrong witness family')
            key=claim_key(root_address,obligation,subject);a=anchors['witnesses'][key]
            need(hex_digest(e['witness_sha256']) and e['witness_sha256']==a['sha256'] and digest(e['facts'])==a['facts_sha256'],'unanchored or stale witness facts')
            check_supported(obligation,subject,e['facts'],row,fieldmap,targetmap,anchors)
        else:consistent=False
        records.append(dict(obligation_id=obligation,subject=subject,occurrence=len(records),evidence_status=status,
                            reason=reason,discharged=False,additional_limit='SOURCE_PHASE_NOT_INDEPENDENTLY_REPLAYED'))
    blockers=copy.deepcopy(row['inherited_blockers']);seen=set()
    for blocker in blockers:
        need(isinstance(blocker['id'],str) and blocker['id'] and integer(blocker['ordinal']) and
             blocker['ordinal'] not in seen and hex_digest(blocker['evidence_sha256']),'malformed/duplicate blocker occurrence')
        seen.add(blocker['ordinal']);records.append(dict(obligation_id=blocker['id'],subject='expanded-blocker',
            occurrence=blocker['ordinal'],evidence_status='unresolved-inherited',reason='INHERITED_EXPANDED_BLOCKER',discharged=False))
    sx_unresolved=validate_safe_seh(row,anchors,targetmap)
    for ordinal in sx_unresolved:
        records.append(dict(obligation_id=GRAPH,subject='SafeSEH:'+str(ordinal),occurrence=ordinal,
                            evidence_status='unknown',reason='UNRESOLVED_SAFESEH_RETENTION',discharged=False))
    if blockers or sx_unresolved:consistent=False
    return dict(kind='prospective-UUID-seven-SOURCE-claim-accounting-v1',root_address=root_address,
                schema_complete=True,evidence_inventory_complete=len(evidence)==len(required),claim_observation_diagnostics=copy.deepcopy(dict(parent_errors=row['parent']['errors'],EH_errors=row['EH_errors'],unknown_diagnostics=row['unknown_diagnostics'])),authored_claims_consistent=consistent,observed_comparison_false=observation_false,
                obligations=records,inherited_blockers=blockers,unresolved_obligation_ids=[r['obligation_id'] for r in records],
                discharged=[],independent_evidence_replay_performed=False,
                supplied_anchors_are_unverified_external_expectations=True,claims_are_not_verified_closure=True,
                **FALSE_FLAGS)
