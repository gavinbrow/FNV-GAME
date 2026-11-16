// @fnv 0x00fbace0
extern "C" unsigned char DAT_012022c0;
extern "C" void __cdecl FUN_00b54620(void);
extern "C" void __cdecl FUN_00b79930(void);
extern "C" void __cdecl FUN_00fdd330(void);
extern "C" void __stdcall FUN_00ec782f(void*, unsigned int, int, void (__cdecl *)(void), void (__cdecl *)(void));
extern "C" int __cdecl atexit(void (__cdecl *function)(void));
extern "C" void __cdecl FUN_00fbace0(void)
{
    FUN_00ec782f(&DAT_012022c0, 4, 26, FUN_00b54620, FUN_00b79930);
    atexit(FUN_00fdd330);
}
