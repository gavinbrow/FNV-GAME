"""Saved-only V13 existing-four CRT refresh; all earlier cohorts stay immutable."""
from __future__ import annotations
import copy
import gzip
import json
import crt_v10_four_alias_contract as previous
import application_link_wave13 as wave13

base=previous.v10
old=base.old
ROOT=base.ROOT
require=base.require
BASE_DIGEST=base.FULL_DIGEST
OWN_SOURCES=base.OWN_SOURCES
OBSERVATION='application-wave13-cohort-observation-v1'
FULL_DIGEST='9c3a5244bc016e8d2a707b6d471823bd968aff21d3be0efb2efed087ec7065a3'
IAT_FIELDS=414
ORDINARY=14528
PINS={
 'application-crt-v10-four-contract-v1.json':previous.PLAN,
 'application-crt-v10-four-contract-peer-v1.json':previous.REVIEW,
 'application-crt-v10-four-proposal-v1.rsp':previous.RESPONSE,
 'crt-v10-four-consumer-peer-v1.json':'4ffdddd38e108fa11f3a80490c91548dcf997a04688208019208f1292ad0270c',
 'application-wave10-cohort-observation-v1/fields.json.gz':'03c64e17917dfdacefbea440431fe52442da2bc0ea93fc2c19f4526044d78978',
 OBSERVATION+'/receipt.json':'e19302008032c9bb733eeaa32e2db1f075aa420ef5067332cf0857eaab094c69',
 OBSERVATION+'/fields.json.gz':'b7823e8892a4a5051d42b6447078058f5d0be4d3db0dc3bfbf5630621b73f23a',
 OBSERVATION+'/independent-outcome-review.json':'aecffece805bad88152f80a340a2074349795b59164390d7376df687c3d008ce',
 'cached-frontier-code-v12-v1/members.json':'5c39833286b1b37f3fcbf9f483daaa8f5852b3bfc1620b9bb2b0732d2fd2581d',
 'cached-frontier-code-v12-v1/field-proofs.jsonl.gz':'57b1ccf51a71eec09b8aae405fc1f4593f55c0cbb48de348431bab76b08a05b5',
 'cached-frontier-code-v12-export-handoff-v1.json':'5150b751ae74e19c7850ddcc8608f0935afea984d22b907d950154963a0debcb',
 'code-lane01-analysis-v1/cached-frontier-code-v12-handoff-review-v1.json':'4264c15143b65197aedc3997e0faa59cb4235f3ee5027c63031f47efbfd921c0',
 'application-wave13-verifier-independent-review.json':'6c997ce04f33dff74bece022e1e6a891b31a5d2345e4ce7a3da6e9412c7ebb36',
 'application-link-diagnostic-v12-comdat-v2/receipt.json':'9dd9b2d6a8627cbbc98eeabadf32a03244645634f852fbd341c85bf3cf30998e',
 'application-link-diagnostic-v12-comdat-v2/link-receipt.json.gz':'6700a779ddbbfc58fd122d7e731d5424920bfb9561ce81a7500ba21c8be19405',
 'application-link-diagnostic-v12-comdat-v2/independent-outcome-review.json':'2da9a6e506ead22b7177c13b460f2190117759b91a686b5e5a1119b8c37cbc17',
 'application-link-diagnostic-v12-comdat-v2/crt-plan-independent-outcome-review.json':'aa5298385ff38d88340b1906c58ab78d83e9454026175bba861edf86dc05854c',
}
SOURCES=('tools/rebuild/crt_v13_four_alias_plan.py','tests/rebuild/test_crt_v13_four_alias_plan.py',
 'tools/rebuild/crt_v10_four_alias_contract.py','tools/rebuild/application_link_wave13.py',
 'tools/rebuild/application_link_diagnostic.py')

def member_proofs(members,envelopes,handoff):
    """Join exact saved normative records to every compact member field.

    This is a source-metadata join. It creates no provider identities and
    retains each normative record, including its unapproved ABI/state flags.
    """
    norms=wave13.verify_proof_ledger(envelopes,members,handoff)
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
    require(len(added)==len(joined)==290 and all(f['component']=='CODE56' for f in added),'not the exact290 CODE56 fields')
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
    require(len(seen)==len(norm)==290,'incomplete original proof coverage')
    return sorted(added,key=old.canonical)

def prepare():
    folder=ROOT/'build/rebuild';paths={folder/p:h for p,h in PINS.items()}
    for p,h in paths.items():require(old.sha(p)==h,'protected input differs: '+p.name)
    load=lambda name:json.loads((folder/name).read_bytes())
    baseline=json.loads(gzip.decompress((folder/'application-wave10-cohort-observation-v1/fields.json.gz').read_bytes()))
    fields=json.loads(gzip.decompress((folder/(OBSERVATION+'/fields.json.gz')).read_bytes()))
    previous.previous.previous.complete_fields(baseline,45947,BASE_DIGEST)
    previous.previous.previous.complete_fields(fields,46237,FULL_DIGEST)
    obs=load(OBSERVATION+'/receipt.json')
    require(obs['kind']=='wave13-CODE56-field-observation' and obs['complete_field_count']==46237 and
        obs['fields_canonical_sha256']==FULL_DIGEST and obs['IAT_fields']==IAT_FIELDS and
        obs['selected_Game_function_candidates']==14533 and obs['ordinary_prepared_count']==ORDINARY,'observation scope differs')
    envelopes=[]
    with gzip.open(folder/'cached-frontier-code-v12-v1/field-proofs.jsonl.gz','rt') as stream:
        for ordinal,line in enumerate(stream,1):
            require(ordinal<=56,'unapproved proof envelope expansion');envelopes.append(json.loads(line))
    members=load('cached-frontier-code-v12-v1/members.json')
    joined=member_proofs(members,envelopes,load('cached-frontier-code-v12-export-handoff-v1.json'))
    added=new_fields(baseline,fields,members,joined)
    prior=load('application-crt-v10-four-contract-v1.json')
    inherited=(folder/'application-crt-v10-four-proposal-v1.rsp').read_bytes();namespace=obs['provider_namespace']['symbols']
    previous.validate((folder/'application-crt-v10-four-contract-v1.json').read_bytes(),
        (folder/'application-crt-v10-four-contract-peer-v1.json').read_bytes(),inherited,baseline,namespace)
    previous.previous.validate_bindings(prior['bindings'],fields,namespace)
    sources={**prior['sources'],**{p:old.sha(ROOT/p) for p in SOURCES}}
    for p,h in prior['sources'].items():require(old.sha(ROOT/p)==h,'inherited source differs')
    require(old.sha(ROOT/'build/units.json')==prior['units_sha256'],'units differ')
    for p,h in OWN_SOURCES.items():require(old.sha(ROOT/p)==h,'own source differs')
    plan=copy.deepcopy(prior)
    plan.update(kind='V13-existing-four-CRT-diagnostic-contract',scope='V12-plus-CODE56',inputs=PINS,sources=sources,
        complete_input_fields=46237,selected_field_sha256=FULL_DIGEST,baseline_complete_fields=45947,
        baseline_field_sha256=BASE_DIGEST,old_raw_source_records_preserved=True,old_annotation_delta=[],extra_fields=290,
        new_field_evidence=added,new_normative_fields=joined,normative_source_evidence_enriched=False,new_fields_use_existing_CRT_aliases=False,new_current_CRT_uses=0,
        inherited_binding_evidence_scope=prior['inherited_binding_evidence_scope'],
        namespace_sha256=old.digest(namespace),unreviewed_new_CRT_aliases=[])
    for p,h in paths.items():require(old.sha(p)==h,'protected input changed')
    for p,h in sources.items():require(old.sha(ROOT/p)==h,'source changed')
    for p,h in OWN_SOURCES.items():require(old.sha(ROOT/p)==h,'own source changed')
    require(old.sha(ROOT/'build/units.json')==plan['units_sha256'],'units changed')
    return plan,inherited

def run():
    folder=ROOT/'build/rebuild';out=folder/'application-crt-v13-four-contract-v1.json';rsp=folder/'application-crt-v13-four-proposal-v1.rsp'
    require(folder.resolve()==folder and not out.exists() and not rsp.exists(),'exclusive private outputs required')
    plan,response=prepare()
    with out.open('x',encoding='utf-8') as stream:json.dump(plan,stream,indent=2);stream.write('\n')
    with rsp.open('xb') as stream:stream.write(response)
    print(json.dumps(dict(plan_sha256=old.sha(out),response_sha256=old.sha(rsp),fields=46237,alias_fields=202,enabled_aliases=4)))

if __name__=='__main__':run()
