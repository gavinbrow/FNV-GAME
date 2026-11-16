extern "C" void __stdcall FUN_00ec782f(void*, unsigned int, int, void (*)(void*), void (*)(void*));
extern "C" int __cdecl FUN_00ec658f(void (*)(void));
extern "C" char DAT_011fdff8;
extern "C" void FUN_00b54620(void*);
extern "C" void FUN_00b79930(void*);
extern "C" void FUN_00fdcd80();
// @fnv 0x00fb9bc0
void FUN_00fb9bc0()
{
    FUN_00ec782f(&DAT_011fdff8, 4, 759, FUN_00b54620, FUN_00b79930);
    FUN_00ec658f(FUN_00fdcd80);
}