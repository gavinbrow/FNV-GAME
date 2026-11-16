struct FUN_007c56e0_shell
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
    int sourceValues[10];
    int unk54;
    int unk58;
    int unk5C;
    int unk60;
    int unk64;
    int unk68;
    int unk6C;
    int unk70;
    int unk74;
    int unk78;
    int unk7C;
    int unk80;
    int unk84;
    int unk88;
    int unk8C;
    int unk90;
    int unk94;
    int unk98;
    int unk9C;
    int unkA0;
    int unkA4;
    int unkA8;
    int unkAC;
    int unkB0;
    int unkB4;
    int unkB8;
    int unkBC;
    int unkC0;
    int unkC4;
    int unkC8;
    int unkCC;
    int valueCount;
    int unkD4;
    int unkD8;
    int savedResults[3];
    int currentResults[3];

    int FUN_007c5760();
    void FUN_007c56e0();
};

int __cdecl FUN_00944460(int, int);

void FUN_007c56e0_shell::FUN_007c56e0()
{
    for (int i = 0; i < 3; ++i)
    {
        savedResults[i] = currentResults[i];
        currentResults[i] = sourceValues[FUN_00944460(0, valueCount * 2 - 1)];
    }

    FUN_007c5760();
}