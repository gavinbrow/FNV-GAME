extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdafb0();

// @fnv 0x00fb5990
extern "C" void __cdecl FUN_00fb5990()
{
    atexit(FUN_00fdafb0);
}
