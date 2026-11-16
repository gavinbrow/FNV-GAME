extern "C" __declspec(dllimport) int __stdcall TlsFree(void*);
extern void* DAT_012687c8;
extern "C" void __cdecl FUN_00fde270(void)
{
    TlsFree(DAT_012687c8);
}
