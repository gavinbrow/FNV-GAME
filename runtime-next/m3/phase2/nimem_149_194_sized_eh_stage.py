"""Stage two independent local sized-delete source declarations."""
import hashlib,json
from pathlib import Path
import baseformcomponent_core_stage as core
M=Path(__file__).resolve().parent.parent;F=M.parent.parent/'fnv_decomp';R=M/'out';P=R/'phase2-nimem-next-source-composed';O=R/'phase2-nimem-149-194-sized-eh-v1'
FILES={'src/bsshader/debugshader_local.h':'e1ddae7bf0813cb8f72ae2f1f0e7ee8d083af81cf5e70c127ac02a810b82a60e','src/bsshader/shadowscenenode_fog_decls.h':'423548e04911f6cdfb7bbd7e1f817f1246d6c64e597a89d181154e0b5b848a6d'}
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve evidence')
 raw=(F/'build/units.json').read_bytes();pm=(P/'manifest.json').read_bytes()
 if sha(raw)!='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68' or sha(pm)!='c1289a7009ada0218ae60bf4d9851ed39512f508e72b8bcf063185c53b40ef53':raise ValueError('baseline changed')
 m=json.loads(pm);ov={}
 for rel,h in m['source_payload_sha256'].items():
  b=(P/'payload'/rel).read_bytes()
  if sha(b)!=h:raise ValueError('composed payload changed')
  ov[rel]=b
 headers=[]
 for rel,pin in FILES.items():
  before=(F/rel).read_bytes()
  if rel in ov or sha(before)!=pin or before.count(b'static void operator delete(void*);')!=1:raise ValueError('ambiguous header preimage')
  ov[rel]=before.replace(b'static void operator delete(void*);',b'static void operator delete(void*, unsigned int);',1);headers.append({'path':rel,'before_sha256':pin,'after_sha256':sha(ov[rel])})
 units=json.loads(raw)['units'];rows=[]
 for i in (149,194):
  u=units[i];orig=core.walk(F,u['source'],{});cand=core.walk(F,u['source'],ov)
  rows.append({'unit':i,'source':u['source'],'compiler':u['compiler'],'flags':u['flags'],'functions':u['functions'],'eh_tails':u.get('eh_tails',[]),'original':orig,'candidate':cand})
 O.mkdir()
 for rel,b in ov.items():
  q=O/'payload'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 m={'base_recipe_sha256':sha(raw),'composed_manifest_sha256':sha(pm),'headers':headers,'units':rows,'source_payload_sha256':{k:sha(v) for k,v in ov.items()},'source_support':['unit149 reference cleanup pushes 0xc0, source class asserts sizeof 192, and its deleting-wrapper source frees 0xc0','unit194 reference cleanup pushes 0x64, source class asserts sizeof 100','both original cleanup calls target independently strict-checked native NiMemObject sized-delete owner unit1664, 0x00aa1460'],'limits':['private proposal; no compilation or install','each local surrogate declaration remains separate; no global class/ODR claim','full affected consumer closure, strict functions, ordinary EH, metadata and generated bodies require proof']};(O/'manifest.json').write_text(json.dumps(m,indent=2));print(sha((O/'manifest.json').read_bytes()))
if __name__=='__main__':main()
