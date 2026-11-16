extern "C" __declspec(dllimport) int __stdcall DeleteCriticalSection(void*);
extern char DAT_01202600[];
extern "C" void __cdecl FUN_00fdd410(void)
{
    DeleteCriticalSection(DAT_01202600);
}
