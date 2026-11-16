"""Reviewed finite lane04 CRT observations, with no search or code execution.

Only exact whole native sections at packet target minus named export value may
be read. Multi-export sections retain every peer and relocation. A match is
candidate evidence, never a runtime provider or full dependency identity proof.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import tempfile

import crt_frontier_lane01 as native
import crt_frontier_lane04 as lane
import crt_table_boundaries as base
from crt_boundary_helpers import field_mask
from crt_provider import archive_member
from data_plan import Pe, file_hash
from compare import Coff

METADATA='56b6bd25ec8615dcd9cb4432be7c7133787cd4c58dc39a3362b4d7c2a8833611'
REQUEST='707d947f77147951517fcaa91b68e5d4fe712727ed163b2fc9d7733b6f4bb018'
SOURCES=('tools/rebuild/crt_lane04_observer.py','tests/rebuild/test_crt_lane04_observer.py',
         'tools/rebuild/crt_frontier_lane04.py','tools/rebuild/crt_frontier_lane01.py',
         'tools/rebuild/crt_table_boundaries.py','tools/rebuild/crt_boundary_helpers.py',
         'tools/rebuild/crt_provider.py','tools/rebuild/data_plan.py','tools/compare.py',
         'tools/rebuild/toolchain.py','tools/build_and_match.py','tools/function_spans.py',
         'tools/rebuild/coff_inventory.py')

def require(ok,message):
    if not ok: raise ValueError(message)

def sources(): return {p:file_hash(base.ROOT/p) for p in SOURCES}

def spans(request):
    """Preflight the complete finite request before the first payload read."""
    result={}; total=0
    for row in request['requests']:
        require(row['target'] not in result,'duplicate target')
        target=int(row['target'],0); starts=[]; ends=[]
        require(row['alternatives'],'empty target alternatives')
        for a in row['alternatives']:
            start=int(a['reference_start'],0); size=a['reference_size']
            require(start==target-a['target_symbol_value'] and 0<size<=4096,
                    'not exact whole-section placement')
            require(base.TEXT['rva']+0x400000<=start and
                    start+size<=0x400000+base.TEXT['rva']+base.TEXT['extent'],
                    'outside fixed text geometry')
            starts.append(start); ends.append(start+size)
        start=min(starts); size=max(ends)-start
        require(size<=4096,'coalesced target exceeds byte cap')
        total+=size; require(total<=262144,'aggregate byte cap')
        result[row['target']]=(start,size)
    require(len(result)==29 and total==6222,'fixed lane request scope differs')
    return result,total

def converted_relocations(member):
    return [dict(offset=r['offset'],kind=r['kind'],addend=r['addend'],
                 symbol_index=r['symbol_index'],symbol=r['name'],symbol_type=r['type'],
                 symbol_section=r['section'],symbol_value=r['value'],symbol_storage=r['storage'])
            for r in member['all_relocations']]

def compare_section(pattern,actual,relocations):
    require(len(pattern)==len(actual),'incomplete span')
    mask=field_mask(len(pattern),relocations)
    fixed=[i for i in range(len(pattern)) if i not in mask]
    return all(pattern[i]==actual[i] for i in fixed),len(fixed)

def prepare():
    folder=base.ROOT/'build/rebuild'
    paths={folder/'crt-frontier-lane04-metadata-v1.json':METADATA,
           folder/'crt-frontier-lane04-observation-request-v1.json':REQUEST,
           folder/'doctor-all.json':base.DOCTOR,
           folder/'application-frontier-dispatch-v1/index.json':lane.INDEX,
           folder/'application-frontier-dispatch-v1/crt-frontier-lane-04.json':lane.PACKET}
    for p,h in paths.items(): require(file_hash(p)==h,'metadata pin differs')
    metadata=json.loads((folder/'crt-frontier-lane04-metadata-v1.json').read_text())
    request=json.loads((folder/'crt-frontier-lane04-observation-request-v1.json').read_text())
    doctor=json.loads((folder/'doctor-all.json').read_text())
    require(request['input_sha256']==METADATA,'request input differs')
    bounds,total=spans(request); byva={t['original_target']:t for t in metadata['targets']}
    contracts=[]; patterns={}
    for row in request['requests']:
        target=byva[row['target']]
        for a in row['alternatives']:
            key=a['library_export']; member=target['members'][key]; family,name=key.split(':',1)
            require(a['all_relocations']==member['all_relocations'] and
                    a['section_function_symbols']==member['section_function_symbols'] and
                    a['reference_size']==member['complete_section_size'] and
                    a['target_symbol_value']==member['value'] and
                    a['member_sha256']==member['identity']['member_sha256'] and
                    a['full_native_section_sha256']==member['complete_section_sha256'],
                    'request/member contract differs')
            lib=Path(doctor['toolchains'][family]['root'])/'VC/lib/libcmt.lib'
            if lib not in paths:
                paths[lib]=base.LIBRARIES[family]
                require(file_hash(lib)==paths[lib],'library differs')
            require(native.metadata(lib,name)==member,'native metadata differs')
            payload,identity=archive_member(lib,name)
            with tempfile.TemporaryDirectory(prefix='fnv_lane04_pattern_') as tmp:
                p=Path(tmp)/'member.obj'; p.write_bytes(payload); coff=Coff(p)
            pattern=coff.sections[member['section']]['data']
            require(hashlib.sha256(pattern).hexdigest()==a['full_native_section_sha256'],'pattern differs')
            identity=row['target']+':'+key
            patterns[identity]=pattern
            contracts.append(dict(identity=identity,target=row['target'],family=family,symbol=name,
                section=member['section'],symbol_value=member['value'],
                start=int(a['reference_start'],0),size=a['reference_size'],
                relocations=converted_relocations(member),section_function_symbols=member['section_function_symbols'],
                native_member=member['identity']))
    return contracts,patterns,paths,bounds,total

def review_gate(review,bundle):
    require(review.get('kind')=='crt-lane04-observer-source-review' and
        review.get('status')=='approved' and review.get('reviewer') and
        review.get('sources')==bundle and review.get('metadata_sha256')==METADATA and
        review.get('request_sha256')==REQUEST and review.get('reference_sha256')==base.REFERENCE and
        review.get('allow_reference_probe') is True and review.get('allow_execute') is False,
        'review does not authorize this fixed observer')

def run(args):
    destination=Path(args.out).resolve(); allowed=(base.ROOT/'build/rebuild').resolve()
    require(destination.is_relative_to(allowed) and not destination.exists(),'new private output required')
    bundle=sources(); require(file_hash(args.review)==args.review_sha256,'review identity differs')
    review_gate(json.loads(Path(args.review).read_text()),bundle)
    contracts,patterns,protected,bounds,total=prepare()
    require(file_hash(args.reference)==base.REFERENCE,'reference differs')
    protected.update({Path(args.review):args.review_sha256,Path(args.reference):base.REFERENCE})
    pe=Pe(args.reference); observations=[]
    try:
        require(pe.base==0x400000 and [s for s in pe.sections if s['name']=='.text']==[base.TEXT],
                'reference text geometry differs')
        highlow=set(pe.relocations()); originals={}
        for target,(start,size) in bounds.items():
            originals[target]=pe.read_rva(start-pe.base,size,allow_code=True)
        for c in contracts:
            start=c['start']; bstart,_=bounds[c['target']]
            actual=originals[c['target']][start-bstart:start-bstart+c['size']]
            equal,count=compare_section(patterns[c['identity']],actual,c['relocations'])
            relocations=base.observe_relocations(c,start,actual,start,pe,highlow)
            for r in relocations:
                same=r['symbol_section']==c['section']
                r['native_same_section']=same
                r['expected_same_section_symbol_va']=start+r['symbol_value'] if same else None
                r['same_section_target_equal']=(r['original_symbol_base_candidate']==start+r['symbol_value']) if same else None
            observations.append(dict(identity=c['identity'],target=c['target'],section_start=start,
                size=c['size'],full_nonrelocation_span_equal=equal,nonrelocation_bytes=count,
                original_span_sha256=hashlib.sha256(actual).hexdigest(),relocations=relocations,
                original_identity_proven=False,complete_relocation_identity_verified=False,provider_selected=False))
    finally: pe.close()
    for p,h in protected.items(): require(file_hash(p)==h,'protected input changed')
    require(sources()==bundle,'implementation changed')
    report=dict(kind='crt-lane04-fixed-observations',schema_version=1,sources=bundle,
        metadata_sha256=METADATA,request_sha256=REQUEST,reference_sha256=base.REFERENCE,
        review_sha256=args.review_sha256,contracts=contracts,observations=observations,
        coalesced_read_spans={k:dict(start=v[0],size=v[1]) for k,v in bounds.items()},
        executable_bytes_requested=total,targets=len(bounds),executed=False,
        provider_selected=False,runtime_eligible=False,ABI_approved=False)
    with destination.open('x',encoding='utf-8') as f: json.dump(report,f,indent=2)
    return dict(output_sha256=file_hash(destination),targets=len(bounds),bytes_requested=total,
                matching_sections=sum(o['full_nonrelocation_span_equal'] for o in observations))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('review','review-sha256','reference','out'):parser.add_argument('--'+name,required=True)
    print(json.dumps(run(parser.parse_args())))
