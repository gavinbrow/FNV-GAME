"""Compare non-recipe COFF sections of the pinned BFC original/candidate cohort.

Diagnostic only: multiset equality does not prove COMDAT or final ownership.
"""
import collections,hashlib,json,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';O=M/'out';sys.path.insert(0,str(F/'tools'));from compare import Coff
INDEX=O/'phase2-bfc-core-proof-index.json';UNITS=O/'phase2-flags-script-production-before/units.json';OUT=O/'phase2-bfc-nonmapped-sections-audit.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def classify(sec,names):
 if any(n.startswith(('??_7','??_R')) for n in names):return 'rtti_or_vtable'
 if any(n.startswith(('??_E','??_G','??_9')) for n in names):return 'deleting_or_adjustor'
 if any(n.startswith(('__eh','?dtor$','?catch$','__unwind')) for n in names) or sec['name'].startswith(('.xdata','.pdata','.text$x')):return 'eh_or_thunk'
 if sec['name'].startswith('.CRT'):return 'static_initializer'
 if sec['flags']&0x20:return 'other_code'
 return 'other_data'
def weak(coff,norm):
 ptr,count=struct.unpack_from('<II',coff.data,8);out=[]
 if ptr+18*count>len(coff.data):raise ValueError('short symbols')
 for i,s in coff.symbols.items():
  if s['storage']!=105:continue
  aux=coff.data[ptr+18*(i+1):ptr+18*(i+2)]
  if len(aux)!=18:raise ValueError('short weak aux')
  tag,kind=struct.unpack_from('<II',aux);target=coff.symbols.get(tag)
  if target is None:raise ValueError('weak fallback index invalid')
  out.append((norm.get(s['name'],s['name']),s['value'],s['section'],s['type'],kind,norm.get(target['name'],target['name']),sha(aux[8:])))
 return sorted(out)
def mapped(coff,unit,norm=None):
 indices=set();missing=[]
 for f in unit['functions']:
  for name in [f['symbol']]+f.get('fold_aliases',[]):
   try:s=coff.named(name);indices.add(s['section'])
   except ValueError:missing.append(name)
 return indices,missing

def signatures(coff,skip,norm):
 defs=collections.defaultdict(list)
 for s in coff.symbols.values():
  if s['section']>0 and not s['name'].startswith('.'):
   defs[s['section']].append((norm.get(s['name'],s['name']),s['value'],s['type'],s['storage']))
 records=[]
 for i,sec in enumerate(coff.sections):
  if not sec or i in skip:continue
  d=sorted(defs[i]);rels=[]
  for off,idx,kind in sec['relocs']:
   t=coff.symbols.get(idx)
   if t is None:raise ValueError('reloc to missing symbol')
   target=norm.get(t['name'],t['name']);tsec=coff.sections[t['section']]['name'] if t['section']>0 else t['section']
   rels.append((off,kind,target,t['value'],t['type'],t['storage'],tsec))
  category=classify(sec,[x[0] for x in d]);sig=(category,sec['name'],sec['flags'],len(sec['data']),sha(sec['data']),tuple(d),tuple(sorted(rels)))
  records.append((i,sig))
 return records

def main():
 if OUT.exists():raise FileExistsError('no overwrite')
 iraw=INDEX.read_bytes();idx=json.loads(iraw);uraw=UNITS.read_bytes()
 if sha(uraw)!=idx['recipe_sha256']:raise ValueError('recipe mismatch')
 units=json.loads(uraw)['units'];tot=collections.Counter();rows=[];exceptions=[]
 for item in idx['units']:
  i=item['unit'];report=M/item['report'];d=report.parent
  try:
   if sha(report.read_bytes())!=item['report_sha256'] or sha((d/'mirror-manifest.json').read_bytes())!=item['mirror_manifest_sha256']:raise ValueError('proof input changed')
   proof=json.loads(report.read_bytes());pairs=proof['mirror_to_candidate_literals'];normal={}
   for p in pairs:
    if p['after'] in normal and normal[p['after']]!=p['before']:raise ValueError('ambiguous literal normalization')
    normal[p['after']]=p['before']
   paths={k:d/(k+'.obj') for k in ('original','candidate')}
   for k,p in paths.items():
    if sha(p.read_bytes())!=item['objects'][k]:raise ValueError('object hash changed')
   a=Coff(str(paths['original']));b=Coff(str(paths['candidate']));sa,ma=mapped(a,units[i]);sb,mb=mapped(b,units[i])
   if ma or mb:raise ValueError('recipe function/alias missing')
   aa=signatures(a,sa,{});bb=signatures(b,sb,normal);ca=collections.Counter(x[1] for x in aa);cb=collections.Counter(x[1] for x in bb);same=ca&cb;left=ca-cb;right=cb-ca;cats=collections.Counter()
   for sig,n in same.items():cats['equal/'+sig[0]]+=n
   for sig,n in left.items():cats['original_only/'+sig[0]]+=n
   for sig,n in right.items():cats['candidate_only/'+sig[0]]+=n
   ambiguous=sum(n for n in same.values() if n>1)
   wa=weak(a,{});wb=weak(b,normal);w_eq=wa==wb
   tot.update(cats);tot['units']+=1;tot['original_nonmapped_sections']+=len(aa);tot['candidate_nonmapped_sections']+=len(bb);tot['duplicate_equal_sections']+=ambiguous;tot['units_weak_mismatch']+=not w_eq
   if left or right or not w_eq:
    def compact(c):return [{'category':s[0],'section':s[1],'flags':s[2],'size':s[3],'data_sha256':s[4],'definitions':[x[0] for x in s[5]],'relocation_count':len(s[6]),'count':n} for s,n in c.items()]
    rows.append({'unit':i,'source':units[i]['source'],'original_mapped_sections_skipped':len(sa),'candidate_mapped_sections_skipped':len(sb),'original_only':compact(left),'candidate_only':compact(right),'weak_equal':w_eq,'weak_counts':[len(wa),len(wb)]})
  except Exception as e:exceptions.append({'unit':i,'error':type(e).__name__+': '+str(e)})
 result={'scope':'all sections outside those containing any recipe function; exact content/definitions/relocations multiset after separately evidenced same-unit SG renaming','cohort_index_sha256':sha(iraw),'recipe_sha256':sha(uraw),'totals':dict(tot),'mismatch_units':rows,'errors':exceptions,'limitations':['mapped sections omitted wholesale; nonfunction bytes sharing those sections remain unreviewed','identical duplicate sections are ambiguous; multiset equality does not prove placement, COMDAT ownership or ICF','raw COFF section bytes include unrelocated addends, not final image relocation results','symbol extents beyond their containing complete section are not independently established','weak aux compared structurally; unchanged does not prove valid resolution','static include/ODR, global data placement and final runtime remain separate']}
 OUT.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'units':tot['units'],'original_sections':tot['original_nonmapped_sections'],'candidate_sections':tot['candidate_nonmapped_sections'],'mismatch_units':len(rows),'weak_mismatch_units':tot['units_weak_mismatch'],'errors':len(exceptions)}))
if __name__=='__main__':main()
