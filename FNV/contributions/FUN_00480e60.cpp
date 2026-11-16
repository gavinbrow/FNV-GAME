struct ModelData {
    virtual void Function0();
    virtual void Function1();
    virtual void Function2();
    virtual void Function3();
    virtual void Function4();
    virtual unsigned int GetValue();
};
struct FormEntry {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    ModelData model;
    unsigned int FUN_00481190(unsigned int);
};
struct ExtraData {
    unsigned int FUN_00401170();
    unsigned int FUN_005f0cc0();
};
struct Reference {
    ExtraData* FUN_00567790();
};
extern "C" unsigned char DAT_01183028;
extern "C" unsigned char DAT_01183978;
extern "C" FormEntry* __cdecl func_0x00ec43fb(void*, unsigned int, void*, void*, unsigned int);
unsigned int __cdecl FUN_00480e60(void* source, Reference* reference) {
    FormEntry* form4 = func_0x00ec43fb(source, 0, &DAT_01183028, &DAT_01183978, 0);
    if (form4 == 0) return 0;
    if (reference == 0) return form4->model.GetValue();
    ExtraData* extra = reference->FUN_00567790();
    unsigned int value = 0;
    if (extra != 0 && extra->FUN_00401170() == 42) {
        value = extra->FUN_005f0cc0();
    }
    return form4->FUN_00481190(value);
}
