"""Isolated three-array/two-W-tail experiment using the private staged generator."""
import json,sys,hashlib,importlib.util
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;D=M/'out/phase2-w-arrays-expanded';sys.path.insert(0,str(M));spec=importlib.util.spec_from_file_location('staged_array_gen',D/'candidate-gen_m3.py');G=importlib.util.module_from_spec(spec);sys.modules[spec.name]=G;spec.loader.exec_module(G)
s=D/'selection.json';entries=json.loads(s.read_text(encoding='utf-8-sig'))['entries'];targets={0x11a7d40,0x11a7e40,0x11aced8,0x11acefc,0x1093b6c};selected=[e for e in entries if e['va'] in targets];assert len(selected)==5
out=D/'isolated-fixture';out.mkdir(exist_ok=False);G.GEN=str(out);G.splice.OBJ=str(out/'m3_data.obj');built=G.build_entries(selected)
for e in built:e['obj']=0
p=G.compile_one(built,0);stdout,stderr=p.communicate();(out/'compile.log').write_text(stdout+'\n'+stderr,encoding='utf-8')
if p.returncode:raise SystemExit('compiler failed: '+str(p.returncode))
bad=G.check(built)
if bad:raise SystemExit('COFF verification failed: '+repr(bad))
res={'selection_sha256':hashlib.sha256(s.read_bytes()).hexdigest(),'staged_generator_sha256':hashlib.sha256((D/'candidate-gen_m3.py').read_bytes()).hexdigest(),'entries':len(built),'bytes':sum(x['size'] for x in built),'checks':'exact expected symbols, external storage, section, reference bytes, complete original DIR32 sites and targets, no dynamic initializer','objects':[{'va':e['va'],'size':e['size'],'sym':e['sym'],'type':e['tc'],'relocation_count':len(e.get('fields',[]))} for e in built]}
(out/'result.json').write_text(json.dumps(res,indent=2)+'\n',encoding='utf-8');print('PASS',res['entries'],res['bytes'])
