"""Add source-supported load-buffer pointer contracts to the typed hypothesis."""
import copy,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';I=M/'out/phase2-class-typed-v1';O=M/'out/phase2-class-typed-v3'
def sha(b):return hashlib.sha256(b).hexdigest()
def once(s,a,b):
 if s.count(a)!=1:raise ValueError('unexpected anchor '+a)
 return s.replace(a,b,1)
def main():
 prev=json.loads((I/'manifest.json').read_text());raw={n:(I/n).read_bytes() for n in prev['outputs']}
 for n,d in prev['outputs'].items():
  if sha(raw[n])!=d:raise ValueError('v1 input changed '+n)
 s={n:b.decode('utf8') for n,b in raw.items()}
 for n in ('tesform_TESForm.h','bgsencounterzone_TESForm.h'):
  s[n]=once(s[n],'struct BGSSaveFormBuffer;','struct BGSSaveFormBuffer;\nstruct BGSLoadFormBuffer;')
  s[n]=once(s[n],'virtual void LoadGame(void* arg);','virtual void LoadGame(BGSLoadFormBuffer* arg);')
  s[n]=once(s[n],'virtual void Revert(unsigned int changedFlags);','virtual void Revert(BGSLoadFormBuffer* buffer);')
 n='bgsencounterzone_decls.h';s[n]=once(s[n],'virtual void LoadGame(void* apLoadGameBuffer);','virtual void LoadGame(BGSLoadFormBuffer* apLoadGameBuffer);');s[n]=once(s[n],'virtual void Revert(unsigned int pLoadBuffer);','virtual void Revert(BGSLoadFormBuffer* pLoadBuffer);')
 n='bgsencounterzone.cpp';s[n]=once(s[n],'void BGSEncounterZone::LoadGame(void* apLoadGameBuffer)','void BGSEncounterZone::LoadGame(BGSLoadFormBuffer* apLoadGameBuffer)');s[n]=once(s[n],'void BGSEncounterZone::Revert(unsigned int pLoadBuffer)','void BGSEncounterZone::Revert(BGSLoadFormBuffer* pLoadBuffer)')
 s['tesform.cpp']=once(s['tesform.cpp'],'void TESForm::LoadGame(void* apLoadBuffer)','void TESForm::LoadGame(BGSLoadFormBuffer* apLoadBuffer)')
 tm=copy.deepcopy(json.loads((I/'tesform-manifest.json').read_text()));bm=copy.deepcopy(json.loads((I/'bgs-manifest.json').read_text()));f=[x for x in json.loads((F/'build/units.json').read_bytes())['units'][998]['functions'] if x['address']=='0x00484da0']
 if len(f)!=1 or f[0]['symbol']!='?LoadGame@TESForm@@UAEXPAX@Z':raise ValueError('base LoadGame definition changed')
 tm['proposed_function_symbol_changes'].append({'address':f[0]['address'],'before':f[0]['symbol'],'after':'?LoadGame@TESForm@@UAEXPAUBGSLoadFormBuffer@@@Z','size':f[0]['size']})
 mapping={'0x005264a0':'?LoadGame@BGSEncounterZone@@UAEXPAUBGSLoadFormBuffer@@@Z','0x00526570':'?Revert@BGSEncounterZone@@UAEXPAUBGSLoadFormBuffer@@@Z'}
 for x in bm['proposed_function_symbol_changes']:
  if x['address'] in mapping:x['after']=mapping[x['address']]
 unit=json.loads((F/'build/units.json').read_bytes())['units'][2];old={'?LoadGame@TESForm@@UAEXPAX@Z':'?LoadGame@TESForm@@UAEXPAUBGSLoadFormBuffer@@@Z','?Revert@TESForm@@UAEXI@Z':'?Revert@TESForm@@UAEXPAUBGSLoadFormBuffer@@@Z'};aliases=[]
 for a,b in old.items():
  if a not in unit['symbols']:raise ValueError('source-backed external binding absent')
  aliases.append({'before':a,'after':b,'address':unit['symbols'][a],'status':'proposed from same source call and original relocation; verify production code/fields'})
 O.mkdir(exist_ok=False);outputs={}
 for n,text in s.items():
  data=text.encode();(O/n).write_bytes(data);outputs[n]=sha(data)
 (O/'tesform-manifest.json').write_text(json.dumps(tm,indent=2));(O/'bgs-manifest.json').write_text(json.dumps(bm,indent=2))
 (O/'manifest.json').write_text(json.dumps({'inputs':{n:sha(b) for n,b in raw.items()},'outputs':outputs,'base_external_symbol_aliases':aliases,'scope':'source-supported BGSLoadFormBuffer pointer contracts in two local base views and derived methods; namespace adapter retained for distinct local surrogate','status':'uncompiled hypothesis; require all 128+24 function/relocation/reference, 78-slot, EH/thunk and global source compatibility checks'},indent=2));print(json.dumps(outputs))
if __name__=='__main__':main()
