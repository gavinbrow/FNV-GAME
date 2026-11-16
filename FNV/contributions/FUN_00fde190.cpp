extern "C" __declspec(dllimport) int __stdcall TlsFree(void*);
extern void* DAT_012681d8;
extern "C" void __cdecl FUN_00fde190(void)
{
    TlsFree(DAT_012681d8);
}
