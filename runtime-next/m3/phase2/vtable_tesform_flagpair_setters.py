"""Stage private paired TESForm flag getter and three native setter declarations."""
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';O=M/'out/phase2-tesform-flagpair-setters'
PIN={'src/fallout_shared/tesform.cpp':'a529256c55d2f2bc9b9ad91a370579ccf4551831b4697dbba7878be9a8bdf1ec','src/fallout_shared/tesform_TESForm.h':'5bd002ee78fa446a1bfef82ce690f5128136e262a19742c200ef86c4327d0ac5','src/bgsencounterzone_TESForm.h':'b5573a98e7dd4fa2ff3767b58211e2d93854b2baaa37386bcc1d8f5679fe268d','build/units.json':'d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160'}
def sha(b):return hashlib.sha256(b).hexdigest()
def rep(s,a,b):
 if s.count(a)!=1:raise ValueError('anchor mismatch '+a[:60])
 return s.replace(a,b,1)
def main():
 raw={p:(F/p).read_bytes() for p in PIN}
 if any(sha(raw[p])!=h for p,h in PIN.items()):raise ValueError('input changed')
 unit=json.loads(raw['build/units.json'])['units'][998];f=[x for x in unit['functions'] if x['address']=='0x004011b0'];old='?IsFlagSet@FUN_004011b0_shell@@QBE_NXZ'
 if len(f)!=1 or f[0]['symbol']!=old or f[0]['size']!=26:raise ValueError('getter source changed')
 s=raw['src/fallout_shared/tesform.cpp'].decode().replace('\r\n','\n');a=raw['src/fallout_shared/tesform_TESForm.h'].decode().replace('\r\n','\n');b=raw['src/bgsencounterzone_TESForm.h'].decode().replace('\r\n','\n')
 oldbody='bool FUN_004011b0_shell::IsFlagSet() const\n{\n    return (m_uiFormFlags & 0x10000) ? true : false;\n}'
 newbody='bool TESForm::Unk_27() const\n{\n    return (m_uiFormFlags & 0x10000) ? true : false;\n}\nbool TESForm::Unk_28() const\n{\n    return (m_uiFormFlags & 0x10000) ? true : false;\n}'
 s=rep(s,oldbody,newbody)
 for n in ('27','28'):
  a=rep(a,'virtual bool Unk_'+n+'(void);','virtual bool Unk_'+n+'(void) const;');b=rep(b,'virtual bool Unk_'+n+'(void);','virtual bool Unk_'+n+'(void) const;')
 for before,after in [('Unk_34','SetFormFlag40'),('Unk_35','SetHavokDeath'),('Unk_36','SetNeedToChangeProcess')]:
  d='virtual void '+after+'(bool set);'
  if a.count(d)!=1:raise ValueError('native setter declaration absent')
  b=rep(b,'virtual void '+before+'(bool set);',d)
 files={'tesform.cpp':s.encode(),'tesform_TESForm.h':a.encode(),'bgsencounterzone_TESForm.h':b.encode()};O.mkdir(parents=False,exist_ok=False)
 for n,v in files.items():(O/n).write_bytes(v)
 m={'scope':'private two flag getter hypotheses and three native setter name alignments','inputs':PIN,'outputs':{n:sha(v) for n,v in files.items()},'getter':{'source_symbol':old,'address':'0x004011b0','size':26,'canonical':'?Unk_27@TESForm@@UBE_NXZ','fold_alias':'?Unk_28@TESForm@@UBE_NXZ','slots':[39,40]},'setters':[{'slot':52,'method':'SetFormFlag40','address':'0x004848b0'},{'slot':53,'method':'SetHavokDeath','address':'0x00484900'},{'slot':54,'method':'SetNeedToChangeProcess','address':'0x00484950'}],'status':'uncompiled hypothesis; exact two bodies, folded ownership, 128+24 functions/EH and 78-slot graph all required','limitations':['source shell getter is const, both local base views changed accordingly','historical names and other TESForm declarations remain unresolved','fold alias is only a proposal until independently verified']}
 (O/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps(m['outputs']))
if __name__=='__main__':main()
