"""Prepare source/ABI paired mirrors against the repaired production recipe."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;sys.path.insert(0,str(H));import rtti_mirror_prepare as r
B=M/'out/phase2-tesform-binding-repair-v3';T=M/'out/phase2-tesform-savegame-slot';G=M/'out/phase2-bgsencounterzone-slot21-corrected'
OLD='e883ac21f25808a7ebba172006e09ae803ae640bf12d389ad2c10641ddba1576';NEW='fa36603e3e9a2ea495644f383db983a9269d2e7cf558282a80746439386dbfc8'
def sha(b):return hashlib.sha256(b).hexdigest()
def readmeta(p):
 m=json.loads((p/'manifest.json').read_bytes());
 for name,digest in m.get('outputs',{}).items():
  if sha((p/name).read_bytes())!=digest:raise ValueError('candidate output changed '+name)
 return m
orig=r.transition
def transition(old,new,current):
 orig(old,new,new)
 a=(B/'units.original').read_bytes();b=(B/'units.generated').read_bytes()
 if sha(a)!=OLD or sha(b)!=NEW or a!=new or b!=current:raise ValueError('repaired recipe transition mismatch')
 x=json.loads(a);y=json.loads(b)
 if [i for i,(u,v) in enumerate(zip(x['units'],y['units'])) if u!=v]!=[998]:raise ValueError('unexpected unit changes')
 for k in x['units'][998]:
  if k!='symbols' and x['units'][998][k]!=y['units'][998][k]:raise ValueError('nonbinding unit change')
 return y
r.transition=transition
def main():
 tm=readmeta(T);bm=readmeta(G)
 if sha((G/'bgsencounterzone.cpp').read_bytes())!=bm['source_overlay_sha256'] or sha((G/'bgsencounterzone_decls.h').read_bytes())!=bm['header_overlay_sha256']:raise ValueError('BGSE candidate mismatch')
 sets=[('src/fallout_shared/tesform.cpp',{'src/fallout_shared/tesform.cpp':(T/'tesform.cpp').read_bytes(),'src/fallout_shared/tesform_TESForm.h':(T/'tesform_TESForm.h').read_bytes()},M/'out/phase2-tesform-savegame-mirror'),('src/bgsencounterzone.cpp',{'src/bgsencounterzone.cpp':(G/'bgsencounterzone.cpp').read_bytes(),'src/bgsencounterzone_decls.h':(G/'bgsencounterzone_decls.h').read_bytes(),'src/bgsencounterzone_TESForm.h':(T/'bgsencounterzone_TESForm.h').read_bytes()},M/'out/phase2-bgs-savegame-paired-mirror')]
 for src,overrides,out in sets:
  m=r.prepare(src,overrides,out);m['units_sha256']=NEW;m['reviewed_units_sha256']=OLD;m['binding_transition_evidence_sha256']=sha((B/'manifest.json').read_bytes());(out/'mirror-manifest.json').write_text(json.dumps(m,indent=2));print(json.dumps({'out':out.name,'unit_source':src,'original_files':len(m['original']['files']),'candidate_files':len(m['candidate']['files']),'recipe_sha256':m['units_sha256']}))
if __name__=='__main__':main()
