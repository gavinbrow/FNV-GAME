"""Stage an AutoMemContext lifetime hypothesis for the unit211 EH discrepancy."""
import hashlib,json
from pathlib import Path
import baseformcomponent_core_stage as core
M=Path(__file__).resolve().parent.parent;F=M.parent.parent/'fnv_decomp';R=M/'out';P=R/'phase2-nimem-next-source-composed';Q=R/'phase2-nimem-psys-pointer-binding-v1';O=R/'phase2-watershader-211-automem-v1';REL='src/bsshader/watershader.cpp'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve prior evidence')
 raw=(F/'build/units.json').read_bytes();pm=(P/'manifest.json').read_bytes();recipe=(Q/'units.generated').read_bytes();proof=R/'phase2-watershader-211-eh-ownership.json'
 if sha(raw)!='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68' or sha(pm)!='c1289a7009ada0218ae60bf4d9851ed39512f508e72b8bcf063185c53b40ef53' or sha(recipe)!='5a51705361ab8a9f2947f815a86c935a195fe82cecd3de7b43a2e7db362a74ad' or sha(proof.read_bytes())!='075ec18c9bdd968d9e218c1475d5ee35803f5759f23404b660bb548e8aa878a8':raise ValueError('input changed')
 m=json.loads(pm);ov={}
 for rel,h in m['source_payload_sha256'].items():
  b=(P/'payload'/rel).read_bytes()
  if sha(b)!=h:raise ValueError('payload changed')
  ov[rel]=b
 b=(F/REL).read_bytes()
 if REL in ov or sha(b)!='0fb67f7563d989f10faa12a88ea005da7083d6e84b7a0c04d6db3f1c9ca97363':raise ValueError('source overlap or drift')
 s=b.decode('utf-8');nl='\r\n' if '\r\n' in s else '\n';a=s.find('class WaterShaderMemScope'+nl);z=s.find('class WaterShaderLoader',a)
 if a<0 or z<0 or s.count('WaterShaderMemScope kScope(0x1d);')!=1:raise ValueError('source lifetime not unique')
 replacement=nl.join(['class AutoMemContext','{','    int m_eMemoryContext;','  public:','    AutoMemContext(int context)','    {','        WaterShaderThreadState* state = WaterShaderGetThreadState();','        m_eMemoryContext = state->m_uiMemoryContext;','        state->m_uiMemoryContext = context;','    }','    ~AutoMemContext();','};',''])+nl
 candidate=(s[:a]+replacement+s[z:]).replace('WaterShaderMemScope kScope(0x1d);','AutoMemContext kScope(0x1d);',1).encode('utf-8');ov[REL]=candidate
 u=json.loads(raw)['units'][211];original=core.walk(F,u['source'],{});modified=core.walk(F,u['source'],ov)
 O.mkdir()
 for rel,data in ov.items():
  q=O/'payload'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
 report={'base_recipe_sha256':sha(raw),'candidate_recipe_parent_sha256':sha(recipe),'composed_manifest_sha256':sha(pm),'ownership_proof_sha256':sha(proof.read_bytes()),'unit':211,'source':u['source'],'compiler':u['compiler'],'flags':u['flags'],'functions':u['functions'],'eh_tails':u.get('eh_tails',[]),'original':original,'candidate':modified,'source_payload_sha256':{k:sha(v) for k,v in ov.items()},'proposed_owner_symbol':'??1AutoMemContext@@QAE@XZ','source_owner_unit':47,'source_owner_address':'0x00404ee0','limits':['private hypothesis only; no compiler or installation','one-argument inline constructor is a local surrogate matching the source context protocol, not proof of a complete canonical class','require all 5647 parent bytes/relocations, frame/local displacements, original EH state/action ownership and strict owner47/Leave781 bodies','source layout, global ODR, final image and runtime remain unproved']};(O/'manifest.json').write_text(json.dumps(report,indent=2));print(sha((O/'manifest.json').read_bytes()))
if __name__=='__main__':main()
