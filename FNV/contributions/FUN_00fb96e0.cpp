extern "C" void __stdcall FUN_00ec782f(void*, int, int, void*, void*);
extern "C" void FUN_00b54620();
extern "C" void FUN_00b66f20();
extern "C" void FUN_00fdcb40();
extern "C" int __cdecl atexit(void (__cdecl *)(void));
extern char DAT_011f9548;

// @fnv 0x00fb96e0
extern "C" void FUN_00fb96e0()
{
    FUN_00ec782f(&DAT_011f9548, 4, 35,
        reinterpret_cast<void*>(&FUN_00b54620),
        reinterpret_cast<void*>(&FUN_00b66f20));
    atexit(&FUN_00fdcb40);
}
