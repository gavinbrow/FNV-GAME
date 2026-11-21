"""Private source-view Cost245 array and retained W-tail feasibility fixture."""
import json,sys,struct
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;sys.path.insert(0,str(M));import gen_m3 as G
q=json.load(open(H/'cost245_candidate.json'));head=q['head'];a=head['va'];raw=G.refbytes(a,head['size']);sites=set(G.ORIG_SITES);ext={};rows=[]
for i in range(16):
 off=i*20; cells=['true' if raw[off] else 'false']
 for j in range(1,5):
  p=off+j*4;b=raw[p:p+4]
  if a+p in sites:
   v=struct.unpack('<I',b)[0];code=G.TLO<=v<G.THI;kind='M3F' if code else 'M3D';ext[v]=('extern "C" void %s_%08x(void);' if code else 'extern "C" char %s_%08x;')%(kind,v);cells.append('(int)&%s_%08x'%(kind,v))
  else:cells.append(G.fmt('I',b))
 rows.append('{%s}'%', '.join(cells))
head_e={'va':a,'size':320,'sym':head['symbol'],'name':'DAT_011886a0','section':'.data','tc':'X','ref':raw.hex(),'obj':0};tail=G.build_entries([q['tail']]);tail[0]['obj']=0
out=M/'out/phase2-cost245/isolated-fixture';out.mkdir(parents=True,exist_ok=False);G.GEN=str(out);G.splice.OBJ=str(out/'m3_data.obj');base=G.cpp
def cpp(es):
 return '#include <stddef.h>\n'+'\n'.join(ext[k] for k in sorted(ext))+'\nnamespace fnv_004a8bb0 { struct Cost245 { bool disabled; int unk04,unk08,unk0c,unk10; }; typedef char SizeCheck[(sizeof(Cost245)==20 && offsetof(Cost245,disabled)==0 && offsetof(Cost245,unk04)==4 && offsetof(Cost245,unk08)==8 && offsetof(Cost245,unk0c)==12 && offsetof(Cost245,unk10)==16)?1:-1]; Cost245 DAT_011886a0[16] = {\n'+',\n'.join(rows)+'\n}; }\n'+base(es)
G.cpp=cpp;p=G.compile_one(tail,0);stdout,stderr=p.communicate();(out/'compile.log').write_text(stdout+'\n'+stderr,encoding='utf-8')
if p.returncode:raise SystemExit('compiler failure '+str(p.returncode))
bad=G.check([head_e]+tail)
if bad:raise SystemExit('COFF verification failure '+repr(bad))
result={'head_va':a,'head_size':320,'head_symbol':head['symbol'],'head_relocations':len(head['relocation_offsets']),'tail_va':q['tail']['va'],'tail_size':64,'tail_relocations':len(q['tail_relocation_offsets']),'checks':'exact symbol/storage/section/reference, original DIR32 sites/targets, no dynamic initializer'}
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print('PASS 320-byte aggregate + 64-byte W tail, relocations',result['head_relocations'],result['tail_relocations'])
