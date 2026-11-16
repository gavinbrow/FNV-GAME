extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdb200();

// @fnv 0x00fb6520
void __cdecl FUN_00fb6520()
{
    atexit(FUN_00fdb200);
}
