// The standard Win32 critical-section object occupies 24 bytes on this target.
struct CriticalSection
{
    void* debugInfo;
    long lockCount;
    long recursionCount;
    void* owningThread;
    void* lockSemaphore;
    unsigned long spinCount;
};

extern CriticalSection DAT_0126820c;
extern "C" __declspec(dllimport) void __stdcall InitializeCriticalSection(CriticalSection* section);
extern "C" void __cdecl FUN_00fde1a0();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbd9c0
void FUN_00fbd9c0()
{
    InitializeCriticalSection(&DAT_0126820c);
    atexit(FUN_00fde1a0);
}
