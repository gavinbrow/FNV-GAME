struct __declspec(align(16)) FUN_00dd1bf0_Obj
{
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
    int unk30;
    int unk34;
    int unk38;
    int unk3C;

    void __thiscall FUN_00dd1bf0(void* target, int a, int b, float c, int d);
};

struct FUN_00d54350_Obj
{
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    void* unk14;

    void __thiscall FUN_00d54350(int a, int b, float c, int d);
};

void __thiscall FUN_00d54350_Obj::FUN_00d54350(int a, int b, float c, int d)
{
    FUN_00dd1bf0_Obj local;
    local.FUN_00dd1bf0(unk14, a, b, c, d);
}
