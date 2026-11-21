"""Private save-override hypotheses based on the copy/compare overlay."""
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;ROOT=M.parent.parent
PRIOR=M/'out/phase2-bgsencounterzone-copycompare'; OUT=M/'out/phase2-bgsencounterzone-save'
def sha(b):return hashlib.sha256(b).hexdigest()
def rep(s,a,b):
 if s.count(a)!=1:raise ValueError('anchor mismatch '+a[:60])
 return s.replace(a,b,1)
def main():
 m=json.loads((PRIOR/'manifest.json').read_text()); sb=(PRIOR/'bgsencounterzone.cpp').read_bytes();hb=(PRIOR/'bgsencounterzone_decls.h').read_bytes();ub=(ROOT/'fnv_decomp/build/units.json').read_bytes()
 if sha(sb)!='c6947b2916c886de25f6c46afed65b5f89fded3faadb5565c1a8fa3334a43dcf' or sha(hb)!='f34b7fdfa2f30a024a3fe2b112048fe7433f19f846eebf6d735b58df5179a3f3' or sha(ub)!=m['input_sha256']['units']:raise ValueError('input changed')
 s=sb.decode();h=hb.decode();u=json.loads(ub)['units'][2]
 h=rep(h,'    virtual ~BGSEncounterZone();\n','    virtual ~BGSEncounterZone();\n    virtual void SaveForm();\n    virtual void SaveGame(unsigned int apSaveGameBuffer);\n')
 s=rep(s,'struct FUN_00525e70 : BGSEncounterZone\n{\n    void Save();\n};\n','');s=rep(s,'void FUN_00525e70::Save()','void BGSEncounterZone::SaveForm()')
 s=rep(s,'struct FUN_00526410 : BGSEncounterZone\n{\n    void SaveGame(BGSSaveFormBuffer* apSaveGameBuffer);\n};\n','');s=rep(s,'void FUN_00526410::SaveGame(BGSSaveFormBuffer* apSaveGameBuffer)','void BGSEncounterZone::SaveGame(unsigned int apSaveGameBuffer)')
 s=rep(s,'reinterpret_cast<S00484d60*>(this)->SaveIfChanged(apSaveGameBuffer);','reinterpret_cast<S00484d60*>(this)->SaveIfChanged(reinterpret_cast<BGSSaveFormBuffer*>(apSaveGameBuffer));')
 start=s.index('void BGSEncounterZone::SaveGame(unsigned int');end=s.index('\n}',start);body=s[start:end];
 if body.count('apSaveGameBuffer->')!=4:raise ValueError('buffer use count')
 s=s[:start]+body.replace('apSaveGameBuffer->','reinterpret_cast<BGSSaveFormBuffer*>(apSaveGameBuffer)->')+s[end:]
 extra=[]
 for va,old,new in [('0x00525e70','?Save@FUN_00525e70@@QAEXXZ','?SaveForm@BGSEncounterZone@@UAEXXZ'),('0x00526410','?SaveGame@FUN_00526410@@QAEXPAUBGSSaveFormBuffer@@@Z','?SaveGame@BGSEncounterZone@@UAEXI@Z')]:
  found=[f for f in u['functions'] if f['address']==va]
  if len(found)!=1 or found[0]['symbol']!=old:raise ValueError('recipe mismatch')
  extra.append(dict(address=va,before=old,after=new,size=found[0]['size']))
 ss=s.encode();hh=h.encode();OUT.mkdir(parents=False,exist_ok=False);(OUT/'bgsencounterzone.cpp').write_bytes(ss);(OUT/'bgsencounterzone_decls.h').write_bytes(hh)
 result=dict(m);result.update(scope='private SaveForm and SaveGame hypotheses stacked on CopyFrom/Compare',proposed_function_symbol_changes=m['proposed_function_symbol_changes']+extra,source_overlay_sha256=sha(ss),header_overlay_sha256=sha(hh),status='uncompiled; all 24 functions, full prefix and ODR remain unverified',known_risks=m['known_risks']+['SaveGame base unsigned int declaration differs from buffer pointer in shell; reinterpretation is an ABI hypothesis only'])
 (OUT/'manifest.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'source':sha(ss),'header':sha(hh),'remaps':len(result['proposed_function_symbol_changes'])}))
if __name__=='__main__':main()
