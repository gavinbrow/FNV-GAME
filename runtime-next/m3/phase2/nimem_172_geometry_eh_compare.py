"""Compare saved private sized-delete objects using unchanged ordinary oracles."""
import argparse,copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';P=R/'phase2-nimem-172-geometry-eh-v1';Q=R/'phase2-nimem-psys-pointer-binding-v1';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
from rtti_hkp_viewer_compare import relocated
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--unit',type=int,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--production-object',type=Path,required=True);ap.add_argument('--production-object-sha256',required=True);a=ap.parse_args();d=a.out.resolve();prod=a.production_object.resolve()
 if a.unit != 172 or not d.is_relative_to((M/'out').resolve()) or not prod.is_relative_to((M/'out').resolve()):raise ValueError('private unit and paths required')
 out=d/'sized-eh-comparison.json'
 if out.exists():raise FileExistsError('preserve prior report')
 if sha(P/'manifest.json')!='17ca3fa00c66a29137e87c842ff1710d4ab400d588100b58d1d4d540e2ed01ca' or sha(Q/'units.generated')!='5a51705361ab8a9f2947f815a86c935a195fe82cecd3de7b43a2e7db362a74ad' or sha(prod)!=a.production_object_sha256.lower():raise ValueError('proof or archive differs')
 m=json.loads((d/'mirror-manifest.json').read_text());run=json.loads((d/'compile-result.json').read_text())
 if m['geometry_eh_manifest_sha256']!=sha(P/'manifest.json') or run['unit_index']!=a.unit or run['mirror_manifest_sha256']!=sha(d/'mirror-manifest.json'):raise ValueError('mirror mismatch')
 units=json.loads((Q/'units.generated').read_text())['units'];owner=[f for f in units[1664]['functions'] if f['symbol']=='??3NiMemObject@@SAXPAXI@Z']
 if len(owner)!=1 or owner[0]['address']!='0x00aa1460':raise ValueError('native source owner differs')
 specs={'production':units[a.unit],'original':units[a.unit],'candidate':copy.deepcopy(units[a.unit])};specs['candidate']['symbols']['??3NiMemObject@@SAXPAXI@Z']=owner[0]['address'];objects={'production':Coff(str(prod))}
 for x in run['outcomes']:
  p=d/(x['tag']+'.obj')
  if x['rc'] or not x['trace_valid'] or sha(p)!=x['object_sha256']:raise ValueError('saved object mismatch')
  objects[x['tag']]=Coff(str(p))
 if set(objects)!={'production','original','candidate'}:raise ValueError('object pair missing')
 pe=Pe(paths.REF_IMAGE);results={}
 for tag,c in objects.items():
  rows=compare(c,pe,specs[tag]);sections,inf,errors=eh_sections(c,pe,specs[tag],rows,recipe_names(units));tails,bad,_,_,conf=eh_tails([specs[tag]],[{'eh_sections':sections,'eh_inferred':{k:'0x%08x'%v for k,v in inf.items()}}],pe)
  results[tag]={'object_sha256':sha(prod if tag=='production' else d/(tag+'.obj')),'functions':len(rows),'matches':sum(x['verdict']=='match' for x in rows),'failures':[{'address':x['address'],'errors':x['errors']} for x in rows if x['verdict']!='match'],'sections':sections,'eh_errors':errors,'bad_tails':bad,'conflicts':conf,'inferred_names':len(inf)}
 pairs=[]
 for f in units[a.unit]['functions']:
  x,xr=relocated(objects['original'],f['symbol'],f['size'],{});y,yr=relocated(objects['candidate'],f['symbol'],f['size'],{})
  if x!=y or xr!=yr:pairs.append({'address':f['address'],'bytes_equal':x==y,'original_relocations':xr,'candidate_relocations':yr})
 out.write_text(json.dumps({'unit':a.unit,'manifest_sha256':sha(P/'manifest.json'),'candidate_recipe_sha256':sha(Q/'units.generated'),'native_owner':owner[0],'local_candidate_binding':{'??3NiMemObject@@SAXPAXI@Z':owner[0]['address']},'results':results,'mapped_pair_differences':pairs,'limits':['source-owner binding is a diagnostic; no recipe installed','ordinary EH sections remain explicit; full generated metadata and ODR require independent review']},indent=2));print(json.dumps({'unit':a.unit,'matches':{k:v['matches'] for k,v in results.items()},'eh_failed':{k:sum(not x[2] for x in v['sections']) for k,v in results.items()},'pair_differences':len(pairs)}))
if __name__=='__main__':main()
