struct _RTL_CRITICAL_SECTION;
typedef _RTL_CRITICAL_SECTION CRITICAL_SECTION;

extern "C" __declspec(dllimport) void __stdcall InitializeCriticalSection(CRITICAL_SECTION* section);
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern CRITICAL_SECTION DAT_011f4800;
void __cdecl FUN_00fdaf50();

// @fnv 0x00fb5890
void FUN_00fb5890()
{
    InitializeCriticalSection(&DAT_011f4800);
    atexit(FUN_00fdaf50);
}
