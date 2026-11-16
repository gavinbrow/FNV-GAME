extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(long volatile* addend);
struct FUN_00ae8650_cls {
    unsigned int m_00,m_04,m_08,m_0c;
    void* m_10;
    float m_14,m_18,m_1c;
    FUN_00ae8650_cls* FUN_00ae8650();
};
FUN_00ae8650_cls* FUN_00ae8650_cls::FUN_00ae8650() {
    void* t;
    {
        void** slot = &m_10;
        *slot = 0;
        if (*slot != 0) {
            t = *slot;
            InterlockedIncrement((long*)((char*)t + 4));
        }
    }
    m_00 = 0;
    m_04 = 0;
    m_08 = 0;
    m_0c = 0;
    m_14 = 0.0f;
    m_18 = 0.0f;
    m_1c = 0.0f;
    return this;
}