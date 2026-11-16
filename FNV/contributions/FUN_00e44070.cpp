extern int DAT_010e60c4;

struct FUN_00e44070 {
    int* volatile m_00;
    unsigned short unk04;
    volatile unsigned short m_06;
    volatile float m_08;
    volatile float m_0c;
    void* volatile m_10;
    volatile int m_14;
    volatile unsigned int m_18;

    FUN_00e44070();
};

FUN_00e44070::FUN_00e44070()
{
    m_06 = 1;
    m_00 = &DAT_010e60c4;
    m_10 = 0;
    m_14 = 0;
    m_18 = 0x80000000u;
    m_08 = 0.0f;
    m_0c = 0.0f;
}