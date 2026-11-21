"""Private VC2008 fixture for actual 16-byte aligned source-view SIMD objects."""
import json,sys,importlib.util,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;D=M/'out/phase2-align16';sys.path.insert(0,str(M))
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod
splice=load('splice',D/'candidate-splice.py');G=load('simd_proposal',D/'candidate-gen_m3.py')
if G.ANYNEG:raise ValueError('positive fixture rejects inherited negative-control mode')
stage=load('staged_m3secs',D/'candidate-m3secs.py');q=json.load(open(H/'simd_candidates.json'));out=D/'isolated-fixture';out.mkdir(exist_ok=False);G.GEN=str(out);splice.OBJ=str(out/'m3_data.obj');splice.MANIFEST=str(out/'m3_manifest.json')
selection=json.loads((D/'selection.json').read_text())['entries'];head=G.build_entries([e for e in selection if e['tc']=='V']);tail=G.build_entries([q['tail']]);es=head+tail
assert len(head)==2 and {e['va'] for e in head}=={x['va'] for x in q['entries']}
for e in es:e['obj']=0
p=G.compile_one(es,0);stdout,stderr=p.communicate();(out/'compile.log').write_text(stdout+'\n'+stderr,encoding='utf-8')
if p.returncode:raise SystemExit('compiler failure '+str(p.returncode))
bad=G.check(head+tail)
if bad:raise SystemExit('COFF verification failure '+repr(bad))
manifest={'entries':[dict(e) for e in head]+[{k:v for k,v in e.items() if k!='items'} for e in tail],'objs':[0]};Path(splice.MANIFEST).write_text(json.dumps(manifest),encoding='utf-8')
loaded=splice.load();units=stage.m3_units()[stage.UID]['secs'];assert len(loaded)==3 and len(units)==3
for obj in units:
 if obj['forced'] in (0x10cb620,0x10cb630):assert obj['flags']&0x00f00000==0x00500000
result={'staged_generator_sha256':hashlib.sha256((D/'candidate-gen_m3.py').read_bytes()).hexdigest(),'selection_sha256':hashlib.sha256((D/'selection.json').read_bytes()).hexdigest(),'head_count':2,'head_bytes':32,'tail_bytes':4,'tail_relocations':len(tail[0]['fields']),'checks':'actual candidate generator; exact native COFF symbols, file-backed bytes, COFF section+symbol 16-alignment, original 16-aligned destination, m3secs 16-byte flags, tail relocation, no dynamic init','staged_splice_sha256':hashlib.sha256((D/'candidate-splice.py').read_bytes()).hexdigest(),'staged_m3secs_sha256':hashlib.sha256((D/'candidate-m3secs.py').read_bytes()).hexdigest()};(out/'result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print('PASS',result['checks'])
