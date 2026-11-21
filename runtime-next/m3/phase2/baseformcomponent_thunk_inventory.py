"""Inventory named compiler-generated thunk changes for pinned BFC object pairs."""
import json,sys,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;sys.path[:0]=[str(M.parent.parent/'fnv_decomp/tools'),str(H)]
from compare import Coff
from tesform_typed_eh_thunk_audit import thunks
I=M/'out/phase2-bfc-core-proof-index.json';O=M/'out/phase2-bfc-core-thunk-inventory.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve evidence')
 idx=json.loads(I.read_text());out=[]
 for x in idx['units']:
  q=M/x['report'];d=q.parent;cs=[]
  for tag in ('original','candidate'):
   p=d/(tag+'.obj')
   if sha(p)!=x['objects'][tag]:raise ValueError('object changed')
   cs.append(thunks(Coff(str(p))))
  a,b=cs;changes={'changed_common':sorted(k for k in a.keys()&b.keys() if a[k]!=b[k]),'original_only':sorted(a.keys()-b.keys()),'candidate_only':sorted(b.keys()-a.keys())}
  if any(changes.values()):out.append({'unit':x['unit'],**changes})
 O.write_text(json.dumps({'index_sha256':sha(I),'scope':'named deleting-destructor and thunk-like section tails only; no global ownership or all generated data coverage','units_with_differences':out},indent=2));print('units with raw named thunk differences',len(out))
if __name__=='__main__':main()
