extern "C" __declspec(dllimport) int __stdcall DeleteCriticalSection(void*);
extern char DAT_011f600c[];
extern "C" void __cdecl FUN_00fdb260(void)
{
    DeleteCriticalSection(DAT_011f600c);
}
