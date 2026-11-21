"""Generate accepted raw data partition from the archived accepted default ranges."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;ROOT=M.parent.parent;sys.path.insert(0,str(M));import gen_m3 as G
D=M/'out/phase2-next-data-default-verified/evidence';B=M/'out/batch8-promoted-default-verified/evidence';OUT=H/'accepted_range_partition.json';OLD=H/'accepted_range_partition.before-next-data.json'
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 review=j(D/'root-default-review.json');print('review status',review.get('status'))
 if not str(review.get('status','')).startswith('PASS'):raise ValueError('default not accepted')
 if OLD.exists():raise FileExistsError(OLD)
 pieces=j(D/'dv1_pieces.json')['pieces'];entries=j(D/'m3_manifest.json')['entries'];produced=j(M/'inventory/b7_produced.json');previous=j(OUT)
 totals={'m3':0,'dv1':0,'produced_unspliced':0,'uncovered_nonzero':0,'uncovered_zero':0,'rewrite':0};value={'m3_zero':0,'m3_nonzero':0,'dv1_zero':0,'dv1_nonzero':0};delta={'produced_unspliced':0,'uncovered_nonzero':0,'uncovered_zero':0,'rewrite':0};oldpieces=j(B/'dv1_pieces.json')['pieces'];oldman=j(B/'m3_manifest.json')['entries']
 for sec in ('.data','.rdata'):
  s=G.SEC[sec];lo=s['va'];n=s['raw'];raw=G.refbytes(lo,n);flags=bytearray(n);old=bytearray(n)
  def paint(a,size,bit,arr,exclusive=False):
   l=max(a,lo)-lo;r=min(a+size,lo+n)-lo
   if l>=r:return
   for i in range(l,r):
    if exclusive and arr[i]&6:raise ValueError('accepted overlap '+hex(lo+i))
    arr[i]|=bit
  for a,size in produced:paint(a,size,1,flags);paint(a,size,1,old)
  for a,size in ((0xfdf000,1188),(0x118062c,6688),(0x110147c,24)):paint(a,size,8,flags);paint(a,size,8,old)
  for records,bit in ((entries,2),(pieces,4)):
   for e in records:
    if e['section']==sec:paint(e['va'],e['size'],bit,flags,True)
  for records,bit in ((oldman,2),(oldpieces,4)):
   for e in records:
    if e['section']==sec:paint(e['va'],e['size'],bit,old,True)
  for i,f in enumerate(flags):
   if f&8:
    if f&6:raise ValueError('rewrite overlap')
    k='rewrite'
   elif f&2:k='m3'
   elif f&4:k='dv1'
   elif f&1:k='produced_unspliced'
   else:k='uncovered_nonzero' if raw[i] else 'uncovered_zero'
   totals[k]+=1
   if k in ('m3','dv1'):value[k+('_nonzero' if raw[i] else '_zero')]+=1
   if f&6 and not old[i]&6:
    oldk='rewrite' if old[i]&8 else 'produced_unspliced' if old[i]&1 else 'uncovered_nonzero' if raw[i] else 'uncovered_zero';delta[oldk]+=1
 remaining={k:totals[k] for k in delta};remaining['total']=sum(remaining.values());accepted={'m3':totals['m3'],'dv1':totals['dv1'],'total':totals['m3']+totals['dv1'],'tls_excluded':sum(e['size'] for e in pieces+entries if e['section']=='.tls'),'reference_values':value}
 if accepted['total']!=1613010 or remaining!={'produced_unspliced':190886,'uncovered_nonzero':67551,'uncovered_zero':100045,'rewrite':7900,'total':366382}:raise ValueError('unexpected partition')
 paths={'old_dv1':B/'dv1_pieces.json','old_m3':B/'m3_manifest.json','new_dv1':D/'dv1_pieces.json','new_m3':D/'m3_manifest.json','produced_inventory':M/'inventory/b7_produced.json','acceptance':D/'root-default-review.json','selection':D/'selection.json','library_selection':D/'library_candidates.json','old_partition':OUT}
 out={'schema':2,'input_sha256':{k:h(p) for k,p in paths.items()},'raw_data_rdata':sum(G.SEC[x]['raw'] for x in ('.data','.rdata')),'accepted':accepted,'delta_since_batch8':delta,'remaining':remaining,'note':'Computed from disjoint actual archived M3/DV1 range union, frozen B7 produced ranges, rewrite union and reference bytes. Produced labels do not imply blocker causes. Typed 364 bytes replace W inside unchanged selected range union.'}
 OLD.write_bytes(OUT.read_bytes());OUT.write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
