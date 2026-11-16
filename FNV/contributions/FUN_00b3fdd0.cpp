
void __cdecl _Deallocate(void*);
struct FUN_00b37880_class {
    void __thiscall FUN_00b37880();
};
struct FUN_00b3fdd0_class {
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
    FUN_00b37880_class* unk5c;
    void __thiscall FUN_00b3fdd0(FUN_00b37880_class* value);
};
void __thiscall FUN_00b3fdd0_class::FUN_00b3fdd0(FUN_00b37880_class* value) {
    if (unk5c != value) {
        FUN_00b37880_class* ptr = unk5c;
        FUN_00b37880_class* old = ptr;
        old ? ((((old->FUN_00b37880(), 1) & 1) ? _Deallocate(old) : (void)0), old) : 0;
        unk5c = value;
    }
}
