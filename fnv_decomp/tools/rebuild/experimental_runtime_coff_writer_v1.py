"""Experimental i386 COFF selection writer for backed/unbacked sections and weak edges.

No namespace changes, native operations or publication. Caller must validate roots.
"""
import struct
import coff_code_archive as coff


def serialize(raw, section_indices, symbol_indices):
    obj=coff.parse(raw); secs=obj['sections']; syms=obj['symbols']
    ks=list(section_indices); ky=list(symbol_indices)
    coff.require(ks==sorted(set(ks)) and ky==sorted(set(ky)) and set(ks)<=secs.keys() and set(ky)<=syms.keys(), 'invalid selection')
    sm={old:i+1 for i,old in enumerate(ks)}; ym={}; am={}; cursor=0
    for old in ky:
        ym[old]=cursor
        for j in range(syms[old]['aux_count']): am[old+j+1]=cursor+j+1
        cursor+=1+syms[old]['aux_count']
    strings=bytearray(4)
    def name(s,section=False):
        rawname=s.encode('ascii')
        if len(rawname)<=8: return rawname.ljust(8,b'\0')
        pos=len(strings);strings.extend(rawname+b'\0')
        if section:
            short=('/'+str(pos)).encode('ascii');coff.require(len(short)<=8,'section name offset overflow');return short.ljust(8,b'\0')
        return struct.pack('<II',0,pos)
    names={i:name(secs[i]['name'],True) for i in ks}; records=bytearray()
    for old in ky:
        s=syms[old]; sec=s['section']; storage=s['storage']; aux=s['aux']
        coff.require(storage in (2,3,105) and (sec<=0 or sec in sm),'unsupported symbol or omitted definition')
        metadata=storage==3 and s['type']==0 and not s['aux_count'] and (s['name']=='@comp.id' or (s['name']=='@feat.00' and s['value']==1))
        coff.require(not (sec==0 and s['value']) and (sec!=-1 or metadata),'common or absolute record unsupported')
        if storage==105:
            coff.require(sec==0 and s['value']==0 and s['type'] in (0,32) and s['aux_count']==1,'weak record unsupported')
            fallback,search=struct.unpack_from('<II',aux)
            coff.require(fallback in ym and search==2 and not any(aux[8:]),'weak fallback unsupported')
            aux=struct.pack('<II',ym[fallback],search)+aux[8:]
        elif aux:
            coff.require(s['aux_count']==1 and storage==3 and s['type']==0 and s['value']==0 and sec in sm and s['name']==secs[sec]['name'],'section auxiliary unsupported')
            length,nr,nl,checksum,assoc,selection,reserved,high=struct.unpack('<IHHIhBBH',aux)
            coff.require(length==secs[sec]['size'] and nr==len(secs[sec]['relocs']) and not nl and not reserved and not high and selection in range(8),'section auxiliary malformed')
            if selection==5:
                coff.require(assoc in sm,'association escapes selection');aux=struct.pack('<IHHIhBBH',length,nr,nl,checksum,sm[assoc],selection,0,0)
            else: coff.require(not assoc,'hidden association')
        records+=struct.pack('<8sIhHBB',name(s['name']),s['value'],sm.get(sec,sec),s['type'],storage,s['aux_count'])+aux
    body=bytearray();headers=bytearray();pos=20+40*len(ks)
    for old in ks:
        s=secs[old];payload=s['payload'];size=s['size']
        if len(payload)!=size:
            coff.require(not payload and bool(s['flags']&0x80) and not s['relocs'],'unsupported unbacked section')
            raw_pointer=0
        else:
            raw_pointer=pos if payload else 0;body+=payload;pos+=len(payload)
        reloc_pointer=pos if s['relocs'] else 0
        for offset,target,kind in s['relocs']:
            coff.require(target in ym and kind in (6,11,20),'unsupported relocation')
            body+=struct.pack('<IIH',offset,ym[target],kind);pos+=10
        headers+=struct.pack('<8sIIIIIIHHI',names[old],0,0,size,raw_pointer,reloc_pointer,0,len(s['relocs']),0,s['flags'])
    struct.pack_into('<I',strings,0,len(strings))
    output=struct.pack('<HHIIIHH',0x14c,len(ks),0,pos,cursor,0,0)+headers+body+records+strings
    receipt=dict(section_map=sm,symbol_map=ym,auxiliary_map=am)
    verify(raw,output,receipt)
    return output,receipt


def verify(raw, output, maps):
    before,after=coff.parse(raw),coff.parse(output);sm=maps['section_map'];ym=maps['symbol_map'];am=maps['auxiliary_map']
    coff.require(len(set(sm.values()))==len(sm) and len(set(ym.values()))==len(ym) and len(set(am.values()))==len(am),'noninjective mapping')
    coff.require(set(after['sections'])==set(sm.values()) and set(after['symbols'])==set(ym.values()),'incomplete mapping')
    expected_aux={old+j:new+j for old,new in ym.items() for j in range(1,before['symbols'][old]['aux_count']+1)}
    coff.require(am==expected_aux and set(ym.values())|set(am.values())==set(range(after['symbol_count'])),'slot mapping differs')
    for old,new in sm.items():
        a,b=before['sections'][old],after['sections'][new]
        coff.require(all(a[k]==b[k] for k in ('name','size','flags','payload')),'section identity differs')
        coff.require([(off,ym[t],kind) for off,t,kind in a['relocs']]==b['relocs'],'relocation identity differs')
    for old,new in ym.items():
        s=dict(before['symbols'][old]); original_sec=s['section'];s['section']=sm.get(original_sec,original_sec)
        if s['storage']==105:
            fallback,search=struct.unpack_from('<II',s['aux']);s['aux']=struct.pack('<II',ym[fallback],search)+s['aux'][8:]
        elif s['aux_count']:
            aux=bytearray(s['aux']);length,nr,nl,checksum,assoc,selection,reserved,high=struct.unpack('<IHHIhBBH',aux)
            if selection==5:struct.pack_into('<h',aux,12,sm[assoc])
            s['aux']=bytes(aux)
        coff.require(s==after['symbols'][new],'symbol identity differs')
