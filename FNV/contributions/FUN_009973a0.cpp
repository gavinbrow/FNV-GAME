struct Inner009973a0
{
    int a;
    int b;
    int c;
    int d;
};

struct FUN_009973a0_class
{
    Inner009973a0 m_00;
    int m_10;
    int m_14;
    float m_18;
    int m_1c;

    void __thiscall FUN_009973a0(const FUN_009973a0_class* src);
};

void __thiscall FUN_009973a0_class::FUN_009973a0(const FUN_009973a0_class* 
src)
{
    m_00 = src->m_00;
    m_10 = src->m_10;
    m_14 = src->m_14;
    m_18 = src->m_18;
    m_1c = src->m_1c;
}
