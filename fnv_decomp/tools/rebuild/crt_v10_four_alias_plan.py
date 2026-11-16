"""Saved-only V10 existing-four CRT refresh; earlier cohorts stay immutable."""
from __future__ import annotations
import copy
import gzip
import json
import crt_v9_four_alias_contract as previous
import application_link_wave10 as wave10

v9=previous.v9
old=v9.old
ROOT=v9.ROOT
require=v9.require
FULL_DIGEST='1cc46a341abefc0a8d31269c650efa1a0337b58bd96e1c3732f440450af47132'
BASE_DIGEST=v9.FULL_DIGEST
OWN_SOURCES=v9.OWN_SOURCES
PINS={
 'application-crt-v9-four-contract-v1.json':previous.PLAN,
 'application-crt-v9-four-contract-peer-v1.json':previous.REVIEW,
 'application-crt-v9-four-proposal-v1.rsp':previous.RESPONSE,
 'crt-v9-four-consumer-peer-v1.json':'4241a5c3dfcea1be82ffe0755b7ae0546279d2cea824e630f12d20316307fc7f',
 'application-wave9-cohort-observation-v1/fields.json.gz':'36c69324f6ebf5113610b4de20bed24476eb2122bd02a585d2eaec773c228976',
 'application-wave10-cohort-observation-v1/receipt.json':'d002831408a68ca88fe6adfedeb7288c0092bf7b818ea0be7d63a032994d0351',
 'application-wave10-cohort-observation-v1/fields.json.gz':'03c64e17917dfdacefbea440431fe52442da2bc0ea93fc2c19f4526044d78978',
 'application-wave10-cohort-observation-v1/independent-outcome-review.json':'8f093e34ada6f7c9e22900987ffbbfbf5182b5129b44e5ec838952a33443040f',
 'frontier-wave-v8-production-v1/members.json':'611947ef6be7a3c3f0892736aad38010b671f352236d9ce59c4d17ee6a9c03e0',
 'frontier-wave-v8-production-v1/field-proofs.jsonl.gz':'5687052d155aa967591ba8007c08682e2c3513c8408a552e42060f1e37a79d74',
 'frontier-wave-v8-export-handoff-v1.json':'1359c2ec60f60cbf0f9b97b02a29dc2869d91b4a6ea5ca909f0c800b5cdc2b0d',
 'application-wave10-verifier-independent-review.json':'e4a599daaddb4e01a7e5c4c1dd5e4ac36b6c1eb966304c69bfa8d48bf22d42e0',
 'crt-v10-source-proof-pretriage-v1.json':'c5d9a331c97173c925267ddc58e18853cdf77f0c34e30e4dd994da7bab3eaf14',
 'crt-v10-pretriage-source-review-lane04-v1.json':'7983eed879422c1642e2cda39c80e30a0e38b8188478595232f050c86b6eddd1',
 'crt-v10-pretriage-source-snapshot-v1.py':'77352b5e6b44a202707203d2cf6a7322f834fcd413ef23bd3a052ac45c2401bb',
 'crt-v10-pretriage-test-snapshot-v1.py':'2feeadde4e0d8a56ff67e3f1993ace7e44e4cd8fe949cc5f540b62b43f85e1f5',
}
SOURCES=('tools/rebuild/crt_v10_four_alias_plan.py','tests/rebuild/test_crt_v10_four_alias_plan.py',
 'tools/rebuild/crt_v9_four_alias_contract.py','tools/rebuild/application_link_wave10.py',
 'tools/rebuild/application_link_diagnostic.py')

def member_proofs(members,envelopes,handoff):
    """Join exact saved normative records to every compact member field.

    This is a source-metadata join. It creates no provider identities and
    retains each normative record, including its unapproved ABI/state flags.
    """
    norms=wave10.verify_proof_ledger(envelopes,members,handoff)
    names={old.undefined(b,r) for b,r,e,k in old.BINDINGS}
    bases={b for b,r,e,k in old.BINDINGS}
    joined=[]
    for member in members:
        p=member['projection'];root=p['requested_roots'][0]
        for compact in p['fields']:
            sha=compact['field_proof_sha256'];full=norms[sha];rel=full['coff_relocation']
            require(full['recipe_id']==root['recipe_id'] and
                (rel['addend'] & 0xffffffff)==compact['addend_bits'],'full source recipe/addend differs')
            require(compact['canonical_name'] not in names and compact['original_base'] not in bases,
                'new use or role collision at an existing CRT identity requires separate source review')
            joined.append(dict(member=member['name'],root=root,compact=compact,normative_sha256=sha,normative_record=full))
    return joined

def new_fields(baseline,fields,members,joined):
    """Join the actual new rows without changing old records or proof classes."""
    before={old.canonical(f):f for f in baseline};after={old.canonical(f):f for f in fields}
    require(len(before)==len(baseline) and len(after)==len(fields),'duplicate complete raw field')
    require(all(k in after for k in before),'old raw source record changed or absent')
    added=[f for k,f in after.items() if k not in before]
    require(len(added)==len(joined)==629 and all(f['component']=='CODE68' for f in added),'not the exact629 CODE68 fields')
    byname={m['name']:m['projection'] for m in members}
    norm={(r['member'],r['compact']['section'],r['compact']['offset'],r['compact']['symbol_index']):r for r in joined}
    seen=set()
    for f in added:
        p=f['proof'];key=(f['member'],p['physical_section'],f['offset'],f['physical_symbol_index'])
        require(key in norm and key not in seen,'new physical field absent or duplicated');seen.add(key)
        r=norm[key];compact=r['compact'];projection=byname[f['member']];root=projection['requested_roots'][0]
        require(p==dict(compact,physical_section=compact['section'],field_offset=compact['offset']), 'new compact proof changed')
        require(f['root']==root['original_address'] and f['recipe_id']==root['recipe_id'] and
            f['object_sha256']==root['object_sha256']==projection['original_object_sha256'] and
            f['member_sha256']==projection['output_sha256'] and f['caller'] in projection['exports'] and
            f['canonical']==compact['canonical_name'] and f['kind']==compact['kind'] and
            f['section']==projection['maps']['section_map'][str(compact['section'])] and
            f['symbol_index']==projection['maps']['symbol_map'][str(compact['symbol_index'])], 'new source/serialized identity differs')
        require(type(f['undefined']) is bool and f['undefined']==any(
            u['serialized_symbol_index']==f['symbol_index'] for u in projection['undefined']), 'new symbol definition class differs')
        if 'original_field_proof' in f:require(f['original_field_proof']==r['normative_record'],'hydrated original proof differs')
    require(len(seen)==len(norm)==629,'incomplete original proof coverage')
    return sorted(added,key=old.canonical)

def prepare():
    folder=ROOT/'build/rebuild';paths={folder/p:h for p,h in PINS.items()}
    for p,h in paths.items():require(old.sha(p)==h,'protected input differs: '+p.name)
    load=lambda name:json.loads((folder/name).read_bytes())
    baseline=json.loads(gzip.decompress((folder/'application-wave9-cohort-observation-v1/fields.json.gz').read_bytes()))
    fields=json.loads(gzip.decompress((folder/'application-wave10-cohort-observation-v1/fields.json.gz').read_bytes()))
    previous.previous.previous.complete_fields(baseline,45318,BASE_DIGEST)
    previous.previous.previous.complete_fields(fields,45947,FULL_DIGEST)
    obs=load('application-wave10-cohort-observation-v1/receipt.json')
    require(obs['kind']=='wave10-CODE68-field-observation' and obs['complete_field_count']==45947 and
        obs['fields_canonical_sha256']==FULL_DIGEST and obs['IAT_fields']==413 and
        obs['selected_Game_function_candidates']==14476 and obs['ordinary_prepared_count']==14471,'observation scope differs')
    envelopes=[]
    with gzip.open(folder/'frontier-wave-v8-production-v1/field-proofs.jsonl.gz','rt') as stream:
        for ordinal,line in enumerate(stream,1):
            require(ordinal<=68,'unapproved proof envelope expansion');envelopes.append(json.loads(line))
    members=load('frontier-wave-v8-production-v1/members.json')
    joined=member_proofs(members,envelopes,load('frontier-wave-v8-export-handoff-v1.json'))
    pretriage=load('crt-v10-source-proof-pretriage-v1.json')
    require(joined==pretriage['joined_normative_fields'] and pretriage['new_existing_four_CRT_uses']==0,
        'accepted normative pretriage differs')
    added=new_fields(baseline,fields,members,joined)
    prior=load('application-crt-v9-four-contract-v1.json')
    inherited=(folder/'application-crt-v9-four-proposal-v1.rsp').read_bytes();namespace=obs['provider_namespace']['symbols']
    previous.validate((folder/'application-crt-v9-four-contract-v1.json').read_bytes(),
        (folder/'application-crt-v9-four-contract-peer-v1.json').read_bytes(),inherited,baseline,namespace)
    previous.previous.validate_bindings(prior['bindings'],fields,namespace)
    sources={**prior['sources'],**{p:old.sha(ROOT/p) for p in SOURCES}}
    for p,h in prior['sources'].items():require(old.sha(ROOT/p)==h,'inherited source differs')
    require(old.sha(ROOT/'build/units.json')==prior['units_sha256'],'units differ')
    for p,h in OWN_SOURCES.items():require(old.sha(ROOT/p)==h,'own source differs')
    plan=copy.deepcopy(prior)
    plan.update(kind='V10-existing-four-CRT-diagnostic-contract',scope='V9-plus-CODE68',inputs=PINS,sources=sources,
        complete_input_fields=45947,selected_field_sha256=FULL_DIGEST,baseline_complete_fields=45318,
        baseline_field_sha256=BASE_DIGEST,old_raw_source_records_preserved=True,old_annotation_delta=[],extra_fields=629,
        new_field_evidence=added,new_fields_use_existing_CRT_aliases=False,new_current_CRT_uses=0,
        inherited_binding_evidence_scope=prior['inherited_binding_evidence_scope'],
        namespace_sha256=old.digest(namespace),unreviewed_new_CRT_aliases=[])
    for p,h in paths.items():require(old.sha(p)==h,'protected input changed')
    for p,h in sources.items():require(old.sha(ROOT/p)==h,'source changed')
    for p,h in OWN_SOURCES.items():require(old.sha(ROOT/p)==h,'own source changed')
    require(old.sha(ROOT/'build/units.json')==plan['units_sha256'],'units changed')
    return plan,inherited

def run():
    folder=ROOT/'build/rebuild';out=folder/'application-crt-v10-four-contract-v1.json';rsp=folder/'application-crt-v10-four-proposal-v1.rsp'
    require(folder.resolve()==folder and not out.exists() and not rsp.exists(),'exclusive private outputs required')
    plan,response=prepare()
    with out.open('x',encoding='utf-8') as stream:json.dump(plan,stream,indent=2);stream.write('\n')
    with rsp.open('xb') as stream:stream.write(response)
    print(json.dumps(dict(plan_sha256=old.sha(out),response_sha256=old.sha(rsp),fields=45947,alias_fields=202,enabled_aliases=4)))

if __name__=='__main__':run()
