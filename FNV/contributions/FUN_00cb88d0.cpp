struct FUN_00d2acf0 {
    void* vtable;
    unsigned short memorySizeAndFlags;
    unsigned short referenceCount;
    unsigned int unk08, unk0C, unk10, unk14;
    unsigned int unk18, unk1C, unk20, unk24;
    unsigned int unk28, unk2C, unk30, unk34;
    unsigned int unk38, unk3C, unk40, unk44;
    unsigned int unk48, unk4C, unk50, unk54;
    unsigned int unk58, unk5C;

    FUN_00d2acf0(void* source, void* start, void* end, float nearValue, float farValue, int flags);
    void FUN_00c905b0();

    static void* operator new(unsigned int bytes) {
        FNVTaskMemoryRouter* router = FUN_00c85750();
        FUN_00d2acf0* object = (FUN_00d2acf0*)((CAC300Allocator*)router->allocator)->Alloc(bytes);
        object->memorySizeAndFlags = (unsigned short)bytes;
        return object;
    }
    static void operator delete(void* object);
};

struct FUN_00cb88d0_owner : CAC300Owner {
    void __thiscall FUN_00cb88d0(void* parameters);
};

void FUN_00cb88d0_owner::FUN_00cb88d0(void* parameters)
{
    CA2020AllocTagScope allocationTag(16);
    FUN_00d2acf0* shape = new FUN_00d2acf0(
        *(void**)((char*)parameters + 4),
        (char*)parameters + 0x10,
        (char*)parameters + 0x20,
        *(float*)((char*)parameters + 0x30),
        *(float*)((char*)parameters + 0x34),
        0);
    SetObject((hkReferencedObject*)shape);
    shape->FUN_00c905b0();
    Apply((int)parameters);
}