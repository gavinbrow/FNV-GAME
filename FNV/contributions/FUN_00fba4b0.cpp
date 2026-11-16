// @fnv 0x00fba4b0
extern "C" unsigned char DAT_012005d0;
extern "C" void __cdecl FUN_00b54620(void);
extern "C" void __cdecl FUN_00b66f20(void);
extern "C" void __cdecl FUN_00fdcf50(void);
extern "C" void __stdcall FUN_00ec782f(void*, unsigned int, int, void (__cdecl *)(void), void (__cdecl *)(void));
extern "C" int __cdecl atexit(void (__cdecl *function)(void));
extern "C" void __cdecl FUN_00fba4b0(void)
{
    FUN_00ec782f(&DAT_012005d0, 4, 4, FUN_00b54620, FUN_00b66f20);
    atexit(FUN_00fdcf50);
}
