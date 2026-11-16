"""Bounded DATA-only successor; immutable accepted CODE archive is unchanged.

Mechanical partial-link provider choices are separate from runtime/ABI approval.
"""
from __future__ import annotations
import copy
import json
from pathlib import Path
import struct
import tempfile

import data_address_projection as data
import runtime_code_pool as namespace
from coff_rewrite import strict_object

POLICY='bounded-data-provider-bridge-v1'
COUNTS=dict(CODE_renames=13,self_definitions=406,DATA_base_definitions=119,CODE_fields=267,
    original_DATA_fields=13869,original_symbols=6381,remaining_new_address_demands=5960)
RUNTIME=dict(runtime_eligible=False,ABI_approved=False,lifetime_approved=False,application_link_ready=False)
sha,require,digest=data.sha,data.require,data.digest


def parsed(path):
    coff,symptr,strptr,_=strict_object(path)
    return coff,symptr,struct.unpack_from('<I',coff.data,12)[0],strptr


def policy_contract(p):
    require(p.get('schema_version')==1 and p.get('policy_id')==POLICY and p.get('counts')==COUNTS,'unsupported bridge scope')
    require(p.get('fragment')==dict(start=data.START,size=data.SIZE,section=1,alignment=4096,anchor_value=0), 'fragment/alignment scope differs')
    require(all(p.get(k)==v for k,v in RUNTIME.items()) and p.get('default_action')=='certify-only' and
        p.get('root_go_required_for_successor') is True,'runtime/default action unsupported')
    require(len(p.get('input_pins',{}))==10 and p.get('CODE_archive_sha256')=='1d5d9ae7ba169f2389a3e9928a46fcbeb8f25b829bcdaee627db3f43e9d89aa5' and
        p.get('whole_DATA_sha256')=='a802d79760989e8131634401f5a1594f800a8e36602b31bdbe9b8a70b0d3486d','accepted artifact scope differs')


def certify_core(path,projection,plan,expected=COUNTS):
    """Pure certificate core; file collector must bind all actual input hashes."""
    coff,symptr,count,strptr=parsed(path)
    require(len(coff.sections)==1 and coff.sections[1]['name']=='.data' and coff.sections[1]['flags']==0xc0d00040 and
        not coff.directives,'unsupported DATA flags/section/directive')
    require(count==len(coff.symbols)==expected['original_symbols'] and all(s['aux_count']==0 for s in coff.symbols.values()),'symbol/auxiliary coverage differs')
    sec=coff.sections[1];fields=projection['fields'];require(len(fields)==expected['original_DATA_fields'],'complete DATA fields required')
    by_name={s['name']:s for s in coff.symbols.values()};require(len(by_name)==count,'duplicate input symbol names')
    raw=struct.unpack_from('<I',coff.data,40)[0];payload=bytearray(coff.data[raw:raw+sec['size']]);physical=[];observed=[]
    for offset,index,kind in sec['relocs']:
        require(kind==6 and 0<=offset<=len(payload)-4,'unsupported DATA relocation')
        physical.append(dict(section=1,offset=offset,kind=6,serialized_symbol_index=index,symbol=coff.symbols[index]['name'],addend=struct.unpack_from('<I',payload,offset)[0]))
        observed.append((offset,coff.symbols[index]['name'],0))
    require(physical==projection['proof']['physical_field_map'] and all(x['addend']==0 for x in physical) and
        sorted(observed)==sorted((f['offset'],f['symbol'],f['addend']) for f in fields),'DATA field/index/zero-addend bijection differs')
    demands={}
    for f in fields:
        require(data.demand_identity(projection['coordinate_space'],f['original_target'],f['identity']['role'])==(f['symbol'],f['identity']) and
            f['addend']==0,'address identity/addend mismatch')
        if f['symbol'] in demands:require(demands[f['symbol']]['original_target']==f['original_target'],'conflicting address demand')
        demands[f['symbol']]=f
        struct.pack_into('<I',payload,f['offset'],f['original_target'])
    require(data.hashlib.sha256(payload).hexdigest()==projection['proof']['payload_sha256'],'input payload provenance differs')
    anchor=by_name.get(projection['anchor']);require(anchor and (anchor['section'],anchor['value'],anchor['storage'])==(1,0,2),'coordinate anchor shifted')
    start=plan['alignment_phase_proof']['original_start'];size=sec['size']
    require(start%4096==0 and plan['alignment_phase_proof']['COFF_required_alignment']==4096 and
        plan['alignment_phase_proof']['coordinate_anchor_value']==0,'alignment phase proof differs')
    renames=[];destinations=set()
    for c in plan['CODE_candidates']:
        name=c['address_demand'];f=demands.get(name);s=by_name.get(name);coverage=c['coverage']['record'];identity=c['input_physical_identity']
        require(f and s and f['identity']['role']==data.CODE_ROLE and f['original_target']==c['original_target'] and
            (s['section'],s['value'],s['storage'],s['type'])==(0,0,2,0),'unproved CODE demand record')
        require(coverage['status']=='EMITTED' and coverage['fresh_reference_match'] is True and
            int(coverage['original_address'],16)==c['original_target'] and coverage['physical_identity']==identity and
            c['canonical_provider']==namespace.canonical(identity) and coverage['member']==c['member']['name'], 'CODE physical provider join differs')
        require(c['canonical_provider'] not in by_name and c['canonical_provider'] not in destinations,'CODE destination collision')
        destinations.add(c['canonical_provider']);renames.append(dict(index=s['index'],old_name=name,new_name=c['canonical_provider'],
            original_target=c['original_target'],provider=copy.deepcopy(c)))
    require(len(renames)==expected['CODE_renames'] and len({r['index'] for r in renames})==len(renames),'CODE rename coverage differs')
    self_defs=[]
    for name,f in demands.items():
        target=f['original_target']
        if f['identity']['role']==data.DATA_ROLE and start<=target<start+size:
            s=by_name[name];require((s['section'],s['value'],s['storage'],s['type'])==(0,0,2,0),'self demand already/incorrectly defined')
            self_defs.append(dict(index=s['index'],name=name,section=1,value=target-start,original_target=target))
    declared={(r['demand'],r['target'],r['section'],r['value']) for r in plan['self_storage_candidates']}
    require({(r['name'],r['original_target'],r['section'],r['value']) for r in self_defs}==declared and
        len(self_defs)==expected['self_definitions'],'complete self-storage candidate set differs')
    bases={};reverse=[];field_keys=set()
    for c in plan['CODE_to_whole_DATA_candidates']:
        o=c['obligation'];base=int(o['original_base'],16);target=int(o['original_target'],16);bits=o['addend_bits']
        require(type(bits) is int and 0<=bits<=0xffffffff and o['kind']==6 and o['role']=='data' and
            o['canonical_name']==namespace.unresolved(o['original_base'],'data'),'reverse CODE identity/representation differs')
        signed=bits if bits<0x80000000 else bits-0x100000000
        require(start<=base<start+size and start<=target<start+size and ((base+bits)&0xffffffff)==target and
            base+signed==target and c['provider_section']==1 and c['provider_value']==base-start and
            c['target_provider_offset']==target-start and c['checked_addend_signed']==signed, 'base/addend algebra/boundary differs')
        key=(c['member'],o['original_address'],o['physical_section'],o['field_offset']);require(key not in field_keys,'duplicate reverse CODE field');field_keys.add(key)
        name=o['canonical_name'];require(name not in by_name and name not in destinations,'reverse DATA alias collision')
        row=dict(name=name,section=1,value=base-start,original_base=base)
        require(name not in bases or bases[name]==row,'conflicting reverse DATA base');bases[name]=row;reverse.append(copy.deepcopy(c))
    require(len(bases)==expected['DATA_base_definitions'] and len(reverse)==expected['CODE_fields'],'reverse DATA/field coverage differs')
    require(not plan['DATA16_candidates'] and not plan['CODE_to_whole_DATA_cross_boundary_blockers'],'unsupported small DATA/cross-boundary bridge')
    remaining=set(demands)-{r['old_name'] for r in renames}-{r['name'] for r in self_defs}
    require(len(remaining)==expected['remaining_new_address_demands'],'remaining unresolved count differs')
    return dict(schema_version=1,kind='bounded-data-provider-bridge-certificate',input_object_sha256=sha(path),
        input_symbols=count,coordinate_space=projection['coordinate_space'],CODE_renames=sorted(renames,key=lambda r:r['index']),
        self_definitions=sorted(self_defs,key=lambda r:r['index']),DATA_base_definitions=[bases[n] for n in sorted(bases)],
        reverse_CODE_field_proofs=reverse,DATA_fields=physical,remaining_new_address_demands=len(remaining),
        alignment_phase_proof=copy.deepcopy(plan['alignment_phase_proof']),actual_final_placement_verified=False,
        CODE_archive_unchanged=True,small_DATA_unchanged=True,bounded_partial_link_provider_selection=dict(applied=False,
            CODE_exports=len(renames),self_storage_views=len(self_defs),canonical_DATA_bases=len(bases),complete_for_application=False),**RUNTIME)


def successor_bytes(path,cert):
    coff,symptr,count,strptr=parsed(path);require(sha(path)==cert['input_object_sha256'],'stale certificate object')
    data_bytes=bytearray(coff.data[:strptr]);strings=bytearray(coff.data[strptr:]);extra=bytearray()
    for r in cert['CODE_renames']:
        name=r['new_name'].encode('ascii');struct.pack_into('<II',data_bytes,symptr+r['index']*18,0,len(strings));strings+=name+b'\0'
    for r in cert['self_definitions']:struct.pack_into('<Ih',data_bytes,symptr+r['index']*18+8,r['value'],1)
    for r in cert['DATA_base_definitions']:
        extra+=struct.pack('<IIIhHBB',0,len(strings),r['value'],1,0,2,0);strings+=r['name'].encode('ascii')+b'\0'
    struct.pack_into('<I',data_bytes,12,count+len(cert['DATA_base_definitions']));struct.pack_into('<I',strings,0,len(strings))
    return bytes(data_bytes+extra+strings)


def validate_successor(original,successor,cert):
    old,sp,count,st=parsed(original);new,nsp,ncount,nst=parsed(successor)
    require(sha(original)==cert['input_object_sha256'] and sp==nsp and ncount==count+len(cert['DATA_base_definitions']), 'symbol table map differs')
    prefix=bytearray(old.data[:sp]);struct.pack_into('<I',prefix,12,ncount)
    require(bytes(prefix)==new.data[:nsp] and old.sections==new.sections and not new.directives,'payload/geometry/relocations changed')
    renames={r['index']:r for r in cert['CODE_renames']};selfs={r['index']:r for r in cert['self_definitions']}
    for index,s in old.symbols.items():
        expected=copy.deepcopy(s)
        if index in renames:expected['name']=renames[index]['new_name']
        if index in selfs:expected.update(section=1,value=selfs[index]['value'])
        require(new.symbols.get(index)==expected,'original symbol/index/type changed outside bridge')
    for i,r in enumerate(cert['DATA_base_definitions']):
        require(new.symbols[count+i]==dict(index=count+i,name=r['name'],value=r['value'],section=1,type=0,storage=2,aux_count=0), 'appended DATA alias differs')
    require(new.data[nst+4:nst+(len(old.data)-st)]==old.data[st+4:] and len({s['name'] for s in new.symbols.values()})==ncount,
        'original strings lost or destination names coalesced')
    # Every relocation preserves its old physical target index. Names may differ
    # only at the thirteen explicitly certified records.
    maps=[]
    for off,index,kind in new.sections[1]['relocs']:
        maps.append(dict(offset=off,kind=kind,original_index=index,serialized_index=index,
            old_name=old.symbols[index]['name'],new_name=new.symbols[index]['name'],
            target_section=new.symbols[index]['section'],target_value=new.symbols[index]['value']))
    require(len(maps)==len(cert['DATA_fields']),'complete DATA field map differs')
    return dict(object_sha256=sha(successor),symbols=ncount,physical_field_map=maps,
        unchanged_payload_and_relocation_records=True,original_symbol_indices_preserved=True,
        undefined_symbols=sum(s['section']==0 for s in new.symbols.values()),**RUNTIME)


def collect(policy_path,plan_path,root):
    root=Path(root).resolve();p=json.loads(Path(policy_path).read_text());policy_contract(p)
    require(sha(plan_path)==p['plan_sha256'],'bridge plan changed');plan=json.loads(Path(plan_path).read_text())
    bindings={str(Path(policy_path).resolve()):sha(policy_path),str(Path(plan_path).resolve()):sha(plan_path),str(Path(__file__).resolve()):sha(__file__)}
    for relative,h in {**p['input_pins'],**p['implementation_pins']}.items():
        path=(root/relative).resolve();require(path.is_relative_to(root),'input path escapes root');bindings[str(path)]=h
    data.stable(bindings);require(not (root/'build/function_index.json').exists(),'optional index state changed')
    projection_path=root/'build/rebuild/data-address-projection-v1/projection.json';projection=json.loads(projection_path.read_text())
    require(projection['coordinate_space']==p['coordinate_space'] and plan['inputs']==p['input_pins'],'coordinate/input joins differ')
    for path,h in projection['protected_inputs'].items():
        require(path not in bindings or bindings[path]==h,'protected input conflict');bindings[path]=h
    original=root/'build/rebuild/data-address-projection-v1/whole-data.obj'
    require(sha(original)==p['whole_DATA_sha256'],'accepted DATA object changed')
    cert=certify_core(original,projection,plan);data.stable(bindings)
    return cert,bindings,original


def operate(policy_path,plan_path,root,authorization_path,out):
    """One existing source-review/root-go gate, no implicit emission/link."""
    auth=json.loads(Path(authorization_path).read_text());out=Path(out).resolve();root=Path(root).resolve()
    require(auth.get('kind')=='bounded-data-provider-bridge-authorization' and auth.get('source_review_accepted') is True and
        auth.get('root_authorized') is True and auth.get('reviewer') and auth.get('action') in ('certificate-only','apply-successor') and
        auth.get('source_sha256')==sha(__file__) and auth.get('policy_sha256')==sha(policy_path),'source/root authorization absent/stale')
    cert,bindings,original=collect(policy_path,plan_path,root);bindings[str(Path(authorization_path).resolve())]=sha(authorization_path)
    require(not out.exists() and all(out!=Path(p) and out not in Path(p).parents for p in bindings),'output/input collision')
    with tempfile.TemporaryDirectory(prefix='fnv_data_bridge_') as tmp:
        staged=None;proof=None
        if auth['action']=='apply-successor':
            staged=Path(tmp)/'whole-data-bridged.obj';staged.write_bytes(successor_bytes(original,cert));proof=validate_successor(original,staged,cert)
        data.stable(bindings);require(not (root/'build/function_index.json').exists(),'optional index appeared')
        out.mkdir();created=[]
        try:
            if staged:
                target=out/staged.name
                with target.open('xb') as stream:created.append(target);stream.write(staged.read_bytes())
                require(sha(target)==proof['object_sha256'],'published DATA successor differs')
            selection=copy.deepcopy(cert['bounded_partial_link_provider_selection']);selection['applied']=bool(staged)
            report=dict(schema_version=1,kind='bounded-data-provider-bridge-result',certificate=cert,successor=proof,
                protected_inputs=bindings,authorization_sha256=sha(authorization_path),old_new_DATA_mutually_exclusive=True,
                bounded_partial_link_provider_selection=selection,CODE_archive_unchanged=True,small_DATA_unchanged=True,
                actual_final_placement_verified=False,link_or_execution_performed=False,**RUNTIME)
            data.stable(bindings);receipt=out/'bridge.json'
            with receipt.open('x') as stream:created.append(receipt);json.dump(report,stream,separators=(',',':'));stream.write('\n')
            data.stable(bindings);require(not (root/'build/function_index.json').exists(),'optional index appeared during publication');return report
        except Exception:
            for path in created:path.unlink()
            out.rmdir();raise
