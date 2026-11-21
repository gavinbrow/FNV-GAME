"""Merge private BGSE save/copy/compare and init/load hypotheses."""
import hashlib,json,sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rtti_bgse_init_load_overlay as initload
H=Path(__file__).resolve().parent;M=H.parent;PRIOR=M/'out/phase2-bgsencounterzone-save'; OTHER=M/'out/phase2-bgsencounterzone-initload-v2'; OUT=M/'out/phase2-bgsencounterzone-six-override'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 m=json.loads((PRIOR/'manifest.json').read_text()); om=json.loads((OTHER/'manifest.json').read_text());s=(PRIOR/'bgsencounterzone.cpp').read_bytes();h=(PRIOR/'bgsencounterzone_decls.h').read_bytes()
 if sha(s)!='eeaf19485eec32ec325b04b6213dbff1acd590d6904f80a2a98cff556ca6e95f' or sha(h)!='0b3e86fd7d2d21a757988bba5eaf95e7f35f11eb673c66c9ab20da66a416580e' or m['source_overlay_sha256']!=sha(s) or m['header_overlay_sha256']!=sha(h):raise ValueError('prior inputs changed')
 # Independently bind the second branch and its common ancestor via manifest.
 if sha((OTHER/'bgsencounterzone.cpp').read_bytes())!=om['source_overlay_sha256'] or sha((OTHER/'bgsencounterzone_decls.h').read_bytes())!=om['header_overlay_sha256']:raise ValueError('init/load branch changed')
 old=m['proposed_function_symbol_changes']; others=om['proposed_function_symbol_changes']; addresses={x['address'] for x in old};extra=[x for x in others if x['address'] not in addresses]
 if {x['address'] for x in extra}!={'0x00525d00','0x00525d40'}:raise ValueError('unexpected additional symbols')
 for a in addresses & {x['address'] for x in others}:
  if next(x for x in old if x['address']==a)!=next(x for x in others if x['address']==a):raise ValueError('common remap differs')
 ss,hh=initload.transform(s.decode(),h.decode());sb=ss.encode();hb=hh.encode();OUT.mkdir(parents=False,exist_ok=False);(OUT/'bgsencounterzone.cpp').write_bytes(sb);(OUT/'bgsencounterzone_decls.h').write_bytes(hb)
 result=dict(m);result.update(scope='private combined six-slot overrides and prior destructor/load/revert; no installed source', proposed_function_symbol_changes=old+extra,source_overlay_sha256=sha(sb),header_overlay_sha256=sha(hb),status='uncompiled; all 24 functions, full 78 slots, global ODR and call compatibility remain to be verified',known_risks=m['known_risks']+om['known_risks'])
 result['merge_input_sha256']={'save_source':sha(s),'save_header':sha(h),'initload_source':om['source_overlay_sha256'],'initload_header':om['header_overlay_sha256']}
 (OUT/'manifest.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'source':sha(sb),'header':sha(hb),'remaps':len(old+extra)}))
if __name__=='__main__':main()

