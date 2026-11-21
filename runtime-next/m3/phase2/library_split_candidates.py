"""Read-only candidates for library sections split at compiler symbol boundaries."""
import json,sys,collections,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent;sys.path[:0]=[str(M),str(R/'data-v2')];import gen_m3 as G;import libsecs
j=lambda p:json.load(open(p,encoding='utf-8-sig'));meta=j(R/'data-v3/out/produced_ranges.json');libs=libsecs.lib_units();ext=[x for x in j(H/'phase2_accounting.json')['extents'] if x['class']=='library'];bounds=[(x['va'],x['end']) for x in ext];whole=j(H/'library_candidates.json')['candidates'];archive=M/'out/batch8-promoted-default-verified/evidence';claims=[(x['va'],x['va']+x['size']) for x in j(archive/'m3_manifest.json')['entries']+j(archive/'dv1_pieces.json')['pieces']+whole]+[(0xfdf000,0xfdf4a4),(0x118062c,0x118204c),(0x110147c,0x1101494)];chunks=[(x['va'],x['va']+x['size'],x['file']) for x in j(R/'data-v3/out/manifest.json') if x['section'] in ('.data','.rdata')];sj=j(R/'data-v3/symbolic.json');fields={G.SEC[r[0]]['va']+r[1] for r in sj['fields']}|G.ORIG_SET;tri=j(H/'library_triage.json');members={x['unit']:x for x in tri['member_coverage_nonadditive']};objects={};uid=100000
for lib in ('libcmt.lib','libcpmt.lib'):
 for _,blob in libsecs.U.read_ar(libsecs.LIB/lib):uid+=1;objects[uid]=hashlib.sha256(blob).hexdigest()
counts=collections.Counter();found=[]
for e in meta:
 a=e['va'];size=e['size'];b=a+size
 if e['unit']<100000 or e['tier']=='M' or e['kind'] not in ('rdata-other-unit','data-unit','rdata-other','data','float-const','string') or size<=0 or G.sec_of(a) not in ('.data','.rdata'):continue
 if not any(x<=a and b<=y for x,y in bounds) or any(x<b and a<y for x,y in claims):continue
 chunk=next((f for x,y,f in chunks if x<=a and b<=y),None)
 if not chunk or any(a-3<=f<b for f in fields):continue
 symoffs={s[0]:s[1]-a for s in e['symbols']}; matches=[]
 for s in libs.get(e['unit'],{}).get('secs',[]):
  if s['flags']&0x1000:continue
  for name,offset,_ in s['defs']:
   if name not in symoffs:continue
   start=offset-symoffs[name];end=start+size
   cuts=sorted({0,len(s['data'])}|{d[1] for d in s['defs'] if 0<d[1]<len(s['data'])})
   if start not in cuts or end not in cuts or cuts.index(end)!=cuts.index(start)+1:continue
   if any(r[0]<end and r[0]+4>start for r in s['relocs']):continue
   bits=(s['flags']>>20)&15;align=1<<(bits-1) if bits else 1
   if a%align or s['data'][start:end]!=G.refbytes(a,size) or not any(s['data'][start:end]):continue
   matches.append((s,start,end,align))
 unique={(x[0]['k'],x[1],x[2]):x for x in matches}
 if len(unique)!=1:counts['no_unique_split_match']+=1;continue
 s,start,end,align=next(iter(unique.values()));member=members[e['unit']];found.append({'va':a,'size':size,'section':e['section'],'chunk':chunk,'kind':e['kind'],'tier':e['tier'],'unit':e['unit'],'unit_section_index':s['k'],'section_name':s['name'],'section_start':start,'section_end':end,'section_size':len(s['data']),'section_flags':s['flags'],'alignment':align,'symbol_offsets':symoffs,'library':member['library'],'member':member['member'],'archive_sha256':tri['library_sha256'][member['library']],'object_sha256':objects[e['unit']],'full_section_sha256':hashlib.sha256(s['data']).hexdigest(),'slice_sha256':hashlib.sha256(s['data'][start:end]).hexdigest()})
by=collections.defaultdict(list)
for x in found:by[(x['va'],x['size'])].append(x)
one=[xs[0] for xs in by.values() if len(xs)==1];out=[x for x in one if not any(y is not x and y['va']<x['va']+x['size'] and x['va']<y['va']+y['size'] for y in one)];out.sort(key=lambda x:x['va']);res={'scope':'Candidate slices exactly between adjacent compiler symbol offsets in non-COMDAT library sections; no reloc/fields; not accepted by existing whole-section hook. Requires fresh PIECES/key ownership validation and full integration.','count':len(out),'bytes':sum(x['size'] for x in out),'rejected':dict(counts),'candidates':out};json.dump(res,open(H/'library_split_candidates.json','w'),indent=2);print('split leads',len(out),res['bytes'],'rejected',dict(counts))
