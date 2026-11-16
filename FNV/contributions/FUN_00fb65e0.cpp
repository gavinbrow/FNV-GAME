struct _RTL_CRITICAL_SECTION;
typedef _RTL_CRITICAL_SECTION CRITICAL_SECTION;

extern "C" __declspec(dllimport) void __stdcall InitializeCriticalSection(CRITICAL_SECTION* section);
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern CRITICAL_SECTION DAT_011f600c;
void __cdecl FUN_00fdb260();

// @fnv 0x00fb65e0
void FUN_00fb65e0()
{
    InitializeCriticalSection(&DAT_011f600c);
    atexit(FUN_00fdb260);
}
