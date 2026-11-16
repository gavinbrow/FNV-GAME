extern "C" __declspec(dllimport) int __stdcall DeleteCriticalSection(void*);
extern char DAT_01267e48[];
extern "C" void __cdecl FUN_00fde140(void)
{
    DeleteCriticalSection(DAT_01267e48);
}
