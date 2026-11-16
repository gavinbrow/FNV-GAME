"""Fixed lane03 named-member observation; never emits code or executes inputs.

Metadata is first saved separately. Image observation requires an independent
review binding this implementation and that metadata, then reads only fixed
target extents (<=4096 each, <=256KiB total) through a checked .text mapping.
"""
from pathlib import Path
import argparse
import hashlib
import json
import struct
import tempfile
import re
from crt_provider import archive_member, Coff

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / 'build/rebuild'
PACKET = PRIVATE / 'application-frontier-dispatch-v1/crt-frontier-lane-03.json'
PACKET_SHA = 'adb0668f8389fa904bf7c68904cc7e44ef67f47adb25c040511f5fec1544f801'
INDEX_SHA = '9db04c24f9030ba7bae153e54c01ef9475a4a1a203268bcbc3edc88136565ae9'
REFERENCE_SHA = 'df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7'
LIBS = {'sp1':'bd9700d126d378f31f32736abc0c88cb08a8e0f0914acb6e2c8cbfd1ab99f411',
        'rtm':'bd8fe9fa475deb84014af41870182b447bb969c91661d7012ae8d1b26bb6a86c',
        'vc8':'3bc6c5b90f8507964839fd0264d8565c3b766d01f9efcad336532a11e8f06ac3'}
# Hypotheses only: no source spelling is accepted as original function identity.
CANDIDATES = {
 '0x00ec7c56':['__invalid_parameter_noinfo'],
 '0x00401460':['_memcpy'], '0x00ec5fce':['??_M@YGXPAXIHP6EX0@Z@Z'],
 '0x00ec7ec0':['__strnicmp'], '0x00ec8660':['__chkstk'],
 '0x00ec5ec0':['__alloca_probe_16'], '0x004564f0':['__mbsnicmp'],
 '0x00406cc0':['_floor'], '0x00ec6da0':['_strcmp'],
 '0x00ec9f30':['_cos'], '0x00ec6380':['_strcat'],
 '0x00ec7f1e':['__splitpath_s'], '0x00ec6370':['_strcpy'],
 '0x0046fd30':['__mbsicmp'], '0x00ec9a5e':['_fopen_s'],
 '0x00ec9e10':['_ceil'], '0x00ec6940':['_atan'],
 '0x00ec8d08':['_strtol'], '0x00ecdd16':['__gcvt'],
 '0x00ec6bb5':['_vsprintf_s'], '0x00ec7d50':['_clock'],
 '0x00ec9050':['__CIatan'], '0x00ec9ac0':['_pow'],
 '0x00ecc104':['_fgets'], '0x00ec716d':['_bsearch'],
 '0x00ecbc80':['_tan'], '0x00ecc250':['__alldiv'],
 '0x00ecda70':['_fflush']}
SOURCES=('tools/rebuild/crt_lane03.py','tests/rebuild/test_crt_lane03.py',
         'tools/rebuild/crt_provider.py','tools/compare.py',
         'tools/function_spans.py','tools/build_and_match.py','tools/rebuild/toolchain.py')

def sources():return {s:sha(ROOT/s) for s in SOURCES}

def eligible(symbol,section,definitions):
    return (symbol['value']==0 and symbol['type']==32 and symbol['storage']==2
        and bool(section['flags']&0x20000000) and 0<len(section['data'])<=4096
        and bool(definitions) and all(s['value']==0 and s['type']==32 for s in definitions))

def require(ok, message):
    if not ok: raise ValueError(message)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''): h.update(block)
    return h.hexdigest()

def save(path, obj):
    path=Path(path).resolve()
    require(path.is_relative_to(PRIVATE.resolve()), 'private output only')
    with path.open('x',encoding='utf-8') as f: json.dump(obj,f,indent=2)

def packet():
    require(sha(PACKET)==PACKET_SHA,'packet changed')
    require(sha(PACKET.parent/'index.json')==INDEX_SHA,'index changed')
    p=json.loads(PACKET.read_text())
    require(p['target_count']==48 and p['field_use_count']==658,'scope changed')
    require(set(CANDIDATES)<=set(t['original_target'] for t in p['targets']),'extra candidate')
    return p

def members():
    doctor=PRIVATE/'doctor-all.json'
    require(sha(doctor)=='9b24d10209fe0361a5e6b16b11a072e8e0ebc6505cd4b5e1bd782fe23854f29f','doctor changed')
    roots=json.loads(doctor.read_text())['toolchains']
    result=[]
    for family,expected in LIBS.items():
        lib=Path(roots[family]['root'])/'VC/lib/libcmt.lib'
        require(sha(lib)==expected,'library changed')
        for target,names in CANDIDATES.items():
            for name in names:
                row=dict(target=target,family=family,export=name,archive_sha256=expected)
                try: payload, meta=archive_member(lib,name)
                except ValueError as e:
                    row.update(status='absent-or-ambiguous',reason=str(e)); result.append((row,None)); continue
                with tempfile.TemporaryDirectory(prefix='fnv_crt_lane03_') as tmp:
                    path=Path(tmp)/'member.obj';path.write_bytes(payload); obj=Coff(path)
                symbol=obj.named(name); section=obj.sections[symbol['section']]
                defs=[s for s in obj.symbols.values() if s['section']==symbol['section'] and s['storage']==2]
                row.update(meta,status='named-member',definition=symbol,section_size=len(section['data']),
                    bounded_single_entry_section=eligible(symbol,section,defs),
                    section_sha256=hashlib.sha256(section['data']).hexdigest(),section_exports=defs,
                    relocations=[dict(offset=o,symbol_index=i,kind=k,symbol=obj.symbols[i]) for o,i,k in section['relocs']],
                    member_undefineds=sorted({s['name'] for s in obj.symbols.values() if s['section']==0 and s['storage']==2}))
                result.append((row,section['data']))
        require(sha(lib)==expected,'library changed after read')
    return result

def metadata():
    p=packet(); source_hashes={};rows=[];texts={}
    for t in p['targets']:
        packet_sources={f['source_path']:f['source_sha256'] for f in t['field_uses']}
        for path,expected in packet_sources.items():
            require(sha(ROOT/path)==expected,'own source changed')
            source_hashes[path]=expected
            if path not in texts:texts[path]=(ROOT/path).read_text(encoding='utf-8')
        excerpts=[]
        for f in t['field_uses']:
            symbol=f['coff_relocation']['symbol']
            token=symbol.split('@')[0].lstrip('?') if symbol.startswith('?') else symbol.lstrip('_')
            if token and token.isidentifier():
                for line,text in enumerate(texts[f['source_path']].splitlines(),1):
                    if re.search(r'\b'+re.escape(token)+r'\s*\(',text):
                        excerpts.append((f['source_path'],line,text.strip()))
        rows.append(dict(target=t['original_target'],field_count=len(t['field_uses']),
            actual_V4_unresolved_group_count=len(t['actual_V4_unresolved_groups']),
            physical_spellings=sorted({f['coff_relocation']['symbol'] for f in t['field_uses']}),
            hypotheses=CANDIDATES.get(t['original_target'],[]),
            source_declaration_or_use_excerpts=[dict(source=s,line=n,text=x)
                for s,n,x in sorted(set(excerpts))],
            contract_verified=False,provider_selected=False,runtime_eligible=False))
    return dict(kind='crt-lane03-metadata',packet_sha256=PACKET_SHA,index_sha256=INDEX_SHA,sources=sources(),
        implementation_sha256=sha(__file__),source_hashes=source_hashes,targets=rows,
        members=[r for r,data in members()],image_read=False,provider_selected=False,runtime_eligible=False)

def text_ranges(stream):
    stream.seek(0x3c); pe=struct.unpack('<I',stream.read(4))[0]
    require(pe<4096,'PE header bound');stream.seek(pe)
    require(stream.read(4)==b'PE\0\0','PE signature')
    head=stream.read(20); machine,count,_,_,_,opts,_=struct.unpack('<HHIIIHH',head)
    require(machine==0x14c and 0<count<32 and 96<=opts<=512,'PE shape')
    optional=stream.read(opts);require(struct.unpack_from('<H',optional)[0]==0x10b,'PE32 required')
    base=struct.unpack_from('<I',optional,28)[0]; ranges=[]
    for i in range(count):
        name,vs,rva,size,raw,_,_,_,_,flags=struct.unpack('<8sIIIIIIHHI',stream.read(40))
        if name.rstrip(b'\0')==b'.text':
            require(flags&0x20000000,'text not executable');ranges.append((base+rva,min(vs,size),raw))
    require(ranges==[(0x401000,12440971,1024)],'fixed text geometry differs');return ranges[0]

def compare(data, original, row):
    require(len(data)==len(original)<=4096,'span bound')
    masks=set();relocs=[]
    for r in row['relocations']:
        off=r['offset'];kind=r['kind']
        require(kind in (6,20) and 0<=off<=len(data)-4,'relocation shape')
        require(not masks.intersection(range(off,off+4)),'overlap')
        addend=struct.unpack_from('<i' if kind==20 else '<I',data,off)[0]
        observed=struct.unpack_from('<i' if kind==20 else '<I',original,off)[0]
        destination=(observed-addend+(int(row['target'],16)+off+4 if kind==20 else 0))&0xffffffff
        relocs.append(dict(offset=off,kind=kind,symbol=r['symbol'],addend=addend,
            observed_destination=f'0x{destination:08x}',dependency_identity_verified=False))
        masks.update(range(off,off+4))
    mismatches=sum(data[i]!=original[i] for i in range(len(data)) if i not in masks)
    return dict(nonrelocation_bytes=len(data)-len(masks),nonrelocation_mismatch_count=mismatches,
        all_nonrelocation_bytes_equal=mismatches==0,all_relocation_fields_accounted=True,
        relocation_identity_verified=False,relocations=relocs,ABI_verified=False,
        provider_selected=False,runtime_eligible=False)

def observe(args):
    require(sha(args.metadata)==args.metadata_sha256,'metadata changed')
    meta=json.loads(Path(args.metadata).read_text())
    require(meta['implementation_sha256']==sha(__file__),'implementation changed')
    require(meta['sources']==sources(),'dependencies changed')
    review=json.loads(Path(args.review).read_text())
    require(sha(args.review)==args.review_sha256 and review.get('approved') is True and review.get('reviewer')
        and review.get('implementation_sha256')==sha(__file__)
        and review.get('sources')==sources()
        and review.get('metadata_sha256')==args.metadata_sha256
        and review.get('allow_fixed_text_read') is True,'review gate')
    packet();require(sha(args.reference)==REFERENCE_SHA,'reference mismatch')
    actual=members();require([r for r,d in actual]==meta['members'],'member evidence changed')
    limits={}
    for row,data in actual:
        if data is not None and row['bounded_single_entry_section']:
            limits[row['target']]=max(limits.get(row['target'],0),len(data))
    require(sum(limits.values())<=256*1024,'total bound')
    observations=[]
    with Path(args.reference).open('rb') as stream:
        va,size,raw=text_ranges(stream);buffers={}
        for target,length in limits.items():
            offset=int(target,16)-va
            require(0<=offset and offset+length<=size,'target outside text')
            stream.seek(raw+offset);buffers[target]=stream.read(length)
            require(len(buffers[target])==length,'short read')
        for row,data in actual:
            r=dict(row)
            if data is not None and row['target'] in buffers and row['bounded_single_entry_section']:
                r['comparison']=compare(data,buffers[row['target']][:len(data)],row)
            else:r['comparison']=dict(status='not-compared',reason='absent or nonzero entry or section bound')
            observations.append(r)
    require(sha(args.reference)==REFERENCE_SHA,'reference changed after observation')
    require(sha(args.metadata)==args.metadata_sha256 and sha(__file__)==meta['implementation_sha256'],'inputs changed')
    require(meta['sources']==sources(),'dependencies changed after observation')
    return dict(kind='crt-lane03-fixed-text-observation',metadata_sha256=args.metadata_sha256,
        review_sha256=args.review_sha256,reference_sha256=REFERENCE_SHA,
        read_targets=limits,total_text_bytes=sum(limits.values()),members=observations,
        provider_selected=False,runtime_eligible=False,ABI_verified=False,executed=False)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['metadata','observe'])
    for name in ['out','metadata','metadata-sha256','review','review-sha256','reference']:
        p.add_argument('--'+name,required=name=='out')
    a=p.parse_args();result=metadata() if a.mode=='metadata' else observe(a)
    save(a.out,result);print(json.dumps(dict(status='saved',sha256=sha(a.out))))

if __name__=='__main__':main()
