extern void* DAT_01070610[];
void __cdecl FUN_00721130(void*);

struct FUN_0072a7c0 : FUN_007240c0, SL {
    int m_0c;
    int m_10;
    int m_14;
    int m_18;
    short m_1c;
    float m_20;
    float m_24;
    float m_28;
    short m_2c;

    void FUN_007a1950(int, int);
    FUN_0072a7c0();
};

FUN_0072a7c0::FUN_0072a7c0() : FUN_007240c0(), SL() {
    m_pad = reinterpret_cast<int>(DAT_01070610);
    m_14 = 0;
    m_10 = 0;
    m_0c = 0;
    m_18 = 0;
    m_2c = 0;
    m_1c = 0;
    m_28 = 0.0f;
    m_24 = 0.0f;
    m_20 = 0.0f;
    FUN_007a1950(0, 1);
    FUN_00721130(this);
}