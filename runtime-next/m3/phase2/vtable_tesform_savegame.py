"""Private TESForm slot22 source-body hypothesis."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M.parent.parent;A=M/'out/phase2-tesform-getter-slots';O=M/'out/phase2-tesform-savegame-slot';U=P/'fnv_decomp/build/units.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def rep(s,a,b):
 if s.count(a)!=1:raise ValueError('anchor mismatch')
 return s.replace(a,b,1)
def main():
 m=json.loads((A/'manifest.json').read_bytes());files={n:(A/n).read_bytes() for n in m['outputs']}
 if any(sha(files[n])!=v for n,v in m['outputs'].items()):raise ValueError('input mismatch')
 s=files['tesform.cpp'].decode();s=rep(s,'void PC7d::FUN_00484c20(unsigned int aiFlags)','void TESForm::SaveGame(unsigned int aiFlags)');s=rep(s,'        FUN_00484ce0((unsigned int)((char*)this + 8), 4);','        reinterpret_cast<PC7d*>(this)->FUN_00484ce0((unsigned int)((char*)this + 8), 4);')
 u=json.loads(U.read_bytes())['units'][998];f=[x for x in u['functions'] if x['address']=='0x00484c20'];old='?FUN_00484c20@PC7d@@QAEXI@Z';new='?SaveGame@TESForm@@UAEXI@Z'
 if len(f)!=1 or f[0]['symbol']!=old or f[0]['size']!=38:raise ValueError('recipe mismatch')
 files['tesform.cpp']=s.encode();O.mkdir(parents=False,exist_ok=False)
 for n,b in files.items():(O/n).write_bytes(b)
 m.update(scope='private slot22 SaveGame source-body hypothesis on previous TESForm work',outputs={n:sha(b) for n,b in files.items()},proposed_function_symbol_changes=m['proposed_function_symbol_changes']+[dict(address='0x00484c20',before=old,after=new,size=38)],status='uncompiled; full unit and paired BGSE slot gates required');m['risks']+=['PC7d shell is not declared derived from TESForm; identical calling convention and this layout require compiler/relocation proof','slot name is current base API, not independent proof of historical semantics']
 (O/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps({'remaps':len(m['proposed_function_symbol_changes']),'source_sha256':sha(files['tesform.cpp'])}))
if __name__=='__main__':main()
