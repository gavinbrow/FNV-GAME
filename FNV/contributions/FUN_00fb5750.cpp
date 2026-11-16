extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdaea0();

// @fnv 0x00fb5750
extern "C" void __cdecl FUN_00fb5750()
{
    atexit(FUN_00fdaea0);
}
