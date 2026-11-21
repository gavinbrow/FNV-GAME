"""Private NiPoint3 aggregate + preserved W-tail compiler/COFF fixture."""
import json,sys,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;sys.path.insert(0,str(M));import gen_m3 as G
from compare import Coff
q=json.load(open(H/'point3_candidate.json'));head=q['head'];out=M/'out/phase2-point3/isolated-fixture';out.mkdir(parents=True,exist_ok=False);G.GEN=str(out);G.splice.OBJ=str(out/'m3_data.obj');tail=G.build_entries([q['tail']]);tail[0]['obj']=0
raw=G.refbytes(head['va'],12);floats=[G.fmt('M',raw[i:i+4]) for i in range(0,12,4)];base_cpp=G.cpp
def cpp(es):
 return 'namespace fnv_005c25f0 { class NiPoint3 { public: float x,y,z; }; NiPoint3 DAT_011a9c30 = {'+','.join(floats)+'}; }\n'+base_cpp(es)
G.cpp=cpp;p=G.compile_one(tail,0);stdout,stderr=p.communicate();(out/'compile.log').write_text(stdout+'\n'+stderr,encoding='utf-8')
if p.returncode:raise SystemExit('compiler failure '+str(p.returncode))
bad=G.check(tail)
if bad:raise SystemExit('W tail check failed '+repr(bad))
entry={'sym':head['symbol'],'name':'DAT_011a9c30','va':head['va'],'size':12,'section':'.data'};data,rel,sec,flags,storage=G.splice.slice_entry(Coff(G.obj_path(0)),entry)
if data!=raw or rel or sec!='.data' or storage!=2:raise SystemExit('head check failed')
result={'head':head,'tail_va':q['tail']['va'],'tail_size':q['tail']['size'],'tail_relocations':len(tail[0]['fields']),'checked':'head exact symbol/storage/section/reference/no reloc; W tail reference bytes and original DIR32 offsets/targets; no dynamic initializer'}
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print('PASS head 12 tail 252 relocations',result['tail_relocations'])
