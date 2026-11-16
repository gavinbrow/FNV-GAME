struct FUN_00aa4060_Class {
    void __thiscall FUN_00aa4060(void*);
};

extern FUN_00aa4060_Class DAT_011f6238;

struct FUN_00a1ec40_Class {
    int m_unk00;
    int m_unk04;
    int m_unk08;
    int m_unk0c;
    int m_unk10;
    int m_unk14;
    int m_unk18;
    int m_unk1c;
    void __thiscall FUN_00a1ec70();
    FUN_00a1ec40_Class* FUN_00a1ec40(unsigned int flags);
};

FUN_00a1ec40_Class* FUN_00a1ec40_Class::FUN_00a1ec40(unsigned int flags)
{
    int l0, l1, l2, l3, l4, l5, l6;
    FUN_00a1ec70();
    if (flags & 1)
        DAT_011f6238.FUN_00aa4060(this);
    return this;
}