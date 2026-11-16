extern "C" int __cdecl atexit(void (__cdecl *callback)());
extern "C" void __stdcall FUN_00ec782f(void *, unsigned int, int, void (__cdecl *)(void *), void (__cdecl *)(void *));
extern "C" void __cdecl FUN_00b54620(void *);
extern "C" void __cdecl FUN_00b66f20(void *);
extern "C" void __cdecl FUN_00fdd110();
extern "C" unsigned int DAT_01200dd8;
// @fnv 0x00fba800
void __cdecl FUN_00fba800()
{
    FUN_00ec782f(&DAT_01200dd8, 4, 57, FUN_00b54620, FUN_00b66f20);
    atexit(FUN_00fdd110);
}
