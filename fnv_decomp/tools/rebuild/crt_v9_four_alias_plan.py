"""Saved-only V9 refresh of the existing four CRT bindings; V8 is immutable."""
from __future__ import annotations
import copy
import gzip
import hashlib
import json

import crt_v8_four_alias_contract as previous

v8=previous.v8
old=v8.old
ROOT=v8.ROOT
require=v8.require
FULL_DIGEST='e48b6cad71c8108c27062db4aa9ae8429af3cfa6f7113753fe3ed8bf4e582d2c'
BASE_DIGEST=v8.FULL_DIGEST
OWN_SOURCES=v8.OWN_SOURCES
PINS={
 'application-crt-v8-four-contract-v1.json':previous.PLAN,
 'application-crt-v8-four-contract-peer-v1.json':previous.REVIEW,
 'application-crt-v8-four-proposal-v1.rsp':previous.RESPONSE,
 'crt-v8-four-consumer-peer-v1.json':'39fd4ef487361e9d3827c1da01cd73501035f3cab674290ae025294b50ae8c78',
 'application-wave8-cohort-observation-v1/fields.json.gz':'2e5cb28f81cf5042c31ae80f7db49ef003df693cf428fb678d7f116a907425bf',
 'application-wave9-cohort-observation-v1/receipt.json':'1aa0c183db889f70dd9af88d934b61f8cc82297924656c5fe7483ebca4c16410',
 'application-wave9-cohort-observation-v1/fields.json.gz':'36c69324f6ebf5113610b4de20bed24476eb2122bd02a585d2eaec773c228976',
 'application-wave9-cohort-observation-v1/independent-outcome-review.json':'7ce0cd49abd728ffc64521193faccbcbe54114904cb3889811cf725327bffae4',
 'frontier-wave-v7-production-v1/members.json':'4d914daea1c5934606b568ecba475343260b3c3d14e83b04879908e280fec166',
 'frontier-wave-v7-export-handoff-v1.json':'68a8110c92bf095a777f448d743ffd364eff370245d492fe26eee4395d3ec509',
}
SOURCES=('tools/rebuild/crt_v9_four_alias_plan.py','tests/rebuild/test_crt_v9_four_alias_plan.py',
 'tools/rebuild/crt_v8_four_alias_contract.py','tools/rebuild/crt_frontier_adoption_contract.py',
 'tools/rebuild/crt_adoption_consumer_contract.py')
EXPECTED={('0x004f8ac0',30):('0x00406d30',79,305,7,'48e2d36174b75af2b280a63569e147b9ba77478a6d64e51b63fe7bd426ae88b9'),
 ('0x0096aaf0',21):('0x0096abc0',65,395,8,'585bd9093d17c9fbd298b1c8a09cd26a144962db6eec871c05634712165ca9ae'),
 ('0x0096aaf0',36):('0x0096aa40',65,394,7,'374238e57784d411cc4fa7efd06bf5a0963c3703090eb397ae8b7f9c1a0db510')}

def new_fields(baseline,fields,members):
    """Prove an exact raw-record superset and the three new physical maps."""
    before={old.canonical(f):f for f in baseline};after={old.canonical(f):f for f in fields}
    require(len(before)==len(baseline) and len(after)==len(fields),'duplicate complete raw field')
    require(all(k in after for k in before),'old raw source record changed or absent')
    added=[f for k,f in after.items() if k not in before]
    require(len(added)==3 and {(f['root'],f['offset']) for f in added}==set(EXPECTED), 'not the three approved new fields')
    require(len(members)==3 and {m['projection']['requested_roots'][0]['original_address'] for m in members}==
        {'0x004f8ac0','0x005d43c0','0x0096aaf0'},'new member scope differs')
    require(sum(len(m['projection']['fields']) for m in members)==3,'member field count differs')
    byname={m['name']:m['projection'] for m in members}
    for f in added:
        base,section,physical,serialized,sha=EXPECTED[(f['root'],f['offset'])]
        p=f['proof'];projection=byname[f['member']];root=projection['requested_roots'][0]
        raw=[r for r in projection['fields'] if r['offset']==f['offset']]
        require(len(raw)==1,'new raw field absent/ambiguous');raw=raw[0]
        expected=dict(raw,physical_section=raw['section'],field_offset=raw['offset'])
        require(p==expected and raw['original_base']==raw['original_target']==base and raw['role']=='code' and
            raw['section']==section and raw['symbol_index']==physical and raw['field_proof_sha256']==sha and
            raw['kind']==20 and raw['addend_bits']==0,'new exact raw proof differs')
        require(f['component']=='V9-three-CODE' and f['root']==root['original_address'] and
            f['recipe_id']==root['recipe_id'] and f['object_sha256']==root['object_sha256']==projection['original_object_sha256'] and
            f['member_sha256']==projection['output_sha256'] and f['caller'] in projection['exports'] and
            f['canonical']==raw['canonical_name'] and f['undefined'] is True and f['kind']==20 and
            f['physical_symbol_index']==physical and f['symbol_index']==serialized==projection['maps']['symbol_map'][str(physical)] and
            f['section']==2==projection['maps']['section_map'][str(section)],'new serialized/source identity differs')
        require(f['canonical'] not in {old.undefined(b,r) for b,r,e,k in old.BINDINGS},'unexpected new use of existing CRT alias')
    return sorted(added,key=old.canonical)

def prepare():
    folder=ROOT/'build/rebuild';paths={folder/p:h for p,h in PINS.items()}
    for p,h in paths.items():require(old.sha(p)==h,'protected input differs: '+p.name)
    load=lambda name:json.loads((folder/name).read_bytes())
    baseline=json.loads(gzip.decompress((folder/'application-wave8-cohort-observation-v1/fields.json.gz').read_bytes()))
    fields=json.loads(gzip.decompress((folder/'application-wave9-cohort-observation-v1/fields.json.gz').read_bytes()))
    previous.previous.previous.complete_fields(baseline,45315,BASE_DIGEST)
    previous.previous.previous.complete_fields(fields,45318,FULL_DIGEST)
    obs=load('application-wave9-cohort-observation-v1/receipt.json')
    require(obs['kind']=='wave9-three-CODE-field-observation' and obs['complete_field_count']==45318 and
        obs['fields_canonical_sha256']==FULL_DIGEST and obs['IAT_fields']==409 and
        obs['selected_Game_function_candidates']==14408 and obs['ordinary_prepared_count']==14403,'observation scope differs')
    added=new_fields(baseline,fields,load('frontier-wave-v7-production-v1/members.json'))
    prior=load('application-crt-v8-four-contract-v1.json')
    inherited=(folder/'application-crt-v8-four-proposal-v1.rsp').read_bytes()
    namespace=obs['provider_namespace']['symbols']
    previous.validate((folder/'application-crt-v8-four-contract-v1.json').read_bytes(),
        (folder/'application-crt-v8-four-contract-peer-v1.json').read_bytes(),inherited,baseline,namespace)
    previous.previous.validate_bindings(prior['bindings'],fields,namespace)
    sources={**prior['sources'],**{p:old.sha(ROOT/p) for p in SOURCES}}
    for p,h in prior['sources'].items():require(old.sha(ROOT/p)==h,'inherited source differs')
    require(old.sha(ROOT/'build/units.json')==prior['units_sha256'],'units differ')
    for p,h in OWN_SOURCES.items():require(old.sha(ROOT/p)==h,'own source differs')
    plan=copy.deepcopy(prior)
    plan.update(kind='V9-existing-four-CRT-diagnostic-contract',scope='V8-plus-three-CODE',inputs=PINS,sources=sources,
        complete_input_fields=45318,selected_field_sha256=FULL_DIGEST,baseline_complete_fields=45315,
        baseline_field_sha256=BASE_DIGEST,old_raw_source_records_preserved=True,old_annotation_delta=[],extra_fields=3,
        new_field_evidence=added,new_fields_use_existing_CRT_aliases=False,new_current_CRT_uses=0,
        inherited_binding_evidence_scope=prior['scope'],
        namespace_sha256=old.digest(namespace),unreviewed_new_CRT_aliases=[])
    for p,h in paths.items():require(old.sha(p)==h,'protected input changed')
    for p,h in sources.items():require(old.sha(ROOT/p)==h,'source changed')
    for p,h in OWN_SOURCES.items():require(old.sha(ROOT/p)==h,'own source changed')
    require(old.sha(ROOT/'build/units.json')==plan['units_sha256'],'units changed')
    return plan,inherited

def run():
    folder=ROOT/'build/rebuild';out=folder/'application-crt-v9-four-contract-v1.json';rsp=folder/'application-crt-v9-four-proposal-v1.rsp'
    require(folder.resolve()==folder and not out.exists() and not rsp.exists(),'exclusive private outputs required')
    plan,response=prepare()
    with out.open('x',encoding='utf-8') as stream:json.dump(plan,stream,indent=2);stream.write('\n')
    with rsp.open('xb') as stream:stream.write(response)
    print(json.dumps(dict(plan_sha256=old.sha(out),response_sha256=old.sha(rsp),fields=45318,alias_fields=202,enabled_aliases=4)))

if __name__=='__main__':run()
