
struct Allocator {
    virtual void vfn0();
    virtual void vfn4();
    virtual void Free(void* pointer, unsigned short size);
};
struct MemorySystem {
    unsigned int field00;
    unsigned int field04;
    unsigned int field08;
    unsigned int field0c;
    Allocator* allocator;
};
extern char DAT_010c6fb0;
extern char DAT_0102e388;
struct Holder {
    void* vtable;
    unsigned short memSizeAndFlags;
    unsigned short referenceCount;
    unsigned int userData;
    unsigned int shapeType;
    void* shapeVtable;
    MemorySystem* __thiscall FUN_00c85750();
    Holder* __thiscall FUN_00cf57e0(unsigned char flags);
};
Holder* __thiscall Holder::FUN_00cf57e0(unsigned char flags)
{
    shapeVtable = &DAT_010c6fb0;
    vtable = &DAT_0102e388;
    if ((flags & 1) != 0) {
        MemorySystem* memory = FUN_00c85750();
        memory->allocator->Free(this, memSizeAndFlags);
    }
    return this;
}