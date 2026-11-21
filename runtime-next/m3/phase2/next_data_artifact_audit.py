"""Read-only audit of one archived next-data build; no build or game launch."""
import argparse,collections,hashlib,json,pickle,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp'
sys.path[:0]=[str(F/'tools'),str(M),str(RN/'data-v1'),str(RN/'data-v2'),str(RN/'data-v3'),str(RN)]
from compare import Coff
import gen_m3 as G,place
TYPES={'H':4,'I':4,'M':4,'N':8,'J':4,'K':4,'F':2,'G':2,'D':1,'E':1,'_N':1,'C':1,'P':4}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def union(rows):
 out=[]
 for a,b in sorted(rows):
  if out and a<out[-1][1]:raise ValueError('overlap at '+hex(a))
  if out and a==out[-1][1]:out[-1]=(out[-1][0],b)
  else:out.append((a,b))
 return out
def pe_sections(p):
 b=p.read_bytes();off=struct.unpack_from('<I',b,0x3c)[0]
 if b[:2]!=b'MZ' or b[off:off+4]!=b'PE\0\0':raise ValueError('not PE')
 machine,count,_,_,_,opt,_=struct.unpack_from('<HHIIIHH',b,off+4);o=off+24
 if machine!=0x14c or struct.unpack_from('<H',b,o)[0]!=0x10b:raise ValueError('not x86 PE32')
 base=struct.unpack_from('<I',b,o+28)[0];sections={}
 for i in range(count):
  z=struct.unpack_from('<8sIIIIIIHHI',b,o+opt+40*i);name=z[0].split(b'\0')[0].decode();sections[name]={'va':base+z[2],'raw':z[3],'offset':z[4]}
 return b,base,sections
def main():
 p=argparse.ArgumentParser();p.add_argument('--evidence',type=Path,required=True);p.add_argument('--exe',type=Path,required=True);p.add_argument('--chunks',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();e=a.evidence
 if a.out.exists():raise FileExistsError(a.out)
 if sha(Path(G.__file__))!='0ae6999c180682514c7f44d43a694ed25adf8029979de2c78bcaf78f5c12b241':raise ValueError('current reference-reading generator differs from reviewed tooling')
 sel=load(e/'selection.json')['entries'];manifest=load(e/'m3_manifest.json')['entries'];log=load(e/'m3_gen.log.json');pieces=load(e/'dv1_pieces.json')['pieces'];library=load(e/'library_candidates.json')['candidates'];summary=load(a.summary)
 if sha(e/'selection.json')!='a0a8e8d2c9818f777f6e07ae18b5cc7d55ff94ca0bd6ccd952ff98ab836d9c3a' or sha(e/'library_candidates.json')!='74e3815454a8926ee3d8f70abf939e8d61eadd7173a7514c93e66fee92589700':raise ValueError('selection mismatch')
 if len(sel)!=8268 or len(manifest)!=len(sel) or log['kept']!=8268 or log['dropped']:raise ValueError('M3 kept/drop mismatch')
 def selspan(x):return x['va'],x['va']+(TYPES[x['tc']] if x['tc'] in TYPES else x['size'])
 if sorted(selspan(x) for x in sel)!=sorted((x['va'],x['va']+x['size']) for x in manifest):raise ValueError('selection/manifest ranges differ')
 old=load(M/'out/phase2-flags-script-positive/evidence/selection.json')['entries']
 if union(map(selspan,sel))!=union(map(selspan,old)):raise ValueError('M3 union changed')
 ranges=[(x['va'],x['va']+x['size'],x['section'],'M3') for x in manifest]+[(x['va'],x['va']+x['size'],x['section'],'DV1') for x in pieces];union((x[0],x[1]) for x in ranges)
 raw=[x for x in ranges if x[2] in ('.data','.rdata')];coverage=sum(b-a for a,b,_,_ in raw);tls=sum(b-a for a,b,s,_ in ranges if s=='.tls');values=collections.Counter()
 for lo,hi,section,owner in raw:
  ref=G.refbytes(lo,hi-lo);values[owner+'_zero']+=ref.count(0);values[owner+'_nonzero']+=len(ref)-ref.count(0)
 statepath=e/'data-v1-scratch/dv1_placed.pkl';expected=summary['provenance']['data_v1_scratch_sha256']['dv1_placed.pkl']
 if sha(statepath)!=expected:raise ValueError('placement snapshot differs')
 st=pickle.loads(statepath.read_bytes());objs={};heads=[];expected_heads={x['va']:x for x in sel if x['tc'] in ('Q','V','Y')}
 if len(expected_heads)!=4:raise ValueError('unexpected typed heads')
 targetvas=set(expected_heads)|{18521148,17610304,18384864}
 for va in sorted(targetvas):
  matches=[x for x in manifest if x['va']==va]
  if len(matches)!=1:raise ValueError('missing unique typed head/tail '+hex(va))
  x=matches[0];number=x.get('obj',0);obj=e/('m3_data.obj' if number==0 else 'm3_data_%d.obj'%number)
  if number not in objs:objs[number]=Coff(str(obj))
  c=objs[number];sym=c.named(x['sym']);sec=c.sections[sym['section']];start=sym['value'];size=x['size'];data=sec['data'][start:start+size]
  if sym['storage']!=2 or sec['name']!=x['section'] or len(data)!=size:raise ValueError('COFF symbol/section mismatch')
  if va in expected_heads and x['sym']!=expected_heads[va]['class_symbol']:raise ValueError('native decorated symbol mismatch')
  rel=[(off-start,c.symbols[idx]['name'],kind) for off,idx,kind in sec['relocs'] if start<=off<start+size]
  original=sorted(v-va for v in G.ORIG_SET if va<=v<va+size)
  if sorted(r[0] for r in rel)!=original or any(r[2]!=6 for r in rel):raise ValueError('original relocation sites differ')
  ref=G.refbytes(va,size)
  if any(data[i]!=ref[i] for i in range(size) if not any(o<=i<o+4 for o,_,_ in rel)):raise ValueError('COFF nonrelocated bytes differ')
  if va in expected_heads and expected_heads[va]['tc']=='V' and (((sec['flags']>>20)&15)<5 or start%16):raise ValueError('COFF 16-alignment failed')
  pseudo=[z for z in st.SEC.values() if 200000 in z['units'] and z.get('forced')==va]
  if len(pseudo)!=1 or pseudo[0]['size']!=size or (va in expected_heads and expected_heads[va]['tc']=='V' and ((pseudo[0]['flags']>>20)&15)!=5):raise ValueError('pseudo-unit mismatch')
  for r in pseudo[0]['relocs']:
   target=struct.unpack('<I',G.refbytes(va+r[0],4))[0]
   if r[7]!='m3' or r[8]!=target:raise ValueError('pseudo-unit relocation target differs')
  heads.append({'va':hex(va),'size':size,'symbol':x['sym'],'object':obj.name,'relocations':len(rel),'coff_alignment_code':(sec['flags']>>20)&15,'pseudo_alignment_code':(pseudo[0]['flags']>>20)&15})
 # Reconstruct default rdata chunk translation: make_image reverses chunk order and preserves va mod16.
 chunks=load(a.chunks);byname={x['file']:x for x in chunks};order=['rdata_03','rdata_02','rdata_01','rdata_00'];offsets={};pos=0
 for n in order:
  ch=byname[n];pos+=(ch['va']-pos)%16;offsets[n]=pos;pos+=ch['size']
 image,base,sections=pe_sections(a.exe);alignments=[]
 for va in (0x10cb620,0x10cb630):
  matches=[byname[n] for n in order if byname[n]['va']<=va and va+16<=byname[n]['va']+byname[n]['size']]
  if len(matches)!=1:raise ValueError('SIMD chunk ambiguous')
  ch=matches[0];newva=sections['.rdata']['va']+offsets[ch['file']]+va-ch['va'];fo=sections['.rdata']['offset']+newva-sections['.rdata']['va']
  if newva%16 or image[fo:fo+16]!=G.refbytes(va,16):raise ValueError('translated PE SIMD alignment/bytes mismatch')
  alignments.append({'source_va':hex(va),'chunk':ch['file'],'final_va':hex(newva),'pe_file_offset':hex(fo),'aligned16':True})
 if len(library)!=405 or sum(x['size'] for x in library)!=16730:raise ValueError('library selection mismatch')
 for x in library:
  hit=[y for y in pieces if (y['va'],y['size'],y['unit'])==(x['va'],x['size'],x['unit']) and y.get('library_opt_in')]
  if len(hit)!=1 or hashlib.sha256(bytes.fromhex(hit[0]['data'])).hexdigest()!=x['compiler_bytes_sha256']:raise ValueError('library piece ownership mismatch')
 out={'status':'archived range/COFF/PE audit; archive section identity separately requires staged library hook dry run','selection_sha256':sha(e/'selection.json'),'library_sha256':sha(e/'library_candidates.json'),'exe_sha256':sha(a.exe),'chunks_sha256':sha(a.chunks),'placed_sha256':sha(statepath),'m3_entries':len(manifest),'dv1_pieces':len(pieces),'raw_data_rdata_bytes':coverage,'reference_value_counts':dict(values),'tls_bytes_separate':tls,'typed_heads_and_tails':heads,'simd_translated':alignments,'library_pieces':len(library),'library_bytes':sum(x['size'] for x in library),'limitations':['data-v1 range metadata is not alone proof of final-image ownership','layout reconstruction assumes default reverse-rdata layout; verify saved run arguments','typed source views do not prove unresolved native pointer semantics']}
 a.out.write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps({'coverage':coverage,'tls':tls,'heads_tails':len(heads),'translated':alignments,'out':str(a.out)}))
if __name__=='__main__':main()
