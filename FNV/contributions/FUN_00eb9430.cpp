struct QueryContext
{
    int unk00;
    void FUN_00eba480(void* detail);
    int FUN_00ebf610(void* a1, void* a2);
};
struct ChildTest
{
    virtual void Slot00() = 0;
    virtual void Slot04() = 0;
    virtual void Slot08() = 0;
    virtual void Slot0c() = 0;
    virtual int Test(void* a1, void* a2, int a3, int a4, void* a5, int a6) = 0;
};
struct RayNode
{
    void* unk00;
    QueryContext context;
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
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    int unk60;
    int unk64;
    int unk68;
    int unk6c;
    int unk70;
    int unk74;
    int unk78;
    int unk7c;
    ChildTest* m_0x80;
    ChildTest* m_0x84;
    int m_0x88;
    int FUN_00eb9430(void* a1, void* a2, int a3, int a4, void* a5, int a6);
};
int RayNode::FUN_00eb9430(void* a1, void* a2, int a3, int a4, void* a5, int a6)
{
    if (a6 != m_0x88)
    {
        context.FUN_00eba480((char*)a5 + 0x68);
        m_0x88 = a6;
    }
    if (!context.FUN_00ebf610(a1, a2))
        return 0;
    int result;
    if (m_0x80 != 0)
    {
        result = m_0x80->Test(a1, a2, a3, a4, a5, a6);
        if (result >= 1)
            return result;
    }
    if (m_0x84 != 0)
    {
        result = m_0x84->Test(a1, a2, a3, a4, a5, a6);
        if (result >= 1)
            return result;
    }
    return 0;
}
