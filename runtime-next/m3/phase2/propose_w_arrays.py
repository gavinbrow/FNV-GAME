"""Produce an opt-in selection from the reviewed array and scalar proposals."""
import json,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;S=M/'out/phase2-w-scalar/selection.json';A=H/'w_array_candidates.json';base=json.loads(S.read_text(encoding='utf-8-sig'));rows=json.loads(A.read_text(encoding='utf-8-sig'))['entries']; by={x['va']:x for x in rows};out=[]
for e in base['entries']:
 x=by.get(e['va'])
 if x:
  assert e['tc']=='W' and e['size']==x['size']==256 and e['ns']==x['namespace'] and e['decl']==[x['symbol']]
  out.append({'va':e['va'],'tc':'A','et':'E','size':256,'align':4,'array_namespace':x['namespace'],'array_const':False,'array_symbol':x['symbol'],'decl':[x['symbol']]})
 else:out.append(e)
assert len(out)==len(base['entries']) and sum('array_symbol' in x for x in out)==9
p=M/'out/phase2-w-arrays/selection.json';p.parent.mkdir(parents=True,exist_ok=True)
result={'note':'Opt-in source-supported 22 scalars + nine arrays; no coverage change; full integration pending.','base_sha256':hashlib.sha256(S.read_bytes()).hexdigest(),'array_count':9,'array_bytes':2304,'entries':out}
p.write_text(json.dumps(result,indent=0)+'\n',encoding='utf-8');print('sha256',hashlib.sha256(p.read_bytes()).hexdigest())
