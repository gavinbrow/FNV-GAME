struct FUN_00df7a60_class {
    void* m_vtable;
    int unk04;
    int unk08;
    int unk0c;
    void* m_p10;
    int unk14;
    int unk18;
    void* m_p1c;

    void __thiscall FUN_00df7a60();
};

extern "C" __declspec(dllimport) long __stdcall InterlockedExchangeAdd(
    volatile long* value,
    long increment);

void __cdecl FUN_00d043c0(void* object, int value);

void FUN_00df7a60_class::FUN_00df7a60()
{
    if (m_p1c != 0) {
        InterlockedExchangeAdd(
            static_cast<volatile long*>(m_p1c),
            1);
    }

    if (m_p10 != 0) {
        FUN_00d043c0(m_p10, 1);
    }
}