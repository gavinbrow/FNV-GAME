"""Stage the static-only TESContainer shell consolidation for units 1111 and 1112."""
import hashlib,json,re
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';T=M/'out/phase2-tesform-load-typed-v4-transaction';O=M/'out/phase2-tescontainer-script-shell'
D='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160';EXPECTED={'src/fallout_shared/tesscript_decls.h':'b8b1065eee55cfe325a35d40fc916e114f295c123c5e344dd8616748a1b308a7','include/TESContainer.h':'747785741a94b4a10eaa7c38be866e707ea5d2c27169c12ca30dabb65d9e4f85','src/fallout_shared/tesscript.cpp':'a08a515e4c695be59e1a241e34e943e9691bb140600271c55b3c0a84463a2317','src/fallout_shared/tesscript_ctx_variant.cpp':'a242ec896e23f4d46cd23c1a94cbdf5d0f5f335a09c522476f1ccfbd5c555ab9'}
OLD='class TESContainer\n{\n  public:\n    static bool IsValidContainerType(unsigned char type);\n};'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 units=(F/'build/units.json').read_bytes();applied=json.loads((T/'manifest.json').read_text())
 if sha(units)!=D or not (T/'applied.json').exists() or applied['files'][-1]['new_sha256']!=D:raise ValueError('exact applied recipe transaction missing')
 doc=json.loads(units)['units'];
 for i,source,count in [(1111,'src/fallout_shared/tesscript.cpp',82),(1112,'src/fallout_shared/tesscript_ctx_variant.cpp',1)]:
  if doc[i]['source']!=source or len(doc[i]['functions'])!=count:raise ValueError('recipe unit changed')
 data={rel:(F/rel).read_bytes() for rel in EXPECTED}
 for rel,d in EXPECTED.items():
  if sha(data[rel])!=d:raise ValueError('input changed '+rel)
 text=data['src/fallout_shared/tesscript_decls.h'].decode('utf-8-sig').replace('\r\n','\n')
 if text.count(OLD)!=1 or len(re.findall(r'\bTESContainer\b',text))!=1:raise ValueError('unexpected TESContainer uses')
 for rel in ('src/fallout_shared/tesscript.cpp','src/fallout_shared/tesscript_ctx_variant.cpp'):
  if re.search(rb'\bTESContainer\b',data[rel]):raise ValueError('source has other TESContainer uses '+rel)
 if b'static bool IsValidContainerType(unsigned char type);' not in data['include/TESContainer.h']:raise ValueError('canonical static declaration changed')
 new=text.replace(OLD,'#include "TESContainer.h"',1).encode();O.mkdir(exist_ok=False);(O/'tesscript_decls.h').write_bytes(new)
 out={'base_units_sha256':D,'inputs':EXPECTED,'candidate_header_sha256':sha(new),'units':[{'unit':1111,'source':'src/fallout_shared/tesscript.cpp','functions':82},{'unit':1112,'source':'src/fallout_shared/tesscript_ctx_variant.cpp','functions':1}],'scope':'replace an otherwise unused static-only global TESContainer shell in a shared header; no class ODR or complete interface claim','status':'uncompiled; require both include closures, 83 mapped functions, EH and literal/relocation checks, production labels, full build and gameplay'}
 (O/'manifest.json').write_text(json.dumps(out,indent=2));print(json.dumps({'header_sha256':sha(new),'units':2,'mapped_functions':83}))
if __name__=='__main__':main()
