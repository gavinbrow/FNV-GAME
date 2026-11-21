"""Correct the private BGSE save-buffer method to inherited slot21 ABI."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;A=M/'out/phase2-bgsencounterzone-six-override';O=M/'out/phase2-bgsencounterzone-slot21-corrected'
def sha(b):return hashlib.sha256(b).hexdigest()
def rep(s,a,b):
 if s.count(a)!=1:raise ValueError('anchor mismatch '+a[:60])
 return s.replace(a,b,1)
def main():
 m=json.loads((A/'manifest.json').read_bytes());s=(A/'bgsencounterzone.cpp').read_bytes();h=(A/'bgsencounterzone_decls.h').read_bytes()
 if sha(s)!=m['source_overlay_sha256'] or sha(h)!=m['header_overlay_sha256'] or sha(s)!='d5fdb1588f3815c090bed42f69734f03d0993d6bdcb0c669c814eb0f142e7105' or sha(h)!='0cbd8a852338f8dbda44010fd324b698182f4016c187cba21d5c5953572893d7':raise ValueError('source mismatch')
 s=rep(s.decode(),'void BGSEncounterZone::SaveGame(unsigned int apSaveGameBuffer)','void BGSEncounterZone::Unk_15(void* apSaveGameBuffer)').encode();h=rep(h.decode(),'    virtual void SaveGame(unsigned int apSaveGameBuffer);','    virtual void Unk_15(void* apSaveGameBuffer);').encode()
 changes=m['proposed_function_symbol_changes'];x=[x for x in changes if x['address']=='0x00526410']
 if len(x)!=1 or x[0]['after']!='?SaveGame@BGSEncounterZone@@UAEXI@Z':raise ValueError('prior mapping changed')
 x[0]['after']='?Unk_15@BGSEncounterZone@@UAEXPAX@Z';O.mkdir(parents=False,exist_ok=False);(O/'bgsencounterzone.cpp').write_bytes(s);(O/'bgsencounterzone_decls.h').write_bytes(h)
 m.update(scope='private slot21 correction and prior overrides; source/ABI hypothesis',source_overlay_sha256=sha(s),header_overlay_sha256=sha(h),status='uncompiled; all 24 functions, 78 slots, caller compatibility and ODR remain open')
 m['known_risks'].append('slot21 inherited void* buffer type matches source shell pointer width, not fully proven pointee semantics; slot22 intentionally inherited')
 (O/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps({'source':sha(s),'header':sha(h),'remaps':len(changes)}))
if __name__=='__main__':main()
