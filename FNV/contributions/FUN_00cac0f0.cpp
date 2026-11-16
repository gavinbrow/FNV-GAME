struct CA0F0Result {
    int unk00;
    int unk04;
    int m_8;
};
struct CA0F0Object : BaseThunk {
    int __thiscall FUN_00cac0f0();
};
int CA0F0Object::FUN_00cac0f0()
{
    int value = 0;
    if (m_8) {
        CA0F0Result* result = static_cast<CA0F0Result*>(m_8->FUN_00cac980());
        if (result)
            value = result->m_8;
    }
    return value;
}