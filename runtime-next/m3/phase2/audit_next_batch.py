"""Read-only range reconciliation for the staged next-batch proposals."""
import json,hashlib,collections,bisect
from pathlib import Path
M=Path(__file__).resolve().parent.parent;load=lambda p:json.load(open(M/p,encoding='utf-8-sig'))
cur=load('out/phase2-w-arrays-expanded/selection.json')['entries'];new=load('out/phase2-cost245-proposal/selection.json')['entries'];lib=load('out/phase2-library-splits/selection-with-atan.json')['candidates'];sm=load('out/phase2-library-cli-smoke/dv1_pieces.json')['pieces']
types={'H':4,'I':4,'M':4,'N':8,'J':4,'K':4,'F':2,'G':2,'D':1,'E':1,'_N':1,'C':1,'P':4}
def span(e):return e['va'],e['va']+(types[e['tc']] if e['tc'] in types else e['size'])
def union(rs):
 out=[]
 for a,b in sorted(rs):
  if out and a<out[-1][1]:raise ValueError('overlapping range')
  if out and a==out[-1][1]:out[-1]=(out[-1][0],b)
  else:out.append((a,b))
 return out
if union(map(span,cur))!=union(map(span,new)):raise ValueError('M3 coverage changed')
union((x['va'],x['va']+x['size']) for x in lib)
sm=sorted(sm,key=lambda x:x['va']); starts=[x['va'] for x in sm]
for x,y in zip(sm,sm[1:]):
 if x['va']+x['size']>y['va']:raise ValueError('smoke DV1 overlap')
def overlaps(a,b):
 i=max(0,bisect.bisect_right(starts,a)-1);out=[]
 while i<len(sm) and sm[i]['va']<b:
  if a<sm[i]['va']+sm[i]['size']:out.append(sm[i])
  i+=1
 return out
for e in new:
 a,b=span(e)
 if overlaps(a,b):raise ValueError('M3 overlaps smoke DV1')
same=[];added=[]
for x in lib:
 matches=overlaps(x['va'],x['va']+x['size'])
 if matches:
  if len(matches)!=1:raise ValueError('ambiguous overlap')
  y=matches[0]
  if (x['va'],x['size'],x['unit'])!=(y['va'],y['size'],y['unit']) or y.get('library_opt_in') is not True or hashlib.sha256(bytes.fromhex(y['data'])).hexdigest()!=x['compiler_bytes_sha256']:raise ValueError('library overlap differs from smoke')
  same.append(x)
 else:added.append(x)
print(json.dumps({'m3_entries_before':len(cur),'m3_entries_after':len(new),'m3_union_equal':True,'m3_smoke_dv1_overlaps':0,'library_existing_pieces':len(same),'library_existing_bytes':sum(x['size'] for x in same),'library_incremental_pieces':len(added),'library_incremental_bytes':sum(x['size'] for x in added),'native_heads':dict(collections.Counter(x['tc'] for x in new if x['tc'] in ('Q','V','Y'))),'limitation':'Range and metadata audit only; not new object/image build or full semantic type proof.'},indent=2))
