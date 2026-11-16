struct _RTL_CRITICAL_SECTION;
typedef _RTL_CRITICAL_SECTION CRITICAL_SECTION;

extern CRITICAL_SECTION DAT_0126f600;
extern "C" __declspec(dllimport) void __stdcall InitializeCriticalSection(CRITICAL_SECTION* section);
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fde330();

// @fnv 0x00fc73e0
void FUN_00fc73e0()
{
    InitializeCriticalSection(&DAT_0126f600);
    atexit(FUN_00fde330);
}
