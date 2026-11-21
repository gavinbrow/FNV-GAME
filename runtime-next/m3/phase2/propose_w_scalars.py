import json,re,sys,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;sys.path.insert(0,str(M));import gen_m3 as G
j=lambda p:json.load(open(p,encoding='utf-8-sig'))
baseline=M/'batch8_final_selection.json'; d=j(baseline); candidates=j(H/'w_candidates.json')['candidates']; units=j(M.parent.parent/'fnv_decomp/build/units.json')['units']; names={}
for u in units:
 for k in u.get('symbols',{}):
  for match in re.finditer(r'(?:DAT|PTR|OFF|UNK|BYTE|WORD|DWORD)_([0-9a-f]{8})',k): names.setdefault(int(match.group(1),16),set()).add(k)
cs={}; rejected=[]
for x in candidates:
 a=x['va']; sym=x['unit_symbol']; code=sym.split('@@3',1)[1][:-1];
 if names.get(a)!={sym}:rejected.append([a,'other_unit_symbol_or_alias']);continue
 if not x['scope_checks'] or not all(t['namespace_marker_before_unclosed_comment'] and t['const_matches_mangled'] for t in x['scope_checks']):rejected.append([a,'namespace_or_const_not_supported']);continue
 try:G.fmt(code,G.refbytes(a,x['size']))
 except Exception:rejected.append([a,'initializer_not_supported']);continue
 cs[a]=x
out=[]
for e in d['entries']:
 x=cs.get(e['va']);
 if x:
  code=x['unit_symbol'].split('@@3',1)[1][:-1];out.append({'va':e['va'],'tc':code,'scalar_namespace':x['namespace'],'scalar_const':x['unit_symbol'].endswith('B'),'scalar_symbol':x['unit_symbol'],'decl':[x['unit_symbol']],'align':e['align']})
 else:out.append(e)
assert len(out)==len(d['entries']);assert sum(e['va'] in cs for e in out)==len(cs)
result={'note':'Opt-in experimental W to exact scalar identity; no compiler or image verification.','base_sha256':hashlib.sha256(baseline.read_bytes()).hexdigest(),'entries':out,'candidate_count':len(cs),'candidate_bytes':sum(x['size'] for x in cs.values()),'rejected':rejected}
p=M/'out/phase2-w-scalar/selection.json';p.write_text(json.dumps(result,indent=0)+'\n');print('selected',len(cs),'bytes',result['candidate_bytes'],'rejected',len(rejected));print('sha256',hashlib.sha256(p.read_bytes()).hexdigest())
