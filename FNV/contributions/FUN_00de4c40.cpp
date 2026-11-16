#include <xmmintrin.h>
struct VectorArray { __m128* data; int size; unsigned int capacityAndFlags; };
struct Heap {
    virtual void unknown0();
    virtual void unknown1();
    virtual void unknown2();
    virtual void unknown3();
    virtual void deallocate(void*, unsigned int);
};
struct GlobalContext { int unk00, unk04, unk08, unk0c; Heap* heap; __forceinline Heap* getHeap() { return heap; } };
extern GlobalContext* __cdecl FUN_00c85750();
extern void __cdecl FUN_00c908c0(void*, VectorArray*, int, int);
struct Geometry {
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
    int unk7c;
    int unk80;
    int unk84;
    int unk88;
    int unk8c;
    int unk90;
    int unk94;
    int unk98;
    int unk9c;
    void __thiscall FUN_00de4af0(VectorArray*);
    void __thiscall FUN_00de4c40(VectorArray*, void*);
};
void __thiscall Geometry::FUN_00de4c40(VectorArray* destination, void* allocator) {
    VectorArray temporary = {0, 0, 0x80000000u};
    FUN_00de4af0(&temporary);
    int required = unk9c * 2;
    int capacity = destination->capacityAndFlags & 0x3fffffff;
    if (capacity < required) {
        int newCapacity = capacity * 2;
        if (required >= newCapacity) newCapacity = required;
        FUN_00c908c0(allocator, destination, newCapacity, 16);
    }
    destination->size = required;
    int outputIndex = 0;
    for (int i = 0; i < unk9c; ++i) {
        destination->data[outputIndex++] = temporary.data[i];
        destination->data[outputIndex++] = temporary.data[i + 1];
    }
    Heap* heap = FUN_00c85750()->getHeap();
    temporary.size = 0;
    if ((temporary.capacityAndFlags & 0x80000000u) == 0) {
        heap->deallocate(temporary.data, (temporary.capacityAndFlags & 0x3fffffff) * 16);
    }
}