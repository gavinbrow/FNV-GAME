extern unsigned char DAT_011cb450;
extern "C" void __cdecl FUN_0096a2d0(void*);
extern "C" void __cdecl FUN_0046ffb0(void*);
extern "C" void __cdecl FUN_00fcb280();
extern "C" void __stdcall FUN_00ec782f(void*, unsigned int, int, void (__cdecl*)(void*), void (__cdecl*)(void*));
extern "C" int __cdecl FUN_00ec658f(void (__cdecl*)());

// @fnv 0x00f51a20
void FUN_00f51a20()
{
    FUN_00ec782f(&DAT_011cb450, 8, 14, FUN_0096a2d0, FUN_0046ffb0);
    FUN_00ec658f(FUN_00fcb280);
}