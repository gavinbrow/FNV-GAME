// @fnv 0x00fb9ce0
extern "C" unsigned char DAT_011ff4a0;
extern "C" void __cdecl FUN_00b54620(void);
extern "C" void __cdecl FUN_0045cec0(void);
extern "C" void __cdecl FUN_00fdcdd0(void);
extern "C" void __stdcall FUN_00ec782f(void*, unsigned int, int, void (__cdecl *)(void), void (__cdecl *)(void));
extern "C" int __cdecl atexit(void (__cdecl *function)(void));
extern "C" void __cdecl FUN_00fb9ce0(void)
{
    FUN_00ec782f(&DAT_011ff4a0, 4, 3, FUN_00b54620, FUN_0045cec0);
    atexit(FUN_00fdcdd0);
}
