extern "C" __declspec(dllimport) int __stdcall DeleteCriticalSection(void*);
extern char DAT_0126813c[];
extern "C" void __cdecl FUN_00fde160(void)
{
    DeleteCriticalSection(DAT_0126813c);
}
