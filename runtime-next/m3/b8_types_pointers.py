exec(open('b8_types_certify.py').read().split('accepted=[];')[0])
found=[]
for r in candidates:
 x=r['va']; ds=r['declarations']; codes={z['code'] for z in r['type_observations']}
 if not codes or not all(c.startswith(('PA','PB','QA','QB')) for c in codes) or not ds: continue
 # Simple pointer declarators only; do not infer array extents or pointers-to-arrays.
 if not all(re.fullmatch(r'\s*extern\s+(?:"C"\s+)?(?:const\s+)?[\w:]+(?:\s+const)?\s*\*\s*(?:const\s+)?DAT_[0-9a-f]{8}\s*;\s*',d) for d in ds): continue
 if x%4 or r['interval_size']<4 or overlap(x,x+4) or x not in drel: continue
 if any(x<v<x+4 for v in bnds) or lab_in(x,x+4): continue
 if any(f!=x for f in fld_near(x-3,x+4)): continue
 raw=refbytes(x,4); target=struct.unpack('<I',raw)[0]
 if not validtarget(target): continue
 found.append(dict(va=x,tc='P',ptr=target,sec=r['section'],size=4,align=4,source_declarations=ds,mangled_declarations=r['mangled_declarations'],raw_hex=raw.hex(),target_section=sec_of(target),symbol='M3_%08x'%x,note='Explicit pointer declarations; type alias identity unresolved; no tail claimed.'))
with open('inventory/b8_types_pointer_candidates.json','w') as f: json.dump({'schema_version':1,'entries':found},f,indent=2)
print('count',len(found)); print(json.dumps(found[:3],indent=2))
