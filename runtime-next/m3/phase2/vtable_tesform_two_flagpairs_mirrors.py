"""Create private getter/setter mirrors against the installed typed transaction."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;sys.path.insert(0,str(H));import rtti_mirror_prepare as r,tesform_load_typed_transaction_v4 as tx
S=M/'out/phase2-tesform-two-flagpairs-setters';D='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160'
def sha(b):return hashlib.sha256(b).hexdigest()
def transition(old,new,current):
 m=tx.manifest()
 for x in m['files']:
  if sha((tx.F/x['path']).read_bytes())!=x['new_sha256']:raise ValueError('typed installed baseline changed '+x['path'])
 if sha(current)!=D:raise ValueError('recipe changed')
 return json.loads(current)
r.transition=transition
def main():
 meta=json.loads((S/'manifest.json').read_bytes())
 for n,h in meta['outputs'].items():
  if sha((S/n).read_bytes())!=h:raise ValueError('candidate changed')
 sets=[('src/fallout_shared/tesform.cpp',{'src/fallout_shared/tesform.cpp':(S/'tesform.cpp').read_bytes(),'src/fallout_shared/tesform_TESForm.h':(S/'tesform_TESForm.h').read_bytes()},M/'out/phase2-tesform-two-flagpairs-mirror'),('src/bgsencounterzone.cpp',{'src/bgsencounterzone_TESForm.h':(S/'bgsencounterzone_TESForm.h').read_bytes()},M/'out/phase2-bgs-two-flagpairs-mirror')]
 for src,overrides,out in sets:
  m=r.prepare(src,overrides,out);m['units_sha256']=D;m['reviewed_units_sha256']=D;m['typed_transaction_manifest_sha256']=tx.PROOF;(out/'mirror-manifest.json').write_text(json.dumps(m,indent=2));print(json.dumps({'out':out.name,'files':len(m['candidate']['files']),'recipe':D}))
if __name__=='__main__':main()
