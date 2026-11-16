struct _RTL_CRITICAL_SECTION;
typedef _RTL_CRITICAL_SECTION CRITICAL_SECTION;

extern "C" __declspec(dllimport) void __stdcall InitializeCriticalSection(CRITICAL_SECTION* section);
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern CRITICAL_SECTION DAT_01267e48;
void __cdecl FUN_00fde140();

// @fnv 0x00fbd590
void FUN_00fbd590()
{
    InitializeCriticalSection(&DAT_01267e48);
    atexit(FUN_00fde140);
}
