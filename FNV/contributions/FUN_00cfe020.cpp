#include <intrin.h>
struct S_cfe020_Entry;
struct S_cfe020_Slot { S_cfe020_Entry* entry; int unk04; };
struct S_cfe020_Owner {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    S_cfe020_Slot* slots;
};
struct S_cfe020_Entry {
    int unk00;
    union {
        int unk04;
        struct { unsigned short idxA; unsigned short idxB; };
    };
    int unk08;
    int unk0c;
    S_cfe020_Owner* ownerA;
    S_cfe020_Owner* ownerB;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    int unk60;
    int unk64;
    int unk68;
    int unk6c;
    int unk70;
    int unk74;
    int unk78;
    volatile int unk7c;
    __forceinline S_cfe020_Entry& operator=(const S_cfe020_Entry& o)
    {
        unk00 = o.unk00;
        unk04 = o.unk04;
        unk08 = o.unk08;
        unk0c = o.unk0c;
        ownerA = o.ownerA;
        ownerB = o.ownerB;
        unk18 = o.unk18;
        unk1c = o.unk1c;
        unk20 = o.unk20;
        unk24 = o.unk24;
        unk28 = o.unk28;
        unk2c = o.unk2c;
        unk30 = o.unk30;
        unk34 = o.unk34;
        unk38 = o.unk38;
        unk3c = o.unk3c;
        unk40 = o.unk40;
        unk44 = o.unk44;
        unk48 = o.unk48;
        unk4c = o.unk4c;
        unk50 = o.unk50;
        unk54 = o.unk54;
        unk58 = o.unk58;
        unk5c = o.unk5c;
        unk60 = o.unk60;
        unk64 = o.unk64;
        unk68 = o.unk68;
        unk6c = o.unk6c;
        unk70 = o.unk70;
        unk74 = o.unk74;
        unk78 = o.unk78;
        unk7c = o.unk7c;
        return *this;
    }
};
struct S_cfe020_Heap { virtual void v0(); virtual void v1(); virtual void blockFree(void* p, int size); };

void __cdecl FUN_00c909d0(S_cfe020_Heap* heap, void* arr, int elemSize, void* mem, int n);

struct S_cfe020_Blocks {
    char** data;
    int size;
    int cap;
    int local;
    __forceinline char* back() { return data[size - 1]; }
    __forceinline void popBack() { size--; }
    __forceinline void optimize()
    {
        if ((cap & 0x80000000) == 0) {
            unsigned int n = size + 3;
            n |= n >> 16;
            n |= n >> 8;
            n |= n >> 4;
            n |= n >> 2;
            n |= n >> 1;
            int newCap = n + 1;
            if (newCap < 1) {
                FUN_00c909d0((S_cfe020_Heap*)&FUN_00c85750().heap(), &data, 4, &local, 1);
            } else if (newCap < (cap & 0x3fffffff)) {
                FUN_00c909d0((S_cfe020_Heap*)&FUN_00c85750().heap(), &data, 4, 0, newCap);
            }
        }
    }
};

struct S_cfe020_Pool {
    int used;
    S_cfe020_Blocks blocks;
};

void FUN_00cfe020(S_cfe020_Pool* pool, S_cfe020_Entry* dest)
{
    S_cfe020_Entry* src = (S_cfe020_Entry*)(pool->blocks.back() + pool->used - 0x80);
    if (dest != src) {
        *dest = *src;
        _ReadWriteBarrier();
        unsigned short a = dest->idxA;
        unsigned short b = dest->idxB;
        dest->ownerA->slots[a].entry = dest;
        dest->ownerB->slots[b].entry = dest;
    }
    pool->used -= 0x80;
    if (pool->used == 0) {
        char* block = pool->blocks.back();
        pool->blocks.popBack();
        ((S_cfe020_Heap*)&FUN_00c85750().heap())->blockFree(block, 0x200);
        pool->used = 0x200;
    }
    pool->blocks.optimize();
}
