struct FUN_00a59d30_Class {
    void* __thiscall FUN_00a59d30(int);
    void __thiscall FUN_00654640(void*);
};

struct FUN_00bb5ff0_Class {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    unsigned int unk20;
    int unk24;
    int unk28;
    int unk2C;
    int unk30;
    int unk34;
    int unk38;
    int unk3C;
    int unk40;
    int unk44;
    int unk48;
    int unk4C;
    int unk50;
    int unk54;
    int unk58;
    float unk5C;

    bool __thiscall FUN_00b67a40(FUN_00a59d30_Class* a1);
    bool __thiscall FUN_00bb5ff0(FUN_00a59d30_Class* a1);
};

bool FUN_00bb5ff0_Class::FUN_00bb5ff0(FUN_00a59d30_Class* a1)
{
    bool result = FUN_00b67a40(a1);
    if ((unk20 & 0x80000) > 0) {
        unk5C = 1.0f;
    }
    void* prop = a1->FUN_00a59d30(10);
    if (prop) {
        a1->FUN_00654640(prop);
    }
    return result;
}
