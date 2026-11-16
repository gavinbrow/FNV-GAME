struct FUN_00a25810_Target
{
    int m_00;
    int m_04;
    int m_08;
    int m_0c;
    int m_10;
    int m_14;
    int m_18;
    int m_1c;
    int m_20;
};

struct FUN_00a25810_Class
{
    void FUN_00a25810();
};

extern "C" void __stdcall FUN_00ee820a(int, unsigned short*);

void FUN_00a25810_Class::FUN_00a25810()
{
    if (*reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(this) + 0x1b88))
    {
        struct Values
        {
            unsigned short m_00;
            unsigned short m_04;
        };

        Values values;
        values.m_00 = 0;
        values.m_04 = 0;

        FUN_00a25810_Target* target =
            *reinterpret_cast<FUN_00a25810_Target**>(
                reinterpret_cast<char*>(this) + 0x1b80);

        target->m_0c = 0;
        target->m_20 = 0;
        FUN_00ee820a(0, &values.m_00);
    }
}