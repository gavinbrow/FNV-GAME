import os, sys, json, re, bisect, collections
from pathlib import Path
here=Path(__file__).resolve().parent.parent
os.chdir(here)
sys.argv=['b7_select.py']
source=(here/'b7_select.py').read_text(); __file__=str(here/'b7_select.py')
exec(compile(source[:source.index('entries = [];')], str(here/'b7_select.py'), 'exec'), globals())
b7=json.load(open(here/'batch7_selection.json'))['entries']
def esize(e): return 4 if e['tc']=='P' else TYPES[e['tc']][1] if e['tc'] in TYPES else e['size']
m3=[(e['va'],e['va']+esize(e)) for e in b7]
# Independently partition every raw byte; rewrite wins even over earlier overlays.
counts=collections.Counter(); sec_counts={}; candidates=[]; skipped_zero=collections.Counter(); rewritten_prior=collections.Counter()
all_decl=set(bnd)|set(inv)
# source inventory represents DAT names not necessarily all symbol forms.
all_decl=sorted(all_decl)
for n in ('.data','.rdata'):
 s=SEC[n]; lo=s['va']; hi=lo+s['raw']; raw=refbytes(lo,s['raw']); tags=bytearray(s['raw'])
 # m3 and selected dv1 supersede produced. Rewrite is final authority.
 for t,rs in ((1,prod),(2,dv1),(3,m3),(4,REWRITTEN)):
  for a,b in rs:
   x=max(a,lo); y=min(b,hi)
   if x<y:
    if t == 4:
     for i in range(x-lo,y-lo): rewritten_prior[('uncovered','produced','dv1','m3','rewritten')[tags[i]]+'_'+('nonzero' if raw[i] else 'zero')]+=1
    tags[x-lo:y-lo]=bytes([t])*(y-x)
 local=collections.Counter()
 for i,q in enumerate(raw):
  key=('uncovered','produced_unspliced','dv1','m3','rewritten')[tags[i]]+'_'+('nonzero' if q else 'zero')
  local[key]+=1; counts[key]+=1
 sec_counts[n]=dict(local)
 # Match batch-7 unowned intervals, cut at all known declaration starts; reject any named owner interval.
 for m in re.finditer(b'\x00+', bytes(tags)):
  ra,rb=lo+m.start(),lo+m.end()
  cuts=[ra]+all_decl[bisect.bisect_right(all_decl,ra):bisect.bisect_left(all_decl,rb)]+[rb]
  for x,y in zip(cuts,cuts[1:]):
   if x in all_decl:
    skipped_zero['starts_at_declaration']+=refbytes(x,y-x).count(0); continue
   for a,b in pieces(x,y)[0]:
    if all(v==0 for v in refbytes(a,b-a)):
     # ensure entire range remains unclaimed, raw backed, no declaration at start/interior
     assert not any(tags[a-lo:b-lo]) and bisect.bisect_left(all_decl,b)==bisect.bisect_left(all_decl,a)
     candidates.append({'va':a,'end':b,'size':b-a,'section':n,'alignment':min(a & -a,4)})
# Record BSS by name/address without assigning an inferred extent.
bss=[g for g in inv.values() if g.get('bss')]
bss_names=sorted({int(m.group(1),16) for u in units for k in u.get('symbols',{}) for m in re.finditer(r'DAT_([0-9a-f]{8})',k) if bss_lo <= int(m.group(1),16) < bss_hi})
print('inv sample', next(iter(inv.values())).keys())
out={'description':'Batch 7 raw-byte partition; rewritten ranges take precedence over overlays and produced ranges. Candidate ranges are zero-only, unclaimed, cut at known names/chunks and field/relocation exclusions; object ownership/type is not proven.', 'section_counts':sec_counts,'totals':dict(counts),'candidate_count':len(candidates),'candidate_bytes':sum(c['size'] for c in candidates),'candidate_extents':candidates,'declaration_start_interval_zero_bytes':dict(skipped_zero),'rewritten_prior_ownership':dict(rewritten_prior),'bss_detected_flag_count':len(bss),'bss_units_dat_addresses':bss_names, 'bss_units_dat_count':len(bss_names)}
json.dump(out,open(here/'inventory/b8_zero_accounting.json','w'),indent=2)
print(json.dumps({k:v for k,v in out.items() if k not in ('candidate_extents','bss_units_dat_addresses')},indent=2))



