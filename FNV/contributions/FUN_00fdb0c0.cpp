extern "C" __declspec(dllimport) int __stdcall DeleteCriticalSection(void*);
extern char DAT_011f5c80[];
extern "C" void __cdecl FUN_00fdb0c0(void)
{
    DeleteCriticalSection(DAT_011f5c80);
}
