"""Stage one canonical public native header plus local forwarding wrapper per BGS class."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';P=M/'out/phase2-bgsbodypart-native-destructor-rebase6757';O=M/'out/phase2-bgs-native-header-forwarders-v2';sys.path.insert(0,str(H));import baseformcomponent_core_stage as core
BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';NAMES=('FileEntryList_native.h','TESModel_native.h','TESModelPSA_native.h','BodyPartInfo_native.h','BGSBodyPart_native.h')
def sha(x):return hashlib.sha256(x).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve prior proposal')
 recipe=(F/'build/units.json').read_bytes();f=json.loads((P/'manifest.json').read_text());doc=json.loads(recipe)
 if sha(recipe)!=BASE or f['semantic_rebase']['new_units_sha256']!=BASE:raise ValueError('recipe differs')
 for n,h in f['outputs'].items():
  if sha((P/n).read_bytes())!=h:raise ValueError('tested payload differs '+n)
 originals={};candidate={}
 for n in NAMES:
  a=(P/'620'/n).read_bytes();b=(P/'621'/n).read_bytes()
  if a!=b:raise ValueError('620/621 header copies differ '+n)
  local='src/fallout_shared/'+n;public='include/'+n
  if (F/local).exists() or (F/public).exists():raise ValueError('native target exists '+n)
  originals[local]=a;candidate[public]=a
  guard='FNV_LOCAL_FORWARD_'+n.replace('.','_').upper();pre={'FileEntryList_native.h':['layout_support.h'],'TESModel_native.h':['BaseFormComponent.h','FileEntryList_native.h'],'TESModelPSA_native.h':['TESModel_native.h'],'BodyPartInfo_native.h':['NiPoint3.h'],'BGSBodyPart_native.h':['TESModelPSA_native.h','BodyPartInfo_native.h']}[n];candidate[local]=('#ifndef '+guard+'\n#define '+guard+'\n'+''.join('#include "'+x+'"\n' for x in pre)+'#include "../../include/'+n+'"\n#endif\n').encode()
 for i,source,header in ((620,'bgsbodypart.cpp','bgsbodypart_decls.h'),(621,'bgsbodypartdata.cpp','bgsbodypartdata.h')):
  for n in (source,header):
   rel='src/fallout_shared/'+n;data=(P/str(i)/n).read_bytes();originals[rel]=data;candidate[rel]=data
 units=[]
 for i in (620,621):
  u=doc['units'][i];a=core.walk(F,u['source'],originals);b=core.walk(F,u['source'],candidate)
  for n in NAMES:
   local='src/fallout_shared/'+n;public='include/'+n
   if local in a['files'] and public not in b['files']:raise ValueError('canonical path missing '+str((i,n)))
  units.append({'unit':i,'source':u['source'],'compiler':u['compiler'],'flags':u['flags'],'functions':len(u['functions']),'eh_tails':len(u.get('eh_tails',[])),'prior':a,'forwarded':b})
 O.mkdir();
 for tag,overrides in [('prior',originals),('forwarded',candidate)]:
  for rel,data in overrides.items():
   q=O/'payload'/tag/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
  for row in units:
   for rel,digest in row[tag]['files'].items():
    data=overrides[rel] if rel in overrides else (F/rel).read_bytes()
    if sha(data)!=digest:raise ValueError('input changed '+rel)
    q=O/str(row['unit'])/tag/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
 result={'base_recipe_sha256':BASE,'tested_fixture_manifest_sha256':sha((P/'manifest.json').read_bytes()),'classes':list(NAMES),'canonical_definition_paths':['include/'+n for n in NAMES],'local_forwarder_paths':['src/fallout_shared/'+n for n in NAMES],'prior_and_forwarded_share_identical_class_header_bytes':True,'units':units,'limits':['private logical include graph; compiler showIncludes and guard/pack histories not yet verified','production source and native headers untouched','only unit 620/621 candidate contexts captured, not all existing TESModel or other native class views','all functions, ordinary EH, weak/RTTI ownership, production-label and final-image gates remain']}
 (O/'manifest.json').write_text(json.dumps(result,indent=2));print(json.dumps({'units':[620,621],'headers':len(NAMES),'counts':[(x['unit'],len(x['prior']['files']),len(x['forwarded']['files'])) for x in units]}))
if __name__=='__main__':main()
