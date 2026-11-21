"""Private TESForm simple flag getter overrides following no-op hypothesis."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M.parent.parent;A=M/'out/phase2-tesform-noop-slots';O=M/'out/phase2-tesform-getter-slots';U=P/'fnv_decomp/build/units.json'
def sha(x):return hashlib.sha256(x).hexdigest()
def rep(s,a,b):
 if s.count(a)!=1:raise ValueError('anchor mismatch '+a[:50])
 return s.replace(a,b,1)
def main():
 m=json.loads((A/'manifest.json').read_bytes());files={n:(A/n).read_bytes() for n in m['outputs']}
 if any(sha(files[n])!=v for n,v in m['outputs'].items()):raise ValueError('input mismatch')
 s=files['tesform.cpp'].decode();s=rep(s,'struct FUN_004011f0_shell : public TESForm\n{\n    bool FUN_004011f0();\n};\n','');s=rep(s,'bool FUN_004011f0_shell::FUN_004011f0()','}  // namespace fnv_004011f0\nbool TESForm::Unk_2B()');s=rep(s,'}\n}  // namespace fnv_004011f0\n\nstruct S3c60','}\n\nstruct S3c60')
 for old,new in [('bool FUN_00401210_shell::HasFlag() const','bool TESForm::Unk_2C()'),('bool FUN_00401250_shell::IsFlag200Set()','bool TESForm::Unk_2E()'),('bool FUN_00549580_shell::FUN_00549580() const','bool TESForm::Unk_26()')]:s=rep(s,old,new)
 u=json.loads(U.read_bytes())['units'][998];extra=[]
 for va,old,new in [('0x004011f0','?FUN_004011f0@FUN_004011f0_shell@fnv_004011f0@@QAE_NXZ','?Unk_2B@TESForm@@UAE_NXZ'),('0x00401210','?HasFlag@FUN_00401210_shell@@QBE_NXZ','?Unk_2C@TESForm@@UAE_NXZ'),('0x00401250','?IsFlag200Set@FUN_00401250_shell@@QAE_NXZ','?Unk_2E@TESForm@@UAE_NXZ'),('0x00549580','?FUN_00549580@FUN_00549580_shell@@QBE_NXZ','?Unk_26@TESForm@@UAE_NXZ')]:
  f=[x for x in u['functions'] if x['address']==va]
  if len(f)!=1 or f[0]['symbol']!=old:raise ValueError('recipe mismatch')
  extra.append(dict(address=va,before=old,after=new,size=f[0]['size']))
 files['tesform.cpp']=s.encode();O.mkdir(parents=False,exist_ok=False)
 for n,b in files.items():(O/n).write_bytes(b)
 m.update(scope='private flag getters atop previous TESForm hypotheses',outputs={n:sha(b) for n,b in files.items()},proposed_function_symbol_changes=m['proposed_function_symbol_changes']+extra,status='uncompiled; 128-function/relocation/reference and BGSE slot checks required')
 m['risks']+=['two source getter shells use const while current virtual declarations are non-const; x86 ABI and source contract remain hypotheses','reference slot address and source body do not establish historical names']
 (O/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps({'remaps':len(m['proposed_function_symbol_changes']),'source_sha256':sha(files['tesform.cpp'])}))
if __name__=='__main__':main()
