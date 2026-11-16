struct FUN_0066e920_Class
{
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
};

extern int DAT_011e0618[77];
extern unsigned char DAT_011e074c;
extern int DAT_011e0750;

FUN_0066e920_Class* __cdecl FUN_0066e920(int index);

void __cdecl FUN_00937fd0()
{
    if (!DAT_011e074c)
    {
        int count = 0;

        for (int index = 0; index < 0x4d; ++index)
        {
            FUN_0066e920_Class* object = FUN_0066e920(index);

            if (object && (object->unk44 & 1))
            {
                DAT_011e0618[index] = count;
                ++count;
            }
            else
            {
                DAT_011e0618[index] = 0x4d;
            }
        }

        DAT_011e0750 = count;
        DAT_011e074c = 1;
    }
}