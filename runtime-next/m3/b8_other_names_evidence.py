import json,sys,os,re,bisect,collections
from pathlib import Path
here=Path(__file__).resolve().parent
sys.path.insert(0,str(here)); sys.path.insert(0,str(here/'tools'))
import inventory_globals as ig
import inventory_symbol_forms as sf
# Execute selector setup only; no selection output or mutation.
source=(here/'b7_select.py').read_text(); setup=source.split('entries = []; stat_bytes')[0]
sys.argv=[str(here/'b7_select.py')]
env={'__file__':str(here/'b7_select.py'),'__name__':'b8_evidence'}
exec(compile(setup,str(here/'b7_select.py'),'exec'),env)
units=env['units']; bnds=env['bnds']; bnd=env['bnd']; refbytes=env['refbytes']; SEC=env['SEC']; tag=env['tag']; decl_class=env['decl_class']
keys=collections.defaultdict(list)
for u in units:
 for key in u.get('symbols',{}):
  for m in env['ADDR_ANY'].finditer(key): keys[int(m.group(1),16)].append(key)
intervals=[]
for n in ('.data','.rdata'):
 lo=SEC[n]['va']; arr=bytes(tag[n])
 for m in re.finditer(b'\x00+',arr):
  ra,rb=lo+m.start(),lo+m.end(); cuts=[ra]+bnds[bisect.bisect_right(bnds,ra):bisect.bisect_left(bnds,rb)]+[rb]
  for x,y in zip(cuts,cuts[1:]):
   if x in bnd and decl_class(x)[1]=='declared-other-name':
    raw=refbytes(x,y-x)
    intervals.append({'start':x,'end':y,'interval_bytes':y-x,'nonzero_bytes':sum(bool(v) for v in raw),'unit_symbol_keys':sorted(set(keys[x]))})
rows=sf.inventory_files(list(ig.iter_source_files()))
byaddr=collections.defaultdict(list)
for r in rows: byaddr[int(r['address'],16)].append(r)
for i in intervals:
 i['source_spellings']=byaddr[i['start']]
 # Every interval is provisional: a symbol name establishes a boundary, not an object extent.
 i['candidate_status']='deferred'
 i['reason']='Interval end is a selector boundary, not evidence of declared object extent; alias linkage and source type require review.'
fields=env['fldall']; original_inv=env['inv']
sizes={'char':1,'unsigned char':1,'short':2,'unsigned short':2,'int':4,'unsigned int':4,'float':4}
for i in intervals:
 x=i['start']; rs=i['source_spellings']; ds=[d for r in rs if r['name']=='DAT_%08x'%x for d in r['declarations']]; types=set()
 for d in ds:
  m=re.fullmatch(r'\s*extern\s+"C"\s+(char|unsigned char|int|unsigned int|float|short|unsigned short)\s+DAT_[0-9a-f]{8}\s*;\s*(?://.*)?',d['text'])
  types.add(m[1] if m else '?')
 if i['unit_symbol_keys']!=['_DAT_%08x'%x] or len(rs)!=1 or len(types)!=1 or '?' in types or not ds or original_inv.get(x,{}).get('defs'): continue
 t=next(iter(types)); n=sizes[t]
 if n>i['interval_bytes'] or any(f<x+n and f+4>x for f in fields) or not any(refbytes(x,n)): continue
 i['candidate_status']='review_candidate'
 i['candidate']={'source_name':'DAT_%08x'%x,'coff_symbol':'_DAT_%08x'%x,'linkage':'extern C','declared_type':t,'declared_extent_bytes':n,'candidate_start':x,'candidate_end':x+n,'extent_basis':'x86 MSVC primitive scalar declaration; not interval tail','required_validation':['verify selected range against current placements and rewritten directories','compile exact declaration and check object bytes, section, alignment and relocations','run integrated byte and relocation checks and negative controls'],'selection_ready':False}
 i['reason']='Scalar head is supported by consistent captured declarations and matching C-decorated unit key; interval tail is explicitly excluded. Lexical scan and placement require validation.'
output={'schema_version':1,'definition':'Batch 7 declared-other-name intervals reconstructed from saved inputs and original read-only image; end is exclusive and is not a declaration extent.','summary':{'interval_count':len(intervals),'interval_bytes':sum(i['interval_bytes'] for i in intervals),'nonzero_bytes':sum(i['nonzero_bytes'] for i in intervals),'candidate_count':sum(i['candidate_status']=='review_candidate' for i in intervals),'candidate_head_bytes':sum(i.get('candidate',{}).get('declared_extent_bytes',0) for i in intervals)},'intervals':intervals}
p=here/'inventory'/'b8_other_names.json'
with p.open('x',encoding='utf-8') as f: json.dump(output,f,indent=2)
print(json.dumps(output['summary']))
print('keys',collections.Counter(re.sub(r'_[0-9a-f]{8}.*','',k) for i in intervals for k in i['unit_symbol_keys']).most_common(15))
print('source spellings',collections.Counter(r['name'].rsplit('_',1)[0] for i in intervals for r in i['source_spellings']))
print('source matching intervals',sum(bool(i['source_spellings']) for i in intervals))
