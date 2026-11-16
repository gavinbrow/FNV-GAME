struct _RTL_CRITICAL_SECTION;
typedef _RTL_CRITICAL_SECTION CRITICAL_SECTION;

extern "C" __declspec(dllimport) void __stdcall InitializeCriticalSection(CRITICAL_SECTION* section);
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern CRITICAL_SECTION DAT_011f5c80;
void __cdecl FUN_00fdb0c0();

// @fnv 0x00fb6090
void FUN_00fb6090()
{
    InitializeCriticalSection(&DAT_011f5c80);
    atexit(FUN_00fdb0c0);
}
