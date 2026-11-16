extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdae50();

// @fnv 0x00fb5500
extern "C" void __cdecl FUN_00fb5500()
{
    atexit(FUN_00fdae50);
}
