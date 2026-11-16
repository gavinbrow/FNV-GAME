struct _RTL_CRITICAL_SECTION;
typedef _RTL_CRITICAL_SECTION CRITICAL_SECTION;

extern "C" __declspec(dllimport) void __stdcall InitializeCriticalSection(CRITICAL_SECTION* section);
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern CRITICAL_SECTION DAT_011f4180;
void __cdecl FUN_00fdae40();

// @fnv 0x00fb54e0
void FUN_00fb54e0()
{
    InitializeCriticalSection(&DAT_011f4180);
    atexit(FUN_00fdae40);
}
