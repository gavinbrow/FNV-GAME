"""Prove unit-local compiler literal renames without changing the oracle."""
import copy,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';D=M/'out/phase2-nimem-adapter-using-v2-u0773';P=M/'out/phase2-nimem-adapter-using-v2';O=M/'out/phase2-nimem-adapter-using-v2-773-literal-proof.json'
sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
from rtti_hkp_viewer_compare import relocated
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve old proof')
 if sha(P/'manifest.json')!='ec90e9a5d649e5841c04d5ad194b07d17eca8c5a12a267d40faed73ed95739e3' or sha(F/'build/units.json')!='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68':raise ValueError('input mismatch')
 run=json.loads((D/'compile-result.json').read_text());mm=D/'mirror-manifest.json'
 if run['unit_index']!=773 or run['mirror_manifest_sha256']!=sha(mm):raise ValueError('mirror identity mismatch')
 for row in run['outcomes']:
  if row['rc'] or not row['trace_valid'] or sha(D/(row['tag']+'.obj'))!=row['object_sha256']:raise ValueError('object identity mismatch')
 units=json.loads((F/'build/units.json').read_text())['units'];spec=units[773];ca=Coff(str(D/'original.obj'));cb=Coff(str(D/'candidate.obj'));paired={};fields=[]
 for f in spec['functions']:
  a,ar=relocated(ca,f['symbol'],f['size'],{});b,br=relocated(cb,f['symbol'],f['size'],{})
  if a!=b or len(ar)!=len(br):raise ValueError('body or relocation count differs '+f['address'])
  for x,y in zip(ar,br):
   if x==y:continue
   if (x[0],x[1],x[3])!=(y[0],y[1],y[3]) or not all(re.fullmatch(r'\$SG\d+',z[2]) for z in (x,y)):raise ValueError('nonliteral difference '+f['address'])
   xs=ca.named(x[2]);ys=cb.named(y[2]);xp=ca.sections[xs['section']];yp=cb.sections[ys['section']]
   if xs['value']!=ys['value'] or xp['name']!='.rdata' or yp['name']!='.rdata' or xp['relocs'] or yp['relocs'] or xp['data']!=yp['data'] or x[2] not in spec['symbols']:raise ValueError('literal pool identity failed')
   va=spec['symbols'][x[2]]
   if y[2] in paired and paired[y[2]]!=va:raise ValueError('ambiguous candidate binding')
   paired[y[2]]=va;fields.append({'function':f['address'],'field_offset':x[0],'old_symbol':x[2],'new_symbol':y[2],'pool_offset':xs['value'],'full_pool_sha256':hashlib.sha256(xp['data']).hexdigest(),'reference_va':va})
 if len(fields)!=6:raise ValueError('unexpected number of changed fields')
 fixed=copy.deepcopy(spec);fixed['symbols'].update(paired);pe=Pe(paths.REF_IMAGE);results={}
 for tag,c,s in [('original',ca,spec),('candidate',cb,fixed)]:
  r=compare(c,pe,s);sections,inferred,errors=eh_sections(c,pe,s,r,recipe_names(units));tails,bad,inf,_,conf=eh_tails([s],[{'eh_sections':sections,'eh_inferred':{k:'0x%08x'%v for k,v in inferred.items()}}],pe)
  results[tag]={'functions':len(r),'matches':sum(x['verdict']=='match' for x in r),'failures':[{'address':x['address'],'errors':x['errors']} for x in r if x['verdict']!='match'],'eh_sections':len(sections),'failed_eh_sections':sum(not x[2] for x in sections),'eh_errors':errors,'eh_bad_tails':bad,'eh_conflicts':conf,'eh_inferred_names':len(inferred),'eh_inferred_tails':len(inf)}
  if results[tag]['matches']!=39 or results[tag]['failed_eh_sections'] or errors or bad or conf:raise ValueError('strict ordinary proof fails '+tag)
 O.write_text(json.dumps({'object_sha256':{'original':sha(D/'original.obj'),'candidate':sha(D/'candidate.obj')},'reference_sha256':sha(Path(paths.REF_IMAGE)),'fields':fields,'unit_local_bindings':paired,'results':results,'limits':['diagnostic, unit-local candidate bindings only; production compiler pool labels must be independently rederived','generated metadata and complete type identity remain separate']},indent=2));print(json.dumps({'fields':len(fields),'bindings':paired,'results':results}))
if __name__=='__main__':main()
