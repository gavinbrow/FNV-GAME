"""Stage two TESForm flag virtual bodies, atop the private base-slot proposal."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M.parent.parent;F=P/'fnv_decomp';A=M/'out/phase2-tesform-base-slots';O=M/'out/phase2-tesform-flag-slots'
def sha(b):return hashlib.sha256(b).hexdigest()
def rep(s,a,b):
 if s.count(a)!=1:raise ValueError('anchor mismatch '+a[:60])
 return s.replace(a,b,1)
def main():
 m=json.loads((A/'manifest.json').read_text()); files={n:(A/n).read_bytes() for n in m['outputs']}
 if any(sha(files[n])!=d for n,d in m['outputs'].items()):raise ValueError('prior payload changed')
 src=files['tesform.cpp'].decode();u=json.loads((F/'build/units.json').read_bytes())['units'][998]
 src=rep(src,'void FUN_004849d0_shell::SetFlag200(bool abVal)','void TESForm::Unk_2F(bool abVal)')
 src=rep(src,'void Fake84860::FUN_00484860(bool abQuest)','void TESForm::SetQuestItem(bool abQuest)')
 start=src.index('void TESForm::SetQuestItem(');end=src.index('\n}',start)+2;body=src[start:end];body=body.replace('_flags','m_uiFormFlags');body=rep(body,'    v18(1);','    MarkAsModified(1);');src=src[:start]+body+src[end:]
 changes=[]
 for va,old,new in [('0x004849d0','?SetFlag200@FUN_004849d0_shell@@QAEX_N@Z','?Unk_2F@TESForm@@UAEX_N@Z'),('0x00484860','?FUN_00484860@Fake84860@@QAEX_N@Z','?SetQuestItem@TESForm@@UAEX_N@Z')]:
  f=[x for x in u['functions'] if x['address']==va]
  if len(f)!=1 or f[0]['symbol']!=old:raise ValueError('recipe mismatch')
  changes.append(dict(address=va,before=old,after=new,size=f[0]['size']))
 files['tesform.cpp']=src.encode(); O.mkdir(parents=False,exist_ok=False)
 for n,b in files.items():(O/n).write_bytes(b)
 result=dict(m);result['outputs']={n:sha(b) for n,b in files.items()};result['proposed_function_symbol_changes']=m['proposed_function_symbol_changes']+changes;result['status']='uncompiled; require 128-function, normalized relocation and 78-slot comparison';result['risks']=m['risks']+['Fake84860 v18 slot is hypothesized to be TESForm MarkAsModified; compiler/relocation gates required','Unk_2F source flag identity uses same bool signature, semantic naming remains unresolved'];(O/'manifest.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['outputs']))
if __name__=='__main__':main()
