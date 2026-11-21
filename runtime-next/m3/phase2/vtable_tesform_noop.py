"""Stage source-contract no-op TESForm Init/Free slot hypotheses privately."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M.parent.parent;F=P/'fnv_decomp';A=M/'out/phase2-tesform-altered-slot';O=M/'out/phase2-tesform-noop-slots'
def sha(b):return hashlib.sha256(b).hexdigest()
def rep(s,a,b):
 if s.count(a)!=1:raise ValueError('anchor mismatch '+a[:60])
 return s.replace(a,b,1)
def main():
 m=json.loads((A/'manifest.json').read_text());files={n:(A/n).read_bytes() for n in m['outputs']}
 if any(sha(files[n])!=d for n,d in m['outputs'].items()):raise ValueError('prior payload changed')
 u=json.loads((F/'build/units.json').read_bytes())['units'][998];f=[x for x in u['functions'] if x['address']=='0x00483710']
 if len(f)!=1 or f[0]['symbol']!='?ClearData@TESForm@@UAEXXZ':raise ValueError('source no-op recipe mismatch')
 src=files['tesform.cpp'].decode();src=rep(src,'void TESForm::ClearData()\n{}','void TESForm::ClearData()\n{}\n\n// Private hypothesis: same no-op ABI as the source ClearData body.\nvoid TESForm::Init()\n{}\nvoid TESForm::Free()\n{}');files['tesform.cpp']=src.encode()
 for n in ('tesform_TESForm.h','bgsencounterzone_TESForm.h'):
  h=files[n].decode();h=rep(h,'    virtual ~TESForm();\n','    virtual ~TESForm();\n    virtual void Init();\n    virtual void Free();\n');files[n]=h.encode()
 O.mkdir(parents=False,exist_ok=False)
 for n,b in files.items():(O/n).write_bytes(b)
 result=dict(m);result['outputs']={n:sha(b) for n,b in files.items()};result['proposed_noop_fold']={'source_address':'0x00483710','source_body_symbol':'?ClearData@TESForm@@UAEXXZ','new_symbols':['?Init@TESForm@@UAEXXZ','?Free@TESForm@@UAEXXZ'],'slot_indices':[0,1],'basis':'void no-argument BaseFormComponent virtual contract; empty source ClearData body; independent TESForm and BGSE observed slot targets','status':'uncompiled hypothesis, no alias or placement installed'};result['status']='uncompiled; 128 function/reference, no-op bytes/calling convention, paired 78-slot class and whole-image ICF proof required';result['risks']=m['risks']+['empty body equivalence does not establish historical method names','identical code folding and unique legal placement must be proven before assigning a common address','other derived classes and global ODR remain unchecked'];(O/'manifest.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['outputs']))
if __name__=='__main__':main()
