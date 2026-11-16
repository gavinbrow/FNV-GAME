"""New V8 metadata-only existing-four CRT contract; V7 artifacts are immutable."""
from __future__ import annotations
import gzip
import hashlib
import json
from pathlib import Path

import crt_frontier_adoption_plan as prior
import frontier_code_factory as factory

old=prior.old
ROOT=old.ROOT
FULL_DIGEST='5b95911096951e2d808b1028d60de12f9ce41010dbdd9c14b7f788a96f618bf2'
BASE_DIGEST='006b6c59df46c55b99ba4f9a644648414db607b52e848d83b9e9618b0129d51a'
MODEL_RECORD='765cb1b2c4ba7e4da4eedf8a359527cd38f0987d1744473f15fb22d472c94f27'
OWN_SOURCES={
 'src/fallout/misc/main.cpp':'89d09f8b4ba6d9758fca0ac3ebd32e18c9cc82c68a739c044457ed5c005ae3c5',
 'src/staging/blk_00440000_od.cpp':'9236184acd1d32db546f728d2b587b9794836daf4cba13b01560029d1c3d6587',
}
PINS={
 'application-crt-frontier-contract-v2.json':'1baadbcd376c2e03dba219558eac940ed50e970cf8e5b12391a4969f336f6e21',
 'application-crt-frontier-contract-peer-v2.json':'8cb0711700c68e799700324de725566991ef7366881190224a77ef3c2aa27357',
 'application-crt-frontier-proposal-v2.rsp':'aaec970cae1dcf32699bda75317afbbcd4551c67252fca0d508d47eec997024a',
 'application-link-diagnostic-v7-frontier/receipt.json':'0dd1b0791b4717b8c3d827f5e17af863200da659eca275f6d3290093f682fdfa',
 'application-wave8-cohort-observation-v1/receipt.json':'7939cdc2912317a9cb1bca0027feba50fa511111fe842308c8f7d8805af28741',
 'application-wave8-cohort-observation-v1/independent-outcome-review.json':'09ae566d99b1bbf58273ce4d3d5252d49411df80cddd30191615de27bef4bbdb',
 'application-wave8-cohort-observation-v1/fields.json.gz':'2e5cb28f81cf5042c31ae80f7db49ef003df693cf428fb678d7f116a907425bf',
 'application-frontier-cohort-observation-v2/fields.json.gz':'02274272cb24b3de74079944fd50e1df05c0dc645e73a56b807fe44d62f1dd0b',
 'frontier-code-production-v5-v1/members.json':'9d7ae7c145a7da035ed5437784d2d0334d4aae9385ce854a5e788e9dc5251429',
 'frontier-code-production-v5-v1/contexts.bin':'eaa283ae4407ae409dd2cc8e10c429cb85e5efd70f0a6ce91139e8368cae90a2',
 'frontier-code-production-v5-v1/contexts-index.json':'b6e507640abd6d3a9c143d97473f9326f5f661c733121a130008f27a5f2ba2e1',
 'code59-iat-annotations-v1/proof-bundle.json':'cea628a8955bbc6c24051723a90981b36ff040d2d760571b344ccd880554a5f1',
 'crt-v8-four-input-preflight-v1.json':'57d26db204b58f1a5dfe231340f2b1aa15b3e29b47f90015deac6453d8a2de5b',
 'parent-eh-model-loader-projection-v1/integration-metadata.json':'e45a0a84e3af7c3b34e80ec107c72894ff96ef3826b2dbc33f944bd554aaa368',
 'parent-eh-model-loader-projection-v1/projection.json':'f90c7d1de48b7ef914eed5036e2c915ba7130c966f76db42e76671808d57a4b8',
 'parent-eh-observation-v2/observations.jsonl.gz':'c5a1b95676e36535b07a5deef2ecd176ec63f4b3a2fe95e614ca77d316f4dbaa',
 'parent-eh-observation-v2/receipt.json':'a43a899d5339e95a2e1cedfaf1e8a64d4b3a97d10fcc381c9e3cc56712f51e2c',
 'code-lane08-source-triage-v1/collector-actual-outcome-review-v2.json':'2e30f5588897dbc7fd3f3feb929dddb36cd3ac059b7555b41ff22d0527228052',
 'crt-v8-model-loader-cookie-proof-peer-v1.json':'e4062f44616618e88e0dd857ccf85fbd8253e17a43d025fdff4f122ab8a9f849',
}
SOURCES=('tools/rebuild/crt_v8_four_alias_plan.py','tests/rebuild/test_crt_v8_four_alias_plan.py',
 'tools/rebuild/crt_frontier_adoption_plan.py','tools/rebuild/crt_provider_adoption_plan.py',
 'tools/rebuild/frontier_code_factory.py','tools/rebuild/ordinary_relocation_factory.py',
 'tools/rebuild/ordinary_code_projection.py','tools/rebuild/coff_code_archive.py')
GS_PROOFS={
 '0x011c16bc':'2528a17587cd694a23d00c94d6b7db52559c5c5d5c6ceef6f837ad1a9303f46d',
 '0x00ec408c':'200303e927e32d77e3f15f1abc6e65b547877e149d11c23f0bae6c18a8d0d77e',
}

def require(ok,message):
    if not ok:raise ValueError(message)

def number(value):return int(value,0) if isinstance(value,str) else value

def spec(field):
    p=field['proof'];base=p['original_base'];role=p['role']
    found=[(e,k) for b,r,e,k in old.BINDINGS if b==base and r==role]
    require(len(found)==1,'not an existing four role-keyed binding');export,kind=found[0]
    require(field['canonical']==p['canonical_name']==old.undefined(base,role) and
        field['kind']==p['kind']==kind and p['addend_bits']==0 and p['original_target']==base and
        field['undefined'] is True,'canonical/relocation boundary differs')
    return base,role,export,kind

def ordinary_evidence(field,member,proofs,unit):
    base,role,export,kind=spec(field);p=field['proof'];projection=member['projection'];root=projection['requested_roots'][0]
    require(field['component']=='CODE59' and field['root']==root['original_address']=='0x0086d500' and
        field['member']==member['name']=='frontier-044-0086d500.obj' and
        field['member_sha256']==projection['output_sha256'] and
        field['object_sha256']==projection['original_object_sha256']==root['object_sha256'] and
        field['recipe_id']==root['recipe_id']=='0576-dd603b7071c482c6','ordinary source/member owner differs')
    raw=[f for f in projection['fields'] if f['section']==p['physical_section'] and
        f['offset']==field['offset'] and f['symbol_index']==field['physical_symbol_index']]
    require(len(raw)==1,'ordinary raw slot absent/ambiguous');raw=raw[0]
    sha=GS_PROOFS[base];norm=proofs[sha];rel=norm['coff_relocation']
    require(raw['field_proof_sha256']==p['field_proof_sha256']==sha==factory.digest(norm), 'normative source record differs')
    require(norm['proof_consistency']=='EXACT_OWN_SOURCE_RESOLUTION' and norm['source_resolution_basis']=='OWN_RECIPE_BINDING' and
        norm['recipe_id']==field['recipe_id'] and norm['function_va']==field['root'] and
        norm['physical_section']==raw['section']==24 and norm['source_field_offset']==raw['offset']==field['offset'] and
        rel['symbol']==export and rel['symbol_index']==raw['symbol_index']==field['physical_symbol_index'] and
        rel['kind']==raw['kind']==kind and rel['addend']==raw['addend_bits']==0 and
        rel['symbol_section']==0 and rel['symbol_storage']==2 and rel['symbol_value']==0,
        'ordinary full source/symbol/class differs')
    require(raw['canonical_name']==field['canonical'] and raw['role']==role and raw['original_base']==base and
        raw['original_target']==base and p['symbol_index']==raw['symbol_index'], 'ordinary compact proof differs')
    maps=projection['maps'];require(field['section']==maps['section_map'][str(raw['section'])] and
        field['symbol_index']==maps['symbol_map'][str(raw['symbol_index'])], 'ordinary serialized mapping differs')
    require(unit['compiler'] in ('sp1','rtm','vc8') and '/GS' in unit['flags'] and
        number(unit['symbols'][export])==number(base),'ordinary actual recipe/helper binding differs')
    before=[r for c in projection['before_comparison'] for r in c['relocations'] if r['offset']==field['offset']]
    after=[r for c in projection['after_comparison'] for r in c['relocations'] if r['offset']==field['offset']]
    require(len(before)==len(after)==1 and before[0]['symbol']==export and after[0]['symbol']==field['canonical'] and
        before[0]['match'] and after[0]['match'] and number(before[0]['observed'])==number(base) and
        number(after[0]['observed'])==number(base),'ordinary saved comparison differs')
    return dict(verified=True,source_class='ordinary-own-recipe compiler GS field',
        proof_consistency='EXACT_OWN_SOURCE_RESOLUTION',normative_sha256=sha,normative_record=norm,
        raw_field=raw,actual_compiler=unit['compiler'],actual_flags=unit['flags'],
        cookie_scalar_basis='i386 compiler-generated GS pair and accepted normal cookie declaration/storage, not DIR32 operand width',
        runtime_ABI_approved=False)

def model_evidence(field,integration,record,unit):
    base,role,export,kind=spec(field);p=field['proof'];helper=role=='crt-contract'
    physical,section,offset,outsection,outindex=(765,421,61,4,6) if helper else (762,420,21,3,4)
    family='PARENT_OWNED_GENERATED_EH_FIELD' if helper else 'PARENT_FINAL_BINDING'
    consistency='EXACT_GENERATED_EH_FIELD_RESOLUTION' if helper else 'EXACT_OWN_SOURCE_RESOLUTION'
    require(field['component']=='ModelLoader-EH' and field['root']==record['root']['original_address']=='0x00448420' and
        field['recipe_id']==record['root']['recipe_id']=='2633-a302a748a2f3dbae' and field['member']=='component.obj' and
        field['object_sha256']==record['root']['object_sha256']==integration['source_object_sha256'] and
        field['member_sha256']==integration['object_sha256'],'ModelLoader source/member differs')
    require(field['physical_symbol_index']==physical and p['physical_section']==section and
        p['symbol_index']==physical and p['field_offset']==field['offset']==offset and
        field['section']==outsection and field['symbol_index']==outindex and p['proof_family']==family,
        'ModelLoader physical/serialized/proof family differs')
    raw=[f for f in integration['fields'] if (f['section'],f['offset'],f['target_index'])==(section,offset,physical)]
    require(len(raw)==1,'ModelLoader raw slot absent/ambiguous');raw=raw[0]
    require(raw['output_section']==outsection and raw['output_target_index']==outindex and raw['kind']==kind and
        raw['addend']==0 and number(raw['original_base'])==number(base) and number(raw['original_target'])==number(base) and
        raw['proof_family']==family and raw['external_identity']==p['external_identity'] and
        raw['output_symbol']==field['canonical'] and raw['output_symbol_section']==0 and
        raw['output_symbol_value']==0 and raw['output_symbol_storage']==2 and
        raw['output_symbol_type']==(32 if helper else 0), 'ModelLoader raw identity differs')
    identity=p['external_identity'];semantic=record['result']['semantic']
    expected_identity=dict(base=number(base),contract_kind='security-cookie-check' if helper else 'security-cookie',
        proof_consistency=consistency,role=role,semantic_domain='code' if helper else 'data',symbol=export,symbol_index=physical)
    require(identity==expected_identity and identity in semantic['external_obligations'],
        'ModelLoader distinct normative class or source symbol differs')
    witnessed=[f for f in semantic['fields'] if (f['section'],f['offset'],f['target_index'])==(section,offset,physical)]
    require(len(witnessed)==1 and all(raw[k]==v for k,v in witnessed[0].items()),'ModelLoader accepted observer field differs')
    require(not record['result']['blockers'] and record['result']['structural_projection_candidate'] and
        semantic['object_sha256']==record['root']['object_sha256'] and
        all(c['nonfield_differences']==0 for c in semantic['comparisons']), 'ModelLoader source observation not positive')
    require(unit['compiler'] in ('sp1','rtm','vc8') and '/GS' in unit['flags'] and '/EHsc' in unit['flags'] and
        unit['source']==record['source'],'ModelLoader actual recipe differs')
    if export in unit['symbols']:require(number(unit['symbols'][export])==number(base),'optional recipe binding conflicts')
    if helper:
        pieces=[c for c in semantic['comparisons'] if c['section']==421 and c['start']==48 and c['end']==75]
        require(len(pieces)==1 and pieces[0]['nonfield_differences']==0 and 48<=offset<75,
            'actual ModelLoader handler coverage differs')
    else:
        own=[f for f in record['central_contract']['fields'] if f['coff_relocation']['symbol_index']==physical and
             f['physical_section']==section and f['source_field_offset']==offset]
        require(len(own)==1 and own[0]['proof_consistency']=='EXACT_OWN_SOURCE_RESOLUTION' and
            own[0]['coff_relocation']['symbol']=='___security_cookie' and
            number(unit['symbols']['___security_cookie'])==number(base),'ModelLoader own-source scalar proof differs')
    return dict(verified=True,source_class=family,proof_consistency=consistency,raw_field=raw,
        external_identity=identity,observer_record_sha256=MODEL_RECORD,actual_compiler=unit['compiler'],actual_flags=unit['flags'],
        handler_interval=[48,75],cookie_scalar_basis='i386 compiler GS and accepted normal scalar storage model',
        runtime_frame_or_ABI_approved=False)

def prepare():
    folder=ROOT/'build/rebuild';paths={folder/p:h for p,h in PINS.items()};paths[ROOT/'build/units.json']=old.UNITS
    paths.update({ROOT/p:h for p,h in OWN_SOURCES.items()})
    sources={p:old.sha(ROOT/p) for p in SOURCES}
    for p,h in paths.items():require(old.sha(p)==h,'input pin differs: '+p.name)
    saved={p:json.loads((folder/p).read_text()) for p in PINS if p.endswith('.json')}
    receipt=saved['application-wave8-cohort-observation-v1/receipt.json']
    require(receipt['baseline_V7_prepared_receipt_sha256']==PINS['application-link-diagnostic-v7-frontier/receipt.json'] and
        receipt['complete_field_count']==45315 and receipt['extra_field_count']==775 and receipt['fields_canonical_sha256']==FULL_DIGEST,
        'V8 prepared/cohort ancestry differs')
    with gzip.open(folder/'application-wave8-cohort-observation-v1/fields.json.gz','rt') as stream:fields=json.load(stream)
    with gzip.open(folder/'application-frontier-cohort-observation-v2/fields.json.gz','rt') as stream:basefields=json.load(stream)
    require(len(fields)==45315 and old.digest(sorted(fields,key=old.canonical))==FULL_DIGEST and
        len(basefields)==44540 and old.digest(sorted(basefields,key=old.canonical))==BASE_DIGEST,'full hydrated view differs')
    by={old.field_key(f):f for f in basefields};newby={old.field_key(f):f for f in fields}
    require(len(by)==44540 and len(newby)==45315 and all(newby.get(k)==f for k,f in by.items()),
        'old selected proof facts changed or physical fields overlap')
    added=[f for k,f in newby.items() if k not in by]
    require(len(added)==775 and sum(f['component']=='CODE59' for f in added)==723 and
        sum(f['component']=='ModelLoader-EH' for f in added)==52,'new selected components differ')
    bundle=saved['code59-iat-annotations-v1/proof-bundle.json']
    selected=[e for e in bundle['sealed_contexts'] if e['root']['original_address']=='0x0086d500']
    require(len(selected)==1,'ordinary sealed context absent/ambiguous');selected=selected[0]
    index=saved['frontier-code-production-v5-v1/contexts-index.json']['0x0086d500']
    require(index==selected['index_frame'],'ordinary sealed index differs')
    with (folder/'frontier-code-production-v5-v1/contexts.bin').open('rb') as stream:
        context=factory.read_context(stream,index,dict(root=selected['root'],authority=selected['authority']))
    proofs={factory.digest(f):f for f in context['contract']['fields'] if factory.digest(f) in GS_PROOFS.values()}
    require(set(proofs)==set(GS_PROOFS.values()),'full ordinary normative proofs absent')
    members=saved['frontier-code-production-v5-v1/members.json']
    ordinary=next(m for m in members if m['name']=='frontier-044-0086d500.obj')
    with gzip.open(folder/'parent-eh-observation-v2/observations.jsonl.gz','rt') as stream:record=json.loads(next(stream))
    require(old.digest(record)==MODEL_RECORD,'ModelLoader exact ordinal1 witness differs')
    integration=saved['parent-eh-model-loader-projection-v1/integration-metadata.json']
    units=json.loads((ROOT/'build/units.json').read_text())['units']
    previous=saved['application-crt-frontier-contract-v2.json'];bindings=[]
    strong=set(receipt['provider_namespace']['symbols'])
    for previous_binding in previous['bindings']:
        b=json.loads(json.dumps(previous_binding));base,role=b['original_base'],b['role']
        kind=next(k for a,r,e,k in old.BINDINGS if a==base and r==role)
        uses=old.census(fields,base,role,kind);new=[f for f in uses if old.field_key(f) not in by]
        require([f for f in uses if old.field_key(f) in by]==b['fields'],'legacy canonical source facts changed')
        evidence=[];reasons=[]
        for f in new:
            try:
                if f['component']=='CODE59':ev=ordinary_evidence(f,ordinary,proofs,units[576])
                elif f['component']=='ModelLoader-EH':ev=model_evidence(f,integration,record,units[2633])
                else:raise ValueError('unreviewed new caller class')
                evidence.append(ev)
            except (ValueError,KeyError,TypeError) as error:reasons.append(str(error))
        if b['canonical_undefined'] in strong:reasons.append('canonical strong definition collision')
        require(b['normal_family']=='sp1' and b['normal_provider']['archive_sha256']==old.LIBRARY,'normal provider owner differs')
        b.update(fields=uses,field_count=len(uses),field_census_sha256=old.digest(uses),new_fields=new,new_field_evidence=evidence,
            baseline_field_count=previous_binding['field_count'],baseline_distinct_input_callers=previous_binding['distinct_input_callers'],
            distinct_input_callers=len({f['caller'] for f in uses}),enabled=not reasons,disabled_reasons=reasons)
        if role=='data':b['recipe_cookie_proofs']=previous_binding['recipe_cookie_proofs']+old.cookie_recipe_proofs(new,units)
        bindings.append(b)
    prior.coupled_disable(bindings)
    response=prior.response_bytes(bindings,(folder/'application-crt-frontier-proposal-v2.rsp').read_bytes())
    require([b['field_count'] for b in bindings]==[102,96,1,3],'full four-alias census differs')
    plan=dict(kind='V8-existing-four-CRT-diagnostic-contract',schema_version=1,inputs=PINS,sources=sources,
        units_sha256=old.UNITS,own_sources=OWN_SOURCES,scope='V7-plus-CODE59-ModelLoader',
        complete_input_fields=45315,selected_field_sha256=FULL_DIGEST,baseline_complete_fields=44540,
        baseline_field_sha256=BASE_DIGEST,old_raw_source_records_preserved=True,old_annotation_delta=[],extra_fields=775,
        alias_field_count=202,bindings=bindings,enabled_alias_count=sum(b['enabled'] for b in bindings),
        enabled_alias_field_count=sum(b['field_count'] for b in bindings if b['enabled']),
        response_sha256=hashlib.sha256(response).hexdigest(),response_text=response.decode('ascii'),
        normal_runtime_owner=previous['normal_runtime_owner'],function_contracts=previous['function_contracts'],
        generated_and_ordinary_proofs_remain_distinct=True,normal_provider_family_does_not_restrict_caller_compiler_label=True,
        normal_CRT_data_need_not_equal_original_addresses=True,unreviewed_new_CRT_aliases=[],
        response_application='remove all four exact inherited CRT tokens before applying enabled subset',
        native_operation_authorized=False,provider_adopted=False,runtime_ABI_approved=False,runtime_eligible=False)
    for p,h in paths.items():require(old.sha(p)==h,'protected input changed: '+p.name)
    for p,h in sources.items():require(old.sha(ROOT/p)==h,'source changed')
    return plan,response

def run():
    folder=ROOT/'build/rebuild';out=folder/'application-crt-v8-four-contract-v1.json';rsp=folder/'application-crt-v8-four-proposal-v1.rsp'
    require(folder.resolve()==folder and not out.exists() and not rsp.exists(),'exclusive private outputs required')
    plan,response=prepare()
    with out.open('x',encoding='utf-8') as stream:json.dump(plan,stream,indent=2);stream.write('\n')
    with rsp.open('xb') as stream:stream.write(response)
    print(json.dumps(dict(plan_sha256=old.sha(out),response_sha256=old.sha(rsp),fields=45315,
        alias_fields=202,enabled_aliases=plan['enabled_alias_count'])))

if __name__=='__main__':run()
