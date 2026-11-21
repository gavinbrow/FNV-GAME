import sys,json,importlib.util,hashlib,collections
from pathlib import Path
M=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(M));import gen_m3 as g
spec=importlib.util.spec_from_file_location('baseline_g',M/'out/phase2-w-scalar/baseline-gen_m3.py');b=importlib.util.module_from_spec(spec);sys.modules[spec.name]=b;spec.loader.exec_module(b)
s=json.load(open(M/'batch8_final_selection.json'))['entries']
def outputs(mod,selection):
 entries=mod.build_entries(selection);mod.partition(entries);groups=collections.defaultdict(list)
 for e in entries:groups[e.get('obj',0)].append(e)
 return {k:hashlib.sha256(mod.cpp(v).encode()).hexdigest() for k,v in groups.items()}
a=outputs(b,s);z=outputs(g,s);assert a==z;print('Legacy outputs identical',a,flush=True)
t=json.load(open(M/'out/phase2-w-scalar/selection.json'))['entries'];x=outputs(g,t);print('Candidate emitted',x,flush=True)
