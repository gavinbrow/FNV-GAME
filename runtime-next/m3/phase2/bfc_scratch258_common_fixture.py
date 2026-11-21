"""Stage a private common-source /Od and /O2 scratch-array hypothesis."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M.parent.parent;F=P/'fnv_decomp';O=M/'out/phase2-scratch258-common-fixture';U=F/'build/units.json';S258=F/'src/fallout/ai/actor_o2_nood_variant.cpp';S2662=F/'src/staging/blk_00620000_od.cpp'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('no overwrite')
 raw=U.read_bytes();units=json.loads(raw)['units'];f=next(x for x in units[258]['functions'] if x['address']=='0x00c7e9a0');g=next(x for x in units[2662]['functions'] if x['address']=='0x00629b40')
 if f['size']!=1718 or g['size']!=83 or units[258]['flags']!=['/MT','/O2','/GS','/EHsc','/Gy'] or '/Od' not in units[2662]['flags']:raise ValueError('source/flags mismatch')
 header=r'''#pragma once
// Provisional common source, derived from the observed three-word array and
// its source-backed cleanup chain. Semantic type names are not asserted.
struct ScratchAllocator {
    virtual void slot0(); virtual void slot4(); virtual void slot8(); virtual void slotC();
    virtual void* Free(void* data, unsigned int bytes);
};
struct ScratchRouter { char* top; int slot4,slot8,slotC; ScratchAllocator* allocator; };
extern "C" ScratchRouter* __cdecl ScratchRouterSource();
struct ScratchStorageRaw {
    void* data; unsigned int size,capacity;
    __forceinline ScratchStorageRaw():data(0),size(0),capacity(0x80000000u){}
    __forceinline ~ScratchStorageRaw() {}
    __forceinline void DestroyElements() { size=0; }
    __forceinline void ClearStorage() {
        ScratchAllocator* allocator=ScratchRouterSource()->allocator;
        DestroyElements();
        unsigned int flags=capacity;
        if (!(flags & 0x80000000u)) allocator->Free(data,(flags & 0x3fffffffu)*4);
        data=0; capacity=0x80000000u;
    }
};
struct ScratchBase629 : ScratchStorageRaw {
    __forceinline ~ScratchBase629() { ClearStorage(); }
};
struct ScratchOuter629 : ScratchBase629 {
    char* saved;
    __forceinline ScratchOuter629() {
        ScratchRouter* router=ScratchRouterSource(); char* p=router->top;
        router->top=p+0x100; data=p; capacity=0x80000040u; saved=p;
    }
    __forceinline ~ScratchOuter629() {
        char* original=saved;
        if (original==data) size=0;
        ScratchRouterSource()->top=original;
    }
};
typedef char ScratchStorageSize[(sizeof(ScratchStorageRaw)==12)?1:-1];
typedef char ScratchOuterSize[(sizeof(ScratchOuter629)==16)?1:-1];
'''
 od='''#include "scratch_common.h"\nvoid ForceBase629(ScratchBase629* p) { p->~ScratchBase629(); }\n'''
 o2='''#include "scratch_common.h"\nvoid ForceScratch629(ScratchOuter629* p) { p->~ScratchOuter629(); }\n'''
 O.mkdir();files={'scratch_common.h':header.encode(),'owner_od.cpp':od.encode(),'scratch_o2.cpp':o2.encode()}
 for n,b in files.items():(O/n).write_bytes(b)
 meta={'scope':'isolated common-source compiler hypothesis, not source patch or address alias','recipe_sha256':sha(raw),'source_inputs':{'unit258':sha(S258.read_bytes()),'unit2662':sha(S2662.read_bytes())},'outputs':{n:sha(b) for n,b in files.items()},'targets':{'od_owner':{'unit':2662,'function':g},'o2_outer':{'unit':258,'source_parent':f,'hypothesized_address':'0x00c7d480'}},'compile_variants':{'od':{'compiler':units[2662]['compiler'],'flags':units[2662]['flags']},'o2':{'compiler':units[258]['compiler'],'flags':units[258]['flags']}},'status':'uncompiled exploration; compiler output may fail exact matching','gates':['discover emitted decorated symbols and full extents','strict 83-byte owner and 157-byte outer bytes and normal relocation targets','constructor layout, this/callee conventions and both exception graphs/xdata','prove source identity and COMDAT ownership across production units before any binding','all affected mapped functions and final image/runtime checks'],'limitations':['provisional type names and allocator semantics; no native class identity claim','single shared header is conceptual reconstruction, not proof original source used these definitions','caller ABI, store-order observability and global ODR remain unresolved']}
 (O/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps({'files':len(files),'od_flags':meta['compile_variants']['od']['flags'],'o2_flags':meta['compile_variants']['o2']['flags']}))
if __name__=='__main__':main()
