extern "C" void __stdcall FUN_00ec782f(void*, unsigned int, int, void (*)(void*), void (*)(void*));
extern "C" int __cdecl FUN_00ec658f(void (*)(void));
extern "C" char DAT_011fdd88;
extern "C" void FUN_00b54620(void*);
extern "C" void FUN_00b66f20(void*);
extern "C" void FUN_00fdcd20();
// @fnv 0x00fb9b90
void FUN_00fb9b90()
{
    FUN_00ec782f(&DAT_011fdd88, 4, 156, FUN_00b54620, FUN_00b66f20);
    FUN_00ec658f(FUN_00fdcd20);
}