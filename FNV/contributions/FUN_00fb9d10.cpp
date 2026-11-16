// @fnv 0x00fb9d10
extern "C" char DAT_011ff4ac[];
extern "C" void FUN_00b54620(void*);
extern "C" void FUN_0045cec0(void*);
extern "C" void FUN_00fdcdf0();
extern "C" void __stdcall FUN_00ec782f(void*, unsigned int, int, void (*)(void*), void (*)(void*));
extern "C" int __cdecl FUN_00ec658f(void (*)());
extern "C" void __cdecl FUN_00fb9d10()
{
    FUN_00ec782f(DAT_011ff4ac, 4, 6, FUN_00b54620, FUN_0045cec0);
    FUN_00ec658f(FUN_00fdcdf0);
}