"""Private compiler fixture for the staged source-view Cost245 emitter."""
import json,sys,hashlib,importlib.util
from pathlib import Path
M=Path(__file__).resolve().parent.parent;D=M/'out/phase2-cost245-proposal';sys.path.insert(0,str(M))
# Exercise the staged helper without changing the accepted build's helper.
helper=D/'candidate-cost245_records.py';live=M/'phase2/cost245_records.py';live_before=live.read_bytes()
hp=importlib.util.spec_from_file_location('cost245_records',helper);C=importlib.util.module_from_spec(hp);sys.modules[hp.name]=C;hp.loader.exec_module(C)
sp=importlib.util.spec_from_file_location('cost_proposal',D/'candidate-gen_m3.py');G=importlib.util.module_from_spec(sp);sys.modules[sp.name]=G;sp.loader.exec_module(G)
if G.ANYNEG:raise ValueError('positive fixture rejects inherited negative-control mode')
p=D/'selection.json';rows=json.load(open(p))['entries'];sel=[e for e in rows if e['va'] in (0x11886a0,0x11887e0)];assert len(sel)==2
out=D/'isolated-fixture';out.mkdir(exist_ok=False);G.GEN=str(out);G.splice.OBJ=str(out/'m3_data.obj');es=G.build_entries(sel)
for e in es:e['obj']=0
proc=G.compile_one(es,0);stdout,stderr=proc.communicate();(out/'compile.log').write_text(stdout+'\n'+stderr,encoding='utf-8')
if proc.returncode:raise SystemExit('compiler failed '+str(proc.returncode))
bad=G.check(es)
if bad:raise SystemExit('COFF mismatch '+repr(bad))
assert sys.modules['cost245_records'] is C and live.read_bytes()==live_before
res={'helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),'live_helper_unchanged':True,'selection_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256((D/'candidate-gen_m3.py').read_bytes()).hexdigest(),'entries':len(es),'bytes':sum(e['size'] for e in es),'relocations':sum(len(e.get('fields',[])) for e in es),'checks':'exact symbols, external storage, sections, reference bytes, relocation sites/targets, no dynamic initializer'};(out/'result.json').write_text(json.dumps(res,indent=2)+'\n',encoding='utf-8');print('PASS',res['entries'],res['bytes'],res['relocations'])
