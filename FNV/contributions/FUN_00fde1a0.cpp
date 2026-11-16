extern "C" __declspec(dllimport) int __stdcall DeleteCriticalSection(void*);
extern char DAT_0126820c[];
extern "C" void __cdecl FUN_00fde1a0(void)
{
    DeleteCriticalSection(DAT_0126820c);
}
