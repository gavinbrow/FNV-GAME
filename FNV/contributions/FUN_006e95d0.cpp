void* __cdecl operator new(unsigned int, void*); 
void __cdecl operator delete(void*, void*);
struct FUN_006f4cd0 {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    FUN_006f4cd0();
};
struct FUN_006e95d0_Class {
    void __thiscall FUN_006e95d0(FUN_006f4cd0* destination, unsigned int count);
};
void FUN_006e95d0_Class::FUN_006e95d0(FUN_006f4cd0* destination, unsigned int count) {
    for (unsigned int i = 0; i < count; ++i) {
        new (destination + i) FUN_006f4cd0;
    }
}