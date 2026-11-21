"""Stage TESForm::SetAltered atop the four-slot private hypothesis."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M.parent.parent;F=P/'fnv_decomp';A=M/'out/phase2-tesform-flag-slots';O=M/'out/phase2-tesform-altered-slot'
def sha(b):return hashlib.sha256(b).hexdigest()
def rep(s,a,b):
 if s.count(a)!=1:raise ValueError('anchor mismatch '+a[:60])
 return s.replace(a,b,1)
def main():
 m=json.loads((A/'manifest.json').read_text());files={n:(A/n).read_bytes() for n in m['outputs']}
 if any(sha(files[n])!=d for n,d in m['outputs'].items()):raise ValueError('prior payload changed')
 src=files['tesform.cpp'].decode();u=json.loads((F/'build/units.json').read_bytes())['units'][998]
 src=rep(src,'struct FUN_00484730_shell : public TESForm\n{\n    void FUN_00484730(bool);\n};\n','')
 src=rep(src,'void FUN_00484730_shell::FUN_00484730(bool abAltered)','}  // namespace fnv_00484730\nvoid TESForm::SetAltered(bool abAltered)')
 start=src.index('void TESForm::SetAltered(');end=src.index('\n}',start)+2;body=src[start:end]
 for n in ('Pathing','Arr','FormArray','NiTLargeArray_TESTopicInfo'):body=body.replace('('+n+'*)','(fnv_00484730::'+n+'*)')
 src=src[:start]+body+src[end:];src=rep(src,'}\n}  // namespace fnv_00484730\n\nstruct BGSSaveFormBuffer;','}\n\nstruct BGSSaveFormBuffer;')
 va='0x00484730';old='?FUN_00484730@FUN_00484730_shell@fnv_00484730@@QAEX_N@Z';new='?SetAltered@TESForm@@UAEX_N@Z';f=[x for x in u['functions'] if x['address']==va]
 if len(f)!=1 or f[0]['symbol']!=old:raise ValueError('recipe mismatch')
 files['tesform.cpp']=src.encode();O.mkdir(parents=False,exist_ok=False)
 for n,b in files.items():(O/n).write_bytes(b)
 result=dict(m);result['outputs']={n:sha(b) for n,b in files.items()};result['proposed_function_symbol_changes']=m['proposed_function_symbol_changes']+[dict(address=va,before=old,after=new,size=f[0]['size'])];result['status']='uncompiled; require 128-function, normalized relocation and 78-slot comparison';result['risks']=m['risks']+['SetAltered helper type qualifications preserve source symbols but require object and all-function comparison'];(O/'manifest.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['outputs']))
if __name__=='__main__':main()
