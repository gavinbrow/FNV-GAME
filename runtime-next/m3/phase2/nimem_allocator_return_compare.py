"""Compare staged 0xaa13e0 return-contract owner without altering the oracle."""
import copy,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';D=M/'out/phase2-nimem-allocator-return';OUT=D/'comparison.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,recipe_names
from rtti_hkp_viewer_compare import relocated
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve proof')
 m=json.loads((D/'manifest.json').read_text());rp=F/'build/units.json';oldp=D/'units.original';newp=D/'units.generated';run=json.loads((D/'compile-result.json').read_text());mm=D/'mirror-manifest.json'
 if sha(rp)!=m['base_recipe_sha256'] or sha(oldp)!=m['base_recipe_sha256'] or sha(newp)!=m['candidate_recipe_sha256'] or run['unit_index']!=2734 or run['mirror_manifest_sha256']!=sha(mm):raise ValueError('input differs')
 old=json.loads(oldp.read_text())['units'];new=json.loads(newp.read_text())['units'];o=old[2734];n=copy.deepcopy(new[2734]);prod=RN/'pinned-build/obj_v3/2734.obj';objects={'production':Coff(str(prod))}
 for x in run['outcomes']:
  p=D/(x['tag']+'.obj')
  if x['rc'] or not x['trace_valid'] or sha(p)!=x['object_sha256']:raise ValueError('compile object mismatch')
  objects[x['tag']]=Coff(str(p))
 if set(objects)!={'production','original','candidate'}:raise ValueError('missing pair')
 pe=Pe(paths.REF_IMAGE);records={}
 for tag in ('production','original'):
  r=compare(objects[tag],pe,o)
  if len(r)!=43 or any(z['verdict']!='match' for z in r):raise ValueError('baseline strict mismatch '+tag)
  records[tag]={'strict_functions':len(r)}
 original=objects['original'];candidate=objects['candidate'];facts=[];newf={x['address']:x for x in n['functions']}
 for f in o['functions']:
  g=newf[f['address']];a,ar=relocated(original,f['symbol'],f['size'],{});b,br=relocated(candidate,g['symbol'],g['size'],{})
  if a!=b or len(ar)!=len(br):raise ValueError('function body or relocations differ '+f['address'])
  for x,y in zip(ar,br):
   if x==y:continue
   if (x[0],x[1],x[3])!=(y[0],y[1],y[3]) or not all(re.fullmatch(r'\$SG\d+',z[2]) for z in (x,y)):raise ValueError('nonliteral relocation differs '+f['address'])
   aa=original.named(x[2]);bb=candidate.named(y[2]);sa=original.sections[aa['section']];sb=candidate.sections[bb['section']]
   if aa['value']!=bb['value'] or sa['name']!='.rdata' or sb['name']!='.rdata' or sa['relocs'] or sb['relocs'] or sa['data']!=sb['data'] or x[2] not in o['symbols']:raise ValueError('literal pool not independently paired')
   value=o['symbols'][x[2]];n['symbols'][y[2]]=value;facts.append({'function':f['address'],'field_offset':x[0],'before':x[2],'after':y[2],'bound_va':value,'pool_offset':aa['value'],'pool_sha256':hashlib.sha256(sa['data']).hexdigest()})
 rows=compare(candidate,pe,n)
 if len(rows)!=43 or any(x['verdict']!='match' for x in rows):raise ValueError('candidate strict mismatch')
 sec,inf,errors=eh_sections(candidate,pe,n,rows,recipe_names(old))
 if errors or any(not x[2] for x in sec):raise ValueError('candidate EH differs')
 OUT.write_text(json.dumps({'scope':'private allocator return-contract source hypothesis; no integration','recipe_sha256':sha(rp),'fixture_manifest_sha256':sha(D/'manifest.json'),'compile_result_sha256':sha(D/'compile-result.json'),'production_object_sha256':sha(prod),'candidate_object_sha256':sha(D/'candidate.obj'),'strict_functions':43,'paired_literal_fields':facts,'target_function':'0x00aa13e0','target_size':62,'candidate_symbol':m['candidate_symbol'],'ordinary_eh_sections':len(sec),'inferred_names':{k:'0x%08x'%v for k,v in inf.items()},'limits':['actual source installation, production-object literal bindings, ownership and final image/runtime remain separate','indirect allocator vtable semantic method name/failure contract not fully recovered']},indent=2));print(json.dumps({'strict_functions':43,'paired_literal_fields':len(facts),'eh_sections':len(sec)}))
if __name__=='__main__':main()
