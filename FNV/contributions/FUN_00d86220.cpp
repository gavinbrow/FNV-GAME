extern int DAT_010d3838;
struct FUN_00d86220_Class {
    unsigned int m_vptr;
    unsigned short m_word04;
    unsigned short m_word06;
    volatile unsigned char m_byte08;
    volatile float m_float0C;
    float m_float10;
    float m_float14;
    float m_float18;
    FUN_00d86220_Class();
};
FUN_00d86220_Class::FUN_00d86220_Class()
{
    m_word06 = 1;
    m_byte08 = 0;
    m_float0C = -1000000.0f;
    m_float10 = 1000000.0f;
    m_vptr = (unsigned int)&DAT_010d3838;
    m_byte08 = 3;
    m_float14 = 0.0f;
    m_float18 = 0.0f;
}
