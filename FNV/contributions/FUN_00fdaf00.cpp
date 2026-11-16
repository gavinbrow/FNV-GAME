extern "C" __declspec(dllimport) int __stdcall DeleteCriticalSection(void*);
extern char DAT_011f4580[];
extern "C" void __cdecl FUN_00fdaf00(void)
{
    DeleteCriticalSection(DAT_011f4580);
}
