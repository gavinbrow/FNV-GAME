"""Stage a private common-source /Od and /O2 scratch-array hypothesis."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M.parent.parent;F=P/'fnv_decomp';O=M/'out/phase2-refptr260-native-header-fixture';U=F/'build/units.json';S258=F/'src/fallout/ai/actor_o2_variant.cpp';S2662=F/'src/fallout/ai/movement/actormover.cpp'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('no overwrite')
 raw=U.read_bytes();units=json.loads(raw)['units'];f=next(x for x in units[260]['functions'] if x['address']=='0x00c7d900');g=next(x for x in units[386]['functions'] if x['address']=='0x0045cec0')
 if f['size']!=822 or g['size']!=29 or units[260]['flags']!=['/MT','/O2','/GS','/EHsc','/Gy'] or '/Od' not in units[386]['flags']:raise ValueError('source/flags mismatch')
 headers=['NiRefObject.h','NiMemObject.h','layout_support.h']
 paths={n:F/'include'/n for n in headers}
 wrapper=r'''#include "NiRefObject.h"
void ForceNativePointer(NiPointer<NiRefObject>* p) { p->~NiPointer<NiRefObject>(); }
void ForceNativeRelease(NiRefObject* p) { p->DecRefCount(); }
'''
 O.mkdir();files={n:q.read_bytes() for n,q in paths.items()};files.update({'owner_od.cpp':wrapper.encode(),'scratch_o2.cpp':wrapper.encode()})
 for n,b in files.items():(O/n).write_bytes(b)
 meta={'scope':'isolated existing NiRefObject/NiPointer header compiler hypothesis, not source patch or address alias','recipe_sha256':sha(raw),'source_inputs':{'unit260':sha(S258.read_bytes()),'unit386':sha(S2662.read_bytes())},'outputs':{n:sha(b) for n,b in files.items()},'targets':{'od_owner':{'unit':386,'function':g},'o2_outer':{'unit':260,'source_parent':f}},'compile_variants':{'od':{'compiler':units[386]['compiler'],'flags':units[386]['flags']},'o2':{'compiler':units[260]['compiler'],'flags':units[260]['flags']}},'status':'uncompiled exploration; compiler output may fail exact matching','gates':['discover emitted decorated symbols and full extents','strict 29-byte owner and optimized release bytes and normal relocation targets','constructor layout, this/callee conventions and both exception graphs/xdata','prove source identity and COMDAT ownership across production units before any binding','all affected mapped functions and final image/runtime checks'],'limitations':['provisional type names and pointee identity; no native class identity claim','same layout and behavior do not establish original pointee class identity','caller ABI, store-order observability and global ODR remain unresolved']}
 (O/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps({'files':len(files),'od_flags':meta['compile_variants']['od']['flags'],'o2_flags':meta['compile_variants']['o2']['flags']}))
if __name__=='__main__':main()
