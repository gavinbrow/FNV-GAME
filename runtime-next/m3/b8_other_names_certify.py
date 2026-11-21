import json,sys,math,struct,bisect,collections
from pathlib import Path
h=Path(__file__).resolve().parent;sys.path.insert(0,str(h));import gen_m3 as g
p=json.loads((h/'inventory/b8_other_names.json').read_text()); inv={int(x['addr'],16):x for x in json.loads((h/'inventory/dat_globals.json').read_text())['globals']}; sj=json.loads((h.parent/'data-v3/symbolic.json').read_text());fields=sorted({g.SEC[r[0]]['va']+r[1] for r in sj['fields']}|g.ORIG_SET)
labels=sorted(int(v['va']) for v in json.loads((h.parent/'data-v3/out/data_labels.json').read_text())['data_labels'].values())
chunks=[(m['va'],m['va']+m['size']) for m in json.loads((h.parent/'data-v3/out/manifest.json').read_text()) if m['section'] in ('.data','.rdata')]
units=json.loads((Path(g.PROJ)/'fnv_decomp/build/units.json').read_text())['units']; import re
names=sorted({int(m.group(1),16) for u in units for k in u.get('symbols',{}) for m in re.finditer(r'(?:DAT|PTR|UNK|OFF|BYTE|WORD|DWORD)_([0-9a-f]{8})',k)})
sel=json.loads((h/'batch7_selection.json').read_text())['entries']; ranges=[]
for e in sel:
 size=4 if e['tc']=='P' else g.TYPES[e['tc']][1] if e['tc'] in g.TYPES else e['size']; ranges.append((e['va'],e['va']+size))
ranges += [(a,a+n) for a,n in json.loads((h/'inventory/b7_dv1_ranges.json').read_text())];ranges += [(a,a+n) for a,n in json.loads((h/'inventory/b7_produced.json').read_text())]
ranges += [(0xfdf000,0xfdf000+1188),(0x118062c,0x118062c+6688),(0x110147c,0x110147c+0x18)]
types={'char':'D','unsigned char':'E','int':'H','float':'M'}; accepted=[]; rejected=[]
for i in p['intervals']:
 if 'candidate' not in i: continue
 c=i['candidate']; x=i['start']; sz=c['declared_extent_bytes']; end=x+sz; tc=types[c['declared_type']]; reasons=[]; record=inv.get(x,{})
 if set(record.get('declared_types',[])) != {c['declared_type']}: reasons.append('legacy DAT inventory missing or conflicting declared type')
 if record.get('defs'): reasons.append('source definition present')
 if x%sz: reasons.append('natural alignment')
 if not any(a<=x and end<=b for a,b in chunks): reasons.append('not wholly within one data-v3 chunk')
 if any(a<end and x<b for a,b in ranges): reasons.append('overlaps existing placement, production, or rewritten directory')
 if any(x<v<end for v in names): reasons.append('symbol inside extent')
 if any(x<v<end for v in labels): reasons.append('data label inside extent')
 if any(f<end and x<f+4 for f in fields): reasons.append('field or relocation overlaps')
 raw=g.refbytes(x,sz)
 if len(raw)!=sz or not any(raw): reasons.append('unavailable or zero bytes')
 if tc=='M':
  v=struct.unpack('<f',raw)[0]
  if not math.isfinite(v) or (v!=0 and abs(v)<1.1754944e-38): reasons.append('float special or subnormal')
 try:
  built=g.build_entries([{'va':x,'tc':tc}])[0]; initializer=built['init']
 except Exception as e: reasons.append('generator cannot render: '+str(e)); initializer=None
 if reasons: rejected.append({'va':x,'reasons':reasons});continue
 accepted.append({'selection':{'va':x,'tc':tc},'source_name':c['source_name'],'source_linkage':c['linkage'],'source_coff_key':c['coff_symbol'],'declared_type':c['declared_type'],'declared_extent':sz,'reference_hex':raw.hex(),'section':g.sec_of(x),'generator_initializer':initializer,'declarations':i['source_spellings'][0]['declarations'],'validation':{'unit_key_only':True,'captured_declarations_agree':True,'legacy_inventory_type_agrees':True,'no_captured_source_alias_or_definition':True,'natural_alignment':True,'within_one_chunk':True,'no_interior_symbol_or_label':True,'no_intersecting_field_or_relocation':True,'no_overlap_saved_b7_or_unit_or_production_or_listed_rewrites':True},'emission_requirement':'Use distinct M3 name or implement matching extern C linkage; current scalar generator DAT name has C++ linkage.'})
out={'schema_version':1,'scope':'Scalar heads only; saved metadata and lexical source evidence; independently compile and verify before integration. Entries do not assert ownership of interval tails.','selection_ready_for_compile':True,'summary':{'accepted':len(accepted),'bytes':sum(x['declared_extent'] for x in accepted),'rejected_review_candidates':len(rejected)},'entries':accepted,'rejected':rejected}
with (h/'inventory/b8_other_names_accepted.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
print(out['summary']);print(collections.Counter(r for x in rejected for r in x['reasons']))
