struct FUN_00e531a0_struct {
    float m_00;
    float m_04;
    float m_08;
    float m_0c;

    FUN_00e531a0_struct* FUN_00e531a0(const FUN_00e531a0_struct* other);
};

FUN_00e531a0_struct* FUN_00e531a0_struct::FUN_00e531a0(const FUN_00e531a0_struct* other)
{
    m_00 += other->m_00;
    m_04 += other->m_04;
    m_08 += other->m_08;
    m_0c += other->m_0c;
    return this;
}
