// @fnv 0x00fba860
extern "C" void __stdcall FUN_00ec782f(void*, unsigned int, int, void (__cdecl*)(void*), void (__cdecl*)(void*));
extern "C" int __cdecl FUN_00ec658f(void (__cdecl*)());
extern "C" void __cdecl FUN_00b54620(void*);
extern "C" void __cdecl FUN_0045cec0(void*);
extern "C" void __cdecl FUN_00fdd130();
extern "C" unsigned char DAT_01201080;

extern "C" void __cdecl FUN_00fba860()
{
    FUN_00ec782f(&DAT_01201080, 4, 17, FUN_00b54620, FUN_0045cec0);
    FUN_00ec658f(FUN_00fdd130);
}
