struct AllocatorInterface {
    virtual void First();
    virtual void Second();
    virtual void Deallocate(void* address, unsigned int size);
};
struct AllocatorHolder {
    int unk00; int unk04; int unk08; int unk0c;
    AllocatorInterface* allocator;
};
AllocatorHolder* __cdecl FUN_00c85750();
struct FUN_00d9c010_class { void __thiscall FUN_00d9c010(); };
struct FUN_00d9c2e0_class {
    virtual ~FUN_00d9c2e0_class();
    int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18;
    FUN_00d9c010_class unk1c;
    int unk20; int unk24; int unk28; int unk2c; int unk30; int unk34; int unk38; int unk3c;
    int unk40; int unk44; int unk48; int unk4c; int unk50; int unk54; int unk58; int unk5c;
    int unk60; int unk64; int unk68; int unk6c; int unk70; int unk74; int unk78; int unk7c;
    static void __cdecl operator delete(void* address, unsigned int size);
};
FUN_00d9c2e0_class::~FUN_00d9c2e0_class() {
    ((FUN_00d9be30_class*)this)->FUN_00d9be30();
    unk1c.FUN_00d9c010();
}
void __cdecl FUN_00d9c2e0_class::operator delete(void* address, unsigned int size) {
    AllocatorHolder* holder = FUN_00c85750();
    holder->allocator->Deallocate(address, size);
}
