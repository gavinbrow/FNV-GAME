struct FUN_00aa5ff0_Class {
    unsigned int m_count;
    unsigned int m_threadId;

    void __thiscall FUN_00aa5ff0();
};

extern "C" __declspec(dllimport) unsigned long __stdcall GetCurrentThreadId();
extern "C" __declspec(dllimport) void __stdcall Sleep(unsigned long);
extern "C" __declspec(dllimport) long __stdcall InterlockedCompareExchange(
    volatile long* destination,
    long exchange,
    long comparand);

void __thiscall FUN_00aa5ff0_Class::FUN_00aa5ff0()
{
    unsigned long threadId = GetCurrentThreadId();

    if (m_threadId == threadId) {
        m_count = m_count + 1;
    } else {
        unsigned int count = m_count & 0x0fffffff;

        while (InterlockedCompareExchange(
                   reinterpret_cast<volatile long*>(&m_count),
                   static_cast<long>(count + 1),
                   static_cast<long>(count)) != static_cast<long>(count)) {
            Sleep(0);
            count = m_count & 0x0fffffff;
        }
    }
}