import os,sys,json,re,bisect,collections
os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.argv=[sys.argv[0]]
s=open('b7_select.py').read().split('entries = [];')[0]; exec(compile(s,'b7_select.py','exec'),globals())
candidates=json.load(open('inventory/b8_type_candidates.json'))['rows']
selected=json.load(open('batch7_selection.json'))['entries']
def esize(e): return 4 if e['tc']=='P' else TYPES[e['tc']][1] if e['tc'] in TYPES else e['size']
covered=[(e['va'],e['va']+esize(e)) for e in selected]+dv1+prod+REWRITTEN
covered.sort(); starts=[a for a,b in covered]; prefix=[]; mx=0
for a,b in covered: mx=max(mx,b); prefix.append(mx)
def overlap(a,b):
 i=bisect.bisect_left(starts,b)-1
 return i>=0 and prefix[i]>a
# Integer types only; exclude bool, float and doubles and any inferred pointer/array.
ctypes={'D':('char',1),'C':('signed char',1),'E':('unsigned char',1),'F':('short',2),'G':('unsigned short',2),'H':('int',4),'I':('unsigned int',4),'J':('long',4),'K':('unsigned long',4)}
normal={'char':'D','signed char':'C','unsigned char':'E','short':'F','short int':'F','signed short':'F','signed short int':'F','unsigned short':'G','unsigned short int':'G','int':'H','signed':'H','signed int':'H','unsigned':'I','unsigned int':'I','long':'J','long int':'J','signed long':'J','signed long int':'J','unsigned long':'K','unsigned long int':'K'}
accepted=[]; rejected=collections.Counter()
for r in candidates:
 x=r['va']; codes={z['code'] for z in r['type_observations']}
 if not codes or not codes <= ctypes.keys(): rejected['noninteger-or-unknown-encoding']+=1; continue
 widths={ctypes[c][1] for c in codes}
 if len(widths)!=1: rejected['different-widths']+=1; continue
 width=next(iter(widths)); ds=r['declarations']
 if not ds: rejected['no-source-evidence']+=1; continue
 parsed=[]
 for d in ds:
  # Require a simple complete declaration: no pointer, array, multiple declarators, or initializer.
  m=re.fullmatch(r'\s*extern\s+(?:(?:const|volatile)\s+)*(.*?)\s+DAT_[0-9a-f]{8}\s*;\s*',d)
  if not m: break
  key=' '.join(m.group(1).split()); c=normal.get(key)
  if c is None: break
  parsed.append(c)
 if len(parsed)!=len(ds) or not set(parsed)<=codes or not codes<=set(parsed): rejected['source-type-mismatch-or-complex']+=1; continue
 if x%width or width>r['interval_size']: rejected['alignment-or-interval']+=1; continue
 if overlap(x,x+width): rejected['existing-or-rewritten-overlap']+=1; continue
 # All named boundaries, data labels, value-rule fields, and original relocations are excluded.
 if any(x<v<x+width for v in bnds) or lab_in(x,x+width): rejected['internal-label']+=1; continue
 if fld_near(x-3,x+width): rejected['field-or-relocation']+=1; continue
 data=refbytes(x,width)
 if len(data)!=width or not any(data): rejected['zero-or-short']+=1; continue
 # Emit storage-preserving unsigned integer; signedness is only a source interpretation.
 bits=int.from_bytes(data,'little')
 accepted.append(dict(va=x,size=width,section=r['section'],source_bucket=r['bucket'],encoded_types=sorted(codes),source_declarations=ds,raw_hex=data.hex(),unsigned_value=bits,proposed_c_type={1:'unsigned char',2:'unsigned short',4:'unsigned int'}[width],proposed_symbol='M3_%08x'%x,alignment=width,extent_evidence='simple scalar extern declarations of same width in source and encoded unit symbols',unresolved='signedness and original symbol/namespace aliases are not resolved; no tail claimed'))
out={'schema_version':1,'method':'Conservative scalar storage heads only; candidates require generator/COFF and round-trip validation before use.','entries':accepted,'rejections':dict(rejected)}
with open('inventory/b8_types_accepted.json','w') as f: json.dump(out,f,indent=2)
print('accepted',len(accepted),'bytes',sum(e['size'] for e in accepted),'buckets',dict(collections.Counter(e['source_bucket'] for e in accepted)),'rejected',dict(rejected))
