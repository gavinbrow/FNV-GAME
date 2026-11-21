"""Stage TESForm no-arg flag pair atop the private flag/setter candidate."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M.parent.parent;F=P/'fnv_decomp';A=M/'out/phase2-tesform-flagpair-setters';O=M/'out/phase2-tesform-two-flagpairs-setters'
def sha(b):return hashlib.sha256(b).hexdigest()
def rep(s,a,b):
 if s.count(a)!=1:raise ValueError('anchor mismatch '+a[:70])
 return s.replace(a,b,1)
def main():
 m=json.loads((A/'manifest.json').read_bytes());files={n:(A/n).read_bytes() for n in m['outputs']}
 if any(sha(files[n])!=v for n,v in m['outputs'].items()) or sha((F/'build/units.json').read_bytes())!=m['inputs']['build/units.json']:raise ValueError('input mismatch')
 u=json.loads((F/'build/units.json').read_bytes())['units'][998];f=[x for x in u['functions'] if x['address']=='0x004011d0'];old='?FUN_004011d0@FUN_004011d0_shell@@QAE_NXZ'
 if len(f)!=1 or f[0]['symbol']!=old or f[0]['size']!=26:raise ValueError('source getter differs')
 src=files['tesform.cpp'].decode();src=rep(src,'bool FUN_004011d0_shell::FUN_004011d0()\n{\n    return (m_uiFormFlags & 0x20000) ? true : false;\n}','bool TESForm::Unk_29()\n{\n    return (m_uiFormFlags & 0x20000) ? true : false;\n}\nbool TESForm::Unk_2A()\n{\n    return (m_uiFormFlags & 0x20000) ? true : false;\n}');files['tesform.cpp']=src.encode()
 for name in ('tesform_TESForm.h','bgsencounterzone_TESForm.h'):
  h=files[name].decode()
  for slot in ('29','2A'):h=rep(h,'virtual bool Unk_'+slot+'(bool set);','virtual bool Unk_'+slot+'(void);')
  files[name]=h.encode()
 O.mkdir(parents=False,exist_ok=False)
 for n,b in files.items():(O/n).write_bytes(b)
 m.update(scope='private no-argument flag getter pairs and native setter declarations',outputs={n:sha(b) for n,b in files.items()},getter2={'source_symbol':old,'address':'0x004011d0','size':26,'canonical':'?Unk_29@TESForm@@UAE_NXZ','fold_alias':'?Unk_2A@TESForm@@UAE_NXZ','slots':[41,42],'evidence':'source-derived TESForm shell has no explicit args; original x86 body reads flags +8 and ends ret without immediate; both observed BGSE slots target it'},status='uncompiled; paired 128+24 functions/EH and all slot/fold/ABI gates required')
 m['limitations']+=['other TESForm declarations retain incompatible guessed bool-argument contracts; broad source ABI and ODR remain unresolved','the two folded getters require separate complete-body/relocation proof']
 (O/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps(m['outputs']))
if __name__=='__main__':main()
