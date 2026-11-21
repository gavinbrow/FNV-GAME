"""Private object-level EH and emitted destructor/thunk inventory."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;sys.path[:0]=[str(P/'fnv_decomp/tools'),str(H)]
from compare import Coff
from rtti_mirror_compare import exception_sections
O=M/'out/phase2-typed-eh-thunk-audit.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def thunks(c):
 result={}
 for name,items in c.by_name.items():
  if not (name.startswith(('??_E','??_G')) or 'adjustor' in name.lower() or 'thunk' in name.lower()):continue
  syms=[x for x in items if x['section']>0]
  if len(syms)!=1:continue
  x=syms[0];sec=c.sections[x['section']];tail=sec['data'][x['value']:];rel=[(o-x['value'],k,c.symbols[i]['name']) for o,i,k in sec['relocs'] if o>=x['value']]
  result[name]={'tail_sha256':hashlib.sha256(tail).hexdigest(),'tail_size':len(tail),'relocations':rel}
 return result

def main():
 if O.exists():raise FileExistsError('refusing overwrite')
 report={}
 for label,name in [('tesform','phase2-tesform-typed-mirror'),('bgse','phase2-bgs-typed-mirror')]:
  d=M/'out'/name;c=json.loads((d/'compile-result.json').read_text());rows={x['tag']:x for x in c['outcomes']};objs={}
  for tag in ('original','candidate'):
   p=d/(tag+'.obj')
   if rows[tag]['rc'] or not rows[tag]['trace_valid'] or sha(p)!=rows[tag]['object_sha256']:raise ValueError('object evidence mismatch')
   objs[tag]=Coff(str(p))
  ea,eb=exception_sections(objs['original']),exception_sections(objs['candidate']);ta,tb=thunks(objs['original']),thunks(objs['candidate'])
  report[label]={'object_sha256':{k:sha(d/(k+'.obj')) for k in objs},'eh':{'original_count':len(ea),'candidate_count':len(eb),'common_exact':sorted(k for k in ea.keys()&eb.keys() if ea[k]==eb[k]),'changed_common':sorted(k for k in ea.keys()&eb.keys() if ea[k]!=eb[k]),'original_only':sorted(ea.keys()-eb.keys()),'candidate_only':sorted(eb.keys()-ea.keys())},'thunks':{'original_count':len(ta),'candidate_count':len(tb),'common_exact':sorted(k for k in ta.keys()&tb.keys() if ta[k]==tb[k]),'changed_common':sorted(k for k in ta.keys()&tb.keys() if ta[k]!=tb[k]),'original_only':sorted(ta.keys()-tb.keys()),'candidate_only':sorted(tb.keys()-ta.keys())}}
 O.write_text(json.dumps({'scope':'COFF named EH/destructor/thunk section-tail inventory only; no global placement, extent or ODR claim','units':report},indent=2));print(json.dumps({k:{'eh_exact':len(v['eh']['common_exact']),'eh_changed':len(v['eh']['changed_common']),'thunk_exact':len(v['thunks']['common_exact']),'thunk_changed':len(v['thunks']['changed_common']),'thunk_removed':v['thunks']['original_only']} for k,v in report.items()}))
if __name__=='__main__':main()
