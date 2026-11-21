import os,sys,json,re,bisect,collections
from pathlib import Path
here=Path(__file__).resolve().parent.parent
os.chdir(here); sys.argv=['b7_select.py']; __file__=str(here/'b7_select.py')
source=(here/'b7_select.py').read_text(); exec(compile(source[:source.index('entries = [];')],__file__,'exec'),globals())
b7=json.load(open(here/'batch7_selection.json'))['entries']
def esize(e): return 4 if e['tc']=='P' else TYPES[e['tc']][1] if e['tc'] in TYPES else e['size']
claims=sorted([(e['va'],e['va']+esize(e)) for e in b7]+dv1+prod+REWRITTEN)
keys=collections.defaultdict(set)
for u in units:
 for k in u.get('symbols',{}):
  for m in ADDR_ANY.finditer(k): keys[int(m.group(1),16)].add(k)
bounds=sorted(set(bnd)|set(inv)); accepted=[]; rejected=collections.Counter()
types={'int':'H','unsigned int':'I','unsigned':'I','long':'J','long int':'J','unsigned long':'K','unsigned long int':'K','float':'M','double':'N','short':'F','short int':'F','unsigned short':'G','unsigned short int':'G','char':'D','signed char':'C','unsigned char':'E','bool':'_N'}
for va,g in sorted(inv.items()):
 if not g['decls'] or g['defs'] or sec_of(va) not in ('.data','.rdata'): continue
 # Strictly parse every recorded declaration, same explicit type/shape, no namespaces or aliases.
 ds=[]
 for d in g['decls']:
  m=re.fullmatch(r'extern\s+(?:(?:"C")\s+)?(const\s+)?([A-Za-z ]+?)\s+(DAT_[0-9a-f]{8})(?:\s*\[\s*(\d+)\s*\])?\s*;',d.strip())
  if not m or m.group(3)!=('DAT_%08x'%va) or m.group(2).strip() not in types: break
  ds.append((types[m.group(2).strip()],int(m.group(4)) if m.group(4) else None,bool(m.group(1))))
 else:
  if len(set(ds))!=1: rejected['inconsistent_declarations']+=1; continue
  tc,num,isconst=ds[0]; n=TYPES[tc][1]*(num or 1)
  if num==0: continue
  ks=keys.get(va,set()); expected='?DAT_%08x@@3'%va
  if not ks or any(not k.startswith(expected) for k in ks) or set(forms[va])!={''} or len(forms[va][''])!=1: rejected['aliases_or_namespace']+=1; continue
  # Exact source type and binary symbol type must agree; arrays are deferred because MSVC encoding requires separate proof.
  if num is not None: rejected['array_mangling_not_proven']+=1; continue
  if next(iter(forms[va]['']))!=tc: rejected['symbol_type_mismatch']+=1; continue
  if va % min(TYPES[tc][1],8): rejected['alignment']+=1; continue
  if any(a<va+n and va<b for a,b in claims): rejected['claimed']+=1; continue
  if any(refbytes(va,n)): rejected['not_zero']+=1; continue
  if bisect.bisect_right(bounds,va)<bisect.bisect_left(bounds,va+n): rejected['inner_name']+=1; continue
  if any(va-3 <= f < va+n for f in fldall): rejected['field_overlap']+=1; continue
  if not any(a<=va and va+n<=b for a,b in chunks): rejected['chunk']+=1; continue
  if lab_in(va,va+n): rejected['inner_label']+=1; continue
  accepted.append({'selection':{'va':va,'tc':tc,'file_backed':True},'size':n,'section':sec_of(va),'declarations':g['decls'],'unit_symbol_keys':sorted(ks),'const':isconst})
assert all(a['selection']['va']+a['size']<=b['selection']['va'] for a,b in zip(accepted,accepted[1:]))
out={'schema_version':1,'description':'Strict lexical source + matching global COFF type; no existing claims or recorded rewrites; names and labels checked within extent. Source declaration inventory is not a complete C++ parser. No padding accepted without ownership proof.','accepted':accepted,'selection_entries':[x['selection'] for x in accepted],'accepted_count':len(accepted),'accepted_bytes':sum(x['size'] for x in accepted),'rejected':dict(rejected),'padding_entries':[],'bss':'Deferred: 7171 distinct units DAT addresses in raw-less virtual tail, no file bytes.'}
json.dump(out,open(here/'inventory/b8_zeros_accepted.json','w'),indent=2)
print(json.dumps({k:v for k,v in out.items() if k not in ('accepted','selection_entries')},indent=2))


