struct FUN_0040c930_m30 {
    virtual void vfn_0();
    virtual void vfn_4();
    virtual void vfn_8();
    virtual void vfn_c();
    virtual void vfn_10();
    virtual void vfn_14();
    virtual void vfn_18();
    virtual void vfn_1c();
    virtual void vfn_20();
    virtual void vfn_24();
    virtual void vfn_28();
    virtual void vfn_2c();
    virtual void vfn_30();
    virtual void vfn_34(MagicItem* other);
};

struct FUN_00405b10_Obj {
    void FUN_00405b10(int other);
};

struct FUN_005054b0_shell {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    int unk20;
    int unk24;
    int unk28;
    int unk2C;
    FUN_0040c930_m30 m30;
    int unk34;
    int unk38;
    FUN_00405b10_Obj m3c;

    void FUN_004851b0(TESForm* other);
    void FUN_0040c930(TESForm* arg);
};

extern int DAT_01183028;
extern int DAT_011830e8;

MagicItemObject* __cdecl FUN_00ec43fb(TESForm* arg, int a, int* b, int* c, int d);

void FUN_005054b0_shell::FUN_0040c930(TESForm* arg)
{
    MagicItemObject* result = FUN_00ec43fb(arg, 0, &DAT_01183028, &DAT_011830e8, 0);
    if (!result)
        return;

    FUN_004851b0(arg);

    m30.vfn_34(result ? reinterpret_cast<MagicItem*>(reinterpret_cast<char*>(result) + 0x30) : 0);

    m3c.FUN_00405b10(result ? reinterpret_cast<int>(reinterpret_cast<char*>(result) + 0x3C) : 0);
}