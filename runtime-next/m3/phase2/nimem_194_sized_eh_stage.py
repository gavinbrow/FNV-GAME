"""Stage unit194 local NiMemObject sized-delete declaration hypothesis."""
import hashlib,json
from pathlib import Path
import baseformcomponent_core_stage as core
M=Path(__file__).resolve().parent.parent;F=M.parent.parent/'fnv_decomp';R=M/'out';P=R/'phase2-nimem-next-source-composed';O=R/'phase2-nimem-194-sized-eh-v1';REL='src/bsshader/shadowscenenode_fog_decls.h'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve existing evidence')
 raw=(F/'build/units.json').read_bytes();pm=(P/'manifest.json').read_bytes()
 if sha(raw)!='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68' or sha(pm)!='c1289a7009ada0218ae60bf4d9851ed39512f508e72b8bcf063185c53b40ef53':raise ValueError('baseline changed')
 m=json.loads(pm);ov={}
 for rel,h in m['source_payload_sha256'].items():
  b=(P/'payload'/rel).read_bytes()
  if sha(b)!=h:raise ValueError('composed payload changed')
  ov[rel]=b
 before=(F/REL).read_bytes()
 if REL in ov or sha(before)!='423548e04911f6cdfb7bbd7e1f817f1246d6c64e597a89d181154e0b5b848a6d' or before.count(b'static void operator delete(void*);')!=1:raise ValueError('ambiguous preimage')
 ov[REL]=before.replace(b'static void operator delete(void*);',b'static void operator delete(void*, unsigned int);',1)
 u=json.loads(raw)['units'][194];orig=core.walk(F,u['source'],{});cand=core.walk(F,u['source'],ov)
 if REL not in cand['files']:raise ValueError('header not in unit closure')
 O.mkdir()
 for rel,b in ov.items():
  q=O/'payload'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 report={'base_recipe_sha256':sha(raw),'composed_manifest_sha256':sha(pm),'unit':194,'source':u['source'],'compiler':u['compiler'],'flags':u['flags'],'functions':u['functions'],'eh_tails':u.get('eh_tails',[]),'header':REL,'before_header_sha256':sha(before),'after_header_sha256':sha(ov[REL]),'original':orig,'candidate':cand,'source_payload_sha256':{k:sha(v) for k,v in ov.items()},'source_support':['BSFogProperty is source-asserted size 100','original cleanup pushes 0x64 and calls source-owned sized delete at 0x00aa1460','native sized delete implementation is source unit1664, already independently strict-checked'],'limits':['private hypothesis only; no compiler or source install','verify all mapped functions, original and changed EH, generated wrappers and actual header consumer closure','local declaration is a surrogate; no global class or ODR claim']};(O/'manifest.json').write_text(json.dumps(report,indent=2));print(sha((O/'manifest.json').read_bytes()))
if __name__=='__main__':main()
