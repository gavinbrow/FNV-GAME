extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdca80();

// @fnv 0x00fb9720
extern "C" void FUN_00fb9720()
{
    atexit(FUN_00fdca80);
}
