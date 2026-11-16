extern "C" __declspec(dllimport) int __stdcall DeleteCriticalSection(void*);
extern char DAT_011f4800[];
extern "C" void __cdecl FUN_00fdaf50(void)
{
    DeleteCriticalSection(DAT_011f4800);
}
