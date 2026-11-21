"""Produce isolated BGSEncounterZone virtual-override experiment; never edit source.

This is a hypothesis generator, not a semantic or binary-match claim. Output
contains copied game-derived source, so it is confined to ignored m3/out.
"""
import hashlib,json,re
from pathlib import Path
H=Path(__file__).resolve().parent; M=H.parent; ROOT=M.parent.parent
FN=ROOT/'fnv_decomp'
SRC=FN/'src/bgsencounterzone.cpp'; HDR=FN/'src/bgsencounterzone_decls.h'; UNITS=FN/'build/units.json'
EXPECTED={'src':'30208087bcd67f1183736ce74dfdd8d35afd76fb924eb7c7f9eabe7ea6a031ee','hdr':'4016f5fee6890cfca0035f1d9cfe33f7da34db8f90a38edd2f67a9036c9bf7b1','units':'ae4182c8062cf566210935d284b6663a83ab63e077b41d8e147fa66cb7aca70e'}
def sha(b):return hashlib.sha256(b).hexdigest()
def replace_once(data,old,new):
 if data.count(old)!=1:raise ValueError('expected exactly one source anchor: '+old[:80])
 return data.replace(old,new,1)
def main():
 raw={k:p.read_bytes() for k,p in [('src',SRC),('hdr',HDR),('units',UNITS)]}
 for k in raw:
  if sha(raw[k])!=EXPECTED[k]:raise ValueError('input digest changed: '+k)
 src=raw['src'].decode('utf8').replace('\r\n','\n');hdr=raw['hdr'].decode('utf8').replace('\r\n','\n');units=json.loads(raw['units'])['units'];u=units[2]
 if u['source']!='src/bgsencounterzone.cpp' or u['compiler']!='sp1':raise ValueError('unit mismatch')
 hdr=replace_once(hdr,'    virtual ~BGSEncounterZone();\n','    virtual ~BGSEncounterZone();\n    virtual void LoadGame(void* apLoadGameBuffer);\n    virtual void Revert(unsigned int pLoadBuffer);\n')
 old='''struct FUN_00526570_shell : BGSEncounterZone
{
    void RevertAndClearIfChanged(BGSLoadFormBuffer* buf);
};
// @fnv 0x00526570
void FUN_00526570_shell::RevertAndClearIfChanged(BGSLoadFormBuffer* pLoadBuffer)
{
    TESForm::Revert(reinterpret_cast<unsigned int>(pLoadBuffer));
    if (pLoadBuffer->GetOldChangeFlags(0x80000000))
        memset((char*)this + 0x20, 0, 0x10);
}
}  // namespace fnv_00526570'''
 new='''}  // namespace fnv_00526570

// @fnv 0x00526570
void BGSEncounterZone::Revert(unsigned int pLoadBuffer)
{
    TESForm::Revert(pLoadBuffer);
    if (reinterpret_cast<fnv_00526570::BGSLoadFormBuffer*>(pLoadBuffer)->GetOldChangeFlags(0x80000000))
        memset((char*)this + 0x20, 0, 0x10);
}'''
 src=replace_once(src,old,new)
 old='''struct FUN_005264a0_shell : public BGSEncounterZone
{
    void FUN_005264a0(BGSLoadFormBuffer* apLoadGameBuffer);
};

// Loads the encounter zone from the buffer, reading a flag byte and, for version 8+, a 16-byte field at offset 0x20.
// @fnv 0x005264a0
void FUN_005264a0_shell::FUN_005264a0(BGSLoadFormBuffer* apLoadGameBuffer)'''
 new='''// Loads the encounter zone from the buffer, reading a flag byte and, for version 8+, a 16-byte field at offset 0x20.
// @fnv 0x005264a0
void BGSEncounterZone::LoadGame(void* apLoadGameBuffer)'''
 src=replace_once(src,old,new)
 start=src.index('void BGSEncounterZone::LoadGame(void* apLoadGameBuffer)');end=src.index('\n}',start)+2
 body=src[start:end];count=body.count('apLoadGameBuffer->')
 if count!=6:raise ValueError('unexpected load-game pointer access count: %d'%count)
 body=body.replace('apLoadGameBuffer->','reinterpret_cast<BGSLoadFormBuffer*>(apLoadGameBuffer)->');src=src[:start]+body+src[end:]
 expected={'0x005264a0':('?FUN_005264a0@FUN_005264a0_shell@@QAEXPAUBGSLoadFormBuffer@@@Z','?LoadGame@BGSEncounterZone@@UAEXPAX@Z'),'0x00526570':('?RevertAndClearIfChanged@FUN_00526570_shell@fnv_00526570@@QAEXPAUBGSLoadFormBuffer@2@@Z','?Revert@BGSEncounterZone@@UAEXI@Z')}
 proposal=[]
 for addr,(old,new) in expected.items():
  matches=[f for f in u['functions'] if f['address'].lower()==addr]
  if len(matches)!=1 or matches[0]['symbol']!=old:raise ValueError('recipe symbol mismatch '+addr)
  proposal.append({'address':addr,'before':old,'after':new,'size':matches[0]['size']})
 out=M/'out/phase2-bgsencounterzone-overlay';out.mkdir(parents=True,exist_ok=False)
 for path,text in [('bgsencounterzone.cpp',src),('bgsencounterzone_decls.h',hdr)]: (out/path).write_bytes(text.encode('utf8'))
 meta={'scope':'isolated exploratory virtual override overlay; not a source installation or native-layout claim','input_sha256':EXPECTED,'unit_index':2,'source':u['source'],'compiler':u['compiler'],'flags':u['flags'],'functions':proposal,'source_overlay_sha256':sha(src.encode()),'header_overlay_sha256':sha(hdr.encode()),'status':'uncompiled hypothesis','known_risks':['surrogate base parameter types may be wrong','all virtual slots, base layout and RTTI not yet established','code bytes and relocations not verified','recipe symbols not changed']}
 (out/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf8');print(json.dumps(meta,indent=2))
if __name__=='__main__':main()


