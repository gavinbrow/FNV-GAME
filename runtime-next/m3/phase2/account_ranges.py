import sys,json,collections,hashlib
from pathlib import Path
from array import array
H=Path(__file__).resolve().parent; M=H.parent; R=M.parent; sys.path.insert(0,str(M)); import gen_m3 as G
j=lambda p:json.load(open(p,encoding='utf-8-sig'))
archive=M/'out/batch8-promoted-default-verified/evidence'; pieces=j(archive/'dv1_pieces.json')['pieces']; man=j(archive/'m3_manifest.json')['entries']; frozen=j(M/'inventory/b7_produced.json'); metadata=j(R/'data-v3/out/produced_ranges.json')
categories={1:'own_rtti',2:'own_vtable',4:'own_other',8:'library'}; totals=collections.Counter(); extents=[]; evidence=collections.Counter()
for sec in ('.data','.rdata'):
 s=G.SEC[sec];lo=s['va'];hi=lo+s['raw']; raw=G.refbytes(lo,s['raw']); status=bytearray(hi-lo); types=bytearray(hi-lo)
 def paint(a,b,flag,arr):
  x=max(lo,a); y=min(hi,b)
  for i in range(x-lo,y-lo):arr[i]|=flag
 for a,n in frozen:paint(a,a+n,1,status)
 for e in man:paint(e['va'],e['va']+e['size'],2,status)
 for e in pieces:paint(e['va'],e['va']+e['size'],4,status)
 for a,b in ((0xfdf000,0xfdf000+1188),(0x118062c,0x118062c+6688),(0x110147c,0x110147c+24)):paint(a,b,8,status)
 for e in metadata:
  if e['tier']=='M':continue
  kind=e['kind'];bit=8 if e['unit']>=100000 else 1 if kind.startswith('rtti') else 2 if kind=='vtable' else 4
  paint(e['va'],e['va']+e['size'],bit,types)
 start=None;old=None
 for i,st in enumerate(status):
  flag=types[i] if st==1 else None
  if flag!=old:
   if old is not None:
    a=lo+start;b=lo+i; chunk=raw[start:i]; name='+'.join(v for k,v in categories.items() if old&k) if old else 'unmatched_in_current_metadata'; extents.append({'va':a,'end':b,'size':b-a,'section':sec,'class':name,'zero':chunk.count(0),'nonzero':sum(bool(q) for q in chunk)});totals[name]+=b-a
   start=i;old=flag
 if old is not None:
  a=lo+start;b=hi;chunk=raw[start:];name='+'.join(v for k,v in categories.items() if old&k) if old else 'unmatched_in_current_metadata';extents.append({'va':a,'end':b,'size':b-a,'section':sec,'class':name,'zero':chunk.count(0),'nonzero':sum(bool(q) for q in chunk)});totals[name]+=b-a
assert sum(totals.values())==207636
out={'schema':1,'description':'Disjoint byte partition of frozen B7 produced ranges after final archived M3/DV1 and recorded rewrites, annotated by overlapping current produced_ranges kind/unit metadata. Multiple classes are explicit; overlap does not prove blocker causality. Current metadata is not archived with final run.','metadata_sha256':hashlib.sha256((R/'data-v3/out/produced_ranges.json').read_bytes()).hexdigest(),'selection_sha256':hashlib.sha256((archive/'batch8_final_selection.json').read_bytes()).hexdigest(),'total':sum(totals.values()),'class_bytes':dict(totals),'extents':extents}
json.dump(out,open(H/'phase2_accounting.json','w'),indent=2);print(dict(totals))
