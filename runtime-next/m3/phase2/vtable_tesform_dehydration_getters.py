"""Stage private TESForm source-backed getters owned by dehydration unit633."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M.parent.parent;F=P/'fnv_decomp';O=M/'out/phase2-tesform-dehydration-getters'
PIN={'src/fallout_shared/bgsdehydration.cpp':'68e945720d7387e6f5963fc1667aa8df08e6244728b359044d8e1d1ca1bca32a','include/TESForm.h':'06cb9e74c6453e2eaeb334bed1d4327e141e3fff6b1eee2874114603829d57a0','src/fallout_shared/tesform_TESForm.h':'cd74c8de1d3240d13f183e75e1f7e6f4f2c669f13df12a3991f187080b5b948f','src/bgsencounterzone_TESForm.h':'8848ca9f59edf754bb8a68069ab9f3255b582f78d9b31ffd1d9af65afd0be7c2','build/units.json':'6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'}
def sha(x):return hashlib.sha256(x).hexdigest()
def rep(s,a,b):
 if s.count(a)!=1:raise ValueError('anchor mismatch '+a)
 return s.replace(a,b,1)
def main():
 raw={p:(F/p).read_bytes() for p in PIN}
 if any(sha(raw[p])!=h for p,h in PIN.items()):raise ValueError('input changed')
 u=json.loads(raw['build/units.json'])['units'][633];expected=[('0x00401190','?FUN_00401190@FUN_00401190_shell@@QAE_NXZ','?IsQuestItem@TESForm@@UAE_NXZ'),('0x00401230','?IsFlag40000000Set@FUN_00401230_shell@@QBE_NXZ','?Unk_2D@TESForm@@UBE_NXZ')];changes=[]
 for va,old,new in expected:
  f=[x for x in u['functions'] if x['address']==va]
  if len(f)!=1 or f[0]['symbol']!=old or f[0]['size']!=26:raise ValueError('source recipe mismatch')
  changes.append({'address':va,'before':old,'after':new,'size':26})
 source=raw['src/fallout_shared/bgsdehydration.cpp'].decode().replace('\r\n','\n');source=rep(source,'bool FUN_00401190_shell::FUN_00401190()','bool TESForm::IsQuestItem()');source=rep(source,'bool FUN_00401230_shell::IsFlag40000000Set() const','bool TESForm::Unk_2D() const')
 outputs={'bgsdehydration.cpp':source.encode()}
 for name in ('include/TESForm.h','src/fallout_shared/tesform_TESForm.h','src/bgsencounterzone_TESForm.h'):
  text=raw[name].decode().replace('\r\n','\n');text=rep(text,'virtual bool Unk_2D(void);','virtual bool Unk_2D(void) const;');outputs[name.replace('/','__')]=text.encode()
 O.mkdir(parents=False,exist_ok=False)
 for n,b in outputs.items():(O/n).write_bytes(b)
 m={'scope':'private unit633 source getters, not an installed class repair','input_sha256':PIN,'outputs':{n:sha(b) for n,b in outputs.items()},'unit_index':633,'function_count':len(u['functions']),'proposed_function_symbol_changes':changes,'evidence':['slot37 target 0x00401190 is TESForm-derived shell no-arg bool flags +8','slot45 target 0x00401230 is const no-arg bool flags +8','both ranges have sole recipe owner in unit633'],'limitations':['global TESForm header const change impacts many TUs and requires complete include/caller/ODR audit','exact all45 function bytes/relocations/reference and affected unit checks are pending','const correctness inferred from source shell; historical virtual identity is unresolved'],'status':'uncompiled hypothesis'}
 (O/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps({'unit_functions':len(u['functions']),'output_sha256':{n:sha(b) for n,b in outputs.items()}}))
if __name__=='__main__':main()
