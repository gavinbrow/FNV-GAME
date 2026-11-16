struct _RTL_CRITICAL_SECTION;
typedef _RTL_CRITICAL_SECTION CRITICAL_SECTION;

extern "C" __declspec(dllimport) void __stdcall InitializeCriticalSection(CRITICAL_SECTION* section);
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern CRITICAL_SECTION DAT_011f4380;
void __cdecl FUN_00fdae60();

// @fnv 0x00fb5670
void FUN_00fb5670()
{
    InitializeCriticalSection(&DAT_011f4380);
    atexit(FUN_00fdae60);
}
