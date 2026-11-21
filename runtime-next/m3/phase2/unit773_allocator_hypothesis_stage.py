"""Generate a private unit 773 allocator-hierarchy hypothesis; no live writes."""
import hashlib,json
from pathlib import Path
import baseformcomponent_core_stage as core
M=Path(__file__).resolve().parent.parent; F=M.parent.parent/'fnv_decomp'; P=M/'out/phase2-nimem-next-source-composed'; R=M/'out/phase2-nimem-psys-pointer-binding-v1/units.generated'; O=M/'out/phase2-unit773-allocator-generated'; I=M/'out/phase2-nimem-next-source-proof-index-v4.json'; sha=lambda b:hashlib.sha256(b).hexdigest()
def main():
 if O.exists(): raise FileExistsError(O)
 parent=(P/'manifest.json').read_bytes();recipe=R.read_bytes();idx=I.read_bytes()
 if sha(parent)!='c1289a7009ada0218ae60bf4d9851ed39512f508e72b8bcf063185c53b40ef53' or sha(recipe)!='5a51705361ab8a9f2947f815a86c935a195fe82cecd3de7b43a2e7db362a74ad' or sha(idx)!='f02c075f5dff6da865990f0fb85c06eb49192955389f42f5610195cfe5e9b826':raise ValueError('input pin')
 pm=json.loads(parent);ov={}
 for rel,h in pm['source_payload_sha256'].items():
  data=(P/'payload'/rel).read_bytes()
  if sha(data)!=h:raise ValueError('payload '+rel)
  ov[rel]=data
 rel='src/fallout_shared/imagespacemodifierinstance_effects.h';before=ov[rel];t=before.decode('utf8')
 for n in ('DRB','DOF'):
  a='class ImageSpaceModifierInstance'+n+' : public ImageSpaceModifierInstanceTemp, public NiMemObjectAllocation';b='class ImageSpaceModifierInstance'+n+' : public ImageSpaceModifierInstanceTemp'
  if t.count(a)!=1:raise ValueError('declaration '+n)
  t=t.replace(a,b)
 for op in ('new','delete'):
  a='using NiMemObjectAllocation::operator '+op+';';b='using NiMemObject::operator '+op+';'
  if t.count(a)!=2:raise ValueError('operator '+op)
  t=t.replace(a,b)
 ov[rel]=t.encode('utf8');units=json.loads(recipe)['units'];u=units[773]
 if len(u['functions'])!=39:raise ValueError('unit shape')
 old=dict(ov);old[rel]=before;orig=core.walk(F,u['source'],old);cand=core.walk(F,u['source'],ov)
 O.mkdir();p=O/'payload'/rel;p.parent.mkdir(parents=True);p.write_bytes(ov[rel])
 data={'parent_manifest_sha256':sha(parent),'recipe_sha256':sha(recipe),'proof_index_sha256':sha(idx),'unit':773,'source':u['source'],'flags':u['flags'],'functions':u['functions'],'eh_tails':u.get('eh_tails',[]),'changed_source':rel,'before_sha256':sha(before),'after_sha256':sha(ov[rel]),'parent_closure':orig,'candidate_closure':cand,'limitations':['private hypothesis; no compiler, placement or runtime','allocation symbol identity and call/cleanup contracts require source-backed verification','all 39 functions, ordinary EH, complete RTTI and native ownership require independent proof']}
 (O/'manifest.json').write_text(json.dumps(data,indent=2)+'\n');print(sha((O/'manifest.json').read_bytes()))
if __name__=='__main__':main()
