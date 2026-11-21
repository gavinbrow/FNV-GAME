"""Opt-in isolated 9-array compiler fixture. No shared generator output is written."""
import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;sys.path.insert(0,str(M));import gen_m3 as G
rows=json.load(open(H/'w_array_candidates.json',encoding='utf-8-sig'))['entries'];assert len(rows)==9
out=M/'out/phase2-w-arrays/isolated-fixture';out.mkdir(parents=True,exist_ok=False);G.GEN=str(out);G.splice.OBJ=str(out/'m3_data.obj')
entries=G.build_entries([dict(va=x['va'],tc='A',et='E',size=256) for x in rows]);
for e,x in zip(entries,rows):e.update(sym=x['symbol'],obj=0)
def cpp(es):
 return 'namespace sa238a0 {\n'+'\n'.join('unsigned char %s[256] = %s;'%(e['name'],e['init']) for e in es)+'\n}\n'
G.cpp=cpp
p=G.compile_one(entries,0);o,err=p.communicate();(out/'compile.log').write_text(o+'\n'+err,encoding='utf-8')
if p.returncode:raise SystemExit('compiler failure '+str(p.returncode))
bad=G.check(entries)
if bad:raise SystemExit('COFF verification failure '+repr(bad))
result={'count':len(entries),'bytes':sum(e['size'] for e in entries),'checks':'expected native symbol, external storage, section, exact reference bytes, no relocations or dynamic initializers','objects':[{'va':e['va'],'sym':e['sym'],'size':e['size'],'section':e['section']} for e in entries]}
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print('PASS',result['count'],result['bytes'])
