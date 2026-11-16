struct _RTL_CRITICAL_SECTION;
typedef _RTL_CRITICAL_SECTION CRITICAL_SECTION;

extern "C" __declspec(dllimport) void __stdcall InitializeCriticalSection(CRITICAL_SECTION* section);
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern CRITICAL_SECTION DAT_011f4580;
void __cdecl FUN_00fdaf00();

// @fnv 0x00fb5800
void FUN_00fb5800()
{
    InitializeCriticalSection(&DAT_011f4580);
    atexit(FUN_00fdaf00);
}
