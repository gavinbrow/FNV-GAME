"""Stage a private common-source /Od and /O2 scratch-array hypothesis."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M.parent.parent;F=P/'fnv_decomp';O=M/'out/phase2-refptr260-common-fixture';U=F/'build/units.json';S258=F/'src/fallout/ai/actor_o2_variant.cpp';S2662=F/'src/fallout/ai/movement/actormover.cpp'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('no overwrite')
 raw=U.read_bytes();units=json.loads(raw)['units'];f=next(x for x in units[260]['functions'] if x['address']=='0x00c7d900');g=next(x for x in units[386]['functions'] if x['address']=='0x0045cec0')
 if f['size']!=822 or g['size']!=29 or units[260]['flags']!=['/MT','/O2','/GS','/EHsc','/Gy'] or '/Od' not in units[386]['flags']:raise ValueError('source/flags mismatch')
 header=r'''#pragma once
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefReleaseView {
    virtual void vf0(); virtual void vf1(); long references;
    __forceinline void Release() { if (InterlockedDecrement(&references)==0) vf1(); }
};
struct RefPointerView {
    RefReleaseView* pointer;
    __forceinline ~RefPointerView() { if (pointer) pointer->Release(); }
};
typedef char RefReleaseSize[(sizeof(RefReleaseView)==8)?1:-1];
typedef char RefPointerSize[(sizeof(RefPointerView)==4)?1:-1];
'''
 od='#include "refptr_common.h"\nvoid ForceRefPointer(RefPointerView* p) { p->~RefPointerView(); }\n'
 o2='#include "refptr_common.h"\nvoid ForceRefPointer(RefPointerView* p) { p->~RefPointerView(); }\n'
 O.mkdir();files={'refptr_common.h':header.encode(),'owner_od.cpp':od.encode(),'scratch_o2.cpp':o2.encode()}
 for n,b in files.items():(O/n).write_bytes(b)
 meta={'scope':'isolated refpointer common-source compiler hypothesis, not source patch or address alias','recipe_sha256':sha(raw),'source_inputs':{'unit260':sha(S258.read_bytes()),'unit386':sha(S2662.read_bytes())},'outputs':{n:sha(b) for n,b in files.items()},'targets':{'od_owner':{'unit':386,'function':g},'o2_outer':{'unit':260,'source_parent':f}},'compile_variants':{'od':{'compiler':units[386]['compiler'],'flags':units[386]['flags']},'o2':{'compiler':units[260]['compiler'],'flags':units[260]['flags']}},'status':'uncompiled exploration; compiler output may fail exact matching','gates':['discover emitted decorated symbols and full extents','strict 29-byte owner and optimized release bytes and normal relocation targets','constructor layout, this/callee conventions and both exception graphs/xdata','prove source identity and COMDAT ownership across production units before any binding','all affected mapped functions and final image/runtime checks'],'limitations':['provisional type names and pointee semantics; no native class identity claim','single shared header is conceptual reconstruction, not proof original source used these definitions','caller ABI, store-order observability and global ODR remain unresolved']}
 (O/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps({'files':len(files),'od_flags':meta['compile_variants']['od']['flags'],'o2_flags':meta['compile_variants']['o2']['flags']}))
if __name__=='__main__':main()
