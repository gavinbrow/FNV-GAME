"""Exact saved V14 combined-cohort four-CRT contract; no native operation."""
from __future__ import annotations
import copy
import gzip
import hashlib
import json
from collections import Counter
import crt_v13_four_alias_contract as predecessor
import application_link_wave14 as wave
import application_uuid2768 as uuid

base=predecessor.v13
old=base.old
ROOT=base.ROOT
require=base.require
BASELINE_FIELDS=46237
COMPLETE_FIELDS=46292
FULL_DIGEST='08106a9552e9fe8fbe43a5bd224a212409b00228c26654432b715223eb0d6da4'
ALIAS_USE_COUNT=204
SCOPE='V13-plus-accepted-ALL21-and-qualified-UUID2768'
response_bytes=base.base.v9.v8.prior.response_bytes
coupled_disable=base.base.v9.v8.prior.coupled_disable
OWN_SOURCES=dict(base.OWN_SOURCES,**{'src/fallout/misc/taskqueueinterface.cpp':'528f0b219a8221cfc8c948b3e8bb66d098d63d00e3b877fbaf0d6dcb4e6e71fa'})
SOURCES=('tools/rebuild/crt_v14_four_alias_plan.py','tests/rebuild/test_crt_v14_four_alias_plan.py',
 'tools/rebuild/crt_v13_four_alias_contract.py','tools/rebuild/application_link_wave14.py',
 'tools/rebuild/application_uuid2768.py','tools/rebuild/application_link_frontier.py',
 'tools/rebuild/coff_code_archive.py','tools/rebuild/application_link_diagnostic.py')

INPUT_PINS={'application-crt-v13-four-contract-v1.json': 'd47b3b0efe542808e1fc22481da41888f6daa11d3d6c928279e397344dec5721', 'application-crt-v13-four-contract-peer-v1.json': 'd020b039377efe24821028b8d4c667f9953ce2116db0bb52871966e652e87b27', 'application-crt-v13-four-proposal-v1.rsp': 'aaec970cae1dcf32699bda75317afbbcd4551c67252fca0d508d47eec997024a', 'crt-v13-four-consumer-peer-v1.json': 'a53697ce5f29aa076187acc87f6b9dfa68753560d4a63f77bbe9189f32253faa', 'application-wave13-cohort-observation-v1/fields.json.gz': 'b7823e8892a4a5051d42b6447078058f5d0be4d3db0dc3bfbf5630621b73f23a', 'application-wave14-CRT-input-handoff-v1.json': '63f20780783a550170721794bc657d8256414692973ab2e674ecbbd92577c6ec', 'application-wave14-cohort-observation-v2/receipt.json': 'b6538d8aa9aff10826da60703500a7cc8b374d5efed6cced3e41debba7332185', 'application-wave14-cohort-observation-v2/fields.json.gz': '73a57a716b97cf116e625f2a585039a494b7d8a06293be5810672d229b211075', 'application-wave14-cohort-observation-v2/independent-outcome-review.json': '6fb2797b42d8c874b901461a900867c62aee64badf13ab6148b7b69a1d47b8fd', 'cached-frontier-code-v13-v1/members.json': '91ec69b946927f0650aa66df1c78544c95445ad463a463e8b8a2a287b8b9818c', 'cached-frontier-code-v13-v1/field-proofs.jsonl.gz': '9f4718e8e3273c088ae671db68c7a9314e33848e3912cb79844c8f9b0b210eb8', 'cached-frontier-code-v13-export-handoff-v1.json': '8fadcc041ae90788a4bf669091ff602a92756ff24f9e56659708d1b890665b11', 'code-lane01-analysis-v1/cached-frontier-code-v13-handoff-review-v1.json': '001fbc4fadd6683b8ce3cc7c484329ae11046b2f7054118ea5c34db062b76605', 'application-wave14-verifier-source-independent-review.json': 'ebf8bc0c11f2fc8714294fc05d0beae74a18371fc4150014d5a640b6d2213894', 'crt-v14-input-triage-v1.json': '2ab80c3f4720af41a2d7793ba832ad1406ff203cc4c80cb8c9a9d8464042314f', 'crt-v14-GS-source-boundary-peer-v1.json': 'aedce9c3ac33bbe85861afdfaa3f65380842cadb0c055fab4be9327e88860e6c', 'uuid2768-factory-result-v2/uuid2768.lib': 'b921ee8a8d6baf9a751f1a488aa10a763627ede51b2b475668c97455a4e9eb53', 'uuid2768-factory-result-v2/independent-outcome-review.json': 'dc5553cc029f0821b01c645a4975a70bdabc1a959f95178919df534f51d6b89e', 'uuid-prefix-dependency-v1/context.json': '8b044fe51ce0b455ea6baac1c88441d566ec1514e4def0866b7102382b1b784f', 'uuid2768-factory-result-v2/independent-directive-continuity-review.json': 'e5bead380f35dbb91947ecf14d2f3d776e5b4cf7523cf8aa28348e8aaf09e8db', 'uuid-prefix-dependency-v1/declaration.json': '2cf2f061f003d027213cbfa77e53f2a15be34de8db62fa32712148ff6dbb51ac', 'uuid-prefix-dependency-v1/independent-declaration-audit.json': '32481c04d52919500766a9e10b1a0d2ffe801254a1d542721e49773c6daad1dd', 'uuid-prefix-dependency-v1/review.json': '9cce2a0d39394c9bf0b564a8f872a83b655f83bb22a6db036f306643f15c9dfd', 'uuid2768-typed-export-handoff-v1.json': '4ce4f515e43a04f622b1efaa70ac47753f16109111944f73ca0aefeb915b06a1', 'uuid2768-typed-handoff-source-v1/independent-output-review-v1.json': '7b879e3baa1bf55e81c9a9884f692b27feff025c0d5fe55a30d7c3d60135ab9d', 'uuid2768-native-conformance-v1/receipt.json': '12dae2e56d941949650dbc8c0d72a0660c4d8da5d4d14f2209db4f79e2c852f1', 'uuid2768-native-conformance-v1/independent-outcome-review.json': 'f161af6ac5ce40e02088724ba156f7737484def6b5aafadc4f8bda104587b7f6', 'uuid2768-factory-result-v2/uuid2768.obj': '6fcd604987e08477566cbf9b6901f3200304eb557fdc8f7c356fedaf27d633b3', 'uuid2768-factory-result-v2/field-proofs.jsonl.gz': '4b7cb6ce64a9a84d461ef0ef536cd17c5952fe03b697e45e652e18c2f5e7cc31', 'uuid2768-factory-result-v2/receipt.json': 'fdec31d202ebbed1e846c0c8198a384db995d05aab5433b75d475b4f820ba98c'}
PINS=INPUT_PINS
UUID_PATHS={'archive': 'uuid2768-factory-result-v2/uuid2768.lib', 'base_review': 'uuid2768-factory-result-v2/independent-outcome-review.json', 'context': 'uuid-prefix-dependency-v1/context.json', 'continuity': 'uuid2768-factory-result-v2/independent-directive-continuity-review.json', 'declaration': 'uuid-prefix-dependency-v1/declaration.json', 'declaration_audit': 'uuid-prefix-dependency-v1/independent-declaration-audit.json', 'declaration_review': 'uuid-prefix-dependency-v1/review.json', 'handoff': 'uuid2768-typed-export-handoff-v1.json', 'handoff_review': 'uuid2768-typed-handoff-source-v1/independent-output-review-v1.json', 'native_receipt': 'uuid2768-native-conformance-v1/receipt.json', 'native_review': 'uuid2768-native-conformance-v1/independent-outcome-review.json', 'object': 'uuid2768-factory-result-v2/uuid2768.obj', 'proof': 'uuid2768-factory-result-v2/field-proofs.jsonl.gz', 'receipt': 'uuid2768-factory-result-v2/receipt.json'}
ACTUAL_COHORT={'complete_field_count': 46292, 'all21_component': 'CODE21', 'uuid_component': 'uuid2768', 'all21_roots': ['0x00726bf0', '0x004702f0', '0x005f65d0', '0x00990890', '0x00991dc0', '0x0097ef50', '0x009dc530', '0x0096e870', '0x0096c950', '0x0087b400', '0x00639aa0', '0x00496960', '0x00493930', '0x0058d630', '0x00984f60', '0x0047c850', '0x005516c0', '0x00a5bfa0', '0x00450fd0', '0x00761540', '0x009914d0'], 'uuid_root': '0x00c5d4e0'}

def cohort_delta(baseline,fields,actual):
    """Retain exact raw records and partition only an accepted actual subset.

    Complete canonical JSON records preserve all fields and unknowns while
    allowing the tuple/list representation change of a saved JSON artifact.
    This is not a source-proof qualification or alias-adoption decision.
    Zero-field emitted providers must additionally join the full namespace.
    """
    require(isinstance(actual,dict),'accepted actual cohort descriptor required')
    required={'complete_field_count','all21_component','uuid_component','all21_roots','uuid_root'}
    require(set(actual)==required and type(actual['complete_field_count']) is int,
        'unknown or incomplete actual cohort descriptor')
    require(actual['all21_component']!=actual['uuid_component'] and
        isinstance(actual['all21_roots'],(list,tuple)) and
        len(set(actual['all21_roots']))==len(actual['all21_roots']) and
        actual['uuid_root'] not in actual['all21_roots'],'cohort owners overlap or are ambiguous')
    before={old.canonical(f):f for f in baseline};after={old.canonical(f):f for f in fields}
    require(len(before)==len(baseline) and len(after)==len(fields),'duplicate raw field record')
    require(all(k in after for k in before),'old raw record or unknown annotation changed')
    require(len(fields)==actual['complete_field_count'],'actual full-field count differs')
    added=[f for k,f in after.items() if k not in before]
    allowed={actual['all21_component'],actual['uuid_component']}
    require(all(f['component'] in allowed for f in added),'unreviewed new component')
    ordinary=[f for f in added if f['component']==actual['all21_component']]
    uuid=[f for f in added if f['component']==actual['uuid_component']]
    require(all(f['root'] in actual['all21_roots'] for f in ordinary),'field from a requested but unaccepted ALL21 root')
    require(len(uuid)==9 and all(f['root']==actual['uuid_root'] for f in uuid) and
        Counter(f['proof']['role'] for f in uuid)=={'code':7,'data':2},'not the qualified UUID2768 nine-field scope')
    names={old.undefined(b,r) for b,r,e,k in old.BINDINGS};bases={b for b,r,e,k in old.BINDINGS}
    require(all(f['canonical'] not in names and f['proof']['original_base'] not in bases for f in uuid),
        'UUID2768 unexpectedly uses an existing CRT identity')
    return sorted(added,key=old.canonical)


def join_code21(fields,members,norms):
    byname={m['name']:m['projection'] for m in members};seen=set();result=[]
    for f in fields:
        p=f['proof'];projection=byname[f['member']];root=projection['requested_roots'][0]
        compact=[r for r in projection['fields'] if r['section']==p['physical_section'] and r['offset']==f['offset'] and r['symbol_index']==f['physical_symbol_index']]
        require(len(compact)==1,'CODE21 physical slot absent or ambiguous');compact=compact[0]
        key=(f['member'],compact['section'],compact['offset']);require(key not in seen,'CODE21 duplicate slot');seen.add(key)
        require(old.canonical(p)==old.canonical(dict(compact,physical_section=compact['section'],field_offset=compact['offset'])),'complete compact proof differs')
        full=norms[compact['field_proof_sha256']]
        require(f['root']==root['original_address'] and f['recipe_id']==root['recipe_id']==full['recipe_id'] and
            f['object_sha256']==root['object_sha256']==projection['original_object_sha256'] and f['member_sha256']==projection['output_sha256'] and
            f['caller'] in projection['exports'] and f['kind']==compact['kind'] and f['canonical']==compact['canonical_name'] and
            f['section']==projection['maps']['section_map'][str(compact['section'])] and
            f['symbol_index']==projection['maps']['symbol_map'][str(compact['symbol_index'])] and
            (full['coff_relocation']['addend'] & 0xffffffff)==compact['addend_bits'],'CODE21 source/serialized identity differs')
        require(type(f['undefined']) is bool and f['undefined']==any(u['serialized_symbol_index']==f['symbol_index'] for u in projection['undefined']),'CODE21 definition class differs')
        if 'original_field_proof' in f:require(old.canonical(f['original_field_proof'])==old.canonical(full),'CODE21 complete original proof differs')
        result.append(dict(field=f,normative=full))
    require(len(result)==len(norms)==46,'CODE21 complete46 source coverage differs')
    return result

def same_record_multiset(left,right):
    """Compare complete saved JSON semantics, including all unknown fields."""
    return old.canonical(sorted(left,key=old.canonical))==old.canonical(sorted(right,key=old.canonical))

def qualify_gs(field,full,unit):
    p=field['proof'];role=p['role'];export='___security_cookie' if role=='data' else '@__security_check_cookie@4'
    raw=(7,199,5,'541797ebdb50efbd2b2817981e78dd40e7b359f198d138222c2a478fab928073') if role=='data' else (50,202,6,'b9c69779949b2a9762385b2d42759c90e65e01e3a52fe5be7e3430886b594608')
    offset,physical,serialized,sha=raw;rel=full['coff_relocation'];baseaddr='0x011c16bc' if role=='data' else '0x00ec408c'
    require(role in ('data','crt-contract') and field['component']=='CODE21' and field['root']=='0x0087b400' and
        field['member']=='CACHED-CODE-009-0087b400.obj' and field['recipe_id']=='0606-3ae3f5da56dcec2b' and
        field['object_sha256']=='3baa5847a0164ca66a03ddebe0fc68ad2519022b1019621e94b0ae463b68f975' and
        field['member_sha256']=='650f6c6b43fc0b7b89ab34a7bf2359de22354143ed10d4f98e4a6b43f9f6f321' and
        field['offset']==offset and field['physical_symbol_index']==physical and field['symbol_index']==serialized and
        field['section']==2 and p['physical_section']==24 and p['original_base']==p['original_target']==baseaddr and
        p['canonical_name']==field['canonical']==old.undefined(baseaddr,role) and p['addend_bits']==0 and
        p['field_proof_sha256']==sha==old.digest(full),'new GS exact original/source field differs')
    require(full['proof_consistency']=='EXACT_OWN_SOURCE_RESOLUTION' and full['source_resolution_basis']=='OWN_RECIPE_BINDING' and
        rel['symbol']==export and rel['symbol_index']==physical and rel['addend']==0 and
        rel['symbol_section']==0 and rel['symbol_storage']==2 and rel['symbol_value']==0 and
        rel['kind']==field['kind']==(6 if role=='data' else 20),'new GS exact symbol/boundary differs')
    require(unit['source']=='src/fallout/misc/taskqueueinterface.cpp' and unit['compiler']=='sp1' and
        all(flag in unit['flags'] for flag in ('/MT','/Od','/Oy-','/GS','/EHsc','/Gy','/GF')) and
        unit['symbols'][export]==baseaddr,'exact unit606 compiler GS recipe differs')
    return dict(verified=True,source_class='ordinary-own-recipe compiler GS pair',normative=full,
        scalar_basis='i386 compiler-generated GS and accepted normal32 storage model, not DIR32 operand width',
        helper_boundary='compiler ECX machineword argument and void result',source_boundary_peer=PINS['crt-v14-GS-source-boundary-peer-v1.json'],runtime_ABI_approved=False)

def prepare():
    folder=ROOT/'build/rebuild';paths={folder/p:h for p,h in INPUT_PINS.items()}
    for p,h in paths.items():require(old.sha(p)==h,'protected input differs: '+p.name)
    load=lambda name:json.loads((folder/name).read_bytes())
    prior=load('application-crt-v13-four-contract-v1.json')
    sources={**prior['sources'],**{p:old.sha(ROOT/p) for p in SOURCES}}
    for p,h in prior['sources'].items():require(old.sha(ROOT/p)==h,'inherited source differs')
    require(old.sha(ROOT/'build/units.json')==prior['units_sha256'],'units differ')
    for p,h in OWN_SOURCES.items():require(old.sha(ROOT/p)==h,'own source differs')
    require(sources['tools/rebuild/application_link_wave14.py']=='5021fbfbf1c4efd4a52e8b65b84bc49b623a009673bebf390724f0c17eb72667' and
        sources['tools/rebuild/application_uuid2768.py']=='e04ec719cb4bf1fdc921b409ac510c85a1cd51255a5b165db9b820868814919a','reviewed shared consumers differ')
    baseline=json.loads(gzip.decompress((folder/'application-wave13-cohort-observation-v1/fields.json.gz').read_bytes()))
    fields=json.loads(gzip.decompress((folder/'application-wave14-cohort-observation-v2/fields.json.gz').read_bytes()))
    predecessor.previous.previous.complete_fields(baseline,BASELINE_FIELDS,base.FULL_DIGEST)
    predecessor.previous.previous.complete_fields(fields,COMPLETE_FIELDS,FULL_DIGEST)
    obs=load('application-wave14-cohort-observation-v2/receipt.json');namespace=obs['provider_namespace']['symbols']
    require(obs['complete_field_count']==COMPLETE_FIELDS and obs['fields_canonical_sha256']==FULL_DIGEST and
        obs['selected_Game_function_candidates']==14555 and obs['IAT_fields']==416,'combined observer scope differs')
    added=cohort_delta(baseline,fields,ACTUAL_COHORT)
    members=load('cached-frontier-code-v13-v1/members.json');wrappers=[]
    with gzip.open(folder/'cached-frontier-code-v13-v1/field-proofs.jsonl.gz','rt') as stream:
        for ordinal,line in enumerate(stream,1):require(ordinal<=21,'CODE21 wrapper expansion');wrappers.append(json.loads(line))
    norms=wave.verify_proof_ledger(wrappers,members,load('cached-frontier-code-v13-export-handoff-v1.json'))
    ordinary=join_code21([f for f in added if f['component']=='CODE21'],members,norms)
    uuid_evidence=uuid.consume({k:(folder/p).read_bytes() for k,p in UUID_PATHS.items()})
    uuid_rows=[f for f in added if f['component']=='uuid2768']
    require(same_record_multiset(uuid_rows,uuid_evidence['mapped_fields']),
        'complete UUID original/normative records differ; no selected-key or tuple/list shortcut')
    units=json.loads((ROOT/'build/units.json').read_bytes())['units'];by={old.field_key(f) for f in baseline}
    full_by={old.digest(r['normative']):r['normative'] for r in ordinary}
    predecessor.validate((folder/'application-crt-v13-four-contract-v1.json').read_bytes(),
        (folder/'application-crt-v13-four-contract-peer-v1.json').read_bytes(),
        (folder/'application-crt-v13-four-proposal-v1.rsp').read_bytes(),baseline,namespace)
    bindings=[]
    for previous_binding in prior['bindings']:
        b=copy.deepcopy(previous_binding);addr,role=b['original_base'],b['role']
        kind=next(k for a,r,e,k in old.BINDINGS if a==addr and r==role)
        uses=old.census(fields,addr,role,kind);new=[f for f in uses if old.field_key(f) not in by]
        require(old.canonical([f for f in uses if old.field_key(f) in by])==old.canonical(b['fields']),'old canonical evidence changed')
        evidence=[];reasons=[]
        for field in new:
            try:evidence.append(qualify_gs(field,full_by[field['proof']['field_proof_sha256']],units[606]))
            except (ValueError,KeyError,TypeError) as error:reasons.append(str(error))
        if b['canonical_undefined'] in namespace:reasons.append('canonical strong definition collision')
        require(b['normal_family']=='sp1' and b['normal_provider']['archive_sha256']==old.LIBRARY,'normal owner differs')
        b.update(inherited_new_fields=previous_binding['new_fields'],inherited_new_field_evidence=previous_binding['new_field_evidence'],
            fields=uses,field_count=len(uses),field_census_sha256=old.digest(uses),new_fields=new,new_field_evidence=evidence,
            baseline_field_count=previous_binding['field_count'],baseline_distinct_input_callers=previous_binding['distinct_input_callers'],
            distinct_input_callers=len({f['caller'] for f in uses}),enabled=not reasons,disabled_reasons=reasons)
        if role=='data':b['recipe_cookie_proofs']=previous_binding['recipe_cookie_proofs']+old.cookie_recipe_proofs(new,units)
        bindings.append(b)
    require([b['field_count'] for b in bindings]==[103,97,1,3],'full204 canonical census differs')
    coupled_disable(bindings)
    response=response_bytes(bindings,(folder/'application-crt-v13-four-proposal-v1.rsp').read_bytes())
    plan=copy.deepcopy(prior)
    plan.update(kind='V14-existing-four-CRT-diagnostic-contract',scope=SCOPE,inputs=INPUT_PINS,sources=sources,own_sources=OWN_SOURCES,
        complete_input_fields=COMPLETE_FIELDS,selected_field_sha256=FULL_DIGEST,actual_cohort=ACTUAL_COHORT,
        baseline_complete_fields=BASELINE_FIELDS,baseline_field_sha256=base.FULL_DIGEST,baseline_bindings=prior['bindings'],
        old_raw_source_records_preserved=True,old_annotation_delta=[],unknown_flags_preserved=True,requested_batch_assumed=False,
        extra_fields=55,new_field_evidence=added,new_normative_fields=ordinary,qualified_UUID_evidence=uuid_evidence,
        alias_field_count=ALIAS_USE_COUNT,new_current_CRT_uses=2,bindings=bindings,
        baseline_binding_contract_scope=prior['scope'],current_binding_evidence_scope=SCOPE,
        enabled_alias_count=sum(b['enabled'] for b in bindings),enabled_alias_field_count=sum(b['field_count'] for b in bindings if b['enabled']),
        response_text=response.decode('ascii'),response_sha256=hashlib.sha256(response).hexdigest(),
        namespace_sha256=old.digest(namespace),unreviewed_new_CRT_aliases=[],
        stability_scope='raw accepted observer receipt bound; underlying full identity ledger delegated to its peer, no identity-path rewalk')
    for p,h in paths.items():require(old.sha(p)==h,'protected input changed')
    for p,h in sources.items():require(old.sha(ROOT/p)==h,'source changed')
    for p,h in OWN_SOURCES.items():require(old.sha(ROOT/p)==h,'own source changed')
    require(old.sha(ROOT/'build/units.json')==plan['units_sha256'],'units changed')
    return plan,response

def run():
    folder=ROOT/'build/rebuild';output=folder/'application-crt-v14-four-contract-v1.json';rsp=folder/'application-crt-v14-four-proposal-v1.rsp'
    require(folder.resolve()==folder and not output.exists() and not rsp.exists(),'exclusive private outputs required')
    plan,response=prepare()
    with output.open('x',encoding='utf-8') as stream:json.dump(plan,stream,indent=2);stream.write('\n')
    with rsp.open('xb') as stream:stream.write(response)
    print(json.dumps(dict(plan_sha256=old.sha(output),response_sha256=old.sha(rsp),fields=COMPLETE_FIELDS,alias_fields=ALIAS_USE_COUNT,enabled_aliases=plan['enabled_alias_count'])))

if __name__=='__main__':run()
