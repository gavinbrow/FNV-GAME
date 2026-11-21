"""Align three BGSE-local TESForm method names with source-native declarations."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M.parent.parent;A=M/'out/phase2-tesform-savegame-slot';O=M/'out/phase2-tesform-three-setter-alignment';F=P/'fnv_decomp'
def sha(b):return hashlib.sha256(b).hexdigest()
def rep(s,a,b):
 if s.count(a)!=1:raise ValueError('anchor mismatch')
 return s.replace(a,b,1)
def main():
 m=json.loads((A/'manifest.json').read_bytes());files={n:(A/n).read_bytes() for n in m['outputs']}
 if any(sha(files[n])!=v for n,v in m['outputs'].items()):raise ValueError('input changed')
 actual=(F/'src/fallout_shared/tesform_TESForm.h').read_text();s=files['bgsencounterzone_TESForm.h'].decode();changes=[]
 for slot,old,new in [(52,'Unk_34','SetFormFlag40'),(53,'Unk_35','SetHavokDeath'),(54,'Unk_36','SetNeedToChangeProcess')]:
  decl='    virtual void '+new+'(bool set);'
  if actual.count(decl)!=1:raise ValueError('native declaration changed '+new)
  s=rep(s,'    virtual void '+old+'(bool set);',decl);changes.append({'slot':slot,'before':old,'after':new,'signature':'void(bool)'})
 files['bgsencounterzone_TESForm.h']=s.encode();O.mkdir(parents=False,exist_ok=False)
 for n,b in files.items():(O/n).write_bytes(b)
 m.update(scope='private BGSE-local TESForm setter name alignment on prior hypotheses',outputs={n:sha(b) for n,b in files.items()},setter_name_alignments=changes,status='uncompiled; 128+24 strict and 78-slot graph required');m['risks']+=['all local class declarations require global ODR review','caller source compatibility and production code/relocation identity remain unverified']
 (O/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps({'header_sha256':sha(files['bgsencounterzone_TESForm.h']),'names':len(changes)}))
if __name__=='__main__':main()
