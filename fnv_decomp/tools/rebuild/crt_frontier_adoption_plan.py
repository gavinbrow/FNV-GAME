"""Separate saved-evidence contract for the 44,540-field CRT successor.

Only the four previously reviewed alternate names are eligible. A new
uncertain use disables that alias; uncertainty in either cookie owner
disables both cookie bindings. Generated EH evidence keeps its own class.
No image, library, object, native tool, or application execution is used.
"""
from __future__ import annotations
import gzip
import hashlib
import json
from pathlib import Path

import crt_provider_adoption_plan as old

ROOT=old.ROOT
PINS={
 'application-crt-adoption-plan-v1.json':'2e3bde14db62d1db03dfd87386d68cdd9707f7c6d6bbea86ddf085795c13973f',
 'application-crt-adoption-plan-peer-lane04-v1.json':'ecfd83f9f2b7d564e73e31361ff19759677f4b933689607e8d1d2f306d307cb5',
 'application-crt-adoption-v4-proposal-v1.rsp':'aaec970cae1dcf32699bda75317afbbcd4551c67252fca0d508d47eec997024a',
 'application-link-diagnostic-v6-crt/link-receipt.json':'50d56dbed059f38c075350eb3852f68b246878bd66632cc4ab32d8b95dba7fdd',
 'application-link-diagnostic-v6-crt/receipt.json':'54165d0899e493556487e1406867d71de33cd7e1961d11a7e9d5ae5806299940',
 'application-link-diagnostic-v6-crt/independent-outcome-review.json':'80b00f8bab2c7f629adabc6c85be2a4c68dbb1593b4a8fa841403d6739d908dd',
 'application-link-diagnostic-v6-crt/crt-plan-independent-outcome-review.json':'d65dc1df79ce7f7ffb1da0e4d52c4abba11fe38b086f79de8debc767bbe63cb9',
 'application-frontier-cohort-observation-v2/receipt.json':'284185702ca7db04e5447d14db74d2a230cd56cb84e6b56886cde90b46b81d83',
 'application-frontier-cohort-observation-v2/independent-outcome-review.json':'c9e30fb9f5fb5c971516bf1a8df8fa504189fc13adef4aba9491fe98dab8ddc2',
 'application-frontier-cohort-observation-v2/fields.json.gz':'02274272cb24b3de74079944fd50e1df05c0dc645e73a56b807fe44d62f1dd0b',
 'ordinary-relocation-first3-v1/members.json':'e562e0444af8e817b4212ab967f3c9591619e2aafd043027afc14c8cea56e8e3',
 'composed-relocation-first12-v1/members.json':'db65da111e1f13401dc82c2d41302881434f93fc5221588abc6e1f7c292766de',
 'parent-eh-file-projection-v1/integration-metadata.json':'b009af1c5402f37d992d0f4fa48b7667780de9fb36ee04de0618007bb3c92931',
 'parent-eh-file-projection-v1/projection.json':'27f183555a60b158a673588a4d8bc313075fe3247a2d0220225d0b378a04fff5',
 'parent-eh-observation-v2/receipt.json':'a43a899d5339e95a2e1cedfaf1e8a64d4b3a97d10fcc381c9e3cc56712f51e2c',
 'parent-eh-observation-v2/observations.jsonl.gz':'c5a1b95676e36535b07a5deef2ecd176ec63f4b3a2fe95e614ca77d316f4dbaa',
 'parent-eh-source-v2/observation-request-v2.json':'456c59288f3e35fedb0b52cd7234fb4441790f8d1e43f6be491beb65007dc58d',
 'code-lane08-source-triage-v1/collector-actual-outcome-review-v2.json':'2e30f5588897dbc7fd3f3feb929dddb36cd3ac059b7555b41ff22d0527228052',
}
FULL_DIGEST='006b6c59df46c55b99ba4f9a644648414db607b52e848d83b9e9618b0129d51a'
BASE_DIGEST='08f5ee8fa735f164b9b49189dadbf2fb75b563a3b284583a0c13cedcd1753f20'
EH_RECORD='591a99aa1ab205e9f18f48fe5f2a47af5284566b275ba476400fd6a8c6dc82c6'
COOKIE_NAMES={old.undefined(base,role) for base,role,export,kind in old.BINDINGS if 'cookie' in export}
SOURCES=('tools/rebuild/crt_frontier_adoption_plan.py',
         'tests/rebuild/test_crt_frontier_adoption_plan.py',
         'tools/rebuild/crt_provider_adoption_plan.py')

def require(ok,message):
    if not ok:raise ValueError(message)

def number(value):return int(value,0) if isinstance(value,str) else value

def ancestry(observation,review,prepared_sha256,link_sha256):
    require(observation['baseline_V6_receipt_sha256']==prepared_sha256 and
        review['prepared_receipt_sha256']==prepared_sha256 and
        review['link_receipt_sha256']==link_sha256,
        'new observer/prepared/actual-link ancestry differs')

def response_bytes(bindings,previous):
    """Select whole already reviewed tokens while retaining exact CRLF bytes."""
    expected={old.undefined(b,r):e for b,r,e,k in old.BINDINGS}
    require(len(bindings)==4 and {b['canonical_undefined'] for b in bindings}==set(expected),
        'not the exact four existing binding roles')
    enabled=set()
    for b in bindings:
        require(b['normal_export']==expected[b['canonical_undefined']], 'new or changed normal export')
        if b['enabled']:enabled.add(b['canonical_undefined'])
    require(not (enabled&COOKIE_NAMES) or COOKIE_NAMES<=enabled,'partial cookie owner pair')
    lines=previous.splitlines(keepends=True)
    require(len(lines)==4 and previous==old.response([
        dict(canonical_undefined=old.undefined(base,role),normal_export=export)
        for base,role,export,kind in old.BINDINGS]).replace('\n','\r\n').encode('ascii'),
        'previous reviewed tokens differ')
    return b''.join(line for line,(base,role,export,kind) in zip(lines,old.BINDINGS)
        if old.undefined(base,role) in enabled)

def coupled_disable(bindings):
    if any(not b['enabled'] for b in bindings if b['canonical_undefined'] in COOKIE_NAMES):
        for b in bindings:
            if b['canonical_undefined'] in COOKIE_NAMES:
                b['enabled']=False
                if 'cookie owner pair disabled' not in b['disabled_reasons']:
                    b['disabled_reasons'].append('cookie owner pair disabled')
    return bindings

def new_field_evidence(field,integration,record,unit):
    """Return explicit evidence or a reason; never relabel generated fields."""
    p=field['proof'];index=field['physical_symbol_index'];semantic=record['result']['semantic']
    expected={506:('0x011c16bc','data',6,'___security_cookie','security-cookie',
                   'EXACT_OWN_SOURCE_RESOLUTION','PARENT_FINAL_BINDING',241,3,4,'data'),
              509:('0x00ec408c','crt-contract',20,'@__security_check_cookie@4','security-cookie-check',
                   'EXACT_GENERATED_EH_FIELD_RESOLUTION','PARENT_OWNED_GENERATED_EH_FIELD',242,4,6,'code')}
    try:
        require(index in expected,'unreviewed new alias field')
        base,role,kind,symbol,contract,consistency,family,section,outsection,outindex,domain=expected[index]
        require(field['component']=='EHFile' and field['member']=='component.obj' and
            field['root']=='0x005e0200' and field['recipe_id']=='2656-e9bf85b93a320794', 'wrong new source owner')
        require(field['object_sha256']==record['root']['object_sha256']==integration['source_object_sha256'] and
            semantic['object_sha256']==record['root']['object_sha256'] and
            field['member_sha256']==integration['object_sha256'], 'source/member identity differs')
        require(field['section']==outsection and field['symbol_index']==outindex and field['offset']==21 and
            field['kind']==kind and field['canonical']==old.undefined(base,role) and field['undefined'] is True,
            'serialized alias field differs')
        raw=[r for r in integration['fields'] if r['section']==section and r['offset']==21 and r['target_index']==index]
        require(len(raw)==1,'raw EH field absent or ambiguous');raw=raw[0]
        require(raw['output_section']==outsection and raw['output_target_index']==outindex and
            raw['kind']==kind and raw['addend']==0 and number(raw['original_base'])==number(base) and
            number(raw['original_target'])==number(base) and raw['proof_family']==family,
            'raw EH slot mapping differs')
        identity=dict(base=number(base),contract_kind=contract,proof_consistency=consistency,
            role=role,semantic_domain=domain,symbol=symbol,symbol_index=index)
        require(p['external_identity']==raw['external_identity']==identity and
            p['proof_family']==family and p['physical_section']==section and p['field_offset']==21 and
            p['kind']==kind and p['addend_bits']==0 and p['symbol_index']==index and
            p['role']==role and p['original_base']==base and p['original_target']==base and
            p['canonical_name']==field['canonical'],
            'distinct source proof class or exact identity differs')
        witnessed=[x for x in semantic['fields'] if x['section']==section and x['offset']==21 and x['target_index']==index]
        require(len(witnessed)==1 and all(raw[k]==v for k,v in witnessed[0].items()), 'accepted observer field differs')
        require(identity in semantic['external_obligations'],'accepted observer external identity absent')
        require(not record['result']['blockers'] and record['result']['structural_projection_candidate'] and
            all(c['nonfield_differences']==0 for c in semantic['comparisons']), 'source observation is not accepted positive evidence')
        require(unit['compiler']=='sp1' and {'/MT','/GS','/EHsc'}<=set(unit['flags']) and
            unit['source']==record['source'], 'generated caller compiler/runtime recipe differs')
        require(number(unit['symbols']['___security_cookie'])==0x011c16bc, 'recipe cookie owner differs')
        if index==506:
            source=[x for x in record['central_contract']['fields'] if x['coff_relocation']['symbol_index']==506]
            require(len(source)==1 and source[0]['proof_consistency']=='EXACT_OWN_SOURCE_RESOLUTION' and
                source[0]['source_resolution_basis']=='OWN_RECIPE_BINDING' and
                source[0]['coff_relocation']['symbol']=='___security_cookie', 'parent own-recipe proof differs')
        elif symbol in unit['symbols']:
            # A recipe can name the same helper globally without providing an
            # own-source field witness for this generated handler slot.
            require(number(unit['symbols'][symbol])==number(base), 'recipe helper identity conflicts with generated witness')
        return dict(verified=True,proof_family=family,proof_consistency=consistency,external_identity=identity,
            raw_field=raw,observer_field=witnessed[0],observer_record_sha256=EH_RECORD,
            runtime_frame_or_ABI_approved=False),None
    except (ValueError,KeyError,TypeError) as error:
        return None,str(error)

def run():
    folder=ROOT/'build/rebuild';out=folder/'application-crt-frontier-contract-v2.json';rsp=folder/'application-crt-frontier-proposal-v2.rsp'
    require(folder.resolve()==folder and not out.exists() and not rsp.exists(),'exclusive private outputs required')
    paths={folder/n:h for n,h in PINS.items()};paths[ROOT/'build/units.json']=old.UNITS
    for p,h in paths.items():require(old.sha(p)==h,'input pin differs: '+p.name)
    sources={p:old.sha(ROOT/p) for p in SOURCES}
    saved={n:json.loads((folder/n).read_text()) for n in PINS if n.endswith('.json')}
    fields=json.load(gzip.open(folder/'application-frontier-cohort-observation-v2/fields.json.gz','rt'))
    require(len(fields)==44540 and old.digest(sorted(fields,key=old.canonical))==FULL_DIGEST,'full selected cohort differs')
    receipt=saved['application-frontier-cohort-observation-v2/receipt.json']
    ancestry(receipt,saved['application-link-diagnostic-v6-crt/independent-outcome-review.json'],
        PINS['application-link-diagnostic-v6-crt/receipt.json'],
        PINS['application-link-diagnostic-v6-crt/link-receipt.json'])
    require(receipt['complete_field_count']==44540 and receipt['extra_field_count']==187 and
        receipt['fields_canonical_sha256']==FULL_DIGEST,'new cohort ancestry differs')
    baseline=saved['application-link-diagnostic-v6-crt/link-receipt.json']
    basefields=[r for rows in baseline['provenance'].values() for r in rows if r.get('proof')]
    require(len(basefields)==44353 and old.digest(sorted(basefields,key=old.canonical))==BASE_DIGEST,'baseline V6 scope differs')
    by={old.field_key(f):f for f in basefields};require(len(by)==len(basefields),'baseline field identity ambiguous')
    require(all(by[old.field_key(f)]==f for f in fields if old.field_key(f) in by),'old input fields changed')
    added=[f for f in fields if old.field_key(f) not in by]
    require(len(added)==187 and {k:sum(f['component']==k for f in added) for k in
        ('ordinary-first3','typed-CODE12','EHFile')}=={'ordinary-first3':29,'typed-CODE12':146,'EHFile':12},'extra components differ')
    ordinary=saved['ordinary-relocation-first3-v1/members.json']+saved['composed-relocation-first12-v1/members.json']
    require(sum(len(r['projection']['fields']) for r in ordinary)==175,'ordinary extra field extent differs')
    aliases={number(b) for b,r,e,k in old.BINDINGS}
    require(not any(number(f['original_base']) in aliases for r in ordinary for f in r['projection']['fields']),
        'ordinary extra caller needs separate alias proof')
    with gzip.open(folder/'parent-eh-observation-v2/observations.jsonl.gz','rt') as stream:
        next(stream);record=json.loads(next(stream))
    require(old.digest(record)==EH_RECORD and record['root']['original_address']=='0x005e0200','EH witness envelope differs')
    units=json.loads((ROOT/'build/units.json').read_text())['units'];unit=units[2656]
    source=ROOT/unit['source'];require(old.sha(source)==record['root']['source_sha256'],'actual own source changed')
    paths[source]=record['root']['source_sha256']
    prior=saved['application-crt-adoption-plan-v1.json'];previous=(folder/'application-crt-adoption-v4-proposal-v1.rsp').read_bytes()
    bindings=[];strong=set(receipt['provider_namespace']['symbols']);integration=saved['parent-eh-file-projection-v1/integration-metadata.json']
    for oldbinding in prior['prospective_expanded_cohort']['bindings']:
        b=json.loads(json.dumps(oldbinding));name=b['canonical_undefined'];base,role=b['original_base'],b['role']
        kind=next(k for address,r,e,k in old.BINDINGS if address==base and r==role)
        uses=old.census(fields,base,role,kind);new=[f for f in uses if old.field_key(f) not in by]
        require([f for f in uses if old.field_key(f) in by]==b['fields'],'legacy alias cohort changed')
        evidence=[];reasons=[]
        for f in new:
            ev,reason=new_field_evidence(f,integration,record,unit)
            if ev:evidence.append(ev)
            else:reasons.append(reason)
        if name in strong:reasons.append('canonical strong definition collision')
        require(b['normal_family']=='sp1' and b['normal_provider']['archive_sha256']==old.LIBRARY,
            'normal single-CRT owner differs')
        b.update(fields=uses,field_count=len(uses),field_census_sha256=old.digest(uses),
            baseline_field_count=len(oldbinding['fields']),new_fields=new,new_field_evidence=evidence,
            baseline_distinct_input_callers=oldbinding['distinct_input_callers'],
            distinct_input_callers=len({f['caller'] for f in uses}),
            enabled=not reasons,disabled_reasons=reasons,provider_adopted=False,runtime_ABI_approved=False)
        if role=='data':
            b['recipe_cookie_proofs']=oldbinding['recipe_cookie_proofs']+old.cookie_recipe_proofs(new,units)
        bindings.append(b)
    coupled_disable(bindings);response=response_bytes(bindings,previous)
    require([b['field_count'] for b in bindings]==[100,94,1,3],'new complete alias census differs')
    plan=dict(kind='expanded-four-CRT-diagnostic-contract',schema_version=1,inputs=PINS,sources=sources,
        units_sha256=old.UNITS,own_source=dict(path=unit['source'],sha256=record['root']['source_sha256']),
        scope='V6-plus-first3-CODE12-EHFile',complete_input_fields=44540,selected_field_sha256=FULL_DIGEST,
        baseline_complete_fields=44353,baseline_field_sha256=BASE_DIGEST,extra_fields=187,
        alias_field_count=198,bindings=bindings,enabled_alias_count=sum(b['enabled'] for b in bindings),
        response_sha256=hashlib.sha256(response).hexdigest(),response_text=response.decode('ascii'),
        baseline_V6_actual_delta=dict(before=277,after=273,added=0),
        normal_runtime_owner=prior['normal_runtime_owner'],function_contracts=prior['function_contracts'],
        generated_EH_proof_remains_distinct=True,normal_CRT_data_need_not_equal_original_addresses=True,
        unreviewed_new_CRT_aliases=[],uncertainty_policy='disable uncertain alias; disable both cookie owners if either is uncertain',
        native_operation_authorized=False,provider_adopted=False,runtime_ABI_approved=False,runtime_eligible=False)
    for p,h in paths.items():require(old.sha(p)==h,'input changed: '+p.name)
    for p,h in sources.items():require(old.sha(ROOT/p)==h,'source changed')
    with out.open('x',encoding='utf-8') as stream:json.dump(plan,stream,indent=2);stream.write('\n')
    with rsp.open('xb') as stream:stream.write(response)
    print(json.dumps(dict(plan_sha256=old.sha(out),response_sha256=old.sha(rsp),
        complete_fields=44540,alias_fields=198,enabled_aliases=plan['enabled_alias_count'])))

if __name__=='__main__':run()
