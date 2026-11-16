struct FUN_00d53d90 : S_00cc4b90_RefObj {
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
    FUN_00d53d90();
};
struct S_00cc9020_Cls {
    int unk00;
    FUN_00d53d90* m_object;
    int __thiscall FUN_00cc9020();
};
int S_00cc9020_Cls::FUN_00cc9020()
{
    S_00cc4b90_Ctx memoryContext(16);
    if (!m_object)
        m_object = new FUN_00d53d90();
    return 52;
}