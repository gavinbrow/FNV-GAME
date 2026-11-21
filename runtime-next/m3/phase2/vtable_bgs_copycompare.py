"""Produce a private, hash-bound BGSE CopyFrom/Compare override hypothesis."""
import hashlib, json
from pathlib import Path
H=Path(__file__).resolve().parent; M=H.parent; ROOT=M.parent.parent
PRIOR=M/'out/phase2-bgsencounterzone-combined'; OUT=M/'out/phase2-bgsencounterzone-copycompare'
S='34be62691a517c9cb81a2f8d84f509b852d0243aa1f58f33c5416899c47bbd8c'; D='d000c5fb3ebed95971f5a83279a4a96c400fc8a4ae955374bb27c682af110c03'
def sha(b): return hashlib.sha256(b).hexdigest()
def replace(s,a,b):
 if s.count(a)!=1: raise ValueError('anchor mismatch: '+a[:70])
 return s.replace(a,b,1)
def main():
 m=json.loads((PRIOR/'manifest.json').read_text()); sb=(PRIOR/'bgsencounterzone.cpp').read_bytes(); hb=(PRIOR/'bgsencounterzone_decls.h').read_bytes(); ub=(ROOT/'fnv_decomp/build/units.json').read_bytes()
 if sha(sb)!=S or sha(hb)!=D or m['source_overlay_sha256']!=S or m['header_overlay_sha256']!=D or sha(ub)!=m['input_sha256']['units']: raise ValueError('input mismatch')
 u=json.loads(ub)['units'][2]; s=sb.decode(); h=hb.decode()
 h=replace(h,'    virtual ~BGSEncounterZone();\n','    virtual ~BGSEncounterZone();\n    virtual void CopyFrom(const TESForm* source);\n    virtual bool Compare(TESForm* other);\n')
 s=replace(s,'struct ZoneComparison : BGSEncounterZone\n{\n    bool FUN_00526000(TESForm* other);\n};\n','')
 s=replace(s,'bool ZoneComparison::FUN_00526000(TESForm* other)','bool BGSEncounterZone::Compare(TESForm* other)')
 s=replace(s,'struct EncounterZoneCopy : BGSEncounterZone\n{\n    void FUN_00525fa0(TESForm* source);\n};\n\n','')
 s=replace(s,'void EncounterZoneCopy::FUN_00525fa0(TESForm* source)','void BGSEncounterZone::CopyFrom(const TESForm* source)')
 s=replace(s,'dynamic_cast<BGSEncounterZone*>(source)','dynamic_cast<BGSEncounterZone*>(const_cast<TESForm*>(source))')
 extra=[]
 for va,old,new in [('0x00525fa0','?FUN_00525fa0@EncounterZoneCopy@@QAEXPAVTESForm@@@Z','?CopyFrom@BGSEncounterZone@@UAEXPBVTESForm@@@Z'),('0x00526000','?FUN_00526000@ZoneComparison@@QAE_NPAVTESForm@@@Z','?Compare@BGSEncounterZone@@UAE_NPAVTESForm@@@Z')]:
  matches=[f for f in u['functions'] if f['address']==va]
  if len(matches)!=1 or matches[0]['symbol']!=old: raise ValueError('recipe mismatch '+va)
  extra.append({'address':va,'before':old,'after':new,'size':matches[0]['size']})
 ss=s.encode(); hh=h.encode(); OUT.mkdir(parents=False,exist_ok=False)
 (OUT/'bgsencounterzone.cpp').write_bytes(ss); (OUT/'bgsencounterzone_decls.h').write_bytes(hh)
 result=dict(m); result.update(scope='private CopyFrom/Compare override hypothesis; no protected source change', proposed_function_symbol_changes=m['proposed_function_symbol_changes']+extra,source_overlay_sha256=sha(ss),header_overlay_sha256=sha(hh),status='uncompiled; all 24 functions, full prefix and ODR remain to be verified',known_risks=m['known_risks']+['CopyFrom base const differs from source shell; cast preserves current shell behavior, not proven semantic signature','surrogate removal may affect external source users or compiler RTTI and symbols'])
 (OUT/'manifest.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps({'source':sha(ss),'header':sha(hh),'remaps':len(result['proposed_function_symbol_changes'])}))
if __name__=='__main__': main()
