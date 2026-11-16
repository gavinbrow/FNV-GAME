extern unsigned char DAT_011dd9e8;
extern "C" void __cdecl FUN_0083b770(void*);
extern "C" void __cdecl FUN_0083b7d0(void*);
extern "C" void __cdecl FUN_00fd8c20();
extern "C" void __stdcall FUN_00ec782f(void*, unsigned int, int, void (__cdecl*)(void*), void (__cdecl*)(void*));
extern "C" int __cdecl FUN_00ec658f(void (__cdecl*)());

// @fnv 0x00f9ec20
void FUN_00f9ec20()
{
    FUN_00ec782f(&DAT_011dd9e8, 36, 20, FUN_0083b770, FUN_0083b7d0);
    FUN_00ec658f(FUN_00fd8c20);
}