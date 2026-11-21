"""Generate a candidate partition from archived native-source positive; never update accepted record."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;sys.path.insert(0,str(M));import gen_m3 as G
OLD=M/'out/phase2-next-data-default-verified/evidence';NEW=M/'out/phase2-native-source-positive/evidence';ACC=H/'accepted_range_partition.json';OUT=NEW/'candidate-disjoint-partition.json'
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError(OUT)
 accepted=j(ACC);prev=sha(ACC);a=j(OLD/'dv1_pieces.json')['pieces'];b=j(NEW/'dv1_pieces.json')['pieces'];am=j(OLD/'m3_manifest.json')['entries'];bm=j(NEW/'m3_manifest.json')['entries'];inventory=M/'inventory/b7_produced.json';produced=j(inventory)
 if sha(OLD/'dv1_pieces.json')!=accepted['input_sha256']['new_dv1'] or sha(OLD/'m3_manifest.json')!=accepted['input_sha256']['new_m3']:raise ValueError('accepted archive differs')
 if sha(NEW/'selection.json')!=sha(OLD/'selection.json') or sorted((x['va'],x['size']) for x in am)!=sorted((x['va'],x['size']) for x in bm):raise ValueError('M3 selection or union changed')
 tails=(0x10cb640,0x11887e0,0x11a9c3c);tailchecks=[]
 for va in tails:
  x=next(x for x in am if x['va']==va);y=next(x for x in bm if x['va']==va)
  if any(x.get(k)!=y.get(k) for k in ('va','size','sym','tgts','fields','section')):raise ValueError('retained W tail metadata changed '+hex(va))
  tailchecks.append({'va':hex(va),'size':x['size'],'symbol':x['sym'],'targets':x.get('tgts')})
 totals={k:0 for k in ('m3','dv1','produced_unspliced','uncovered_nonzero','uncovered_zero','rewrite')};vals={k:0 for k in ('m3_zero','m3_nonzero','dv1_zero','dv1_nonzero')};delta={k:0 for k in ('produced_unspliced','uncovered_nonzero','uncovered_zero','rewrite')}
 for sec in ('.data','.rdata'):
  s=G.SEC[sec];lo=s['va'];n=s['raw'];raw=G.refbytes(lo,n);now=bytearray(n);before=bytearray(n)
  def paint(pos,size,bit,dst,exclusive=False):
   l=max(pos,lo)-lo;r=min(pos+size,lo+n)-lo
   if l>=r:return
   for i in range(l,r):
    if exclusive and dst[i]&6:raise ValueError('accepted range overlaps')
    dst[i]|=bit
  for pos,size in produced:paint(pos,size,1,now);paint(pos,size,1,before)
  for pos,size in ((0xfdf000,1188),(0x118062c,6688),(0x110147c,24)):paint(pos,size,8,now);paint(pos,size,8,before)
  for rows,bit in ((bm,2),(b,4)):
   for x in rows:
    if x['section']==sec:paint(x['va'],x['size'],bit,now,True)
  for rows,bit in ((am,2),(a,4)):
   for x in rows:
    if x['section']==sec:paint(x['va'],x['size'],bit,before,True)
  for i,f in enumerate(now):
   if f&8:
    if f&6:raise ValueError('rewrite overlap')
    cat='rewrite'
   elif f&2:cat='m3'
   elif f&4:cat='dv1'
   elif f&1:cat='produced_unspliced'
   else:cat='uncovered_nonzero' if raw[i] else 'uncovered_zero'
   totals[cat]+=1
   if cat in ('m3','dv1'):vals[cat+('_nonzero' if raw[i] else '_zero')]+=1
   if f&6 and not before[i]&6:
    oldcat='rewrite' if before[i]&8 else 'produced_unspliced' if before[i]&1 else 'uncovered_nonzero' if raw[i] else 'uncovered_zero';delta[oldcat]+=1
 remaining={k:totals[k] for k in delta};remaining['total']=sum(remaining.values());candidate={'m3':totals['m3'],'dv1':totals['dv1'],'total':totals['m3']+totals['dv1'],'tls_excluded':sum(x['size'] for x in bm+b if x['section']=='.tls'),'reference_values':vals}
 if candidate['total']!=1613018 or remaining!={'produced_unspliced':190878,'uncovered_nonzero':67551,'uncovered_zero':100045,'rewrite':7900,'total':366374} or delta!={'produced_unspliced':8,'uncovered_nonzero':0,'uncovered_zero':0,'rewrite':0}:raise ValueError('unexpected candidate partition')
 report={'status':'candidate positive only; not accepted','raw_data_rdata':1979392,'candidate':candidate,'delta_from_accepted_by_prior_bucket':delta,'remaining':remaining,'inputs':{'accepted_partition_sha256':prev,'accepted_prior_backup_sha256':sha(H/'accepted_range_partition.before-next-data.json'),'old_dv1_sha256':sha(OLD/'dv1_pieces.json'),'new_dv1_sha256':sha(NEW/'dv1_pieces.json'),'old_m3_sha256':sha(OLD/'m3_manifest.json'),'new_m3_sha256':sha(NEW/'m3_manifest.json'),'selection_sha256':sha(NEW/'selection.json'),'produced_inventory_sha256':sha(inventory),'range_delta_proof_sha256':sha(NEW/'independent-range-delta.json'),'coverage_proof_sha256':sha(NEW/'independent-coverage-audit.json')},'m3_selection_and_range_union_unchanged':True,'retained_w_tail_metadata':tailchecks,'limitations':['positive candidate awaits controls, repeat and root acceptance','M3 tail actual COFF/reference relocation checks recorded in coverage proof','produced annotation does not imply a specific blocker cause']}
 if sha(ACC)!=prev:raise ValueError('accepted file changed during analysis')
 OUT.write_text(json.dumps(report,indent=2));print(json.dumps({'output_sha256':sha(OUT),'candidate':candidate,'remaining':remaining,'delta':delta}))
if __name__=='__main__':main()
