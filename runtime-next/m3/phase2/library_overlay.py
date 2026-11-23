"""Fail-closed opt-in library objects for the DV1 overlay; not a default route."""
import hashlib
import json
from pathlib import Path

ALLOWED_KINDS = frozenset(('rdata-other-unit','data-unit','rdata-other','data','float-const','string'))
REWRITTEN = ((0xfdf000,0xfdf4a4),(0x118062c,0x118204c),(0x110147c,0x1101494))

def _digest(data): return hashlib.sha256(data).hexdigest()

def select_library(path, expected_sha256, st, m3skip, accepted, chunks, fields, original_sites, read_ref, libsecs):
    raw=Path(path).read_bytes()
    if len(expected_sha256)!=64 or _digest(raw)!=expected_sha256.lower(): raise ValueError('library selection digest mismatch')
    doc=json.loads(raw.decode('utf-8-sig'))
    if not isinstance(doc,dict): raise ValueError('invalid library selection')
    candidates=doc.get('candidates'); count=doc.get('candidate_count'); total=doc.get('candidate_bytes')
    if type(candidates) is not list or not candidates or type(count) is not int or type(total) is not int or any(not isinstance(x,dict) or type(x.get('size')) is not int for x in candidates): raise ValueError('invalid library selection schema')
    if len(candidates)!=count or sum(x['size'] for x in candidates)!=total: raise ValueError('library selection count mismatch')
    units={}; uid=100000; archive_hashes={}
    for name in ('libcmt.lib','libcpmt.lib'):
        path=libsecs.LIB/name; archive_hashes[name]=_digest(path.read_bytes())
        for _,blob in libsecs.U.read_ar(path): uid+=1; units[uid]=(name,_digest(blob))
    # Fresh placement is the authority: do not trust old annotation metadata.
    by_place={}; archive_units=libsecs.lib_units()
    for key,(address,tier) in st.placed.items():
        s=st.SEC[key]
        for u in s['units']:
            if u>=100000: by_place.setdefault((u,address),[]).append((key,s,tier))
    claims=[(a,a+n) for a,n in m3skip]+[(x['va'],x['va']+x['size']) for x in accepted]+list(REWRITTEN)
    output=[]; allfields=set(fields)|set(original_sites)
    for c in sorted(candidates,key=lambda x:x['va']):
        a=c['va'];n=c['size'];b=a+n;unit=c['unit']; name=c['library']
        if type(a) is not int or type(n) is not int or type(unit) is not int or n<=0 or c['kind'] not in ALLOWED_KINDS or unit<100000: raise ValueError('invalid library entry')
        if archive_hashes.get(name)!=c['archive_sha256'] or units.get(unit)!=(name,c['object_sha256']): raise ValueError('library archive/member mismatch')
        matches=by_place.get((unit,a),[])
        if len(matches)!=1: raise ValueError('library placement missing or ambiguous')
        key,s,tier=matches[0]
        originals=[x for x in archive_units.get(unit,{}).get('secs',[]) if x['k']==c['unit_section_index']]
        if len(originals)!=1: raise ValueError('original library section missing or ambiguous')
        original=originals[0]
        if c.get('split_section') is True:
            start,end=c.get('section_start'),c.get('section_end')
            if type(start) is not int or type(end) is not int or type(c.get('section_size')) is not int or c['section_size'] != len(original['data']) or not 0 <= start < end <= len(original['data']) or end-start != n or original['flags'] & 0x1000:
                raise ValueError('invalid library split extent')
            cuts=sorted({0,len(original['data'])} | {d[1] for d in original['defs'] if 0 < d[1] < len(original['data'])})
            if start not in cuts or end not in cuts or cuts.index(end) != cuts.index(start)+1: raise ValueError('library split is not an adjacent symbol interval')
            pieces=st.PIECES.get((unit,c['unit_section_index']),[])
            if [k for lo,hi,k in pieces if lo==start and hi==end] != [key]: raise ValueError('library split placement identity mismatch')
            if _digest(original['data'])!=c['full_section_sha256'] or original['name']!=s['name'] or original['flags']!=s['flags'] or original['data'][start:end]!=s['data']:
                raise ValueError('library split source section changed')
            if any(r[0]<end and start<r[0]+4 for r in original['relocs']): raise ValueError('library source relocation crosses or enters split')
            defs=[(d[0],d[1]-start,d[2]) for d in original['defs'] if start<=d[1]<end]
            if defs!=s['defs']: raise ValueError('library split definitions changed')
        elif 'split_section' in c:
            raise ValueError('invalid split marker')
        else:
            if st.KEYOF.get((unit,c['unit_section_index'])) != key: raise ValueError('library unit/section placement identity mismatch')
            if original['flags']!=s['flags'] or original['name']!=s['name'] or original['data']!=s['data'] or original['relocs'] or original['defs']!=s['defs']:
                raise ValueError('library section split, deduplicated incompatibly, or changed')
        data=s['data'];alignbits=(s['flags']>>20)&15;alignment=1<<(alignbits-1) if alignbits else 1
        if tier!=c['tier'] or s['kind']!=c['kind'] or s['name']!=c['section_name'] or s['flags']!=c['section_flags']: raise ValueError('library placement metadata changed')
        if len(data)!=n or not any(data) or s['relocs'] or _digest(data)!=c['compiler_bytes_sha256'] or a%alignment or alignment!=c['alignment']: raise ValueError('library section contents/relocations/alignment mismatch')
        if not any(d[0] in c['symbol_offsets'] and c['symbol_offsets'][d[0]]==d[1] for d in s['defs']): raise ValueError('library section symbol/offset missing')
        if read_ref(a,n)!=data or any(a-3<=f<b for f in allfields): raise ValueError('library reference/field mismatch')
        actual=[(name,sec) for x,y,sec,name in chunks if x<=a and b<=y]
        if actual!=[(c['chunk'],c['section'])] or any(x<b and a<y for x,y in claims): raise ValueError('library chunk/overlap mismatch')
        claims.append((a,b));output.append(dict(va=a,size=n,kind=c['kind'],tier=tier,unit=unit,nunits=len(s['units']),section=c['section'],chunk=c['chunk'],names=[d[0] for d in s['defs'] if d[2]==2][:2],ext=False,data=data,relocs=[],sources=['library-opt-in'],library_opt_in=True,k=key))
    return output,dict(selection_sha256=_digest(raw),selected=len(output),bytes=sum(x['size'] for x in output),archive_sha256=archive_hashes)
