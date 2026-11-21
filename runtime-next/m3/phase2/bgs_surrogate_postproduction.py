"""Confirm obsolete BGSE surrogate references after the typed production compile."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';O=M/'out/phase2-bgs-surrogate-postproduction.json';sys.path[:0]=[str(F/'tools'),str(RN/'pinned-build'),str(H)]
from compare import Coff
import bgs_surrogate_ownership_audit as prior

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError('refusing overwrite')
 previous=M/'out/phase2-bgs-surrogate-ownership.json';before=json.loads(previous.read_text());p=RN/'pinned-build/obj_v3/0002.obj';proof=M/'out/phase2-tesform-load-typed-v4-transaction/production-correction/manifest.json';e=json.loads(proof.read_text());units=F/'build/units.json'
 if sha(p)!=e['bgs_object_sha256'] or sha(units)!=e['original_sha256']:raise ValueError('current production inputs changed')
 c=Coff(str(p));names=(prior.OLD_E,prior.OLD_G);hits={x:[] for x in names};index=hashlib.sha256();files=sorted((RN/'pinned-build/obj_v3').glob('*.obj'))
 for f in files:
  data=f.read_bytes();index.update(f.name.encode()+b'\0'+hashlib.sha256(data).digest())
  for name in names:
   if name.encode() in data:hits[name].append(f.name)
 if any(hits.values()):raise ValueError('obsolete surrogate symbol remains in production objects')
 if c.by_name.get('??_7FUN_00525ce0@@6B@'):raise ValueError('surrogate vtable remains in production object')
 if prior.weak(c,prior.NATIVE_E)!=prior.NATIVE_G or prior.body(c,prior.NATIVE_G)!=before['retained_native_g_body']:
  # JSON converts tuples to lists; compare a canonical serialized value.
  if json.loads(json.dumps(prior.body(c,prior.NATIVE_G)))!=before['retained_native_g_body']:raise ValueError('retained native G differs')
 m3=M/'gen/m3_manifest.json';dv=M/'gen/dv1_pieces.json';sym=RN/'data-v3/symbolic.json'
 for key,pth in [('m3',m3),('dv1',dv),('symbolic',sym)]:
  if sha(pth)!=before['input_sha256'][key]:raise ValueError('selected ownership input changed '+key)
 result={'scope':'actual post-source COFF exact-name demand and selected-first-slot evidence; no full vtable/ODR claim','production_object_count':len(files),'production_object_index_sha256':index.hexdigest(),'exact_old_symbol_hits':hits,'production_bgs_sha256':sha(p),'recipe_sha256':sha(units),'native_weak_fallback':prior.weak(c,prior.NATIVE_E),'native_g_body_matches_prior':True,'old_surrogate_vtable_symbol_present':False,'prior_ownership_evidence_sha256':sha(previous),'correction_proof_sha256':sha(proof),'limitations':['former original surrogate weak E relocation existed only in its old vtable section','current M3/DV1 first slot remains unselected and data-v3 captured mapping is unchanged','complete vtable, weak ownership outside scanned object set, and final image gates remain open']}
 O.write_text(json.dumps(result,indent=2));print(json.dumps({'objects':len(files),'obsolete_symbol_hits':hits,'native_g_match':True}))
if __name__=='__main__':main()
