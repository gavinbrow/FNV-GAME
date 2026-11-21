"""Stage source-owned allocation/cleanup lookup for unit172 geometry."""
import hashlib,json
from pathlib import Path
import baseformcomponent_core_stage as core
M=Path(__file__).resolve().parent.parent;F=M.parent.parent/'fnv_decomp';R=M/'out';P=R/'phase2-nimem-next-source-composed';O=R/'phase2-nimem-172-geometry-eh-v2';SRC='src/bsshader/imagespacemanager.cpp';HDR='src/bsshader/imagespacemanager_geometry.h'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve prior proposal')
 raw=(F/'build/units.json').read_bytes();pm=(P/'manifest.json').read_bytes()
 if sha(raw)!='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68' or sha(pm)!='c1289a7009ada0218ae60bf4d9851ed39512f508e72b8bcf063185c53b40ef53':raise ValueError('baseline changed')
 m=json.loads(pm);ov={}
 for rel,h in m['source_payload_sha256'].items():
  b=(P/'payload'/rel).read_bytes()
  if sha(b)!=h:raise ValueError('payload changed')
  ov[rel]=b
 src=(F/SRC).read_bytes();hdr=(F/HDR).read_bytes()
 if SRC in ov or HDR in ov or sha(src)!='19f5a16b7653a538116494d596f7f12f963a0955c9c9202492e61f5a4afd317a' or sha(hdr)!='74db570e2a3ecf67471ce7d0847fcc78601d26b143c1921743e9d357b211aef7':raise ValueError('source overlap or drift')
 old=b'this->m_pMenuBackgroundScreenElements = ::new NiScreenElements(spScreenData);'
 if src.count(old)!=1:raise ValueError('allocation source not unique')
 ov[SRC]=src.replace(old,old.replace(b'::new',b'new'),1)
 start=hdr.find(b'class NiScreenElements : public NiAVObject');end=hdr.find(b'\r\n};',start)
 if start<0 or end<0:raise ValueError('class range missing')
 block=hdr[start:end];needle=b'static void operator delete(void*, unsigned int);'
 if block.count(needle)!=1:raise ValueError('delete declaration not unique')
 newneedle=b'static void* operator new(unsigned int) throw();'
 if block.count(newneedle)!=1:raise ValueError('new declaration not unique')
 block=block.replace(newneedle,b'using NiMemObject::operator new;',1).replace(needle,b'using NiMemObject::operator delete;',1)
 ov[HDR]=hdr[:start]+block+hdr[end:]
 u=json.loads(raw)['units'][172];orig=core.walk(F,u['source'],{});cand=core.walk(F,u['source'],ov)
 if HDR not in cand['files']:raise ValueError('header missing from closure')
 O.mkdir()
 for rel,b in ov.items():
  q=O/'payload'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 report={'base_recipe_sha256':sha(raw),'composed_manifest_sha256':sha(pm),'unit':172,'source':u['source'],'compiler':u['compiler'],'flags':u['flags'],'functions':u['functions'],'eh_tails':u.get('eh_tails',[]),'original':orig,'candidate':cand,'source_payload_sha256':{k:sha(v) for k,v in ov.items()},'source_support':['original strict-matching function allocates 0xc4 bytes via 0x00aa13e0','reference cleanup pushes 0xc4 and calls source-owned sized delete at 0x00aa1460','class source inherits NiObject; local using declarations select source-owned NiMemObject new and sized delete'],'limits':['private source hypothesis; no compiler or source install','source class and generated hierarchy/ODR not claimed native','all functions, cleanup fields and metadata need fresh original/candidate proof']};(O/'manifest.json').write_text(json.dumps(report,indent=2));print(sha((O/'manifest.json').read_bytes()))
if __name__=='__main__':main()
