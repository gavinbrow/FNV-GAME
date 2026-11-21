import json,collections,sys,hashlib,ntpath,re
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent;P=M.parent.parent
sys.path.insert(0,str(R/'pinned-build'));import uncovered_v2 as U
lib=Path(r'C:\path\to\Decompilation\FNV\tools\vc2008\VC\lib'); ids={};uid=100000
for f in ('libcmt.lib','libcpmt.lib'):
 members=U.read_ar(lib/f); longnames=next((body for name,body in members if name=='//'),b'')
 for name,blob in members:
  uid+=1
  if name.startswith('/') and name[1:].isdigit():
   offset=int(name[1:]); end=longnames.find(b'\0',offset)
   name=ntpath.basename(longnames[offset:end].decode('latin1')) if end>=0 else name
  ids[uid]={'library':f,'member':name}
meta=json.load(open(R/'data-v3/out/produced_ranges.json')); ext=[x for x in json.load(open(H/'phase2_accounting.json'))['extents'] if x['class']=='library'];
bykind=collections.Counter();bymember=collections.Counter();unmapped=collections.Counter();mixed=collections.Counter(); rows=[]
for x in ext:
 a=x['va'];b=x['end']; relevant=[e for e in meta if e['tier']!='M' and e['unit']>=100000 and e['va']<b and a<e['va']+e['size']]
 cuts=sorted({a,b}|{max(a,e['va']) for e in relevant}|{min(b,e['va']+e['size']) for e in relevant})
 for lo,hi in zip(cuts,cuts[1:]):
  matches=[e for e in relevant if e['va']<hi and lo<e['va']+e['size']]; kinds=tuple(sorted({e['kind'] for e in matches}));members=tuple(sorted({e['unit'] for e in matches}));n=hi-lo
  if len(kinds)==1:bykind[kinds[0]]+=n
  else:mixed['+'.join(kinds)]+=n
  for uid in members:bymember[uid]+=n
  if not members:unmapped['no_current_metadata']+=n
  rows.append({'va':lo,'end':hi,'size':n,'kinds':list(kinds),'units':list(members)})
assert sum(bykind.values())+sum(mixed.values())==65726
res={'scope':'Disjoint saved library-only 65,726-byte subset; kind labels and pseudo-unit IDs from current unarchived produced_ranges metadata. Per-member coverage may overlap and does not imply causal rejection.','total':65726,'kind_unique_bytes':dict(bykind),'mixed_kind_bytes':dict(mixed),'unmapped':dict(unmapped),'member_coverage_nonadditive':[{'unit':k,'library':ids.get(k,{}).get('library'),'member':ids.get(k,{}).get('member'),'bytes':v} for k,v in bymember.most_common()],'extent_annotations':rows}
groups=collections.Counter()
for row in rows:
 flags=[bool(re.search(r'(?:_pow|_atan|_acos|_asin|_tan|_log|_sin|_cos|_exp)',ids[u]['member'].lower())) for u in row['units']]
 groups['math_named_only' if flags and all(flags) else 'math_and_other' if any(flags) else 'other_only']+=row['size']
res['member_name_group_bytes']=dict(groups)
res['multiple_members_overlapping_bytes']=sum(row['size'] for row in rows if len(row['units'])>1)
res['library_sha256']={n:hashlib.sha256((lib/n).read_bytes()).hexdigest() for n in ('libcmt.lib','libcpmt.lib')}
json.dump(res,open(H/'library_triage.json','w'),indent=2);print('kinds',dict(bykind),'mixed',dict(mixed),'top',res['member_coverage_nonadditive'][:8])

