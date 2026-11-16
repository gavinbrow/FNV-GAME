// @fnv 0x00fba7d0
extern "C" unsigned char DAT_01200d10;
extern "C" void __cdecl FUN_00b54620(void);
extern "C" void __cdecl FUN_00b66f20(void);
extern "C" void __cdecl FUN_00fdd0f0(void);
extern "C" void __stdcall FUN_00ec782f(void*, unsigned int, int, void (__cdecl *)(void), void (__cdecl *)(void));
extern "C" int __cdecl atexit(void (__cdecl *function)(void));
extern "C" void __cdecl FUN_00fba7d0(void)
{
    FUN_00ec782f(&DAT_01200d10, 4, 50, FUN_00b54620, FUN_00b66f20);
    atexit(FUN_00fdd0f0);
}
