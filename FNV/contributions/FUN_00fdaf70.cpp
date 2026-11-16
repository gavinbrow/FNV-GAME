extern "C" __declspec(dllimport) int __stdcall DeleteCriticalSection(void*);
extern char DAT_011f4900[];
extern "C" void __cdecl FUN_00fdaf70(void)
{
    DeleteCriticalSection(DAT_011f4900);
}
