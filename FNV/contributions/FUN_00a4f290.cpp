struct FUN_00a4f290_class {
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

    bool __thiscall FUN_00a57c10(FUN_00a4f290_class*);
    unsigned char __thiscall FUN_00a4f290(FUN_00a4f290_class*);
};

unsigned char FUN_00a4f290_class::FUN_00a4f290(FUN_00a4f290_class* param)
{
    if (!FUN_00a57c10(param)) {
        return 0;
    }

    return unk4c == param->unk4c;
}