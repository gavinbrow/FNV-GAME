struct FUN_00d5ee80_class {
    unsigned int unk00;
    void* unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    void* unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    void* unk30;
    void* unk34;
    void* unk38;
    void* unk3c;
    volatile void* unk40;
    unsigned int unk44;
    void __thiscall FUN_00d5ee80(void* a, void* b, void* c, void* d);
};
struct Allocator { virtual void* first(); virtual void* allocate(unsigned int); };
struct Existing { void __thiscall FUN_00c903a0(); };
struct Old { void __thiscall FUN_00c903b0(); };
extern void* DAT_01269a84;
extern void* __cdecl FUN_00da2bc0();
void __thiscall FUN_00d5ee80_class::FUN_00d5ee80(void* a, void* b, void* c, void* d) {
    unk30 = a; unk34 = b; unk38 = c; unk3c = d; unk44 = 0;
    if (!DAT_01269a84) {
        void* x = FUN_00da2bc0();
        if (DAT_01269a84) ((Old*)DAT_01269a84)->FUN_00c903b0();
        DAT_01269a84 = x;
    }
    unk04 = DAT_01269a84;
    ((Existing*)unk04)->FUN_00c903a0();
    void* result = ((Allocator*)b)->allocate(12);
    if (result) { ((unsigned int*)result)[0] = 0; ((unsigned int*)result)[1] = 0; ((unsigned int*)result)[2] = 0xffffffff; } else { result = 0; }
    this->unk14 = b; this->unk40 = result;
}













