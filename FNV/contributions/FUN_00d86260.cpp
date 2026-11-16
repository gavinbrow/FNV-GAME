extern int DAT_010d3838;
struct FUN_00d86260_Class {
    unsigned int m_vptr;
    unsigned short m_word04;
    unsigned short m_word06;
    volatile unsigned char m_byte08;
    volatile float m_float0C;
    float m_float10;
    float m_float14;
    float m_float18;
    FUN_00d86260_Class(float a, float b, float c);
};
FUN_00d86260_Class::FUN_00d86260_Class(float a, float b, float c)
{
    m_word06 = 1;
    m_byte08 = 0;
    m_float0C = -c;
    m_vptr = (unsigned int)&DAT_010d3838;
    m_float10 = c;
    m_byte08 = 3;
    m_float14 = a;
    m_float18 = b;
}