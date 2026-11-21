"""Inventory actual archived mapped-function rel32 calls to two NiRef source views."""
import json,hashlib,sys
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;sys.path.insert(0,str(R/'fnv_decomp/tools'));from compare import Coff
O=M/'out';A=O/'phase2-nimem-operators-825d-production-archive';B=O/'phase2-nimem-kind-production-archive';D=O/'phase2-niref-primary-inline-fixture';OUT=D/'archived-physical-owner-callers.json';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();j=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 if OUT.exists():raise FileExistsError(OUT)
 if h(A/'manifest.json')!='25e303cfcef7555e59437901586e1085cec1df91b6487d9acb1bee6e12a30bdc' or h(B/'manifest.json')!='62a67ba7b952e0b04f52c019652e035214dee8ffb425daedfbbf099ebf0967e5':raise ValueError('archive manifest differs')
 a={x['unit']:x for x in j(A/'manifest.json')['objects']};b={x['unit']:x for x in j(B/'manifest.json')['objects']};r825=j(O/'phase2-source-integration6757-transaction-v2/0.candidate')['units'];r675=j(O/'phase2-source-integration6757-transaction-v2/0.original')['units'];calendar=j(O/'phase2-nimem-calendar-binding-v1/units.generated')['units'];targets={'0x00a5d3d0','0x00496910'}
 aliases=[{'unit':i,'name':k,'target':v} for i,u in enumerate(calendar) for k,v in u.get('symbols',{}).items() if v.lower() in targets];ids=sorted({x['unit'] for x in aliases});hits=[];missing=[];errors=[]
 for i in ids:
  directory,entry,recipe=(A,a[i],r825) if i in a else (B,b[i],r675) if i in b else (None,None,None)
  if directory is None:missing.append(i);continue
  path=directory/('%04d.obj'%i)
  if h(path)!=entry['sha256']:raise ValueError('archive object changed')
  u=recipe[i];co=Coff(str(path));alias={k:v for k,v in u['symbols'].items() if v.lower() in targets};mapped=[]
  for f in u['functions']:
   try:
    z=co.named(f['symbol']);s=co.sections[z['section']];start=z['value'];end=start+f['size']
    if end>len(s['data']):raise ValueError('function extent')
    for off,k,kind in s['relocs']:
     symbol=co.symbols[k]['name']
     if start<=off and off+4<=end and kind==20 and symbol in alias:
      mapped.append({'caller':f['address'],'function':f['symbol'],'offset':off-start,'opcode':hex(s['data'][off-1]) if off>start else None,'symbol':symbol,'target':alias[symbol]})
   except (ValueError,KeyError,IndexError) as e:errors.append({'unit':i,'function':f['address'],'error':str(e)})
  if mapped:hits.append({'unit':i,'source':u['source'],'archive':'825d' if directory==A else '6757','object_sha256':h(path),'calls':mapped})
 out={'scope':'physical archived objects and recipe-mapped REL32 fields; mapping is a source-view lead, not global identity','calendar_recipe_sha256':h(O/'phase2-nimem-calendar-binding-v1/units.generated'),'archive_manifests':{'825d':h(A/'manifest.json'),'6757':h(B/'manifest.json')},'recipe_aliases':aliases,'archived_units_with_calls':hits,'unarchived_unit_ids':missing,'object_inspection_errors':errors,'limitations':['mapped target aliases are per-unit recipe metadata, not independent native identities','archived call relocations are not the live final link namespace','object inspection errors and unarchived units make this a bounded inventory','no final provider or ODR claim']}
 OUT.write_text(json.dumps(out,indent=2));print(json.dumps({'sha256':h(OUT),'alias_units':len(ids),'hit_units':len(hits),'fields':sum(len(x['calls']) for x in hits),'unarchived':missing,'errors':len(errors)}))
if __name__=='__main__':main()
