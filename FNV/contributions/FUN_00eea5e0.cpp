extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long* value);
extern const char* _EmptyFS;
extern volatile long DAT_011f4400;
extern unsigned int UNK_0101dce4;

struct FixedStringOwner {
    void* m_vftable;
    unsigned int m_uiUnknown04;
    const char* m_firstString;
    const char* m_secondString;
    const char* m_thirdString;
    const char* m_fourthString;
    const char* m_fifthString;

    void FUN_00eea5e0();
};

void FixedStringOwner::FUN_00eea5e0() {
    if (m_fifthString != _EmptyFS)
        InterlockedDecrement(reinterpret_cast<volatile long*>(const_cast<char*>(m_fifthString) - 8));
    if (m_fourthString != _EmptyFS)
        InterlockedDecrement(reinterpret_cast<volatile long*>(const_cast<char*>(m_fourthString) - 8));
    if (m_thirdString != _EmptyFS)
        InterlockedDecrement(reinterpret_cast<volatile long*>(const_cast<char*>(m_thirdString) - 8));
    if (m_secondString != _EmptyFS)
        InterlockedDecrement(reinterpret_cast<volatile long*>(const_cast<char*>(m_secondString) - 8));
    if (m_firstString != _EmptyFS)
        InterlockedDecrement(reinterpret_cast<volatile long*>(const_cast<char*>(m_firstString) - 8));

    m_vftable = &UNK_0101dce4;
    InterlockedDecrement(&DAT_011f4400);
}