extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdb000();

// @fnv 0x00fb5ae0
extern "C" void __cdecl FUN_00fb5ae0()
{
    atexit(FUN_00fdb000);
}
