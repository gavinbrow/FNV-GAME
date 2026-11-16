struct FUN_009f7500_class {
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
    unsigned int unk4c;
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int unk5c;
    unsigned int unk60;
    unsigned int unk64;
    unsigned int unk68;
    unsigned int unk6c;
    unsigned int unk70;
    unsigned int unk74;
    unsigned int unk78;
    unsigned int unk7c;
    unsigned int field80;
    float field84;
    float field88;
    float field8c;
    unsigned char field90;
    unsigned char pad91;
    unsigned char pad92;
    unsigned char pad93;
    struct ThreeWords {
        unsigned int first;
        unsigned int second;
        unsigned int third;
    } field94;
    ArrSI arrA0;
    void FUN_00673290(void*);
    void FUN_009f7500(void*);
};
extern int DAT_01183028;
extern int DAT_011a5fd8;
extern void* __cdecl FUN_00ec43fb(void*, int, int*, int*, int);
void FUN_009f7500_class::FUN_009f7500(void* param_2)
{
    FUN_00673290(param_2);
    FUN_009f7500_class* other = (FUN_009f7500_class*)FUN_00ec43fb(
        param_2, 0, &DAT_01183028, &DAT_011a5fd8, 0);
    if (other != 0)
    {
        field80 = other->field80;
        field84 = other->field84;
        field88 = other->field88;
        field8c = other->field8c;
        field94 = other->field94;
        field90 = other->field90;
        int count = other->arrA0.GetFlags();
        ((FUN_009f8b30_class*)&arrA0)->FUN_009f8b30(count, 1);
        int i;
        for (i = 0; i < count; i++)
        {
            ((SpectatorThreatInfo62d0*)((FUN_009f8a80_class*)&arrA0)->FUN_009f8a80(i))->FUN_009f7630(
                *(SpectatorThreatInfo62d0*)((FUN_009f8a80_class*)&other->arrA0)->FUN_009f8a80(i));
        }
    }
}