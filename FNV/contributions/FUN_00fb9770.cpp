extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdcae0();

// @fnv 0x00fb9770
extern "C" void FUN_00fb9770()
{
    atexit(FUN_00fdcae0);
}
