"""Private lookup-restoration experiment; retains all existing adapter bases."""
import hashlib,json
from pathlib import Path
import baseformcomponent_core_stage as core
M=Path(__file__).resolve().parent.parent;F=M.parent.parent/'fnv_decomp';P=M/'out/phase2-nimem-combined-825d';O=M/'out/phase2-nimem-adapter-using-v2'
PIN='6b9dc1950f489c696364820186a4beba3e1618d127c4a656ecb677b53e32e1a3';BASE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68'
FILES={
 'src/bsshader/bsshaderlightingproperty_types_BSShaderLightingProperty.h':('b28cb6597405e4aaeda991d8a1bb583be77e1c37819d1fb765ae51798c6836e5',[('class BSShaderLightingProperty : public BSShaderProperty, public NiMemObjectAllocation',False)]),
 'src/bsshader/shadowscenelight.cpp':('7cc03bda111d384f4c37f07cc727ec0965df452ca53bb92976411885a29cc472',[('struct FUN_00a712f0 : ShadowObject, NiMemObjectAllocation',False)]),
 'src/fallout_shared/imagespacemodifierinstance.cpp':('dc32452404aa27eaab3659fad2969ef2980fbdb0e9d25239c879604aeba187f0',[('class ImageSpaceModifierInstanceForm : public ImageSpaceModifierInstance, public NiMemObjectAllocation',True),('class ImageSpaceModifierInstanceRB : public ImageSpaceModifierInstanceTemp, public NiMemObjectAllocation',True)]),
 'src/fallout_shared/imagespacemodifierinstance_effects.h':('b4dee10c39da2f0846397119a0b47b96ad2bcc3bfad798bc61abce015f1d6685',[('class ImageSpaceModifierInstanceDRB : public ImageSpaceModifierInstanceTemp, public NiMemObjectAllocation',True),('class ImageSpaceModifierInstanceDOF : public ImageSpaceModifierInstanceTemp, public NiMemObjectAllocation',True)])}
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve evidence')
 raw=(F/'build/units.json').read_bytes()
 if sha(raw)!=BASE or sha((P/'manifest.json').read_bytes())!=PIN:raise ValueError('recipe or combined proposal changed')
 cm=json.loads((P/'manifest.json').read_bytes());units=json.loads(raw)['units'];overrides={}
 for rel,h in cm['source_payload_sha256'].items():
  data=(P/'payload'/rel).read_bytes()
  if sha(data)!=h:raise ValueError('combined payload changed')
  overrides[rel]=data
 changed=[]
 for rel,(pin,classes) in FILES.items():
  before=(F/rel).read_bytes()
  if sha(before)!=pin:raise ValueError('source changed '+rel)
  text=before.decode('utf-8');nl='\r\n' if '\r\n' in text else '\n'
  for declaration,delete in classes:
   marker=declaration+nl+'{'+nl
   if text.count(marker)!=1:raise ValueError('nonunique class '+declaration)
   using='  public:'+nl+'    using NiMemObjectAllocation::operator new;'+nl
   if delete:using+='    using NiMemObjectAllocation::operator delete;'+nl
   text=text.replace(marker,marker+using,1)
  after=text.encode('utf-8');overrides[rel]=after;changed.append({'path':rel,'before_sha256':pin,'after_sha256':sha(after),'classes':[x[0] for x in classes]})
 rows=[]
 for i in (128,129,191,773):
  u=units[i];original=core.walk(F,u['source'],{});candidate=core.walk(F,u['source'],overrides)
  rows.append({'unit':i,'source':u['source'],'compiler':u['compiler'],'flags':u['flags'],'functions':u['functions'],'eh_tails':u.get('eh_tails',[]),'original':original,'candidate':candidate})
 O.mkdir()
 for rel,b in overrides.items():
  q=O/'payload'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 m={'base_recipe_sha256':BASE,'combined_proposal_sha256':PIN,'source_payload_sha256':{k:sha(v) for k,v in overrides.items()},'adapter_changes':changed,'units':rows,'limits':['private using-declaration lookup hypothesis only; original bases and class fields preserved','128/191 retain their existing unsized adapter delete; 773 retains sized delete including unwind cleanup','adapter identity is not established as native class; full mapped functions, EH, layout and generated wrappers require independent comparison','unit129 requires separately captured current production object']}
 (O/'manifest.json').write_text(json.dumps(m,indent=2));print(sha((O/'manifest.json').read_bytes()))
if __name__=='__main__':main()
