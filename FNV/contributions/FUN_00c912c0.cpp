struct FUN_00c912c0_Class : hkpWorld {
    unsigned int FUN_00c912c0();
};
unsigned int FUN_00c912c0_Class::FUN_00c912c0()
{
    volatile unsigned short* markCount = &m_multiThreadCheck.m_markCount;
    unsigned char highBit = static_cast<unsigned char>(*markCount >> 15);
    return highBit & 1;
}