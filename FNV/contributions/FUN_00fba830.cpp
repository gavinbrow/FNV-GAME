extern "C" int __cdecl atexit(void (__cdecl *callback)());
extern "C" void __stdcall FUN_00ec782f(void *, unsigned int, int, void (__cdecl *)(void *), void (__cdecl *)(void *));
extern "C" void __cdecl FUN_00b54620(void *);
extern "C" void __cdecl FUN_00b79930(void *);
extern "C" void __cdecl FUN_00fdd170();
extern "C" unsigned int DAT_01200ec0;
// @fnv 0x00fba830
void __cdecl FUN_00fba830()
{
    FUN_00ec782f(&DAT_01200ec0, 4, 112, FUN_00b54620, FUN_00b79930);
    atexit(FUN_00fdd170);
}
