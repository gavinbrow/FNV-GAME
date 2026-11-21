import sys,json,importlib.util,hashlib,collections
from pathlib import Path
M=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(M));import gen_m3 as g
spec=importlib.util.spec_from_file_location('baseline_arrays',M/'out/phase2-w-arrays/baseline-gen_m3.py');b=importlib.util.module_from_spec(spec);sys.modules[spec.name]=b;spec.loader.exec_module(b)
def outputs(mod,selection):
 entries=mod.build_entries(selection);mod.partition(entries);groups=collections.defaultdict(list)
 for e in entries:groups[e.get('obj',0)].append(e)
 return {k:hashlib.sha256(mod.cpp(v).encode()).hexdigest() for k,v in groups.items()}
for f in ('batch8_final_selection.json','out/phase2-w-scalar/selection.json'):
 s=json.load(open(M/f,encoding='utf-8-sig'))['entries'];a=outputs(b,s);z=outputs(g,s)
 if a!=z:raise SystemExit('legacy output changed: '+f)
 print(f,'unchanged',a,flush=True)
