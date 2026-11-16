extern "C" __declspec(dllimport) unsigned long __stdcall GetTickCount();

struct FUN_00aea0a0_Class
{
    void* vtbl;
    unsigned long m_tick;
    int m_zero;

    void* __thiscall FUN_00aea0a0();
};

void* __thiscall FUN_00aea0a0_Class::FUN_00aea0a0()
{
    m_zero = 0;
    vtbl = (void*)0x927c0;
    m_tick = GetTickCount();
    return this;
}