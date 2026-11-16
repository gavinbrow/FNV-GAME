extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdcbc0();

// @fnv 0x00fb9790
extern "C" void FUN_00fb9790()
{
    atexit(FUN_00fdcbc0);
}
