"""Lane two fixed-address CRT hypotheses; metadata first, reviewed probes only.

No search, compiler, linker, execution, provider adoption or source rewriting.
Complete native single-function sections only; unresolved hypotheses survive.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import struct
import tempfile

import crt_table_boundaries as base
from coff_inventory import Coff
from crt_provider import archive_member
from data_plan import Pe, file_hash

PACKET = '8b006fbb9d5097bc696873c7bd2df80e35318cd012d069617b0df02f53b0389c'
HYPOTHESES = {
 '0x00ec61c0':'_memset', '0x00ec65a6':'_strcpy_s', '0x00ec6bd2':'_strcat_s',
 '0x00ec623a':'_sprintf', '0x00ec7750':'_strstr', '0x00ec8a19':'_strncmp',
 '0x00eca060':'_sin', '0x00ec7ce3':'_memmove_s', '0x00eca6d3':'_atol',
 '0x00ecbf05':'__access', '0x00ecc300':'__allmul', '0x00ec7690':'_strchr',
 '0x00ec7894':'__CxxThrowException@8', '0x00ecc5f8':'_strtok_s',
 '0x00eca590':'_tan', '0x00ec6054':'_sqrt', '0x00ec89e9':'_isalnum',
 '0x00ec8feb':'__strlwr_s', '0x00ec9760':'_atan2', '0x00ecb086':'_fwrite',
 '0x00ec858a':'__stricmp', '0x00ecc071':'__wcsicmp', '0x00ecd31f':'__msize',
}
SOURCES = ('tools/rebuild/crt_lane02.py','tests/rebuild/test_crt_lane02.py',
           'tools/rebuild/crt_table_boundaries.py','tools/rebuild/crt_provider.py',
           'tools/rebuild/coff_inventory.py','tools/rebuild/data_plan.py','tools/compare.py',
           'tools/rebuild/toolchain.py','tools/build_and_match.py','tools/function_spans.py')

def require(ok, message):
    if not ok: raise ValueError(message)

def sources():
    return {n:file_hash(base.ROOT/n) for n in SOURCES}

def section_contract(coff, name):
    definitions = [s for s in coff.symbols.values() if s['name']==name and
                   s['section']>0 and s['type']==32]
    require(len(definitions)==1, 'absent/ambiguous native function definition')
    symbol=definitions[0]; section=coff.sections[symbol['section']]
    peers=[s for s in coff.symbols.values() if s['section']==symbol['section'] and s['type']==32]
    require(symbol['value']==0 and len(peers)==1 and section['flags'] & 0x20000000 and
            0<section['size']<=4096, 'not a complete unique bounded function section')
    raw=struct.unpack_from('<I',coff.data,20+(section['index']-1)*40+20)[0]
    require(raw>0,'function lacks raw section')
    pattern=coff.take(raw,section['size']); relocs=[]
    for offset,index,kind in section['relocs']:
        target=coff.symbols[index]
        require(0<=offset<=len(pattern)-4,'relocation outside span')
        relocs.append(dict(offset=offset,kind=kind,addend=struct.unpack_from('<i',pattern,offset)[0],
            symbol_index=index,symbol=target['name'],symbol_type=target['type'],
            symbol_section=target['section'],symbol_value=target['value'],symbol_storage=target['storage']))
    spans=base.fixed_segments(len(pattern),relocs)
    return dict(symbol=name,section=section['index'],symbol_index=symbol['index'],symbol_value=0,
        size=len(pattern),span_sha256=hashlib.sha256(pattern).hexdigest(),
        fixed_spans=spans,relocations=relocs),pattern

def prepare(doctor_path,packet_path):
    require(file_hash(doctor_path)==base.DOCTOR,'doctor differs')
    require(file_hash(packet_path)==PACKET,'lane packet differs')
    doctor=json.loads(Path(doctor_path).read_text()); packet=json.loads(Path(packet_path).read_text())
    require(packet['lane']==2 and packet['target_count']==48 and packet['field_use_count']==658,'lane scope differs')
    protected=[(Path(doctor_path),base.DOCTOR),(Path(packet_path),PACKET)]
    contracts=[]; patterns={}; outcomes=[]
    for family in ('sp1','rtm','vc8'):
        library=Path(doctor['toolchains'][family]['root'])/'VC/lib/libcmt.lib'
        require(file_hash(library)==base.LIBRARIES[family],'library differs')
        protected.append((library,base.LIBRARIES[family]))
        for target in packet['targets']:
            va=target['original_target']; name=HYPOTHESES.get(va)
            if not name: continue
            try:
                payload,member=archive_member(library,name)
                with tempfile.TemporaryDirectory(prefix='fnv_crt_lane02_') as folder:
                    path=Path(folder)/'member.obj'; path.write_bytes(payload); coff=Coff(path)
                contract,pattern=section_contract(coff,name)
            except ValueError as exc:
                outcomes.append(dict(target=va,family=family,symbol=name,status='unresolved',reason=str(exc)))
                continue
            identity=family+':'+va+':'+name
            contract.update(identity=identity,family=family,target=va,member=member)
            contracts.append(contract); patterns[identity]=pattern
    return dict(kind='fnv-crt-lane02-contracts',schema_version=1,sources=sources(),
        packet_sha256=PACKET,doctor_sha256=base.DOCTOR,libraries=base.LIBRARIES,
        hypotheses=HYPOTHESES,targets=packet['targets'],contracts=contracts,unresolved=outcomes,
        text_geometry=base.TEXT,max_per_target=4096,max_total=262144,
        hypothesis_only=True,not_all_frontier_targets_are_actual_LINK_unresolved=True,
        provider_selected=False,runtime_eligible=False),patterns,protected

def run(args):
    destination=Path(args.out).resolve(); allowed=(base.ROOT/'build/rebuild').resolve()
    require(destination.is_relative_to(allowed) and not destination.exists(),'output must be new private rebuild file')
    document,patterns,protected=prepare(args.doctor,args.packet)
    if args.mode=='probes':
        require(file_hash(args.contracts)==args.contracts_sha256,'contracts identity differs')
        require(json.loads(Path(args.contracts).read_text())==json.loads(json.dumps(document)),
                'contracts changed')
        require(file_hash(args.review)==args.review_sha256,'review identity differs')
        review=json.loads(Path(args.review).read_text())
        require(review.get('kind')=='fnv-crt-lane02-source-review' and review.get('status')=='approved' and
            review.get('reviewer') and review.get('sources')==sources() and
            review.get('contracts_sha256')==args.contracts_sha256 and review.get('allow_reference_probe') is True and
            review.get('allow_execute') is False and review.get('reference_sha256')==base.REFERENCE,
            'review does not authorize exact fixed probes')
        require(file_hash(args.reference)==base.REFERENCE,'reference differs')
        protected += [(Path(args.contracts),args.contracts_sha256),(Path(args.review),args.review_sha256),
                      (Path(args.reference),base.REFERENCE)]
        pe=Pe(args.reference); observations=[]; requested=0
        try:
            require(pe.base==0x400000 and [s for s in pe.sections if s['name']=='.text']==[base.TEXT],'text geometry differs')
            highlow=set(pe.relocations())
            spans={}
            for c in document['contracts']:
                spans[c['target']]=max(spans.get(c['target'],0),c['size'])
            originals={}
            for target,size in spans.items():
                va=int(target,0); requested+=size
                require(size<=4096 and requested<=262144 and pe.base+base.TEXT['rva']<=va<=pe.base+base.TEXT['rva']+base.TEXT['extent']-size,'span outside budget/text')
                originals[target]=pe.read_rva(va-pe.base,size,allow_code=True)
            for c in document['contracts']:
                va=int(c['target'],0); size=c['size']
                actual=originals[c['target']][:size]; pattern=patterns[c['identity']]
                equal=all(actual[a:b]==pattern[a:b] for a,b in c['fixed_spans'])
                observations.append(dict(identity=c['identity'],target=c['target'],size=size,
                    full_nonrelocation_span_equal=equal,
                    relocations=base.observe_relocations(c,va,actual,va,pe,highlow),
                    original_identity_proven=False,complete_relocation_identity_verified=False,
                    provider_selected=False))
        finally: pe.close()
        document=dict(kind='fnv-crt-lane02-fixed-observations',schema_version=1,contracts=document,
            observations=observations,executable_bytes_requested=requested,reference_sha256=base.REFERENCE,
            review_sha256=args.review_sha256,provider_selected=False,runtime_eligible=False,executed=False)
    for path,digest in protected: require(file_hash(path)==digest,'input changed')
    bundle=document if args.mode=='contracts' else document['contracts']
    require(bundle['sources']==sources(),'implementation changed')
    with destination.open('x',encoding='utf-8') as stream: json.dump(document,stream,indent=2)
    return dict(output_sha256=file_hash(destination),contracts=len(patterns),observations=len(document.get('observations',[])))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',choices=('contracts','probes'),required=True)
    for name in ('doctor','packet','out'): parser.add_argument('--'+name,required=True)
    for name in ('contracts','contracts_sha256','review','review_sha256','reference'):
        parser.add_argument('--'+name.replace('_','-'))
    print(json.dumps(run(parser.parse_args())))

if __name__=='__main__': main()
