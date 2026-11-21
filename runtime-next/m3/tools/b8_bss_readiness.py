import json,re,collections,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent.parent; root=H.parent.parent
D=json.load(open(H/'inventory/dat_globals.json')); inv={int(g['addr'],16):g for g in D['globals']}; bss=json.load(open(H/'inventory/b8_zero_accounting.json'))['bss_units_dat_addresses']; units=json.load(open(root/'fnv_decomp/build/units.json'))['units']
keys=collections.defaultdict(set); r=re.compile(r'(?:DAT|PTR|UNK|OFF|BYTE|WORD|DWORD)_([0-9a-f]{8})')
for u in units:
 for k in u.get('symbols',{}):
  for m in r.finditer(k):keys[int(m.group(1),16)].add(k)
T={'int':('H',4),'unsigned int':('I',4),'unsigned':('I',4),'long':('J',4),'long int':('J',4),'unsigned long':('K',4),'unsigned long int':('K',4),'float':('M',4),'double':('N',8),'short':('F',2),'short int':('F',2),'unsigned short':('G',2),'unsigned short int':('G',2),'char':('D',1),'signed char':('C',1),'unsigned char':('E',1),'bool':('_N',1)}
allstarts=sorted(set(keys)|set(inv)); lo=0x011c3200; hi=0x01271a9c
scan=subprocess.run(['rg','-o','--no-filename',r'(?:_DAT|PTR|UNK|OFF|BYTE|WORD|DWORD)_[0-9a-f]{8}',str(root/'fnv_decomp/src'),str(root/'fnv_decomp/include')],capture_output=True,text=True,check=False)
if scan.returncode not in (0,1): raise RuntimeError('source alias scan failed')
aliases=collections.defaultdict(set)
for name in scan.stdout.splitlines(): aliases[int(name[-8:],16)].add(name)
labels=sorted(int(v['va']) for v in json.load(open(H.parent/'data-v3/out/data_labels.json'))['data_labels'].values())
ready=[]; bounded_arrays=[]; counts=collections.Counter(); rejected=[]
import bisect
for va in bss:
 g=inv.get(va); ks=sorted(keys[va]); reason=None; parsed=[]
 if not g: reason='no_source_inventory'
 elif not g['decls']: reason='no_extern_declaration'
 elif g['defs']: reason='source_definition_present'
 else:
  for d in g['decls']:
   m=re.fullmatch(r'extern\s+(?:(?:"C")\s+)?(const\s+)?([A-Za-z ]+?)\s+(DAT_[0-9a-f]{8})(?:\s*\[\s*(\d+)\s*\])?\s*;',d.strip())
   if not m or m.group(2).strip() not in T or m.group(3)!='DAT_%08x'%va: reason='complex_or_other_declaration'; break
   code,n=T[m.group(2).strip()]; parsed.append((code,n,int(m.group(4)) if m.group(4) else None,bool(m.group(1))))
  if not reason and len(set(parsed))!=1: reason='inconsistent_declarations'
  if not reason and any(chr(34)+'C'+chr(34) in d for d in g['decls']): reason='c_linkage_requires_review'
  if not reason and parsed[0][3]: reason='const_storage_unverified'
  if not reason:
   code,sz,n,const=parsed[0]; extent=sz*(n or 1)
   if n==0:reason='zero_array_bound'
   elif n is not None:
    reason='array_symbol_encoding_unverified'; bounded_arrays.append({'va':va,'element_type':code,'count':n,'size':extent,'source_declarations':g['decls'],'unit_symbol_keys':ks})
   elif any(k!='?DAT_%08x@@3%s%s'%(va,code,'B' if const else 'A') for k in ks): reason='alias_namespace_or_symbol_type'
   elif va in aliases:reason='source_alias'
   elif va%sz:reason='unaligned'
   elif va+extent>hi:reason='outside_virtual_tail'
   elif bisect.bisect_right(allstarts,va)<bisect.bisect_left(allstarts,va+extent):reason='interior_named_address'
   elif bisect.bisect_right(labels,va)<bisect.bisect_left(labels,va+extent):reason='interior_data_label'
   else: ready.append({'va':va,'name':'DAT_%08x'%va,'type_code':code,'size':extent,'alignment':sz,'section':'.bss','source_declarations':g['decls'],'unit_symbol_keys':ks})
 if reason: counts[reason]+=1; rejected.append({'va':va,'reason':reason})
 else: counts['scalar_ready_metadata']+=1
# Check only claims, not inferred source ownership of previous addresses.
ready.sort(key=lambda e:e['va']); assert all(a['va']+a['size']<=b['va'] for a,b in zip(ready,ready[1:]))
out={'schema_version':1,'scope':'Distinct DAT-containing unit symbol addresses in the raw-less .data virtual tail. Strict lexical evidence; namespace/alias uncertainty is deferred. No object definition or build verification.', 'bounds':{'start':lo,'end':hi},'unit_dat_addresses':len(bss),'counts':dict(counts),'scalar_candidates':ready,'scalar_candidate_bytes_virtual_only':sum(x['size'] for x in ready),'fixed_arrays_pending_symbol_encoding':bounded_arrays,'deferred':rejected,'limitations':['Source inventory is lexical, not a full C++ parser.','No byte size or ownership inferred from distance to next symbol.','Definitions require actual source linkage compatibility, placement and object validation.']}
json.dump(out,open(H/'inventory/b8_bss_definition_candidates.json','w'),indent=2)
print(json.dumps({k:v for k,v in out.items() if k not in ('scalar_candidates','fixed_arrays_pending_symbol_encoding','deferred')},indent=2))



