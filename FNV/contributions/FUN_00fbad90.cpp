// @fnv 0x00fbad90
extern "C" unsigned char DAT_01202350;
extern "C" void __cdecl FUN_00b54620(void);
extern "C" void __cdecl FUN_00b79930(void);
extern "C" void __cdecl FUN_00fdd350(void);
extern "C" void __stdcall FUN_00ec782f(void*, unsigned int, int, void (__cdecl *)(void), void (__cdecl *)(void));
extern "C" int __cdecl atexit(void (__cdecl *function)(void));
extern "C" void __cdecl FUN_00fbad90(void)
{
    FUN_00ec782f(&DAT_01202350, 4, 30, FUN_00b54620, FUN_00b79930);
    atexit(FUN_00fdd350);
}
