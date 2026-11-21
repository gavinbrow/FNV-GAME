"""Isolated unit775 global TESContainer shell-to-canonical header hypothesis."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';O=M/'out/phase2-tescontainer-inventory775';sys.path.insert(0,str(H));import tescontainer_experiment as t
SRC=F/'src/fallout_shared/inventorychanges_ctxr_variant.cpp';HDR=F/'include/TESContainer.h';UNIT=F/'build/units.json'
SHA={'source':'4d778925d80a99d10ab4c9900ade804380fe2868029d05186c45f268d0f84e24','header':'fa04e82ae34b60fbb75e97fc100bd791b7b490a213496b9478c1b07daeeef0f0','units':'a7470e7f0f8c59ea4b201a1e1f72bb552d3bbd00596db2fdc4911b94b6c18a56'}
OLD='struct TESContainer\n{\n    bool HasObjectOfType(TESObject*);\n    int GetObjectCount(TESObject*);\n};'
def sha(b):return hashlib.sha256(b).hexdigest()
def transform(s):
 if s.count(OLD)!=1:raise ValueError('expected exact class shell')
 return s.replace(OLD,'#include "TESContainer.h"',1)
def main():
 data={k:p.read_bytes() for k,p in [('source',SRC),('header',HDR),('units',UNIT)]}
 if any(sha(v)!=SHA[k] for k,v in data.items()):raise ValueError('input mismatch')
 u=json.loads(data['units'])['units'][775]
 if len(u['functions'])!=1 or u['source']!='src/fallout_shared/inventorychanges_ctxr_variant.cpp' or u['functions'][0]['address']!='0x004cb5f0':raise ValueError('unit changed')
 h=data['header'].decode();
 for sig in ('bool HasObjectOfType(TESObject* object);','int GetObjectCount(TESObject* object);'):
  if h.count(sig)!=1:raise ValueError('canonical method absent')
 source=transform(data['source'].decode('utf-8-sig').replace('\r\n','\n')).encode();closure=t.closure(SRC);O.mkdir(exist_ok=False);(O/'inventorychanges_ctxr_variant.cpp').write_bytes(source)
 meta={'unit_index':775,'source':u['source'],'source_sha256':SHA['source'],'units_sha256':SHA['units'],'canonical_header_sha256':SHA['header'],'overlay_sha256':sha(source),'original_include_closure':closure,'source_function_count':1,'risk':'shell omitted vptr and fields; replacing it could change unrelated body code, type declarations, packing and ODR. One mapped function does not cover all generated object sections.','status':'private uncompiled hypothesis; require original/overlay full object and function checks before any source proposal'}
 (O/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'overlay_sha256':sha(source),'closure_count':len(closure)}))
if __name__=='__main__':main()
