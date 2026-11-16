struct ACS00bac {
    void* m_p;
};

struct A5A040Cls {
    void FUN_00a5a040();
};

struct BA86C0Owner {
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
    int unk40;
    int unk44;
    int unk48;
    int unk4C;
    int unk50;
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
    int* unkAC;

    int FUN_00ba86c0(A5A040Cls* pArg, int arg2, int arg3);
};

int BA86C0Owner::FUN_00ba86c0(A5A040Cls* pArg, int arg2, int arg3)
{
    if ((char*)pArg + 0x9c == 0)
        pArg->FUN_00a5a040();
    if (*unkAC == 0)
        unk58 = 0;
    return 0;
}
