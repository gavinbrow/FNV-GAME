"""Unify local BGSLoadFormBuffer class-key spelling without altering layout."""
import copy,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;I=M/'out/phase2-class-typed-v3';O=M/'out/phase2-class-typed-v4'
def sha(b):return hashlib.sha256(b).hexdigest()
def once(s,a,b):
 if s.count(a)!=1:raise ValueError('anchor changed '+a)
 return s.replace(a,b,1)
def main():
 meta=json.loads((I/'manifest.json').read_text());raw={n:(I/n).read_bytes() for n in meta['outputs']}
 for n,d in meta['outputs'].items():
  if sha(raw[n])!=d:raise ValueError('prior output changed '+n)
 s={n:b.decode() for n,b in raw.items()}
 for n in ('tesform_TESForm.h','bgsencounterzone_TESForm.h'):s[n]=once(s[n],'struct BGSLoadFormBuffer;','class BGSLoadFormBuffer;')
 n='bgsencounterzone.cpp';s[n]=once(s[n],'struct BGSLoadFormBuffer\n{\n    virtual unsigned char GetVersion();','class BGSLoadFormBuffer\n{\n  public:\n    virtual unsigned char GetVersion();')
 tm=copy.deepcopy(json.loads((I/'tesform-manifest.json').read_text()));bm=copy.deepcopy(json.loads((I/'bgs-manifest.json').read_text()))
 for m in (tm,bm):
  for x in m['proposed_function_symbol_changes']:x['after']=x['after'].replace('PAUBGSLoadFormBuffer@@','PAVBGSLoadFormBuffer@@')
 aliases=copy.deepcopy(meta['base_external_symbol_aliases'])
 for x in aliases:x['after']=x['after'].replace('PAUBGSLoadFormBuffer@@','PAVBGSLoadFormBuffer@@')
 O.mkdir(exist_ok=False);outputs={}
 for n,text in s.items():
  b=text.encode();(O/n).write_bytes(b);outputs[n]=sha(b)
 (O/'tesform-manifest.json').write_text(json.dumps(tm,indent=2));(O/'bgs-manifest.json').write_text(json.dumps(bm,indent=2));(O/'manifest.json').write_text(json.dumps({'inputs':{n:sha(b) for n,b in raw.items()},'outputs':outputs,'base_external_symbol_aliases':aliases,'scope':'unify class-key spelling only; namespace-local load-buffer surrogate remains distinct','status':'uncompiled; require exact all-function, reference, graph and EH/thunk checks'},indent=2));print(json.dumps(outputs))
if __name__=='__main__':main()
