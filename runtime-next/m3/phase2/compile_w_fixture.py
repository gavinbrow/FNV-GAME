"""Isolated opt-in scalar fixture. Writes only to a newly created private directory."""
import sys,json,hashlib
from pathlib import Path
M=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(M));import gen_m3 as G
sel=M/'out/phase2-w-scalar/selection.json';obj=json.load(open(sel,encoding='utf-8-sig')); picked=[r for r in obj['entries'] if 'scalar_symbol' in r]
assert len(picked)==obj['candidate_count']==22
out=M/'out/phase2-w-scalar/isolated-fixture';out.mkdir(exist_ok=False)
G.GEN=str(out);G.splice.OBJ=str(out/'m3_data.obj')
entries=G.build_entries(picked)
for e in entries:e['obj']=0
p=G.compile_one(entries,0);stdout,stderr=p.communicate()
(out/'compile.log').write_text(stdout+'\n'+stderr,encoding='utf-8')
if p.returncode:raise SystemExit('compiler failed: '+str(p.returncode))
bad=G.check(entries)
if bad:raise SystemExit('COFF verification failed: '+repr(bad))
result={'selection_sha256':hashlib.sha256(sel.read_bytes()).hexdigest(),'count':len(entries),'bytes':sum(e['size'] for e in entries),'verified':'exact symbol, external storage, section, reference bytes, no relocations or dynamic initializer','objects':[{'va':e['va'],'sym':e['sym'],'size':e['size'],'section':e['section']} for e in entries]}
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print('PASS',len(entries),result['bytes'])
