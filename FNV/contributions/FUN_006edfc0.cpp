extern unsigned int DAT_010a2720;
void* __cdecl operator new(unsigned int size, void* place);
void __cdecl operator delete(void* ptr, void* place);
struct FUN_006ee050_Size28 : public FUN_006ee050_Class {
    int extra0c;
    int extra10;
    int extra14;
    int extra18;
    __forceinline FUN_006ee050_Size28() : FUN_006ee050_Class() {}
};
struct FUN_006edfc0_Host {
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
    FUN_00aa54a0_s allocator;
    void* __thiscall FUN_006edfc0();
};
void* FUN_006edfc0_Host::FUN_006edfc0() {
    void* memory = allocator.Allocate(0x1c, DAT_010a2720);
    new (memory) FUN_006ee050_Size28;
    return memory;
}