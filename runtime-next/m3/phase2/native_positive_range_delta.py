"""Compare archived M3/DV1 coverage ranges of accepted default and source positive."""
import hashlib,json,sys
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;sys.path[:0]=[str(M),str(M.parent.parent/'fnv_decomp/tools')]
import gen_m3 as G
from compare import Coff
A=M/'out/phase2-next-data-default-verified/evidence';B=M/'out/phase2-native-source-positive/evidence';P=B/'independent-range-delta.json'
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if P.exists():raise FileExistsError(P)
 pieces=[j(x/'dv1_pieces.json')['pieces'] for x in (A,B)];ms=[j(x/'m3_manifest.json')['entries'] for x in (A,B)];delta=[];tot=[]
 for p,m in zip(pieces,ms):
  allranges=sorted((x['va'],x['va']+x['size']) for x in p+m)
  if any(a[1]>b[0] for a,b in zip(allranges,allranges[1:])):raise ValueError('M3/DV1 overlap')
  tot.append({s:sum(x['size'] for x in p if x['section']==s) for s in ('.data','.rdata','.tls')})
 if sorted((x['va'],x['size']) for x in ms[0])!=sorted((x['va'],x['size']) for x in ms[1]):raise ValueError('M3 extents changed')
 for sec in ('.data','.rdata','.tls'):
  aa=sorted((x for x in pieces[0] if x['section']==sec),key=lambda x:x['va']);bb=sorted((x for x in pieces[1] if x['section']==sec),key=lambda x:x['va']);bounds=sorted({v for x in aa+bb for v in (x['va'],x['va']+x['size'])});i=k=0
  for l,r in zip(bounds,bounds[1:]):
   while i<len(aa) and aa[i]['va']+aa[i]['size']<=l:i+=1
   while k<len(bb) and bb[k]['va']+bb[k]['size']<=l:k+=1
   x=aa[i] if i<len(aa) and aa[i]['va']<=l<r<=aa[i]['va']+aa[i]['size'] else None;y=bb[k] if k<len(bb) and bb[k]['va']<=l<r<=bb[k]['va']+bb[k]['size'] else None
   if bool(x)!=bool(y):
    q=x or y;item={'section':sec,'va':hex(l),'end':hex(r),'size':r-l,'direction':'lost' if x else 'gained','piece_va':hex(q['va']),'piece_size':q['size'],'kind':q['kind'],'unit':q['unit'],'names':q['names'],'relocations':q['relocs']}
    if sec in ('.data','.rdata'):
     data=G.refbytes(l,r-l);item['reference_zero']=data.count(0);item['reference_nonzero']=sum(bool(x) for x in data)
    delta.append(item)
 if len(delta)!=1 or delta[0]['va']!='0x1045400' or delta[0]['size']!=8 or delta[0]['unit']!=620 or delta[0]['direction']!='gained':raise ValueError('unexpected coverage delta')
 c=Coff(str(B/'0620.obj'));s=c.named('??_7BGSBodyPart@@6B@');z=c.sections[s['section']];rel=[(v,c.symbols[n]['name'],kind) for v,n,kind in z['relocs']]
 if z['name']!='.rdata' or s['value']!=4 or len(z['data'])!=8 or rel!=[(0,'??_R4BGSBodyPart@@6B@',6),(4,'?QueueResourceLoad@BGSBodyPart@@UAEXW4IO_TASK_PRIORITY@@PAVQueuedFile@@@Z',6)]:raise ValueError('native BGS table differs')
 tls=[]
 for p in pieces:
  tls.append([{'va':hex(x['va']),'size':x['size'],'section':x['section'],'unit':x['unit'],'names':x['names']} for x in p if x['kind']=='tls'])
 if tls[0]!=tls[1] or sorted((x['section'],x['size']) for x in tls[0])!=[('.rdata',20),('.tls',1),('.tls',4)]:raise ValueError('TLS kind decomposition changed')
 out={'scope':'actual archived nonoverlapping selected ranges; candidate positive only','input_sha256':{n:sha(e/n) for e,prefix in ((A,'old'),(B,'new')) for n in []},'old_dv1_sha256':sha(A/'dv1_pieces.json'),'new_dv1_sha256':sha(B/'dv1_pieces.json'),'old_m3_sha256':sha(A/'m3_manifest.json'),'new_m3_sha256':sha(B/'m3_manifest.json'),'new_620_object_sha256':sha(B/'0620.obj'),'m3_extents_identical':True,'dv1_section_totals':tot,'range_delta':delta,'tls_kind_pieces':tls[1],'tls_kind_explanation':'kind tls includes 20 bytes physically in .rdata and 5 bytes in .tls; kind and physical section are different attributes','coff_native_table':{'symbol':'??_7BGSBodyPart@@6B@','section':'.rdata','symbol_offset':4,'section_size':8,'relocations':rel},'status':'positive candidate; accepted default accounting unchanged pending controls and repeat'}
 P.write_text(json.dumps(out,indent=2));print(json.dumps({'sha256':sha(P),'delta':delta,'totals':tot}))
if __name__=='__main__':main()
