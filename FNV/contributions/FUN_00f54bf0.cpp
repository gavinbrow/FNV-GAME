// @fnv 0x00f54bf0
extern "C" char DAT_011cbf60;
extern "C" void FUN_005aa0f0();
extern "C" void FUN_005aa1a0();
extern "C" void FUN_00fcb8c0();
extern "C" void __stdcall FUN_00ec782f(void*, unsigned int, int, void (*)(), void (*)());
extern "C" int __cdecl atexit(void (__cdecl *)());

void FUN_00f54bf0()
{
    FUN_00ec782f(&DAT_011cbf60, 84, 2, FUN_005aa0f0, FUN_005aa1a0);
    atexit(FUN_00fcb8c0);
}
