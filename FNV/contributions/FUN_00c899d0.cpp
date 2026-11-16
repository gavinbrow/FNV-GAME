struct FUN_00c899d0_Target {
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
    void* unk2c;
};

struct FUN_00c899d0_Class {
    int unk00;
    int unk04;
    FUN_00c899d0_Target* unk08;

    void FUN_00c87c90(bool b);
    void FUN_00c899d0(bool b);
};

void FUN_00c899d0_Class::FUN_00c899d0(bool b)
{
    if (this && unk08) {
        unk08->unk2c = b ? this : 0;
    }
    FUN_00c87c90(b);
}
