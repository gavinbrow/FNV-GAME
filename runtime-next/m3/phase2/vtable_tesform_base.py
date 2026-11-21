"""Generate private TESForm base-slot 2/3 hypothesis, never modify source."""
import hashlib,json,re
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';OUT=M/'out/phase2-tesform-base-slots';BGS=M/'out/phase2-bgsencounterzone-six-override'
def sha(x):return hashlib.sha256(x).hexdigest()
def rep(s,a,b):
 if s.count(a)!=1:raise ValueError('anchor mismatch '+a[:80])
 return s.replace(a,b,1)
def main():
 paths=['src/fallout_shared/tesform.cpp','src/fallout_shared/tesform_TESForm.h','src/fallout_shared/tesform_calls.h','build/units.json']; raw={p:(F/p).read_bytes() for p in paths}; u=json.loads(raw[paths[3]])['units'][998]
 if u['source']!=paths[0] or len(u['functions'])!=128:raise ValueError('unit mismatch')
 src=raw[paths[0]].decode().replace('\r\n','\n');hdr=raw[paths[1]].decode().replace('\r\n','\n');bh=(BGS/'bgsencounterzone_decls.h').read_bytes();bm=json.loads((BGS/'manifest.json').read_text())
 if sha(bh)!=bm['header_overlay_sha256'] or sha(bh)!='0cbd8a852338f8dbda44010fd324b698182f4016c187cba21d5c5953572893d7':raise ValueError('BGSE input mismatch')
 declaration='    virtual void CopyFromBase(BaseFormComponent* apCopyFC);\n    virtual bool CompareWithBase(BaseFormComponent* apOther);\n'
 hdr=rep(hdr,'    virtual ~TESForm();\n','    virtual ~TESForm();\n'+declaration);bgs=rep(bh.decode(),'    virtual ~TESForm();\n','    virtual ~TESForm();\n'+declaration) if False else None
 # BGSE local TESForm declaration is a separate include, not its class header.
 bgst=(F/'src/bgsencounterzone_TESForm.h').read_bytes();bgsh=rep(bgst.decode().replace('\r\n','\n'),'    virtual ~TESForm();\n','    virtual ~TESForm();\n'+declaration)
 src=rep(src,'struct FUN_00485340_shell : public TESForm\n{\n    void FUN_00485340(BaseFormComponent* apCopyFC);\n};\n','')
 src=rep(src,'void FUN_00485340_shell::FUN_00485340(BaseFormComponent* apCopyFC)','}  // namespace fnv_00485340\nvoid TESForm::CopyFromBase(BaseFormComponent* apCopyFC)')
 start=src.index('void TESForm::CopyFromBase(');end=src.index('\n}',start)+2;body=src[start:end].replace('(Pathing*)','(fnv_00485340::Pathing*)').replace('(ArrSI*)','(fnv_00485340::ArrSI*)');src=src[:start]+body+src[end:];src=rep(src,'}\n}  // namespace fnv_00485340\n\nnamespace fnv_00436180','}\n\nnamespace fnv_00436180')
 src=rep(src,'    bool FUN_004853e0(BaseFormComponent* rhs);\n','');src=rep(src,'bool CompareForm::FUN_004853e0(BaseFormComponent* apOther)','bool TESForm::CompareWithBase(BaseFormComponent* apOther)')
 start=src.index('bool TESForm::CompareWithBase(');end=src.index('\n}',start)+2;body=src[start:end];body=rep(body,'if (FUN_00474cb0() ||','if (reinterpret_cast<CompareForm*>(this)->FUN_00474cb0() ||');body=rep(body,'if (FUN_00474cb0() !=','if (reinterpret_cast<CompareForm*>(this)->FUN_00474cb0() !=');body=rep(body,'unsigned int flagsA = FUN_0044ddc0();','unsigned int flagsA = reinterpret_cast<CompareForm*>(this)->FUN_0044ddc0();');src=src[:start]+body+src[end:]
 extra=[]
 for va,old,new in [('0x00485340','?FUN_00485340@FUN_00485340_shell@fnv_00485340@@QAEXPAVBaseFormComponent@@@Z','?CopyFromBase@TESForm@@UAEXPAVBaseFormComponent@@@Z'),('0x004853e0','?FUN_004853e0@CompareForm@@QAE_NPAVBaseFormComponent@@@Z','?CompareWithBase@TESForm@@UAE_NPAVBaseFormComponent@@@Z')]:
  match=[x for x in u['functions'] if x['address']==va]
  if len(match)!=1 or match[0]['symbol']!=old:raise ValueError('recipe mismatch '+va)
  extra.append(dict(address=va,before=old,after=new,size=match[0]['size']))
 OUT.mkdir(parents=False,exist_ok=False); outputs={'tesform.cpp':src.encode(),'tesform_TESForm.h':hdr.encode(),'tesform_calls.h':raw[paths[2]],'bgsencounterzone_TESForm.h':bgsh.encode()}
 for n,b in outputs.items():(OUT/n).write_bytes(b)
 manifest={'unit_index':998,'source':u['source'],'flags':u['flags'],'functions_count':128,'inputs':{p:sha(x) for p,x in raw.items()},'bgs_header_input_sha256':sha(bgst),'bgs_six_header_sha256':sha(bh),'outputs':{n:sha(b) for n,b in outputs.items()},'proposed_function_symbol_changes':extra,'status':'uncompiled hypothesis; require all 128 functions, normalized relocations, BGSE slot graph and include closure','risks':['CompareForm helper calls preserve old shell symbol identities via this cast but their ABI is unverified','paired unit-local TESForm declarations are not global ODR proof','folded empty virtual slots 0/1 are not inferred']}
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest['outputs']))
if __name__=='__main__':main()

