extern "C" __declspec(dllimport) unsigned long __stdcall TlsAlloc();
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern unsigned long DAT_012681d8;
void __cdecl FUN_00fde190();

// @fnv 0x00fbd8c0
void FUN_00fbd8c0()
{
    DAT_012681d8 = TlsAlloc();
    atexit(FUN_00fde190);
}
