struct FUN_006a21c0_class
{
    virtual void v0();
    virtual int v4(int value);
    virtual int v8(int value);
    virtual int vc(int value1, int value2);

    int m_4;
    int m_8;
    int m_c;

    void __thiscall FUN_006a21c0(int value, int flag);
    void __thiscall FUN_006a2270(int value1, int value2, int value3);
    void __thiscall FUN_006a8500();
};

void __thiscall FUN_006a21c0_class::FUN_006a21c0(int value, int flag)
{
    if (m_4 != 0)
    {
        if (flag == m_c)
        {
            m_4 = vc(m_4, value);
        }
        else
        {
            int newValue = v4(value);
            FUN_006a2270(newValue, m_4, flag);
            FUN_006a8500();
            m_4 = newValue;
        }
    }
    else
    {
        m_4 = v4(value);
        m_c = value;
    }
}