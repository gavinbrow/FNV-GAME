"""Bounded private BGSE InitializeComponent/LoadForm override hypothesis."""
import hashlib,json,re
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;PROJECT=M.parent.parent;PRIOR=M/'out/phase2-bgsencounterzone-combined';OUT=M/'out/phase2-bgsencounterzone-initload-v2'
SRC_SHA='34be62691a517c9cb81a2f8d84f509b852d0243aa1f58f33c5416899c47bbd8c';HDR_SHA='d000c5fb3ebed95971f5a83279a4a96c400fc8a4ae955374bb27c682af110c03'


def sha(b):return hashlib.sha256(b).hexdigest()

def replace_once(data,old,new,label):
 if data.count(old)!=1:raise ValueError('expected exactly one '+label+' anchor')
 return data.replace(old,new,1)

def transform(source,header):
 if re.search(r'BGSEncounterZone\s*::\s*(?:InitializeComponent|LoadForm)\s*\(',source):raise ValueError('native override definition already exists')
 if re.search(r'\bvirtual\s+(?:void\s+InitializeComponent|bool\s+LoadForm)\s*\(',header):raise ValueError('native override already declared')
 source=replace_once(source,'    ResetFormData();\n','    BGSEncounterZone::InitializeComponent();\n','constructor call')
 source=replace_once(source,'void BGSEncounterZone::ResetFormData()','void BGSEncounterZone::InitializeComponent()','initialize definition')
 source=replace_once(source,'bool BGSEncounterZone::Load(TESFile* file)','bool BGSEncounterZone::LoadForm(TESFile* file)','load definition')
 header=replace_once(header,'    void ResetFormData();\n','    virtual void InitializeComponent();\n','initialize declaration')
 header=replace_once(header,'    bool Load(TESFile* file);\n','    virtual bool LoadForm(TESFile* file);\n','load declaration')
 return source,header


def main():
 m=json.loads((PRIOR/'manifest.json').read_text());sp=PRIOR/'bgsencounterzone.cpp';hp=PRIOR/'bgsencounterzone_decls.h';s=sp.read_bytes();h=hp.read_bytes();up=PROJECT/'fnv_decomp/build/units.json';ub=up.read_bytes()
 if sha(s)!=SRC_SHA or sha(h)!=HDR_SHA or m['source_overlay_sha256']!=SRC_SHA or m['header_overlay_sha256']!=HDR_SHA or sha(ub)!=m['input_sha256']['units']:raise ValueError('prior inputs changed')
 unit=json.loads(ub)['units'][2];expected=[('0x00525d00','?ResetFormData@BGSEncounterZone@@QAEXXZ','?InitializeComponent@BGSEncounterZone@@UAEXXZ'),('0x00525d40','?Load@BGSEncounterZone@@QAE_NPAVTESFile@@@Z','?LoadForm@BGSEncounterZone@@UAE_NPAVTESFile@@@Z')];extra=[]
 for va,old,new in expected:
  found=[f for f in unit['functions'] if f['address']==va]
  if len(found)!=1 or found[0]['symbol']!=old:raise ValueError('unexpected original function symbol '+va)
  extra.append({'address':va,'before':old,'after':new,'size':found[0]['size']})
 ss,hh=transform(s.decode('utf8'),h.decode('utf8'));sb=ss.encode();hb=hh.encode();OUT.mkdir(parents=False,exist_ok=False)
 with (OUT/'bgsencounterzone.cpp').open('xb') as f:f.write(sb)
 with (OUT/'bgsencounterzone_decls.h').open('xb') as f:f.write(hb)
 result={'schema_version':1,'scope':'private source-supported slot5/slot8 override hypothesis, not ABI or global ODR proof',
  'input_sha256':dict(m['input_sha256'],prior_combined_source=SRC_SHA,prior_combined_header=HDR_SHA),
  'unit_index':2,'source':unit['source'],'compiler':unit['compiler'],'flags':unit['flags'],
  'proposed_function_symbol_changes':m['proposed_function_symbol_changes']+extra,'proposed_external_symbol_alias':m['proposed_external_symbol_alias'],
  'original_include_closure':m['original_include_closure'],'system_includes':m['system_includes'],
  'source_overlay_sha256':sha(sb),'header_overlay_sha256':sha(hb),
  'source_evidence':['slot 5 reference target 0x00525d00 is unit2 ResetFormData','slot 8 reference target 0x00525d40 is unit2 Load(TESFile*)','base class declares virtual InitializeComponent() and LoadForm(TESFile*)'],
  'known_risks':['unverified override semantics and method-call compatibility across all TUs','possible compiler code and relocation changes including constructor direct dispatch','other BGSE definitions differ; global ODR not established','vtable slots, base class and deleting destructor remain incomplete'],
  'status':'uncompiled hypothesis; verify all 24 original functions and all observed vtable slots; no protected source or recipe modification'}
 with (OUT/'manifest.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
 print(json.dumps({'source_sha256':result['source_overlay_sha256'],'header_sha256':result['header_overlay_sha256'],'functions_remapped':len(result['proposed_function_symbol_changes'])}))

if __name__=='__main__':main()
