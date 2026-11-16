struct _RTL_CRITICAL_SECTION
{
    void* debugInfo;
    long lockCount;
    long recursionCount;
    void* owningThread;
    void* lockSemaphore;
    unsigned long spinCount;
};
extern _RTL_CRITICAL_SECTION DAT_01203328;
extern "C" __declspec(dllimport) void __stdcall DeleteCriticalSection(_RTL_CRITICAL_SECTION* cs);
struct CriticalSectionCleanup
{
    ~CriticalSectionCleanup()
    {
        DeleteCriticalSection(&DAT_01203328);
    }
};
// @fnv 0x00fddcd0
CriticalSectionCleanup g_criticalSectionCleanup;
