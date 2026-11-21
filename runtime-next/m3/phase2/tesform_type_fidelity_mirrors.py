"""Prepare fa-pinned mirrors for type-fidelity class candidate."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;sys.path.insert(0,str(H));import rtti_mirror_prepare as r,rtti_tesform_bindings_transaction as tx
B=M/'out/phase2-tesform-binding-repair-v3';S=M/'out/phase2-class-typed-v1';P='7242e851405ec30aed816f65d1c134405f229b4458ee6ec3f4a5bca4cb327c59'
def sha(b):return hashlib.sha256(b).hexdigest()
def transition(old,new,current):
 a=(B/'units.original').read_bytes();b=(B/'units.generated').read_bytes();e=(B/'manifest.json').read_bytes()
 if sha(e)!=P:raise ValueError('repair proof changed')
 tx.validate_payloads(a,b,json.loads(e))
 if new!=a or current!=b:raise ValueError('recipe transition changed')
 return json.loads(b)
r.transition=transition
def main():
 meta=json.loads((S/'manifest.json').read_text())
 for n,d in meta['outputs'].items():
  if sha((S/n).read_bytes())!=d:raise ValueError('typed candidate changed '+n)
 sets=[('src/fallout_shared/tesform.cpp',{'src/fallout_shared/tesform.cpp':(S/'tesform.cpp').read_bytes(),'src/fallout_shared/tesform_TESForm.h':(S/'tesform_TESForm.h').read_bytes()},M/'out/phase2-tesform-typed-mirror'),('src/bgsencounterzone.cpp',{'src/bgsencounterzone.cpp':(S/'bgsencounterzone.cpp').read_bytes(),'src/bgsencounterzone_decls.h':(S/'bgsencounterzone_decls.h').read_bytes(),'src/bgsencounterzone_TESForm.h':(S/'bgsencounterzone_TESForm.h').read_bytes()},M/'out/phase2-bgs-typed-mirror')]
 for source,overrides,out in sets:
  m=r.prepare(source,overrides,out);m['units_sha256']=sha((B/'units.generated').read_bytes());m['reviewed_units_sha256']=sha((B/'units.original').read_bytes());m['binding_transition_evidence_sha256']=P;(out/'mirror-manifest.json').write_text(json.dumps(m,indent=2));print(out.name,len(m['original']['files']),len(m['candidate']['files']))
if __name__=='__main__':main()
