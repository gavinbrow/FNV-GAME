// @fnv 0x00fba890
extern "C" void __stdcall FUN_00ec782f(void*, unsigned int, int, void (__cdecl*)(void*), void (__cdecl*)(void*));
extern "C" int __cdecl FUN_00ec658f(void (__cdecl*)());
extern "C" void __cdecl FUN_00b54620(void*);
extern "C" void __cdecl FUN_0045cec0(void*);
extern "C" void __cdecl FUN_00fdd150();
extern "C" unsigned char DAT_012010c4;

extern "C" void __cdecl FUN_00fba890()
{
    FUN_00ec782f(&DAT_012010c4, 4, 10, FUN_00b54620, FUN_0045cec0);
    FUN_00ec658f(FUN_00fdd150);
}
