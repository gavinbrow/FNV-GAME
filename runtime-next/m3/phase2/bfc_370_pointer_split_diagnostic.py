"""Reconcile scoped names and source-grounded literals; use unchanged EH oracle."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out/phase2-bfc-370-pointer-split-mirror';P=M/'out/phase2-bfc-370-pointer-split';B=M/'out/phase2-baseformcomponent-core';I=M/'out/phase2-bfc-core-proof-index.json'
sys.path[:0]=[str(F/'tools'),str(H),str(RN)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
from build_and_match import eh_sections,recipe_names
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=O/'diagnostic-proof.json'
 if out.exists():raise FileExistsError(out)
 index=json.loads(I.read_text());m=json.loads((O/'mirror-manifest.json').read_text());run=json.loads((O/'compile-result.json').read_text());unitsfile=F/'build/units.json'
 if sha(unitsfile)!='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c':raise ValueError('recipe changed')
 z=next(x for x in index['units'] if x['unit']==370);prod=O/'production-baseline.obj'
 if sha(prod)!=z['production_object_sha256'] or sha(prod)!=m['production_object_sha256']:raise ValueError('production object changed')
 ev=B/'local-string-evidence-v3.json';key=str(ev.relative_to(M)).replace('\\','/')
 if sha(ev)!=index['pinned_inputs'][key] or json.loads(ev.read_text())['source_derived_local_bindings']['370'].get('$SG58544')!='0x010898c0':raise ValueError('local literal evidence changed')
 objects={'production':Coff(str(prod))}
 for r in run['outcomes']:
  p=O/(r['tag']+'.obj')
  if r['rc'] or not r['trace_valid'] or sha(p)!=r['object_sha256']:raise ValueError('invalid mirror')
  objects[r['tag']]=Coff(str(p))
 if set(objects)!={'production','original','candidate'}:raise ValueError('objects missing')
 units=json.loads(unitsfile.read_bytes())['units'];u=copy.deepcopy(units[370]);candidate=json.loads((P/'unit-overlay.json').read_text())
 if sha(P/'unit-overlay.json')!=m['unit_overlay_sha256'] or len(u['functions'])!=178:raise ValueError('candidate recipe changed')
 pool=[]
 for label,name in (('production','$SG27267'),('original','$SG27267'),('candidate','$SG27297')):
  c=objects[label];s=c.named(name);section=c.sections[s['section']]
  if section['name']!='.rdata' or section['relocs']:raise ValueError('literal pool unexpected')
  pool.append({'object':label,'symbol':name,'offset':s['value'],'size':len(section['data']),'sha256':hashlib.sha256(section['data']).hexdigest()})
 if len({(x['offset'],x['size'],x['sha256']) for x in pool})!=1 or u['symbols'].get('$SG27267')!='0x01088220':raise ValueError('literal pool identity not proven')
 norm={'??0PtrA96@@QAE@H@Z':'??0FUN_00528cb0@@QAE@H@Z','??0PtrB96@@QAE@H@Z':'??0FUN_00528cb0@@QAE@H@Z','?FUN_006f74f0@PtrA96@@QAEXPAX@Z':'?FUN_006f74f0@FUN_00528cb0@@QAEXH@Z','?FUN_0092c8b0@PtrB96@@QAEXPAX@Z':'?FUN_0092c8b0@FUN_00528cb0@@QAEXH@Z'}
 facts=[]
 for f in u['functions']:
  n=norm if f['address']=='0x00913fe0' else {'$SG27297':'$SG27267'} if f['address']=='0x008f36c0' else {}
  a,ar=relocated(objects['original'],f['symbol'],f['size'],{});b,br=relocated(objects['candidate'],f['symbol'],f['size'],n)
  facts.append({'address':f['address'],'bytes_equal':a==b,'relocations_equal':ar==br})
 if any(not f['bytes_equal'] or not f['relocations_equal'] for f in facts):raise ValueError('function mismatch')
 u['symbols']['$SG58544']='0x010898c0';candidate['symbols'].update({'$SG58544':'0x010898c0','$SG27297':'0x01088220'});pe=Pe(paths.REF_IMAGE);results={}
 for tag,spec in [('production',u),('original',u),('candidate',candidate)]:
  rows=compare(objects[tag],pe,spec)
  if len(rows)!=178 or any(r['verdict']!='match' for r in rows):raise ValueError('strict reference mismatch '+tag)
  sections,inf,errors=eh_sections(objects[tag],pe,spec,rows,recipe_names(units))
  results[tag]={'functions':len(rows),'match':178,'eh_sections':len(sections),'eh_failed':[x for x in sections if not x[2]],'eh_errors':errors,'inferred':{k:hex(v) for k,v in inf.items()}}
 if results['candidate']['eh_failed'] or results['candidate']['eh_errors']:raise ValueError('candidate EH did not pass')
 report={'scope':'unit-local source-backed literal bindings, scoped normalization and unchanged ordinary EH oracle; no placement/runtime acceptance',
   'units_sha256':sha(unitsfile),'manifest_sha256':sha(O/'mirror-manifest.json'),'compile_result_sha256':sha(O/'compile-result.json'),'production_sha256':sha(prod),'local_literal_evidence_sha256':sha(ev),'literal_pools':pool,'functions':facts,'results':results,
   'limitations':['constructor/method renamed views require source and ABI review','five/four other inferred EH names are reported separately','global image placement and runtime controls not performed']}
 out.write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps({'output':str(out),'sha256':sha(out),'candidate_eh':results['candidate']}))
if __name__=='__main__':main()
