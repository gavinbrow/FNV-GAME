"""Stage evidence-based pointer and const contracts for existing class hypotheses."""
import copy,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;O=M/'out/phase2-class-typed-v1';T=M/'out/phase2-tesform-savegame-slot';B=M/'out/phase2-bgsencounterzone-slot21-corrected'
def sha(b):return hashlib.sha256(b).hexdigest()
def once(s,a,b):
 if s.count(a)!=1:raise ValueError('expected one anchor '+a[:80])
 return s.replace(a,b,1)
def main():
 tm=json.loads((T/'manifest.json').read_text());bm=json.loads((B/'manifest.json').read_text());
 files={'tesform.cpp':(T/'tesform.cpp').read_bytes(),'tesform_TESForm.h':(T/'tesform_TESForm.h').read_bytes(),'bgsencounterzone_TESForm.h':(T/'bgsencounterzone_TESForm.h').read_bytes(),'bgsencounterzone.cpp':(B/'bgsencounterzone.cpp').read_bytes(),'bgsencounterzone_decls.h':(B/'bgsencounterzone_decls.h').read_bytes()}
 for n,b in files.items():
  expected=tm['outputs'].get(n) if n in tm['outputs'] else bm['source_overlay_sha256' if n=='bgsencounterzone.cpp' else 'header_overlay_sha256']
  if sha(b)!=expected:raise ValueError('input digest changed '+n)
 s={n:b.decode('utf-8-sig').replace('\r\n','\n') for n,b in files.items()}
 for n in ('tesform_TESForm.h','bgsencounterzone_TESForm.h'):
  s[n]=once(s[n],'class TESForm : public BaseFormComponent','struct BGSSaveFormBuffer;\nclass TESForm : public BaseFormComponent')
  s[n]=once(s[n],'virtual void Unk_15(void* arg);','virtual void Unk_15(BGSSaveFormBuffer* arg);')
  for k in ('2C','26'):s[n]=once(s[n],'virtual bool Unk_'+k+'(void);','virtual bool Unk_'+k+'(void) const;')
 s['bgsencounterzone_decls.h']=once(s['bgsencounterzone_decls.h'],'virtual void Unk_15(void* apSaveGameBuffer);','virtual void Unk_15(BGSSaveFormBuffer* apSaveGameBuffer);')
 s['bgsencounterzone.cpp']=once(s['bgsencounterzone.cpp'],'void BGSEncounterZone::Unk_15(void* apSaveGameBuffer)','void BGSEncounterZone::Unk_15(BGSSaveFormBuffer* apSaveGameBuffer)')
 # Keep cast spelling in the body: the compiler comparison judges codegen.
 for k in ('2C','26'):s['tesform.cpp']=once(s['tesform.cpp'],'bool TESForm::Unk_'+k+'()','bool TESForm::Unk_'+k+'() const')
 tmeta=copy.deepcopy(tm);bmeta=copy.deepcopy(bm)
 replacements={'0x00401210':'?Unk_2C@TESForm@@UBE_NXZ','0x00549580':'?Unk_26@TESForm@@UBE_NXZ','0x00526410':'?Unk_15@BGSEncounterZone@@UAEXPAUBGSSaveFormBuffer@@@Z'}
 for m in (tmeta,bmeta):
  for x in m['proposed_function_symbol_changes']:
   if x['address'] in replacements:x['after']=replacements[x['address']]
 O.mkdir(exist_ok=False);out={}
 for n,text in s.items():
  b=text.encode();(O/n).write_bytes(b);out[n]=sha(b)
 (O/'tesform-manifest.json').write_text(json.dumps(tmeta,indent=2));(O/'bgs-manifest.json').write_text(json.dumps(bmeta,indent=2))
 meta={'inputs':{n:sha(b) for n,b in files.items()},'outputs':out,'evidence':['unit2 original FUN_00526410::SaveGame(BGSSaveFormBuffer*)','unit998 original FUN_00401210_shell::HasFlag() const','unit998 original FUN_00549580_shell::FUN_00549580() const'],'scope':'local two-TU reconstruction; other TESForm definitions are not established as compatible','status':'uncompiled hypothesis: require unchanged all 128+24 code/reference, vtable slots, EH/thunks, actual production labels and full image gates'}
 (O/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps(out))
if __name__=='__main__':main()
