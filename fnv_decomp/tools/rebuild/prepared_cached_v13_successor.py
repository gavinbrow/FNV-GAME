"""Pure 21-root V13 prepared-exclusion successor; no I/O or adoption.

Only fixed-hash ``from_bytes`` is intended for reviewed production callers.
``build`` accepts authenticated values for review and authored fixture tests.
"""
import copy
import gzip
import hashlib
import io
import json
import re

PARENT='8dde3e03371386c14fe8751a2e3eda65fbd591f6e386caa0e705621d7b94ee41'
HANDOFF='8fadcc041ae90788a4bf669091ff602a92756ff24f9e56659708d1b890665b11'
PEER='001fbc4fadd6683b8ce3cc7c484329ae11046b2f7054118ea5c34db062b76605'
MEMBERS='91ec69b946927f0650aa66df1c78544c95445ad463a463e8b8a2a287b8b9818c'
PROOFS='9f4718e8e3273c088ae671db68c7a9314e33848e3912cb79844c8f9b0b210eb8'
UUID_NEGATIVE='7c4704d0c777585656272cd2a39a06437d124e34d4cea712236b982641cf9a26'
UUID_COMPOSED='69076d817070c2411fbb8d3dbf9cf1ea0ca3409d6a438360c25dffc19aa7d238'
UUID_TOKEN=r'C:\path\to\Decompilation\FNV\tools\vc2008\VC\PlatformSDK\Lib\Uuid.Lib'
ROOT_KEYS={'original_address','recipe_id','recipe_index','object_sha256','source_sha256','symbol','symbol_index','section','value','size'}


def need(v,message):
    if not v:raise ValueError(message)


def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')
def digest(v):return hashlib.sha256(canonical(v)).hexdigest()


def physical(value):
    need(type(value) is dict and set(value)=={'recipe_id','object_sha256','symbol_index'} and
         type(value['recipe_id']) is str and bool(value['recipe_id']) and type(value['object_sha256']) is str and
         re.fullmatch('[0-9a-f]{64}',value['object_sha256']) and type(value['symbol_index']) is int and value['symbol_index']>=0,
         'invalid physical identity')
    return '_fnv_code_'+digest(value)


def census(records):
    names=set();addresses=set();ordinary=set()
    for row in records:
        name=row['canonical'];address=row['original_address']
        need(name==physical(row['namespace_identity']) and name not in names,'duplicate/invalid namespace')
        physical(row['origin_identity'])
        need(type(address) is str and re.fullmatch('0x[0-9a-f]{8}',address) and address not in addresses and
             row['category'] in ('ordinary','application-candidate'),'duplicate/invalid address or category')
        names.add(name);addresses.add(address)
        if row['category']=='ordinary':ordinary.add(name)
    return sorted(names),sorted(ordinary)


def comparison(rows,root,name,count):
    need(type(rows) is list and len(rows)==1,'singleton MATCH required');r=rows[0]
    need(r.get('address')==root['original_address'] and r.get('symbol')==name and
         type(r.get('size')) is int and r['size']==root['size'] and type(r.get('compiled_extent')) is int and
         r['compiled_extent']==root['size'] and r.get('verdict')=='match' and r.get('errors')==[] and
         not r.get('byte_differences',[]) and type(r.get('relocations')) is list and len(r['relocations'])==count and
         all(type(x) is dict and x.get('match') is True for x in r['relocations']), 'full comparison differs')


def build(parent,handoff,peer,members,proofs):
    """Reconcile all 21 admitted original/member/proof records with parent epoch."""
    need(type(parent) is dict and type(parent.get('schema_version')) is int and parent['schema_version']==8 and
         parent.get('kind')=='prepared-CODE-collision-exclusions' and parent.get('policy_id')=='prepared-UUID2768-successor-v1' and
         type(parent.get('ordinary_prepared_count')) is int and parent['ordinary_prepared_count']==14529 and
         type(parent.get('collision_exclusion_count')) is int and parent['collision_exclusion_count']==14535 and
         parent.get('application_selected_code_count') is None and parent.get('application_selection_inferred_from_counts') is False and
         'application_manifest_adopted' not in parent and parent.get('historical_records_preserved') is True,
         'qualified UUID parent scope differs')
    old=parent['records'];names,ordinary=census(old)
    need(len(old)==len(names)==14535 and len(ordinary)==14529 and names==parent['exclusion_names'] and
         ordinary==parent['ordinary_names'],'complete parent census differs')
    uuid=[r for r in old if r['original_address']=='0x00c5d4e0']
    need(len(uuid)==1 and uuid[0].get('identity_mode')=='original-selected-physical-qualified-UUID-directives' and
         uuid[0].get('original_negative_certificate_sha256')==UUID_NEGATIVE and
         uuid[0].get('qualified_composition_sha256')==UUID_COMPOSED and uuid[0].get('future_uuid_response_token')==UUID_TOKEN and
         len(uuid[0].get('normalized_fields',[]))==9,'parent UUID qualified obligation differs')
    need(type(handoff) is dict and type(handoff.get('schema_version')) is int and handoff['schema_version']==1 and
         handoff.get('kind')=='accepted-prepared-CODE-export-handoff' and handoff.get('cohort')=='V13-cache-qualified-native-positive-21' and
         handoff.get('operation_status')=='completed' and handoff.get('requires_successor_exclusion_epoch') is True and
         all(type(handoff.get(k)) is int and handoff[k]==v for k,v in [('requested_candidates',21),('new_distinct_exports',21),
             ('quarantined_candidates',0),('full_field_proof_records',21),('full_field_proof_rows',46),
             ('upstream_ordinary_prepared_count',14529),('upstream_collision_exclusion_count',14535),
             ('successor_ordinary_prepared_count',14550),('successor_collision_exclusion_count',14556)]) and
         handoff.get('upstream_prepared_epoch',{}).get('sha256')==PARENT and handoff.get('members',{}).get('sha256')==MEMBERS and
         handoff.get('field_proofs',{}).get('sha256')==PROOFS and
         all(handoff.get(k) is False for k in ('application_cohort_adopted','application_manifest_adopted','provider_selected',
             'runtime_eligible','ABI_verified','link_ready','native_tools_run','native_archive_conformance_verified')),
         'accepted 21-root handoff differs')
    need(type(peer) is dict and peer.get('kind')=='independent-final21-metadata-handoff-review' and
         peer.get('status')=='accepted-conditional-metadata-handoff' and peer.get('handoff_sha256')==HANDOFF and
         peer.get('full21_root_canonical_serialized_map_and_proofordinal_join') is True and
         type(peer.get('exports')) is int and peer['exports']==21 and type(peer.get('fields')) is int and peer['fields']==46 and
         peer.get('successor_epoch_created') is False and peer.get('requires_successor_exclusion_epoch') is True and
         peer.get('provider_selected') is False and peer.get('runtime_eligible') is False,'independent handoff peer differs')
    rows=handoff['records'];need(type(rows) is list and len(rows)==21 and type(members) is list and len(members)==21 and
                                 type(proofs) is list and len(proofs)==21,'complete 21-record sets required')
    by_name={m['name']:m['projection'] for m in members};need(len(by_name)==21,'duplicate member')
    new=copy.deepcopy(old);field_count=0
    for ordinal,(row,proof) in enumerate(zip(rows,proofs),1):
        root=row['root'];need(type(root) is dict and set(root)==ROOT_KEYS and
            all(type(root[k]) is int for k in ('recipe_index','section','size','symbol_index','value')) and
            root['section']>0 and root['size']>0 and root['value']==0 and type(root['symbol']) is str and bool(root['symbol']) and
            type(root['source_sha256']) is str and re.fullmatch('[0-9a-f]{64}',root['source_sha256']), 'root identity/schema differs')
        ident={k:root[k] for k in ('recipe_id','object_sha256','symbol_index')};name=physical(ident);p=by_name[row['member']]
        need(name==row['canonical'] and p['requested_roots']==[root] and p['exports']==[name] and
             p['output_sha256']==row['member_sha256'] and p['original_object_sha256']==root['object_sha256']==row['original_object_sha256'] and
             p['authority']==row['authority'] and p['certificate_sha256']==row['certificate_sha256'] and
             p['contract_identity_sha256']==row['contract_identity_sha256'] and
             type(row['fields']) is int and row['fields']>=0 and row['fields']==len(p['fields']) and
             type(row['field_proof_ordinal']) is int and row['field_proof_ordinal']==ordinal and
             type(row['serialized_section']) is int and row['serialized_section']>0 and
             type(row['serialized_symbol_index']) is int and row['serialized_symbol_index']>=0 and
             type(p['maps']['section_map'][str(root['section'])]) is int and
             p['maps']['section_map'][str(root['section'])]==row['serialized_section'] and
             type(p['maps']['symbol_map'][str(root['symbol_index'])]) is int and
             p['maps']['symbol_map'][str(root['symbol_index'])]==row['serialized_symbol_index'], 'member identity/physical map differs')
        need(type(proof.get('schema_version')) is int and proof['schema_version']==1 and proof.get('source_evidence_enriched') is False and
             proof.get('member')==row['member'] and proof.get('requested_root')==root and proof.get('authority')==row['authority'] and
             proof.get('output_object_sha256')==row['member_sha256'] and proof.get('certificate_sha256')==row['certificate_sha256'] and
             proof.get('contract_identity_sha256')==row['contract_identity_sha256'] and proof.get('fields_sha256')==row['original_fields_sha256'] and
             proof.get('central_record_sha256')==row['authority']['record_sha256'] and digest(proof)==row['field_proof_record_sha256'] and
             type(proof.get('fields')) is list and len(proof['fields'])==row['fields'] and
             digest(proof['fields'])==proof['fields_sha256'] and
             [digest(x) for x in proof['fields']]==[x['field_proof_sha256'] for x in p['fields']], 'full proof/ordinal join differs')
        seen=set()
        for original,observed in zip(proof['fields'],p['fields']):
            cr=original['coff_relocation'];key=(original['physical_section'],cr['offset'],cr['symbol_index'],cr['kind'])
            need(all(type(v) is int for v in key) and key not in seen and
                 key==(observed['section'],observed['offset'],observed['symbol_index'],observed['kind']) and
                 str(key[0]) in p['maps']['section_map'] and str(key[2]) in p['maps']['symbol_map'] and
                 type(p['maps']['section_map'][str(key[0])]) is int and p['maps']['section_map'][str(key[0])]>0 and
                 type(p['maps']['symbol_map'][str(key[2])]) is int and p['maps']['symbol_map'][str(key[2])]>=0,
                 'field physical mapping differs')
            seen.add(key)
        comparison(p['before_comparison'],root,root['symbol'],row['fields']);comparison(p['after_comparison'],root,name,row['fields'])
        field_count+=row['fields']
        new.append(dict(canonical=name,original_address=root['original_address'],category='ordinary',
            cohort='V13-cache-qualified-native-positive-21',identity_mode='original-selected-physical',
            namespace_identity=ident,origin_identity=copy.deepcopy(ident),logical_binding_applied=True,
            member=row['member'],member_sha256=row['member_sha256'],original_root=copy.deepcopy(root),
            serialization_maps=copy.deepcopy(p['maps']),serialized_section=row['serialized_section'],
            serialized_symbol_index=row['serialized_symbol_index'],source_ledger_sha256=HANDOFF,
            source_record_ordinal=ordinal,source_record_sha256=digest(row),member_ledger_sha256=MEMBERS,
            full_field_proof_ledger_sha256=PROOFS,field_proof_ordinal=ordinal,
            field_proof_record_sha256=row['field_proof_record_sha256'],original_fields_sha256=row['original_fields_sha256'],
            original_field_count=row['fields'],certificate_sha256=row['certificate_sha256'],
            contract_identity_sha256=row['contract_identity_sha256'],authority=copy.deepcopy(row['authority'])))
    names,ordinary=census(new);need(field_count==46 and len(names)==14556 and len(ordinary)==14550,'successor census differs')
    result=copy.deepcopy(parent)
    result.update(schema_version=9,policy_id='prepared-cached-V13-successor-v1',parent_manifest_sha256=PARENT,
        records=new,exclusion_names=names,ordinary_names=ordinary,ordinary_prepared_count=14550,collision_exclusion_count=14556,
        successor_handoff_sha256=HANDOFF,successor_handoff_review_sha256=PEER,successor_member_ledger_sha256=MEMBERS,
        successor_field_proofs_sha256=PROOFS,successor_export_count=21,successor_field_count=46,
        historical_records_preserved=True,fresh_original_stability_verified=False)
    need(result['records'][:14535]==old and 'application_manifest_adopted' not in result and
         result['application_selected_code_count'] is None,'parent records or unknown application state changed')
    return result


def from_bytes(parent_bytes,handoff_bytes,peer_bytes,members_bytes,proofs_gzip):
    for raw,expected in ((parent_bytes,PARENT),(handoff_bytes,HANDOFF),(peer_bytes,PEER),(members_bytes,MEMBERS),(proofs_gzip,PROOFS)):
        need(type(raw) is bytes and hashlib.sha256(raw).hexdigest()==expected,'fixed input hash differs')
    with gzip.GzipFile(fileobj=io.BytesIO(proofs_gzip)) as stream:raw=stream.read(16*1024*1024+1)
    need(len(raw)<=16*1024*1024 and raw.endswith(b'\n'),'bounded proof stream required')
    lines=raw.splitlines();need(len(lines)==21 and all(lines),'exact 21 proof records required')
    return build(json.loads(parent_bytes),json.loads(handoff_bytes),json.loads(peer_bytes),json.loads(members_bytes),
                 [json.loads(line) for line in lines])
