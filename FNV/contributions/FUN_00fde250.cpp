extern "C" __declspec(dllimport) int __stdcall TlsFree(void*);
extern void* DAT_0126835c;
extern "C" void __cdecl FUN_00fde250(void)
{
    TlsFree(DAT_0126835c);
}
