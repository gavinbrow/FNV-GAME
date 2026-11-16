"""Lane01 finite fixed-target adapter over the reviewed CRT observation helpers.

No candidate search, native execution, source rewriting, or provider adoption.
The normal entrypoint requires a hash-bound technical source review and root's
separate operation delegation. Read-only original observations stay private.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import tempfile

import crt_lane04_observer as shared

ROOT = shared.base.ROOT
METADATA = 'd74c0d4b4e9c199da7b335a846aaf6fe6a8fabfb2863acaedcab71ebc593d771'
REQUEST = '1b00e3bd36e3c34a00eae81edd3430167bcbae4110bbf6518ac287b39c82062f'
SOURCES = tuple(sorted(set(shared.SOURCES + (
    'tools/rebuild/crt_lane01_observer.py',
    'tests/rebuild/test_crt_lane01_observer.py'))))

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sources():
    return {p:shared.file_hash(ROOT/p) for p in SOURCES}

def bounds_for(request):
    bounds = {}
    for row in request['requests']:
        require(row['target'] not in bounds and row['alternatives'], 'duplicate/empty target')
        target = int(row['target'], 0)
        starts, ends = [], []
        for alternative in row['alternatives']:
            start = int(alternative['reference_start'], 0)
            size = alternative['reference_size']
            require(start == target-alternative['target_symbol_value'] and
                    0 < size <= 4096, 'not exact whole-section placement')
            require(0x400000+shared.base.TEXT['rva'] <= start and
                start+size <= 0x400000+shared.base.TEXT['rva']+shared.base.TEXT['extent'],
                'outside checked reference text')
            starts.append(start); ends.append(start+size)
        start = min(starts); size = max(ends)-start
        require(size <= 4096, 'coalesced per-target cap exceeded')
        bounds[row['target']] = (start, size)
    total = sum(size for start,size in bounds.values())
    require(total <= 262144, 'aggregate cap exceeded')
    return bounds, total

def prepare():
    folder = ROOT/'build/rebuild'
    pins = {folder/'crt-frontier-lane01-metadata-v2.json':METADATA,
            folder/'crt-frontier-lane01-observation-request-v2.json':REQUEST,
            folder/'doctor-all.json':shared.base.DOCTOR,
            folder/'application-frontier-dispatch-v1/crt-frontier-lane-01.json':shared.native.PACKET,
            folder/'application-frontier-dispatch-v1/index.json':shared.lane.INDEX}
    for p,h in pins.items(): require(shared.file_hash(p)==h, 'input pin differs')
    metadata = json.loads((folder/'crt-frontier-lane01-metadata-v2.json').read_text())
    request = json.loads((folder/'crt-frontier-lane01-observation-request-v2.json').read_text())
    doctor = json.loads((folder/'doctor-all.json').read_text())
    require(request['input_sha256']==METADATA, 'request input differs')
    bounds,total = bounds_for(request)
    require(len(bounds)==25 and total==4233, 'finite lane scope differs')
    byva = {t['original_target']:t for t in metadata['targets']}
    contracts,patterns = [],{}
    for target in metadata['targets']:
        for src in target['source_inputs']:
            p=ROOT/src['path']; pins[p]=src['sha256']
            require(shared.file_hash(p)==pins[p], 'source pin differs')
    for row in request['requests']:
        for a in row['alternatives']:
            key = a['library_export']; member = byva[row['target']]['members'][key]
            family,name = key.split(':',1)
            require(a['reference_size']==member['complete_section_size'] and
                a['target_symbol_value']==member['value'] and a['section']==member['section'] and
                a['all_relocations']==member['all_relocations'] and
                a['section_function_symbols']==member['section_function_symbols'] and
                a['member_sha256']==member['identity']['member_sha256'] and
                a['full_native_section_sha256']==member['complete_section_sha256'],
                'request/native metadata differs')
            library=Path(doctor['toolchains'][family]['root'])/'VC/lib/libcmt.lib'
            if library not in pins:
                pins[library]=shared.base.LIBRARIES[family]
                require(shared.file_hash(library)==pins[library], 'library pin differs')
            require(shared.native.metadata(library,name)==member, 'current native metadata differs')
            payload,identity=shared.archive_member(library,name)
            require(identity==member['identity'], 'archive member identity differs')
            with tempfile.TemporaryDirectory(prefix='fnv_lane01_pattern_') as temporary:
                p=Path(temporary)/'member.obj'; p.write_bytes(payload); coff=shared.Coff(p)
            pattern=coff.sections[member['section']]['data']
            require(hashlib.sha256(pattern).hexdigest()==a['full_native_section_sha256'], 'pattern differs')
            identity=row['target']+':'+key; patterns[identity]=pattern
            contracts.append(dict(identity=identity,target=row['target'],symbol=name,family=family,
                section=member['section'],symbol_value=member['value'],
                start=int(a['reference_start'],0),size=a['reference_size'],
                relocations=shared.converted_relocations(member),
                section_function_symbols=member['section_function_symbols'],native_member=member['identity']))
    return contracts,patterns,pins,bounds,total

def review_gate(review,bundle):
    require(review.get('kind')=='crt-lane01-observer-source-review' and
        review.get('status')=='approved' and review.get('reviewer') and
        review.get('sources')==bundle and review.get('metadata_sha256')==METADATA and
        review.get('request_sha256')==REQUEST and
        review.get('reference_sha256')==shared.base.REFERENCE and
        review.get('allow_reference_probe') is True and review.get('allow_execute') is False,
        'review does not cover exact lane01 observer')

def run(args):
    output=Path(args.out).resolve()
    require(output.is_relative_to((ROOT/'build/rebuild').resolve()) and not output.exists(),
        'exclusive private output required')
    bundle=sources(); require(shared.file_hash(args.review)==args.review_sha256,'review differs')
    review_gate(json.loads(Path(args.review).read_text()),bundle)
    contracts,patterns,pins,bounds,total=prepare()
    require(shared.file_hash(args.reference)==shared.base.REFERENCE,'reference differs')
    pins.update({Path(args.review):args.review_sha256,Path(args.reference):shared.base.REFERENCE})
    pe=shared.Pe(args.reference); observations=[]
    try:
        require(pe.base==0x400000 and [s for s in pe.sections if s['name']=='.text']==[shared.base.TEXT],
                'checked reference text geometry differs')
        highlow=set(pe.relocations())
        original={t:pe.read_rva(start-pe.base,size,allow_code=True) for t,(start,size) in bounds.items()}
        for c in contracts:
            start=c['start']; bstart,_=bounds[c['target']]
            actual=original[c['target']][start-bstart:start-bstart+c['size']]
            equal,count=shared.compare_section(patterns[c['identity']],actual,c['relocations'])
            relocations=shared.base.observe_relocations(c,start,actual,start,pe,highlow)
            for field in relocations:
                same=field['symbol_section']==c['section']
                field['native_same_section']=same
                field['expected_same_section_symbol_va']=start+field['symbol_value'] if same else None
                field['same_section_target_equal']=(field['original_symbol_base_candidate']==start+field['symbol_value']) if same else None
            observations.append(dict(identity=c['identity'],target=c['target'],section_start=start,
                size=c['size'],full_nonrelocation_span_equal=equal,nonrelocation_bytes=count,
                original_span_sha256=hashlib.sha256(actual).hexdigest(),relocations=relocations,
                original_identity_proven=False,complete_relocation_identity_verified=False,provider_selected=False))
    finally:
        pe.close()
    for p,h in pins.items(): require(shared.file_hash(p)==h,'protected input changed')
    require(sources()==bundle,'source implementation changed')
    report=dict(kind='crt-lane01-fixed-observations',schema_version=1,sources=bundle,
        metadata_sha256=METADATA,request_sha256=REQUEST,reference_sha256=shared.base.REFERENCE,
        review_sha256=args.review_sha256,contracts=contracts,observations=observations,
        coalesced_read_spans={t:dict(start=v[0],size=v[1]) for t,v in bounds.items()},
        executable_bytes_requested=total,targets=len(bounds),executed=False,
        provider_selected=False,runtime_eligible=False,ABI_approved=False)
    with output.open('x',encoding='utf-8') as stream:json.dump(report,stream,indent=2)
    return dict(output_sha256=shared.file_hash(output),targets=len(bounds),bytes_requested=total,
        matching_sections=sum(o['full_nonrelocation_span_equal'] for o in observations))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('review','review-sha256','reference','out'):parser.add_argument('--'+name,required=True)
    print(json.dumps(run(parser.parse_args())))
