extern "C" __declspec(dllimport) int __stdcall TlsFree(void*);
extern void* DAT_01268108;
extern "C" void __cdecl FUN_00fde150(void)
{
    TlsFree(DAT_01268108);
}
