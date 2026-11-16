extern "C" __declspec(dllimport) int __stdcall DeleteCriticalSection(void*);
extern char DAT_0126f600[];
extern "C" void __cdecl FUN_00fde330(void)
{
    DeleteCriticalSection(DAT_0126f600);
}
