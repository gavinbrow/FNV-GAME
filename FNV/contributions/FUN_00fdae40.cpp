extern "C" __declspec(dllimport) int __stdcall DeleteCriticalSection(void*);
extern char DAT_011f4180[];
extern "C" void __cdecl FUN_00fdae40(void)
{
    DeleteCriticalSection(DAT_011f4180);
}
