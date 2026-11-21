import json,sys,collections,hashlib,bisect
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent;sys.path.insert(0,str(M));sys.path.insert(0,str(R/'data-v2'));import gen_m3 as G;import libsecs
j=lambda p:json.load(open(p,encoding='utf-8-sig'))
meta=j(R/'data-v3/out/produced_ranges.json'); libs=libsecs.lib_units(); ext=[x for x in j(H/'phase2_accounting.json')['extents'] if x['class']=='library'];lohi=sorted((x['va'],x['end']) for x in ext)
triage=j(H/'library_triage.json'); members={x['unit']:x for x in triage['member_coverage_nonadditive']};object_hashes={};uid=100000
for library in ('libcmt.lib','libcpmt.lib'):
 for _,blob in libsecs.U.read_ar(libsecs.LIB/library):
  uid+=1;object_hashes[uid]=hashlib.sha256(blob).hexdigest()
manifest=j(M/'out/batch8-promoted-default-verified/evidence/m3_manifest.json')['entries'];pieces=j(M/'out/batch8-promoted-default-verified/evidence/dv1_pieces.json')['pieces'];claims=[(e['va'],e['va']+e['size']) for e in manifest+pieces];rewrite=[(0xfdf000,0xfdf4a4),(0x118062c,0x118204c),(0x110147c,0x1101494)];claims+=rewrite
chunks=[(c['va'],c['va']+c['size'],c['file']) for c in j(R/'data-v3/out/manifest.json') if c['section'] in ('.data','.rdata')];sj=j(R/'data-v3/symbolic.json');fields=sorted({G.SEC[r[0]]['va']+r[1] for r in sj['fields']}|G.ORIG_SET);counts=collections.Counter();found=[]
for e in meta:
 if e['unit']<100000 or e['tier']=='M' or e['kind'] not in ('rdata-other-unit','data-unit','rdata-other','data','float-const','string'):continue
 a=e['va'];b=a+e['size'];size=e['size'];
 if size==0 or G.sec_of(a) not in ('.data','.rdata') or not any(x<=a and b<=y for x,y in lohi):counts['outside_library_only_extent']+=1;continue
 if any(x<b and a<y for x,y in claims):counts['claimed']+=1;continue
 chunk=next((name for x,y,name in chunks if x<=a and b<=y),None)
 if not chunk:counts['chunk']+=1;continue
 if any(a-3<=f<b for f in fields):counts['field']+=1;continue
 lib=libs.get(e['unit']);
 if not lib:counts['missing_unit']+=1;continue
 syms={s[0]:s[1]-a for s in e['symbols']}; possible=[]
 for s in lib['secs']:
  if len(s['data'])!=size or s['relocs'] or not any(z[0] in syms and syms[z[0]]==z[1] for z in s['defs']):continue
  if s['data']==G.refbytes(a,size):possible.append(s)
 if len(possible)!=1:counts['not_unique_exact_section']+=1;continue
 s=possible[0];bits=(s['flags']>>20)&15;alignment=1<<(bits-1) if bits else 1
 if a%alignment:counts['alignment']+=1;continue
 if not any(s['data']):counts['all_zero']+=1;continue
 member=members[e['unit']]
 found.append({'va':a,'size':size,'section':e['section'],'chunk':chunk,'kind':e['kind'],'tier':e['tier'],'unit':e['unit'],'library':member['library'],'archive_sha256':triage['library_sha256'][member['library']],'member':member['member'],'object_sha256':object_hashes[e['unit']],'unit_section_index':s['k'],'section_flags':s['flags'],'alignment':alignment,'symbol_offsets':syms,'section_name':s['name'],'compiler_bytes_sha256':hashlib.sha256(s['data']).hexdigest(),'evidence':'existing compiler archive section exactly equals reference; no reloc/field; final archived claim and recorded rewrite excluded','limitations':'library placement opt-in, final integration validation and source ownership still require review'})
# A candidate cannot be proposed twice or overlap another candidate; retain only unique address/size identity.
by=collections.defaultdict(list)
for x in found:by[(x['va'],x['size'])].append(x)
unique=[xs[0] for xs in by.values() if len(xs)==1];unique.sort(key=lambda x:x['va']);safe=[]
for i,x in enumerate(unique):
 if any(y is not x and y['va']<x['va']+x['size'] and x['va']<y['va']+y['size'] for y in unique):counts['candidate_overlap']+=1
 else:safe.append(x)
out={'scope':'Non-EH/non-CRT/non-class library section matches; metadata and hashes only, not ready to splice.','candidate_count':len(safe),'candidate_bytes':sum(x['size'] for x in safe),'rejected':dict(counts),'candidates':safe}
json.dump(out,open(H/'library_candidates.json','w'),indent=2);print('candidates',len(safe),'bytes',out['candidate_bytes'],'rejects',dict(counts));print([(hex(x['va']),x['size'],x['kind']) for x in safe[:8]])
