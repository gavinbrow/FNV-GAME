"""Private source hypothesis preserving previously selected global placement overloads."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;F=M.parent.parent/'fnv_decomp';O=M/'out/phase2-nimem-global-placement-v2';B=M/'out/phase2-nimem-combined-825d'
PIN='6b9dc1950f489c696364820186a4beba3e1618d127c4a656ecb677b53e32e1a3'
FILES={
 'src/bsshader/speedtreeleafshader.cpp':('fc89ded7891afe9804424b6879ab9da2d9119277974e2febedb518b88dc21f76',[(b'new ((FadeTag*)0) SpeedTreeLeafShader',b'::new ((FadeTag*)0) SpeedTreeLeafShader')]),
 'src/gamebryo2.2/corelibs/nianimation/nicolorinterpolator.cpp':('8f5944cda428f18952ca27bf68f6b401723f0bf6c722b949e5bf19bb104c64b0',[(b'new (memory) NiColorInterpolator(0)',b'::new (memory) NiColorInterpolator(0)')]),
 'src/gamebryo2.2/corelibs/nianimation/nitexturetransformcontroller.cpp':('41a66e7b51ecbdc40ad5cac6673aca03136a63f5c3b4bc30456cc30c45f39d01',[(b'new (pkObject) NiTextureTransformController',b'::new (pkObject) NiTextureTransformController'),(b'return new (storage)',b'return ::new (storage)')]),
 'src/gamebryo2.2/corelibs/niparticle/nipsysemitterctlr.cpp':('d112e69c10aff8bf79800661dd0236cfe5fe6b7b158331e674ca9926a42e429e',[(b'new (floatMemory) NiFloatInterpolator(0)',b'::new (floatMemory) NiFloatInterpolator(0)')]),
}
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve previous evidence')
 if sha((B/'manifest.json').read_bytes())!=PIN:raise ValueError('combined proposal changed')
 result=[];payload={}
 for name,(pin,edits) in FILES.items():
  before=(F/name).read_bytes()
  if sha(before)!=pin:raise ValueError('source preimage changed '+name)
  after=before
  for old,new in edits:
   if after.count(old)!=1:raise ValueError('site is not unique '+name)
   after=after.replace(old,new,1)
  payload[name]=after;result.append({'path':name,'before_sha256':sha(before),'after_sha256':sha(after),'edits':len(edits)})
 O.mkdir()
 for name,data in payload.items():
  q=O/'payload'/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
 (O/'manifest.json').write_text(json.dumps({'combined_proposal_sha256':PIN,'files':result,'units':[200,1203,1271,1598],'limits':['private source hypothesis, not compiled','preserves exact original global placement overload selection; reference function bytes, allocation targets and EH remain to verify','separate from unresolved allocator-adapter and broader API/EH effects']},indent=2))
 print(sha((O/'manifest.json').read_bytes()))
if __name__=='__main__':main()
