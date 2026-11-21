import sys,json,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;sys.path.insert(0,str(M));import gen_m3 as G
base=M/'out/phase2-w-arrays/selection.json';src=json.loads(base.read_text(encoding='utf-8-sig'));p=json.load(open(H/'array_split_candidates.json'));by={x['va']:x for x in p['array_candidates']};out=[]
for e in src['entries']:
 q=by.get(e['va'])
 if not q:out.append(e);continue
 assert e['tc']=='W' and e['size']==q['original_w_size']
 out.append({'va':e['va'],'tc':'A','et':q['element_type_code'],'size':q['size'],'align':e['align'],'array_namespace':q['namespace'],'array_const':False,'array_symbol':q['symbol'],'decl':[q['symbol']]})
 if q['tail_size']:
  raw=G.refbytes(e['va'],e['size']);items=G.g_items(e['va'],raw,e['runs']);first=0
  while first<len(e['runs']) and sum(G.RUN_SZ[k]*n for k,n in e['runs'][:first])<q['size']:first+=1
  titems=G.g_items(q['tail_va'],raw[q['size']:],q['tail_runs']);assert items[first:]==titems
  out.append({'va':q['tail_va'],'tc':'W','size':q['tail_size'],'kind':'tail-m3','ns':'','named':False,'head':None,'runs':q['tail_runs'],'align':4})
assert len(out)==len(src['entries'])+2
p=M/'out/phase2-w-arrays-expanded/selection.json';r={'note':'Experimental 22 scalars, 12 bounded arrays and two identity-preserving W tail splits; no coverage change.','base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'array_count':12,'array_bytes':2612,'entries':out};p.write_text(json.dumps(r,indent=0)+'\n',encoding='utf-8');print('sha256',hashlib.sha256(p.read_bytes()).hexdigest(),'entries',len(out))
