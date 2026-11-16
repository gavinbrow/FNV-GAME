extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdb270();

// @fnv 0x00fb65d0
extern "C" void FUN_00fb65d0()
{
    atexit(FUN_00fdb270);
}
